"""
SESIÓN 9 — Laboratorio: diseño y construcción de un dashboard
Versión de trabajo para estudiantes.

Completa los apartados TODO. Ejecuta con:
    streamlit run app.py
"""

import streamlit as st
import plotly.express as px

from data_processing import (
    load_data, prepare_data, filter_data, calculate_kpis,
    aggregate_by_hour, aggregate_by_day, compare_users,
    aggregate_by_weekday, get_summary
)

st.set_page_config(
    page_title="Dashboard de bicicletas compartidas",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def get_dataset():
    return prepare_data(load_data())

df = get_dataset()

st.title("🚲 Análisis del sistema de bicicletas compartidas")
st.caption("Exploración de la demanda histórica de alquileres en Washington D. C. (2011–2012)")

# =========================================================
# 1. DISEÑO DE FILTROS
# Requisito: al menos DOS controles de interacción.
# =========================================================
st.sidebar.header("Filtros")

# TODO 1. Crea un multiselect para seleccionar uno o ambos años.
# Pista: años disponibles = sorted(df["year_label"].unique())
selected_years = None

# TODO 2. Crea otro control: tipo de día, estación o mes.
selected_day_types = None

# TODO 3. (Opcional) Añade filtros adicionales.
selected_months = None
selected_seasons = None

filtered = filter_data(
    df,
    years=selected_years,
    months=selected_months,
    day_types=selected_day_types,
    seasons=selected_seasons,
)

if filtered.empty:
    st.warning("No hay registros para la combinación de filtros seleccionada.")
    st.stop()

# =========================================================
# 2. INDICADORES KPI
# Requisito: mostrar al menos CUATRO indicadores relevantes.
# =========================================================
kpis = calculate_kpis(filtered)
st.subheader("Indicadores principales")

# TODO 4. Organiza cuatro indicadores con st.columns() y st.metric().
# Sugerencias disponibles en kpis:
# total_rentals, mean_hourly_rentals, registered_share_pct,
# casual_share_pct y peak_hour.

# =========================================================
# 3. VISUALIZACIONES
# Requisito: evolución temporal, comparación de grupos y
# distribución por una dimensión temporal.
# =========================================================
st.subheader("Comportamiento de la demanda")

# TODO 5. Evolución temporal: usa aggregate_by_day().
daily = aggregate_by_day(filtered)
# Construye un gráfico de líneas con px.line() y muéstralo
# mediante st.plotly_chart(..., use_container_width=True).

# TODO 6. Patrón horario: usa aggregate_by_hour().
hourly = aggregate_by_hour(filtered)
# Construye un gráfico de barras con px.bar().

# TODO 7. Comparación de usuarios: usa compare_users().
users = compare_users(filtered)
# Construye un gráfico apropiado (por ejemplo, px.pie() o px.bar()).

# TODO 8. (Recomendado) Compara la demanda por día de la semana.
weekday = aggregate_by_weekday(filtered)
# Construye otro gráfico con px.bar().

# =========================================================
# 4. RESUMEN E INTERPRETACIÓN
# =========================================================
st.subheader("Resumen del subconjunto seleccionado")
summary = get_summary(filtered)

# TODO 9. Presenta al menos dos medidas del resumen:
# records, days, mean, median y maximum.

# TODO 10. Escribe al menos DOS conclusiones basadas en los
# resultados visibles. Deben referirse al subconjunto filtrado.
st.info("Escribe aquí una conclusión basada en los resultados del dashboard.")

with st.expander("Acerca de los datos y sus limitaciones"):
    st.markdown(
        """
        **Fuente:** UCI Machine Learning Repository — Bike Sharing Dataset.

        Los registros corresponden a Washington D. C. durante 2011 y 2012.
        Cada fila representa una hora de operación.

        Las variables `temp`, `atemp`, `hum` y `windspeed` están normalizadas.
        No deben interpretarse directamente como grados Celsius, humedad
        porcentual o velocidad en km/h.

        El conjunto no contiene inventario por estación ni disponibilidad en
        tiempo real. Una asociación entre variables no demuestra causalidad.
        """
    )
