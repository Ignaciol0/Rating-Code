import pandas as pd 
import os

path = 'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Sets/Stats/'
def scrape_top_5():
    for stat in ['passing']:
        start_year = 2017
        for e in range(10):
            if start_year <2023:
                url = f'https://fbref.com/en/comps/Big5/{str(start_year)}-{str(start_year+1)}/{stat}/players/{str(start_year)}-{str(start_year+1)}-Big-5-European-Leagues-Stats'
                df = pd.read_html(url)
                print(df)
                df[0].to_csv(path+f'{start_year}/{stat}_top_5.csv')
            start_year += 1

def merge_top_attrib(start_year = 2017,curr_year=2023):
    Attributes = {'defense':['Player','Pos','Squad','Rk','Tkl','TklW','Blocks','Int','Clr','Err'],
    'passing':['Player','Pos','Squad','Rk','90s','Cmp','Cmp%','Ast','xAG','KP','1/3','PPA','CrsPA','PrgP'],
    'gca':['Player','Pos','Squad','Rk','SCA','GCA'],
    'shooting':['Player','Pos','Squad','Rk','Sh','SoT%','npxG'],
    'possession':['Player','Pos','Squad','Rk','Touches','Att','Succ%','PrgC','Mis','Dis','PrgR'],
    'stats': ['Player','Pos','Squad','Rk','G-PK'],
    'misc': ['Player','Pos','Squad','Rk','Fls','Fld','PKwon','OG','Recov','Won%']}
    while start_year < curr_year:
        for e in Attributes.keys():
            df = pd.read_csv(path + f'{start_year}\{e}_top_5.csv')
            df =df.set_axis(axis = 1,labels=df.iloc[0].tolist())
            df = df.drop(0)
            df = df.loc[:,Attributes[e]]
            df = df.loc[df['Rk'] != 'Rk']
            if e == 'defense':
                dataframe = df
            else:
                dataframe = pd.merge(dataframe,df, on=['Rk','Player','Squad','Pos'])
        dataframe.to_csv(path + f'{start_year}/total_top_5.csv')
        start_year += 1

def clean_duplicate_column_names():
    start_year = 2017
    for e in range(10):
        df = pd.read_csv(path + f'{start_year}/total_top_5.csv')
        duplicates = [x for x in df.columns.values.tolist() if '.' in x]
        df = df.drop(columns=duplicates)
        df.to_csv(path + f'{start_year}/total_top_5.csv')
        start_year +=1

def get_transfered(year=2017):
    while year < 2023:
        transfers = pd.read_csv('C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Sets/Transfers/Top_five.csv')
        stats = pd.read_csv(f'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Sets/Stats/{year}/total_top_5.csv')
        transfers = transfers.loc[transfers['year'] == (year + 1)]
        comun = list(set(transfers.loc[:,'player_name']) & set(stats.loc[:,'Player']))
        print(len(comun))
        data = pd.merge(stats,transfers,right_on='player_name',left_on='Player')
        data.to_csv(f'Data Sets/Stats/{year}/transfered_players_top_5.csv')
        year += 1
    
get_transfered()