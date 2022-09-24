from utils import Utility

def scrub_data(df):
    """
    Clean daily ingested dataset.
    """
   
    df.columns = Utility.clean_columns_name(df) 
    df = Utility.filter_negative(df, 'customer_age')
    df = Utility.filter_negative(df, 'order_quantity')
    df = Utility.reformat_date(df)
    df = Utility.reformat_postcode(df)
    df = Utility.filter_delivery(df)

    print('Data scrubbing completed')
    return df


def handler(event,context):
    """
    Update production schema with cleaned data from staging schema.
    """

    engine = Utility.connect_to_db()
    df = Utility.query_db('SELECT * FROM week4_john_staging.staging_ecommerce', engine)
    scrubbed_df = scrub_data(df)
    scrubbed_df.to_sql('production_ecommerce', engine, if_exists='replace', schema='week4_john_production')

    print('Scrubbed data uploaded to production schema')
    return 'Data transformation complete'     
