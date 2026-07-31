from fastapi import APIRouter, Depends, HTTPException
from practice.debate.schemas import PersonaRequest, PersonaResponse, DebateTurnRequest, DebateTurnResponse
from practice.debate.services import DebateService
from practice.debate.dependencies import get_debate_service
from core.security import verify_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/debate")

@router.post("/generate-persona", response_model=PersonaResponse)
async def api_generate_persona(
    payload: PersonaRequest,
    service: DebateService = Depends(get_debate_service),
    _: str = Depends(verify_api_key),
):
    try:
        master_prompt = service.generate_persona(payload)
        return PersonaResponse(master_prompt=master_prompt)
    except Exception as e:
        logger.exception("Failed to generate debate persona")
        raise HTTPException(status_code=500, detail="Internal AI Processing Error")

@router.post("/execute-turn", response_model=DebateTurnResponse)
async def api_execute_turn(
    payload: DebateTurnRequest,
    service: DebateService = Depends(get_debate_service),
    _: str = Depends(verify_api_key),
):
    try:
        result = service.execute_turn(payload)
        return DebateTurnResponse(
            rebuttal_summary=result.rebuttal_summary,
            argument_body=result.argument_body,
            rhetorical_devices=result.rhetorical_devices,
            next_question=result.next_question
        )
    except Exception as e:
        logger.exception("Failed to execute debate turn")
        raise HTTPException(
            status_code=500,
            detail=f"AI Turn Execution Failed: {str(e)}"
        )