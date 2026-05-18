from datetime import datetime

import pandas  as pd 
import glob
import os
# from scripts.db import engine

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

POSTGRES_USER  = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}",
    connect_args={
            "options": "-csearch_path=OLTP" #   Set the search path to OLTP schema
    }
)

def list_file_exists():
    # list all file in the bronze folder
    files_list = glob.glob("data/bronze/*.csv")


    # Check file in bronze folder has been processed
    query = """
        SELECT file_name
        FROM processed_files
    """
    df_processed = pd.read_sql(query, engine)
    processed_files = df_processed['file_name'].tolist()

    new_file  = [file for file in files_list 
                    if file not in processed_files]
    
    
    if not new_file:
        print ("No new file to process")
        return 
    else:   
    
       


        df_list = [pd.read_csv(file) for file in new_file]


        df = pd.concat(df_list, ignore_index=True)
        
        df_silver_old = pd.read_csv("./data/silver/orders_silver.csv")
        df_silver_new = pd.concat([df_silver_old, df], ignore_index=True)
        df_silver_new.to_csv("./data/silver/orders_silver.csv", index=False)
        print ("processed done")
        print (df_silver_new)

        with engine.connect() as conn:
        
            for file in new_file:
            
                conn.execute(
                    text("""
                        INSERT INTO processed_files(
                            file_name,
                            processed_at
                        )VALUES(
                            :file_name,
                            :processed_at
                        )
                        ON CONFLICT (file_name) DO NOTHING

                    """),
                    {
                        "file_name": file,
                        "processed_at": datetime.now()
                    }
                ) 
                conn.commit()


if __name__ == "__main__":              
    list_file_exists()