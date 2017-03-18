# Given a csv file with PP/ND values, item #s for words, add these values to the wordbank CDI data file

import csv

with open("../../data/WSs_final_withzscores_031817.csv") as f:
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
    PS_sum_adults = []
    PS_avg_adults = []
    B_sum_adults = []
    B_avg_adults = []
    ND_adults = []
    Neighbors_adults = []
    PS_avg_diff = []
    B_avg_diff = []
    ND_diff = []
    PS_avg_z_children = []
    B_avg_z_children = []
    ND_z_children = []
    PS_avg_z_adults = []
    B_avg_z_adults = []
    ND_z_adults = []
        
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
        PS_sum_adults.append(row[29].replace(" " , ""))
        PS_avg_adults.append(row[30].replace(" " , ""))
        B_sum_adults.append(row[31].replace(" " , ""))
        B_avg_adults.append(row[32].replace(" " , ""))
        ND_adults.append(row[33].replace(" " , ""))
        Neighbors_adults.append(row[34])
        PS_avg_diff.append(row[35])
        B_avg_diff.append(row[36])
        ND_diff.append(row[37])
        PS_avg_z_children.append(row[51])
        B_avg_z_children.append(row[50])
        ND_z_children.append(row[54])
        PS_avg_z_adults.append(row[52])
        B_avg_z_adults.append(row[53])
        ND_z_adults.append(row[55])
    
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
    item_values[c]['PS_sum_adults'] = PS_sum_adults[i+1]
    item_values[c]['PS_avg_adults'] = PS_avg_adults[i+1]
    item_values[c]['B_sum_adults'] = B_sum_adults[i+1]
    item_values[c]['B_avg_adults'] = B_avg_adults[i+1]
    item_values[c]['ND_adults'] = ND_adults[i+1]
    item_values[c]['Neighbors_adults'] = Neighbors_adults[i+1]
    item_values[c]['PS_avg_diff'] = PS_avg_diff[i+1]
    item_values[c]['B_avg_diff'] = B_avg_diff[i+1]
    item_values[c]['ND_diff'] = ND_diff[i+1]
    item_values[c]['PS_avg_z_children'] = PS_avg_z_children[i+1]
    item_values[c]['B_avg_z_children'] = B_avg_z_children[i+1]
    item_values[c]['ND_z_children'] = ND_z_children[i+1]
    item_values[c]['PS_avg_z_adults'] = PS_avg_z_adults[i+1]
    item_values[c]['B_avg_z_adults'] = B_avg_z_adults[i+1]
    item_values[c]['ND_z_adults'] = ND_z_adults[i+1]          
            
with open('../../wordbank/instrument_data_child_by_word_wordsandsentences.csv') as f:
    csv_file = csv.reader(f, delimiter=',')
    
    orig = []
    output = []
    
    for row in csv_file:      
        
        if str(row[5][5:]) in item_values:
            output.append([item_values[row[5][5:]]['transcription'],item_values[row[5][5:]]['length'],item_values[row[5][5:]]['PS_sum_children'],item_values[row[5][5:]]['PS_avg_children'],item_values[row[5][5:]]['B_sum_children'],item_values[row[5][5:]]['B_avg_children'],item_values[row[5][5:]]['ND_children'],item_values[row[5][5:]]['Neighbors_children'],item_values[row[5][5:]]['PS_sum_adults'],item_values[row[5][5:]]['PS_avg_adults'],item_values[row[5][5:]]['B_sum_adults'],item_values[row[5][5:]]['B_avg_adults'],item_values[row[5][5:]]['ND_adults'],item_values[row[5][5:]]['Neighbors_adults'],item_values[row[5][5:]]['PS_avg_diff'],item_values[row[5][5:]]['B_avg_diff'],item_values[row[5][5:]]['ND_diff'],item_values[row[5][5:]]['PS_avg_z_children'],item_values[row[5][5:]]['B_avg_z_children'],item_values[row[5][5:]]['ND_z_children'],item_values[row[5][5:]]['PS_avg_z_adults'],item_values[row[5][5:]]['B_avg_z_adults'],item_values[row[5][5:]]['ND_z_adults']])
        else:
            output.append([])
                                 
        orig.append(row)
    
with open('../../wordbank/CDI_added_to_child_data.csv', "w") as h:
    commaout = csv.writer(h, delimiter=',')
    for i, c in enumerate(output):
        commaout.writerow(orig[i]+output[i])
