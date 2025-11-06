# metrics/quality_rating.py
from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    """Contenedor de métricas individuales"""
    reliability_score: float
    maintainability_score: float
    performance_score: float
    weighted_quality_score: float
    rating: str
    rating_color: str


class QualityRatingCalculator:
    """
    Calculador de Calificación General de Calidad según estándares IEEE/ISO
    
    Referencias:
    - IEEE Std 982.1-1988: Fault Density para Fiabilidad
    - IEEE Std 829-2008: Test Coverage para Mantenibilidad
    - ISO/IEC 25010:2011: Performance Efficiency
    - IEEE Std 1061-1998: Software Quality Metrics Methodology
    """
    
    # Pesos según ISO/IEC 25010 (ajustables según contexto)
    WEIGHT_RELIABILITY = 0.40      # 40%
    WEIGHT_MAINTAINABILITY = 0.40  # 40%
    WEIGHT_PERFORMANCE = 0.20      # 20%
    
    # Umbral de tiempo para eficiencia (configurable)
    PERFORMANCE_THRESHOLD = 0.5  # segundos por prueba
    
    # Rangos de calificación (similar a SonarQube/SQALE)
    RATING_RANGES = {
        'A': (90, 100),   # Excelente
        'B': (80, 89),    # Bueno
        'C': (70, 79),    # Aceptable
        'D': (60, 69),    # Pobre
        'E': (0, 59)      # Crítico
    }
    
    RATING_COLORS = {
        'A': '#28a745',  # Verde
        'B': '#5cb85c',  # Verde claro
        'C': '#ffc107',  # Amarillo
        'D': '#fd7e14',  # Naranja
        'E': '#dc3545'   # Rojo
    }
    
    def __init__(self, junit_data: Dict = None, jacoco_data: Dict = None):
        """
        Inicializar calculador de calificación
        
        Args:
            junit_data: Datos parseados de JUnit
            jacoco_data: Datos parseados de JaCoCo
        """
        self.junit_data = junit_data
        self.jacoco_data = jacoco_data
        
    def calculate_reliability_score(self) -> Tuple[float, Dict]:
        """
        Calcular puntuación de Fiabilidad según IEEE 982.1-1988
        
        Formula: RS = (1 - FD) × 100
        Donde: FD = (Failures + Errors) / Total_Tests
        
        Referencia:
        IEEE Std 982.1-1988, Section 3.5.1 - Fault Density (FD)
        "Fault Density = Number_of_Faults / Size_Metric"
        
        Aplicado a pruebas:
        Test_Failure_Density = (Failed_Tests + Error_Tests) / Total_Tests
        
        Returns:
            Tuple[float, Dict]: (score, detalles)
        """
        if not self.junit_data:
            return 0.0, {'error': 'No JUnit data available'}
        
        total_tests = self.junit_data.get('total_tests', 0)
        if total_tests == 0:
            return 0.0, {'error': 'No tests executed'}
        
        failures = self.junit_data.get('failures', 0)
        errors = self.junit_data.get('errors', 0)
        
        # Cálculo de Fault Density (IEEE 982.1)
        fault_density = (failures + errors) / total_tests
        
        # Reliability Score (inversamente proporcional a FD)
        reliability_score = (1 - fault_density) * 100
        
        details = {
            'total_tests': total_tests,
            'failures': failures,
            'errors': errors,
            'fault_density': fault_density * 100,  # Como porcentaje
            'formula': 'RS = (1 - FD) × 100',
            'standard': 'IEEE Std 982.1-1988, Section 3.5.1',
            'calculation': f'RS = (1 - {fault_density:.4f}) × 100 = {reliability_score:.2f}'
        }
        
        return reliability_score, details
    
    def calculate_maintainability_score(self) -> Tuple[float, Dict]:
        """
        Calcular puntuación de Mantenibilidad según IEEE 829 e ISO 25010
        
        Formula: MS = (w₁ × Line_Coverage) + (w₂ × Branch_Coverage)
        Donde: w₁ = 0.6, w₂ = 0.4
        
        Referencia:
        - ISO/IEC 25010:2011, Section 4.2.6 - Maintainability/Testability
        - IEEE Std 829-2008, Section 5.3 - Test Coverage
        - IEEE Std 1061-1998, Section 3.2.2 - Testability Metric
        
        "Testability_Metric = (Tested_Units / Total_Units) × 100"
        "Higher coverage indicates better testability and maintainability"
        
        Returns:
            Tuple[float, Dict]: (score, detalles)
        """
        if not self.jacoco_data:
            return 0.0, {'error': 'No JaCoCo data available'}
        
        line_coverage = self.jacoco_data.get('line_coverage', 0)
        branch_coverage = self.jacoco_data.get('branch_coverage', 0)
        
        # Pesos según IEEE 1061 (mayor peso a cobertura de líneas)
        w_line = 0.6
        w_branch = 0.4
        
        # Maintainability Score
        maintainability_score = (w_line * line_coverage) + (w_branch * branch_coverage)
        
        details = {
            'line_coverage': line_coverage,
            'branch_coverage': branch_coverage,
            'lines_covered': self.jacoco_data.get('lines_covered', 0),
            'lines_total': self.jacoco_data.get('lines_total', 0),
            'branches_covered': self.jacoco_data.get('branches_covered', 0),
            'branches_total': self.jacoco_data.get('branches_total', 0),
            'formula': f'MS = ({w_line} × LC) + ({w_branch} × BC)',
            'standards': [
                'ISO/IEC 25010:2011, Section 4.2.6',
                'IEEE Std 829-2008, Section 5.3',
                'IEEE Std 1061-1998, Section 3.2.2'
            ],
            'calculation': f'MS = ({w_line} × {line_coverage:.2f}) + ({w_branch} × {branch_coverage:.2f}) = {maintainability_score:.2f}'
        }
        
        return maintainability_score, details
    
    def calculate_performance_score(self) -> Tuple[float, Dict]:
        """
        Calcular puntuación de Eficiencia según ISO/IEC 25010
        
        Formula: PS = min(100, (Threshold_Time / Avg_Test_Time) × 100)
        
        Referencia:
        ISO/IEC 25010:2011, Section 4.2.1 - Performance Efficiency/Time Behaviour
        "Time_Behaviour_Score = (Expected_Time / Actual_Time) × 100"
        "Response times and throughput rates should meet requirements"
        
        Returns:
            Tuple[float, Dict]: (score, detalles)
        """
        if not self.junit_data:
            return 0.0, {'error': 'No JUnit data available'}
        
        total_time = self.junit_data.get('execution_time', 0)
        total_tests = self.junit_data.get('total_tests', 0)
        
        if total_tests == 0 or total_time == 0:
            return 100.0, {'note': 'No performance data, assuming optimal'}
        
        # Tiempo promedio por prueba
        avg_test_time = total_time / total_tests
        
        # Performance Score (si es más rápido que el umbral, score = 100)
        if avg_test_time <= self.PERFORMANCE_THRESHOLD:
            performance_score = 100.0
        else:
            performance_score = min(100, (self.PERFORMANCE_THRESHOLD / avg_test_time) * 100)
        
        # Throughput (pruebas por segundo)
        throughput = total_tests / total_time if total_time > 0 else 0
        
        details = {
            'total_execution_time': total_time,
            'total_tests': total_tests,
            'avg_test_time': avg_test_time,
            'threshold_time': self.PERFORMANCE_THRESHOLD,
            'throughput': throughput,
            'formula': 'PS = min(100, (Threshold / Avg_Time) × 100)',
            'standard': 'ISO/IEC 25010:2011, Section 4.2.1',
            'calculation': f'PS = min(100, ({self.PERFORMANCE_THRESHOLD} / {avg_test_time:.4f}) × 100) = {performance_score:.2f}'
        }
        
        return performance_score, details
    
    def calculate_weighted_quality_score(self) -> Tuple[float, Dict]:
        """
        Calcular Calificación General Ponderada (WQS)
        
        Formula: WQS = (w₁ × RS) + (w₂ × MS) + (w₃ × PS)
        Donde:
        - w₁ = 0.40 (Fiabilidad)
        - w₂ = 0.40 (Mantenibilidad)
        - w₃ = 0.20 (Eficiencia)
        
        Referencia:
        ISO/IEC 25010:2011, Section 4.1 - Quality Model
        "The relative importance of quality characteristics depends on 
        the intended use. For enterprise software, Reliability and 
        Maintainability are typically prioritized."
        
        Returns:
            Tuple[float, Dict]: (wqs, detalles completos)
        """
        # Calcular scores individuales
        reliability_score, rel_details = self.calculate_reliability_score()
        maintainability_score, maint_details = self.calculate_maintainability_score()
        performance_score, perf_details = self.calculate_performance_score()
        
        # Weighted Quality Score
        wqs = (
            (self.WEIGHT_RELIABILITY * reliability_score) +
            (self.WEIGHT_MAINTAINABILITY * maintainability_score) +
            (self.WEIGHT_PERFORMANCE * performance_score)
        )
        
        # Determinar rating (A, B, C, D, E)
        rating = self._get_rating(wqs)
        rating_color = self.RATING_COLORS[rating]
        
        details = {
            'weighted_quality_score': wqs,
            'rating': rating,
            'rating_color': rating_color,
            'weights': {
                'reliability': self.WEIGHT_RELIABILITY,
                'maintainability': self.WEIGHT_MAINTAINABILITY,
                'performance': self.WEIGHT_PERFORMANCE
            },
            'scores': {
                'reliability': reliability_score,
                'maintainability': maintainability_score,
                'performance': performance_score
            },
            'details': {
                'reliability': rel_details,
                'maintainability': maint_details,
                'performance': perf_details
            },
            'formula': 'WQS = (0.40 × RS) + (0.40 × MS) + (0.20 × PS)',
            'standard': 'ISO/IEC 25010:2011, Section 4.1',
            'calculation': (
                f'WQS = (0.40 × {reliability_score:.2f}) + '
                f'(0.40 × {maintainability_score:.2f}) + '
                f'(0.20 × {performance_score:.2f}) = {wqs:.2f}'
            )
        }
        
        return wqs, details
    
    def _get_rating(self, wqs: float) -> str:
        """
        Determinar rating basado en WQS
        
        Sistema de clasificación similar a SonarQube/SQALE:
        A: 90-100 (Excelente)
        B: 80-89  (Bueno)
        C: 70-79  (Aceptable)
        D: 60-69  (Pobre)
        E: 0-59   (Crítico)
        
        Args:
            wqs: Weighted Quality Score
            
        Returns:
            str: Rating (A, B, C, D, E)
        """
        for rating, (min_score, max_score) in self.RATING_RANGES.items():
            if min_score <= wqs <= max_score:
                return rating
        return 'E'  # Por defecto
    
    def get_quality_metrics(self) -> QualityMetrics:
        """
        Obtener todas las métricas de calidad calculadas
        
        Returns:
            QualityMetrics: Objeto con todas las métricas
        """
        reliability_score, _ = self.calculate_reliability_score()
        maintainability_score, _ = self.calculate_maintainability_score()
        performance_score, _ = self.calculate_performance_score()
        wqs, details = self.calculate_weighted_quality_score()
        
        return QualityMetrics(
            reliability_score=reliability_score,
            maintainability_score=maintainability_score,
            performance_score=performance_score,
            weighted_quality_score=wqs,
            rating=details['rating'],
            rating_color=details['rating_color']
        )
    
    def get_rating_description(self, rating: str) -> Dict:
        """
        Obtener descripción detallada de un rating
        
        Args:
            rating: Rating (A, B, C, D, E)
            
        Returns:
            Dict con descripción y recomendaciones
        """
        descriptions = {
            'A': {
                'title': 'Excelente',
                'description': 'Calidad Superior - El código cumple con los más altos estándares de calidad',
                'recommendation': 'Mantener las buenas prácticas actuales',
                'icon': '🏆'
            },
            'B': {
                'title': 'Bueno',
                'description': 'Calidad Alta - El código está bien estructurado con mejoras menores posibles',
                'recommendation': 'Enfocarse en alcanzar cobertura completa y reducir fallos ocasionales',
                'icon': '✅'
            },
            'C': {
                'title': 'Aceptable',
                'description': 'Calidad Media - El código es funcional pero requiere mejoras',
                'recommendation': 'Aumentar cobertura de pruebas y reducir la densidad de fallos',
                'icon': '⚠️'
            },
            'D': {
                'title': 'Pobre',
                'description': 'Necesita Mejora - El código presenta deficiencias significativas',
                'recommendation': 'Priorizar refactorización y aumento de pruebas unitarias',
                'icon': '❌'
            },
            'E': {
                'title': 'Crítico',
                'description': 'Requiere Atención Inmediata - La calidad es inaceptable',
                'recommendation': 'Revisión completa del código y estrategia de testing urgente',
                'icon': '🚨'
            }
        }
        return descriptions.get(rating, descriptions['E'])


class QualityReportGenerator:
    """Generador de reportes detallados de calidad"""
    
    def __init__(self, calculator: QualityRatingCalculator):
        self.calculator = calculator
        
    def generate_text_report(self) -> str:
        """
        Generar reporte de calidad en formato texto
        
        Returns:
            str: Reporte formateado
        """
        wqs, details = self.calculator.calculate_weighted_quality_score()
        rating = details['rating']
        rating_info = self.calculator.get_rating_description(rating)
        
        report = []
        report.append("=" * 70)
        report.append("REPORTE DE CALIDAD DE SOFTWARE")
        report.append("Basado en Estándares IEEE/ISO")
        report.append("=" * 70)
        report.append("")
        
        # Calificación General
        report.append(f"CALIFICACIÓN GENERAL: {rating_info['icon']} {rating} - {rating_info['title']}")
        report.append(f"Puntuación WQS: {wqs:.2f}/100")
        report.append("")
        report.append(f"Descripción: {rating_info['description']}")
        report.append(f"Recomendación: {rating_info['recommendation']}")
        report.append("")
        report.append("-" * 70)
        
        # Fiabilidad
        report.append("1. FIABILIDAD (Reliability) - 40% del score total")
        report.append(f"   Estándar: {details['details']['reliability']['standard']}")
        report.append(f"   Puntuación: {details['scores']['reliability']:.2f}/100")
        report.append(f"   Fórmula: {details['details']['reliability']['formula']}")
        report.append(f"   Cálculo: {details['details']['reliability']['calculation']}")
        if 'fault_density' in details['details']['reliability']:
            fd = details['details']['reliability']['fault_density']
            report.append(f"   Densidad de Fallos: {fd:.2f}%")
        report.append("")
        
        # Mantenibilidad
        report.append("2. MANTENIBILIDAD (Maintainability) - 40% del score total")
        maint_standards = details['details']['maintainability'].get('standards', [])
        report.append(f"   Estándares: {', '.join(maint_standards)}")
        report.append(f"   Puntuación: {details['scores']['maintainability']:.2f}/100")
        report.append(f"   Fórmula: {details['details']['maintainability']['formula']}")
        report.append(f"   Cálculo: {details['details']['maintainability']['calculation']}")
        report.append("")
        
        # Eficiencia
        report.append("3. EFICIENCIA DEL DESEMPEÑO (Performance) - 20% del score total")
        report.append(f"   Estándar: {details['details']['performance']['standard']}")
        report.append(f"   Puntuación: {details['scores']['performance']:.2f}/100")
        report.append(f"   Fórmula: {details['details']['performance']['formula']}")
        report.append(f"   Cálculo: {details['details']['performance']['calculation']}")
        report.append("")
        
        report.append("-" * 70)
        report.append("CÁLCULO FINAL")
        report.append(f"Fórmula: {details['formula']}")
        report.append(f"Cálculo: {details['calculation']}")
        report.append("")
        report.append("PONDERACIÓN (según ISO/IEC 25010:2011)")
        report.append(f"  • Fiabilidad: {details['weights']['reliability']*100}%")
        report.append(f"  • Mantenibilidad: {details['weights']['maintainability']*100}%")
        report.append(f"  • Eficiencia: {details['weights']['performance']*100}%")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def generate_html_report(self) -> str:
        """Generar reporte HTML (para exportar)"""
        wqs, details = self.calculator.calculate_weighted_quality_score()
        rating = details['rating']
        rating_info = self.calculator.get_rating_description(rating)
        color = details['rating_color']
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Calidad de Software</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; background: #0d6efd; color: white; padding: 20px; }}
                .rating {{ text-align: center; margin: 30px 0; }}
                .rating-badge {{ 
                    display: inline-block;
                    font-size: 72px;
                    font-weight: bold;
                    color: {color};
                    border: 5px solid {color};
                    border-radius: 50%;
                    width: 150px;
                    height: 150px;
                    line-height: 150px;
                }}
                .score {{ font-size: 24px; color: #666; margin: 10px 0; }}
                .section {{ margin: 30px 0; padding: 20px; background: #f8f9fa; border-left: 4px solid #0d6efd; }}
                .metric {{ margin: 15px 0; }}
                .formula {{ background: #e9ecef; padding: 10px; font-family: monospace; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #0d6efd; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>REPORTE DE CALIDAD DE SOFTWARE</h1>
                <p>Basado en Estándares IEEE/ISO</p>
            </div>
            
            <div class="rating">
                <div class="rating-badge">{rating}</div>
                <h2>{rating_info['title']}</h2>
                <div class="score">Puntuación WQS: {wqs:.2f}/100</div>
                <p><strong>{rating_info['description']}</strong></p>
                <p>Recomendación: {rating_info['recommendation']}</p>
            </div>
            
            <div class="section">
                <h3>🛡️ 1. FIABILIDAD (Reliability) - 40%</h3>
                <div class="metric">
                    <strong>Estándar:</strong> {details['details']['reliability']['standard']}<br>
                    <strong>Puntuación:</strong> {details['scores']['reliability']:.2f}/100
                </div>
                <div class="formula">
                    <strong>Fórmula:</strong> {details['details']['reliability']['formula']}<br>
                    <strong>Cálculo:</strong> {details['details']['reliability']['calculation']}
                </div>
            </div>
            
            <div class="section">
                <h3>⚙️ 2. MANTENIBILIDAD (Maintainability) - 40%</h3>
                <div class="metric">
                    <strong>Estándares:</strong> {', '.join(details['details']['maintainability'].get('standards', []))}<br>
                    <strong>Puntuación:</strong> {details['scores']['maintainability']:.2f}/100
                </div>
                <div class="formula">
                    <strong>Fórmula:</strong> {details['details']['maintainability']['formula']}<br>
                    <strong>Cálculo:</strong> {details['details']['maintainability']['calculation']}
                </div>
            </div>
            
            <div class="section">
                <h3>⏱️ 3. EFICIENCIA DEL DESEMPEÑO (Performance) - 20%</h3>
                <div class="metric">
                    <strong>Estándar:</strong> {details['details']['performance']['standard']}<br>
                    <strong>Puntuación:</strong> {details['scores']['performance']:.2f}/100
                </div>
                <div class="formula">
                    <strong>Fórmula:</strong> {details['details']['performance']['formula']}<br>
                    <strong>Cálculo:</strong> {details['details']['performance']['calculation']}
                </div>
            </div>
            
            <div class="section">
                <h3>📊 CÁLCULO FINAL</h3>
                <div class="formula">
                    <strong>Fórmula:</strong> {details['formula']}<br>
                    <strong>Cálculo:</strong> {details['calculation']}
                </div>
                
                <h4>Ponderación (según ISO/IEC 25010:2011)</h4>
                <table>
                    <tr>
                        <th>Característica</th>
                        <th>Peso</th>
                        <th>Puntuación</th>
                        <th>Contribución</th>
                    </tr>
                    <tr>
                        <td>Fiabilidad</td>
                        <td>{details['weights']['reliability']*100:.0f}%</td>
                        <td>{details['scores']['reliability']:.2f}</td>
                        <td>{details['weights']['reliability']*details['scores']['reliability']:.2f}</td>
                    </tr>
                    <tr>
                        <td>Mantenibilidad</td>
                        <td>{details['weights']['maintainability']*100:.0f}%</td>
                        <td>{details['scores']['maintainability']:.2f}</td>
                        <td>{details['weights']['maintainability']*details['scores']['maintainability']:.2f}</td>
                    </tr>
                    <tr>
                        <td>Eficiencia</td>
                        <td>{details['weights']['performance']*100:.0f}%</td>
                        <td>{details['scores']['performance']:.2f}</td>
                        <td>{details['weights']['performance']*details['scores']['performance']:.2f}</td>
                    </tr>
                    <tr style="background: #e9ecef; font-weight: bold;">
                        <td>TOTAL</td>
                        <td>100%</td>
                        <td>-</td>
                        <td>{wqs:.2f}</td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
        """
        return html