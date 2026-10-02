# Interview Practice API

The interview module is mounted under `/practice/interview`. It uses the shared API-key dependency. Session state is returned to the client for persistence and is sent back with each answer.

## `POST /practice/interview/start`

Starts an interview and returns the first question.

```json
{
  "candidate_profile": {"skills": ["Python", "FastAPI"], "experience_years": 5},
  "position_details": {"title": "Senior Backend Engineer", "level": "senior"},
  "interview_context": {"type": "technical", "format": "onsite", "interviewer_role": "Tech Lead"},
  "max_questions": 8,
  "time_remaining_minutes": 45
}
```

The response includes `session_id`, the generated `question`, and the initial `progress_state`.

## `POST /practice/interview/answer`

Submits an answer with the state returned by the preceding calls. The response includes the assessment, updated history and progress, and either `next_question` or `is_complete: true`.

Send the previous response's `session_id`, `progress_state`, question/history, plus candidate and position context, `candidate_answer`, `questions_asked`, `max_questions`, and `time_remaining_minutes`.
