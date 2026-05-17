import pandas as pd 
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime
from watermark import  get_watermark
from db import engine
from extract import extract_changes


old_watermark = get_watermark()

batch_end_query = """
    SELECT MAX(changed_at) AS batch_end
    FROM orders_cdc_log
"""

batch_end = pd.read_sql(
    batch_end_query,
    engine
).iloc[0]["batch_end"]

print (batch_end)
df = extract_changes(old_watermark, batch_end)

print (df)

if not df.empty:

    filename = datetime.now().strftime(
        "data/bronze/orders_%Y%m%d%H%M%S.csv"
    )

    df.to_csv(filename, index=False)

    # STEP 5
    update_query = f"""
    UPDATE pipeline_state
    SET last_watermark = '{batch_end}'
    WHERE pipeline_name = 'orders_cdc'
    """

    with engine.begin() as conn:
        conn.execute(update_query)

    print("Pipeline completed.")
else:
    print("No new changes.")



# query = "SELECT * FROM orders;"

# # Read data into pandas DataFrame
# df = pd.read_sql(query, engine)

# # Show result
# print(df)


# current_time = datetime.now().strftime("%Y%m%d%H%M%S")
# print (current_time)

# df.to_csv(f"./data/orders_{current_time}.csv", index=False)





