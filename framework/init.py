"""
AI-DNA Charter Framework
Ethical AI implementation framework based on the AI-DNA Charter v2.1.1
"""

from .ai_dna_framework import (
    CharteredAI,
    DecisionContext,
    EthicalViolation,
    ParadigmType,
    Layer1EthicsCore,
    DiversityChecker
)

__version__ = "2.1.1"
__author__ = "TerisC"
__charter_version__ = "2.1.1"

__all__ = [
    "CharteredAI",
    "DecisionContext", 
    "EthicalViolation",
    "ParadigmType",
    "Layer1EthicsCore",
    "DiversityChecker"
]
