import os
import pandas as pd
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
from sqlalchemy import create_engine




def download_data(dataset: str, file_name: str, path: str = "data/"):
    """Downloads dataset file from Kaggle and saves it locally."""
    api = KaggleApi()
    api.authenticate()
    os.makedirs(path, exist_ok=True)  
    api.dataset_download_file(dataset=dataset, file_name=file_name, path=path, quiet=False)

def load_data(file_path: str) -> pd.DataFrame:
    """Reads the dataset into a Pandas DataFrame."""
    df = pd.read_csv(file_path, na_values=['NA', 'Not Available', 'unknown'])
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the dataset by removing null values and renaming columns."""
    df_clean = df.dropna().drop(columns=['WAB', 'SEED', 'ADJ_T'], errors='ignore')
    column_map = {
        'RK': 'rank', 'Team': 'team', 'CONF': 'conference', 'G': 'games',
        'W': 'games_won', 'ADJOE': 'offensive_efficiency', 'ADJDE': 'defensive_efficiency',
        'BARTHAG': 'power_rating', 'EFG_O': 'field_goal_percentage', 'EFG_D': 'field_goal_percentage_allowed',
        'TOR': 'turnover_percentage', 'TORD': 'turnover_percentage_allowed', 'ORB': 'offensive_rebound_rate',
        'DRB': 'offensive_rebound_rate_allowed', 'FTR': 'free_throw_rate', 'FTRD': 'free_throw_rate_allowed',
        '2P_O': 'two_pt_shooting_percentage', '2P_D': 'two_pt_shooting_percentage_allowed',
        '3P_O': 'three_pt_shooting_percentage', '3P_D': 'three_pt_shooting_percentage_allowed',
        '3PR': 'three_pt_rate', '3PRD': 'three_pt_rate_allowed'
    }
    df_clean = df_clean.rename(columns=column_map)
    return df_clean

def get_database_connection():
    """Establishes a connection to the PostgreSQL database using environment variables."""
    load_dotenv()
    db_url = f"postgresql+psycopg2://{os.getenv('user')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('dbname')}?sslmode=require"
    engine = create_engine(db_url)
    return engine

def load_to_database(df: pd.DataFrame, table_name: str, engine):
    """Uploads the cleaned DataFrame to the PostgreSQL database."""
    with engine.connect() as conn:
        df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)

def main():
    """Main function to execute the pipeline."""
    dataset = "andrewsundberg/college-basketball-dataset"
    file_name = "cbb25.csv"
    file_path = f"data/{file_name}"
    
    download_data(dataset, file_name)
    df = load_data(file_path)
    df_clean = clean_data(df)
    
    engine = get_database_connection()
    load_to_database(df_clean, "college_basketball", engine)

    print("Data pipeline executed successfully.")

if __name__ == "__main__":
    main()
# This script downloads a dataset from Kaggle, cleans it, and loads it into a PostgreSQL database.

















