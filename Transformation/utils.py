import pandas as pd
import sqlalchemy


class Utility:
    """
    Class for exporting utility methods.
    """
    
    @staticmethod
    def clean_columns_name(df:pd.DataFrame) -> pd.DataFrame:
        """
        Reformat dataframe column names to snake & lowercase.
        """
        return [column.replace(' ','_').lower() for column in df.columns]


    @staticmethod
    def filter_negative(df:pd.DataFrame, column_name:str) -> pd.DataFrame:
        """
        Discard dataframe rows containing negative quantities.
        """
        return df[df[column_name] > 0]


    @staticmethod
    def reformat_date(df:pd.DataFrame) -> pd.DataFrame:
        """
        Change data columns containing dates to datetime type.
        """
        for column in df:
            if 'date' in column:
                df[f"{column}"] = pd.to_datetime(df[f"{column}"])
        return df


    @staticmethod
    def reformat_postcode(df:pd.DataFrame) -> pd.DataFrame:
        """
        Standardize postcode formats to match a given format.
        """
        for column in df:
            if 'postcode' in column:
                df[f"{column}"] = df[f"{column}"].str.replace('%20', '').str.upper().str.replace(' ', '')
        return df


    @staticmethod
    def filter_delivery(df:pd.DataFrame) -> pd.DataFrame:
        """
        Discard dataframes rows that do not follow a chronological order. 
        E.g. delivery date before dispatch date
        """
        df = df.loc[~(df["dispatched_date"] < df["order_date"])]
        df = df.loc[~(df["delivery_date"] < df["dispatched_date"])]
        return df


    @staticmethod
    def connect_to_db(username,password,host,db_name) -> sqlalchemy.engine:
        """
        Create engine to connect to aurora database for given credentials.
        """

        engine = sqlalchemy.create_engine(
        f"""postgresql+psycopg2://{username}:{password}@{host}/{db_name}""")
        return engine


    @staticmethod
    def query_db(query:str, connection) -> pd.DataFrame:
        """
        Query a database via a given engine connection.
        """
        return pd.read_sql_query(query,connection)