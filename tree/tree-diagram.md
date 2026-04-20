flowchart TD
    START([🌙 START\nGood evening...]) --> A1_OPEN

    A1_OPEN[Q: One word for today?\nProductive / Challenging / Frustrating / Mixed]
    A1_OPEN --> A1_D1{Decision}

    A1_D1 -- Productive / Mixed --> A1_Q_AGENCY_HIGH[Q: What drove things going well?\nPrepared / Adapted / Luck / Team]
    A1_D1 -- Challenging / Frustrating --> A1_Q_AGENCY_LOW[Q: Hard moment — first instinct?\nControl / Wait / Push / Stuck]

    A1_Q_AGENCY_HIGH --> A1_D2{Decision}
    A1_Q_AGENCY_LOW --> A1_D2B{Decision}

    A1_D2 -- Prepared / Adapted --> A1_Q2_INTERNAL
    A1_D2 -- Luck / Team --> A1_Q2_EXTERNAL
    A1_D2B -- Control / Push --> A1_Q2_INTERNAL
    A1_D2B -- Wait / Stuck --> A1_Q2_EXTERNAL

    A1_Q2_INTERNAL[Q: When things went wrong, mind went to?\nChange / Missed / Responsible / Why me]
    A1_Q2_EXTERNAL[Q: What would have made it different?\nActed sooner / Others / Fairer / Info]

    A1_Q2_INTERNAL --> A1_D3{Decision}
    A1_Q2_EXTERNAL --> A1_D3B{Decision}

    A1_D3 -- Change / Missed --> A1_R_INT
    A1_D3 -- Responsible / Why me --> A1_R_EXT
    A1_D3B -- Acted sooner / Info --> A1_R_INT
    A1_D3B -- Others / Fairer --> A1_R_EXT

    A1_R_INT[💡 Reflection: You see your agency\n— curious about what you controlled]
    A1_R_EXT[💡 Reflection: Attention pulled outward\n— find the one choice you made]

    A1_R_INT --> BRIDGE_1_2
    A1_R_EXT --> BRIDGE_1_2

    BRIDGE_1_2([🌉 BRIDGE: Axis 1 → 2\nShift from how you responded\nto what you gave])

    BRIDGE_1_2 --> A2_OPEN[Q: Best describes a moment today?\nHelped unprompted / Deserved more / Did unnoticed work / Frustrated by others]

    A2_OPEN --> A2_D1{Decision}
    A2_D1 -- Helped / Unnoticed --> A2_Q_CONTRIB[Q: What drove that extra effort?\nNeeded / Right for project / No one else / Felt good]
    A2_D1 -- Deserved more / Frustrated --> A2_Q_ENTITLE[Q: What would have made it right?\nAcknowledgment / Public credit / Reward / Others doing more]

    A2_Q_CONTRIB --> A2_Q2[Q: What were you thinking about more today?\nContribute / Fairly measured / Team / My growth]
    A2_Q_ENTITLE --> A2_Q2B[Q: Did you give something that surprised you?\nStepped up / More than required / Stuck to expected / No]

    A2_Q2 --> A2_D2{Decision}
    A2_Q2B --> A2_D2B{Decision}

    A2_D2 -- Contribute / Team --> A2_R_CONTRIB
    A2_D2 -- Measured / Growth --> A2_R_ENTITLE
    A2_D2B -- Stepped up / More than required --> A2_R_CONTRIB
    A2_D2B -- Expected / No --> A2_R_ENTITLE

    A2_R_CONTRIB[💡 Reflection: You gave discretionary effort\n— that's how cultures are built]
    A2_R_ENTITLE[💡 Reflection: Wanting recognition is human\n— notice the ratio: give vs receive]

    A2_R_CONTRIB --> BRIDGE_2_3
    A2_R_ENTITLE --> BRIDGE_2_3

    BRIDGE_2_3([🌉 BRIDGE: Axis 2 → 3\nFrom what you gave\nto how wide your circle was])

    BRIDGE_2_3 --> A3_OPEN[Q: Biggest challenge — who came to mind?\nJust me / My team / A colleague / Customers]

    A3_OPEN --> A3_D1{Decision}
    A3_D1 -- Just me --> A3_Q_SELF[Q: Did you notice someone else struggling?\nYes + acted / Yes + too busy / No bandwidth / No, all fine]
    A3_D1 -- Team / Colleague / Customer --> A3_Q_OTHER[Q: What did you do with that awareness?\nActed / Checked in / Kept to own work / Shared with others]

    A3_Q_SELF --> A3_D2{Decision}
    A3_Q_OTHER --> A3_D2B{Decision}

    A3_D2 -- Yes + acted --> A3_R_ALTROCENTRIC
    A3_D2 -- Too busy / No bandwidth / All fine --> A3_R_SELF
    A3_D2B -- Acted / Checked in / Shared --> A3_R_ALTROCENTRIC
    A3_D2B -- Kept to own work --> A3_R_SELF

    A3_R_ALTROCENTRIC[💡 Reflection: You transcended your frame\n— Maslow's self-transcendence in action]
    A3_R_SELF[💡 Reflection: Energy stayed close today\n— one moment of looking up is enough]

    A3_R_ALTROCENTRIC --> SUMMARY
    A3_R_SELF --> SUMMARY

    SUMMARY[📋 SUMMARY\nAxis 1: {axis1.dominant}\nAxis 2: {axis2.dominant}\nAxis 3: {axis3.dominant}\n+ Personalized reflection template]

    SUMMARY --> END([✨ END\nRest well. See you tomorrow.])

    style START fill:#4a90d9,color:#fff
    style END fill:#4a90d9,color:#fff
    style BRIDGE_1_2 fill:#f0a500,color:#fff
    style BRIDGE_2_3 fill:#f0a500,color:#fff
    style SUMMARY fill:#27ae60,color:#fff
    style A1_R_INT fill:#8e44ad,color:#fff
    style A1_R_EXT fill:#8e44ad,color:#fff
    style A2_R_CONTRIB fill:#8e44ad,color:#fff
    style A2_R_ENTITLE fill:#8e44ad,color:#fff
    style A3_R_ALTROCENTRIC fill:#8e44ad,color:#fff
    style A3_R_SELF fill:#8e44ad,color:#fff
