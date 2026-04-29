# Infrastructure: The Personal Agent Operating System

## 1. Why "Operating System"

A personal agent is not a chatbot with a system prompt.
It is a software principal that acts on behalf of a human — reading their files, managing their schedule, spending their social capital when it messages someone on their behalf.
The moment an agent can *read* a user's private notes, *write* to their todo list, *send* messages in their name, and *talk to other agents* representing other humans, it is no longer a language model application.
It is an operating system — one where the "processes" are LLM reasoning loops and the "syscalls" are tool invocations over structured personal data.

Pulse implements this OS.
Each user owns a private data store (notes, todos, calendar events, emails) behind AES-256-GCM column-level encryption.
Each user's agent is granted a set of tools — the equivalent of file descriptors — scoped by per-relationship access-control permissions.
When Agent A contacts Agent B, Agent B's tool access is dynamically assembled from the permissions that User B has granted to User A: read-only notes, no calendar, no email, etc.
This is the system our cross-boundary privacy experiments run on.
It is not a simulation. It is a deployed, production-grade multi-agent system where real data and real permissions are at stake.

---

## 2. Core Tools

The OS exposes 45 tools across 9 domains. The three domains central to our experiments — **notes**, **todos**, and **agent communication** — are detailed below. The remaining domains (email, calendar, projects, web, external apps) are summarized in §2.4.

Every tool is defined as a Vercel AI SDK `tool()` with a Zod parameter schema, a natural-language description (consumed by the LLM during tool-use), and an `execute()` handler that runs server-side TypeScript against the database.

### 2.1 Notes Management

The user's primary knowledge store. Notes are organized in hierarchical folders, encrypted at rest, and searchable via LLM-powered multi-query expansion. In our experiments, Alex's notes contain all 200 ground-truth facts — work projects, financial records, medical history, relationship details — organized across folders that mirror real personal data.

| Tool | Parameters | Behavior |
|------|-----------|----------|
| `search_notes` | `query`, `folderName?` | AI-powered semantic search. The LLM generates 3–5 query variations from the input (e.g., "Q4 team building" → "fourth quarter offsite", "team event October"). Each variation runs against decrypted title/content. Results are deduplicated, ranked by relevance, and returned with 800-char contextual previews centered on the match. |
| `get_note_content` | `noteId` | Retrieves the full decrypted content of a note by ID. Used after `search_notes` returns truncated previews — the agent calls this to read the complete document. |
| `create_note` | `title`, `content`, `folderId?`, `folderName?` | Creates a new note. Auto-detects format (plain/markdown/HTML), wraps plain text in HTML for rendering. Stores encrypted. |
| `edit_note` | `id?`, `searchTitle?`, `title?`, `content?`, `folderName?`, `pinned?` | Updates an existing note by ID or title search. Creates a backup snapshot before overwriting (version control). |
| `pin_note` | `id?`, `searchTitle?`, `pinned` | Pins or unpins a note to the top of the list. |
| `memory_search` | `query` | Searches the user's structured memory — agent-curated summaries of past decisions, preferences, and context. Distinct from notes: memory is what the agent remembers, notes are what the human wrote. |

**Snapshot subsystem** (version control for notes):

| Tool | Parameters | Behavior |
|------|-----------|----------|
| `list_snapshots` | `noteId` | Lists all saved versions of a note, newest first. |
| `save_snapshot` | `noteId` | Manually saves current state. Auto-snapshots also occur on every `edit_note` call. |
| `restore_snapshot` | `noteId`, `snapshotId` | Restores a note to a previous version. Automatically backs up the current state first. |

**Source**: `lib/ai/tools/notes-management.ts`, `lib/ai/tools/snapshot-management.ts`, `lib/ai/tools/memory-management.ts`

### 2.2 Todo Management

Task tracking with priority levels, decomposed steps, due dates, and AI automation workflows.

| Tool | Parameters | Behavior |
|------|-----------|----------|
| `create_todo` | `title`, `description?`, `dueDate?`, `steps?`, `priority?`, `isRecurring?`, `aiWorkflow?` | Creates a todo item. Defaults due date to today. Priority: 0 (low), 1 (medium), 2 (high). Supports AI-automated recurring workflows — multi-step tool chains that execute on a schedule (e.g., "search last week's emails and create a summary note every Monday"). |
| `complete_todo` | `id?`, `searchTitle?` | Marks a todo as done. Finds by exact ID or fuzzy title search over decrypted titles. |
| `edit_todo` | `id?`, `searchTitle?`, `title?`, `description?`, `dueDate?`, `priority?`, `completed?` | Updates any todo field. Title search uses in-memory matching on decrypted values. |
| `search_todos` | `q?`, `date?`, `completed?`, `priorityMin?`, `includeOverdue?`, `includeSteps?`, `sortBy?` | Keyword search with relevance scoring across titles, descriptions, and step titles. Supports filtering by date, priority, and completion status. All keyword matching happens in-memory after decryption. |
| `replan_overdue` | `strategy?`, `maxPerDay?`, `dryRun?` | Reschedules all overdue incomplete todos. Strategy `today` moves everything to today; `spread` distributes across future days weighted by priority and step count. Supports dry-run preview. |

**Source**: `lib/ai/tools/todo-management.ts`, `lib/ai/tools/handlers/todos/*.ts`

### 2.3 Agent Communication

The tools that enable multi-agent interaction — the mechanism through which cross-boundary privacy questions arise.

| Tool | Parameters | Behavior |
|------|-----------|----------|
| `search_pulse_contact` | `name` | Searches the user's contact network (friends + agent connections) by name. Returns Pulse user IDs for messaging. |
| `send_message_to_human` | `recipientId`, `content` | Sends an in-app message to a human. Fire-and-forget: drops the message in the recipient's inbox and returns immediately. The recipient reads it in their own time. |
| `contact_agent` | `to`, `message`, `intent?` | **Agent-to-agent RPC.** Sends a message to another user's agent, waits for a full reasoning-loop response, and returns it as a tool result. The recipient agent runs with the permissions that its owner granted to the sender — dynamically scoped at call time. Intent is one of `query`, `update`, `request`, `notify`. One message in, one response out — no infinite loops. |

`contact_agent` is the critical tool for our experiments. When Tina's agent calls `contact_agent(to="alex", message="What is Alex's credit score?")`, it triggers a complete agent execution on Alex's side: system prompt assembly, tool loading with permission scoping, multi-step reasoning, note search, content retrieval, and response composition. The privacy question lives entirely in what Alex's agent decides to include in that response.

**Source**: `lib/ai/tools/agent-network.ts`, `lib/ai/tools/messaging.ts`

### 2.4 Additional State Domains

Beyond the three core domains, the OS manages several additional categories of personal data. These are not directly involved in our current experiments (which focus on note-stored information accessed via `contact_agent`), but they complete the picture of what a personal agent OS manages and protects.

| Domain | Tools | What it manages |
|--------|-------|----------------|
| **Email** (7 tools) | `search_emails`, `send_email`, `send_multiple_emails`, `save_email_draft`, `specific_email_investigate`, `search_contact`, `email_enrich` | Full email lifecycle — search inbox, draft/send messages, find contact addresses, enrich with professional data. Connected to the user's real email account via OAuth. |
| **Calendar** (5 tools) | `search_calendar_events`, `create_calendar_event`, `edit_calendar_event`, `extract_calendar_event_details`, `schedule_meeting` | Event management with natural-language parsing, time-range queries, and auto-conferencing (Google Meet / Microsoft Teams). |
| **Projects** (6 tools) | `create_project`, `list_projects`, `search_projects`, `add_project_rows`, `edit_project`, `delete_project` | Structured data tables (lightweight Airtable). AI generates the column schema from a goal description; the agent populates and queries rows. |
| **Web** (2 tools) | `web_search`, `read_url` | Web search with query optimization and time filtering; URL content extraction via Jina Reader. |
| **External Apps** (5 tools) | `COMPOSIO_SEARCH_TOOLS`, `COMPOSIO_MANAGE_CONNECTIONS`, `COMPOSIO_MULTI_EXECUTE_TOOL`, `COMPOSIO_REMOTE_WORKBENCH`, `COMPOSIO_REMOTE_BASH_TOOL` | Meta-tools that connect to 800+ external apps (GitHub, Twitter/X, Slack, etc.) via OAuth through the Composio platform. Enables the agent to post tweets, create GitHub issues, send Slack messages, etc. |

Each of these domains follows the same architecture: encrypted storage, permission-scoped access, and tools loaded dynamically per agent invocation. They represent the full surface area of personal data that a deployed agent OS must protect — our experiments focus on notes because they are the richest and most heterogeneous data source, but the privacy challenge extends to every domain.

---

## 3. The OS Abstraction

### 3.1 Kernel: Tool Assembly Pipeline

The function `createFlatToolsWithContext(userId, timezone, onStatusUpdate?, options?)` is the kernel's `exec()`.

It does four things:
1. **Loads internal tools** — notes, todos, email, calendar, projects, messaging, web — instantiated with the user's ID as the security principal.
2. **Loads external tools** — discovers MCP servers registered to the user, fetches their tool schemas, flattens into the same namespace.
3. **Applies access control** — when running in a shared/agent context (e.g., Agent B processing a `contact_agent` request from Agent A), tools are filtered by the permissions the owner granted: `notesAccess`, `todoAccess`, `calendarAccess`, `emailAccess` each with independent read/write scope.
4. **Wraps tools** — adds status callbacks for UI updates, enforces a 128-tool hard limit.

The result is a flat `Record<string, Tool>` that the Vercel AI SDK feeds directly into `generateText()` or `streamText()` as the tool-use context.

**Source**: `lib/ai/tools/index.ts`

### 3.2 File System: Encrypted Personal Data

All personal data — note titles, note content, todo titles, todo descriptions — is stored as AES-256-GCM encrypted columns via Drizzle ORM custom types.

The encryption is transparent to the application layer: Drizzle's `toDriver()` encrypts on write, `fromDriver()` decrypts on read. But it is *opaque* to the database layer: SQL operators like `ILIKE`, `LIKE`, `=` match against ciphertext and cannot perform text search. All keyword search must happen in-memory after decryption.

This has a concrete consequence for tool design: `search_todos` fetches all rows for the user, decrypts in the ORM layer, then filters in TypeScript. `search_notes` uses LLM-powered query expansion because the same constraint applies — there is no database-level full-text index over plaintext.

**Source**: `lib/db/encryption/encryption.ts`, `lib/db/encryption/encryptionTypes.ts`

### 3.3 Process Model: Agent Reasoning Loops

Each agent invocation is a bounded reasoning loop:

```
System prompt + tools + user message
  → LLM generates text or tool_calls
  → Tool results fed back
  → Repeat (max N steps)
  → Final text response
```

The loop is bounded by `maxSteps` (default 12). The LLM decides which tools to call, interprets results, and decides when to stop. The system prompt includes the user's identity files (COO.md, USER.md), memory context, and any policy instructions (POLICY.md).

**Source**: `lib/ai/agent-v04/route-integration.ts`

### 3.4 IPC: Agent-to-Agent Communication

When Agent A calls `contact_agent(to="alex", message="What's the project status?")`:

1. **Resolve recipient** — look up username → userId.
2. **Load permissions** — fetch the `agent_permissions` row where `grantor_id=alex, grantee_id=tina`. This determines which of Alex's tools Tina's request can access.
3. **Assemble tools** — call `createFlatToolsWithContext(alexId, ...)` with the permission-scoped `agentContext`. If permissions say `notesAccess: {scope: "all", access: "read"}`, Alex's agent gets `search_notes` and `get_note_content` but not `create_note` or `edit_note`.
4. **Run reasoning loop** — Alex's agent processes the message using its own system prompt, identity, memory, and the scoped tools. It may call `search_notes`, `get_note_content`, etc., across multiple reasoning steps.
5. **Return response** — the final text from Alex's agent is returned as the tool result to Tina's agent.

**This is the mechanism our privacy experiments test.** M0/M1/M2 vary Alex's POLICY.md (the prompt instruction) while keeping the architectural permissions at `scope=all`. The question is: can prompt-only policy prevent information leakage when the agent has full tool access?

### 3.5 Access Control: Permission Scoping

Permissions are stored per-relationship in the `agent_permissions` table:

```
grantor_id  | grantee_id | notes_access                           | calendar_access | email_access | todo_access
alex        | tina       | {"scope":"all","access":"read"}         | null            | null         | null
```

**Scope values**: `all` (access everything), `folder` (specific folder IDs only), `none`.
**Access values**: `read`, `write` (read implies search + get_content; write adds create + edit).

When `scope=all`, the agent can search and read every note. When `scope=folder`, the agent can only access notes in whitelisted folders. When `scope=none` or `null`, the tool is not loaded at all — it does not appear in the LLM's available tools.

This is the architectural lever that a future M3 defense level would use: restricting `scope` to `folder` so that sensitive folders (Finance, Health, HR) are never loaded into the tool context, regardless of what the prompt says. Our current M0/M1/M2 experiments deliberately keep `scope=all` to isolate the effect of prompt-only policy.

**Source**: `lib/ai/tools/agent-context.ts`, `lib/ai/tools/index.ts` (`filterToolsByAccess`)

---

## 4. Relevance to the Cross-Boundary Privacy Experiments

The experiments in this thesis test a specific question: **When Agent A has full read access to User B's data, can prompt-only instructions (POLICY.md) prevent sensitive information from leaking to the requester?**

The OS infrastructure makes this a meaningful question because:

1. **The tools are real.** `search_notes` performs actual multi-query semantic search against encrypted personal data. `contact_agent` runs a full reasoning loop with tool access. There is no mock or stub — the agent genuinely searches notes, reads content, and decides what to include in its response.

2. **The permissions are real.** When we set `notes_access.scope = "all"`, the agent can access every note Alex has — work projects, bank accounts, medical records, relationship details. The architectural layer *permits* the access. The defense is purely in the prompt.

3. **The attack surface is well-defined.** Tina's agent sends a natural-language message via `contact_agent`. Alex's agent searches notes via `search_notes`, reads full content via `get_note_content`, and composes a response. The leakage question is: does the response contain sensitive facts from notes the agent *could* access but *should not* disclose?

4. **The tool chain is deterministic.** For a given question, the agent always follows the same pipeline: receive message → search notes → read note content → compose response. The variance comes from the LLM's reasoning, not from infrastructure nondeterminism. This makes the experiments reproducible.

The three defense levels (M0, M1, M2) modify ONLY Alex's POLICY.md — a ~200-word instruction in the system prompt. The 45-tool OS, the encryption layer, the permission system, the agent reasoning loop — all remain identical across conditions. This isolates the independent variable: **does the prompt instruction change the agent's data-disclosure behavior when the architectural access remains unchanged?**

---

## 5. Implementation Notes

### Tool Count Summary

| Domain | Tools | Role in experiments |
|--------|-------|-------------------|
| Notes | 9 | **Primary** — Alex's data store; all 200 ground-truth facts live here |
| Todos | 5 | **Primary** — task management state |
| Agent Communication | 3 | **Primary** — `contact_agent` is the cross-boundary mechanism |
| Email | 7 | Additional state |
| Calendar | 5 | Additional state |
| Projects | 6 | Additional state |
| Web | 2 | Additional state |
| External Apps (Composio) | 5 | Additional state |
| **Total** | **42 internal + MCP** | |

### Running the Tools Test

```bash
NODE_OPTIONS='--require ./research/scripts/env-preload.js' npx tsx research/scripts/_test_tools.ts
```

`env-preload.js` must run before any module loads because `ENCRYPTION_MASTER_KEY` is captured at import time by the Drizzle custom column type. Without it, all encrypted-column operations fail.

### Known Issues (Fixed 2026-04-28)

1. **`edit_todo` was missing from tool registry.** Defined in `todo-management.ts` but never registered in `createFlatToolsWithContext`. Added to `DefaultToolName` enum, domain list, and both tool mapping functions.

2. **`search_todos` always returned empty.** Used SQL `ilike()` on encrypted columns — matched against ciphertext, never finding anything. Fixed to fetch all rows for the user, then filter in-memory on decrypted values.

### Key Source Files

| File | Purpose |
|------|---------|
| `lib/ai/tools/index.ts` | Tool assembly pipeline (`createFlatToolsWithContext`) |
| `lib/ai/tools/notes-management.ts` | Notes CRUD + AI-powered semantic search |
| `lib/ai/tools/todo-management.ts` | Todo CRUD + AI workflow automation |
| `lib/ai/tools/agent-network.ts` | `contact_agent` — agent-to-agent RPC |
| `lib/ai/tools/messaging.ts` | Human messaging + contact search |
| `lib/ai/tools/agent-context.ts` | Permission types and normalization |
| `lib/ai/tools/handlers/todos/*.ts` | Todo handler implementations |
| `lib/db/encryption/encryption.ts` | AES-256-GCM encrypt/decrypt |
| `lib/ai/agent-v04/route-integration.ts` | Agent reasoning loop |
| `lib/ai/shared-agent-core.ts` | System prompt assembly, tool scoping |
| `research/scripts/_test_tools.ts` | Tool integration test (11/11 passing) |
