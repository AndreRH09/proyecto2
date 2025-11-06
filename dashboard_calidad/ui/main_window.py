# ui/main_window.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

from parsers.junit_parser import JUnitParser
from parsers.jacoco_parser import JaCoCoParser
from metrics.reliability_metrics import ReliabilityMetrics
from metrics.maintainability_metrics import MaintainabilityMetrics
from metrics.performance_metrics import PerformanceMetrics
from ui.charts import ChartGenerator
from metrics.quality_rating import QualityRatingCalculator, QualityReportGenerator


class QualityDashboard:
    """Dashboard principal de calidad de software"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard de Calidad de Software - IEEE/ISO")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variables de datos
        self.junit_data = None
        self.jacoco_data = None
        self.junit_path = tk.StringVar(value="No seleccionado")
        self.jacoco_path = tk.StringVar(value="No seleccionado")
        
        # Inicializar generador de gráficos
        self.chart_gen = ChartGenerator()
        
        # Configurar estilo
        self._setup_styles()
        
        # Crear interfaz
        self._create_header()
        self._create_file_selector()
        self._create_notebook()
        self._create_status_bar()
        
    def _setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones
        style.configure('Primary.TButton',
                       background='#0d6efd',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        
        # Estilo para frames de métricas
        style.configure('Metric.TFrame',
                       background='white',
                       relief='raised',
                       borderwidth=2)
        
        # Estilo para labels de métricas
        style.configure('MetricTitle.TLabel',
                       background='white',
                       font=('Arial', 10),
                       foreground='#6c757d')
        
        style.configure('MetricValue.TLabel',
                       background='white',
                       font=('Arial', 24, 'bold'))
        
    def _create_header(self):
        """Crear encabezado del dashboard"""
        header_frame = tk.Frame(self.root, bg='#0d6efd', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="📊 Dashboard de Calidad de Software",
            font=('Arial', 20, 'bold'),
            bg='#0d6efd',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_frame,
            text="Basado en estándares IEEE 982.1, IEEE 829, ISO/IEC 25010",
            font=('Arial', 10),
            bg='#0d6efd',
            fg='#ccddff'
        )
        subtitle_label.pack()
        
    def _create_file_selector(self):
        """Crear selector de archivos"""
        selector_frame = tk.Frame(self.root, bg='#f0f0f0')
        selector_frame.pack(fill='x', padx=20, pady=10)
        
        # Frame para JUnit
        junit_frame = ttk.LabelFrame(selector_frame, text="Reporte JUnit/Surefire", padding=10)
        junit_frame.grid(row=0, column=0, padx=5, sticky='ew')
        
        tk.Label(junit_frame, textvariable=self.junit_path, 
                relief='sunken', width=50).pack(side='left', padx=5)
        ttk.Button(junit_frame, text="Seleccionar XML", 
                  command=self._select_junit_file).pack(side='left')
        
        # Frame para JaCoCo
        jacoco_frame = ttk.LabelFrame(selector_frame, text="Reporte JaCoCo", padding=10)
        jacoco_frame.grid(row=0, column=1, padx=5, sticky='ew')
        
        tk.Label(jacoco_frame, textvariable=self.jacoco_path, 
                relief='sunken', width=50).pack(side='left', padx=5)
        ttk.Button(jacoco_frame, text="Seleccionar XML", 
                  command=self._select_jacoco_file).pack(side='left')
        
        # Botón de carga
        load_frame = tk.Frame(selector_frame, bg='#f0f0f0')
        load_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(load_frame, text="🔄 Cargar y Analizar Datos", 
                  style='Primary.TButton',
                  command=self._load_data).pack()
        
        selector_frame.columnconfigure(0, weight=1)
        selector_frame.columnconfigure(1, weight=1)
        
    def _create_notebook(self):
        """Crear pestañas del dashboard"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Pestaña 1: Fiabilidad
        self.reliability_frame = self._create_tab("🛡️ Fiabilidad")
        self.notebook.add(self.reliability_frame, text="Fiabilidad")
        
        # Pestaña 2: Mantenibilidad
        self.maintainability_frame = self._create_tab("⚙️ Mantenibilidad")
        self.notebook.add(self.maintainability_frame, text="Mantenibilidad")
        
        # Pestaña 3: Eficiencia
        self.performance_frame = self._create_tab("⏱️ Eficiencia")
        self.notebook.add(self.performance_frame, text="Eficiencia del Desempeño")
        
        # Pestaña 4: Resumen General
        self.summary_frame = self._create_tab("📈 Resumen")
        self.notebook.add(self.summary_frame, text="Resumen General")
        
    def _create_tab(self, title):
        """Crear estructura base de una pestaña"""
        frame = tk.Frame(self.notebook, bg='#f0f0f0')
        
        # Título de la pestaña
        title_label = tk.Label(
            frame,
            text=title,
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#212529'
        )
        title_label.pack(pady=10)
        
        # Frame para métricas
        metrics_frame = tk.Frame(frame, bg='#f0f0f0')
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        # Frame para gráficos
        charts_frame = tk.Frame(frame, bg='#f0f0f0')
        charts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Almacenar referencias
        frame.metrics_frame = metrics_frame
        frame.charts_frame = charts_frame
        
        return frame
        
    def _create_status_bar(self):
        """Crear barra de estado"""
        self.status_bar = tk.Label(
            self.root,
            text="Listo - Selecciona los archivos XML para comenzar",
            bd=1,
            relief='sunken',
            anchor='w',
            bg='#e9ecef',
            font=('Arial', 9)
        )
        self.status_bar.pack(side='bottom', fill='x')
        
    def _select_junit_file(self):
        """Seleccionar archivo JUnit XML"""
        filename = filedialog.askopenfilename(
            title="Seleccionar reporte JUnit",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            initialdir="data/junit_reports"
        )
        if filename:
            self.junit_path.set(filename)
            
    def _select_jacoco_file(self):
        """Seleccionar archivo JaCoCo XML"""
        filename = filedialog.askopenfilename(
            title="Seleccionar reporte JaCoCo",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
            initialdir="data/jacoco_reports"
        )
        if filename:
            self.jacoco_path.set(filename)
            
    def _load_data(self):
        """Cargar y procesar datos XML"""
        try:
            self.status_bar.config(text="Cargando datos...")
            self.root.update()
            
            # Cargar JUnit
            if self.junit_path.get() != "No seleccionado":
                parser = JUnitParser(self.junit_path.get())
                self.junit_data = parser.parse()
                self.status_bar.config(text="Datos JUnit cargados...")
                self.root.update()
            
            # Cargar JaCoCo
            if self.jacoco_path.get() != "No seleccionado":
                parser = JaCoCoParser(self.jacoco_path.get())
                self.jacoco_data = parser.parse()
                self.status_bar.config(text="Datos JaCoCo cargados...")
                self.root.update()
            
            # Actualizar visualizaciones
            self._update_reliability_tab()
            self._update_maintainability_tab()
            self._update_performance_tab()
            self._update_summary_tab()
            
            self.status_bar.config(text="✅ Datos cargados y analizados correctamente")
            messagebox.showinfo("Éxito", "Datos cargados correctamente")
            
        except Exception as e:
            self.status_bar.config(text=f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar datos:\n{str(e)}")
            
    def _update_reliability_tab(self):
        """Actualizar pestaña de Fiabilidad"""
        if not self.junit_data:
            return
            
        # Limpiar frame
        for widget in self.reliability_frame.metrics_frame.winfo_children():
            widget.destroy()
        for widget in self.reliability_frame.charts_frame.winfo_children():
            widget.destroy()
            
        # Calcular métricas
        rel_metrics = ReliabilityMetrics()
        failure_density = rel_metrics.calculate_failure_density(self.junit_data)
        success_rate = rel_metrics.calculate_success_rate(self.junit_data)
        status = rel_metrics.get_reliability_status(failure_density)
        
        # Crear tarjetas de métricas
        metrics = [
            ("Total de Pruebas", self.junit_data['total_tests'], "🧪", "#0d6efd"),
            ("Densidad de Fallos", f"{failure_density:.2f}%", "⚠️", self._get_status_color(status['color'])),
            ("Tasa de Éxito", f"{success_rate:.2f}%", "✅", "#28a745"),
            ("Fallos Totales", self.junit_data['failures'] + self.junit_data['errors'], "❌", "#dc3545")
        ]
        
        for i, (title, value, icon, color) in enumerate(metrics):
            self._create_metric_card(
                self.reliability_frame.metrics_frame,
                title, value, icon, color, i
            )
        
        # Crear gráficos
        self._create_reliability_charts()
        
    def _update_maintainability_tab(self):
        """Actualizar pestaña de Mantenibilidad"""
        if not self.jacoco_data:
            return
            
        # Limpiar frame
        for widget in self.maintainability_frame.metrics_frame.winfo_children():
            widget.destroy()
        for widget in self.maintainability_frame.charts_frame.winfo_children():
            widget.destroy()
            
        # Calcular métricas
        maint_metrics = MaintainabilityMetrics()
        testability = maint_metrics.get_testability_score(self.jacoco_data)
        status = maint_metrics.get_maintainability_status(testability)
        
        # Crear tarjetas de métricas
        metrics = [
            ("Cobertura de Líneas", f"{self.jacoco_data.get('line_coverage', 0):.2f}%", "📝", "#17a2b8"),
            ("Cobertura de Ramas", f"{self.jacoco_data.get('branch_coverage', 0):.2f}%", "🌳", "#ffc107"),
            ("Testability Score", f"{testability:.2f}%", "🧬", self._get_status_color(status['color']))
        ]
        
        for i, (title, value, icon, color) in enumerate(metrics):
            self._create_metric_card(
                self.maintainability_frame.metrics_frame,
                title, value, icon, color, i
            )
        
        # Crear gráficos
        self._create_maintainability_charts()
        
    def _update_performance_tab(self):
        """Actualizar pestaña de Eficiencia"""
        if not self.junit_data:
            return
            
        # Limpiar frame
        for widget in self.performance_frame.metrics_frame.winfo_children():
            widget.destroy()
        for widget in self.performance_frame.charts_frame.winfo_children():
            widget.destroy()
            
        # Calcular métricas
        perf_metrics = PerformanceMetrics()
        avg_time = perf_metrics.calculate_avg_test_time(self.junit_data)
        status = perf_metrics.get_performance_status(
            self.junit_data['execution_time'],
            self.junit_data['total_tests']
        )
        
        throughput = (self.junit_data['total_tests'] / self.junit_data['execution_time'] 
                     if self.junit_data['execution_time'] > 0 else 0)
        
        # Crear tarjetas de métricas
        metrics = [
            ("Tiempo Total", f"{self.junit_data['execution_time']:.2f}s", "⏱️", self._get_status_color(status['color'])),
            ("Tiempo Promedio", f"{avg_time:.3f}s", "⏰", "#0d6efd"),
            ("Throughput", f"{throughput:.2f} test/s", "🚀", "#28a745")
        ]
        
        for i, (title, value, icon, color) in enumerate(metrics):
            self._create_metric_card(
                self.performance_frame.metrics_frame,
                title, value, icon, color, i
            )
        
        # Crear gráficos
        self._create_performance_charts()
        
    def _update_summary_tab(self):
        """Actualizar pestaña de Resumen con Calificación General"""
        # Limpiar frames
        for widget in self.summary_frame.metrics_frame.winfo_children():
            widget.destroy()
        for widget in self.summary_frame.charts_frame.winfo_children():
            widget.destroy()
        
        if not self.junit_data and not self.jacoco_data:
            no_data_label = tk.Label(
                self.summary_frame.charts_frame,
                text="No hay datos cargados",
                font=('Arial', 14),
                bg='#f0f0f0',
                fg='#6c757d'
            )
            no_data_label.pack(pady=50)
            return
        
        # Calcular calificación general
        calculator = QualityRatingCalculator(self.junit_data, self.jacoco_data)
        wqs, details = calculator.calculate_weighted_quality_score()
        rating = details['rating']
        rating_info = calculator.get_rating_description(rating)
        color = details['rating_color']
        
        # ========== SECCIÓN SUPERIOR: RATING Y WQS ==========
        top_section = tk.Frame(self.summary_frame.metrics_frame, bg='#f0f0f0')
        top_section.pack(fill='x', pady=20)
        
        # Badge de Rating (más compacto)
        badge_frame = tk.Frame(top_section, bg=color, relief='raised', borderwidth=3)
        badge_frame.pack(side='left', padx=(50, 30))
        
        rating_label = tk.Label(
            badge_frame,
            text=rating,
            font=('Arial', 80, 'bold'),
            bg=color,
            fg='white',
            width=2,
            height=1
        )
        rating_label.pack(padx=15, pady=15)
        
        # Información del Rating
        info_frame = tk.Frame(top_section, bg='#f0f0f0')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Título
        title_label = tk.Label(
            info_frame,
            text="CALIFICACIÓN GENERAL DE CALIDAD",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#212529'
        )
        title_label.pack(anchor='w', pady=(10, 5))
        
        # WQS Score
        score_label = tk.Label(
            info_frame,
            text=f"Weighted Quality Score (WQS): {wqs:.2f}/100",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#495057'
        )
        score_label.pack(anchor='w', pady=5)
        
        # Estado
        status_label = tk.Label(
            info_frame,
            text=f"{rating_info['icon']} {rating_info['title']} - {rating_info['description']}",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg=color,
            wraplength=500
        )
        status_label.pack(anchor='w', pady=5)
        
        # Recomendación
        recommend_label = tk.Label(
            info_frame,
            text=f"💡 {rating_info['recommendation']}",
            font=('Arial', 11, 'italic'),
            bg='#f0f0f0',
            fg='#6c757d',
            wraplength=500
        )
        recommend_label.pack(anchor='w', pady=(5, 10))
        
        # ========== SEPARADOR ==========
        separator = tk.Frame(self.summary_frame.metrics_frame, bg='#dee2e6', height=2)
        separator.pack(fill='x', pady=15)
        
        # ========== MÉTRICAS INDIVIDUALES ==========
        scores_frame = tk.Frame(self.summary_frame.metrics_frame, bg='#f0f0f0')
        scores_frame.pack(fill='x', padx=50)
        
        # Tarjetas de scores (más compactas)
        scores_data = [
            ("Fiabilidad", details['scores']['reliability'], "🛡️", "#0d6efd", "40%"),
            ("Mantenibilidad", details['scores']['maintainability'], "⚙️", "#17a2b8", "40%"),
            ("Eficiencia", details['scores']['performance'], "⏱️", "#28a745", "20%")
        ]
        
        for i, (name, score, icon, score_color, weight) in enumerate(scores_data):
            self._create_compact_score_card(scores_frame, name, score, icon, score_color, weight, i)
        
        # ========== GRÁFICOS ==========
        self._create_summary_charts()
        
        # ========== FÓRMULA Y ESTÁNDARES (Compacto) ==========
        self._create_compact_formula_section()

    def _create_compact_score_card(self, parent, name, score, icon, color, weight, column):
        """Crear tarjeta compacta de score"""
        card = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        parent.columnconfigure(column, weight=1)
        
        # Peso (badge pequeño)
        weight_badge = tk.Label(
            card,
            text=weight,
            font=('Arial', 8, 'bold'),
            bg=color,
            fg='white',
            padx=5,
            pady=2
        )
        weight_badge.pack(pady=(8, 3))
        
        # Nombre
        name_label = tk.Label(
            card,
            text=f"{icon} {name}",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#212529'
        )
        name_label.pack(pady=3)
        
        # Score
        score_label = tk.Label(
            card,
            text=f"{score:.1f}",
            font=('Arial', 28, 'bold'),
            bg='white',
            fg=color
        )
        score_label.pack()
        
        # "/100"
        max_label = tk.Label(
            card,
            text="/100",
            font=('Arial', 9),
            bg='white',
            fg='#6c757d'
        )
        max_label.pack(pady=(0, 8))

    def _create_summary_charts(self):
        """Crear gráficos de resumen"""
        charts_container = self.summary_frame.charts_frame
        
        # Crear figura con 2 gráficos
        fig = Figure(figsize=(12, 5), facecolor='#f0f0f0')
        
        # Preparar datos
        categories = []
        values = []
        
        if self.junit_data:
            rel_metrics = ReliabilityMetrics()
            success_rate = rel_metrics.calculate_success_rate(self.junit_data)
            categories.append('Fiabilidad')
            values.append(success_rate)
        
        if self.jacoco_data:
            maint_metrics = MaintainabilityMetrics()
            testability = maint_metrics.get_testability_score(self.jacoco_data)
            categories.append('Mantenibilidad')
            values.append(testability)
        
        if self.junit_data:
            perf_metrics = PerformanceMetrics()
            avg_time = perf_metrics.calculate_avg_test_time(self.junit_data)
            normalized_perf = max(0, 100 - (avg_time * 100))
            categories.append('Eficiencia')
            values.append(normalized_perf)
        
        # Gráfico 1: Radar Chart
        ax1 = fig.add_subplot(121)
        self.chart_gen.create_radar_chart(ax1, categories, values, 
                                        "Características de Calidad")
        
        # Gráfico 2: Barras comparativas
        ax2 = fig.add_subplot(122)
        colors_bars = ['#0d6efd', '#17a2b8', '#28a745']
        bars = ax2.barh(categories, values, color=colors_bars, alpha=0.8, edgecolor='black')
        
        # Agregar valores
        for bar, value in zip(bars, values):
            ax2.text(value + 2, bar.get_y() + bar.get_height()/2, 
                    f'{value:.1f}',
                    va='center', fontweight='bold', fontsize=11)
        
        ax2.set_xlabel('Puntuación', fontsize=10)
        ax2.set_title('Comparativa de Métricas', fontsize=12, fontweight='bold', pad=15)
        ax2.set_xlim(0, 110)
        ax2.axvline(x=80, color='green', linestyle='--', alpha=0.5, label='Umbral Bueno')
        ax2.axvline(x=60, color='orange', linestyle='--', alpha=0.5, label='Umbral Mínimo')
        ax2.legend(loc='lower right', fontsize=8)
        ax2.grid(axis='x', alpha=0.3)
        ax2.set_axisbelow(True)
        
        fig.tight_layout()
        
        # Embeber
        canvas = FigureCanvasTkAgg(fig, master=charts_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, pady=10)

    def _create_compact_formula_section(self):
        """Crear sección compacta de fórmula y estándares"""
        formula_frame = tk.Frame(self.summary_frame.charts_frame, bg='white', 
                                relief='solid', borderwidth=1)
        formula_frame.pack(fill='x', padx=50, pady=(10, 20))
        
        # Título
        title = tk.Label(
            formula_frame,
            text="📐 Cálculo de WQS (Weighted Quality Score)",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#212529'
        )
        title.pack(pady=(10, 5))
        
        # Fórmula
        calculator = QualityRatingCalculator(self.junit_data, self.jacoco_data)
        wqs, details = calculator.calculate_weighted_quality_score()
        
        formula_label = tk.Label(
            formula_frame,
            text=f"Fórmula: {details['formula']}",
            font=('Courier', 10, 'bold'),
            bg='white',
            fg='#0d6efd'
        )
        formula_label.pack(pady=3)
        
        # Cálculo
        calc_label = tk.Label(
            formula_frame,
            text=details['calculation'],
            font=('Courier', 9),
            bg='white',
            fg='#495057'
        )
        calc_label.pack(pady=3)
        
        # Estándares aplicados
        standards_text = (
            "Estándares: IEEE 982.1-1988 (Fiabilidad) | "
            "IEEE 829-2008, ISO/IEC 25010 (Mantenibilidad) | "
            "ISO/IEC 25010 (Eficiencia)"
        )
        standards_label = tk.Label(
            formula_frame,
            text=standards_text,
            font=('Arial', 8, 'italic'),
            bg='white',
            fg='#6c757d',
            wraplength=800
        )
        standards_label.pack(pady=(5, 10))
        
        # Botones de exportación (inline)
        export_frame = tk.Frame(formula_frame, bg='white')
        export_frame.pack(pady=(5, 10))
        
        ttk.Button(
            export_frame,
            text="📄 Exportar Reporte TXT",
            command=lambda: self._export_text_report(calculator)
        ).pack(side='left', padx=5)
        
        ttk.Button(
            export_frame,
            text="🌐 Exportar Reporte HTML",
            command=lambda: self._export_html_report(calculator)
        ).pack(side='left', padx=5)

    def _export_text_report(self, calculator):
        """Exportar reporte en formato texto"""
        try:
            generator = QualityReportGenerator(calculator)
            report_text = generator.generate_text_report()
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Guardar Reporte de Calidad"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                messagebox.showinfo("Éxito", f"Reporte exportado a:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar reporte:\n{str(e)}")

    def _export_html_report(self, calculator):
        """Exportar reporte en formato HTML"""
        try:
            import webbrowser
            
            generator = QualityReportGenerator(calculator)
            report_html = generator.generate_html_report()
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                title="Guardar Reporte de Calidad"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report_html)
                messagebox.showinfo("Éxito", f"Reporte HTML exportado correctamente")
                
                if messagebox.askyesno("Abrir Reporte", "¿Desea abrir el reporte en el navegador?"):
                    webbrowser.open(f'file://{filename}')
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar reporte:\n{str(e)}")
        
    def _create_metric_card(self, parent, title, value, icon, color, column):
        """Crear tarjeta de métrica individual"""
        card = tk.Frame(parent, bg='white', relief='raised', borderwidth=2)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        parent.columnconfigure(column, weight=1)
        
        # Ícono
        icon_label = tk.Label(
            card,
            text=icon,
            font=('Arial', 32),
            bg='white'
        )
        icon_label.pack(pady=(10, 5))
        
        # Título
        title_label = tk.Label(
            card,
            text=title,
            font=('Arial', 10),
            bg='white',
            fg='#6c757d'
        )
        title_label.pack()
        
        # Valor
        value_label = tk.Label(
            card,
            text=str(value),
            font=('Arial', 24, 'bold'),
            bg='white',
            fg=color
        )
        value_label.pack(pady=(5, 10))
        
    def _create_reliability_charts(self):
        """Crear gráficos de fiabilidad"""
        charts_frame = self.reliability_frame.charts_frame
        
        # Crear figura con subplots
        fig = Figure(figsize=(12, 5), facecolor='#f0f0f0')
        
        # Gráfico 1: Gauge de tasa de éxito
        ax1 = fig.add_subplot(121)
        success_rate = ReliabilityMetrics.calculate_success_rate(self.junit_data)
        self.chart_gen.create_gauge_chart(ax1, success_rate, "Tasa de Éxito (%)")
        
        # Gráfico 2: Distribución de pruebas
        ax2 = fig.add_subplot(122)
        labels = ['Pasadas', 'Falladas', 'Errores', 'Omitidas']
        sizes = [
            self.junit_data['passed'],
            self.junit_data['failures'],
            self.junit_data['errors'],
            self.junit_data['skipped']
        ]
        colors = ['#28a745', '#dc3545', '#fd7e14', '#6c757d']
        self.chart_gen.create_pie_chart(ax2, sizes, labels, colors, 
                                        "Distribución de Resultados")
        
        fig.tight_layout()
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_maintainability_charts(self):
        """Crear gráficos de mantenibilidad"""
        charts_frame = self.maintainability_frame.charts_frame
        
        # Crear figura
        fig = Figure(figsize=(12, 5), facecolor='#f0f0f0')
        
        # Gráfico 1: Barras de cobertura
        ax1 = fig.add_subplot(121)
        categories = ['Líneas', 'Ramas', 'Instrucciones']
        values = [
            self.jacoco_data.get('line_coverage', 0),
            self.jacoco_data.get('branch_coverage', 0),
            self.jacoco_data.get('instruction_coverage', 0)
        ]
        colors = ['#17a2b8', '#ffc107', '#6f42c1']
        self.chart_gen.create_bar_chart(ax1, categories, values, colors, 
                                        "Cobertura de Código (%)")
        
        # Gráfico 2: Cobertura por paquete
        ax2 = fig.add_subplot(122)
        if self.jacoco_data.get('package_details'):
            pkg_df = pd.DataFrame(self.jacoco_data['package_details'])
            self.chart_gen.create_horizontal_bar_chart(
                ax2,
                pkg_df['name'].tolist()[:10],  # Top 10 paquetes
                pkg_df['line_coverage'].tolist()[:10],
                "Cobertura por Paquete (%)"
            )
        
        fig.tight_layout()
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_performance_charts(self):
        """Crear gráficos de eficiencia"""
        charts_frame = self.performance_frame.charts_frame
        
        # Crear figura
        fig = Figure(figsize=(12, 5), facecolor='#f0f0f0')
        
        # Gráfico: Top 10 pruebas más lentas
        ax = fig.add_subplot(111)
        
        if self.junit_data.get('test_details'):
            test_times = [(t['name'], t['time']) for t in self.junit_data['test_details']]
            test_times.sort(key=lambda x: x[1], reverse=True)
            top_tests = test_times[:10]
            
            names = [t[0].split('.')[-1][:30] for t in top_tests]  # Acortar nombres
            times = [t[1] for t in top_tests]
            
            self.chart_gen.create_horizontal_bar_chart(
                ax, names, times, "Top 10 Pruebas Más Lentas (segundos)"
            )
        
        fig.tight_layout()
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_summary_chart(self):
        """Crear gráfico resumen de todas las métricas"""
        charts_frame = self.summary_frame.charts_frame
        
        # Crear figura
        fig = Figure(figsize=(10, 6), facecolor='#f0f0f0')
        ax = fig.add_subplot(111)
        
        # Preparar datos
        categories = []
        values = []
        colors_list = []
        
        if self.junit_data:
            rel_metrics = ReliabilityMetrics()
            success_rate = rel_metrics.calculate_success_rate(self.junit_data)
            categories.append('Fiabilidad\n(Tasa Éxito)')
            values.append(success_rate)
            colors_list.append('#28a745')
        
        if self.jacoco_data:
            maint_metrics = MaintainabilityMetrics()
            testability = maint_metrics.get_testability_score(self.jacoco_data)
            categories.append('Mantenibilidad\n(Testability)')
            values.append(testability)
            colors_list.append('#17a2b8')
        
        if self.junit_data:
            perf_metrics = PerformanceMetrics()
            avg_time = perf_metrics.calculate_avg_test_time(self.junit_data)
            # Normalizar tiempo a escala 0-100 (inversamente proporcional)
            normalized_perf = max(0, 100 - (avg_time * 100))
            categories.append('Eficiencia\n(Rendimiento)')
            values.append(normalized_perf)
            colors_list.append('#ffc107')
        
        # Crear gráfico de radar/spider
        self.chart_gen.create_radar_chart(ax, categories, values, 
                                          "Resumen de Calidad del Software")
        
        fig.tight_layout()
        
        # Embeber en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _get_status_color(self, status_color):
        """Convertir colores de estado a códigos hex"""
        color_map = {
            'success': '#28a745',
            'info': '#17a2b8',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'primary': '#0d6efd'
        }
        return color_map.get(status_color, '#6c757d')


def main():
    """Función principal"""
    root = tk.Tk()
    app = QualityDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()