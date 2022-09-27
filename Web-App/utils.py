import os

from dotenv import load_dotenv
import pandas as pd
import sqlalchemy

DB_HOST='database-data-eng-instance-1.c9gelistqio1.us-east-1.rds.amazonaws.com'
DB_PORT=5432
DB_USER='john'
DB_PASSWORD='sigmastudent'
DB_NAME='week4_ecommerce'

class Utility:
    """
    Class for exporting utility methods associated with transforming data for plotting.
    """
    
    @staticmethod
    def get_order_time_distribution(df:pd.DataFrame) -> pd.DataFrame:
        """
        Transform df - quantity of toothbrush types ordered against hours of the day
        """
        order_time_distribution  = df
        order_time_distribution['hour'] = order_time_distribution ['order_date'].dt.hour
        order_time_distribution = order_time_distribution.groupby(['toothbrush_type','hour'])['order_quantity'].count()
        return order_time_distribution.reset_index(level = ['toothbrush_type','hour'])
    
    @staticmethod
    def get_delivery_status(df):
        """
        Transform df - find the percentage of delivery status' relative to eachother with respect to the give hour range
        """
        delivery_status_df = df[['delivery_status', 'order_quantity', 'delivery_date']]
        delivery_status_df  = delivery_status_df.dropna()
        delivery_status_df['delivery_date'] = delivery_status_df['delivery_date'].dt.hour
        delivery_status_df = delivery_status_df.groupby(['delivery_date', 'delivery_status'])['order_quantity'].count()
        delivery_status_df = delivery_status_df.reset_index(level = ['delivery_date', 'delivery_status'])
        quantity_date = pd.DataFrame(delivery_status_df.groupby(['delivery_date'])['order_quantity'].sum())
        merge = pd.merge(delivery_status_df, quantity_date, left_on='delivery_date', right_on=quantity_date.index)
        merge.rename(columns={"order_quantity_x": "order_quantity", "order_quantity_y": "month_orders"}, inplace=True)
        return  (merge['order_quantity'].div(merge['month_orders'])*100).round(2)

    @staticmethod
    def get_order_quantity_distribution(df):
        """
        Transform df - Number of toothbrushes bought per order
        """
        order_quantity_distribution = pd.DataFrame(df.groupby(['order_quantity'])['order_number'].count())
        order_quantity_distribution.rename(columns={"order_number": "order_frequency"}, inplace=True)
        return order_quantity_distribution.reset_index(level = ['order_quantity'])

    @staticmethod
    def get_dispatched(df):
        """
        Retrieve entries only containing orders which have a dispatched status
        """
        dispatched = df[(df["dispatch_status"] == "Dispatched")]
        dispatched['difference_hours']= (dispatched["dispatched_date"] - dispatched["order_date"]).dt.total_seconds() / 60 / 60
        dispatched['difference_hours'] = dispatched['difference_hours'].astype('int64')
        dispatched = dispatched.groupby('difference_hours').sum()
        return dispatched.reset_index(level = ['difference_hours'])

    @staticmethod
    def get_regional_distribution(df):
        """
        The number of orders per uk postal region for both toothbrush types
        """
        df['region']  = df.delivery_postcode.apply(lambda x: x[:2])
        regional_orders  = pd.DataFrame(df.groupby(['region'])['order_quantity'].sum())
        regional_orders = regional_orders.reset_index(level = ['region'])
        return regional_orders.sort_values(by=['order_quantity'], ascending=False)

    @staticmethod
    def connect_to_db() -> sqlalchemy.engine:
        """
        Create engine to connect to aurora database for given credentials.
        """

        engine = sqlalchemy.create_engine(
        f"""postgresql+psycopg2://
        {DB_USER}:
        {DB_PASSWORD}@
        {DB_HOST}/
        {DB_NAME}""")
        return engine


    @staticmethod
    def query_db(query:str, connection) -> pd.DataFrame:
        """
        Query a database via a given engine connection.
        """
        return pd.read_sql_query(query,connection)