from fastapi import APIRouter, Depends, HTTPException, status
from learning.memory_helper.schemas import MemoryRequest, MemoryResponse
from learning.memory_helper.services import MemoryService
from learning.memory_helper.services import MemoryService

def get_memory_service() -> MemoryService:
    """Dependency injector for the MemoryService."""
    return MemoryService()
    
router = APIRouter(
    prefix="/memory-helper",
    tags=["Memory Specialist"]
)

@router.post("/process", response_model=MemoryResponse)
async def process_memory_request(
    payload: MemoryRequest,
    service: MemoryService = Depends(get_memory_service)
):
    """
    Takes complex data and returns structured mnemonics and a retention plan.
    """
    try:
        result = service.run_agent(payload)
        return {
            "explanation": result.explanation,
            "memory_hooks": result.memory_hooks,
            "retention_plan": result.retention_plan
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while processing cognitive hooks."
        )