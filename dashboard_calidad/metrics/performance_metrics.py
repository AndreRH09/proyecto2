# metrics/performance_metrics.py
from typing import Dict

class PerformanceMetrics:
    """
    Cálculo de métricas de Eficiencia del Desempeño según ISO/IEC 25010
    """
    
    @staticmethod
    def calculate_avg_test_time(junit_data: Dict) -> float:
        """
        Tiempo Promedio de Ejecución por Prueba
        """
        total_time = junit_data['execution_time']
        total_tests = junit_data['total_tests']
        
        if total_tests == 0:
            return 0.0
        
        return total_time / total_tests
    
    @staticmethod
    def get_performance_status(total_time: float, total_tests: int) -> Dict:
        """
        Determina el estado de eficiencia basado en tiempo de ejecución
        
        Umbrales sugeridos (tiempo promedio por test):
        - Excelente: < 0.1s
        - Bueno: 0.1-0.5s
        - Aceptable: 0.5-1s
        - Pobre: > 1s
        """
        avg_time = total_time / total_tests if total_tests > 0 else 0
        
        if avg_time < 0.1:
            return {'status': 'Excelente', 'color': 'success'}
        elif avg_time < 0.5:
            return {'status': 'Bueno', 'color': 'info'}
        elif avg_time < 1.0:
            return {'status': 'Aceptable', 'color': 'warning'}
        else:
            return {'status': 'Pobre', 'color': 'danger'}