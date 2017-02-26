# Note: to open this in python shell: exec(open('SpanPPND.py').read())

## To do: right now, the calculator is only partially aware of stress and that's when an accented vowel is in a word; otherwise, it does not take stress into account; is this good? Also, accented vowels might in some sense 'throw off' the calculations for PP/ND... Possibly we could disregard stress for PP but include it for ND?
## To do: make sure that when searching for ND matches, the matches are case-sensitive [will matter when we change our corpus to our final encoding]
## To do: find a list of representative Spanish words that both children and adults would likely know for comparing PP/ND (similar to Storkel & Hoover, 2010, p. 500)

## In process:
## To do: make final decisions about how to treat different characters:
    ### Either code this in our calculator or use this scheme to recode our corpus:
        ### For c and g, look ahead one position and then categorize as theta, k, x, or g
        ### For ll and rr, look ahead one position and then categorize as L or R
        ### For ch, look ahead.... categorize as C
        ### For h, delete it
        ### For ü, this should be taken care of in g code
        ### For x, change to ks or x or h...
            ### We need a list of x-words
    ### **** Or: have users' input be phonemic, which would allow nonsense words/syllables to be input. We would then need to code our input corpus phonemically. I'm thinking that this is the best of our options.

## Elizabeth: 
## To do: write something to export PP/ND values to CSV file for later analysis
## Make a function that can expect a dictionary as input in the following form:
## input_dictionary = {'mama': {'PS_phonemes_children': ['m1', 'a2', 'm3', 'a4'], 'PS_children': ['0.070354', '0.209508', '0.045825', '0.167909'], 'PS_sum_children': '0.493596', 'PS_avg_children': '0.123399', 'PS_phonemes_adults': ['m1', 'a2', 'm3', 'a4'], 'PS_adults': ['0.066131', '0.196646', '0.045695', '0.156658'], 'PS_sum_adults': '0.46513', 'PS_avg_adults': '0.116282', 'B_avg_children': '0.0131', 'B_sum_children': '0.0393', 'B_phonemes_children': ['ma1', 'am2', 'ma3'], 'B_children': ['0.019057', '0.013471', '0.006771'], 'B_avg_adults': '0.011943', 'B_sum_adults': '0.03583', 'B_phonemes_adults': ['ma1', 'am2', 'ma3'], 'B_adults': ['0.017061', '0.011384', '0.007385'], 'Neighbors_children': ['mami', 'mamá', 'cama', 'mala', 'rama', 'mata', 'ama'], 'Neighbors_adults': ['mami', 'mamá', 'cama', 'mala', 'rama', 'mamar', 'mata', 'ama'], 'ND_children': 7, 'ND_adults': 8}, 'Word2': {etc.}}.
## And from this information export a csv file 

## Complete:
## To do: make the PP/ND return code loop over a list of words provided by the user
## To do: reformat the PP/ND return code so that it returns a standardized dictionary format that can later be used to create tables [see section below for details]
## To do: clean up the ND candidate return code so that it returns the candidate from the function in addition to 0 or 1, puts them into a list, and then outputs them later in a nice list [no longer relevant]
## To do: format the output in tables --> output.txt


# Loading corpus words: https://pythonprogramming.net/reading-csv-files-python-3/

import csv

f = open('children_forimport_022117.csv')
csv_children = csv.reader(f, delimiter=',')

children_words = []
children_logfreq = []

for row in csv_children:
    children_lf = row[0]
    children_w = row[1]
    children_logfreq.append(children_lf)
    children_words.append(children_w)

f.close()

f = open('adults_forimport_022117.csv')
csv_adults = csv.reader(f, delimiter=',')

adults_words = []
adults_logfreq = []

for row in csv_adults:
    adults_lf = row[0]
    adults_w = row[1]
    adults_logfreq.append(adults_lf)
    adults_words.append(adults_w)
    
f.close()
    
# Positional segment calculation

children_PS = {}
    
for word in children_words:
    word_index = children_words.index(word)
    logfreq = children_logfreq[word_index]
    for i, c in enumerate(word):
        newkey = c+str(i+1)
        if newkey in children_PS:
            children_PS[newkey] += float(logfreq)
        else:
            children_PS[newkey] = float(logfreq)
        
adults_PS = {}
    
for word in adults_words:
    word_index = adults_words.index(word)
    logfreq = adults_logfreq[word_index]
    for i, c in enumerate(word):
        newkey = c+str(i+1)
        if newkey in adults_PS:
            adults_PS[newkey] += float(logfreq)
        else:
            adults_PS[newkey] = float(logfreq)
        
# Biphone calculation
# Note: biphone positions are indexed by their first element

children_B = {}

for word in children_words:
    word_index = children_words.index(word)
    logfreq = children_logfreq[word_index]
    for i, c in enumerate(word):
        if len(word) != 1:
            if len(word) != i+1:
                newkey = c+word[i+1]+str(i+1)
                if newkey in children_B:
                    children_B[newkey] += float(logfreq)
                else:
                    children_B[newkey] = float(logfreq)

adults_B = {}

for word in adults_words:
    word_index = adults_words.index(word)
    logfreq = adults_logfreq[word_index]
    for i, c in enumerate(word):
        if len(word) != 1:
            if len(word) != i+1:
                newkey = c+word[i+1]+str(i+1)
                if newkey in adults_B:
                    adults_B[newkey] += float(logfreq)
                else:
                    adults_B[newkey] = float(logfreq)

# Single position logfreqs

children_P1 = {}

for word in children_words:
    word_index = children_words.index(word)
    logfreq = children_logfreq[word_index]
    for i, c in enumerate(word):
        if i in children_P1:
            children_P1[i] += float(logfreq)
        else:
            children_P1[i] = float(logfreq)
            
adults_P1 = {}

for word in adults_words:
    word_index = adults_words.index(word)
    logfreq = adults_logfreq[word_index]
    for i, c in enumerate(word):
        if i in adults_P1:
            adults_P1[i] += float(logfreq)
        else:
            adults_P1[i] = float(logfreq)
            
# Biphone position logfreqs

children_P2 = {}

for word in children_words:
    word_index = children_words.index(word)
    logfreq = children_logfreq[word_index]
    for i, c in enumerate(word):
        if len(word) != 1:
            if len(word) != i+1:
                if i in children_P2:
                    children_P2[i] += float(logfreq)
                else:
                    children_P2[i] = float(logfreq)

adults_P2 = {}

for word in adults_words:
    word_index = adults_words.index(word)
    logfreq = adults_logfreq[word_index]
    for i, c in enumerate(word):
        if len(word) != 1:
            if len(word) != i+1:
                if i in adults_P2:
                    adults_P2[i] += float(logfreq)
                else:
                    adults_P2[i] = float(logfreq)
                    
# ND finding matches

def find_matches_children(candidate):
    matches = 0
    if candidate in children_words:
        matches = 1
        #print('Children: '+candidate)
    return matches

def find_matches_adults(candidate):
    matches = 0
    if candidate in adults_words:
        matches = 1
        #print('Adults: '+candidate)
    return matches

# PS / B / ND return

def return_values(input_word):
    
    return_dict = {}
    
    #print("****************************************")
    
    #print("Word: "+input_word)
    
    #print("Positional segment frequency")

    PS_sum_children = 0
    
    PS_phonemes_list_children = []
    
    PS_values_list_children = []

    for i, c in enumerate(input_word):
        newkey = c+str(i+1)
        if newkey in children_PS:
            #print(newkey+": "+str(round(children_PS[newkey]/children_P1[i],6)))
            PS_phonemes_list_children.append(str(newkey))
            PS_values_list_children.append(str(round(children_PS[newkey]/children_P1[i],6)))
            PS_sum_children += children_PS[newkey]/children_P1[i]
        else:
            #print(newkey+": N/A")
            PS_phonemes_list_children.append(str(newkey))
            PS_values_list_children.append("N/A")
            
    #print("Positional segment frequency sum: "+str(round(PS_sum,6)))
        
    #print("Positional segment frequency average: "+str(round(PS_sum/len(input_word),6)))
    
    return_dict['PS_phonemes_children']=PS_phonemes_list_children
    return_dict['PS_children']=PS_values_list_children
    return_dict['PS_sum_children']=str(round(PS_sum_children,6))
    return_dict['PS_avg_children']=str(round(PS_sum_children/len(input_word),6))

    PS_sum_adults = 0
    
    PS_phonemes_list_adults = []
    
    PS_values_list_adults = []

    for i, c in enumerate(input_word):
        newkey = c+str(i+1)
        if newkey in adults_PS:
            #print(newkey+": "+str(round(children_PS[newkey]/children_P1[i],6)))
            PS_phonemes_list_adults.append(str(newkey))
            PS_values_list_adults.append(str(round(adults_PS[newkey]/adults_P1[i],6)))
            PS_sum_adults += adults_PS[newkey]/adults_P1[i]
        else:
            #print(newkey+": N/A")
            PS_phonemes_list_adults.append(str(newkey))
            PS_values_list_adults.append("N/A")
            
    #print("Positional segment frequency sum: "+str(round(PS_sum,6)))
        
    #print("Positional segment frequency average: "+str(round(PS_sum/len(input_word),6)))
    
    return_dict['PS_phonemes_adults']=PS_phonemes_list_adults
    return_dict['PS_adults']=PS_values_list_adults
    return_dict['PS_sum_adults']=str(round(PS_sum_adults,6))
    return_dict['PS_avg_adults']=str(round(PS_sum_adults/len(input_word),6))

    #print("Biphone frequency")

    B_sum_children = 0
    
    B_phonemes_list_children = []
    
    B_values_list_children = []

    for i, c in enumerate(input_word):
        if len(input_word) != 1:
            if len(input_word) != i+1:
                newkey = c+input_word[i+1]+str(i+1)
                if newkey in children_B:
                    #print(newkey+": "+str(round(children_B[newkey]/children_P2[i],6)))
                    B_sum_children += children_B[newkey]/children_P2[i]
                    B_phonemes_list_children.append(str(newkey))
                    B_values_list_children.append(str(round(children_B[newkey]/children_P2[i],6)))
                else:
                    #print(newkey+": N/A")
                    B_phonemes_list_children.append(str(newkey))
                    B_values_list_children.append("0")
        else:
            #print("No biphone frequency")
            B_phonemes_list_children.append("N/A")
            B_values_list_children.append("N/A")
    
    #print("Biphone frequency sum: "+str(round(B_sum,6)))
            
    if len(input_word) > 1:
        #print("Biphone frequency average: "+str(round(B_sum/(len(input_word)-1),6)))
        return_dict['B_avg_children']=str(round(B_sum_children/(len(input_word)-1),6))
        return_dict['B_sum_children']=str(round(B_sum_children,6))
    else:
        #print("Biphone frequency average: N/A")
        return_dict['B_avg_children']="N/A"
        return_dict['B_sum_children']="N/A"
        
    return_dict['B_phonemes_children']=B_phonemes_list_children
    return_dict['B_children']=B_values_list_children

    B_sum_adults = 0
    
    B_phonemes_list_adults = []
    
    B_values_list_adults = []

    for i, c in enumerate(input_word):
        if len(input_word) != 1:
            if len(input_word) != i+1:
                newkey = c+input_word[i+1]+str(i+1)
                if newkey in adults_B:
                    #print(newkey+": "+str(round(children_B[newkey]/children_P2[i],6)))
                    B_sum_adults += adults_B[newkey]/adults_P2[i]
                    B_phonemes_list_adults.append(str(newkey))
                    B_values_list_adults.append(str(round(adults_B[newkey]/adults_P2[i],6)))
                else:
                    #print(newkey+": N/A")
                    B_phonemes_list_adults.append(str(newkey))
                    B_values_list_adults.append("0")
        else:
            #print("No biphone frequency")
            B_phonemes_list_adults.append("N/A")
            B_values_list_adults.append("N/A")
    
    #print("Biphone frequency sum: "+str(round(B_sum,6)))
            
    if len(input_word) > 1:
        #print("Biphone frequency average: "+str(round(B_sum/(len(input_word)-1),6)))
        return_dict['B_avg_adults']=str(round(B_sum_adults/(len(input_word)-1),6))
        return_dict['B_sum_adults']=str(round(B_sum_adults,6))
    else:
        #print("Biphone frequency average: N/A")
        return_dict['B_avg_adults']="N/A"
        return_dict['B_sum_adults']="N/A"
        
    return_dict['B_phonemes_adults']=B_phonemes_list_adults
    return_dict['B_adults']=B_values_list_adults

    #print("Neighborhood density")

    # ND

    # Possible phonemes: need to update this
    
    phonemes = ('a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú', 'y', 'ñ', 'b', 'c', 'C', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'L', 'm', 'n', 'p', 'q', 'r', 'R', 's', 't', 'v', 'w', 'x', 'z')

    # For each word, cycle through each of the following processes, searching through the wordlists and adding up matches

    # 1. Addition: cycle through each position, adding each of the possible phonemes around that position (before and after for initial position, after only for all others)
    # 2. Deletion: cycle through each position, deleting a phoneme
    # 3. Substitution: cycle through each position, changing it to any dissimilar phoneme

    matches_children = 0
    matches_adults = 0
    
    N_children = []
    N_adults = []
    ND_children_num = []
    ND_adults_num = []
    
    for j in phonemes:
        for i, c in enumerate(input_word):
            newword_addition = input_word[:i]+j+input_word[i:]
            if find_matches_children(newword_addition) == 1:
                matches_children += 1
                N_children.append(newword_addition)
            if find_matches_adults(newword_addition) == 1:
                matches_adults += 1
                N_adults.append(newword_addition)
            if i+1 == len(input_word):
                newword_addition = input_word[:i+1]+j
                if find_matches_children(newword_addition) == 1:
                    matches_children += 1
                    N_children.append(newword_addition)
                if find_matches_adults(newword_addition) == 1:
                    matches_adults += 1
                    N_adults.append(newword_addition)
            if j != input_word[i]:
                if i == 0:
                    newword_substitution = j+input_word[i+1:]
                    if find_matches_children(newword_substitution) == 1:
                        matches_children += 1
                        N_children.append(newword_substitution)
                    if find_matches_adults(newword_substitution) == 1:
                        matches_adults += 1
                        N_adults.append(newword_substitution)
                else:
                    newword_substitution = input_word[:i]+j+input_word[i+1:]
                    if find_matches_children(newword_substitution) == 1:
                        matches_children += 1
                        N_children.append(newword_substitution)
                    if find_matches_adults(newword_substitution) == 1:
                        matches_adults += 1
                        N_adults.append(newword_substitution)

    for i, c in enumerate(input_word):
        if i == 0:
            newword_deletion = input_word[i+1:]
            if find_matches_children(newword_deletion) == 1:
                matches_children += 1
                N_children.append(newword_deletion)
            if find_matches_adults(newword_deletion) == 1:
                matches_adults += 1
                N_adults.append(newword_deletion)
        else:
            newword_deletion = input_word[:i]+input_word[i+1:]
            if find_matches_children(newword_deletion) == 1:
                matches_children += 1
                N_children.append(newword_deletion)
            if find_matches_adults(newword_deletion) == 1:
                matches_adults += 1
                N_adults.append(newword_deletion)

    #print('# of neighbors (children): '+str(matches_children))

    #print('# of neighbors (adults): '+str(matches_adults))
    
    return_dict['Neighbors_children']=N_children
    return_dict['Neighbors_adults']=N_adults
    return_dict['ND_children']=str(matches_children)
    return_dict['ND_adults']=str(matches_adults)

    return return_dict

# User input

user_input = input("Enter space-separated list of words: ")
user_input_list = user_input.split(' ')

collated_output={}

for word in user_input_list:
    collated_output[word]=return_values(word)

#print(collated_output)

## input_dictionary = {'mama': {'PS_phonemes_children': ['m1', 'a2', 'm3', 'a4'], 'PS_children': ['0.070354', '0.209508', '0.045825', '0.167909'], 'PS_sum_children': '0.493596', 'PS_avg_children': '0.123399', 'PS_phonemes_adults': ['m1', 'a2', 'm3', 'a4'], 'PS_adults': ['0.066131', '0.196646', '0.045695', '0.156658'], 'PS_sum_adults': '0.46513', 'PS_avg_adults': '0.116282', 'B_avg_children': '0.0131', 'B_sum_children': '0.0393', 'B_phonemes_children': ['ma1', 'am2', 'ma3'], 'B_children': ['0.019057', '0.013471', '0.006771'], 'B_avg_adults': '0.011943', 'B_sum_adults': '0.03583', 'B_phonemes_adults': ['ma1', 'am2', 'ma3'], 'B_adults': ['0.017061', '0.011384', '0.007385'], 'Neighbors_children': ['mami', 'mamá', 'cama', 'mala', 'rama', 'mata', 'ama'], 'Neighbors_adults': ['mami', 'mamá', 'cama', 'mala', 'rama', 'mamar', 'mata', 'ama'], 'ND_children': 7, 'ND_adults': 8}, 'Word2': {etc.}}.

# Table output here

def children_table():

    with open("output.txt", "w") as f:
        
        f.write("Children\n")

        # Go through each key, count up members of B and PS lists, use this information to have proper # of PS, B columns

        max_PS_length=0

        for key, val in collated_output.items():
            if len(collated_output[key]['PS_phonemes_children']) > max_PS_length:
                max_PS_length = len(collated_output[key]['PS_phonemes_children'])

        PS_columns=""

        for i in range(max_PS_length+1,1,-1):
            PS_columns = '{0: <10}'.format("PS"+str(i-1))+"\t"+PS_columns
            
        B_columns=""

        for i in range(max_PS_length,1,-1):
            B_columns = '{0: <10}'.format("B"+str(i-1))+"\t"+B_columns

        f.write('{0: <10}'.format("Word")+"\t"+PS_columns+'{0: <10}'.format("PS sum")+"\t"+'{0: <10}'.format("PS avg")+"\t"+B_columns+'{0: <10}'.format("B sum")+"\t"+'{0: <10}'.format("B avg")+"\t"+'{0: <10}'.format("ND")+"\t"+'{0: <10}'.format("Neighbors")+"\n")

        for key, val in collated_output.items():
            PS_output_line=""
            
            for i in range(max_PS_length,0,-1):
                if len(collated_output[key]['PS_children']) < i:
                    PS_output_line='{0: <10}'.format('--')+"\t"+PS_output_line
                else:
                    PS_output_line='{0: <10}'.format(collated_output[key]['PS_children'][i-1])+"\t"+PS_output_line
                    
            B_output_line=""
            
            for i in range(max_PS_length-1,0,-1):
                if len(collated_output[key]['B_children']) < i:
                    B_output_line='{0: <10}'.format('--')+"\t"+B_output_line
                else:
                    B_output_line='{0: <10}'.format(collated_output[key]['B_children'][i-1])+"\t"+B_output_line
                    
            neighbors_output_line=""
            
            for i, c in enumerate(collated_output[key]['Neighbors_children']):
                neighbors_output_line=collated_output[key]['Neighbors_children'][i]+' '+neighbors_output_line
                
            output_line=""
            
            # Ensuring consistent spacing: '{0: <16}'.format('Hi')
            # https://docs.python.org/3.6/library/string.html#formatstrings
            # http://stackoverflow.com/questions/2872512/python-truncate-a-long-string
            
            word = (key[:7] + '...') if len(key) > 10 else key
            
            output_line='{0: <10}'.format(word)+"\t"+PS_output_line+'{0: <10}'.format(collated_output[key]['PS_sum_children'])+"\t"+'{0: <10}'.format(collated_output[key]['PS_avg_children'])+"\t"+B_output_line+'{0: <10}'.format(collated_output[key]['B_sum_children'])+"\t"+'{0: <10}'.format(collated_output[key]['B_avg_children'])+"\t"+'{0: <10}'.format(collated_output[key]['ND_children'])+"\t"+neighbors_output_line
            
            f.write(output_line+"\n")
    return

children_table()

def adults_table():

    with open("output.txt", "a") as f:
        
        f.write("Adults\n")

        # Go through each key, count up members of B and PS lists, use this information to have proper # of PS, B columns

        max_PS_length=0

        for key, val in collated_output.items():
            if len(collated_output[key]['PS_phonemes_adults']) > max_PS_length:
                max_PS_length = len(collated_output[key]['PS_phonemes_adults'])

        PS_columns=""

        for i in range(max_PS_length+1,1,-1):
            PS_columns = '{0: <10}'.format("PS"+str(i-1))+"\t"+PS_columns
            
        B_columns=""

        for i in range(max_PS_length,1,-1):
            B_columns = '{0: <10}'.format("B"+str(i-1))+"\t"+B_columns

        f.write('{0: <10}'.format("Word")+"\t"+PS_columns+'{0: <10}'.format("PS sum")+"\t"+'{0: <10}'.format("PS avg")+"\t"+B_columns+'{0: <10}'.format("B sum")+"\t"+'{0: <10}'.format("B avg")+"\t"+'{0: <10}'.format("ND")+"\t"+'{0: <10}'.format("Neighbors")+"\n")

        for key, val in collated_output.items():
            PS_output_line=""
            
            for i in range(max_PS_length,0,-1):
                if len(collated_output[key]['PS_adults']) < i:
                    PS_output_line='{0: <10}'.format('--')+"\t"+PS_output_line
                else:
                    PS_output_line='{0: <10}'.format(collated_output[key]['PS_adults'][i-1])+"\t"+PS_output_line
                    
            B_output_line=""
            
            for i in range(max_PS_length-1,0,-1):
                if len(collated_output[key]['B_adults']) < i:
                    B_output_line='{0: <10}'.format('--')+"\t"+B_output_line
                else:
                    B_output_line='{0: <10}'.format(collated_output[key]['B_adults'][i-1])+"\t"+B_output_line
                    
            neighbors_output_line=""
            
            for i, c in enumerate(collated_output[key]['Neighbors_adults']):
                neighbors_output_line=collated_output[key]['Neighbors_adults'][i]+' '+neighbors_output_line
                
            output_line=""
            
            # Ensuring consistent spacing: '{0: <16}'.format('Hi')
            # https://docs.python.org/3.6/library/string.html#formatstrings
            # http://stackoverflow.com/questions/2872512/python-truncate-a-long-string
            
            word = (key[:7] + '...') if len(key) > 10 else key
            
            output_line='{0: <10}'.format(word)+"\t"+PS_output_line+'{0: <10}'.format(collated_output[key]['PS_sum_adults'])+"\t"+'{0: <10}'.format(collated_output[key]['PS_avg_adults'])+"\t"+B_output_line+'{0: <10}'.format(collated_output[key]['B_sum_adults'])+"\t"+'{0: <10}'.format(collated_output[key]['B_avg_adults'])+"\t"+'{0: <10}'.format(collated_output[key]['ND_adults'])+"\t"+neighbors_output_line
            
            f.write(output_line+"\n")
    return

adults_table()

#### NOTES/TESTING BELOW:

# Ideally, this function will not print anything out here but instead will return the information necessary to produce pretty tables and summary information, so that after we loop through all the user's input words, we can simply throw all the information together into one table (instead of separate sections for each word as it is now)

# Goal: have this function return a dictionary formatted like this (**note, see below for change): {[wordname]: [input_word], [PS_phonemes]: [PS_phoneme1,PS_phoneme2,etc.], [PS]: [PS1,PS2,etc.], [Biphones]: [Biphone1,Biphone2,etc.], [B]: [B1,B2,B3,etc.], [ND_children]: [neighbor1,neighbor2,etc.], [ND_children_num]: [# of neighbors], [ND_adults]: [neighbor1,neighbor2,etc.], [ND_adults_num]: [# of neighbors]}

# Example: test = {'wordname': ['mama'], 'PS_phonemes': ['m', 'a', 'm', 'a'], 'PS': [1.2, 2.2, 3.3, 3.4], 'Biphones': ['ma', 'am', 'ma'], 'B': [1.5, 2.5, 3.5], 'ND_children': ['mami', 'nama'], 'ND_children_num': [2], 'ND_adults': ['mami', 'nama', 'mapa'], 'ND_adults_num': [3]}

#>>> print(tabulate(test,headers="keys"))
#wordname    PS_phonemes      PS  Biphones      B  ND_children      ND_children_num  ND_adults      ND_adults_num
#----------  -------------  ----  ----------  ---  -------------  -----------------  -----------  ----------------
#mama        m               1.2  ma          1.5  mami                           2  mami                        3
            #a               2.2  am          2.5  nama                              nama
            #m               3.3  ma          3.5                                    mapa
            #a               3.4

# It might be best to then take this output and add it to a dictionary of dictionaries to collate the output for all the user's words: https://www.quora.com/In-Python-can-we-add-a-dictionary-inside-a-dictionary-If-yes-how-can-we-access-the-inner-dictionary-using-the-key-in-the-primary-dictionary http://stackoverflow.com/questions/1024847/add-key-to-a-dictionary-in-python

# Therefore, let's change our output dictionary format to this: test = {'PS_phonemes': ['m', 'a', 'm', 'a'], 'PS': [1.2, 2.2, 3.3, 3.4], 'Biphones': ['ma', 'am', 'ma'], 'B': [1.5, 2.5, 3.5], 'ND_children': ['mami', 'nama'], 'ND_children_num': [2], 'ND_adults': ['mami', 'nama', 'mapa'], 'ND_adults_num': [3]}. Note that the word no longer appears.

# This allows us to add other entries as needed with the key being the word. We will need to check for collisions in keys. If there is a collision, rather than dropping, just have the dictionary refer to the identical entry and then use that entry to later populate the lines in the output table. Use some sort of code dummy variable to indicate to the table function that it needs to copy from another entry.

# After our function returns the dictionary, we must add it to a global dictionary of dictionaries that collects all the output for each word, using the input_word as the key: collated_output[input_word] = //returned dictionary//. This will be done outside the function.

# Then, we will use the dictionary of dictionaries to create a table that lays out all of the information for all the words in a consistent manner amenable to copying and pasting.

# Functions: https://www.tutorialspoint.com/python/python_functions.htm

# Checking if something is in list: http://stackoverflow.com/questions/11251709/check-if-item-is-in-an-array

# Cutting/slicing strings: http://pythoncentral.io/cutting-and-slicing-strings-in-python/

# User input: http://stackoverflow.com/questions/8162021/analyzing-string-input-until-it-reaches-a-certain-letter-on-python

# Table output: https://pypi.python.org/pypi/tabulate

#table = [["Word1","PS1","PS2","PS3"],["Word2","PS1"]]
#print(tabulate(table,headers=["Word","PS1","PS2","PS3","PS4"],tablefmt="fancy_grid"))
#Word    PS1    PS2    PS3
#------  -----  -----  -----
#Word1   PS1    PS2    PS3
#Word2   PS1

# Rounding ouput: http://stackoverflow.com/questions/20457038/python-how-to-round-down-to-2-decimals

    
# Testing: looking up logfreq based on a word "zumo"

#word_index = children_words.index('zumo')
#logfreq = children_logfreq[word_index]
#print(logfreq)

    #for key2, val2 in collated_output[key].items():
        #print(str(key2)+": "+str(collated_output[key][key2]))
        

        # Need to have user-selected adult / children, then construct table with one set of values
        # Construct table like so: Word SP1 SP2 SP# SP_sum SP_avg B1 B2 B# B_sum B_avg ND


######

## Positional segment frequency initial calculation

# Set up 2xn array [A] for position :: phoneme --> contents: logfreq(word)

# Testing: creating a two dimensional array: http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python


#children_PS = {}
#children_PS[0,0] = 'phon1'
#children_PS[0,1] = 'freq1'
#children_PS[1,0] = 'phon2'
#children_PS[1,1] = 'freq2'
#print(children_PS[0,0])
#print(children_PS[0,1])
#print(children_PS[1,0])
#print(children_PS[1,1])

# Testing: looking up test logfreq 1 based on test phoneme 1 value: http://stackoverflow.com/questions/6518291/using-index-on-multidimensional-lists, ** http://stackoverflow.com/questions/2205985/searching-a-2-dimensional-tuple-list-in-python

#temp_index = children_PS.index('test phoneme 1')
#temp = children_PS[temp_index,1]

#i = None
#for index, item in enumerate(children_PS):
#    if item[0] == 'test logfreq 1':
#         i = index
#         break
#print(i)

# Testing: dictionaries instead: http://openbookproject.net/thinkcs/python/english3e/dictionaries.html, http://stackoverflow.com/questions/960733/python-creating-a-dictionary-of-lists

#children_PS = {}

# Testing: I have a phoneme 'n' in position 1 and it has logfreq 3.45

#children_PS['n'] = (1, 3.45)

# Testing: or, we name the keys of our dictionary like this --> children_PS[phonene_positionnumber] = logfreq

#children_PS['n1'] = 3.45
#print(children_PS['n1'])

# Testing: I have another phoneme 'n' in position 1 and it has logfreq 2.35. I must add 2.35 to 3.45.

#children_PS['n1'] += 2.35
#print(children_PS['n1'])

# Testing: I have detected a phoneme 'n' in position 3 with logfreq 5.32 and I need to add it to the dictionary:

#newkey = 'n'+str(3)
#children_PS[newkey] = 5.32
#print(children_PS['n3'])

# Testing: I have a test word 'test' and I want to add its logfreq (1.23) to the dictionary with the appropriate keys: http://stackoverflow.com/questions/538346/iterating-over-a-string

#for i, c in enumerate('test'):
#    newkey = c+str(i+1)
#    children_PS[newkey] = 1.23
#    print(children_PS[newkey])

# Testing: I have a word 'tease' and I want to add its logfreq (2.00) to the dictionary, making sure to add to values when appropriate: http://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary

#for i, c in enumerate('tease'):
#    newkey = c+str(i+1)
#    if newkey in children_PS:
#        children_PS[newkey] += 2.00
#    else:
#        children_PS[newkey] = 2.00
#        print(children_PS[newkey])
    
# Testing: I have a list of words and associated logfreqs. I want to add them to the dictionary

#testing_words = ['hat', 'hit', 'cat', 'bag']
#testing_logfreq = [2, 3.1, 1.5, 10]

#for word in testing_words:
    #word_index = testing_words.index(word)
    #logfreq = testing_logfreq[word_index]
    #for i, c in enumerate(word):
        #newkey = c+str(i+1)
        #if newkey in children_PS:
            #children_PS[newkey] += logfreq
        #else:
            #children_PS[newkey] = logfreq
        #print(word)
        #print(newkey)
        #print(children_PS[newkey])
        
# Testing: now with our corpus: float: http://stackoverflow.com/questions/1094717/convert-a-string-to-integer-with-decimal-in-python

#for word in children_words:
    #word_index = children_words.index(word)
    #logfreq = children_logfreq[word_index]
    #for i, c in enumerate(word):
        #newkey = c+str(i+1)
        #if newkey in children_PS:
            #children_PS[newkey] += float(logfreq)
        #else:
            #children_PS[newkey] = float(logfreq)
        #print(word)
        #print(newkey)
        #print(children_PS[newkey])

# For each word, cycle through each phoneme, add logfreq(word) to array at that position :: phoneme cell


## Biphone frequency initial calculation

# Set up 2xn array [C] for position :: biphone --> contents: logfreq(word)

# Input corpus words

# For each word, cycle through each biphone, add logfreq(word) to array at that position :: biphone cell


## Positional segment frequency return

# Set up 2xn array [B] for word :: position --> contents: PS frequency
# Must set some arbitrary upper limit on # of phonemes

# Input words from user

# Calculate PS frequency for input word
# For each word, cycle through each phoneme, retrieve cell contents from PS initial calculation array [A] and divide by sum of all cell contents across that position
# == logfreq(words having target phoneme) / logfreq(words having target position)
# Store this result in PS frequency return array [B]

# Output PS frequency
# Return a formatted PS frequency list, including sum/mean PS frequency

###

## Biphone frequency return

# Set up 2xn array [D] for word :: biphone position --> contents: biphone frequency

# Input words from user

# Calculate biphone frequency for input word
# For each word, cycle through each biphone, retrieve cell contents from biphone frequency initial calculation array [C] and divide by sum of all cell contents across that position
# == logfreq(words having target biphone) / logfreq(words having target position)
# Store this result in biphone frequency return array [D]

# Output biphone frequency
# Return a formatted biphone frequency list, including sum/mean biphone frequency

###

## Neighborhood density initial calculation

# Set up a list of all possible phonemes

# Input words from user

# For each word, cycle through each of the following processes, saving result of that process in a list

# 1. Addition: cycle through each position, adding each of the possible phonemes around that position (before and after for initial position, after only for all others)
# 2. Deletion: cycle through each position, deleting a phoneme
# 3. Substitution: cycle through each position, changing it to any dissimilar phoneme

# Compare the resultant list to the corpus list, counting up and storing matches

# Output neighbors and number of neighbors
