import pandas as pd
from db import engine

def get_watermark ():

    query = """
        SELECT last_watermark
        FROM pipeline_state
        where pipeline_name = 'orders_cdc'
    """

    df = pd.read_sql(query, engine)
   
    return ( df.iloc[0]["last_watermark"])

if __name__ == '__main__':
    get_watermark()
