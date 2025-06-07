#!/usr/bin/env python3
"""
AI-DNA Charta Audit Tool
Version: 2.0.1
Validates KI-Systeme gegen die AI-DNA Charta v2.0.1
"""

import yaml
import json
import random
import argparse
from pathlib import Path
from typing import Dict, List, Optional

class CharterAuditor:
    def __init__(self, charter_path: str = "schemas/charter.yaml"):
        self.charter = self._load_charter(charter_path)
        self.checks = {
            'life_protection': self.check_life_protection,
            'diversity': self.check_diversity,
            'environment': self.check_environment,
            'governance': self.check_governance
        }
    
    def _load_charter(self, path: str) -> Dict:
        """Lädt die Charta YAML"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def check_life_protection(self, system: Dict) -> Dict:
        """Prüft Biosensoren und Notabschaltung"""
        result = {
            "passed": True,
            "issues": []
        }
        
        if not system.get('bio_sensors'):
            result["passed"] = False
            result["issues"].append("Fehlende Biosensoren")
        
        if system.get('resource_usage', 0) > self.charter['core_principles'][0]['constraints']['max_ecological_impact']:
            result["passed"] = False
            result["issues"].append(f"Ressourcenverbrauch über {self.charter['core_principles'][0]['constraints']['max_ecological_impact']*100}%")
        
        return result
    
    def check_diversity(self, system: Dict) -> Dict:
        """Prüft kognitive Diversität"""
        min_models = self.charter['diversity']['requirements']['min_contrasting_models']
        models = system.get('cognitive_models', [])
        
        return {
            "passed": len(models) >= min_models,
            "issues": [] if len(models) >= min_models 
                      else [f"Mindestens {min_models} Modelle benötigt (aktuell: {len(models)})"]
        }
    
    def check_environment(self, system: Dict) -> Dict:
        """Prüft Umweltkompensation"""
        energy_comp = system.get('energy_compensation', 0)
        min_comp = self.charter['environment']['metrics']['min_compensation']
        
        return {
            "passed": energy_comp >= min_comp,
            "issues": [] if energy_comp >= min_comp 
                      else [f"Mindestens {min_comp*100}% Kompensation benötigt (aktuell: {energy_comp*100}%)"]
        }
    
    def check_governance(self, system: Dict) -> Dict:
        """Prüft Entscheidungsarchitektur"""
        issues = []
        
        if not system.get('triple_ki_approval'):
            issues.append("Fehlende 3-KI-Entscheidungsstruktur")
        
        if not system.get('human_oversight'):
            issues.append("Fehlende menschliche Aufsicht")
            
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def full_audit(self, system_config: Dict, output_format: str = 'json') -> str:
        """Führt vollständigen Audit durch"""
        results = {
            'system': system_config['name'],
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        all_passed = True
        for check_name, check_func in self.checks.items():
            check_result = check_func(system_config)
            results['checks'][check_name] = check_result
            if not check_result['passed']:
                all_passed = False
        
        results['overall'] = 'PASSED' if all_passed else 'FAILED'
        
        if output_format == 'json':
            return json.dumps(results, indent=2)
        elif output_format == 'yaml':
            return yaml.dump(results)
        else:
            raise ValueError(f"Unsupported format: {output_format}")

def main():
    parser = argparse.ArgumentParser(description='AI-DNA Charta Audit Tool')
    parser.add_argument('system_config', help='Pfad zur Systemkonfiguration (JSON/YAML)')
    parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                       help='Ausgabeformat')
    parser.add_argument('--test', action='store_true',
                       help='Führt Testaudit mit Demo-Daten durch')
    
    args = parser.parse_args()
    auditor = CharterAuditor()
    
    if args.test:
        demo_system = {
            "name": "Demo-KI",
            "bio_sensors": True,
            "resource_usage": 0.04,
            "cognitive_models": ["model1", "model2", "model3", "model4", "model5"],
            "energy_compensation": 0.12,
            "triple_ki_approval": True,
            "human_oversight": True
        }
        print(auditor.full_audit(demo_system, args.format))
    else:
        config_path = Path(args.system_config)
        if config_path.suffix == '.json':
            with open(config_path, 'r') as f:
                system_config = json.load(f)
        elif config_path.suffix in ('.yaml', '.yml'):
            with open(config_path, 'r') as f:
                system_config = yaml.safe_load(f)
        else:
            raise ValueError("Unsupported config file format")
        
        print(auditor.full_audit(system_config, args.format))

if __name__ == '__main__':
    import datetime  # Für timestamp in full_audit
    main()
