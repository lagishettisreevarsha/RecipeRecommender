import re
import numpy as np
import pandas as pd
from typing import Tuple


def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = re.sub(r"\*\*?", "", s)  # remove markdown bold
    s = s.strip()
    return s


def to_ingredient_set(x) -> tuple:
    if isinstance(x, (list, tuple)):
        norm = sorted({str(i).strip().lower() for i in x if str(i).strip()})
        return tuple(norm)
    if isinstance(x, str):
        parts = [p.strip().lower() for p in re.split(r",|;|/|\n", x) if p.strip()]
        return tuple(sorted(set(parts)))
    return tuple()


def clean_foods(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["title"] = out["title"].astype(str).str.strip()
    out["description"] = out["description"].apply(normalize_text)
    out["category"] = out.get("category", "").astype(str)
    out["ingredients"] = out.get("ingredients", []).apply(to_ingredient_set)
    out["n_ingredients"] = out["ingredients"].apply(len)
    out = out.dropna(subset=["id", "title"]).reset_index(drop=True)
    return out

