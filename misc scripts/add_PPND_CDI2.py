# Given a csv file with PP/ND values for children by length, calculate z-scores / median transformation scores for words at a given length from another csv file, add these values to the wordbank CDI data file

import csv

with open("../../data/childwords_PPND_summarystats_032217.csv") as g:
    csv_summary = csv.reader(g, delimiter=',')
    
    csv_file2 = []
    
    for row in csv_summary:
        csv_file2.append(row)
        
#print(csv_file2)

with open("../../data/WSs_final_withzscores_031817_noheader.csv") as f:
    csv_file = csv.reader(f, delimiter=',')
    
    item_num = []
    transcription = []
    length = []
    PS_sum_children = []
    PS_avg_children = []
    B_sum_children = []
    B_avg_children = []
    ND_children = []
    Neighbors_children = []
    PS_avg_z_children = []
    B_avg_z_children = []
    ND_z_children = []
    PS_avg_med_children = []
    B_avg_med_children = []
    ND_med_children = []

    for row in csv_file:
        item_num.append(row[0])
        transcription.append(row[21])
        length.append(row[22].replace(" " , ""))
        PS_sum_children.append(row[23].replace(" " , ""))
        PS_avg_children.append(row[24].replace(" " , ""))
        B_sum_children.append(row[25].replace(" " , ""))
        B_avg_children.append(row[26].replace(" " , ""))
        ND_children.append(row[27].replace(" " , ""))
        Neighbors_children.append(row[28])

        B_avg_z_children.append((float(row[26].replace(" " , "")) - float(csv_file2[int(row[22].replace(" ",""))][1])) / float(csv_file2[int(row[22].replace(" ",""))][4]))
        PS_avg_z_children.append((float(row[24].replace(" " , "")) - float(csv_file2[int(row[22].replace(" ",""))][2])) / float(csv_file2[int(row[22].replace(" ",""))][5]))
        ND_z_children.append((float(row[27].replace(" " , "")) - float(csv_file2[int(row[22].replace(" ",""))][3])) / float(csv_file2[int(row[22].replace(" ",""))][6]))
        
        B_avg_med_children.append((float(row[26].replace(" " , "")) - float(csv_file2[int(row[22].replace(" ",""))][7])) / (0.5 * float(csv_file2[int(row[22].replace(" ",""))][10])))
        PS_avg_med_children.append((float(row[24].replace(" " , "")) - float(csv_file2[int(row[22].replace(" ",""))][8])) / (0.5 * float(csv_file2[int(row[22].replace(" ",""))][11])))
        ND_med_children.append((float(row[27].replace(" " , "")) - float(csv_file2[int(row[22].replace(" ",""))][9])) / (0.5 * float(csv_file2[int(row[22].replace(" ",""))][12])))
                
item_values = {}

for i, c in enumerate(item_num[1:]):
    c = str(c)
    item_values[c] = {}
      
    item_values[c]['transcription'] = transcription[i+1]
    item_values[c]['length'] = length[i+1]
    item_values[c]['PS_sum_children'] = PS_sum_children[i+1]
    item_values[c]['PS_avg_children'] = PS_avg_children[i+1]
    item_values[c]['B_sum_children'] = B_sum_children[i+1]
    item_values[c]['B_avg_children'] = B_avg_children[i+1]
    item_values[c]['ND_children'] = ND_children[i+1]
    item_values[c]['Neighbors_children'] = Neighbors_children[i+1]
    item_values[c]['PS_avg_z_children'] = PS_avg_z_children[i+1]
    item_values[c]['B_avg_z_children'] = B_avg_z_children[i+1]
    item_values[c]['ND_z_children'] = ND_z_children[i+1]
    item_values[c]['PS_avg_med_children'] = PS_avg_med_children[i+1]
    item_values[c]['B_avg_med_children'] = B_avg_med_children[i+1]
    item_values[c]['ND_med_children'] = ND_med_children[i+1]
     
            
with open('../../wordbank/instrument_data_child_by_word_wordsandsentences.csv') as f:
    csv_file = csv.reader(f, delimiter=',')
    
    orig = []
    output = []
    
    for row in csv_file:      
        
        if str(row[5][5:]) in item_values:
            output.append([item_values[row[5][5:]]['transcription'],item_values[row[5][5:]]['length'],item_values[row[5][5:]]['PS_sum_children'],item_values[row[5][5:]]['PS_avg_children'],item_values[row[5][5:]]['B_sum_children'],item_values[row[5][5:]]['B_avg_children'],item_values[row[5][5:]]['ND_children'],item_values[row[5][5:]]['Neighbors_children'],item_values[row[5][5:]]['PS_avg_z_children'],item_values[row[5][5:]]['B_avg_z_children'],item_values[row[5][5:]]['ND_z_children'],item_values[row[5][5:]]['PS_avg_med_children'],item_values[row[5][5:]]['B_avg_med_children'],item_values[row[5][5:]]['ND_med_children']])
        else:
            output.append([])
                                 
        orig.append(row)
    
with open('../../data/CDI_added_to_child_data_032317.csv', "w") as h:
    commaout = csv.writer(h, delimiter=',')
    for i, c in enumerate(output):
        commaout.writerow(orig[i]+output[i])
