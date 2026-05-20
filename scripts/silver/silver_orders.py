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

    f_latest["rank"] = f_latest.groupby("order_id")["changed_at"]\
        .rank(method="dense", ascending=False)  

    f_latest = f_latest[f_latest["rank"] == 1]
    
   
    #nếu không có giá trị của cột update at thì lấy giá trị của cột changed_at
    f_latest["date"] = f_latest["updated_at"].fillna(f_latest["changed_at"])

    # check senario in the dataframe have 2 record with the same ID. we will keep  the record with the latest date
    # df_result = df_result.drop_duplicates(subset=["order_id"], keep="last")

    # check total amount must be greater than 0
    f_latest = f_latest[f_latest["total_amount"] > 0]
    # f_latest = f_latest.dropna()

    datetime_cols = ["updated_at", "changed_at", "date"]

    for col in datetime_cols:
        # df_result[col] = pd.to_datetime(df_result[col]).dt.strftime("%d-%m-%Y %H:%M:%S")
        f_latest[col] = pd.to_datetime(
            f_latest[col],
            format="mixed"
        ).dt.strftime("%d-%m-%Y")

    f_latest = f_latest[["order_id", "user_id", "status", "total_amount", "date"]]

    
    f_latest.to_csv(
        "./data/gold/gold_orders.csv",
        index=False
    )
    print (f_latest)

if __name__ == "__main__":  
    silver_orders()

