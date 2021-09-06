import pandas as pd

#-----------------------Variables/ Lists / Dictionaries Used------------------#
months=['Jan',
'Feb',
'Mar',
'Apr',
'May',
'June',
'July',
'Aug',
'Sept',
'Oct',
'Nov',
'Dec']

p_vals={
 
    'California':5,   #Latitude coordinates 0-5 for 35-60 degrees
    'Iowa':4,
    'Nebraska':4,
    'Illinois':4,
    'Texas':5,
}

days={
    'Jan':31,
'Feb':28,
'Mar':31,
'Apr':30,
'May':31,
'June':30,
'July':31,
'Aug':31,
'Sept':30,
'Oct':31,
'Nov':30,
'Dec':31
}

stages=['Initial stage','Crop dev. stage','Mid-season stage','Late season stage']

#----------------------------------------------------------------------------------------#


def get_temp(state):
    df = pd.read_excel (rf'C:\Users\anjis\Desktop\hackathon\project\irrigation\main_app\static\tables\{state}\temp.xlsx')

    return {'Jan':df['Average'][0],
            'Feb':df['Average'][1],
            'Mar':df['Average'][2],
            'Apr':df['Average'][3],
            'May':df['Average'][4],
            'June':df['Average'][5],
            'July':df['Average'][6],
            'Aug':df['Average'][7],
            'Sept':df['Average'][8],
            'Oct':df['Average'][9],
            'Nov':df['Average'][10],
            'Dec':df['Average'][11]}

#----------------------------------------------------------------------------------------#
    

def get_p(state):
    global p_vals,months
    df = pd.read_excel (rf'C:\Users\anjis\Desktop\hackathon\project\irrigation\main_app\static\tables\p(North).xlsx')
    p={}
    for i in months:
        p[i]=(df[i][p_vals[state]])
    return p
#----------------------------------------------------------------------------------------#


def get_eto(pVals,tempDict):
    eto={}
    for i in months:
        eto[i]= pVals[i] * ( 0.46*tempDict[i] +8 )


    return eto

#----------------------------------------------------------------------------------------#



def get_et(eto,month,kc,stage_dur):       #When the crop is transplanted, the length of the initial stage should be reduced ->: around half?
    global days                                                          # When a crop is harvested "green" the late seson stage is shorter
    month_list=[]  
    index=months.index(month)
    et={'Jan':0,
        'Feb':0,
        'Mar':0,
        'Apr':0,
        'May':0,
        'June':0,
        'July':0,
        'Aug':0,
        'Sept':0,
        'Oct':0,
        'Nov':0,
        'Dec':0}                                                           #et= eto x kc
    for i in range(len(months)):
        month_list.append(months[index])
        if index==len(months)-1:
            index=0
        else:
            index+=1
    temp_days=days.copy()
    stage_iter=iter(stages)
    months_iter=iter(month_list)
    stage_item=next(stage_iter)
    month_item=next(months_iter)
    while True:
        total_days=days[month_item]
        if temp_days[month_item]>stage_dur[stage_item]:
            
            et[month_item]+=eto[month_item]*kc[stage_item]*(stage_dur[stage_item]/total_days)
            temp_days[month_item]-=stage_dur[stage_item]
            try:
                stage_item=next(stage_iter)
            except Exception as e:
                print(e)
                break

        elif temp_days[month_item]==stage_dur[stage_item]:

            et[month_item]+=eto[month_item]*kc[stage_item]*(temp_days[month_item]/total_days)
            month_item=next(months_iter)
            try:
                stage_item=next(stage_iter)
            except Exception as e:
                print(e)
                break


        else:
            stage_dur[stage_item]-=temp_days[month_item]
            et[month_item]+=eto[month_item] * (temp_days[month_item]/total_days)*kc[stage_item]
            month_item=next(months_iter)


    return et
    
#----------------------------------------------------------------------------------------#
def get_kc(crop):
    global stages
    df = pd.read_excel (rf'C:\Users\anjis\Desktop\hackathon\project\irrigation\main_app\static\tables\Kc.xlsx')
    index=(list(df['Crop']).index(crop))
    kc={}
    for i in stages:
        kc[i]=df[i][index]

    return kc




#----------------------------------------------------------------------------------------#
def get_durs(crop,crop_Sown_or_Transplanted,green_or_Fresh,expected_harvest_days):
    df = pd.read_excel (rf'C:\Users\anjis\Desktop\hackathon\project\irrigation\main_app\static\tables\stages.xlsx')
    stages=['Initial stage','Crop dev. stage','Mid-season stage','Late season stage','Total']
    ans={}
    index=list(df['Crop']).index(crop)
    for i in stages:
        ans[i]=df[i][index+1]
    diff= ans['Total']-int(expected_harvest_days)

    if diff<0:
        diff=0

    if crop_Sown_or_Transplanted=='Transplanted' and green_or_Fresh== 'Green':
        ans['Initial stage']-= diff/2
        ans['Late season stage']-=diff/2
        if crop_Sown_or_Transplanted=='Transplanted':
            ans['Initial stage']-= diff
        if green_or_Fresh== 'Green':
            ans['Late season stage']-=diff


    return ans


#----------------------------------------------------------------------------------------#
def get_pe(state):
    df = pd.read_excel (rf'C:\Users\anjis\Desktop\hackathon\project\irrigation\main_app\static\tables\{state}\rain.xlsx')
    ans={}



    for i in months:
        if df[i][0] > 75:
            ans[i]= (0.8 * df[i][0]) - 25
            if ans[i]<0: ans[i]=0
        elif df[i][0] < 75:
            ans[i]= (0.6 * df[i][0]) - 10
            if ans[i]<0: ans[i]=0

  

    return ans
#----------------------------------------------------------------------------------------#


def get_in(et,pe):
    mon={}
    dail={}

    for key in et.keys():
        if et[key]!=0:
            mon[key]=round((et[key]* days[key] - pe[key]),3)
            dail[key]=round((et[key] - pe[key] /30),3)
        else:
            mon[key]=0
            dail[key]=0
    return [mon,dail]

#----------------------------------------------------------------------------------------#


def get_data(queryData):
    state=queryData['state']
    crop=queryData['crop']
    month=queryData['planted_Month']
    green_or_Fresh=queryData['green_or_Fresh']
    crop_Sown_or_Transplanted=queryData['crop_Sown_or_Transplanted']
    expected_harvest_days=queryData['expected_harvest_days']

    tempDict= get_temp(state)
    pVals=get_p(state)
    eto=get_eto(pVals,tempDict)
    stage_dur=get_durs(crop,crop_Sown_or_Transplanted,green_or_Fresh,expected_harvest_days)
    kc=get_kc(crop)
    et=get_et(eto,month,kc,stage_dur)   # ET per day
    pe=get_pe(state)    
    final_results=get_in(et,pe)    #month

    return final_results
 



    
    
    
    
