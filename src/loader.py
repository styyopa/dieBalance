import pandas as pd

RENAME_MAP = {
    "Carbohydrates": "carbs",
    "Glycemic Index": "glycemic_index",
    "Protein": "protein",
    "Fiber": "fiber",
    "Fat": "fat",
}


def load_foods(path: str = "data/foods.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    return df.rename(columns=RENAME_MAP)


def get_food_by_name(df: pd.DataFrame, name: str):
    match = df[df["name"].str.lower() == name.lower()]
    if match.empty:
        return None
    return match.iloc[0]


if __name__ == "__main__":
    foods = load_foods()
    print(foods.head())
    print(f"\nTotal products loaded: {len(foods)}")
