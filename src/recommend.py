from typing import List, Optional
import pandas as pd


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def recommend_by_ingredients(
    foods: pd.DataFrame,
    liked_ingredients: List[str],
    category: Optional[str] = None,
    top_n: int = 5,
) -> pd.DataFrame:
    liked = {i.strip().lower() for i in liked_ingredients if str(i).strip()}
    df = foods.copy()
    if category:
        df = df[df["category"].str.lower() == category.strip().lower()]
    df["score"] = df["ingredients"].apply(lambda t: jaccard(set(t), liked))
    df = df.sort_values(["score", "n_ingredients"], ascending=[False, True])
    return df.head(top_n)[["id", "title", "category", "score"]]


def recommend_similar_recipes(
    foods: pd.DataFrame,
    recipe_id: int,
    top_n: int = 5,
) -> pd.DataFrame:
    target = foods[foods["id"] == recipe_id]
    if target.empty:
        return pd.DataFrame()
    target_ing = set(target.iloc[0]["ingredients"])
    df = foods[foods["id"] != recipe_id].copy()
    df["score"] = df["ingredients"].apply(lambda t: jaccard(set(t), target_ing))
    return df.sort_values("score", ascending=False).head(top_n)[["id", "title", "category", "score"]]

