"""
Funciones de apoyo para el laboratorio de dashboards.
Estas funciones están preparadas para que el estudiante se concentre
en el diseño de la interfaz y la integración de visualizaciones.

Dataset: UCI Bike Sharing Dataset, archivo hour.csv.
Variables meteorológicas temp, atemp, hum y windspeed están normalizadas.
"""

from pathlib import Path
import zipfile
import urllib.request

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
CSV_PATH = DATA_DIR / "hour.csv"
ZIP_PATH = DATA_DIR / "bike_sharing_dataset.zip"
UCI_URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"


def load_data() -> pd.DataFrame:
    """Carga hour.csv; si no existe, descarga y extrae el conjunto de datos."""
    DATA_DIR.mkdir(exist_ok=True)

    if not CSV_PATH.exists():
        urllib.request.urlretrieve(UCI_URL, ZIP_PATH)
        with zipfile.ZipFile(ZIP_PATH, "r") as archive:
            member = next(
                (name for name in archive.namelist() if name.endswith("hour.csv")),
                None
            )
            if member is None:
                raise FileNotFoundError("No se encontró hour.csv dentro del ZIP de UCI.")
            with archive.open(member) as source:
                CSV_PATH.write_bytes(source.read())

    return pd.read_csv(CSV_PATH)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Añade etiquetas interpretables y variables temporales."""
    data = df.copy()
    data["datetime"] = pd.to_datetime(data["dteday"]) + pd.to_timedelta(data["hr"], unit="h")
    data["year_label"] = data["yr"].map({0: "2011", 1: "2012"})
    data["season_label"] = data["season"].map({
        1: "Invierno", 2: "Primavera", 3: "Verano", 4: "Otoño"
    })
    data["weekday_label"] = data["weekday"].map({
        0: "Domingo", 1: "Lunes", 2: "Martes", 3: "Miércoles",
        4: "Jueves", 5: "Viernes", 6: "Sábado"
    })
    data["weather_label"] = data["weathersit"].map({
        1: "Despejado o parcialmente nublado",
        2: "Niebla o nublado",
        3: "Lluvia ligera o nieve",
        4: "Condiciones severas"
    })
    data["day_type"] = data["workingday"].map({
        0: "No laboral", 1: "Laboral"
    })
    data["total_users_check"] = data["casual"] + data["registered"]
    return data


def filter_data(
    df: pd.DataFrame,
    years=None,
    months=None,
    day_types=None,
    seasons=None
) -> pd.DataFrame:
    """Filtra por año, mes, tipo de día y estación. None significa sin filtro."""
    data = df.copy()

    if years:
        data = data[data["year_label"].isin(years)]
    if months:
        data = data[data["mnth"].isin(months)]
    if day_types:
        data = data[data["day_type"].isin(day_types)]
    if seasons:
        data = data[data["season_label"].isin(seasons)]

    return data


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calcula indicadores generales para el subconjunto recibido."""
    if df.empty:
        return {
            "total_rentals": 0,
            "mean_hourly_rentals": 0,
            "registered_share_pct": 0.0,
            "casual_share_pct": 0.0,
            "peak_hour": None,
        }

    total = int(df["cnt"].sum())
    registered = int(df["registered"].sum())
    casual = int(df["casual"].sum())
    peak_hour = int(df.groupby("hr")["cnt"].mean().idxmax())

    return {
        "total_rentals": total,
        "mean_hourly_rentals": float(df["cnt"].mean()),
        "registered_share_pct": (registered / total * 100) if total else 0.0,
        "casual_share_pct": (casual / total * 100) if total else 0.0,
        "peak_hour": peak_hour,
    }


def aggregate_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """Demanda media por hora del día."""
    return (
        df.groupby("hr", as_index=False)["cnt"]
        .mean()
        .rename(columns={"hr": "hour", "cnt": "mean_rentals"})
        .sort_values("hour")
    )


def aggregate_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """Demanda total por fecha."""
    return (
        df.groupby("dteday", as_index=False)["cnt"]
        .sum()
        .rename(columns={"dteday": "date", "cnt": "rentals"})
        .sort_values("date")
    )


def compare_users(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara comparación entre usuarios ocasionales y registrados."""
    return pd.DataFrame({
        "Tipo de usuario": ["Ocasionales", "Registrados"],
        "Alquileres": [int(df["casual"].sum()), int(df["registered"].sum())]
    })


def aggregate_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """Demanda media por día de la semana."""
    order = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    result = (
        df.groupby("weekday_label", as_index=False)["cnt"]
        .mean()
        .rename(columns={"cnt": "mean_rentals"})
    )
    result["weekday_label"] = pd.Categorical(
        result["weekday_label"], categories=order, ordered=True
    )
    return result.sort_values("weekday_label")


def get_summary(df: pd.DataFrame) -> dict:
    """Resumen descriptivo básico del subconjunto recibido."""
    if df.empty:
        return {"records": 0, "days": 0, "mean": 0, "median": 0, "maximum": 0}
    return {
        "records": int(len(df)),
        "days": int(df["dteday"].nunique()),
        "mean": float(df["cnt"].mean()),
        "median": float(df["cnt"].median()),
        "maximum": int(df["cnt"].max()),
    }
