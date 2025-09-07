import argparse
import pandas as pd

# Allow running both as a module (py -m src.app) and as a script (python src/app.py)
try:
    from . import data_ingest, data_clean, recommend, db, viz
    from .utils import DEFAULT_TOP_N
except ImportError:  # no known parent package -> fallback for direct execution
    import sys, pathlib
    ROOT = pathlib.Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))
    from src import data_ingest, data_clean, recommend, db, viz
    from src.utils import DEFAULT_TOP_N


def run_pipeline():
    foods_raw, _ = data_ingest.load_raw()
    foods = data_clean.clean_foods(foods_raw)

    # DB init and load
    db.init_db()
    for _, row in foods.iterrows():
        rec = {
            "id": int(row["id"]),
            "title": row["title"],
            "description": row.get("description", ""),
            "category": row.get("category", "")
        }
        db.upsert_recipe(rec, row["ingredients"])

    # Visualizations
    p1 = viz.plot_category_counts(foods)
    p2 = viz.plot_top_ingredients(foods)
    print(f"Saved plots: {p1}, {p2}")

    # Sample recommendations
    print("\nSample: Recommend by ingredients ['chicken','tomato']")
    recs = recommend.recommend_by_ingredients(foods, ["chicken", "tomato"], top_n=DEFAULT_TOP_N)
    print(recs.to_string(index=False))

    if not foods.empty:
        rid = int(foods.iloc[0]["id"])
        print(f"\nSample: Similar to recipe id {rid} ({foods.iloc[0]['title']})")
        recs2 = recommend.recommend_similar_recipes(foods, rid, top_n=DEFAULT_TOP_N)
        print(recs2.to_string(index=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-all", action="store_true", help="Run full pipeline")
    args = parser.parse_args()

    if args.run_all:
        run_pipeline()
    else:
        print("Use --run-all to ingest, clean, load DB, plot, and print sample recommendations.")

if __name__ == "__main__":
    main()
