import pandas as pd 
df = pd.read_csv('rating.csv')
df = df.loc[:,['market_value_in_eur','age in days','contract expiry','Rating','position']]
normalized_df=(df-df.min())/(df.max()-df.min())
print(df.min())