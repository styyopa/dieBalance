
import pandas as pd

NUMERIC_COLUMNS = [
    "carbs",
    "glycemic_index",
    "protein",
    "fiber",
    "fat"
]


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].fillna(0)
    return df


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def remove_negative_values(df: pd.DataFrame) -> pd.DataFrame:
    for column in NUMERIC_COLUMNS:
        df[column] = df[column].clip(lower=0)

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_duplicates(df)
    df = convert_numeric_columns(df)
    df = clean_missing_values(df)
    df = remove_negative_values(df)

    return df