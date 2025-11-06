# parsers/jacoco_parser.py
from lxml import etree
import pandas as pd
from pathlib import Path
from typing import Dict, List

class JaCoCoParser:
    """Parser para reportes XML de JaCoCo"""
    
    def __init__(self, report_path: str):
        self.report_path = Path(report_path)
        self.data = None
    
    def parse(self) -> Dict:
        """
        Extrae métricas de cobertura del reporte JaCoCo XML
        
        Returns:
            Dict con métricas de cobertura:
            {
                'line_coverage': float,
                'branch_coverage': float,
                'instruction_coverage': float,
                'complexity_coverage': float,
                'package_details': List[Dict]
            }
        """
        try:
            tree = etree.parse(str(self.report_path))
            root = tree.getroot()
            
            # Extraer contadores globales
            metrics = self._extract_counters(root)
            
            # Extraer detalles por paquete
            package_details = []
            for package in root.findall('.//package'):
                pkg_data = {
                    'name': package.get('name', 'default'),
                    **self._extract_counters(package)
                }
                package_details.append(pkg_data)
            
            metrics['package_details'] = package_details
            self.data = metrics
            return metrics
            
        except Exception as e:
            raise Exception(f"Error parsing JaCoCo report: {str(e)}")
    
    def _extract_counters(self, element) -> Dict:
        """
        Extrae contadores de cobertura de un elemento XML
        
        Tipos de contadores JaCoCo:
        - INSTRUCTION: Instrucciones de bytecode
        - BRANCH: Bifurcaciones de flujo de control
        - LINE: Líneas de código fuente
        - COMPLEXITY: Complejidad ciclomática
        - METHOD: Métodos
        - CLASS: Clases
        """
        counters = {}
        
        for counter in element.findall('.//counter'):
            counter_type = counter.get('type')
            missed = int(counter.get('missed', 0))
            covered = int(counter.get('covered', 0))
            total = missed + covered
            
            coverage = (covered / total * 100) if total > 0 else 0.0
            
            if counter_type == 'LINE':
                counters['line_coverage'] = coverage
                counters['lines_covered'] = covered
                counters['lines_total'] = total
            elif counter_type == 'BRANCH':
                counters['branch_coverage'] = coverage
                counters['branches_covered'] = covered
                counters['branches_total'] = total
            elif counter_type == 'INSTRUCTION':
                counters['instruction_coverage'] = coverage
            elif counter_type == 'COMPLEXITY':
                counters['complexity_coverage'] = coverage
        
        return counters
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convierte package_details a DataFrame"""
        if self.data is None:
            raise ValueError("No data parsed yet. Call parse() first.")
        return pd.DataFrame(self.data['package_details'])