## Retrieve lemmas for our corpus words using freeling

import csv
from subprocess import Popen, PIPE

f = open('children_forimport_030117.csv')
csv_children = csv.reader(f, delimiter=',')

children_words = []

for row in csv_children:
    children_w = row[1]
    children_words.append(children_w)

f.close()

with open("lemmas_children_030117.txt", "w") as f:

    for word in children_words:
        p1 = Popen(["echo", word], stdout=PIPE)
        p2 = Popen(["fl_analyze", "-f /usr/share/freeling/config/es.cfg --outlv morfo --output json"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        response = p2.communicate()[0]
        f.write(word+"\t"+str(response)+"\n")

f = open('adults_forimport_030117.csv')
csv_adults = csv.reader(f, delimiter=',')

adults_words = []

for row in csv_adults:
    adults_w = row[1]
    adults_words.append(adults_w)
    
f.close()

with open("lemmas_adults_030117.txt", "w") as f:

    for word in adults_words:
        p1 = Popen(["echo", word], stdout=PIPE)
        p2 = Popen(["fl_analyze", "-f /usr/share/freeling/config/es.cfg --outlv morfo --output json"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        response = p2.communicate()[0]
        f.write(word+"\t"+str(response)+"\n")
