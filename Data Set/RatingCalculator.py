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
def atacking_stats(df):
    atacking_data = pd.read_csv('Data Set/Atacking Data.csv')
    atacking_data = atacking_data.drop(index=atacking_data[atacking_data['Rk'] == 'Rk'].index)
    atacking_data = atacking_data.loc[:,['Player','90s','SoT/90','SoT%']]
    atacking_data.set_index('Player',inplace=True)
    atacking_data.fillna(0,inplace=True)
    atacking_data.loc[:,'SoT%']=pd.to_numeric(atacking_data.loc[:,'SoT%'])
    atacking_data.loc[:,'SoT/90']=pd.to_numeric(atacking_data.loc[:,'SoT/90'])
    atacking_data.loc[:,'90s']=pd.to_numeric(atacking_data.loc[:,'90s'])
    return pd.merge(df,atacking_data,on="Player")
# Normilices the individual stats and add them up multiplied by the weight of the stat
def rating_calculator(data,position):
    data=data.drop_duplicates('Player',keep='first')
    jugadores, gas,media= [],[],[]
    players = data.loc[:,'Player'].values.tolist()
    weights = json.load(open('weights.json'))
    data.set_index('Player',inplace=True)
    std = data.std()
    median = data.median()
    stats = ['Non-Penalty xG','Shots Total','xAG','npxG + xAG','Shot-Creating Actions','Passes Attempted','Pass Completion %','Progressive Passes','Progressive Carries','Successful Take-Ons','Touches (Att Pen)','Progressive Passes Rec','Tackles','Interceptions','Blocks','Clearances','Aerials won','SoT/90','SoT%','90s']

    
    for player in players:
        rating = 0
        for stat in stats:
            non_pk = data.loc[player,'Non-Penalty Goals']
            matches= data.loc[player,'90s']
            assits = data.loc[player,'Assists']
            rating += (data.loc[player,stat]- median[stat])/std[stat] * 0.05 * weights[position[0]][stats.index(stat)]
        ga= matches * assits + matches * non_pk
        jugadores += [player]
        media += [rating]
        gas += [ga]
    return pd.DataFrame({'player':jugadores,'rating':media,'goals+assists':gas})
# Normilices the g/a and the rating obtained in the previous method, then it adds them up
def second_normalization(data,position, path):
    rating = rating_calculator(data,position)
    players=rating.loc[:,'player'].tolist()
    rating.set_index('player',inplace=True)
    median = rating.median()
    std = rating.std()
    ratings ={}
    if position[0] == 'F':
        goal_weight = 1
    elif position[0] == 'W' or position == 'M':
        goal_weight = 0.7
    else:
        goal_weight = 0.5
    for player in players:
        rating_deviation = (rating.loc[player,'rating']- median['rating'])/std['rating']
        ga_deviation = (rating.loc[player,'goals+assists']- median['goals+assists'])/std['goals+assists']
        ratings[player] = rating_deviation + goal_weight * ga_deviation + 3.25 # The 3 is so the lowest number is >0
    pd.DataFrame({'Name':ratings.keys(),'Rating':ratings.values()}).sort_values(by='Rating',ascending=False).to_csv(path +f'{position[1]}_{position[0]}_rating.csv')

def calculate_all_ratings(path):
    positions = ['Forwards', 'AtMid_Wingers','Midfielders','CenterBacks','FullBacks']
    for analyzed in positions:
        second_normalization(atacking_stats(take_individual_stat(analyzed)),position_selector(analyzed),path)

