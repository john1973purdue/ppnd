# Spanish PP/ND calculator (05/01/17)

import csv
import math
from multiprocessing import Process, Queue
import random

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
            
            key_reform = key.split(';')[0]
                                    
            word = (key_reform[:7] + '...') if len(key_reform) > 10 else key_reform
            
            output_line='{0: <10}'.format(word)+"\t"+'{0: <10}'.format(str(len(key_reform)))+"\t"+PS_output_line+'{0: <10}'.format(collated_output[age][key]['PS_sum'])+"\t"+'{0: <10}'.format(collated_output[age][key]['PS_avg'])+"\t"+B_output_line+'{0: <10}'.format(collated_output[age][key]['B_sum'])+"\t"+'{0: <10}'.format(collated_output[age][key]['B_avg'])+"\t"+'{0: <10}'.format(collated_output[age][key]['ND'])+"\t"+neighbors_output_line
            
            f.write(output_line+"\n")
    return

if __name__=='__main__':
    
    # User input

    user_input = input("Enter space-separated list of words: ")
    user_input_list = user_input.split(' ')
        
    # Init calc

    init_dict['Children'] = init_calc('Children')
    init_dict['Adults'] = init_calc('Adults')
    
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

    for word in user_input_list:
        
        if len(word) != 0:
        
            if word in collated_output['Children']:
                collated_output['Children'][word+';'+str(random.random())] = collated_output['Children'][word]
            else:
                collated_output['Children'][word] = return_values(word, 'Children')
            
            if word in collated_output['Adults']:
                collated_output['Adults'][word+';'+str(random.random())] = collated_output['Adults'][word]
            else:
                collated_output['Adults'][word] = return_values(word, 'Adults')
            
    # Write table

    with open("output.txt", "w") as f:
        f.write("Children\n")

    table('Children')

    with open("output.txt", "a") as f:
        f.write("Adults\n")

    table('Adults')
