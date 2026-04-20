#!/usr/bin/env python3
"""
Daily Reflection Tree Agent
Part B of the DT Fellowship Assignment.
 
Loads the reflection tree from reflection-tree.json and walks the employee
through a fully deterministic conversation. No LLM is called at runtime.
All branching is based on lookup + string matching.
 
Usage:
    python agent.py                         # uses reflection-tree.json in same folder
    python agent.py --tree path/to/tree.json
"""
 
import json
import sys
import os
import textwrap
import time
from argparse import ArgumentParser
 
# ─────────────────────────────────────────────
# GUARDRAILS AGAINST HALLUCINATION / BAD DATA
# ─────────────────────────────────────────────
# Since the tree is loaded from a JSON file, we validate it rigorously
# before running, so no missing node references, invalid types, or broken
# routing can cause undefined behavior at runtime.
 
VALID_NODE_TYPES = {"start", "question", "decision", "reflection", "bridge", "summary", "end"}
REQUIRED_FIELDS = {"id", "type", "text", "options", "target", "signal"}
 
 
def validate_tree(nodes: list[dict]) -> None:
    """
    Guardrail: Validate the tree data before any execution.
    Raises ValueError with a descriptive message if the tree is malformed.
    This prevents hallucinated or corrupted JSON from causing runtime surprises.
    """
    node_ids = {n["id"] for n in nodes}
    errors = []
 
    for node in nodes:
        nid = node.get("id", "<unknown>")
 
        # Check all required fields exist
        for field in REQUIRED_FIELDS:
            if field not in node:
                errors.append(f"Node '{nid}' is missing field '{field}'")
 
        # Check type is valid
        if node.get("type") not in VALID_NODE_TYPES:
            errors.append(f"Node '{nid}' has invalid type '{node.get('type')}'")
 
        # Check target references exist (if set)
        if node.get("target") and node["target"] not in node_ids:
            errors.append(f"Node '{nid}' has target '{node['target']}' which does not exist")
 
        # Decision nodes must have routing rules in options
        if node.get("type") == "decision":
            for rule in node.get("options", []):
                if ":" not in rule:
                    errors.append(f"Decision node '{nid}' has malformed routing rule: '{rule}'")
                else:
                    destination = rule.split(":")[-1]
                    if destination not in node_ids:
                        errors.append(f"Decision node '{nid}' routes to '{destination}' which does not exist")
 
    if errors:
        raise ValueError("Tree validation failed:\n" + "\n".join(f"  ✗ {e}" for e in errors))
 
    print(f"  ✓ Tree validated: {len(nodes)} nodes, all references intact.\n")
 
 
# ─────────────────────────────────────────────
# INTERPOLATION
# ─────────────────────────────────────────────
 
def interpolate(text: str, state: dict) -> str:
    """
    Replace {NODE_ID.answer} and {axis1.dominant} etc. placeholders with
    actual values from state. If a placeholder can't be resolved, leave it
    literally — never crash or invent a value (anti-hallucination guardrail).
    """
    import re
    pattern = re.compile(r"\{([^}]+)\}")
 
    def replace(match):
        key = match.group(1)
        # Try state["answers"][node_id]
        if "." in key:
            parts = key.split(".", 1)
            section, field = parts[0], parts[1]
            if section == "axis1" and field == "dominant":
                return compute_dominant(state, "axis1")
            if section == "axis2" and field == "dominant":
                return compute_dominant(state, "axis2")
            if section == "axis3" and field == "dominant":
                return compute_dominant(state, "axis3")
            # NODE_ID.answer
            node_id = section
            if node_id in state.get("answers", {}):
                return state["answers"][node_id]
        # Direct key lookup
        if key in state.get("answers", {}):
            return state["answers"][key]
        # Fallback — return placeholder unchanged (safe, honest)
        return match.group(0)
 
    return pattern.sub(replace, text)
 
 
def compute_dominant(state: dict, axis: str) -> str:
    """Return the dominant pole label for a given axis based on signal tallies."""
    signals = state.get("signals", {})
    if axis == "axis1":
        internal = signals.get("axis1:internal", 0)
        external = signals.get("axis1:external", 0)
        return "internally (with agency)" if internal >= external else "externally (circumstance-focused)"
    if axis == "axis2":
        contrib = signals.get("axis2:contribution", 0)
        entitle = signals.get("axis2:entitlement", 0)
        return "toward contribution" if contrib >= entitle else "toward entitlement"
    if axis == "axis3":
        altro = signals.get("axis3:altrocentric", 0)
        self_ = signals.get("axis3:self", 0)
        return "altrocentrically (beyond yourself)" if altro >= self_ else "self-centrically (close focus)"
    return axis
 
 
def resolve_summary_reflection(state: dict) -> str:
    """Pick the best matching summary template based on signal tallies."""
    a1 = "internal" if state["signals"].get("axis1:internal", 0) >= state["signals"].get("axis1:external", 0) else "external"
    a2 = "contribution" if state["signals"].get("axis2:contribution", 0) >= state["signals"].get("axis2:entitlement", 0) else "entitlement"
    a3 = "altrocentric" if state["signals"].get("axis3:altrocentric", 0) >= state["signals"].get("axis3:self", 0) else "self"
    key = f"{a1}_{a2}_{a3}"
    templates = state.get("_summary_templates", {})
    return templates.get(key, "Every day is information. See you tomorrow.")
 
 
# ─────────────────────────────────────────────
# ROUTING
# ─────────────────────────────────────────────
 
def resolve_decision(node: dict, state: dict) -> str:
    """
    Parse decision node routing rules and return the target node ID.
    Rule format: "answer=OPT1|OPT2:TARGET_ID"
    Guardrail: if no rule matches, raise clearly — never silently skip.
    """
    last_answer = state.get("last_answer", "")
    for rule in node["options"]:
        condition, target = rule.rsplit(":", 1)
        # Parse condition: "answer=OPT1|OPT2"
        if condition.startswith("answer="):
            allowed = condition[len("answer="):].split("|")
            if last_answer in allowed:
                return target.strip()
    raise RuntimeError(
        f"Decision node '{node['id']}': no rule matched for answer='{last_answer}'.\n"
        f"Rules: {node['options']}\n"
        f"This is a tree design error — every answer must be handled."
    )
 
 
def find_next_node(current_node: dict, nodes_by_id: dict, state: dict) -> str | None:
    """
    Determine the ID of the next node after the current one.
    Priority: explicit target > decision routing > first child in tree.
    """
    if current_node["type"] == "decision":
        return resolve_decision(current_node, state)
    if current_node.get("target"):
        return current_node["target"]
    # Find children: nodes whose parentId matches current node's id
    children = [n for n in nodes_by_id.values() if n.get("parentId") == current_node["id"]]
    if children:
        return children[0]["id"]
    return None  # End of tree
 
 
# ─────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────
 
WIDTH = 70
 
def hr():
    print("─" * WIDTH)
 
def print_wrapped(text: str, indent: int = 0):
    prefix = " " * indent
    for line in text.splitlines():
        wrapped = textwrap.fill(line, width=WIDTH - indent, initial_indent=prefix, subsequent_indent=prefix)
        print(wrapped)
 
def slow_print(text: str, delay: float = 0.01):
    """Print character by character for a conversational feel."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
 
def prompt_choice(options: list[str]) -> str:
    """Show numbered options and return the chosen option text."""
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")
    print()
    while True:
        raw = input("  Your choice (number): ").strip()
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        print(f"  ⚠ Please enter a number between 1 and {len(options)}.")
 
 
# ─────────────────────────────────────────────
# MAIN AGENT LOOP
# ─────────────────────────────────────────────
 
def run_session(tree_path: str):
    # Load
    with open(tree_path, "r", encoding="utf-8") as f:
        tree_data = json.load(f)
 
    nodes = tree_data["nodes"]
 
    # Guardrail: validate before any execution
    print("\nValidating tree structure...")
    validate_tree(nodes)
 
    nodes_by_id = {n["id"]: n for n in nodes}
 
    # Session state
    state = {
        "answers": {},          # node_id → answer text
        "signals": {},          # "axis1:internal" → count
        "last_answer": None,
        "_summary_templates": tree_data["nodes"][-2].get("summary_templates", {})  # pulled from SUMMARY node
    }
 
    # Find SUMMARY node's templates
    for n in nodes:
        if n["type"] == "summary" and "summary_templates" in n:
            state["_summary_templates"] = n["summary_templates"]
 
    # Find start node
    start_nodes = [n for n in nodes if n["type"] == "start"]
    if not start_nodes:
        raise RuntimeError("No 'start' node found in tree.")
    current_id = start_nodes[0]["id"]
 
    # Session header
    print()
    hr()
    print("  DAILY REFLECTION TREE".center(WIDTH))
    print("  End-of-Day Check-In".center(WIDTH))
    hr()
    print()
 
    visited = set()  # Infinite loop guard (anti-hallucination guardrail)
 
    while current_id:
        if current_id in visited:
            raise RuntimeError(f"Infinite loop detected at node '{current_id}'. Tree design error.")
        visited.add(current_id)
 
        node = nodes_by_id.get(current_id)
        if not node:
            raise RuntimeError(f"Node '{current_id}' referenced but not found in tree. Tree design error.")
 
        ntype = node["type"]
        text = interpolate(node.get("text") or "", state)
 
        # Accumulate signal
        if node.get("signal"):
            sig = node["signal"]
            state["signals"][sig] = state["signals"].get(sig, 0) + 1
 
        if ntype == "start":
            slow_print(f"\n  {text}")
            print()
            time.sleep(0.5)
 
        elif ntype == "question":
            hr()
            print()
            print_wrapped(text, indent=2)
            print()
            answer = prompt_choice(node["options"])
            state["answers"][current_id] = answer
            state["last_answer"] = answer
            print()
 
        elif ntype == "decision":
            # Invisible to user — pure routing
            state["last_answer"] = state.get("last_answer", "")
 
        elif ntype in ("reflection", "bridge"):
            print()
            if ntype == "reflection":
                print("  ✦ " + "─" * (WIDTH - 4))
            print_wrapped(text, indent=4)
            if ntype == "reflection":
                print("  ✦ " + "─" * (WIDTH - 4))
                input("\n  [Press Enter to continue]\n")
            else:
                print()
                time.sleep(0.8)
 
        elif ntype == "summary":
            # Resolve the summary_reflection placeholder
            state["answers"]["summary_reflection"] = resolve_summary_reflection(state)
            text = interpolate(text, state)
            hr()
            print()
            print("  TODAY'S REFLECTION".center(WIDTH))
            print()
            print_wrapped(text, indent=2)
            print()
            hr()
            input("\n  [Press Enter to close the session]\n")
 
        elif ntype == "end":
            print()
            slow_print(f"  {text}")
            print()
            break
 
        # Advance
        next_id = find_next_node(node, nodes_by_id, state)
        current_id = next_id
 
    hr()
    print()
 
 
# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
 
if __name__ == "__main__":
    parser = ArgumentParser(description="Daily Reflection Tree Agent")
    parser.add_argument(
        "--tree",
        default=os.path.join(os.path.dirname(__file__), "..", "tree", "reflection-tree.json"),
        help="Path to the reflection tree JSON file"
    )
    args = parser.parse_args()
 
    if not os.path.exists(args.tree):
        print(f"Error: tree file not found at '{args.tree}'")
        sys.exit(1)
 
    try:
        run_session(args.tree)
    except KeyboardInterrupt:
        print("\n\n  Session ended early. See you tomorrow.\n")
    except (RuntimeError, ValueError) as e:
        print(f"\n  ⛔ Error: {e}\n")
        sys.exit(1)
 
