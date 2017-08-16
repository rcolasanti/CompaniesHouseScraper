

import requests
import json
import numpy as np
import pandas as pd
import CoHouseToken
from difflib import SequenceMatcher



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
    df = pd.read_csv(file)
    companies = df.Organisation
    found = open("found.csv",'w')
    missing = open("missing.csv",'w')
    count=0
    for c in companies:
        c =c.upper().replace("&","AND")
        c = c.split(" T/A ")[0]
        c = c.split("WAS ")[0]
        c= spaces(c)
        url=search_url+c
        #print(url)
        results = json.loads(requests.get(url, auth=(token,pw)).text)
        res,line,number = match(c,results)
        if res:
            found.write("%s,%s,%s,\n"%(c,line,number))
            print("*",end="")
            count+=1
        else:
            missing.write("%s\n"%(c))
            print(".")
            
    found.close()
    missing.close()
    print()
    print(count/len(companies))




    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))





