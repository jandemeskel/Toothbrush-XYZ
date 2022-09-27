import plotly.express as px

from utils import Utility


engine = Utility.connect_to_db()
df = Utility.query_db('SELECT * FROM week4_john_production.production_ecommerce', engine)

order_time_distribution = Utility.get_order_time_distribution(df)
delivery_status_df = Utility.get_delivery_status(df)
order_quantity_distribution = Utility.get_order_quantity_distribution(df)
dispatched = Utility.get_dispatched(df)
regional_distribution = Utility.get_regional_distribution(df)


age_distribution = px.histogram(df,  x="customer_age", y="order_quantity", color = "toothbrush_type",nbins=120, barmode="group", labels={'order_quantity': 'Order Quantity', 'customer_age':'Customer ages'}, title = ' Age distribution of Order Quantity ')
dispatched_time = px.histogram(dispatched,  x="difference_hours", y="order_quantity",nbins=6, title = ' Order to dispatch time taken ')
order_frequency = px.line( x=order_quantity_distribution['order_quantity'], y=order_quantity_distribution["order_frequency"])
regional_plot= px.bar( x=regional_distribution['region'], y=regional_distribution["order_quantity"])


age_distribution.update_layout(legend_title_text='Toothbrush Type', yaxis_title = 'Order quantity', xaxis_title = 'Customer ages')
dispatched_time.update_layout( yaxis_title = 'Order quantity', xaxis_title = 'Time Taken to dispatch (hours)')
order_frequency.update_layout( title = 'Number of toothbrushes bought per order', yaxis_title = 'Number of orders', xaxis_title = 'Number of toothbrushes')
regional_plot.update_layout( title = 'Order quantity per postcode region', yaxis_title = 'Number of orders', xaxis_title = 'Postcode region')
