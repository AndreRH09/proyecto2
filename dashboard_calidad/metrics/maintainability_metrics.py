# metrics/maintainability_metrics.py
from typing import Dict

class MaintainabilityMetrics:
    """
    Cálculo de métricas de Mantenibilidad según ISO/IEC 25010
    """
    
    @staticmethod
    def get_testability_score(jacoco_data: Dict) -> float:
        """
        Puntuación de Capacidad de Prueba (Testability)
        Promedio ponderado de coberturas
        """
        line_cov = jacoco_data.get('line_coverage', 0)
        branch_cov = jacoco_data.get('branch_coverage', 0)
        
        # Ponderación: 60% líneas, 40% ramas
        return (line_cov * 0.6) + (branch_cov * 0.4)
    
    @staticmethod
    def get_maintainability_status(testability_score: float) -> Dict:
        """
        Determina el estado de mantenibilidad basado en umbrales
        
        Umbrales recomendados (Cobertura):
        - Excelente: ≥ 80%
        - Bueno: 70-80%
        - Aceptable: 60-70%
        - Pobre: < 60%
        """
        if testability_score >= 80:
            return {'status': 'Excelente', 'color': 'success'}
        elif testability_score >= 70:
            return {'status': 'Bueno', 'color': 'info'}
        elif testability_score >= 60:
            return {'status': 'Aceptable', 'color': 'warning'}
        else:
            return {'status': 'Pobre', 'color': 'danger'}