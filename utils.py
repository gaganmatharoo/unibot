import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "uni-secret-key.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "unibotagent-yqjsuh"

import universities 
from pymongo import MongoClient
client = MongoClient("mongodb+srv://bot:supersamurai@cluster0-ymjz2.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('bot_data')
records = db.user_query

import wikipedia


uni = universities.API()


def getUniv(parameters):
    uniName = parameters.get('univ_name')
    records.insert_one({"User Query: ": str(parameters)})
    #myUniv = uni.lucky(name=uniName)
    return uniName

def getLoc(parameters):
    records.insert_one({"User Query: ": str(parameters)})
    univ = parameters.get('geo-country')
    print("Univ Name is: "  + str(univ))
    #data = uni.search(country = univ)
    return univ

def getImage(parameters):
    records.insert_one({"User Query: ": str(parameters)})
    uni = parameters.get('univ_name')
    #imgLink = "https://www.google.com?q=" + uni + ".jpg"
    l = wikipedia.WikipediaPage(title = uni)
    myList = l.images
    
    myLink = "*Check out the following images:*\n\n"
    for i in range(5):
        myLink+=myList[i]+"\n\n"
    
    return myLink

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    
    if response.intent.display_name == 'getUniv':
        uname = getUniv(dict(response.parameters))
        res = uni.lucky(name=uname)


        if res:
            res_str = "*_Name of the Institute:_* {}\n*_State:_* {}\n*_Country:_* {}\n*_Country Code:_* {}\n*_Domain:_* {}\n*_Web Page:_* {}\n\n".format(res.name, res.stateprov, res.country, res.country_code, res.domains, res.web_pages)
            data = uname.split()
            finalLink="*For more Information, please check this link:* https://en.wikipedia.org/wiki/"

            for w in data:
                finalLink+=w+"_"
        
            res_str += finalLink   

        else:
            res_str = "Sorry!!I have no information about this!"
        
        
        return res_str

    elif response.intent.display_name == 'getLoc':
        
        uniRes = getLoc(dict(response.parameters))
        print(str(uniRes))
        data = list(uni.search(country = uniRes))
        
        #tempRes = "Location is: {}".format(uniRes) 

        final_res = "*_List of first 35 Universities(alphabetically):_*" + "\n\n"
        for i in range(35):
            final_res += str(i+1) + ".) " + data[i].name + "\n"
            
        return final_res
        #return str(tempRes)

    elif response.intent.display_name == 'getImage':
        
        imgLink = getImage(dict(response.parameters))

        return imgLink        

    else:
        return response.fulfillment_text
    
    
