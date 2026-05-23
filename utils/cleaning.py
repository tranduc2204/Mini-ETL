import pandas as pd


def trim_all_string_columns(df):
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()
    return df


def normalize_email(df, column):
    df[column] = df[column].str.lower()
    return df


def remove_duplicates(df, subset):
    return df.drop_duplicates(subset=subset)
