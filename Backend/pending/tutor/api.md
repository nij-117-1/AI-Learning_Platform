# Tutor Module API

Base path: `/tutor`

## Endpoints

### POST `/tutor/explain`

Submit a student query and receive an adaptive pedagogical response.

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `system_prompt` | string | yes | Persona and pedagogical rules |
| `user_query` | string | yes | The student's question or struggle |
| `student_level` | string | yes | Proficiency level (e.g. Toddler, High School, Expert) |
| `learning_style` | string | yes | Preferred framing (analogical, first_principles, etc.) |
| `current_scenario` | string | yes | Learning context (e.g. "preparing for an exam") |
| `chat_history` | array[ChatMessage] | no | Previous conversation turns (default: `[]`) |
| `last_topic_taught` | string | no | Context of the previous lesson |

`ChatMessage: { role: string, content: string }`

**Response `200`:**

| Field | Type | Description |
|---|---|---|
| `adapted_explanation` | string | AI-generated teaching content |
| `concept_analogy` | string or null | A metaphor or mental hook |
| `tutor_feedback` | string | Conversational nudge or question |

---

### POST `/tutor/prompts`

Create or update a prompt template. Stored as a YAML file in `tutor/prompts/`.

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Unique identifier (used as filename) |
| `content` | string | yes | The system prompt text |

**Response `201`:** `{ "message": "Prompt '<name>' created/updated successfully" }`

---

### GET `/tutor/prompts`

List all available prompt names.

**Response `200`:** `["socratic_tutor", "cheerful_coach", ...]`

---

### GET `/tutor/prompts/{name}`

Retrieve a single prompt by name.

**Response `200`:**

| Field | Type | Description |
|---|---|---|
| `name` | string | Prompt identifier |
| `content` | string | Prompt body text |
| `created_at` | datetime (ISO-8601) | Creation timestamp |
| `updated_at` | datetime (ISO-8601) | Last-update timestamp |

**Response `404`:** Prompt not found.

---

### PUT `/tutor/prompts/{name}`

Update an existing prompt.

**Request body:** Same as POST (name + content).

**Response `200`:** `{ "message": "Updated" }`

---

### DELETE `/tutor/prompts/{name}`

Delete a prompt file.

**Response `204`:** No content.

**Response `404`:** Prompt not found.
