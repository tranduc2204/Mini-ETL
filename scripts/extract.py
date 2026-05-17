import pandas as pd
from db import engine

def extract_changes(old_watermark, batch_end):

    query = f"""
    SELECT *
    FROM orders_cdc_log
    WHERE changed_at > '{old_watermark}'
    AND changed_at <= '{batch_end}'
    ORDER BY changed_at
    """

    df = pd.read_sql(query, engine)

    return df