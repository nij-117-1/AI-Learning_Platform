from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from learning.tutor.schemas import TutorRequest, TutorResponse, PromptCreateUpdate, PromptResponse
from learning.tutor.services import TutorService, PromptService
from learning.tutor.dependencies import get_tutor_service, get_prompt_service

router = APIRouter(prefix="/tutor", tags=["Tutor"])


@router.post("/explain", response_model=TutorResponse)
async def explain_concept(
    request: TutorRequest,
    service: TutorService = Depends(get_tutor_service),
) -> TutorResponse:
    try:
        return await service.get_adaptive_response(request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Tutor engine failed to process the request.",
        )


@router.post("/prompts", status_code=201)
def create_prompt(
    data: PromptCreateUpdate,
    service: PromptService = Depends(get_prompt_service),
) -> dict:
    name = service.create_or_update_prompt(data)
    return {"message": f"Prompt '{name}' created/updated successfully"}


@router.get("/prompts", response_model=List[str])
def list_prompts(
    service: PromptService = Depends(get_prompt_service),
) -> List[str]:
    return service.list_prompts()


@router.get("/prompts/{name}", response_model=PromptResponse)
def get_prompt(
    name: str,
    service: PromptService = Depends(get_prompt_service),
) -> PromptResponse:
    prompt = service.read_prompt_full(name)
    return PromptResponse(
        name=prompt.name,
        content=prompt.content,
        created_at=prompt.created_at,
        updated_at=prompt.updated_at,
    )


@router.put("/prompts/{name}")
def update_prompt(
    name: str,
    data: PromptCreateUpdate,
    service: PromptService = Depends(get_prompt_service),
) -> dict:
    service.create_or_update_prompt(data)
    return {"message": "Updated"}


@router.delete("/prompts/{name}", status_code=204)
def delete_prompt(
    name: str,
    service: PromptService = Depends(get_prompt_service),
) -> Response:
    service.delete_prompt(name)
    return Response(status_code=204)
