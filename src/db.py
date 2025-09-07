import sqlite3
from contextlib import closing
from typing import Iterable, Dict, Any
from .utils import DB_PATH

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS recipes (
  recipe_id INTEGER PRIMARY KEY,
  title TEXT,
  description TEXT,
  category TEXT
);

CREATE TABLE IF NOT EXISTS ingredients (
  ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
  recipe_id INTEGER,
  ingredient_id INTEGER,
  PRIMARY KEY (recipe_id, ingredient_id),
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
  FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ratings (
  user_id INTEGER,
  recipe_id INTEGER,
  rating REAL,
  PRIMARY KEY (user_id, recipe_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
);
"""

def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with closing(get_conn()) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()


def upsert_recipe(recipe: Dict[str, Any], ingredients: Iterable[str]):
    with closing(get_conn()) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO recipes(recipe_id, title, description, category) VALUES (?, ?, ?, ?)",
            (recipe["id"], recipe.get("title"), recipe.get("description", ""), recipe.get("category", "")),
        )
        # ingredients
        for name in ingredients:
            cur.execute("INSERT OR IGNORE INTO ingredients(name) VALUES (?)", (name,))
            cur.execute("SELECT ingredient_id FROM ingredients WHERE name = ?", (name,))
            ing_id = cur.fetchone()[0]
            cur.execute(
                "INSERT OR IGNORE INTO recipe_ingredients(recipe_id, ingredient_id) VALUES (?, ?)",
                (recipe["id"], ing_id),
            )
        conn.commit()

