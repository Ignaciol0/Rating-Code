import pandas as pd
import json

'''Put in analyced the name of the db you want to use or
    F for forwards
    W for wingers and atacking mids
    M for midfielders
    D for central defenders
    L for fullbacks
    G for goalkeepers'''
analyzed = 'FullBacks'

# Allows for cleared user input
def position_selector(analyzed):
    dict = {'Forwards': 'F', 'AtMid_Wingers':'W','Midfielders':'M','CenterBacks':'D','FullBacks':'L','GoalKeepers':'G'}
    if len(analyzed) == 1:
        analyzed = dict.keys()[dict.values.index(analyzed)]
    return [dict[analyzed],analyzed]

# Takes the general data from the dataset
def take_individual_stat(analyzed):
    analyzed = position_selector(analyzed)[1]
    df =pd.read_csv(f"Data Set/{analyzed}.csv")
    df =df.drop("Number", axis=1)   
    names = df.loc[:,"Name"].values.tolist()
    df.set_index("Name", inplace=True)
    df=df.drop("Percentiles", axis=1)
    Non_Penalty_Goals=[]
    Non_Penalty_xG=[]
    Shots_Total=[]
    Assists=[]
    xAG=[]
    npxG_xAG=[]
    Shot_Creating_Actions=[]
    Passes_Attempted=[]
    Pass_Completion=[]
    Progressive_Passes=[]
    Progressive_Carries=[]
    Successful_Take_Ons=[]
    Touches_Att_Pen=[]
    Progressive_Passes_Rec=[]
    Tackles=[]
    Interceptions=[]
    Blocks=[]
    Clearances=[]
    Aerials_won=[]
    df=df.values.tolist()
    for e in df:
        data= json.loads(e[0])
        Non_Penalty_Goals+=[data[0]]
        Non_Penalty_xG+=[data[1]]
        Shots_Total+=[data[2]]
        Assists+=[data[3]]
        xAG+=[data[4]]
        npxG_xAG+=[data[5]]
        Shot_Creating_Actions+=[data[6]]
        Passes_Attempted+=[data[7]]
        Pass_Completion+=[data[8]]
        Progressive_Passes+=[data[9]]
        Progressive_Carries+=[data[10]]
        Successful_Take_Ons+=[data[11]]
        Touches_Att_Pen+=[data[12]]
        Progressive_Passes_Rec+=[data[13]]
        Tackles+=[data[14]]
        Interceptions+=[data[15]]
        Blocks+=[data[16]]
        Clearances+=[data[17]]
        Aerials_won+=[data[18]]
    data = pd.DataFrame({"Player":names,'Non-Penalty Goals':Non_Penalty_Goals,'Aerials won':Aerials_won,'Non-Penalty xG':Non_Penalty_xG,
    'Shots Total':Shots_Total,
    'Assists':Assists,
    'xAG':xAG,
    'npxG + xAG':npxG_xAG,
    'Shot-Creating Actions':Shot_Creating_Actions,
    'Passes Attempted':Passes_Attempted,
    'Pass Completion %':Pass_Completion,
    'Progressive Passes':Progressive_Passes,
    'Progressive Carries':Progressive_Carries,
    'Successful Take-Ons':Successful_Take_Ons,
    'Touches (Att Pen)':Touches_Att_Pen,
    'Progressive Passes Rec':Progressive_Passes_Rec,
    'Tackles':Tackles,
    'Interceptions':Interceptions,
    'Blocks':Blocks,
    'Clearances':Clearances})
    return data
# Gets the specified stats for atackers and puts them in the db
'''def atacking_stats(df):
    atacking_data = pd.read_csv('Data Set/Atacking Data.csv')
    atacking_data = atacking_data.drop(index=atacking_data[atacking_data['Rk'] == 'Rk'].index)
    atacking_data = atacking_data.loc[:,['Player','90s','SoT/90','SoT%']]
    atacking_data.set_index('Player',inplace=True)
    atacking_data.fillna(0,inplace=True)
    atacking_data.loc[:,'SoT%']=pd.to_numeric(atacking_data.loc[:,'SoT%'])
    atacking_data.loc[:,'SoT/90']=pd.to_numeric(atacking_data.loc[:,'SoT/90'])
    atacking_data.loc[:,'90s']=pd.to_numeric(atacking_data.loc[:,'90s'])
    return pd.merge(df,atacking_data,on="Player")'''
# Normilices the individual stats and add them up multiplied by the weight of the stat
def rating_calculator(data,position,total_data):
    data=data.drop_duplicates('Player',keep='first')
    jugadores, gas,media= [],[],[]
    players = data.loc[:,'Player'].values.tolist()
    weights = json.load(open('weights.json'))
    data.set_index('Player',inplace=True)
    data['npxG + xAG'] = data['xAG'] + data['npxG']
    data['TklW%'] = round((data['TklW']/data['Tkl']),2)
    total_data['npxG + xAG'] = total_data['xAG'] + total_data['npxG']
    total_data['TklW%'] = round((total_data['TklW']/total_data['Tkl']),2)
    stats = ['npxG','xAG','npxG + xAG','SCA','Att','Cmp%','PrgP','PrgC','Succ%','PPA','PrgR','Tkl','Int','Blocks','Clr','Won%','Sh','SoT%','90s','KP','1/3','CrsPA','GCA','TklW%','Err','Touches','Dis','Mis','Recov','PKwon','Fld','Fls']
    total_data = total_data.loc[:,stats]
    std = total_data.std()
    median = total_data.median()
    for player in players:
        rating = 0
        for stat in stats:
            non_pk = data.loc[player,'G-PK']
            matches= data.loc[player,'90s']
            assits = data.loc[player,'Ast']
            own_goals = data.loc[player,'OG']
            rating += (data.loc[player,stat]- median[stat])/std[stat] * 0.05 * weights[position][stats.index(stat)]
        ga= assits + non_pk - own_goals
        jugadores += [player]
        media += [rating]
        gas += [ga]
    return pd.DataFrame({'player':jugadores,'rating':media,'goals+assists':gas})
# Normilices the g/a and the rating obtained in the previous method, then it adds them up
def final_rating(year=2017):
    while year < 2023:
        for e in ['F','M','D']:
            total_data = pd.read_csv(f'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Sets/Stats/{year}/total_top_5.csv')
            data = pd.read_csv(f'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Sets/Stats/{year}/transfered_players_top_5.csv')
            if e == 'F':
                data = data.loc[(data['Pos'] == 'FW') | (data['Pos'] == 'FW,MF') | (data['Pos'] == 'FW,DF')]
                total_data = total_data.loc[(total_data['Pos'] == 'FW') | (total_data['Pos'] == 'FW,MF') | (total_data['Pos'] == 'FW,DF')]
            elif e == 'M':
                data = data.loc[(data['Pos'] == 'MF') |  (data['Pos'] == 'MF,DF') | (data['Pos'] == 'MF,FW')]
                total_data = total_data.loc[(total_data['Pos'] == 'MF') |  (total_data['Pos'] == 'MF,DF') | (total_data['Pos'] == 'MF,FW')]
            elif e == 'D':
                data = data.loc[(data['Pos'] == 'DF') |  (data['Pos'] == 'DF,MF') | (data['Pos'] == 'DF,FW')]
                total_data = total_data.loc[(total_data['Pos'] == 'DF') |  (total_data['Pos'] == 'DF,MF') | (total_data['Pos'] == 'DF,FW')]
            print(data)
            rating = rating_calculator(data,e,total_data)
            players=rating.loc[:,'player'].tolist()
            rating.set_index('player',inplace=True)
            median = rating.median()
            std = rating.std()
            ratings ={}
            non_ga = []
            ga = []
            for player in players:
                rating_deviation = (rating.loc[player,'rating']- median['rating'])/std['rating']
                ga_deviation = (rating.loc[player,'goals+assists']- median['goals+assists'])/std['goals+assists']
                non_ga += [rating_deviation]
                ga += [ga_formula(ga_deviation,e,std,median)]
                ratings[player] = rating_deviation + ga_formula(ga_deviation,e,std,median)
            pd.DataFrame({'Name':ratings.keys(),'Rating':ratings.values()}).sort_values(by='Rating',ascending=False).to_csv(f'C:/Users/ignac/Documents/Documentos/Football/Futty Data/Rating Code/Data Sets/Stats/Ratings/{year}_{e}_rating.csv')
        year += 1

def ga_formula(ga,e,std,median):
    if e == 'F':
        gas = ga * std['goals+assists'] + median['goals+assists']
        if (gas < 25):
            return gas/5
        else:
            return (1.065**gas+0.1723) # Geogebra function
    if e == 'M':
        return ga/2 #El Rating fluctua entre (4,-2) y de goles 20 serán 8 en la normalización y  
    else:
        return ga/3 #En Rating fluctuan entre (3,-2) y de goles 10 serán 5 en la normalización y 1.66 
    

final_rating()
