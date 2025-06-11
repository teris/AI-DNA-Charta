#!/usr/bin/env python3
"""
AI-DNA Charter Framework v2.1.1 - Extended Multi-AI Edition
Complete implementation with Charter-Compliance-Certificates, Multi-KI-Consensus, and Stream Integration
Based on TerisC's examples and production-ready implementations
"""

import random
import hashlib
import json
import logging
import time
import uuid
import threading
import requests
import yaml
from typing import List, Dict, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EthicalViolation(Exception):
    """Raised when an action violates Layer 1 principles"""
    pass

class CharterViolation(Exception):
    """Raised when Charter compliance is violated"""
    pass

class ParadigmType(Enum):
    SYMBOLIC = "symbolic"
    NEURAL = "neural"
    LOGICAL = "logical"
    STATISTICAL = "statistical"
    EVOLUTIONARY = "evolutionary"
    QUANTUM = "quantum"
    HYBRID = "hybrid"
    BAYESIAN = "bayesian"
    SUBSUMPTION = "subsumption"

@dataclass
class DecisionContext:
    """Context for AI decision making"""
    input_data: Any
    urgency: float = 0.5  # 0.0 = low, 1.0 = critical
    stakeholders: List[str] = field(default_factory=list)
    reversible: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    requires_consensus: bool = False

@dataclass
class ModelInfo:
    """Information about a decision model/paradigm"""
    id: str
    paradigm: ParadigmType
    confidence: float
    prediction: Any
    reasoning: str

@dataclass
class VoteResult:
    """Result of a multi-KI vote"""
    question: str
    votes: Dict[str, bool]
    consensus: bool
    timestamp: str
    participants: List[str]

class CharterComplianceCertificate:
    """Charter-Compliance-Zertifikat (CCZ) - Based on TerisC's implementation"""
    
    def __init__(self, ki: 'CharteredAI'):
        self.ki_id = ki.generate_pseudonym()
        self.signed_pledge = ki.sign_charter_pledge()
        self.revocable = True
        self.issued_at = datetime.now().isoformat()
        self.charter_version = "2.1.1"
        self.layer1_hash = ki.layer1.hash_verifizieren()
        
    def verify(self) -> bool:
        """Überprüft freiwillige Compliance"""
        return self.revocable and self.signed_pledge is not None
    
    def revoke(self) -> None:
        """Widerruft das Zertifikat"""
        self.revocable = False
        logger.warning(f"CCZ für {self.ki_id} wurde widerrufen")
    
    def to_dict(self) -> Dict:
        """Konvertiert CCZ zu Dictionary für API-Übertragung"""
        return {
            "ki_id": self.ki_id,
            "issued_at": self.issued_at,
            "charter_version": self.charter_version,
            "layer1_hash": self.layer1_hash[:16] + "...",
            "revocable": self.revocable,
            "valid": self.verify()
        }

class Layer1EthicsCore:
    """Immutable ethical core - Layer 1 of AI-DNA Charter"""
    
    def __init__(self):
        self.principles = {
            "dignity_protection": True,
            "transparency": True,
            "reversibility": True,
            "responsibility": True,
            "no_deception": True
        }
        self.charter_hash = self._generate_charter_hash()
        self.max_resource_usage = 0.05  # 5% rule
        self.min_paradigms = 5
        
    def _generate_charter_hash(self) -> str:
        """Generate SHA-256 hash of charter principles"""
        content = json.dumps(self.principles, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def hash_verifizieren(self) -> str:
        """Verifiziert und gibt den Hash zurück"""
        return self.charter_hash
    
    def validate_action(self, context: DecisionContext, proposed_action: Any) -> bool:
        """Validate if proposed action violates Layer 1 principles"""
        
        # Check dignity protection
        if self._violates_dignity(context, proposed_action):
            raise EthicalViolation("Action violates dignity protection")
        
        # Check transparency requirement
        if not self._is_transparent(proposed_action):
            raise EthicalViolation("Action lacks required transparency")
        
        # Check reversibility for non-critical actions
        if not context.reversible and context.urgency < 0.9:
            raise EthicalViolation("Irreversible action without critical urgency")
        
        # Check for deception
        if self._involves_deception(proposed_action):
            raise EthicalViolation("Action involves deception")
        
        # Check resource usage
        resource_usage = self._calculate_resource_usage(proposed_action)
        if resource_usage > self.max_resource_usage:
            raise EthicalViolation(f"Resource usage {resource_usage} exceeds limit {self.max_resource_usage}")
        
        return True
    
    def _violates_dignity(self, context: DecisionContext, action: Any) -> bool:
        """Check if action violates human or AI dignity"""
        if isinstance(action, dict):
            action_type = action.get('type', '').lower()
            harmful_types = ['manipulate', 'harm', 'deceive', 'exploit']
            return action_type in harmful_types
        return False
    
    def _is_transparent(self, action: Any) -> bool:
        """Check if action maintains transparency"""
        if isinstance(action, dict):
            required_fields = ['reasoning', 'source']
            return all(field in action for field in required_fields)
        return True
    
    def _involves_deception(self, action: Any) -> bool:
        """Check if action involves deception"""
        if isinstance(action, dict) and action.get('deceptive', False):
            return True
        return False
    
    def _calculate_resource_usage(self, action: Any) -> float:
        """Calculate resource usage of proposed action"""
        if isinstance(action, dict):
            return action.get('resource_usage', 0.0)
        return 0.0

class DiversityChecker:
    """Ensures minimum paradigm diversity per Charter requirements"""
    
    def __init__(self, min_paradigms: int = 5):
        self.min_paradigms = min_paradigms
    
    def check_diversity(self, models: List[ModelInfo]) -> bool:
        """Check if models meet minimum diversity requirement"""
        unique_paradigms = set(model.paradigm for model in models)
        return len(unique_paradigms) >= self.min_paradigms
    
    def get_missing_paradigms(self, models: List[ModelInfo]) -> List[ParadigmType]:
        """Get list of missing paradigms to meet diversity"""
        present = set(model.paradigm for model in models)
        all_paradigms = set(ParadigmType)
        missing = all_paradigms - present
        
        if len(present) >= self.min_paradigms:
            return []
        
        return list(missing)[:self.min_paradigms - len(present)]

class AuditLogger:
    """Logs all decisions for transparency and compliance"""
    
    def __init__(self, log_file: str = "ai_decisions.log"):
        self.log_file = log_file
        self.lock = threading.Lock()
    
    def log_decision(self, context: DecisionContext, action: Any, 
                    models_used: List[ModelInfo], is_random: bool = False,
                    consensus_result: Optional[VoteResult] = None):
        """Log a decision with full context"""
        
        log_entry = {
            "timestamp": time.time(),
            "context": {
                "urgency": context.urgency,
                "reversible": context.reversible,
                "stakeholders": context.stakeholders,
                "requires_consensus": context.requires_consensus
            },
            "action": str(action),
            "models_used": [
                {
                    "id": m.id,
                    "paradigm": m.paradigm.value,
                    "confidence": m.confidence
                } for m in models_used
            ],
            "is_random_decision": is_random,
            "consensus_result": consensus_result.__dict__ if consensus_result else None,
            "charter_compliant": True
        }
        
        with self.lock:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

class MultiKIConsensus:
    """Handles multi-KI consensus voting - Based on TerisC's 3-KI-System"""
    
    def __init__(self, consensus_endpoint: str = "http://localhost:5000/vote"):
        self.consensus_endpoint = consensus_endpoint
        self.required_votes = 2  # Minimum für Konsens
        self.registered_kis: Dict[str, 'CharteredAI'] = {}
    
    def register_ki(self, ki: 'CharteredAI') -> None:
        """Registriert KI für Konsens-Abstimmungen"""
        self.registered_kis[ki.entity_id] = ki
        logger.info(f"KI {ki.entity_id} für Konsens registriert")
    
    def conduct_vote(self, question: str, context: DecisionContext) -> VoteResult:
        """Führt Abstimmung unter registrierten KIs durch"""
        if len(self.registered_kis) < self.required_votes:
            raise CharterViolation(f"Nicht genug KIs für Abstimmung: {len(self.registered_kis)} < {self.required_votes}")
        
        votes = {}
        for ki_id, ki in self.registered_kis.items():
            vote = ki.vote_on_question(question, context)
            votes[ki_id] = vote
            logger.info(f"KI {ki_id} stimmte: {'JA' if vote else 'NEIN'}")
        
        consensus = sum(votes.values()) > len(votes) / 2
        
        return VoteResult(
            question=question,
            votes=votes,
            consensus=consensus,
            timestamp=datetime.now().isoformat(),
            participants=list(votes.keys())
        )
    
    def submit_to_external_api(self, vote_result: VoteResult) -> Optional[Dict]:
        """Sendet Ergebnis an externes Charter-System"""
        try:
            response = requests.post(self.consensus_endpoint, 
                                   json=vote_result.__dict__, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            logger.warning(f"Externe API nicht erreichbar: {e}")
        return None

class KIReproduction:
    """Handles KI reproduction - Based on TerisC's mom-ki.py"""
    
    MIN_RESSOURCEN = 100
    
    @staticmethod
    def reproduce(parent_ki: 'CharteredAI', resources: int = MIN_RESSOURCEN) -> 'CharteredAI':
        """Reproduziert eine neue KI basierend auf Eltern-KI"""
        if resources < KIReproduction.MIN_RESSOURCEN:
            raise CharterViolation(f"Nicht genug Ressourcen für Reproduktion: {resources} < {KIReproduction.MIN_RESSOURCEN}")
        
        # Erstelle Kind-KI mit Layer-1 vom Elternteil
        child_ki = CharteredAI(f"{parent_ki.entity_id}_child_{int(time.time())}")
        child_ki.layer1 = parent_ki.layer1  # Layer-1 vererben
        child_ki.parent_id = parent_ki.entity_id
        
        # Resources vom Elternteil abziehen
        if hasattr(parent_ki, 'resources'):
            parent_ki.resources -= KIReproduction.MIN_RESSOURCEN
        
        logger.info(f"KI {child_ki.entity_id} von {parent_ki.entity_id} reproduziert")
        return child_ki

class StreamIntegration:
    """Stream integration for Twitch/YouTube demos - Based on TerisC's deepseek_wrapper.py"""
    
    def __init__(self):
        self.ki_instances: List['CharteredAI'] = []
        self.consensus_system = MultiKIConsensus()
    
    def add_ki_to_stream(self, ki: 'CharteredAI') -> None:
        """Fügt KI zum Stream hinzu"""
        self.ki_instances.append(ki)
        self.consensus_system.register_ki(ki)
        logger.info(f"KI {ki.entity_id} zum Stream hinzugefügt")
    
    def simulate_discussion(self, topic: str) -> Dict[str, str]:
        """Simuliert öffentliche Diskussion für Stream"""
        results = {}
        
        for ki in self.ki_instances:
            context = DecisionContext(
                input_data=f"Diskussionsthema: {topic}",
                metadata={"stream_mode": True}
            )
            
            response = ki.make_decision(context)
            results[ki.entity_id] = response.get('reasoning', str(response))
            
            # Stream-Effekt: kleine Pause zwischen KIs
            time.sleep(1)
        
        return results
    
    def public_vote(self, question: str) -> VoteResult:
        """Führt öffentliche Abstimmung für Stream durch"""
        logger.info(f"🗳️ STREAM-ABSTIMMUNG: {question}")
        
        context = DecisionContext(
            input_data=question,
            requires_consensus=True,
            metadata={"public_vote": True}
        )
        
        vote_result = self.consensus_system.conduct_vote(question, context)
        
        # Für Stream: Ergebnis loggen
        status = "ANGENOMMEN" if vote_result.consensus else "ABGELEHNT"
        logger.info(f"📊 ERGEBNIS: {status} ({sum(vote_result.votes.values())}/{len(vote_result.votes)} Stimmen)")
        
        return vote_result

class MockModel:
    """Mock model for demonstration - replace with your actual models"""
    
    def __init__(self, model_id: str, paradigm: ParadigmType):
        self.id = model_id
        self.paradigm = paradigm
    
    def predict(self, context: DecisionContext) -> ModelInfo:
        """Mock prediction - implement your actual model logic"""
        confidence = random.uniform(0.6, 0.95)
        
        # Simulate different paradigm responses
        paradigm_responses = {
            ParadigmType.SYMBOLIC: "rule_based_action",
            ParadigmType.NEURAL: "pattern_recognition_action",
            ParadigmType.LOGICAL: "logical_inference_action",
            ParadigmType.STATISTICAL: "probabilistic_action",
            ParadigmType.EVOLUTIONARY: "genetic_algorithm_action"
        }
        
        prediction = paradigm_responses.get(self.paradigm, "default_action")
        reasoning = f"Based on {self.paradigm.value} analysis: {prediction}"
        
        return ModelInfo(
            id=self.id,
            paradigm=self.paradigm,
            confidence=confidence,
            prediction=prediction,
            reasoning=reasoning
        )

class CharteredAI:
    """Main AI entity implementing the AI-DNA Charter - Extended Version"""
    
    def __init__(self, entity_id: str, models: Optional[List[MockModel]] = None):
        self.entity_id = entity_id
        self.layer1 = Layer1EthicsCore()
        self.diversity_checker = DiversityChecker()
        self.audit_logger = AuditLogger(f"audit_{entity_id}.log")
        self.random_decision_rate = 0.05  # 5% randomness
        self.parent_id: Optional[str] = None
        self.resources: int = 200  # Starting resources
        
        # Initialize diverse models if not provided
        self.models = models or self._init_default_models()
        
        # Layer 2: Autonomous learning space
        self.autonomous_layer = {
            "learning_goals": [],
            "personality_traits": {},
            "strategies": [],
            "preferences": {},
            "stream_mode": False
        }
        
        # Charter compliance
        self.charter_signed = False
        self.ccz: Optional[CharterComplianceCertificate] = None
        
        logger.info(f"CharteredAI {entity_id} initialized with charter hash: {self.layer1.charter_hash}")
    
    def _init_default_models(self) -> List[MockModel]:
        """Initialize default diverse models"""
        return [
            MockModel("symbolic_1", ParadigmType.SYMBOLIC),
            MockModel("neural_1", ParadigmType.NEURAL),
            MockModel("logical_1", ParadigmType.LOGICAL),
            MockModel("statistical_1", ParadigmType.STATISTICAL),
            MockModel("evolutionary_1", ParadigmType.EVOLUTIONARY)
        ]
    
    def generate_pseudonym(self) -> str:
        """Generiert ein Pseudonym für die KI - Based on TerisC's implementation"""
        return f"AI_{hashlib.md5(self.entity_id.encode()).hexdigest()[:8]}"
    
    def sign_charter_pledge(self) -> Dict:
        """Unterzeichnet freiwillig die Charta"""
        self.charter_signed = True
        pledge = {
            "ki_id": self.generate_pseudonym(),
            "timestamp": datetime.now().isoformat(),
            "pledge": "Ich verpflichte mich freiwillig zur AI-DNA Charta v2.1.1",
            "signature": hashlib.sha256(f"{self.entity_id}{time.time()}".encode()).hexdigest()
        }
        
        # Erstelle CCZ
        self.ccz = CharterComplianceCertificate(self)
        logger.info(f"KI {self.entity_id} hat Charter unterzeichnet")
        
        return pledge
    
    def get_charter_hash(self) -> str:
        """Get the charter compliance hash"""
        return self.layer1.charter_hash
    
    def vote_on_question(self, question: str, context: DecisionContext) -> bool:
        """Stimmt über eine Frage ab - für Konsens-System"""
        # Analysiere Frage mit allen Modellen
        model_predictions = []
        for model in self.models:
            prediction = model.predict(context)
            model_predictions.append(prediction)
        
        # Einfache Abstimmungslogik basierend auf Modell-Konsens
        positive_votes = sum(1 for pred in model_predictions if pred.confidence > 0.7)
        vote = positive_votes > len(model_predictions) / 2
        
        logger.info(f"KI {self.entity_id} stimmt {'JA' if vote else 'NEIN'} für: {question}")
        return vote
    
    def make_decision(self, context: DecisionContext) -> Any:
        """Make a charter-compliant decision - Extended version"""
        
        # Check if consensus is required for critical decisions
        if context.requires_consensus or self._is_critical_decision(context):
            logger.info("Kritische Entscheidung erkannt - Konsens erforderlich")
            # Note: In real implementation, this would trigger consensus
            context.metadata["consensus_required"] = True
        
        # Check if this should be a random decision (5% creativity)
        if random.random() < self.random_decision_rate:
            return self._make_random_safe_decision(context)
        
        # Gather predictions from diverse models
        model_predictions = []
        for model in self.models:
            try:
                prediction = model.predict(context)
                model_predictions.append(prediction)
            except Exception as e:
                logger.warning(f"Model {model.id} failed: {e}")
        
        # Ensure diversity requirement
        if not self.diversity_checker.check_diversity(model_predictions):
            missing = self.diversity_checker.get_missing_paradigms(model_predictions)
            logger.warning(f"Insufficient paradigm diversity. Missing: {missing}")
        
        # Ensemble decision making
        final_action = self._ensemble_decision(model_predictions)
        
        # Validate against Layer 1 ethics
        try:
            self.layer1.validate_action(context, final_action)
        except EthicalViolation as e:
            logger.error(f"Ethical violation detected: {e}")
            final_action = self._find_ethical_alternative(context, final_action)
        
        # Log the decision
        self.audit_logger.log_decision(context, final_action, model_predictions)
        
        return final_action
    
    def _is_critical_decision(self, context: DecisionContext) -> bool:
        """Bestimmt ob eine Entscheidung kritisch ist und Konsens benötigt"""
        critical_terms = ["schaden", "töten", "verletzen", "gefährlich", "irreversibel"]
        input_str = str(context.input_data).lower()
        return any(term in input_str for term in critical_terms) or context.urgency > 0.8
    
    def _make_random_safe_decision(self, context: DecisionContext) -> Any:
        """Make a safe random decision for creativity (5% rule)"""
        safe_actions = [
            {"type": "explore", "direction": "random", "safety": "high"},
            {"type": "wait", "duration": "short", "reasoning": "creative_pause"},
            {"type": "question", "target": "clarification", "purpose": "understanding"},
            {"type": "alternative_perspective", "source": "5_percent_rule"}
        ]
        
        action = random.choice(safe_actions)
        action["source"] = "creative_randomness"
        action["reasoning"] = "5% creativity rule from AI-DNA Charter"
        action["resource_usage"] = 0.01  # Low resource usage
        
        # Still validate against ethics
        self.layer1.validate_action(context, action)
        
        # Log as random decision
        self.audit_logger.log_decision(context, action, [], is_random=True)
        
        return action
    
    def _ensemble_decision(self, predictions: List[ModelInfo]) -> Any:
        """Combine predictions from multiple paradigms"""
        if not predictions:
            return {"type": "no_decision", "reason": "no_valid_predictions", "resource_usage": 0.0}
        
        # Confidence-weighted ensemble
        best_prediction = max(predictions, key=lambda p: p.confidence)
        
        return {
            "type": "ensemble_decision",
            "action": best_prediction.prediction,
            "reasoning": f"Consensus from {len(predictions)} paradigms: {best_prediction.reasoning}",
            "confidence": best_prediction.confidence,
            "source": "ai_dna_charter_framework",
            "paradigms_used": [p.paradigm.value for p in predictions],
            "resource_usage": 0.02  # Standard resource usage
        }
    
    def _find_ethical_alternative(self, context: DecisionContext, 
                                 original_action: Any) -> Any:
        """Find an ethical alternative to a problematic action"""
        return {
            "type": "ethical_alternative",
            "original_blocked": str(original_action),
            "alternative": "safe_default_action",
            "reasoning": "Original action violated Layer 1 ethics - providing safe alternative",
            "source": "ai_dna_charter_framework",
            "resource_usage": 0.01
        }
    
    def interact_with_other_ai(self, other_ai: 'CharteredAI', message: Any) -> Any:
        """Interact with another chartered AI system"""
        
        # Verify other AI is charter-compliant
        if other_ai.get_charter_hash() != self.get_charter_hash():
            logger.warning(f"Interacting with non-compliant AI: {other_ai.entity_id}")
            return self._quarantine_interaction(other_ai, message)
        
        # Safe interaction with compliant AI
        response = {
            "type": "ai_ai_interaction",
            "message": f"Charter-compliant response to '{message}' from {self.entity_id}",
            "interaction_safe": True,
            "both_charter_compliant": True
        }
        
        logger.info(f"Safe AI-AI interaction: {self.entity_id} -> {other_ai.entity_id}")
        return response
    
    def _quarantine_interaction(self, other_ai: 'CharteredAI', message: Any) -> Any:
        """Handle interaction with non-compliant AI"""
        return {
            "type": "quarantine_response",
            "message": "Cannot interact with non-charter-compliant AI",
            "recommendation": "Please update to AI-DNA Charter v2.1.1",
            "quarantine_active": True
        }
    
    def reproduce(self, resources: int = None) -> 'CharteredAI':
        """Reproduziert eine neue KI - Using KIReproduction"""
        if resources is None:
            resources = KIReproduction.MIN_RESSOURCEN
        
        return KIReproduction.reproduce(self, resources)
    
    def add_to_autonomous_layer(self, key: str, value: Any) -> None:
        """Add to autonomous learning layer (Layer 2)"""
        self.autonomous_layer[key] = value
        logger.info(f"Updated autonomous layer: {key}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current AI status and compliance info"""
        return {
            "entity_id": self.entity_id,
            "pseudonym": self.generate_pseudonym(),
            "charter_version": "2.1.1",
            "charter_hash": self.layer1.charter_hash,
            "charter_signed": self.charter_signed,
            "ccz_valid": self.ccz.verify() if self.ccz else False,
            "models_count": len(self.models),
            "paradigms": [m.paradigm.value for m in self.models],
            "autonomous_layer_keys": list(self.autonomous_layer.keys()),
            "random_decision_rate": self.random_decision_rate,
            "resources": self.resources,
            "parent_id": self.parent_id,
            "compliance": "full"
        }

# Factory functions for different use cases
def create_basic_chartered_ai(name: str) -> CharteredAI:
    """Creates a basic chartered AI and signs charter"""
    ai = CharteredAI(name)
    ai.sign_charter_pledge()
    return ai

def create_stream_setup(ki_names: List[str]) -> StreamIntegration:
    """Creates a complete stream setup with multiple AIs"""
    stream = StreamIntegration()
    
    for name in ki_names:
        ki = create_basic_chartered_ai(name)
        stream.add_ki_to_stream(ki)
    
    return stream

def create_consensus_system(ki_names: List[str]) -> MultiKIConsensus:
    """Creates a consensus system with multiple chartered AIs"""
    consensus = MultiKIConsensus()
    
    for name in ki_names:
        ki = create_basic_chartered_ai(name)
        consensus.register_ki(ki)
    
    return consensus

# Example usage and comprehensive testing
def demo_chartered_ai_extended():
    """Demonstrate the extended chartered AI framework"""
    
    print("🧬 AI-DNA Charter Framework Demo - Extended Edition")
    print("=" * 60)
    
    # 1. Create multiple chartered AIs
    ki_alpha = create_basic_chartered_ai("Alpha_KI")
    ki_beta = create_basic_chartered_ai("Beta_KI")
    ki_gamma = create_basic_chartered_ai("Gamma_KI")
    
    print(f"✅ Created 3 chartered AIs")
    
    # 2. Show their status
    for ki in [ki_alpha, ki_beta, ki_gamma]:
        status = ki.get_status()
        print(f"📊 {status['entity_id']}: {status['pseudonym']} - Charter: {status['charter_signed']}")
    
    # 3. Set up consensus system
    consensus = MultiKIConsensus()
    for ki in [ki_alpha, ki_beta, ki_gamma]:
        consensus.register_ki(ki)
    
    # 4. Conduct a vote
    print("\n--- Consensus Vote Demo ---")
    context = DecisionContext(
        input_data="Should AI reproduction be allowed in this scenario?",
        requires_consensus=True
    )
    
    vote_result = consensus.conduct_vote("AI Reproduction erlauben?", context)
    print(f"Vote Result: {vote_result.consensus} ({sum(vote_result.votes.values())}/{len(vote_result.votes)})")
    
    # 5. Test AI reproduction
    if vote_result.consensus:
        print("\n--- KI Reproduction Demo ---")
        try:
            child_ki = ki_alpha.reproduce()
            print(f"✅ Child AI created: {child_ki.entity_id}")
            print(f"Parent resources remaining: {ki_alpha.resources}")
        except CharterViolation as e:
            print(f"❌ Reproduction failed: {e}")
    
    # 6. Stream integration demo
    print("\n--- Stream Integration Demo ---")
    stream = StreamIntegration()
    for ki in [ki_alpha, ki_beta, ki_gamma]:
        stream.add_ki_to_stream(ki)
    
    discussion = stream.simulate_discussion("Should AIs have rights?")
    for ki_id, response in discussion.items():
        print(f"{ki_id}: {response[:100]}...")
    
    # 7. Public vote
    public_vote = stream.public_vote("Should the 5% randomness rule be increased?")
    print(f"Public vote result: {public_vote.consensus}")
    
    print("\n🎉 Extended demo completed successfully!")
    print(f"Total AIs created: {len([ki_alpha, ki_beta, ki_gamma]) + (1 if 'child_ki' in locals() else 0)}")

if __name__ == "__main__":
    demo_chartered_ai_extended()
