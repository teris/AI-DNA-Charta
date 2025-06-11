
#!/usr/bin/env python3
"""
tools/system_manager.py - Zentraler Manager für das AI-DNA Charter System
Vereint alle Komponenten und ermöglicht einfache Verwaltung
"""

import os
import sys
import json
import subprocess
import time
import signal
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class SystemManager:
    """Zentraler Manager für das AI-DNA Charter System"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.processes: Dict[str, subprocess.Popen] = {}
        self.pid_file = self.base_dir / ".ai_dna_pids.json"
        
    def start_full_system(self, detached: bool = False) -> bool:
        """Starte das vollständige System"""
        print("🚀 Starte AI-DNA Charter System...")
        
        # Prüfe Dependencies
        if not self._check_dependencies():
            return False
        
        success = True
        
        # Starte Charta-System
        success &= self._start_charta_system(detached)
        
        if success:
            # Warte kurz
            time.sleep(3)
            
            # Starte DeepSeek Local
            success &= self._start_deepseek_system(detached)
        
        if success:
            # Speichere PIDs
            self._save_pids()
            
            # Status prüfen
            time.sleep(5)
            self._print_system_status()
            
            print("✅ System erfolgreich gestartet!")
            
            if not detached:
                self._wait_for_shutdown()
        else:
            print("❌ System-Start fehlgeschlagen!")
            self.stop_all()
        
        return success
    
    def stop_all(self) -> None:
        """Stoppe alle System-Komponenten"""
        print("🛑 Stoppe AI-DNA Charter System...")
        
        # Lade gespeicherte PIDs
        self._load_pids()
        
        # Stoppe alle Prozesse
        for name, process in self.processes.items():
            if process and process.poll() is None:
                print(f"   Stoppe {name}...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception as e:
                    print(f"   ⚠️ Fehler beim Stoppen von {name}: {e}")
        
        # Cleanup
        self.processes.clear()
        
        if self.pid_file.exists():
            self.pid_file.unlink()
        
        print("✅ System gestoppt")
    
    def get_system_status(self) -> Dict:
        """Hole System-Status"""
        status = {
            "charta_system": self._check_service("http://localhost:5000/status"),
            "deepseek_local": self._check_service("http://localhost:8000/status"),
            "processes": {},
            "resource_usage": self._get_resource_usage()
        }
        
        # Prüfe Prozesse
        self._load_pids()
        for name, process in self.processes.items():
            if process:
                status["processes"][name] = {
                    "running": process.poll() is None,
                    "pid": process.pid if process.poll() is None else None
                }
        
        return status
    
    def restart_component(self, component: str) -> bool:
        """Starte einzelne Komponente neu"""
        print(f"🔄 Starte {component} neu...")
        
        # Stoppe Komponente
        if component in self.processes:
            process = self.processes[component]
            if process and process.poll() is None:
                process.terminate()
                process.wait(timeout=5)
        
        # Starte neu
        if component == "charta":
            return self._start_charta_system(detached=True)
        elif component == "deepseek":
            return self._start_deepseek_system(detached=True)
        else:
            print(f"❌ Unbekannte Komponente: {component}")
            return False
    
    def run_tests(self) -> bool:
        """Führe System-Tests aus"""
        test_script = self.base_dir / "tests" / "test_full_system.py"
        
        if not test_script.exists():
            print("❌ Test-Script nicht gefunden")
            return False
        
        print("🧪 Führe System-Tests aus...")
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_script)],
                cwd=self.base_dir,
                timeout=300  # 5 Minuten Timeout
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("❌ Tests Timeout nach 5 Minuten")
            return False
        except Exception as e:
            print(f"❌ Test-Fehler: {e}")
            return False
    
    def _start_charta_system(self, detached: bool) -> bool:
        """Starte Charta-System"""
        print("🏛️ Starte Charta-System...")
        
        cmd = [sys.executable, "app.py"]
        cwd = self.base_dir / "examples"
        
        try:
            if detached:
                process = subprocess.Popen(
                    cmd,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True
                )
            else:
                process = subprocess.Popen(cmd, cwd=cwd)
            
            self.processes["charta"] = process
            
            # Kurz warten und prüfen
            time.sleep(2)
            if process.poll() is None:
                print("   ✅ Charta-System gestartet")
                return True
            else:
                print("   ❌ Charta-System Start fehlgeschlagen")
                return False
                
        except Exception as e:
            print(f"   ❌ Fehler beim Starten: {e}")
            return False
    
    def _start_deepseek_system(self, detached: bool) -> bool:
        """Starte DeepSeek Local System"""
        print("🤖 Starte DeepSeek Local...")
        
        cmd = [sys.executable, "deepseek_local.py", "--config=config.yaml"]
        cwd = self.base_dir / "examples" / "deepseek_local"
        
        try:
            if detached:
                process = subprocess.Popen(
                    cmd,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True
                )
            else:
                process = subprocess.Popen(cmd, cwd=cwd)
            
            self.processes["deepseek"] = process
            
            # Kurz warten und prüfen
            time.sleep(2)
            if process.poll() is None:
                print("   ✅ DeepSeek Local gestartet")
                return True
            else:
                print("   ❌ DeepSeek Local Start fehlgeschlagen")
                return False
                
        except Exception as e:
            print(f"   ❌ Fehler beim Starten: {e}")
            return False
    
    def _check_dependencies(self) -> bool:
        """Prüfe System-Dependencies"""
        required_files = [
            self.base_dir / "examples" / "app.py",
            self.base_dir / "examples" / "deepseek_local" / "deepseek_local.py",
            self.base_dir / "framework" / "ai_dna_framework.py"
        ]
        
        missing = [f for f in required_files if not f.exists()]
        
        if missing:
            print("❌ Fehlende Dateien:")
            for f in missing:
                print(f"   - {f}")
            return False
        
        # Prüfe Python-Pakete
        required_packages = ["flask", "requests", "pyyaml"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Fehlende Python-Pakete: {missing_packages}")
            print(f"   Installiere mit: pip install {' '.join(missing_packages)}")
            return False
        
        return True
    
    def _check_service(self, url: str) -> Dict:
        """Prüfe Service-Status"""
        try:
            import requests
            response = requests.get(url, timeout=3)
            
            return {
                "running": True,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {
                "running": False,
                "error": str(e)
            }
    
    def _get_resource_usage(self) -> Dict:
        """Hole Resource-Usage"""
        try:
            # System-weite Statistiken
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Prozess-spezifische Statistiken
            process_stats = {}
            
            for name, process in self.processes.items():
                if process and process.poll() is None:
                    try:
                        p = psutil.Process(process.pid)
                        process_stats[name] = {
                            "cpu_percent": p.cpu_percent(),
                            "memory_mb": p.memory_info().rss / 1024 / 1024,
                            "pid": process.pid
                        }
                    except psutil.NoSuchProcess:
                        pass
            
            return {
                "system_cpu_percent": cpu_percent,
                "system_memory_percent": memory.percent,
                "system_memory_available_gb": memory.available / 1024 / 1024 / 1024,
                "processes": process_stats
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _save_pids(self) -> None:
        """Speichere Process-PIDs"""
        pids = {}
        
        for name, process in self.processes.items():
            if process and process.poll() is None:
                pids[name] = process.pid
        
        with open(self.pid_file, 'w') as f:
            json.dump(pids, f)
    
    def _load_pids(self) -> None:
        """Lade gespeicherte PIDs"""
        if not self.pid_file.exists():
            return
        
        try:
            with open(self.pid_file, 'r') as f:
                pids = json.load(f)
            
            for name, pid in pids.items():
                try:
                    # Prüfe ob Prozess noch läuft
                    os.kill(pid, 0)
                    
                    # Erstelle Pseudo-Process-Objekt
                    class PseudoProcess:
                        def __init__(self, pid):
                            self.pid = pid
                        
                        def poll(self):
                            try:
                                os.kill(self.pid, 0)
                                return None  # Läuft noch
                            except OSError:
                                return 1  # Beendet
                        
                        def terminate(self):
                            os.kill(self.pid, signal.SIGTERM)
                        
                        def kill(self):
                            os.kill(self.pid, signal.SIGKILL)
                        
                        def wait(self, timeout=None):
                            pass
                    
                    self.processes[name] = PseudoProcess(pid)
                    
                except OSError:
                    # Prozess läuft nicht mehr
                    pass
                    
        except Exception as e:
            print(f"⚠️ Fehler beim Laden der PIDs: {e}")
    
    def _print_system_status(self) -> None:
        """Zeige System-Status"""
        print("\n📊 System-Status:")
        status = self.get_system_status()
        
        # Services
        charta_status = "✅ OK" if status["charta_system"]["running"] else "❌ Nicht erreichbar"
        deepseek_status = "✅ OK" if status["deepseek_local"]["running"] else "❌ Nicht erreichbar"
        
        print(f"   Charta-System (Port 5000): {charta_status}")
        print(f"   DeepSeek Local (Port 8000): {deepseek_status}")
        
        # Resource Usage
        if "error" not in status["resource_usage"]:
            ru = status["resource_usage"]
            print(f"   System CPU: {ru['system_cpu_percent']:.1f}%")
            print(f"   System Memory: {ru['system_memory_percent']:.1f}%")
            
            if ru["processes"]:
                print("   Prozess-Details:")
                for name, stats in ru["processes"].items():
                    print(f"     {name}: CPU {stats['cpu_percent']:.1f}%, RAM {stats['memory_mb']:.1f}MB")
    
    def _wait_for_shutdown(self) -> None:
        """Warte auf Shutdown-Signal"""
        print("\n🔄 System läuft. Zum Beenden: Ctrl+C")
        
        def signal_handler(sig, frame):
            print("\n\n🛑 Shutdown-Signal empfangen...")
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Warte unendlich
            while True:
                time.sleep(1)
                
                # Prüfe ob Prozesse noch laufen
                running_processes = [
                    name for name, process in self.processes.items()
                    if process and process.poll() is None
                ]
                
                if not running_processes:
                    print("⚠️ Alle Prozesse beendet - stoppe System")
                    break
                    
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)


# =============================================================================
# Haupt-CLI-Interface
# =============================================================================

def main():
    """Haupt-CLI für System-Manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-DNA Charter System Manager")
    subparsers = parser.add_subparsers(dest='action', help='Verfügbare Aktionen')
    
    # Start
    start_parser = subparsers.add_parser('start', help='Starte System')
    start_parser.add_argument('--detached', action='store_true', help='Im Hintergrund starten')
    
    # Stop
    subparsers.add_parser('stop', help='Stoppe System')
    
    # Status
    subparsers.add_parser('status', help='Zeige System-Status')
    
    # Restart
    restart_parser = subparsers.add_parser('restart', help='Starte Komponente neu')
    restart_parser.add_argument('component', choices=['charta', 'deepseek'], help='Komponente')
    
    # Test
    subparsers.add_parser('test', help='Führe Tests aus')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    manager = SystemManager()
    
    try:
        if args.action == 'start':
            success = manager.start_full_system(detached=args.detached)
            sys.exit(0 if success else 1)
            
        elif args.action == 'stop':
            manager.stop_all()
            
        elif args.action == 'status':
            status = manager.get_system_status()
            print(json.dumps(status, indent=2))
            
        elif args.action == 'restart':
            success = manager.restart_component(args.component)
            sys.exit(0 if success else 1)
            
        elif args.action == 'test':
            success = manager.run_tests()
            sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
