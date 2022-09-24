# IMPORT  MODULES
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import sqlalchemy

# LOAD DATA
load_dotenv()
engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}")
df = pd.read_sql_query('SELECT * FROM week4_john_production.production_ecommerce', engine)

# TRANSFORM DATA

order_time_distribution  = df
order_time_distribution['hour'] = order_time_distribution ['order_date'].dt.hour
order_time_distribution = order_time_distribution.groupby(['toothbrush_type','hour'])['order_quantity'].count()
order_time_distribution = order_time_distribution.reset_index(level = ['toothbrush_type','hour'])

delivery_status_df = df[['delivery_status', 'order_quantity', 'delivery_date']]
delivery_status_df  = delivery_status_df.dropna()

delivery_status_df['delivery_date'] = delivery_status_df['delivery_date'].dt.hour
delivery_status_df = delivery_status_df.groupby(['delivery_date', 'delivery_status'])['order_quantity'].count()
delivery_status_df = delivery_status_df.reset_index(level = ['delivery_date', 'delivery_status'])
x = pd.DataFrame(delivery_status_df.groupby(['delivery_date'])['order_quantity'].sum())
merge = pd.merge(delivery_status_df, x, left_on='delivery_date', right_on=x.index)
merge.rename(columns={"order_quantity_x": "order_quantity", "order_quantity_y": "month_orders"}, inplace=True)
delivery_status_df['pct_delivery'] = (merge['order_quantity'].div(merge['month_orders'])*100).round(2)

order_quantity_distribution = pd.DataFrame(df.groupby(['order_quantity'])['order_number'].count())
order_quantity_distribution.rename(columns={"order_number": "order_frequency"}, inplace=True)
order_quantity_distribution = order_quantity_distribution.reset_index(level = ['order_quantity'])


DF_only_dispatched = df[(df["dispatch_status"] == "Dispatched")]
DF_only_dispatched['difference_hours']= (DF_only_dispatched["dispatched_date"] - DF_only_dispatched["order_date"]).dt.total_seconds() / 60 / 60
DF_only_dispatched['difference_hours'] = DF_only_dispatched['difference_hours'].astype('int64')
DF_only_dispatched = DF_only_dispatched.groupby('difference_hours').sum()
DF_only_dispatched = DF_only_dispatched.reset_index(level = ['difference_hours'])

order_quantity_distribution = pd.DataFrame(df.groupby(['order_quantity'])['order_number'].count())
order_quantity_distribution.rename(columns={"order_number": "order_frequency"}, inplace=True)
order_quantity_distribution = order_quantity_distribution.reset_index(level = ['order_quantity'])

df['region']  = df.delivery_postcode.apply(lambda x: x[:2])
regional_orders  = pd.DataFrame(df.groupby(['region'])['order_quantity'].sum())

regional_orders = regional_orders.reset_index(level = ['region'])
regional_orders = regional_orders.sort_values(by=['order_quantity'], ascending=False)


# # # PLOT GRAPHS 

age_distribution = px.histogram(df,  x="customer_age", y="order_quantity", color = "toothbrush_type",nbins=120, barmode="group", labels={'order_quantity': 'Order Quantity', 'customer_age':'Customer ages'}, title = ' Age distribution of Order Quantity ')
dispatched_time = px.histogram(DF_only_dispatched,  x="difference_hours", y="order_quantity",nbins=6, title = ' Order to dispatch time taken ')
order_frequency = px.line( x=order_quantity_distribution['order_quantity'], y=order_quantity_distribution["order_frequency"])
regional_plot= px.bar( x=regional_orders['region'], y=regional_orders["order_quantity"])

#  #  FORMAT GRAPHS

age_distribution.update_layout(legend_title_text='Toothbrush Type', yaxis_title = 'Order quantity', xaxis_title = 'Customer ages')
dispatched_time.update_layout( yaxis_title = 'Order quantity', xaxis_title = 'Time Taken to dispatch (hours)')
order_frequency.update_layout( title = 'Number of toothbrushes bought per order', yaxis_title = 'Number of orders', xaxis_title = 'Number of toothbrushes')
regional_plot.update_layout( title = 'Order quantity per postcode region', yaxis_title = 'Number of orders', xaxis_title = 'Postcode region')
