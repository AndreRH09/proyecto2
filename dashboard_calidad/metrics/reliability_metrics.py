# metrics/reliability_metrics.py
from typing import Dict

class ReliabilityMetrics:
    """
    Cálculo de métricas de Fiabilidad según IEEE 982.1
    """
    
    @staticmethod
    def calculate_failure_density(junit_data: Dict) -> float:
        """
        Densidad de Fallos de Prueba
        Formula: (Failures + Errors) / Total Tests * 100
        """
        total = junit_data['total_tests']
        if total == 0:
            return 0.0
        
        failures = junit_data['failures'] + junit_data['errors']
        return (failures / total) * 100
    
    @staticmethod
    def calculate_success_rate(junit_data: Dict) -> float:
        """
        Tasa de Éxito de Pruebas
        Formula: Passed Tests / Total Tests * 100
        """
        total = junit_data['total_tests']
        if total == 0:
            return 0.0
        
        return (junit_data['passed'] / total) * 100
    
    @staticmethod
    def get_reliability_status(failure_density: float) -> Dict:
        """
        Determina el estado de fiabilidad basado en umbrales
        
        Umbrales recomendados:
        - Excelente: < 5%
        - Bueno: 5-10%
        - Aceptable: 10-20%
        - Pobre: > 20%
        """
        if failure_density < 5:
            return {'status': 'Excelente', 'color': 'success'}
        elif failure_density < 10:
            return {'status': 'Bueno', 'color': 'info'}
        elif failure_density < 20:
            return {'status': 'Aceptable', 'color': 'warning'}
        else:
            return {'status': 'Pobre', 'color': 'danger'}