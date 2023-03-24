import requests
import pandas as pd
from datetime import date
from datetime import timedelta
import time

adccounts = ['AD_ACCOUNTS']
access_token = 'ACCESS_KEY'

#To get all the campaigns from the ad accounts
def getAllCampaigns(params, adaccount):
    access = access_token
    my_headers = {'Authorization': 'Bearer ' + access}
    param = params
    response = requests.get(f'https://graph.facebook.com/v15.0/{adaccount}/insights', headers=my_headers, params=param)
    result = response.json()
    return result

#To extract other metrics from the campaigns
def deepDive(adccounts, numDays):

    today = date.today()
    backdate = today - timedelta(days=numDays)
    datelist = []
    paramslist = {'level': 'campaign', 'fields': 'account_name,campaign_name,campaign_id,spend,cpc,cpp,cpm,account_currency'}
    for i in range(numDays):
        todaystr = str(backdate)
        year = todaystr[:4]
        month = todaystr[6:7]
        day = todaystr[-2:]
        # currday = int(day) - days
        rangestr = "{'since':'"+year+"-"+month+"-"+str(day)+"','until':'"+year+"-"+month+"-"+str(day)+"'}"
        datelist.append({'time_range':rangestr})
        backdate = backdate + timedelta(days=1)

    finalDf = pd.DataFrame(columns=['account_name','campaign_name','campaign_id','spend','account_currency','cpc','cpp','cpm', "date", 'category'])
    dfIndex = 0

    print(finalDf)

    for adaccount in adccounts:
        for i in datelist:
            paramslist.update(i)
            for campaign in getAllCampaigns(paramslist, adaccount)['data']:
                try:
                    finalDf.loc[dfIndex, "account_name"] = campaign['account_name']
                    finalDf.loc[dfIndex, "campaign_name"] = campaign['campaign_name']
                    finalDf.loc[dfIndex, "campaign_id"] = campaign['campaign_id']
                    finalDf.loc[dfIndex, "spend"] = campaign['spend']
                    finalDf.loc[dfIndex, "account_currency"] = campaign['account_currency']
                    finalDf.loc[dfIndex, "cpc"] = campaign['cpc']
                    finalDf.loc[dfIndex, "cpp"] = campaign['cpp']
                    finalDf.loc[dfIndex, "cpm"] = campaign['cpm']
                    finalDf.loc[dfIndex, "date"] = campaign['date_start']
                    finalDf.loc[dfIndex, "category"] = campaign['campaign_name'].split('|')[3].strip(' ')
                except:
                    print("=====================================================================================")
                    print(campaign)
                    print("=====================================================================================")
                    finalDf.loc[dfIndex, "account_name"] = 'N/A'
                    finalDf.loc[dfIndex, "campaign_name"] = 'N/A'
                    finalDf.loc[dfIndex, "campaign_id"] = 'N/A'
                    finalDf.loc[dfIndex, "spend"] = 'N/A'
                    finalDf.loc[dfIndex, "account_currency"] = 'N/A'
                    finalDf.loc[dfIndex, "cpc"] = 'N/A'
                    finalDf.loc[dfIndex, "cpp"] = 'N/A'
                    finalDf.loc[dfIndex, "cpm"] = 'N/A'
        
                dfIndex += 1

    print(finalDf)
    return finalDf