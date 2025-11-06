# ui/charts.py
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge
import seaborn as sns

class ChartGenerator:
    """Generador de gráficos personalizados"""
    
    def __init__(self):
        # Configurar estilo de seaborn
        sns.set_style("whitegrid")
        plt.rcParams['font.family'] = 'Arial'
        
    def create_gauge_chart(self, ax, value, title):
        """
        Crear gráfico tipo velocímetro/gauge
        
        Args:
            ax: Axes de matplotlib
            value: Valor a mostrar (0-100)
            title: Título del gráfico
        """
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Dibujar arco de fondo
        theta = np.linspace(0, np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        
        # Colores de fondo (zonas)
        colors = ['#dc3545', '#ffc107', '#28a745']
        boundaries = [0, 70, 90, 100]
        
        for i in range(len(colors)):
            start_angle = (boundaries[i] / 100) * 180
            end_angle = (boundaries[i+1] / 100) * 180
            wedge = Wedge((0, 0), 0.9, start_angle, end_angle, 
                         width=0.3, facecolor=colors[i], alpha=0.3)
            ax.add_patch(wedge)
        
        # Dibujar aguja
        angle = np.radians(180 - (value / 100 * 180))
        ax.arrow(0, 0, 0.7*np.cos(angle), 0.7*np.sin(angle),
                head_width=0.1, head_length=0.1, fc='#212529', ec='#212529', 
                linewidth=3)
        
        # Valor central
        ax.text(0, -0.3, f"{value:.1f}%", 
               ha='center', va='center', fontsize=24, fontweight='bold')
        
        # Título
        ax.text(0, -0.6, title, 
               ha='center', va='center', fontsize=12, color='#6c757d')
        
    def create_pie_chart(self, ax, sizes, labels, colors, title):
        """Crear gráfico de pastel"""
        # Filtrar valores cero
        non_zero = [(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0]
        if not non_zero:
            ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center')
            return
            
        sizes, labels, colors = zip(*non_zero)
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10}
        )
        
        # Hacer el texto de porcentaje más legible
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        
    def create_bar_chart(self, ax, categories, values, colors, title):
        """Crear gráfico de barras vertical"""
        bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
        
        # Agregar valores sobre las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Porcentaje (%)', fontsize=10)
        ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
    def create_horizontal_bar_chart(self, ax, categories, values, title):
        """Crear gráfico de barras horizontal"""
        # Crear gradiente de color
        colors = plt.cm.RdYlGn(np.array(values) / 100)
        
        bars = ax.barh(categories, values, color=colors, alpha=0.8, edgecolor='black')
        
        # Agregar valores al final de las barras
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax.text(value + 1, i, f'{value:.2f}', 
                   va='center', fontweight='bold', fontsize=9)
        
        ax.set_xlabel('Valor', fontsize=10)
        ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
        ax.set_xlim(0, max(values) * 1.15 if values else 100)
        ax.grid(axis='x', alpha=0.3)
        ax.set_axisbelow(True)
        
    def create_radar_chart(self, ax, categories, values, title):
        """Crear gráfico de radar/spider"""
        N = len(categories)
        
        # Calcular ángulos
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values = values + [values[0]]  # Cerrar el polígono
        angles += angles[:1]
        
        # Crear el gráfico
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Dibujar ejes
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        
        # Dibujar yticks
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=8)
        ax.set_rlabel_position(0)
        
        # Dibujar polígono
        ax.plot(angles, values, 'o-', linewidth=2, color='#0d6efd', label='Calidad')
        ax.fill(angles, values, alpha=0.25, color='#0d6efd')
        
        # Agregar líneas de referencia
        for angle, value, category in zip(angles[:-1], values[:-1], categories):
            ax.plot([angle, angle], [0, 100], '--', color='gray', alpha=0.3, linewidth=0.5)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True, alpha=0.3)