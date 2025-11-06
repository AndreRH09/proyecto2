# parsers/junit_parser.py
from lxml import etree
import pandas as pd
from pathlib import Path
from typing import Dict, List

class JUnitParser:
    """Parser para reportes XML de JUnit/Surefire"""
    
    def __init__(self, report_path: str):
        self.report_path = Path(report_path)
        self.data = None
    
    def parse(self) -> Dict:
        """
        Extrae métricas de los reportes JUnit XML
        
        Returns:
            Dict con métricas agregadas:
            {
                'total_tests': int,
                'passed': int,
                'failures': int,
                'errors': int,
                'skipped': int,
                'execution_time': float,
                'failure_density': float,
                'test_details': List[Dict]
            }
        """
        try:
            tree = etree.parse(str(self.report_path))
            root = tree.getroot()
            
            # Extracción de atributos del testsuite
            testsuite = root if root.tag == 'testsuite' else root.find('testsuite')
            
            metrics = {
                'total_tests': int(testsuite.get('tests', 0)),
                'failures': int(testsuite.get('failures', 0)),
                'errors': int(testsuite.get('errors', 0)),
                'skipped': int(testsuite.get('skipped', 0)),
                'execution_time': float(testsuite.get('time', 0))
            }
            
            # Calcular pruebas pasadas
            metrics['passed'] = (metrics['total_tests'] - 
                               metrics['failures'] - 
                               metrics['errors'] - 
                               metrics['skipped'])
            
            # Calcular Densidad de Fallos (Métrica IEEE 982.1)
            if metrics['total_tests'] > 0:
                metrics['failure_density'] = (
                    (metrics['failures'] + metrics['errors']) / 
                    metrics['total_tests']
                ) * 100
            else:
                metrics['failure_density'] = 0.0
            
            # Extraer detalles de cada test case
            test_details = []
            for testcase in testsuite.findall('.//testcase'):
                detail = {
                    'name': testcase.get('name'),
                    'classname': testcase.get('classname'),
                    'time': float(testcase.get('time', 0)),
                    'status': self._get_test_status(testcase)
                }
                test_details.append(detail)
            
            metrics['test_details'] = test_details
            self.data = metrics
            return metrics
            
        except Exception as e:
            raise Exception(f"Error parsing JUnit report: {str(e)}")
    
    def _get_test_status(self, testcase) -> str:
        """Determina el estado de un test case"""
        if testcase.find('failure') is not None:
            return 'FAILED'
        elif testcase.find('error') is not None:
            return 'ERROR'
        elif testcase.find('skipped') is not None:
            return 'SKIPPED'
        else:
            return 'PASSED'
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convierte test_details a DataFrame para análisis"""
        if self.data is None:
            raise ValueError("No data parsed yet. Call parse() first.")
        return pd.DataFrame(self.data['test_details'])