# GitHub Actions Workflows

Este directorio contiene los workflows de GitHub Actions para automatizar y verificar el proyecto de pruebas de PDF.

## Workflows Disponibles

### 1. CI (ci.yml)
**Trigger:** Push y Pull Requests a las ramas main/master/develop

**Qué hace:**
- Compila el proyecto Java con Maven
- Ejecuta las pruebas automatizadas
- Configura Chrome y ChromeDriver automáticamente
- Sube los resultados de las pruebas como artefactos
- Genera un resumen de la ejecución

**Configuración necesaria:**
- `APPLITOOLS_API_KEY`: Secret de GitHub con tu API key de Applitools (opcional)

### 2. Release (release.yml)
**Trigger:** Creación de un release o ejecución manual

**Qué hace:**
- Compila el proyecto para release
- Ejecuta todas las pruebas
- Genera artefactos para distribución

### 3. Nightly (nightly.yml)
**Trigger:** Ejecución diaria a las 2 AM UTC o ejecución manual

**Qué hace:**
- Ejecuta la suite completa de pruebas cada noche
- Notifica en Slack si hay fallos (opcional)

**Configuración necesaria:**
- `APPLITOOLS_API_KEY`: Secret de GitHub
- `SLACK_WEBHOOK_URL`: Secret de GitHub para notificaciones (opcional)

## Configuración de Secrets

Para configurar los secrets en GitHub:

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click en "New repository secret"
4. Agrega los siguientes secrets:

### APPLITOOLS_API_KEY
Tu API key de Applitools para validación visual de PDFs.

**Obtener la API key:**
1. Ve a https://applitools.com/
2. Crea una cuenta o inicia sesión
3. Ve al Dashboard
4. Copia tu API Key

### SLACK_WEBHOOK_URL (Opcional)
Webhook URL de Slack para notificaciones de fallos en pruebas nocturnas.

## Uso Local

Para ejecutar los mismos pasos localmente:

```bash
# Instalar dependencias
mvn clean install

# Ejecutar pruebas
mvn test

# Con configuración específica
mvn test -Dtest=PDFTests
```

## Estructura de Artefactos

Los workflows generan los siguientes artefactos:

- **test-results**: Reportes de pruebas en formato XML y texto
- **screenshots**: Capturas de pantalla si hay fallos
- **generated-pdfs**: PDFs generados durante las pruebas

## Troubleshooting

### ChromeDriver no se encuentra
El workflow descarga automáticamente ChromeDriver compatible con la versión de Chrome instalada.

### ImageTester.jar faltante
El workflow continuará sin ImageTester.jar, pero las pruebas de validación de PDF fallarán. Descarga manualmente desde:
https://applitools.com/tutorials/sdk/pdf-testing.html

### Pruebas fallan por timeout
Aumenta el timeout en `BaseTests.java` o ajusta las esperas en los Page Objects.

## Personalización

Puedes modificar los workflows para:
- Cambiar la versión de Java
- Agregar más pasos de validación
- Integrar con otros servicios
- Configurar notificaciones adicionales

0