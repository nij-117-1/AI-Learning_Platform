import os
import uuid
import aiofiles
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from learning.grader.services import GraderService
from learning.grader.utils import resize_image
from learning.grader.schemas import GradingResponse
from config import master_llm_config as config
from typing import Optional


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/grader", tags=["Performance Grader"])

BASE_STORAGE_DIR = "Data/Grader"

@router.post("/evaluate", response_model=GradingResponse)
async def evaluate_submission(
    username: str = Form(..., description="User identifier for storage"),
    scenario: str = Form(...),
    question_asked: str = Form(...),
    target_objective: str = Form(...),
    expected_level: str = Form(...),
    user_answer_text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Handles image upload, resize (max 1024px), and LLM grading.
    """
    user_dir = os.path.join(BASE_STORAGE_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    processed_bytes = None

    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

        file_ext = os.path.splitext(image.filename)[1] or ".jpg"
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(user_dir, unique_filename)

        content = await image.read()
        logger.info("📸 Image received: %s (%d bytes, type=%s)", image.filename, len(content), image.content_type)

        processed_bytes = resize_image(content)

        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(processed_bytes)

    # 4. Process Logic
    try:
        payload = {
            "scenario": scenario,
            "question_asked": question_asked,
            "target_objective": target_objective,
            "expected_level": expected_level,
            "user_answer_text": user_answer_text
        }
        
        return await GraderService.process_grading_logic(
            processed_bytes=processed_bytes,
            payload=payload,
            config=config
        )
    except Exception as e:
        logger.exception(f"Grading failed for {username}")
        raise HTTPException(status_code=500, detail=str(e))