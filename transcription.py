# Retrieve XSAMPA transcriptions for our corpus words from http://store.apicultur.io/api/silabea/1.0.0

import requests
import json
import time
import csv

access_token="uJh6uMp_KRu8PZYSQq7tDJBKvmYa"
headers = {'Authorization':'Bearer '+access_token}

# 1 = IPA [but just the ASCII numeric codes that correspond to UTF-8 IPA symbols...]
# 2 = XSAMPA
encoding="2"

#f = open('children_forimport_022117_trans.csv')
#csv_children = csv.reader(f, delimiter=',')

#children_words = []

#for row in csv_children:
    #children_w = row[1]
    #children_words.append(children_w)

#f.close()

#with open("transcription_children.txt", "w") as f:

    #for word in children_words:
        #url="http://store.apicultur.io/api/silabea/1.0.0/"+word+"/"+encoding
        #response=requests.get(url,headers=headers).json()
        #output_line=""
        #response['palabraSilabeada'].reverse()
        #for i in response['palabraSilabeada']:
            #output_line=i+" "+output_line
        #f.write(word+"\t"+output_line+"\n")
        #time.sleep(1.25) # We get 200000 or so requests for free, but only 1/second

f = open('adults_forimport_022117_trans.csv')
csv_adults = csv.reader(f, delimiter=',')

adults_words = []

for row in csv_adults:
    adults_w = row[1]
    adults_words.append(adults_w)
    
f.close()

with open("transcription_adults.txt", "w") as f:

    for word in adults_words:
        url="http://store.apicultur.io/api/silabea/1.0.0/"+word+"/"+encoding
        response=requests.get(url,headers=headers).json()
        output_line=""
        response['palabraSilabeada'].reverse()
        for i in response['palabraSilabeada']:
            output_line=i+" "+output_line
        f.write(word+"\t"+output_line+"\n")
        time.sleep(1.25)
