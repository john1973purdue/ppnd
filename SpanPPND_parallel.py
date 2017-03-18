# Note: to open this in python shell: exec(open('SpanPPND.py').read())

## To do: two streams -- lemma vs word-as-shown

## Justin:
## To do: matching transcriptions to the word for output in table, making sure duplicate words in user_input are duplicated in table (right now duplicates are simply dropped)
## To do: prepare final transcription guidelines


## Elizabeth: 
## To do: write something to export PP/ND values to CSV file for later analysis
## Make a function that can expect a dictionary as input in the following form:
## input_dictionary = {'mamá': {'PS_phonemes_children': ['m1', 'a2', 'm3', 'á4'], 'PS_children': ['0.070354', '0.209508', '0.045825', '0.00955'], 'PS_sum_children': '0.335237', 'PS_avg_children': '0.083809', 'PS_phonemes_adults': ['m1', 'a2', 'm3', 'á4'], 'PS_adults': ['0.066131', '0.196646', '0.045695', '0.009752'], 'PS_sum_adults': '0.318223', 'PS_avg_adults': '0.079556', 'B_avg_children': '0.01125', 'B_sum_children': '0.03375', 'B_phonemes_children': ['ma1', 'am2', 'má3'], 'B_children': ['0.019057', '0.013471', '0.001221'], 'B_avg_adults': '0.009823', 'B_sum_adults': '0.02947', 'B_phonemes_adults': ['ma1', 'am2', 'má3'], 'B_adults': ['0.017061', '0.011384', '0.001025'], 'Neighbors_children': ['mama', 'mami', 'mamás'], 'Neighbors_adults': ['mama', 'mami', 'mamás'], 'Neighbors_children_add': ['mamás'], 'Neighbors_children_sub': ['mama', 'mami'], 'Neighbors_children_del': [], 'Neighbors_adults_add': ['mamás'], 'Neighbors_adults_sub': ['mama', 'mami'], 'Neighbors_adults_del': [], 'ND_children': '3', 'ND_adults': '3'}, 'Word2': {etc.}}.
## And from this information export a csv file 
## To do: interface to website

## Complete:
## To do: make the PP/ND return code loop over a list of words provided by the user
## To do: reformat the PP/ND return code so that it returns a standardized dictionary format that can later be used to create tables [see section below for details]
## To do: clean up the ND candidate return code so that it returns the candidate from the function in addition to 0 or 1, puts them into a list, and then outputs them later in a nice list [no longer relevant]
## To do: format the output in tables --> output.txt
## To do: make final decisions about how to treat different characters: users' input will be broad transcriptions
## To do: find a list of representative Spanish words that both children and adults would likely know for comparing PP/ND (similar to Storkel & Hoover, 2010, p. 500) --> Spanish CDI
## To do: right now, the calculator is only partially aware of stress and that's when an accented vowel is in a word; otherwise, it does not take stress into account; is this good? Also, accented vowels might in some sense 'throw off' the calculations for PP/ND... Possibly we could disregard stress for PP but include it for ND?
    # Plan:
    # Initial stage of calculator: accent (=CAPITALIZE) first vowel encountered after ', then discard '/.
    # For PP: this is transparent -- just replace vowels with accented vowels in transcription
    # For ND: (1) take each word, move stressed vowel around before any substitution/addition/replacement, then look for match; (2) for each candidate word, move stressed vowel around, then look for match
    # e.g., completó: compléto, compléta, completé, compléte, compléten, complétos
        # (1) yields: compléto
        # (2) yields: ó --> a + stress search: compléta
                    # ó --> e + stress search: completé, compléte
                    # +s + stress search: complétos
## To do: update the csv reading code:
    ## 1. first pass: scan character by character, removing . and changing first vowel following ' to capitalized (=stressed) version
    ## 2. second pass: logfreq calculation: for each word in children_words[], construct dictionary of {'word': 'rawfreq'} based on matching words and then transform back to list of words and list of calculated logfreqs so that we can continue to use the same code for PS/B as before
## To do: make sure that when searching for ND matches, the matches are case-sensitive [will matter when we change our corpus to our final encoding]
## To do: using Spanish-spoken-in-Spain adult oral language corpus from Alonso, M. a, Fernandez, A., & Diez, E. (2011). Oral frequency norms for 67,979 Spanish words. Behavior Research Methods, 43(2), 449–458, create adult corpus for comparison purposes. Don't use the CLEARPOND/BuscaPalabras calculators for adult vaues because they use different transcription scheme than ours (a problem if we're comparing words based on their transcriptions) and the Alonso et al. word lists are much better, being oral data from Spain only. 
## To do: improve calculator speed if easy/possible with simple parallelism (http://chriskiehl.com/article/parallelism-in-one-line/) --> might be able to make the initial csv import code for adults/children run simultaneously, and then run the adults/children PP/ND logfreq code simultaneously, and then just do everything else sequentially
## To do: update list of phonemes to match transcription: make decisions about L vs Z vs j

import csv
import math
from multiprocessing.dummy import Pool as ThreadPool 
from multiprocessing import Process, Queue

vowels = ["a","e","i","o","u","A","E","I","O","U"]
stress = False
stressoutput = []

init_dict = {}
init_dict['Children'] = {}
init_dict['Adults'] = {}

def init_calc(age):
    
    vowels = ["a","e","i","o","u","A","E","I","O","U"]
    stress = False
    stressoutput = []
    
    words_temp = []
    rawfreq_temp = []
    
    with open("./"+age+"_031817.csv") as f:
        csv_file = csv.reader(f, delimiter=',')

        for row in csv_file:
            rawfreq_temp.append(row[1])
            w = row[4]
            
            # Encode stress
            
            for i, c in enumerate(list(w)):
                if stress:
                    if c in vowels:
                        stressoutput.append(c.upper())
                        stress = False
                    else:
                        stressoutput.append(c)
                else:
                    stressoutput.append(c)
                if c == "'":
                    stress = True
            w = "".join(stressoutput)
            stressoutput = []
            
            w = w.replace("'","")
            w = w.replace(".","")
            w = w.replace("Z","L")
            words_temp.append(w)

        freq_temp = {}    

        for word in words_temp:
            word_index = words_temp.index(word)
            rawfreq = rawfreq_temp[word_index]
            if word in freq_temp:
                freq_temp[word] += int(rawfreq)
            else:
                freq_temp[word] = int(rawfreq)
                
        words = []
        logfreq_list = []
                
        for key, val in freq_temp.items():
            words.append(key)
            logfreq_list.append(math.log10(val)+1)
            
    init_calc_dict = {}
    init_calc_dict['words'] = words
    init_calc_dict['logfreq_list'] = logfreq_list
        
    return init_calc_dict
        
            
def PS_init(age, words, logfreq_list, q):
            
    PS = {}
    
    for word in words:
        word_index = words.index(word)
        logfreq = logfreq_list[word_index]
        for i, c in enumerate(word):
            newkey = c+str(i+1)
            if newkey in PS:
                PS[newkey] += float(logfreq)
            else:
                PS[newkey] = float(logfreq)   
    
    q.put(PS)
    
    return

def B_init(age, words, logfreq_list, q):
    
    B = {}

    for word in words:
        word_index = words.index(word)
        logfreq = logfreq_list[word_index]
        for i, c in enumerate(word):
            if len(word) != 1:
                if len(word) != i+1:
                    newkey = c+word[i+1]+str(i+1)
                    if newkey in B:
                        B[newkey] += float(logfreq)
                    else:
                        B[newkey] = float(logfreq)
                        
    q.put(B)
        
    return

def P1_init(age, words, logfreq_list, q):
                               
    P1 = {}

    for word in words:
        word_index = words.index(word)
        logfreq = logfreq_list[word_index]
        for i, c in enumerate(word):
            if i in P1:
                P1[i] += float(logfreq)
            else:
                P1[i] = float(logfreq)
                
    q.put(P1)
        
    return

def P2_init(age, words, logfreq_list, q):
                
    P2 = {}

    for word in words:
        word_index = words.index(word)
        logfreq = logfreq_list[word_index]
        for i, c in enumerate(word):
            if len(word) != 1:
                if len(word) != i+1:
                    if i in P2:
                        P2[i] += float(logfreq)
                    else:
                        P2[i] = float(logfreq)
    
    q.put(P2)
                   
    return
                    
# Moving stress around: returns [words]

def move_accent(word):
    
    accentlist = []
    stressoutput = []
   
    for i, c in enumerate(list(word)):
        if c in vowels:
            stressoutput.append(c.lower())
        else:
            stressoutput.append(c)
    wordtemp = "".join(stressoutput)
    
    for i, c in enumerate(list(wordtemp)):
        if c in vowels:
            accentlist.append(wordtemp[:i]+c.upper()+wordtemp[i+1:])
    
    return accentlist
                    
# ND finding matches: returns [# of matches, [words]]

def find_matches(candidate, input_word, age):
    wordlist = []
    matches = 0
    for c in move_accent(candidate):
        if c != input_word:
            if c in init_dict[age]['words']:
                matches += 1
                wordlist.append(c)
    matchlist = [matches,wordlist]
    return matchlist

# PS / B / ND return

def return_values(input_word, age):
                
    return_dict = {}
    
    PS_sum = 0
    
    PS_phonemes_list = []
    
    PS_values_list = []

    for i, c in enumerate(input_word):
        newkey = c+str(i+1)
        if newkey in init_dict[age]['PS']:
            PS_phonemes_list.append(str(newkey))
            PS_values_list.append(str(round(init_dict[age]['PS'][newkey]/init_dict[age]['P1'][i],6)))
            PS_sum += init_dict[age]['PS'][newkey]/init_dict[age]['P1'][i]
        else:
            PS_phonemes_list.append(str(newkey))
            PS_values_list.append("N/A")
    
    return_dict['PS_phonemes']=PS_phonemes_list
    return_dict['PS']=PS_values_list
    return_dict['PS_sum']=str(round(PS_sum,6))
    return_dict['PS_avg']=str(round(PS_sum/len(input_word),6))
    
    B_sum = 0
    
    B_phonemes_list = []
    
    B_values_list = []

    for i, c in enumerate(input_word):
        if len(input_word) != 1:
            if len(input_word) != i+1:
                newkey = c+input_word[i+1]+str(i+1)
                if newkey in init_dict[age]['B']:
                    B_sum += init_dict[age]['B'][newkey]/init_dict[age]['P2'][i]
                    B_phonemes_list.append(str(newkey))
                    B_values_list.append(str(round(init_dict[age]['B'][newkey]/init_dict[age]['P2'][i],6)))
                else:
                    B_phonemes_list.append(str(newkey))
                    B_values_list.append("0")
        else:
            B_phonemes_list.append("N/A")
            B_values_list.append("N/A")
            
    if len(input_word) > 1:
        return_dict['B_avg']=str(round(B_sum/(len(input_word)-1),6))
        return_dict['B_sum']=str(round(B_sum,6))
    else:
        return_dict['B_avg']="N/A"
        return_dict['B_sum']="N/A"
        
    return_dict['B_phonemes']=B_phonemes_list
    return_dict['B']=B_values_list
        
    phonemes = ('a', 'e', 'i', 'o', 'u', 'j', 'L', 'J', 'b', 'T', 'C', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 'r', '4', 's', 't', 'v', 'w', 'x', 'z')

    matches_count = 0
    
    matches = []
    N = []
    N_add = []
    N_sub = []
    N_del = []
    ND_num = []
    
    for j in phonemes:
        for i, c in enumerate(input_word):
            newword_addition = input_word[:i]+j+input_word[i:]
            matches = find_matches(newword_addition, input_word, age)
            if matches[0] >= 1:
                matches_count += matches[0]
                for c in matches[1]:
                    N.append(c)
                    N_add.append(c)
            if i+1 == len(input_word):
                newword_addition = input_word[:i+1]+j
                matches = find_matches(newword_addition, input_word, age)
                if matches[0] >= 1:
                    matches_count += matches[0]
                    for c in matches[1]:
                        N.append(c)
                        N_add.append(c)
            if j != input_word[i]:
                if i == 0:
                    newword_substitution = j+input_word[i+1:]
                    matches = find_matches(newword_substitution, input_word, age)
                    if matches[0] >= 1:
                        matches_count += matches[0]
                        for c in matches[1]:
                            N.append(c)
                            N_sub.append(c)
                else:
                    newword_substitution = input_word[:i]+j+input_word[i+1:]
                    matches = find_matches(newword_substitution, input_word, age)
                    if matches[0] >= 1:
                        matches_count += matches[0]
                        for c in matches[1]:
                            N.append(c)
                            N_sub.append(c)

    for i, c in enumerate(input_word):
        if i == 0:
            newword_deletion = input_word[i+1:]
            matches = find_matches(newword_deletion, input_word, age)
            if matches[0] >= 1:
                matches_count += matches[0]
                for c in matches[1]:
                    N.append(c)
                    N_del.append(c)
        else:
            newword_deletion = input_word[:i]+input_word[i+1:]
            matches = find_matches(newword_deletion, input_word, age)
            if matches[0] >= 1:
                matches_count += matches[0]
                for c in matches[1]:
                    N.append(c)
                    N_del.append(c)
    
    return_dict['Neighbors']=N
    return_dict['Neighbors_add']=N_add
    return_dict['Neighbors_sub']=N_sub
    return_dict['Neighbors_del']=N_del
    return_dict['ND']=str(matches_count)

    return return_dict

def table(age):

    with open("output.txt", "a") as f:
        
        max_PS_length=0

        for key, val in collated_output[age].items():
            if len(collated_output[age][key]['PS_phonemes']) > max_PS_length:
                max_PS_length = len(collated_output[age][key]['PS_phonemes'])

        PS_columns=""

        for i in range(max_PS_length+1,1,-1):
            PS_columns = '{0: <10}'.format("PS"+str(i-1))+"\t"+PS_columns
            
        B_columns=""

        for i in range(max_PS_length,1,-1):
            B_columns = '{0: <10}'.format("B"+str(i-1))+"\t"+B_columns

        f.write('{0: <10}'.format("Word")+"\t"+'{0: <10}'.format("Length")+"\t"+PS_columns+'{0: <10}'.format("PS sum")+"\t"+'{0: <10}'.format("PS avg")+"\t"+B_columns+'{0: <10}'.format("B sum")+"\t"+'{0: <10}'.format("B avg")+"\t"+'{0: <10}'.format("ND")+"\t"+'{0: <10}'.format("Neighbors")+"\n")

        for key, val in collated_output[age].items():
            PS_output_line=""
            
            for i in range(max_PS_length,0,-1):
                if len(collated_output[age][key]['PS']) < i:
                    PS_output_line='{0: <10}'.format('--')+"\t"+PS_output_line
                else:
                    PS_output_line='{0: <10}'.format(collated_output[age][key]['PS'][i-1])+"\t"+PS_output_line
                    
            B_output_line=""
            
            for i in range(max_PS_length-1,0,-1):
                if len(collated_output[age][key]['B']) < i:
                    B_output_line='{0: <10}'.format('--')+"\t"+B_output_line
                else:
                    B_output_line='{0: <10}'.format(collated_output[age][key]['B'][i-1])+"\t"+B_output_line
                    
            neighbors_output_line=""
            
            for i, c in enumerate(collated_output[age][key]['Neighbors']):
                neighbors_output_line=collated_output[age][key]['Neighbors'][i]+' '+neighbors_output_line
                
            output_line=""
                                    
            word = (key[:7] + '...') if len(key) > 10 else key
            
            output_line='{0: <10}'.format(word)+"\t"+'{0: <10}'.format(str(len(key)))+"\t"+PS_output_line+'{0: <10}'.format(collated_output[age][key]['PS_sum'])+"\t"+'{0: <10}'.format(collated_output[age][key]['PS_avg'])+"\t"+B_output_line+'{0: <10}'.format(collated_output[age][key]['B_sum'])+"\t"+'{0: <10}'.format(collated_output[age][key]['B_avg'])+"\t"+'{0: <10}'.format(collated_output[age][key]['ND'])+"\t"+neighbors_output_line
            
            f.write(output_line+"\n")
    return

# User input

user_input = input("Enter space-separated list of words: ")
user_input_list = user_input.split(' ')

user_input_list_accented = []

for word in user_input_list:
    
    # Temporary accenting
    
    stress = False
    
    for i, c in enumerate(list(word)):
        if stress:
            if c in vowels:
                stressoutput.append(c.upper())
                stress = False
            else:
                stressoutput.append(c)
        else:
            stressoutput.append(c)
        if c == "'":
            stress = True
    word = "".join(stressoutput)
    stressoutput = []
    
    word = word.replace("'","")
    word = word.replace(".","")
    word = word.replace("Z","L")
    
    user_input_list_accented.append(word)
    

ages = ['Children','Adults']

pool = ThreadPool()

# Init calc

init_dict['Children'] = init_calc('Children')
init_dict['Adults'] = init_calc('Adults')

if __name__=='__main__':
    
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()
    q4 = Queue()
    r1 = Queue()
    r2 = Queue()
    r3 = Queue()
    r4 = Queue()
    
    a1 = Process(target = PS_init, args = ('Children', init_dict['Children']['words'], init_dict['Children']['logfreq_list'], q1))
    a2 = Process(target = B_init, args = ('Children', init_dict['Children']['words'], init_dict['Children']['logfreq_list'], q2))
    a3 = Process(target = P1_init, args = ('Children', init_dict['Children']['words'], init_dict['Children']['logfreq_list'], q3))
    a4 = Process(target = P2_init, args = ('Children', init_dict['Children']['words'], init_dict['Children']['logfreq_list'], q4))
    a1.start()
    a2.start()
    a3.start()
    a4.start()
    
    init_dict['Children']['PS'] = q1.get()
    init_dict['Children']['B'] = q2.get()
    init_dict['Children']['P1'] = q3.get()
    init_dict['Children']['P2'] = q4.get()
    
    b1 = Process(target = PS_init, args = ('Adults', init_dict['Adults']['words'], init_dict['Adults']['logfreq_list'], r1))
    b2 = Process(target = B_init, args = ('Adults', init_dict['Adults']['words'], init_dict['Adults']['logfreq_list'], r2))
    b3 = Process(target = P1_init, args = ('Adults', init_dict['Adults']['words'], init_dict['Adults']['logfreq_list'], r3))
    b4 = Process(target = P2_init, args = ('Adults', init_dict['Adults']['words'], init_dict['Adults']['logfreq_list'], r4))
    b1.start()
    b2.start()
    b3.start()
    b4.start()
    
    init_dict['Adults']['PS'] = r1.get()
    init_dict['Adults']['B'] = r2.get()
    init_dict['Adults']['P1'] = r3.get()
    init_dict['Adults']['P2'] = r4.get()
    
    a1.join()
    a2.join()
    a3.join()
    a4.join()
    b1.join()
    b2.join()
    b3.join()
    b4.join()

collated_output = {}
collated_output['Children'] = {}
collated_output['Adults'] = {}

for word in user_input_list_accented:
    collated_output['Children'][word] = return_values(word, 'Children')
    collated_output['Adults'][word] = return_values(word, 'Adults')

# Write table

with open("output.txt", "w") as f:
    f.write("Children\n")

table('Children')

with open("output.txt", "a") as f:
    f.write("Adults\n")

table('Adults')
