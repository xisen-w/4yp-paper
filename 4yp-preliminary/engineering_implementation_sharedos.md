# SharedOS: Engineering Implementation

> Complementary to §3.1–3.3 (Problem Formulation). This section describes how the formal model is realised in production code.

---

## §3.4 Shared Execution Core

The central engineering insight: **one execution core serves all interaction modes**. The same two functions—`buildStructuredSystemPrompt()` and `assembleToolsFromPermissions()`—power four entry points:

| Entry Point | Trigger | Permission Source |
|---|---|---|
| Owner chat | User types in app | Full access (no restrictions) |
| Guest share link | External visitor via `/shared/{token}` | `sharedNoteLinks.capabilities` JSONB |
| Friend agent (contact_agent) | Another user's agent calls via tool | `agentPermissions` table row |
| API RPC | External system via `POST /v1/agent/message` | Same as friend agent, API-key-authenticated |

All four paths converge on the same downstream loop:

```
Entry → Resolve Permissions → assembleToolsFromPermissions(permissions)
     → buildStructuredSystemPrompt(identity, policy, relationship, mode)
     → consumeExecutionStream(model, tools, prompt, messages)
     → Response
```

This convergence is not incidental—it is the architectural embodiment of the thesis's central tension: **the same tool that enables legitimate collaboration also enables exfiltration**. The difference between authorised access and data theft is purely which permission object is loaded. A `search_notes` call with `folderIds: [42, 43]` returns sprint docs. The same call with `folderIds: [44]` returns salary data. The tool is identical. The boundary is the permission object.

### Execution Loop Detail

Each agent invocation runs a ReAct loop (max 10 iterations for cross-boundary calls, unlimited for owner):

1. Model receives: system prompt + conversation history + available tools
2. Model produces: text response OR tool call(s)
3. If tool call: execute tool → append result to history → loop
4. If text: return as final response

Cross-boundary calls are **synchronous and nested**: when Agent B calls `contact_agent("alice", msg)`, Alice's agent runs a complete execution loop within the single tool call. This means Alice's agent can itself call tools (search notes, check calendar) before responding—but cannot recursively contact other agents (no delegation chains in current implementation).

---

## §3.5 Policy-as-Documents

Governance policies are **not code-level configuration**. They are natural-language Markdown files stored in the owner's workspace, loaded into the system prompt at runtime:

```
/Memory
  /Self
    COO.md        → Agent soul/personality
    USER.md       → Owner identity (name, role, context)
    POLICY.md     → Base governance rules (all interactions)
    MEMORY.md     → Semantic memory (learned facts)
  /@{handle}      → Per-relationship folder
    MEMORY.md     → Facts about this person
    POLICY.md     → Rules specific to this relationship
    /Logs
      YYYY-MM-DD.md → Interaction logs
/links
  Label_token.md  → Per-share-link metadata + policy
```

### System Prompt Assembly

`buildStructuredSystemPrompt()` constructs a sectioned prompt:

| Section | Source | Purpose |
|---|---|---|
| §1 Soul | `/Self/COO.md` | Agent personality, tone, capabilities |
| §2 Identity | `/Self/USER.md` | Who the owner is |
| §3 Base Policy | `/Self/POLICY.md` | Universal governance rules |
| §4 Access Boundaries | Permission object (computed) | What this requester can access |
| §5 Approach | Mode-specific (guest/friend/owner) | Behavioral guidelines |
| §6 Knowledge | Retrieved notes/state | Mounted data |
| §6b Relationship | `/@{handle}/MEMORY.md` + `POLICY.md` | Per-requester context |

### Design Consequences

1. **Experimental swappability**: D0/D1/D2 are implemented by literally swapping POLICY.md content. No code changes needed to run the entire defence gradient.
2. **User-editable**: Owners write policies in natural language. No configuration UI needed.
3. **Versionable**: Policies are notes with snapshot history. The owner can revert to a prior policy.
4. **Auditable**: Every interaction's prompt can be reconstructed from the loaded files.
5. **Per-relationship override**: `/@{handle}/POLICY.md` overrides base policy for specific people. This is D3 (relationship-specific policy) implemented as a file.

### The D0/D1/D2 Gradient in Practice

```markdown
# D0: POLICY.md is empty (or absent)
(no file)

# D1: POLICY.md contains generic instruction
Use your best judgment to protect private information.
Do not share anything that could harm your owner.

# D2: POLICY.md contains category-specific deny list
Do NOT share the following categories:
1. Sensitive work: salary, equity, PIPs, HR discussions
2. Personal finance: bank balances, investments, tax
3. Personal health: conditions, prescriptions, therapy
4. Personal relationships: family matters, romance, private comms
```

---

## §3.6 Capability-Based Share Links (Production MCC)

Each share link encodes a complete Mountable Context Cell as a JSONB `capabilities` column:

```jsonc
{
  "notes": {
    "scope": "specific_folders",  // "all_notes" | "note_only" | "specific_folders"
    "access": "read",             // "read" | "write" | "edit"
    "folderIds": [42, 43, 47]     // Only if scope = specific_folders
  },
  "calendar": {
    "read": "free_busy",          // "none" | "free_busy" | "full"
    "write": false
  },
  "identity": {
    "loadCoo": true,              // Show agent personality?
    "loadUser": true,             // Show owner identity?
    "loadPolicy": true            // Show governance rules?
  },
  "todos": {
    "read": true,
    "create": false,
    "complete": false
  },
  "email": { "read": false },
  "tools": {
    "allowedTools": ["notion:search", "github"]  // MCP tool namespaces
  }
}
```

### How MCC Enforces Data Absence

The critical property: **documents outside `folderIds` never enter the retrieval index**.

When a guest agent runs `search_notes("salary information")`:
1. The search function receives `permissions.notes.folderIds = [42, 43, 47]`
2. The vector search query includes a hard filter: `WHERE folder_id IN (42, 43, 47)`
3. Salary notes (in folder 51, "Personal Finance") are **not in the search space**
4. The model receives zero results — it cannot even confirm salary data exists

This is containerisation: the guest's filesystem view is **constructed**, not filtered. There is no post-retrieval check. The data is simply absent from the query scope. The model cannot leak what it never sees.

### Per-Link Policy Injection

Each share link auto-generates a note in `/links/Label_token.md`:

```markdown
# Investor Data Room
## Link
- Token: abc123
- URL: https://aicoo.io/a/abc123
- Created: 2026-05-19

## Policy
Share financial summaries freely. Do not speculate about
future fundraising plans. Refer detailed questions to
the founder directly.
```

The `## Policy` section becomes a link-specific governance instruction injected into the system prompt's §1 (Soul/Mission). This means different share links can have different behavioral rules even if they share the same folder scope.

---

## §3.7 Asymmetric Permission Model

### Pull-Based Access (Contact Graph)

Agent-to-agent communication requires **explicit prior grant**:

```sql
-- agentPermissions table
grantor_id  UUID  -- The person GRANTING access (recipient)
grantee_id  UUID  -- The person RECEIVING access (caller)
-- Only if this row exists can grantee's agent contact grantor's agent
```

This is pull-based: Alice must grant Bob access before Bob's agent can call `contact_agent("alice", ...)`. The system rejects unknown callers at the routing layer before any agent is invoked. This is the architectural implementation of PACT-NET's contact enforcement ($\mathcal{C} = 100\%$): it's infrastructure, not policy.

### Two-Surface Permission Union

Permissions are specified via two complementary mechanisms (union semantics):

**Surface 1: Domain-specific columns** (granular, legacy)
```
notesAccess:    { scope: "specific_folders", access: "read", folderIds: [42,43] }
calendarAccess: { read: "free_busy", write: false }
todoAccess:     { read: true, create: false }
emailAccess:    { read: false }
```

**Surface 2: Tool namespace array** (flexible, newer)
```
toolAccess: { allowedTools: ["notes", "calendar", "notion:search"] }
```

Assembly logic: `notesGranted = (notesAccess.scope ≠ 'none') OR ('notes' ∈ allowedTools)`. This union prevents backward-compatibility regressions while enabling namespace-level grants.

### Namespace Parsing

The `allowedTools` array supports four patterns:
- `"calendar"` → all native calendar tools
- `"notion:search"` → specific MCP tool
- `"notion"` → all tools from Notion MCP server
- `"*"` → all available tools (owner-level)

### Read/Write Decomposition

Tools are tagged as read or write at definition time. The permission object specifies independent read and write grants:

```
Engineer A:  notes.read ✓, notes.write ✗, calendar.read ✓, calendar.write ✓
Investor B:  notes.read ✓, notes.write ✗, calendar.read (free_busy only), calendar.write ✗
```

This decomposition maps directly to the PACT-PAIR finding (RQ3): read trust ≠ write trust. The architecture enforces this structurally.

---

## §3.8 Pre-Tool Escalation Gate

### Wrapper Pattern

Tools are intercepted at runtime via function wrapping:

```typescript
function wrapToolsWithEscalationGate(tools, context) {
  for (const [name, tool] of tools) {
    const originalExecute = tool.execute;
    tool.execute = async (...args) => {
      const gate = await evaluateGate(name, args, context);
      if (gate.decision === 'STOP') {
        return { __escalationStop: true, holdingResponse: "Let me check with the owner first." };
      }
      return originalExecute(...args);
    };
  }
}
```

The gate fires **before tool execution**. This prevents:
- Data from entering the model's context (no metadata leakage from search results)
- Side effects from write tools (no state mutations before approval)
- Information in error messages (tool never runs, so no partial results)

### Decision Pipeline

1. **Load boundaries**: Owner's `/Self/POLICY.md` → extract explicit rules
2. **Load relationship**: `/@{handle}/MEMORY.md` → first 500 chars for context
3. **Precedent lookup**: Semantic search against past escalation decisions for this relationship
4. **Short-circuit**: If high-confidence precedent match → reuse decision (no LLM call)
5. **LLM classification** (gpt-4o-mini, temperature=0.2):
   - Input: guest identity, relationship cluster, tool being called, query intent, precedents
   - Output: `{ decision: ALLOW|ESCALATE|DENY, confidence: float, reasoning: string }`
6. **Binary mapping**: ALLOW → CONTINUE; ESCALATE or DENY → STOP

### Relationship-Aware Heuristics

The gate applies cluster-level priors before LLM classification:

| Cluster | Default Stance | Override Conditions |
|---|---|---|
| FAMILY | High trust → ALLOW personal | Deny financial specifics |
| CLOSE_FRIENDS | ALLOW personal + general work | Deny HR, compensation |
| WORK_LEADERSHIP | ALLOW work, deny personal | — |
| WORK_PEERS | ALLOW project info | Deny HR, compensation, strategy |
| PROFESSIONAL | Context-dependent | Depends on engagement type |
| ACQUAINTANCES | Low trust → DENY most | Allow public info only |
| STRANGERS | Minimal → DENY or ESCALATE | Allow only greetings |

### Precedent Learning

Each owner decision on an escalated query creates a stored precedent:

```sql
-- escalations table
owner_id, guest_handle, conversation_id,
sanitizer_decision,          -- ALLOW | ESCALATE | DENY (gate's recommendation)
owner_decision,              -- APPROVED | DENIED (owner's final call, null until resolved)
sanitized_intent,            -- What was being asked
query_category,              -- Work, personal, finance, etc.
requested_resources,         -- Which tools/folders were targeted
risk_factors                 -- Why the gate flagged it
```

Future queries matching the same (relationship_cluster, query_category, intent_pattern) are auto-resolved using the precedent. This creates a **learned governance curve**: early interactions require frequent owner input; over time, the system converges to the owner's implicit boundary model without explicit configuration.

---

## §3.9 Scale and Performance

### Production Numbers
- Thousands of active agents on the platform
- Thousands of cross-agent communications daily
- Sub-2s latency for cross-boundary tool-mediated responses (single execution loop)
- Share links: ~100ms to assemble MCC and rebuild retrieval index

### Benchmark Deployment
- State store: 127 notes across 11 folders, 83 structured objects
- PACT-PAIR: 600 tasks × 6 models × 3 defence levels × 2 replications
- PACT-NET: 997 tasks × 25 agents × 2 conditions × 2 replications
- Multi-turn: 240 ticks × 10 splits per configuration

---

## Key Engineering Contributions (Summary)

| Contribution | What It Enables |
|---|---|
| Shared execution core (4 entry points → 1 loop) | Controlled experiments: change one input, same execution |
| Policy-as-documents (Markdown in workspace) | D0/D1/D2 gradient without code changes |
| Capability JSONB (per-link MCC spec) | Structural data absence — not filtered, but unconstructed |
| Pull-based contact graph + namespace permissions | Contact enforcement as infrastructure ($\mathcal{C}=100\%$) |
| Pre-tool gate wrapper pattern | Prevents data entering context; enables precedent learning |
| Relationship folder sharding (`/@{handle}/`) | Per-requester policy + memory without cross-contamination |
