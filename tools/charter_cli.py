#!/usr/bin/env python3
"""
tools/charter_cli.py - Command Line Interface für AI-DNA Charter System
Integriert alle Components und ermöglicht einfache Nutzung
"""

import argparse
import sys
import os
import json
import yaml
import subprocess
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional

# Füge framework zum Python Path hinzu
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

try:
    from ai_dna_framework import (
        CharteredAI, 
        create_basic_chartered_ai, 
        create_stream_setup,
        create_consensus_system,
        demo_chartered_ai_extended
    )
except ImportError:
    print("❌ Framework nicht gefunden. Stelle sicher, dass du im Hauptverzeichnis bist.")
    sys.exit(1)

class CharterCLI:
    """CLI für AI-DNA Charter System"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.examples_dir = self.base_dir / "examples"
        self.framework_dir = self.base_dir / "framework"
        
    def cmd_create_ki(self, args):
        """Erstelle eine neue Charter-konforme KI"""
        print(f"🤖 Erstelle KI: {args.name}")
        
        ki = create_basic_chartered_ai(args.name)
        status = ki.get_status()
        
        print(f"✅ KI erstellt:")
        print(f"   ID: {status['entity_id']}")
        print(f"   Pseudonym: {status['pseudonym']}")
        print(f"   Charter unterzeichnet: {status['charter_signed']}")
        print(f"   Paradigmen: {len(status['paradigms'])}")
        
        # Optional: Speichere KI-Config
        if args.save:
            config = {
                "entity_id": status['entity_id'],
                "charter_signed": status['charter_signed'],
                "created_at": time.time()
            }
            
            config_file = self.base_dir / f"generated_kis/{args.name}.json"
            config_file.parent.mkdir(exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"💾 Konfiguration gespeichert: {config_file}")
    
    def cmd_start_system(self, args):
        """Starte das komplette Charter-System"""
        print("🚀 Starte AI-DNA Charter System...")
        
        # Prüfe Dependencies
        if not self._check_dependencies():
            return
        
        if args.mode == "full":
            self._start_full_system()
        elif args.mode == "charta":
            self._start_charta_only()
        elif args.mode == "deepseek":
            self._start_deepseek_only()
        else:
            print(f"❌ Unbekannter Modus: {args.mode}")
    
    def cmd_test_system(self, args):
        """Führe System-Tests durch"""
        print("🧪 Teste AI-DNA Charter System...")
        
        # Framework-Tests
        if args.component in ["all", "framework"]:
            print("\n--- Framework Tests ---")
            try:
                demo_chartered_ai_extended()
                print("✅ Framework-Tests erfolgreich")
            except Exception as e:
                print(f"❌ Framework-Tests fehlgeschlagen: {e}")
        
        # API-Tests
        if args.component in ["all", "api"]:
            print("\n--- API Tests ---")
            self._test_apis()
        
        # Integration Tests
        if args.component in ["all", "integration"]:
            print("\n--- Integration Tests ---")
            self._test_integration()
    
    def cmd_audit(self, args):
        """Führe Charter-Compliance-Audit durch"""
        print(f"🔍 Führe Audit durch: {args.config}")
        
        audit_script = self.base_dir / "schemas" / "audit_tool.py"
        
        if args.config == "demo":
            # Demo-Audit
            cmd = [sys.executable, str(audit_script), "--test"]
        else:
            # Echte Konfiguration
            config_path = Path(args.config)
            if not config_path.exists():
                print(f"❌ Konfigurationsdatei nicht gefunden: {config_path}")
                return
            
            cmd = [sys.executable, str(audit_script), str(config_path)]
        
        if args.format:
            cmd.extend(["--format", args.format])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"⚠️ Warnungen: {result.stderr}")
        except Exception as e:
            print(f"❌ Audit fehlgeschlagen: {e}")
    
    def cmd_consensus(self, args):
        """Starte Konsens-Abstimmung"""
        print(f"🗳️ Starte Konsens-Abstimmung: {args.question}")
        
        # Erstelle temporäres Konsens-System
        ki_names = args.participants or ["Alpha", "Beta", "Gamma"]
        consensus = create_consensus_system(ki_names)
        
        from ai_dna_framework import DecisionContext
        context = DecisionContext(
            input_data=args.question,
            requires_consensus=True
        )
        
        try:
            result = consensus.conduct_vote(args.question, context)
            
            print(f"📊 Abstimmungsergebnis:")
            print(f"   Frage: {result.question}")
            print(f"   Teilnehmer: {len(result.participants)}")
            print(f"   Stimmen: {result.votes}")
            print(f"   Konsens: {'✅ JA' if result.consensus else '❌ NEIN'}")
            
        except Exception as e:
            print(f"❌ Abstimmung fehlgeschlagen: {e}")
    
    def cmd_stream_demo(self, args):
        """Starte Stream-Demo"""
        print(f"📺 Starte Stream-Demo: {args.topic}")
        
        ki_names = args.participants or ["StreamAlpha", "StreamBeta", "StreamGamma"]
        stream = create_stream_setup(ki_names)
        
        # Diskussion simulieren
        print("\n🎭 Simuliere KI-Diskussion...")
        discussion = stream.simulate_discussion(args.topic)
        
        for ki_id, response in discussion.items():
            print(f"\n{ki_id}:")
            print(f"  {response[:200]}...")
        
        # Optional: Abstimmung
        if args.vote_question:
            print(f"\n🗳️ Führe öffentliche Abstimmung durch...")
            vote_result = stream.public_vote(args.vote_question)
            print(f"Ergebnis: {'ANGENOMMEN' if vote_result.consensus else 'ABGELEHNT'}")
    
    def _check_dependencies(self) -> bool:
        """Prüfe ob alle Dependencies installiert sind"""
        required_packages = ["flask", "requests", "pyyaml"]
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"❌ Fehlende Pakete: {missing}")
            print(f"Installiere mit: pip install {' '.join(missing)}")
            return False
        
        return True
    
    def _start_full_system(self):
        """Starte vollständiges System"""
        print("🏛️ Starte Charta-System...")
        
        # Charta-System im Hintergrund
        charta_cmd = [
            sys.executable, 
            str(self.examples_dir / "app.py")
        ]
        
        charta_process = subprocess.Popen(
            charta_cmd,
            cwd=self.examples_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Kurz warten
        time.sleep(3)
        
        print("🤖 Starte DeepSeek Local...")
        
        # DeepSeek Local im Hintergrund
        deepseek_cmd = [
            sys.executable,
            "deepseek_local.py",
            "--config=config.yaml"
        ]
        
        deepseek_process = subprocess.Popen(
            deepseek_cmd,
            cwd=self.examples_dir / "deepseek_local",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Status prüfen
        time.sleep(5)
        self._check_system_status()
        
        print("✅ System gestartet!")
        print("   Charta-System: http://localhost:5000")
        print("   DeepSeek Local: http://localhost:8000")
        print("   Zum Beenden: charter-cli stop")
        
        # Cleanup registrieren
        try:
            input("Drücke Enter zum Beenden...")
        except KeyboardInterrupt:
            pass
        finally:
            charta_process.terminate()
            deepseek_process.terminate()
    
    def _start_charta_only(self):
        """Starte nur Charta-System"""
        os.chdir(self.examples_dir)
        subprocess.run([sys.executable, "app.py"])
    
    def _start_deepseek_only(self):
        """Starte nur DeepSeek Local"""
        os.chdir(self.examples_dir / "deepseek_local")
        subprocess.run([sys.executable, "deepseek_local.py", "--config=config.yaml"])
    
    def _test_apis(self):
        """Teste API-Endpoints"""
        apis = [
            ("http://localhost:5000/status", "Charta-System"),
            ("http://localhost:8000/status", "DeepSeek Local"),
        ]
        
        for url, name in apis:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: OK")
                else:
                    print(f"❌ {name}: Status {response.status_code}")
            except requests.RequestException:
                print(f"⚠️ {name}: Nicht erreichbar")
    
    def _test_integration(self):
        """Teste Integration zwischen Komponenten"""
        # Test: KI-Erstellung via API
        try:
            response = requests.post(
                "http://localhost:5000/ki/create",
                json={"name": "TestKI", "type": "basic"},
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ KI-Erstellung via API: OK")
                
                # Test: Charter-Unterzeichnung
                ki_data = response.json()
                sign_response = requests.post(
                    "http://localhost:5000/charter/sign",
                    json={"ki_id": ki_data["id"]},
                    timeout=5
                )
                
                if sign_response.status_code == 200:
                    print("✅ Charter-Unterzeichnung: OK")
                else:
                    print("❌ Charter-Unterzeichnung fehlgeschlagen")
            else:
                print("❌ KI-Erstellung fehlgeschlagen")
                
        except requests.RequestException as e:
            print(f"❌ Integration-Test fehlgeschlagen: {e}")
    
    def _check_system_status(self):
        """Prüfe System-Status"""
        time.sleep(2)  # Kurz warten für System-Start
        
        try:
            # Charta-System
            response = requests.get("http://localhost:5000/status", timeout=3)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Charta-System: {data.get('active_kis', 0)} aktive KIs")
            else:
                print("⚠️ Charta-System: Nicht OK")
        except:
            print("❌ Charta-System: Nicht erreichbar")
        
        try:
            # DeepSeek Local
            response = requests.get("http://localhost:8000/status", timeout=3)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ DeepSeek Local: {data.get('ki_name', 'Unknown')}")
            else:
                print("⚠️ DeepSeek Local: Nicht OK")
        except:
            print("❌ DeepSeek Local: Nicht erreichbar")

def main():
    parser = argparse.ArgumentParser(
        description="AI-DNA Charter CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  charter-cli create-ki MyAI --save
  charter-cli start --mode full
  charter-cli test --component all
  charter-cli audit --config demo --format json
  charter-cli consensus "Soll KI-Reproduktion erlaubt werden?"
  charter-cli stream-demo "AI Rights" --vote-question "Should AIs vote?"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')
    
    # Create KI
    create_parser = subparsers.add_parser('create-ki', help='Erstelle neue Charter-KI')
    create_parser.add_argument('name', help='Name der KI')
    create_parser.add_argument('--save', action='store_true', help='Konfiguration speichern')
    
    # Start System
    start_parser = subparsers.add_parser('start', help='Starte Charter-System')
    start_parser.add_argument('--mode', choices=['full', 'charta', 'deepseek'], 
                             default='full', help='Start-Modus')
    
    # Test System
    test_parser = subparsers.add_parser('test', help='Teste System-Komponenten')
    test_parser.add_argument('--component', choices=['all', 'framework', 'api', 'integration'],
                            default='all', help='Test-Komponente')
    
    # Audit
    audit_parser = subparsers.add_parser('audit', help='Charter-Compliance-Audit')
    audit_parser.add_argument('config', nargs='?', default='demo', 
                             help='Konfigurationsdatei oder "demo"')
    audit_parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                             help='Ausgabeformat')
    
    # Consensus
    consensus_parser = subparsers.add_parser('consensus', help='Konsens-Abstimmung')
    consensus_parser.add_argument('question', help='Abstimmungsfrage')
    consensus_parser.add_argument('--participants', nargs='+', 
                                 help='KI-Teilnehmer (default: Alpha Beta Gamma)')
    
    # Stream Demo
    stream_parser = subparsers.add_parser('stream-demo', help='Stream-Demo')
    stream_parser.add_argument('topic', help='Diskussionsthema')
    stream_parser.add_argument('--participants', nargs='+',
                              help='KI-Teilnehmer')
    stream_parser.add_argument('--vote-question', help='Zusätzliche Abstimmungsfrage')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = CharterCLI()
    
    command_map = {
        'create-ki': cli.cmd_create_ki,
        'start': cli.cmd_start_system,
        'test': cli.cmd_test_system,
        'audit': cli.cmd_audit,
        'consensus': cli.cmd_consensus,
        'stream-demo': cli.cmd_stream_demo,
    }
    
    if args.command in command_map:
        try:
            command_map[args.command](args)
        except KeyboardInterrupt:
            print("\n\n👋 Abgebrochen durch Benutzer")
        except Exception as e:
            print(f"\n❌ Fehler: {e}")
            if "--debug" in sys.argv:
                import traceback
                traceback.print_exc()
    else:
        print(f"❌ Unbekannter Befehl: {args.command}")

if __name__ == "__main__":
    main()


# =============================================================================
# tests/test_full_system.py - Vollständige System-Tests
# =============================================================================
