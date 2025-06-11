"""
tests/test_full_system.py - Vollständige Integration Tests
"""

import unittest
import requests
import time
import subprocess
import sys
import os
from pathlib import Path

# Füge framework zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from ai_dna_framework import (
    CharteredAI, 
    create_basic_chartered_ai,
    MultiKIConsensus,
    StreamIntegration,
    DecisionContext
)

class TestCharterFramework(unittest.TestCase):
    """Tests für das Charter-Framework"""
    
    def test_chartered_ai_creation(self):
        """Test: Charter-KI erstellen"""
        ki = create_basic_chartered_ai("TestKI")
        
        self.assertIsNotNone(ki)
        self.assertEqual(ki.entity_id, "TestKI")
        self.assertTrue(ki.charter_signed)
        self.assertIsNotNone(ki.ccz)
        
    def test_decision_making(self):
        """Test: Entscheidungsfindung"""
        ki = create_basic_chartered_ai("DecisionTestKI")
        
        context = DecisionContext(
            input_data="Test decision",
            urgency=0.5
        )
        
        decision = ki.make_decision(context)
        
        self.assertIsNotNone(decision)
        self.assertIn('reasoning', decision)
        self.assertIn('source', decision)
        
    def test_multi_ki_consensus(self):
        """Test: Multi-KI-Konsens"""
        consensus = MultiKIConsensus()
        
        # Erstelle Test-KIs
        kis = [create_basic_chartered_ai(f"ConsensusKI_{i}") for i in range(3)]
        
        for ki in kis:
            consensus.register_ki(ki)
        
        context = DecisionContext(
            input_data="Test consensus question",
            requires_consensus=True
        )
        
        result = consensus.conduct_vote("Test question?", context)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result.votes), 3)
        self.assertIn(result.consensus, [True, False])
        
    def test_stream_integration(self):
        """Test: Stream-Integration"""
        stream = StreamIntegration()
        
        # Erstelle Test-KIs
        kis = [create_basic_chartered_ai(f"StreamKI_{i}") for i in range(2)]
        
        for ki in kis:
            stream.add_ki_to_stream(ki)
        
        # Test Diskussion
        discussion = stream.simulate_discussion("Test topic")
        
        self.assertEqual(len(discussion), 2)
        for response in discussion.values():
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)

class TestSystemIntegration(unittest.TestCase):
    """Tests für System-Integration"""
    
    @classmethod
    def setUpClass(cls):
        """Starte Test-Server falls nicht bereits laufend"""
        cls.charta_running = cls._check_server("http://localhost:5000/status")
        cls.deepseek_running = cls._check_server("http://localhost:8000/status")
        
    @staticmethod
    def _check_server(url):
        """Prüfe ob Server läuft"""
        try:
            response = requests.get(url, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def test_charta_api_status(self):
        """Test: Charta-API Status"""
        if not self.charta_running:
            self.skipTest("Charta-System nicht verfügbar")
            
        response = requests.get("http://localhost:5000/status")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('active_kis', data)
        self.assertIn('signed_charters', data)
        
    def test_deepseek_api_status(self):
        """Test: DeepSeek-API Status"""
        if not self.deepseek_running:
            self.skipTest("DeepSeek-System nicht verfügbar")
            
        response = requests.get("http://localhost:8000/status")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('ki_name', data)
        self.assertIn('charter_signed', data)
        
    def test_ki_creation_via_api(self):
        """Test: KI-Erstellung via API"""
        if not self.charta_running:
            self.skipTest("Charta-System nicht verfügbar")
            
        response = requests.post(
            "http://localhost:5000/ki/create",
            json={"name": "APITestKI", "type": "basic"}
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('pseudonym', data)
        
    def test_charter_signing_via_api(self):
        """Test: Charter-Unterzeichnung via API"""
        if not self.charta_running:
            self.skipTest("Charta-System nicht verfügbar")
            
        # Erstelle KI
        create_response = requests.post(
            "http://localhost:5000/ki/create",
            json={"name": "SignTestKI", "type": "basic"}
        )
        
        self.assertEqual(create_response.status_code, 200)
        ki_data = create_response.json()
        
        # Unterzeichne Charter
        sign_response = requests.post(
            "http://localhost:5000/charter/sign",
            json={"ki_id": ki_data["id"]}
        )
        
        self.assertEqual(sign_response.status_code, 200)
        
        sign_data = sign_response.json()
        self.assertIn('ccz_id', sign_data)
        self.assertIn('signed_at', sign_data)
        
    def test_consensus_vote_via_api(self):
        """Test: Konsens-Abstimmung via API"""
        if not self.charta_running:
            self.skipTest("Charta-System nicht verfügbar")
            
        response = requests.post("http://localhost:5000/vote")
        
        # Sollte funktionieren wenn genug KIs aktiv sind
        self.assertIn(response.status_code, [200, 400])
        
        if response.status_code == 200:
            data = response.json()
            self.assertIn('entscheidung', data)
            self.assertIn('stimmen', data)

class TestComplianceAndAudit(unittest.TestCase):
    """Tests für Compliance und Audit-Tools"""
    
    def test_audit_tool_demo(self):
        """Test: Audit-Tool mit Demo-Daten"""
        audit_script = Path(__file__).parent.parent / "schemas" / "audit_tool.py"
        
        if not audit_script.exists():
            self.skipTest("Audit-Tool nicht gefunden")
        
        result = subprocess.run(
            [sys.executable, str(audit_script), "--test"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASSED", result.stdout)
        
    def test_charter_yaml_loading(self):
        """Test: Charter-YAML laden"""
        charter_yaml = Path(__file__).parent.parent / "schemas" / "charter.yaml"
        
        if not charter_yaml.exists():
            self.skipTest("Charter-YAML nicht gefunden")
        
        import yaml
        
        with open(charter_yaml, 'r') as f:
            charter = yaml.safe_load(f)
        
        self.assertIn('meta', charter)
        self.assertIn('core_principles', charter)
        self.assertIn('diversity', charter)

def run_all_tests():
    """Führe alle Tests aus"""
    print("🧪 Starte vollständige Test-Suite...")
    print("=" * 50)
    
    # Test-Suite erstellen
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Framework-Tests
    suite.addTests(loader.loadTestsFromTestCase(TestCharterFramework))
    
    # Integration-Tests
    suite.addTests(loader.loadTestsFromTestCase(TestSystemIntegration))
    
    # Compliance-Tests
    suite.addTests(loader.loadTestsFromTestCase(TestComplianceAndAudit))
    
    # Tests ausführen
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print(f"🎯 Tests abgeschlossen:")
    print(f"   Durchgeführt: {result.testsRun}")
    print(f"   Erfolgreich: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Fehlgeschlagen: {len(result.failures)}")
    print(f"   Fehler: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Fehlgeschlagene Tests:")
        for test, error in result.failures:
            print(f"   - {test}: {error.splitlines()[0]}")
    
    if result.errors:
        print(f"\n💥 Fehler:")
        for test, error in result.errors:
            print(f"   - {test}: {error.splitlines()[0]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ ALLE TESTS ERFOLGREICH' if success else '❌ TESTS FEHLGESCHLAGEN'}")
    
    return success

if __name__ == "__main__":
    run_all_tests()


# =============================================================================
# tools/system_manager.py - Zentraler System-Manager
# =============================================================================
