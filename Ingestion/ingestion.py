import os

from dotenv import load_dotenv

from utils import Utility


def data_dump():
    """
    Ingest latest data from s3 bucket and load into pandas dataframe 
    """
    ecommerce_bucket = Utility.retrieve_bucket('sigma-week4-ecommerce-data')
    print('Bucket contents retrieved')

    return Utility.retrieve_data(ecommerce_bucket)


def handler(event, context):
    """
    Update aurora database schema with latest data dump
    """
    

    load_dotenv()

    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    ecommerce_df = data_dump()
    print('Data dumped')

    engine = Utility.connect_to_db(username,  password, host, db_name)
    ecommerce_df.to_sql('staging_ecommerce', engine, if_exists='replace', schema='week4_john_staging')
    print('Staging schema data updated')

    return 'Daily ingestion completed'



