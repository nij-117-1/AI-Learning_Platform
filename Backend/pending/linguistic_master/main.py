import logging
from fastapi import FastAPI
from .word_of_the_day.router import router as wotd_router
from .translator.router import router as translator_router
from .rewriter.router import router as rewriter_router
from .sentence_of_the_day.router import router as sentence_router
from .poet_engine.router import router as poet_router
from .idioms.router import router as idioms_router
from .language_tester.router import router as language_tester_router
from .roleplay_module.router import router as roleplay_router
from .lesson.router import router as lesson_router
from .simulator.router import router as simulator_router
# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Linguistic Master API")

# Mount the pluggable modules under the "/linguistic" prefix
app.include_router(wotd_router, prefix="/linguistic")
app.include_router(translator_router, prefix="/linguistic")
app.include_router(rewriter_router, prefix="/linguistic")
app.include_router(sentence_router, prefix="/linguistic")
app.include_router(poet_router, prefix="/linguistic")
app.include_router(idioms_router, prefix="/linguistic")
app.include_router(language_tester_router, prefix="/linguistic")
app.include_router(roleplay_router, prefix="/linguistic")
app.include_router(lesson_router, prefix="/linguistic")
app.include_router(simulator_router, prefix="/linguistic")
# Health check accessible at /linguistic/health
@app.get("/linguistic/health")
async def health_check():
    return {"status": "online"}