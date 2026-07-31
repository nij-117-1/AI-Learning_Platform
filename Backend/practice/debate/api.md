# Debate Engine API

Base path: `/practice/debate`
Tag: `Practice Module`

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

**Example request**:

```bash
curl -X POST http://localhost:8000/practice/debate/generate-persona \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <your-key>" \
  -d '{
    "topic": "Universal Basic Income",
    "stance": "Strongly Opposed",
    "debate_style": "Socratic",
    "user_constraints": "Focus on inflation."
  }'
```

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

**Example request**:

```bash
curl -X POST http://localhost:8000/practice/debate/execute-turn \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <your-key>" \
  -d '{
    "persona": "You are a skeptical philosopher...",
    "topic": "Is AI a threat to creativity?",
    "theme": "Philosopher vs Silicon Valley CEO",
    "history": [
      {"role": "CEO", "content": "AI is just a tool."}
    ],
    "context": "impact on jobs",
    "strategy": "counter",
    "instructions": "Be concise and sharp.",
    "evidence": "Oxford 2023 study on creative occupations"
  }'
```

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

## Error responses

All endpoints return a JSON body on failure.

| Status | Code | Detail |
|--------|------|--------|
| `400` | `validation_error` | Pydantic request validation failed |
| `403` | — | Invalid or missing `X-API-Key` header |
| `500` | — | Internal AI processing failure |

**Example 500:**

```json
{
  "detail": "Internal AI Processing Error"
}
```

## Authentication

Optional `X-API-Key` header. When `LLM_API_KEY` is set in the environment, the server rejects requests without a matching key. When blank, the guard is disabled.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `LLM_MODEL_NAME` | `gpt-4o-mini` | Model passed to DSPy |
| `LLM_API_KEY` | *(empty)* | Provider API key / auth guard |
| `LLM_API_BASE` | `https://api.openai.com/v1` | OpenAI-compatible base URL |
| `LLM_TEMPERATURE` | `0.7` | Sampling temperature |
| `DEBUG` | `false` | FastAPI debug mode |
| `LOG_LEVEL` | `INFO` (`DEBUG` if `DEBUG=true`) | Logging verbosity |
| `HOST` / `PORT` | `0.0.0.0` / `8000` | Uvicorn bind address |

---

## Shared models

### `DebateSession`

Data contract for tracking a debate across multiple turns (persistence not yet wired up).

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
