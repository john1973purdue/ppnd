# Retrieve XSAMPA transcriptions for our corpus words from http://store.apicultur.io/api/silabea/1.0.0

import requests
import json
import time
import csv

#access_token="uJh6uMp_KRu8PZYSQq7tDJBKvmYa"
access_token="unLTgrPyQACwm9NXN2f9gLfPyi0a"
headers = {'Authorization':'Bearer '+access_token}

# 1 = IPA [but just the ASCII numeric codes that correspond to UTF-8 IPA symbols...]
# 2 = XSAMPA
encoding="2"

#f = open('children_forimport_lemmatized_030117(2).csv')
#csv_children = csv.reader(f, delimiter=',')

#children_words = []

#for row in csv_children:
    #children_w = row[1]
    #children_words.append(children_w)

#f.close()

#with open("transcription_children_original_030117.txt", "w") as f:

    #for word in children_words:
        #url="http://store.apicultur.io/api/silabea/1.0.0/"+word+"/"+encoding
        #response=requests.get(url,headers=headers).json()
        #output_line=""
        #response['palabraSilabeada'].reverse()
        #for i in response['palabraSilabeada']:
            #output_line=i+" "+output_line
        #f.write(word+"\t"+output_line+"\n")
        #time.sleep(1.3) # We get 200000 or so requests for free, but only 1/second

f = open('../wordbank/CDI_WGs_properties.csv')
csv_adults = csv.reader(f, delimiter=',')

adults_words = []

for row in csv_adults:
    adults_w = row[0]
    adults_words.append(adults_w)
    
f.close()

with open("transcription_CDI_030417.txt", "w") as f:

    for word in adults_words:
        url="http://store.apicultur.io/api/silabea/1.0.0/"+word+"/"+encoding
        response=requests.get(url,headers=headers).json()
        output_line=""
        response['palabraSilabeada'].reverse()
        for i in response['palabraSilabeada']:
            output_line=i+" "+output_line
        f.write(word+"\t"+output_line+"\n")
        time.sleep(1.4)
