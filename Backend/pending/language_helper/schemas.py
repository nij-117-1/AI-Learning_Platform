from pydantic import BaseModel, Field
from typing import Optional, Literal, List


class IdiomRequest(BaseModel):
    target_language: str = Field(..., example="French")
    user_proficiency: Literal["beginner", "intermediate", "advanced", "native-aspirant"]
    theme_or_keyword: str = Field(..., example="Success")
    native_language: str = Field(default="English")
    seed: str = Field(..., description="Unique string for variety")
    custom_user_request: Optional[str] = Field(None, example="Make it food related")

class IdiomResponse(BaseModel):
    rationale: str
    idiom_in_target_language: str
    phonetic_pronunciation: str
    figurative_meaning: str
    cultural_context: str
    equivalent_in_native_language: str
    dialogue_scenario: str
    practice_prompt: str

class PoeticRequest(BaseModel):
    target_language: str = Field(..., example="Japanese")
    concept_word: str = Field(..., example="Kintsugi")
    poetic_style: Literal["Shayari/Couplet", "Haiku", "Metaphorical Prose", "Ghazal-style"]
    seed: str = Field(..., description="Seed for imagery variety")
    user_mood: Optional[str] = Field(None, example="healing and resilient")
    user_custom_instruction: Optional[str] = Field(None, example="Compare to urban architecture")

class PoeticResponse(BaseModel):
    rationale: str
    original_poetry: str
    deep_meaning_translation: str
    philosophical_reflection: str
    visual_metaphor: str

class WordOfDayRequest(BaseModel):
    language: str = Field(..., example="German")
    user_proficiency: Literal["basic", "academic", "poetic", "slang"]
    thematic_focus: Optional[str] = Field(None, example="Nature and Solitude")
    seed: str = Field(..., description="Entropy string for uniqueness")
    user_custom_instructions: Optional[str] = Field(None, example="Rare untranslatable words")

class WordOfDayResponse(BaseModel):
    word: str
    phonetic_and_audio_guide: str
    morphology_breakdown: str
    primary_definition: str
    the_vibe_check: str
    historical_evolution: str
    modern_usage_sentence: str
    synonym_web: List[str]

class LessonRequest(BaseModel):
    language: str = Field(..., example="French")
    current_level: Literal["A1", "A2", "B1", "B2", "C1"]
    last_lesson_topic: Optional[str] = Field(None, example="Passé Composé")
    learning_focus: Literal["Grammar", "Vocabulary", "Conversation", "Culture"]
    seed: str = Field(..., description="Entropy for variety")
    user_custom_instruction: Optional[str] = Field(None, example="Space exploration theme")

class LessonResponse(BaseModel):
    lesson_title: str
    concept_explanation: str
    connection_to_previous: str
    themed_examples: List[str]
    practice_exercises: List[str]
    suggested_homework: str


class TranslationRequest(BaseModel):
    text_to_translate: str = Field(..., min_length=1)
    source_language: str = Field(default="Auto-detect")
    target_language: str = Field(..., example="German")
    tone: Literal["formal", "casual", "business", "poetic", "technical"] = Field(default="formal")
    reference_material: Optional[str] = Field(None, description="Glossary or context snippets")
    custom_instructions: Optional[str] = Field(None, example="Do not translate technical terms like 'Load Balancer'")

class TranslationResponse(BaseModel):
    rationale: str
    translated_text: str
    cultural_notes: Optional[str] = None

class RewriteRequest(BaseModel):
    original_text: str = Field(..., min_length=1)
    target_tone: str = Field(..., example="professional")
    audience: str = Field(default="General", example="executives")
    transformation_goal: Literal["paraphrase", "shorten", "expand", "simplify"] = Field(...)
    custom_instructions: Optional[str] = Field(None, example="Use active voice")

class RewriteResponse(BaseModel):
    rationale: str
    rewritten_text: str
    improvements_made: List[str]