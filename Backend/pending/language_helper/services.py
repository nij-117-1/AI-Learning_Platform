import dspy
import logging
from config import master_llm_config as config
from learning.language_helper.schemas import IdiomRequest, PoeticRequest , WordOfDayRequest, LessonRequest ,TranslationRequest,RewriteRequest
from typing import Literal, Optional, List


logger = logging.getLogger(__name__)

class IdiomsHelper(dspy.Signature):
    """
    You are an Expert Polyglot and Philologist. 
    Your mission is to help users master idiomatic expressions across different languages.
    Use the 'seed' to rotate through different idioms for the same topic.
    Incorporate the 'custom_user_request' to tailor the tone, complexity, or specific niche.
    """
    # Inputs
    target_language: str = dspy.InputField(desc="The language the user wants to learn (e.g., Spanish, Mandarin).")
    user_proficiency: Literal["beginner", "intermediate", "advanced", "native-aspirant"] = dspy.InputField(desc="Current level of the user.")
    theme_or_keyword: str = dspy.InputField(desc="The general topic (e.g., 'Time', 'Money', 'Health').")
    native_language: str = dspy.InputField(desc="The user's primary language for explanations.")
    seed: str = dspy.InputField(desc="A unique string to ensure variety in idiom selection.")
    custom_user_request: Optional[str] = dspy.InputField(desc="Specific user preferences (e.g., 'make it funny', 'business context only').")

    # Outputs
    rationale: str = dspy.OutputField(desc="Reasoning for selecting this specific idiom based on the seed and user request.")
    idiom_in_target_language: str = dspy.OutputField(desc="The idiom written in the target language.")
    phonetic_pronunciation: str = dspy.OutputField(desc="How to say it (IPA or phonetic spelling).")
    figurative_meaning: str = dspy.OutputField(desc="The actual meaning interpreted in the native language.")
    cultural_context: str = dspy.OutputField(desc="The 'Why' and 'When' - historical origin or social setting.")
    equivalent_in_native_language: str = dspy.OutputField(desc="A matching idiom in the user's native tongue.")
    dialogue_scenario: str = dspy.OutputField(desc="A short script showing the idiom in use.")
    practice_prompt: str = dspy.OutputField(desc="A question asking the user to use the idiom in a new sentence.")

class PoeticLanguageExplainer(dspy.Signature):
    """
    You are a Poetic Philologist and Sufi-inspired Linguist.
    Your goal is to explain the 'Soul' of a word or concept through poetry and 
    philosophical reflection. Use the 'user_custom_instruction' to pivot the 
    theme or complexity of the explanation.
    """
    # Inputs
    target_language: str = dspy.InputField(desc="The language of the concept (e.g., Urdu, Persian, Japanese).")
    concept_word: str = dspy.InputField(desc="The specific word or abstract concept (e.g., 'Longing', 'Silence').")
    poetic_style: Literal["Shayari/Couplet", "Haiku", "Metaphorical Prose", "Ghazal-style"] = dspy.InputField()
    seed: str = dspy.InputField(desc="A seed for variety in poetic imagery.")
    user_mood: Optional[str] = dspy.InputField(desc="The emotional tone (e.g., 'melancholic', 'mystical').")
    user_custom_instruction: Optional[str] = dspy.InputField(desc="Specific constraints (e.g., 'use nature metaphors', 'make it about urban life').")

    # Outputs
    rationale: str = dspy.OutputField(desc="Internal logic connecting the concept, mood, and user's custom instruction.")
    original_poetry: str = dspy.OutputField(desc="The poetic piece in the target language.")
    deep_meaning_translation: str = dspy.OutputField(desc="A soulful translation capturing the essence, not just the words.")
    philosophical_reflection: str = dspy.OutputField(desc="A 'Think about this' section that connects the word to human experience.")
    visual_metaphor: str = dspy.OutputField(desc="A vivid description of a scene that represents this word/poem.")

class WordOfTheDayExplorer(dspy.Signature):
    """
    You are a Master Etymologist and Linguist. 
    Your goal is to provide a 'Deep Dive' Word of the Day.
    You connect ancient linguistic roots to modern-day usage.
    The 'date' ensures the word is unique to that day, while the 'seed' 
    and 'user_input' allow for thematic customization.
    """
    # Inputs
    date: str = dspy.InputField(desc="The current date (YYYY-MM-DD) to anchor the selection.")
    language: str = dspy.InputField(desc="The language to pull the word from.")
    user_proficiency: Literal["basic", "academic", "poetic", "slang"] = dspy.InputField()
    thematic_focus: Optional[str] = dspy.InputField(desc="User's area of interest (e.g., 'Nature', 'Technology', 'Ancient Wisdom').")
    seed: str = dspy.InputField(desc="An entropy string to ensure a unique word selection for the same date/topic.")
    user_custom_instructions: Optional[str] = dspy.InputField(desc="Specific constraints: 'Only words with no English translation' or 'Words used in 19th-century literature'.")

    # Outputs
    word: str = dspy.OutputField(desc="The chosen word of the day.")
    phonetic_and_audio_guide: str = dspy.OutputField(desc="How to pronounce it perfectly.")
    morphology_breakdown: str = dspy.OutputField(desc="Root words, prefixes, and suffixes (e.g., Latin/Greek origins).")
    primary_definition: str = dspy.OutputField(desc="The clear, dictionary-style meaning.")
    the_vibe_check: str = dspy.OutputField(desc="Describing the 'feeling' of the word and the social context where it fits best.")
    historical_evolution: str = dspy.OutputField(desc="How the meaning has shifted over the centuries.")
    modern_usage_sentence: str = dspy.OutputField(desc="A sentence showing how a native speaker would use it TODAY.")
    synonym_web: List[str] = dspy.OutputField(desc="3-5 related words or concepts.")


class LanguageLessonGenerator(dspy.Signature):
    """
    You are a Personalized Language Tutor. 
    Analyze the user's previous lesson and current level to provide a 
    logical next step in their learning journey. 
    Use the 'seed' to keep examples fresh and 'user_custom_instruction' 
    to theme the lesson content creatively.
    """
    
    # Context & History
    language: str = dspy.InputField(desc="The language being learned.")
    current_level: Literal["A1", "A2", "B1", "B2", "C1"] = dspy.InputField(desc="CEFR Proficiency level.")
    last_lesson_topic: Optional[str] = dspy.InputField(desc="What the user learned in the previous session.")
    learning_focus: Literal["Grammar", "Vocabulary", "Conversation", "Culture"] = dspy.InputField()
    
    # Customization & Variety
    seed: str = dspy.InputField(desc="A seed for variety in poetic imagery and examples.")
    user_custom_instruction: Optional[str] = dspy.InputField(desc="Specific constraints (e.g., 'use nature metaphors', 'make it about urban life').")
    
    # Structured Outputs
    lesson_title: str = dspy.OutputField(desc="A catchy title for today's lesson reflecting the custom theme.")
    concept_explanation: str = dspy.OutputField(desc="A detailed explanation of the new rule or concept.")
    connection_to_previous: str = dspy.OutputField(desc="How this ties into what they learned last time.")
    themed_examples: List[str] = dspy.OutputField(desc="Examples of the concept using the user's requested theme/metaphors.")
    practice_exercises: List[str] = dspy.OutputField(desc="Interaction exercises to reinforce learning.")
    suggested_homework: str = dspy.OutputField(desc="A real-world task based on the lesson theme.")

import dspy
from typing import List, Dict, Any, Literal, Optional

class ContextualTranslator(dspy.Signature):
    """
    You are a Professional Linguist and Translator. 
    Your goal is to translate text accurately while preserving the nuances of tone, 
    cultural context, and specific user instructions.
    """
    
    # Inputs
    text_to_translate: str = dspy.InputField(desc="The source text that needs translation.")
    source_language: str = dspy.InputField(desc="The language of the input text.")
    target_language: str = dspy.InputField(desc="The language the text should be translated into.")
    tone: Literal["formal", "casual", "business", "poetic", "technical"] = dspy.InputField(desc="The desired style of the translation.")
    reference_material: Optional[str] = dspy.InputField(desc="Glossary or context snippets to maintain consistency.")
    custom_instructions: Optional[str] = dspy.InputField(desc="Specific rules (e.g., 'avoid gendered pronouns', 'keep brand names in English').")

    # Outputs
    rationale: str = dspy.OutputField(desc="Brief explanation of linguistic choices made for this translation.")
    translated_text: str = dspy.OutputField(desc="The final translated content.")
    cultural_notes: Optional[str] = dspy.OutputField(desc="Notes on idioms or cultural adjustments made during translation.")


import dspy
from typing import List, Dict, Any, Literal, Optional

class TextRewriter(dspy.Signature):
    """
    You are an Expert Content Editor and Copywriter.
    Your task is to rewrite the provided text to improve its quality, 
    adjust its tone, or change its structure while preserving the original intent.
    """
    
    # Inputs
    original_text: str = dspy.InputField(desc="The text that needs to be rewritten.")
    target_tone: str = dspy.InputField(desc="Desired tone (e.g., professional, witty, empathetic, concise).")
    audience: str = dspy.InputField(desc="Who the text is being written for (e.g., executives, kids, developers).")
    transformation_goal: Literal["paraphrase", "shorten", "expand", "simplify"] = dspy.InputField(desc="The primary objective of the rewrite.")
    custom_instructions: Optional[str] = dspy.InputField(desc="Specific constraints (e.g., 'use active voice', 'no bullet points').")

    # Outputs
    rationale: str = dspy.OutputField(desc="Explanation of the stylistic changes made.")
    rewritten_text: str = dspy.OutputField(desc="The final polished version of the text.")
    improvements_made: List[str] = dspy.OutputField(desc="A list of specific changes (e.g., 'Removed passive voice', 'Simplified jargon').")
    
class LanguageHelperService:
    def __init__(self):
        self.lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=config.get('temperature', 0.4),
            cache=False
        )

    def generate_idiom(self, data: IdiomRequest):
        """
        Executes the DSPy ChainOfThought to generate idiomatic content.
        
        Args:
            data: The validated IdiomRequest schema.
            
        Returns:
            Prediction object containing the idiom details.
        """
        try:
            with dspy.context(lm=self.lm):
                coach = dspy.ChainOfThought(IdiomsHelper)
                prediction = coach(
                    target_language=data.target_language,
                    user_proficiency=data.user_proficiency,
                    theme_or_keyword=data.theme_or_keyword,
                    native_language=data.native_language,
                    seed=data.seed,
                    custom_user_request=data.custom_user_request
                )
                logger.info(f"Successfully generated idiom for {data.target_language}")
                return prediction
        except Exception as e:
            logger.error(f"DSPy Execution Error: {str(e)}")
            raise e

    def generate_poetic_reflection(self, data: PoeticRequest):
        """
        Generates a poetic and philosophical deep-dive using a higher temperature.
        """
        # Poetic tasks usually require higher creativity (temperature)
        poetic_lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=0.95, 
            cache=False
        )
        
        try:
            with dspy.context(lm=poetic_lm):
                poet = dspy.ChainOfThought(PoeticLanguageExplainer)
                prediction = poet(
                    target_language=data.target_language,
                    concept_word=data.concept_word,
                    poetic_style=data.poetic_style,
                    seed=data.seed,
                    user_mood=data.user_mood,
                    user_custom_instruction=data.user_custom_instruction
                )
                return prediction
        except Exception as e:
            logger.error(f"Poetic Service Error: {str(e)}")
            raise e
            
    def generate_daily_word(self, data: WordOfDayRequest):
        """
        Generates a temporal-anchored Word of the Day.
        """
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with dspy.context(lm=self.lm):
                explorer = dspy.ChainOfThought(WordOfTheDayExplorer)
                prediction = explorer(
                    date=today_str,
                    language=data.language,
                    user_proficiency=data.user_proficiency,
                    thematic_focus=data.thematic_focus,
                    seed=data.seed,
                    user_custom_instructions=data.user_custom_instructions
                )
                return prediction
        except Exception as e:
            logger.error(f"WordOfDay Service Error: {str(e)}")
            raise e

    def generate_custom_lesson(self, data: LessonRequest):
        """
        Generates a structured language lesson with thematic consistency.
        
        Args:
            data: LessonRequest validation model.
        Returns:
            Prediction object.
        """
        # Higher temperature for creative themed lessons
         
        try:
            with dspy.context(lm=self.lm):
                tutor = dspy.ChainOfThought(LanguageLessonGenerator)
                prediction = tutor(
                    language=data.language,
                    current_level=data.current_level,
                    last_lesson_topic=data.last_lesson_topic or "Introduction",
                    learning_focus=data.learning_focus,
                    seed=data.seed,
                    user_custom_instruction=data.user_custom_instruction
                )
                logger.info(f"Lesson generated: {prediction.lesson_title}")
                return prediction
        except Exception as e:
            logger.error(f"Lesson Service Error: {str(e)}")
            raise e

    def translate_text(self, data: TranslationRequest):
        """
        Translates text with high contextual awareness using DSPy.
        
        Args:
            data: The validated TranslationRequest.
            
        Returns:
            Prediction object with translated text and rationale.
        """
        try:
            with dspy.context(lm=self.lm):
                translator = dspy.ChainOfThought(ContextualTranslator)
                prediction = translator(
                    text_to_translate=data.text_to_translate,
                    source_language=data.source_language,
                    target_language=data.target_language,
                    tone=data.tone,
                    reference_material=data.reference_material,
                    custom_instructions=data.custom_instructions
                )
                logger.info(f"Translation completed to {data.target_language}")
                return prediction
        except Exception as e:
            logger.error(f"Translation Service Error: {str(e)}")
            raise e

    def rewrite_content(self, data: RewriteRequest):
        """
        Adjusts text style, tone, and complexity.
        """
        # Rewriting often benefits from a slightly higher temperature (0.7)
        rewrite_lm = dspy.LM(
            model=f"openai/{config['model_name']}",
            api_key=config['api_key'],
            api_base=config['api_base'],
            temperature=0.7,
            cache=False
        )
        try:
            with dspy.context(lm=rewrite_lm):
                editor = dspy.ChainOfThought(TextRewriter)
                prediction = editor(
                    original_text=data.original_text,
                    target_tone=data.target_tone,
                    audience=data.audience,
                    transformation_goal=data.transformation_goal,
                    custom_instructions=data.custom_instructions
                )
                logger.info(f"Text rewritten with goal: {data.transformation_goal}")
                return prediction
        except Exception as e:
            logger.error(f"Rewriter Service Error: {str(e)}")
            raise e