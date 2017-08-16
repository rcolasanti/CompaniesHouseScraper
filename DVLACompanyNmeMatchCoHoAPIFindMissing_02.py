

import requests
import json
import numpy as np
import pandas as pd
import CoHouseToken
from difflib import SequenceMatcher
from operator import itemgetter



# In[3]:


def exactMatch(line1, line2):
    line1=line1.upper().rstrip()    
    line2=line2.upper().rstrip()
    #print("|"+line1+"|"+line2+"|",line1==line2)
    return line1==line2




def aStopWord(word):
    return word.upper().replace("COMPANY","CO").replace("LIMITED","LTD").replace("&","AND").rstrip() 





def spaces(word):
    w = word.upper().replace("/"," ")
    w = w.replace("."," ").replace(","," ").replace("-"," ").rstrip() 
    return w





def removeAStopWord(word):
    w = word.upper().replace("LTD"," ").replace("CO"," ").replace("AND"," ").replace("("," ").replace("/"," ")
    w = w.replace(")"," ").replace("."," ").replace(","," ").replace("-"," ").rstrip() 
    return w





def removeABlank(word):
    w = word.replace(" ","")
    return w





def removeABracket (line):
    flag = False
    word=""
    for a in line:
        if a=="(":
            flag = True
            a=""
        if a==")":
            a=""
            flag = False
        if flag:
            a=""
        word+=a
    return word
    





def stopWord(line1, line2):
    line1=aStopWord(line1)  
    line2=aStopWord(line2)
    #print("|"+line1+"|"+line2+"|",line1==line2)
    return line1==line2





def removeStopWord(line1, line2):
    line1=spaces(line1)  
    line2=spaces(line2)
    line1=aStopWord(line1)  
    line2=aStopWord(line2)
    line1=removeAStopWord(line1)  
    line2=removeAStopWord(line2)
    #print("|"+line1+"|"+line2+"|",line1==line2)
    return line1==line2





def removeBlanks(line1, line2):
    line1=spaces(line1)  
    line2=spaces(line2)
    line1=aStopWord(line1)  
    line2=aStopWord(line2)
    line1=removeAStopWord(line1)  
    line2=removeAStopWord(line2)
    line1=removeABlank(line1)  
    line2=removeABlank(line2)
    return line1==line2





def removeBrackets(line1, line2):
    line1=removeABracket(line1)  
    line2=removeABracket(line2)
    line1=spaces(line1)  
    line2=spaces(line2)
    line1=aStopWord(line1)  
    line2=aStopWord(line2)
    line1=removeAStopWord(line1)  
    line2=removeAStopWord(line2)
    line1=removeABlank(line1)  
    line2=removeABlank(line2)
   #print("|"+line1+"|"+line2+"|",line1==line2)
    
    return line1==line2





def strip(line1, line2):
    line1=removeABracket(line1)  
    line2=removeABracket(line2)
    line1=spaces(line1)  
    line2=spaces(line2)
    line1=aStopWord(line1)  
    line2=aStopWord(line2)
    line1=removeAStopWord(line1)  
    line2=removeAStopWord(line2)
    line1=removeABlank(line1)  
    line2=removeABlank(line2)
    
    return line1,line2





def match(company,results):
    for i in results['items']:
        line = i['title']
        number = i['company_number']
        if(exactMatch(company,line)):
            return True,line,number
            
    for i in results['items']:
        line = i['title']
        number = i['company_number']
        if(stopWord(company,line)):
            return True,line,number
            
    for i in results['items']:
        line = i['title']
        number = i['company_number']
        if(removeStopWord(company,line)):
            return True,line,number
            
    for i in results['items']:
        line = i['title']
        number = i['company_number']
        if(removeBlanks(company,line)):
            return True,line,number
            
    for i in results['items']:
        line = i['title']
        number = i['company_number']
        if(removeBrackets(company,line)):
            return True,line,number
        
        #old_match(company,results)
    return False,"",""




def main(args):
    print(args[0])
    search_url ="https://api.companieshouse.gov.uk/search/companies?q="
    token = CoHouseToken.getToken()
    pw = ''
    base_url = 'https://api.companieshouse.gov.uk'
    file = args[1]
    print(file)
    df = pd.read_csv(file,names=['Organisation'])
    companies = df.Organisation
    count=0
    found = open("found2.csv",'w')
    missing = open("missing2.csv",'w')

    for c in companies:
        c =c.upper().replace("&","AND")
        c = c.split(" T/A ")[0]
        c = c.split("WAS ")[0]
        c= spaces(c)
        url=search_url+c
        results = json.loads(requests.get(url, auth=(token,pw)).text)
        
        for i , key  in enumerate(results['items']):
            a,b = strip(c, key['title'])
            r = SequenceMatcher(None, a, b).ratio()
            results['items'][i]['ratio'] = r
            
        newlist = sorted(results['items'], key=itemgetter('ratio'),reverse=True) 
        for i , key  in enumerate(newlist):
            print("%s \t %s\t %.2f \t %s \t %s"%(i,c,key['ratio'],key['company_number'],key['title']))
        
        v = input('type number or return to reject: ')
        if v =="":
            print("reject")
            missing.write("%s\n"%(c))
        else:
            key = newlist[int(v)]
            print("%s \t %s\t %.2f \t %s \t %s"%(v,c,r,key['company_number'],key['title']))
            print("*************************")
            found.write("%s,%s,%s,\n"%(c,key['title'],key['company_number']))
        
            
    print()
    #print(count/len(companies))




    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))





