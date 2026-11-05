# Sesión 9 — Laboratorio de dashboard con Streamlit

## Objetivo
Construir individualmente una aplicación interactiva para explorar la demanda histórica del sistema de bicicletas compartidas de Washington D. C. (2011–2012).

## Entorno
GitHub Codespaces + Python 3.11 + Streamlit + Pandas + Plotly.

## Inicio rápido
1. Sube **el contenido** de esta carpeta a un repositorio GitHub (no el ZIP como único archivo).
2. Crea un Codespace desde la rama `main`.
3. Espera a que se instalen las dependencias.
4. En la terminal ejecuta `streamlit run app.py`.
5. Abre el puerto 8501 desde la pestaña **Ports** si no se abre automáticamente.

Si la instalación automática no se ejecuta:
`pip install -r requirements.txt`

## Archivos
- `app.py`: estructura inicial de la aplicación. Completa los apartados `TODO`.
- `data_processing.py`: funciones de carga, preparación, filtrado y agregación ya implementadas.
- `requirements.txt`: bibliotecas necesarias.
- `.devcontainer/devcontainer.json`: configuración del entorno de Codespaces.
- `data/`: carpeta donde se descarga `hour.csv` automáticamente.

## Requisitos mínimos
1. Al menos cuatro KPI.
2. Evolución temporal de la demanda.
3. Comparación de al menos dos grupos o categorías.
4. Distribución de la demanda por una dimensión temporal.
5. Al menos dos controles de interacción.
6. Los KPI y gráficos deben responder coherentemente a los filtros.
7. Interfaz organizada y legible.
8. Al menos dos conclusiones sustentadas en los datos.

## Importante
La primera ejecución descarga el conjunto de datos desde UCI y requiere conexión a Internet. No subas credenciales ni datos personales al repositorio. Si trabajas en un repositorio privado, revisa que el docente tenga acceso.

## Limitaciones del conjunto
Los datos son históricos, de Washington D. C. (2011–2012), y cada registro representa una hora. `temp`, `atemp`, `hum` y `windspeed` están normalizadas. No hay inventario ni disponibilidad por estación. No se pueden inferir causalidades a partir de correlaciones.
