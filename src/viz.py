import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .utils import PROCESSED_DIR


def plot_category_counts(foods: pd.DataFrame):
    plt.figure(figsize=(6,4))
    ax = sns.countplot(x="category", data=foods, order=foods["category"].value_counts().index)
    plt.xticks(rotation=30, ha="right")
    plt.title("Recipes by Category")
    plt.tight_layout()
    out = PROCESSED_DIR / "category_counts.png"
    plt.savefig(out)
    plt.close()
    return out


def plot_top_ingredients(foods: pd.DataFrame, top_k: int = 15):
    # expand ingredients
    exploded = foods.explode("ingredients")
    counts = exploded["ingredients"].value_counts().head(top_k).reset_index()
    counts.columns = ["ingredient", "count"]
    plt.figure(figsize=(6,4))
    sns.barplot(y="ingredient", x="count", data=counts)
    plt.title("Top Ingredients")
    plt.tight_layout()
    out = PROCESSED_DIR / "top_ingredients.png"
    plt.savefig(out)
    plt.close()
    return out

