import pandas as pd 
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from scripts.bronze.bronze_watermark import get_watermark, update_watermark
from scripts.bronze.conn import engine
from scripts.bronze.bronze_extract_changes import extract_changes


def bronze_extract (**context):


    pipeline_name = "orders_cdc"

    old_watermark = get_watermark(pipeline_name)

    batch_end_query = """
        SELECT MAX(changed_at) AS batch_end
        FROM orders_cdc_log
    """

    batch_end = pd.read_sql(
        batch_end_query,
        engine
    ).iloc[0]["batch_end"]

    if pd.isna(batch_end):
        print("No CDC data found.")
        return

    print(f"Old watermark: {old_watermark}")
    print(f"Batch end: {batch_end}")

    filename = datetime.now(timezone.utc).strftime(
        "data/bronze/orders_%Y%m%d%H%M%S_%f.csv"
    )

    df = extract_changes(old_watermark, batch_end)

    if df.empty:
        print("No new changes.")
        return

    print(f"Extracted {len(df)} records")

    filename = datetime.now(timezone.utc).strftime(
        "data/bronze/orders_%Y%m%d%H%M%S_%f.csv"
    )

    df.to_csv(filename, index=False)

    update_watermark(pipeline_name, batch_end)

    print(f"Bronze file created: {filename}")
    print("Pipeline completed.")

    # # Step1 get the last watermark it mean the last time we run pipeline to extract
    # old_watermark = get_watermark("orders_cdc")
    # batch_end_query = """
    #     SELECT MAX(changed_at) AS batch_end
    #     FROM orders_cdc_log
    # """

    # batch_end = pd.read_sql(
    #     batch_end_query,
    #     engine
    # ).iloc[0]["batch_end"]
    # print ("Old watermark: ", old_watermark)
    # print ("Batch end: ", batch_end)
    # df = extract_changes(old_watermark, batch_end)

    
    # if not df.empty:

    #     filename = datetime.now().strftime(
    #         "data/bronze/orders_%Y%m%d%H%M%S.csv"
    #     )

    #     df.to_csv(filename, index=False)
        
    #     update_query = f"""
    #         UPDATE pipeline_state
    #         SET last_watermark = '{batch_end}'
    #         WHERE pipeline_name = 'orders_cdc'
    #     """
        
    #     with engine.begin() as conn:
    #         conn.execute(text(update_query))

    #     print("Pipeline completed.")
    # else:
    #     print("No new changes.")


if __name__ == "__main__":
    bronze_extract()







    