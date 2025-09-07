import json
import pandas as pd
from typing import Tuple
from .utils import RAW_JSON

# Optional API enrichment example
import requests


def load_raw() -> Tuple[pd.DataFrame, pd.DataFrame]:
    with open(RAW_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    foods = pd.DataFrame(data.get("foods", []))
    categories = pd.DataFrame(data.get("categories", []))
    return foods, categories


def fetch_mealdb_example(query: str = "chicken") -> pd.DataFrame:
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        j = r.json()
        meals = j.get("meals") or []
        return pd.DataFrame(meals)
    except Exception:
        return pd.DataFrame()

