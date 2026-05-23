import pandas as pd

def read_csv(path):
    return pd.read_csv(path)


def save_parquet(df, path):
    df.to_parquet(path, index=False)