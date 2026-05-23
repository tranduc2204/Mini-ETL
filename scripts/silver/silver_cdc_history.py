from datetime import datetime

import pandas  as pd 
import glob
import os
from scripts.bronze.conn import engine

from dotenv import load_dotenv
import os
from sqlalchemy import text

SILVE_PATH = os.getenv("SILVER_PATH")

def process_bronze_to_silver():
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
        # silver_path = "./data/silver/orders_silver.csv"
        
        df_list = [pd.read_csv(file) for file in new_file]

     
        

        bronze_df = pd.concat(df_list, ignore_index=True)

  
        if os.path.exists(SILVE_PATH):
            df_silver_old = pd.read_csv(SILVE_PATH)
        else:
            df_silver_old = pd.DataFrame()
        
      
        # df_silver_new = (
        #     pd.concat([df_silver_old, bronze_df], ignore_index=True) #
        #     .sort_values("changed_at")
          
        # )
        df_silver_new = (
            pd.concat([df_silver_old, bronze_df])
            .sort_values("changed_at")
            .drop_duplicates(subset=["order_id"], keep="last")
        )

        df_silver_new.to_csv(SILVE_PATH, index=False)
       
       
        print(f"Found {len(new_file)} new files")
        print(f"Silver rows: {len(df_silver_new)}")

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
        print ("processed done")

if __name__ == "__main__":              
    process_bronze_to_silver()