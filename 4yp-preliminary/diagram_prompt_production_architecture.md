# Prompt for GPT Image Generation: SharedOS Production Architecture Diagram

> Use this prompt with GPT-4o / DALL-E or a diagramming tool (Excalidraw, Figma, TikZ).

---

## Prompt (for GPT or diagram AI):

Create a clean, professional system architecture diagram for a research paper. Style: white background, thin black/dark-grey lines, blue accent color for the "Shared Execution Core", minimal text, no shadows or gradients. Layout: landscape orientation, ~1200x700px.

### Structure:

**LEFT SIDE: Four Entry Points (vertical stack)**

Four boxes on the left, each with a small icon and label:
1. 🖥️ "Owner Chat" — arrow pointing right labeled "full access"
2. 🔗 "Guest Share Link" — arrow pointing right labeled "capabilities JSONB"
3. 🤝 "Friend Agent (contact_agent)" — arrow pointing right labeled "agentPermissions row"
4. 🔌 "API RPC (/v1/agent/message)" — arrow pointing right labeled "API key → permissions"

All four arrows converge into:

**CENTER: Shared Execution Core (highlighted blue box)**

A large rounded rectangle in the center. Inside it, three stacked sub-components:

```
┌─────────────────────────────────────────────────┐
│          SHARED EXECUTION CORE                   │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │  buildStructuredSystemPrompt()            │  │
│  │  [Soul | Identity | Policy | Boundaries   │  │
│  │   | Approach | Knowledge | Relationship]  │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │  assembleToolsFromPermissions()           │  │
│  │  Domain gates + Namespace filtering       │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │  ReAct Execution Loop                     │  │
│  │  (model → tool call → result → loop)      │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Between Entry Points and Execution Core: Permission Resolution Layer**

A thin horizontal band labeled "Permission Resolution" that normalizes all four input formats into a canonical `AgentPermissions` object. Show:
- `normalizeAgentPermissions()`
- Arrow from each entry point passes through this band

**RIGHT SIDE: Data & Policy Sources (vertical stack)**

Boxes feeding INTO the execution core from the right:

1. **State Layer** (folder icon)
   - "Notes (127 files, 11 folders)"
   - "Structured State (todos, calendar, CRM)"
   - "Memory Shards"
   - Note: dashed line with label "Scoped by folderIds / MCC"

2. **Policy Documents** (document icon)
   - `/Self/POLICY.md` → "Base governance"
   - `/@{handle}/POLICY.md` → "Per-relationship override"
   - `/links/Label.md § Policy` → "Per-link rules"

3. **Contact Graph** (network icon)
   - `agentPermissions` table
   - Arrow with "REJECT" label going back left (for non-contacts)

**BELOW THE CORE: Pre-Tool Escalation Gate**

A red-outlined box sitting between the execution core and the state layer:

```
┌─────────────────────────────────────────┐
│  PRE-TOOL ESCALATION GATE               │
│                                          │
│  Tool Call → [Precedent Check]           │
│           → [LLM Sanitizer]             │
│           → CONTINUE / STOP              │
│                                          │
│  STOP → Holding response + escalation    │
│          record for owner review         │
└─────────────────────────────────────────┘
```

Arrow from "ReAct Execution Loop" going down to the gate, then from the gate going right to "State Layer". This shows: tool calls pass through the gate before reaching data.

**ANNOTATIONS:**

- Label the boundary between Entry Points and Execution Core: "Ownership Boundary"
- Label the space between Execution Core and State Layer: "Data Absence Boundary (MCC)"
- Small note at bottom: "Same execution path for all modes. Security is determined by which permissions and policies are loaded, not by separate code paths."

### Color Coding:
- Blue: Shared Execution Core
- Green: Policy/Governance documents
- Orange/Red outline: Escalation Gate
- Grey: Data/State layer
- Light purple: Entry points

### Typography:
- Function names in monospace: `buildStructuredSystemPrompt()`, `assembleToolsFromPermissions()`
- Layer labels in bold sans-serif
- Annotations in italic

---

## Alternative: Simplified Version (for thesis figure)

If the above is too complex, here's a minimal version:

```
    Owner    Guest    Friend    API
      │        │        │        │
      └────────┴────────┴────────┘
                    │
            [Permission Resolution]
                    │
         ┌──────────▼──────────┐
         │  SHARED EXECUTION   │◄──── Policy Docs
         │       CORE          │      (POLICY.md,
         │                     │       @handle/POLICY.md)
         │  System Prompt +    │
         │  Tool Assembly +    │
         │  ReAct Loop         │
         └──────────┬──────────┘
                    │
          [Escalation Gate]
            CONTINUE│STOP
                    │
         ┌──────────▼──────────┐
         │    STATE LAYER      │
         │  (MCC-scoped view)  │
         │                     │
         │  Notes │ Todos │ Cal│
         └─────────────────────┘
```

---

## Key Terms to Include in Diagram:

- SharedOS
- Shared Execution Core
- buildStructuredSystemPrompt()
- assembleToolsFromPermissions()
- ReAct Execution Loop
- Permission Resolution / normalizeAgentPermissions()
- AgentPermissions (canonical type)
- Mountable Context Cell (MCC) / capabilities JSONB
- Pre-Tool Escalation Gate
- CONTINUE / STOP
- Policy-as-Documents (POLICY.md)
- Relationship Shards (/@{handle}/)
- Contact Graph (agentPermissions table)
- Ownership Boundary
- Data Absence Boundary
- folderIds scoping
- Precedent Learning
