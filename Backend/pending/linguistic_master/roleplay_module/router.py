from fastapi import APIRouter, HTTPException, Depends
from .schemas import RoleplayRequest, RoleplayResponse
from .services import RoleplayService
from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import RoleplayRecord, RoleplayUpdate, RoleplayRequest, RoleplayResponse
from .services import RoleplayStorageService, RoleplayService

router = APIRouter(prefix="/roleplay", tags=["Roleplay AI"])
storage = RoleplayStorageService()
ai_service = RoleplayService()

@router.post("/chat", response_model=RoleplayResponse)
async def chat_interaction(request_data: RoleplayRequest):
    """
    Endpoint to interact with the Roleplay Chatbot.
    """
    service = RoleplayService()
    try:
        response = service.generate_response(request_data)
        return RoleplayResponse(response_message=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal AI Processing Error")


@router.post("/roles", response_model=RoleplayRecord)
def create_role(role: RoleplayRecord):
    """Create a new roleplay YAML file."""
    return storage.create_role(role)

@router.get("/roles", response_model=List[str])
def list_roles():
    """List all available role names."""
    return storage.list_roles()

@router.get("/roles/{name}", response_model=RoleplayRecord)
def get_role(name: str):
    """Get the system prompt for a specific role."""
    return storage.get_role(name)

@router.patch("/roles/{name}", response_model=RoleplayRecord)
def update_role(name: str, update: RoleplayUpdate):
    """Update the prompt for an existing role."""
    return storage.update_role(name, update.prompt)

@router.delete("/roles/{name}")
def delete_role(name: str):
    """Delete a roleplay YAML file."""
    return storage.delete_role(name)

# --- CHAT ENDPOINT (Modified to use stored roles) ---

@router.post("/chat/stored/{name}", response_model=RoleplayResponse)
async def chat_with_stored_role(name: str, request: RoleplayRequest):
    """
    Chat using a pre-saved persona from YAML. 
    It overrides the request system_prompt with the stored one.
    """
    stored_role = storage.get_role(name)
    request.system_prompt = stored_role.prompt
    
    response = ai_service.generate_response(request)
    return RoleplayResponse(response_message=response)