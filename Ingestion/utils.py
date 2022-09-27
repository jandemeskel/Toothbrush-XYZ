import pandas as pd
import s3fs
import sqlalchemy

from datetime import date, timedelta

class Utility:
    """
    Class for exporting utility methods.
    """
    
    @staticmethod
    def retrieve_bucket(bucket_name:str) -> list:
        """
        Retrieve a list of files within a given s3 bucket
        """
        return s3fs.S3FileSystem().find(bucket_name)
    
    @staticmethod
    def retrieve_data(bucket:list) -> pd.DataFrame:
        """
        Search through all files in s3 bucket to find latest csv
        """
        yesterday = date.today() - timedelta(days = 1)
        csv_filepath = yesterday.strftime("%y/%m/%d")
        daily_ingestion = [file for file in bucket if csv_filepath in file][0]

        return  pd.read_csv(f's3://{daily_ingestion}') 

    @staticmethod
    def connect_to_db(username,password,host,db_name) -> sqlalchemy.engine:
        """
        Create engine to connect to aurora database for given credentials.
        """

        engine = sqlalchemy.create_engine(
        f"""postgresql+psycopg2://
        {username}:
        {password}@
        {host}/
        {db_name}""")
        return engine