from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
# Ensure these imports match your project structure
from Tools.diagram.utils import execute_drawio_task, execute_mermaid_task

# 1. Create the router object
router = APIRouter(
    prefix="/diagrams",
    tags=["Diagram Generation"]
)

# --- Data Models ---
class DiagramRequest(BaseModel):
    format: str  # "mermaid" or "drawio"
    instruction: str
    context: Optional[str] = ""
    existing_code: Optional[str] = ""

class DiagramResponse(BaseModel):
    message: str
    code: str
    format: str

# --- The API Endpoint ---
@router.post("/generate", response_model=DiagramResponse)
async def generate_diagram(request: DiagramRequest):
    try:
        format_type = request.format.lower()
        
        if format_type == "mermaid":
            result = execute_mermaid_task(
                code=request.existing_code,
                instruction=request.instruction,
                context=request.context
            )
        elif format_type == "drawio":
            result = execute_drawio_task(
                instruction=request.instruction,
                context=request.context,
                code=request.existing_code
            )
        else:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported format. Use 'mermaid' or 'drawio'."
            )

        return DiagramResponse(
            message=result.answer_message,
            code=result.updated_code,
            format=format_type
        )

    except Exception as e:
        # It's better to log 'e' here for debugging
        print(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")