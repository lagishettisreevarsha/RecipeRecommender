from src.data_clean import to_ingredient_set

def test_to_ingredient_set_list():
    assert to_ingredient_set(["Tomato", "tomato", " basil "]) == ("basil", "tomato")

