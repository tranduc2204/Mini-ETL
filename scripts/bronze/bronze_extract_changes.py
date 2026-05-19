import pandas as pd
from scripts.bronze.conn import engine 
from sqlalchemy import text


def extract_changes(old_watermark, batch_end):

    query = text  ("""
            SELECT
                l.log_id,
                l.operation_type,
                l.changed_at,
                o.order_id,
                o.user_id,
                o.status,
                o.total_amount,
                o.updated_at

            FROM orders_cdc_log l

            LEFT JOIN orders o
                ON l.order_id = o.order_id

            WHERE l.changed_at > :old_watermark
            AND l.changed_at <= :batch_end

            ORDER BY l.changed_at        
    """)
    df = pd.read_sql(
        query, 
        engine,
        params={
            "old_watermark": old_watermark,
            "batch_end": batch_end
        }   
    )
    return df


    # query = f"""
    #     SELECT *
    #     FROM orders_cdc_log
    #     WHERE changed_at > '{old_watermark}'
    #     AND changed_at <= '{batch_end}'
    #     ORDER BY changed_at
    # """

    # df = pd.read_sql(query, engine)

    # list_id = df['order_id'].tolist()

    # if not list_id:
    #     return pd.DataFrame()

    # if len(list_id) == 1:
    #     ids = f"({list_id[0]})"
    # else:
    #     ids = tuple(list_id)

    # query = f"""
    #     SELECT *
    #     FROM orders
    #     WHERE order_id IN {ids}
    # """
    # df_orders = pd.read_sql(query, engine)
    

    # df_result = df.merge(df_orders, on='order_id', how='left')

   
    # return df_result
 
 
# if __name__ == "__main__":
#     old_watermark = '2026-05-17 21:28:28.431739'
#     batch_end = '2026-05-17 21:28:28.431739'
#     df = extract_changes(old_watermark, batch_end)
#     print(df)