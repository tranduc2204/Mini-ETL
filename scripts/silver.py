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

    print (files_list)
    
   
    with engine.connect() as conn:
    
        for file in files_list:
          
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
    


    df_list = [pd.read_csv(file) for file in files_list]


    df = pd.concat(df_list, ignore_index=True)
    



if __name__ == "__main__":              
    list_file_exists()