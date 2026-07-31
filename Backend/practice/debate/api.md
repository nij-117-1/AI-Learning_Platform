# Debate Engine API

Base path: `/practice/debate`

## Endpoints

### `POST /practice/debate/generate-persona`

Generates a master system prompt for a debate persona using DSPy.

**Request body** (`PersonaRequest`):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | `string` | ✅ | The subject of the debate (e.g., "Universal Basic Income") |
| `stance` | `string` | ✅ | The position the persona should take (e.g., "Strongly Opposed") |
| `debate_style` | `string` | ✅ | One of: `Socratic`, `Aggressive`, `Scientific`, `Empathetic`, `Formal` |
| `user_constraints` | `string` | ❌ | Specific traits or focus areas (e.g., "Focus on inflation.") |

**Response** (`PersonaResponse`):

```json
{
  "master_prompt": "You are a sharp, evidence-driven debater...",
  "status": "success"
}
```

---

### `POST /practice/debate/execute-turn`

Processes a single turn in a debate, generating a rebuttal and argument.

**Request body** (`DebateTurnRequest`):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `persona` | `string` | ✅ | The system prompt defining the character |
| `topic` | `string` | ✅ | Core question being debated (e.g., "Is AI a threat to creativity?") |
| `theme` | `string` | ✅ | Framing context (e.g., "Philosopher vs Silicon Valley CEO") |
| `history` | `array[object]` | ✅ | List of previous `{role, content}` messages |
| `context` | `string` | ✅ | Focus area for this turn (e.g., "impact on jobs") |
| `strategy` | `string` | ✅ | One of: `attack`, `defend`, `counter` |
| `instructions` | `string` | ❌ | Custom constraints (default: "Be concise and sharp.") |
| `evidence` | `string` | ❌ | Supporting facts or raw data to anchor the argument |

**Response** (`DebateTurnResponse`):

```json
{
  "rebuttal_summary": "The opponent argues that AI enhances creativity...",
  "argument_body": "While AI can generate variations, true creativity requires...",
  "rhetorical_devices": ["Ethos", "Logos", "Aporia"],
  "next_question": "How do you define original thought in an age of generative models?",
  "status": "success"
}
```

---

## Shared models

### `DebateSession`

Data contract for tracking a debate across multiple turns.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique session identifier |
| `topic` | `string` | Core debate question |
| `theme` | `string` | Framing context |
| `persona` | `string` | The active persona definition |
| `stance` | `string` | Position taken |
| `debate_style` | `string` | Rhetorical approach |
| `history` | `array[object]` | All previous exchanges |
| `created_at` | `datetime` | Session creation timestamp |
| `updated_at` | `datetime` | Last-updated timestamp |
| `is_active` | `bool` | Whether the session is ongoing |
