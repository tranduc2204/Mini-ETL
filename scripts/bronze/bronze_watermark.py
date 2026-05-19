import pandas as pd
from scripts.bronze.conn import engine
from sqlalchemy import text
from datetime import datetime


def get_watermark (pipeline_name: str):  
    # không nên dùng pd.read_sql để lấy 1 giá trị. bị overskill hơi chậm
    
    #orders_cdc

    query = text("""
        SELECT last_watermark
        FROM pipeline_state
        where pipeline_name = :pipeline_name
    """)
   

    with engine.connect() as conn:
        result = conn.execute(
            query, {"pipeline_name": pipeline_name}
        ).fetchone()
    

    if result is not None:
        return result[0]
    else:
        return None
    
    
def update_watermark(pipeline_name: str, new_watermark: datetime):
    query = text("""
        UPDATE pipeline_state
        SET last_watermark = :new_watermark
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.connect() as conn:
        conn.execute(
            query, {
                "new_watermark": new_watermark,
                "pipeline_name": pipeline_name
            }
        )

   
# query = """
#     SELECT last_watermark
#     FROM pipeline_state
#     where pipeline_name = 'orders_cdc'
# """

# df = pd.read_sql(query, engine)

# return ( df.iloc[0]["last_watermark"])

if __name__ == "__main__":
    pipeline_name = "orders_cdc"

    old_watermark = get_watermark(pipeline_name)
    print ("old_watermark: ", old_watermark)