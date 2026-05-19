from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

POSTGRES_USER  = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# engine = create_engine(
#     f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )
#docker
# engine = create_engine(
#         f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}",
#         connect_args={
#             "options": "-csearch_path=OLTP" #   Set the search path to OLTP schema
#         }
#     )


# local
engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}",
    connect_args={
        "options": "-csearch_path=oltp"
    }
)
