from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd 
import numpy as np
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv



api = KaggleApi()
api.authenticate()  
api.dataset_download_file(
    dataset="andrewsundberg/college-basketball-dataset",
    file_name="cbb25.csv",
    path="data/",
    quiet=False
)

cbb_df = pd.read_csv('data/cbb25.csv', na_values=['NA','Not Available','unknown'])
cbb_df_clean = cbb_df.dropna().drop(columns=['WAB','SEED','ADJ_T'], axis=1)


column_map = {
    'RK': 'rank',
    'Team': 'team',
    'CONF':'conference',
    'G':'games',
    'W':'games_won',
    'ADJOE':'offensive_efficiency',
    'ADJDE':'defensive_efficiency',
    'BARTHAG':'power_rating',
    'EFG_O':'field_goal_percentage',
    'EFG_D':'field_goal_percentage_allowed',
    'TOR':'turnover_percentage',
    'TORD':'turnover_percentage_allowed',
    'ORB':'offensive_rebound_rate',
    'DRB':'offensive_rebound_rate_allowed',
    'FTR':'free_throw_rate',
    'FTRD':'free_throw_rate_allowed',
    '2P_O':'two_pt_shooting_percentage',
    '2P_D':'two_pt_shooting_percentage_allowed',
    '3P_O':'three_pt_shooting_percentage',
    '3P_D':'three_pt_shooting_percentage_allowed',
    '3PR':'three_pt_rate',
    '3PRD':'three_pt_rate_allowed',
}

cbb_df_clean = cbb_df_clean.rename(columns = column_map)


load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    cbb_df_clean.to_sql(
        name = "college_basketball",
        con = conn,
        if_exists ="replace",
        index = False
    )
