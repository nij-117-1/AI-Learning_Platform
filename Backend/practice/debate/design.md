# Design Guidelines & Checklist

Engineering rules enforced across this sub-project. Every new module/feature must pass all items before it is considered done.

## Project structure

Each sub-feature lives in its own package under `practice/`, fully decoupled from the master app:

```
Backend/
├── main.py                     # Slim entry point — only includes practice_router
├── .env                        # Local secrets (gitignored)
├── .env.example                # Committed template of all config keys
├── core/
│   └── config.py               # Reads .env, falls back to defaults
└── practice/
    ├── router.py               # Aggregates all sub-feature routers
    ├── debate/
    │   ├── router.py           # APIRouter + endpoints
    │   ├── schemas.py          # Pydantic v2 request/response models
    │   ├── services.py         # Business logic (DSPy calls)
    │   ├── dependencies.py     # Auth / service injectors
    │   ├── models.py           # Data contracts for future DB integration
    │   ├── api.md              # API documentation
    │   └── design.md           # This file
    └── <next-feature>/
        ├── router.py
        ├── schemas.py
        ├── services.py
        ├── dependencies.py
        └── models.py
```

## Engineering rules (mandatory)

- [ ] **Type safety** — every function signature has explicit type hints; no bare `def foo(x):`.
- [ ] **Docstrings** — Google style (`Args:`, `Returns:`, `Raises:`) on all public functions and classes.
- [ ] **Logging** — use the `logging` module with `logger = logging.getLogger(__name__)`. No `print()` statements.
- [ ] **Validation** — all schemas use Pydantic v2 (`BaseModel`, `Field`, `Literal`, `Optional`).
- [ ] **Routing** — `APIRouter` with a `prefix` and `tags`. Prefix must match the package name.
- [ ] **Absolute imports** — always `from practice.<feature>.xyz import ...`, never relative.
- [ ] **Slim `main.py`** — the master entry must only do `app.include_router(practice_router)`; it never knows about individual features.
- [ ] **Errors** — raise custom `HTTPException` subclasses; never let raw exceptions reach the client.

## Adding a new sub-feature (checklist)

1. Create `practice/<feature>/` with `router.py`, `schemas.py`, `services.py`, `dependencies.py`, `models.py` (+ `__init__.py`).
2. Register the router in `practice/router.py` with one line:
   ```python
   from practice.<feature>.router import router as <feature>_router
   practice_router.include_router(<feature>_router)
   ```
3. Do **not** modify `main.py`.
4. Add feature-specific config to `.env` and `.env.example`; expose them via `core/config.py` with defaults.
5. Write `api.md` documenting every endpoint (method, path, request/response tables, curl examples, error codes).

## Configuration rules

- All config is read from `.env` via `os.getenv(key, default)`.
- Every key must have a sensible default in `core/config.py` so the app boots without `.env`.
- Secrets never go in `.env.example` or into git.
- Logging verbosity is controlled by `LOG_LEVEL`; developers can set `LOG_LEVEL=DEBUG` without enabling FastAPI debug mode.

## File responsibility

| File | Owns | Must not do |
|------|------|-------------|
| `router.py` | HTTP endpoints, status codes, request → service wiring | Business logic, direct DSPy calls |
| `schemas.py` | Pydantic request/response models | Business logic |
| `services.py` | Business logic, DSPy orchestration | HTTP concerns, `HTTPException` |
| `dependencies.py` | Dependency injection, auth guards | Endpoint definitions |
| `models.py` | Persistence data contracts | Business logic |
