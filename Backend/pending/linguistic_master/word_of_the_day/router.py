from fastapi import APIRouter, HTTPException, Depends
from .schemas import WOTDRequest, WOTDResponse
from .services import LinguisticService

router = APIRouter(
    prefix="/wotd",
    tags=["Word of the Day"]
)

@router.post("/", response_model=WOTDResponse)
async def get_word_of_the_day(payload: WOTDRequest):
    """
    Fetch a linguistically rich Word of the Day based on the provided configuration.
    """
    service = LinguisticService()
    try:
        prediction = await service.generate_daily_word(payload)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail="Linguistic engine error.")