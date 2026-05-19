import pandas as pd 
from datetime import datetime
import os





def silver_orders():

    path = './data/silver/orders_silver.csv'

    if os.path.exists(path):
        df_silver = pd.read_csv(path)
        
    else:
        
        print ("No silver data found.")
        columns = [
                "order_id",
                "user_id",
                "status",
                "total_amount",
                "updated_at",
                "log_id",
                "changed_at",
                "operation_type"
        ]
        df_silver = pd.DataFrame(columns=columns)
        

    
    df_result = df_silver[["order_id", "user_id", "status", "total_amount", "updated_at", "log_id", "changed_at","operation_type"]]


    # business rule INSERT | UPDATE | DELETE

    df_silver = df_silver.sort_values(
        by=["changed_at", "log_id"]
    )

    df_latest = (
        df_silver
        .sort_values(["changed_at", "log_id"])
        .drop_duplicates(subset=["order_id","operation_type"], keep="last")
    )

    f_latest = df_latest[
        df_latest["operation_type"] != "DELETE"
    ]

    print (f_latest)
    return
    print (f_latest)
    #nếu không có giá trị của cột update at thì lấy giá trị của cột changed_at
    df_result["date"] = df_result["updated_at"].fillna(df_result["changed_at"])

    # check senario in the dataframe have 2 record with the same ID. we will keep  the record with the latest date
    # df_result = df_result.drop_duplicates(subset=["order_id"], keep="last")

    # check total amount must be greater than 0
    df_result = df_result[df_result["total_amount"] > 0]
    # df_result = df_result.dropna()

    datetime_cols = ["updated_at", "changed_at", "date"]

    for col in datetime_cols:
        # df_result[col] = pd.to_datetime(df_result[col]).dt.strftime("%d-%m-%Y %H:%M:%S")
        df_result[col] = pd.to_datetime(
            df_result[col],
            format="mixed"
        ).dt.strftime("%d-%m-%Y")

    print (df_result)

if __name__ == "__main__":  
    silver_orders()

