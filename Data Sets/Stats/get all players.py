import pandas as pd 
from RatingCalculator import calculate_all_ratings
import os

path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Set/Stats'
output_path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code'
def merge_data_sets():
    mid = pd.read_csv(path + 'Midfielders.csv',index_col=None)
    fb = pd.read_csv(path + 'FullBacks.csv',index_col=None)
    fw = pd.read_csv(path + 'Forwards.csv',index_col=None)
    wing = pd.read_csv(path + 'AtMid_Wingers.csv',index_col=None)
    cb = pd.read_csv(path + 'CenterBacks.csv',index_col=None)
    values = pd.read_csv(path + 'Valuations/current_players.csv')
    db = mid._append(fb._append(fw._append(wing._append(cb))))
    db =db.loc[:,['Name','Percentiles']]
    values = values.loc[:,["Name",'contract_expiration_date','market_value_in_eur','date_of_birth']]
    uniques = pd.merge(db,values, on='Name')
    cleaned = pd.merge(uniques,get_from_date(uniques,'2023-02-19'))
    cleaned = cleaned.loc[:,['Name','market_value_in_eur','age in days','contract expiry','Percentiles']]
    cleaned =cleaned.drop_duplicates(subset=['Name'])
    return cleaned

def get_from_date(db,today):
    names = db.loc[:,'Name'].tolist()
    birthdates = db.loc[:,'date_of_birth'].tolist()
    contract_dates = db.loc[:,'contract_expiration_date'].tolist()
    age = []
    age_days = []
    remaing_contract = []
    for e in range(len(birthdates)):
        years = int(today.split('-')[0]) - int(birthdates[e].split('-')[0])
        age += [years]
        months =  int(today.split('-')[1]) - int(birthdates[e].split('-')[1])
        days = int(today.split('-')[2]) - int(birthdates[e].split('-')[2])
        age_days += [years * 365 + months * 30 + days]
        if isinstance(contract_dates[e], str):
            years = int(contract_dates[e].split('-')[0]) - int(today.split('-')[0])
            months =  int(contract_dates[e].split('-')[1]) - int(today.split('-')[1])
            days = int(contract_dates[e].split('-')[2].split(' ')[0]) - int(today.split('-')[2])
            remaing_contract += [years * 365 + months * 30 + days]
        else:
            remaing_contract += [0]
    return pd.DataFrame({'Name':names,'age':age,'age in days':age_days,'contract expiry':remaing_contract})

def merge_ratings_data(path):
    calculate_all_ratings(path)
    mid = pd.read_csv(path + 'Midfielders_M_rating.csv',index_col=None)
    fb = pd.read_csv(path + 'FullBacks_L_rating.csv',index_col=None)
    fw = pd.read_csv(path + 'Forwards_F_rating.csv',index_col=None)
    wing = pd.read_csv(path + 'AtMid_Wingers_W_rating.csv',index_col=None)
    cb = pd.read_csv(path + 'CenterBacks_D_rating.csv',index_col=None)
    for e in ['Midfielders_M_rating.csv','FullBacks_L_rating.csv','Forwards_F_rating.csv','AtMid_Wingers_W_rating.csv','CenterBacks_D_rating.csv']:
        os.remove(path + e)
    mid['position'] = 3
    fb['position'] = 2
    fw['position'] = 5
    wing['position'] = 4
    cb['position'] = 1
    db = mid._append(fb._append(fw._append(wing._append(cb))))
    pd.merge(merge_data_sets(), db, on='Name').loc[:,['Name','position','market_value_in_eur','age in days','contract expiry','Rating']].to_csv(output_path + 'rating.csv')

merge_ratings_data(path)