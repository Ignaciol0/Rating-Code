import pandas as pd 
import numpy as np

path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Sets/Transfers/'

def get_league_data(path):
    bundesliga = pd.read_csv(path +'bundesliga.csv')
    laliga = pd.read_csv(path + 'primera-division.csv')
    ligue1 = pd.read_csv(path + 'ligue-1.csv')
    seriea = pd.read_csv(path + 'serie-a.csv')
    premier = pd.read_csv(path + 'premier-league.csv')

    eredivise = pd.read_csv(path + 'eredivisie.csv')
    liganos = pd.read_csv(path + 'liga-nos.csv')
    championship = pd.read_csv(path + 'championship.csv')

    rest = [eredivise,liganos,championship]
    top_five = [bundesliga, laliga, ligue1, seriea, premier]
    empty_df = pd.DataFrame(columns=['club_name','player_name','age','position','club_involved_name','fee','transfer_movement','transfer_period','fee_cleaned','league_name','year','season'])

    def clean_input(df,list,year = 2016, transfer_type = 'out'):
        for league in list:
            league = league.fillna('NA')
            league = league.loc[league['transfer_movement'] == transfer_type]
            league = league.loc[league['fee'] != '?']
            league = league.loc[league['fee_cleaned'] != 'NA']
            league = league.loc[league['year'] > year]
            df = df._append(league)
        return df

    clean_input(empty_df,top_five).to_csv(path + 'Top_five.csv')
    clean_input(empty_df,rest,2017).to_csv(path + 'Rest_otw.csv')

