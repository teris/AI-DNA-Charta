"""
AI-DNA Charter Framework
Ethical AI implementation framework based on the AI-DNA Charter v2.1.1
With multilingual support
"""

from .ai_dna_framework import (
    CharteredAI,
    DecisionContext,
    EthicalViolation,
    ParadigmType,
    Layer1EthicsCore,
    DiversityChecker,
    create_basic_chartered_ai,
    create_stream_setup,
    create_consensus_system,
    demo_chartered_ai_extended
)

from .language_manager import (
    Language,
    LanguageManager,
    lang,
    _,
    set_language,
    get_language
)

__version__ = "2.1.1"
__author__ = "TerisC"
__charter_version__ = "2.1.1"

__all__ = [
    # Core Framework
    "CharteredAI",
    "DecisionContext", 
    "EthicalViolation",
    "ParadigmType",
    "Layer1EthicsCore",
    "DiversityChecker",
    # Factory functions
    "create_basic_chartered_ai",
    "create_stream_setup",
    "create_consensus_system",
    "demo_chartered_ai_extended",
    # Language support
    "Language",
    "LanguageManager",
    "lang",
    "_",
    "set_language",
    "get_language"
]

# Initialize language system on import
import os

# Set default language from environment or use German
default_lang_code = os.environ.get('AI_DNA_LANGUAGE', 'de').lower()
try:
    default_lang = Language(default_lang_code)
    set_language(default_lang)
except ValueError:
    # Fallback to German if invalid language code
    set_language(Language.DE)

# Log available languages
available_langs = lang.get_available_languages()
if available_langs:
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"AI-DNA Charter Framework v{__version__} initialized")
    logger.info(f"Available languages: {', '.join([l['code'] for l in available_langs])}")
    logger.info(f"Current language: {get_language().value}")
