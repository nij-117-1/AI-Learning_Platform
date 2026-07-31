from learning.roadmap.services import RoadmapService
from config import master_llm_config

def get_roadmap_service() -> RoadmapService:
    """
    Dependency injector for the RoadmapService.
    """
    return RoadmapService(config=master_llm_config)