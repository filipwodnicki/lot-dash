import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:////Users/Filip/code/python/lot-dash/app.db')

df = pd.read_csv('/Users/Filip/code/python/lot-dash/db/test.csv')
df.to_sql('user',con=engine, if_exists='append',index=False)
