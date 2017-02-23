# Note: to open this in python shell: exec(open('SpanPPND.py').read())

## To do: clean up the ND candidate return code so that it returns the candidate from the function in addition to 0 or 1, puts them into a list, and then outputs them later in a nice list
## To do: make final decisions about how to treat different characters, code this in our calculator:
    ### For c and g, look ahead one position and then categorize as theta, k, x, or g
    ### For ll and rr, look ahead one position and then categorize as L or R
    ### For ch, look ahead.... categorize as C
    ### For h, delete it
    ### For ü, this should be taken care of in g code
    ### For x, change to ks or x or h...
        ### We need a list of x-words
## To do: right now, the calculator is only partially aware of stress and that's when an accented vowel is in a word; otherwise, it does not take stress into account; is this good? Also, accented vowels might in some sense 'throw off' the calculations for PP/ND... Possibly we could disregard stress for PP but include it for ND?
## To do: make sure that when searching for ND matches, the matches are case-sensitive [will matter when we change our corpus to our final encoding]
## To do: find a list of representative Spanish words that both children and adults would likely know for comparing PP/ND (similar to Storkel & Hoover, 2010, p. 500)

## In process:
## To do: reformat the PP/ND return code so that it returns a standardized dictionary format that can later be used to create tables [see section below for details]
## To do: format the output in tables
        # Trying to use tabulate to format the tables, but they're coming out looking terrible and weird:
        
            #╒═════╤═════╤═════╤═════╕
            #│ 1   │ 2   │ 3   │ 4   │
            #╞═════╪═════╪═════╪═════╡
            #│ 0   │ 0   │ 0   │ 0   │
            #├─────┼─────┼─────┼─────┤
            #│ .   │ .   │ .   │ .   │
            #├─────┼─────┼─────┼─────┤
            #│ 0   │ 2   │ 0   │ 1   │
            #├─────┼─────┼─────┼─────┤
            #│ 7   │ 0   │ 4   │ 6   │
            #├─────┼─────┼─────┼─────┤
            #│ 0   │ 9   │ 5   │ 7   │
            #├─────┼─────┼─────┼─────┤
            #│ 3   │ 5   │ 8   │ 9   │
            #├─────┼─────┼─────┼─────┤
            #│ 5   │ 0   │ 2   │ 0   │
            #├─────┼─────┼─────┼─────┤
            #│ 3   │ 8   │ 5   │ 9   │
            #├─────┼─────┼─────┼─────┤
            #│ 8   │ 0   │ 2   │ 0   │
            #├─────┼─────┼─────┼─────┤
            #│ 9   │ 6   │ 6   │ 6   │
            #├─────┼─────┼─────┼─────┤
            #│ 4   │ 7   │ 4   │ 7   │
            #├─────┼─────┼─────┼─────┤
            #│ 0   │ 6   │ 3   │ 1   │
            #├─────┼─────┼─────┼─────┤
            #│ 4   │ 5   │ 8   │ 5   │
            #├─────┼─────┼─────┼─────┤
            #│ 8   │ 0   │ 8   │ 8   │
            #├─────┼─────┼─────┼─────┤
            #│ 5   │ 7   │ 7   │ 5   │
            #├─────┼─────┼─────┼─────┤
            #│ 7   │ 8   │ 1   │ 8   │
            #├─────┼─────┼─────┼─────┤
            #│ 9   │ 7   │ 9   │ 7   │
            #├─────┼─────┼─────┼─────┤
            #│ 2   │ 4   │ 6   │ 1   │
            #├─────┼─────┼─────┼─────┤
            #│     │ 2   │ 4   │ 4   │
            #╘═════╧═════╧═════╧═════╛
            
        # PrettyTable is also promising, and allows us to build up tables one row at a time: https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki
        
## Elizabeth: ## To do: write something to export PP/ND values to CSV file for later analysis
## Make a function that can expect a dictionary as input in the following form:
## input_dictionary = {'Word': ['word'], 'PS_phonemes': ['m', 'a', 'm', 'a'], 'PS': [1.2, 2.2, 3.3, 3.4], 'Biphones': ['ma', 'am', 'ma'], 'B': [1.5, 2.5, 3.5], 'ND_children': ['mami', 'nama'], 'ND_children_num': [2], 'ND_adults': ['mami', 'nama', 'mapa'], 'ND_adults_num': [3]}.
## And from this information export a csv file 

## Complete:
## To do: make the PP/ND return code loop over a list of words provided by the user


# Loading corpus words: https://pythonprogramming.net/reading-csv-files-python-3/

import csv

# Table output: https://pypi.python.org/pypi/tabulate
#from tabulate import tabulate

f = open('children_forimport_022117.csv')
csv_children = csv.reader(f, delimiter=',')

children_words = []
children_logfreq = []

for row in csv_children:
    children_lf = row[0]
    children_w = row[1]
    children_logfreq.append(children_lf)
    children_words.append(children_w)

f = open('adults_forimport_022117.csv')
csv_adults = csv.reader(f, delimiter=',')

adults_words = []
adults_logfreq = []

for row in csv_adults:
    adults_lf = row[0]
    adults_w = row[1]
    adults_logfreq.append(adults_lf)
    adults_words.append(adults_w)
    
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
        print('Children: '+candidate)
    return matches

def find_matches_adults(candidate):
    matches = 0
    if candidate in adults_words:
        matches = 1
        print('Adults: '+candidate)
    return matches

# PS / B / ND return

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

# It might be best to then take this output and add it to a dictionary of dictionaries to collate the output for all the user's words: https://www.quora.com/In-Python-can-we-add-a-dictionary-inside-a-dictionary-If-yes-how-can-we-access-the-inner-dictionary-using-the-key-in-the-primary-dictionary

# Therefore, let's change our output dictionary format to this: test = {'PS_phonemes': ['m', 'a', 'm', 'a'], 'PS': [1.2, 2.2, 3.3, 3.4], 'Biphones': ['ma', 'am', 'ma'], 'B': [1.5, 2.5, 3.5], 'ND_children': ['mami', 'nama'], 'ND_children_num': [2], 'ND_adults': ['mami', 'nama', 'mapa'], 'ND_adults_num': [3]}. Note that the word no longer appears.

# This allows us to add other entries as needed with the key being the word. We will need to check for collisions in keys. If there is a collision, rather than dropping, just have the dictionary refer to the identical entry and then use that entry to later populate the lines in the output table. Use some sort of code dummy variable to indicate to the table function that it needs to copy from another entry.

# After our function returns the dictionary, we must add it to a global dictionary of dictionaries that collects all the output for each word, using the input_word as the key: collated_output[input_word] = //returned dictionary//. This will be done outside the function.

# Then, we will use the dictionary of dictionaries to create a table that lays out all of the information for all the words in a consistent manner amenable to copying and pasting.

def return_values(input_word):
    
    return_dict = {}
    
    print("****************************************")
    
    print("Word: "+input_word)
    
    print("Positional segment frequency")

    PS_sum = 0
    
    #PS_dict = {}
    
    # Desired structure of dictionary: {[positionkey]: [PS1 etc.]}

    for i, c in enumerate(input_word):
        newkey = c+str(i+1)
        if newkey in children_PS:
            print(newkey+": "+str(round(children_PS[newkey]/children_P1[i],6)))
            #PS_table.append(str(children_PS[newkey]/children_P1[i]))
            #PS_dict[i+1] = str(children_PS[newkey]/children_P1[i])
            PS_sum += children_PS[newkey]/children_P1[i]
        else:
            print(newkey+": N/A")
            #PS_table.append("N/A")
            #PS_dict[i+1] = "N/A"
            
    #print(tabulate(PS_dict,headers="keys",tablefmt="fancy_grid"))
            
    print("Positional segment frequency sum: "+str(round(PS_sum,6)))

    #print(PS_sum)
        
    print("Positional segment frequency average: "+str(round(PS_sum/len(input_word),6)))
    
    #print(PS_sum/len(input_word))

    print("Biphone frequency")

    B_sum = 0
    
    B_table = [input_word]

    for i, c in enumerate(input_word):
        if len(input_word) != 1:
            if len(input_word) != i+1:
                newkey = c+input_word[i+1]+str(i+1)
                if newkey in children_B:
                    print(newkey+": "+str(round(children_B[newkey]/children_P2[i],6)))
                    #B_table.append(children_B[newkey]/children_P2[i])
                    B_sum += children_B[newkey]/children_P2[i]
                else:
                    print(newkey+": N/A")
                    #B_table.append("N/A")
        else:
            print("No biphone frequency")
            #B_table.append("N/A")
            
    #print(tabulate(B_table,headers=["Word","B1","B2","B3","B4","B5","B6","B7","B8","B9"],tablefmt="fancy_grid",floatfmt=".4f"))
    
    print("Biphone frequency sum: "+str(round(B_sum,6)))

    #print(B_sum)
            
    if len(input_word) > 1:
        print("Biphone frequency average: "+str(round(B_sum/(len(input_word)-1),6)))
    else:
        print("Biphone frequency average: N/A")

    print("Neighborhood density")

    # ND

    # Possible phonemes

    phonemes = ('a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú', 'y', 'ñ', 'b', 'c', 'C', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'L', 'm', 'n', 'p', 'q', 'r', 'R', 's', 't', 'v', 'w', 'x', 'z')

    # For each word, cycle through each of the following processes, searching through the wordlists and adding up matches

    # 1. Addition: cycle through each position, adding each of the possible phonemes around that position (before and after for initial position, after only for all others)
    # 2. Deletion: cycle through each position, deleting a phoneme
    # 3. Substitution: cycle through each position, changing it to any dissimilar phoneme

    matches_children = 0
    matches_adults = 0
    
    # A change here to add candidates to the dictionary by testing on value of the find_matches functions is necessary to implement the overall change to the return_values function

    for j in phonemes:
        for i, c in enumerate(input_word):
            newword_addition = input_word[:i]+j+input_word[i:]
            matches_children += find_matches_children(newword_addition)
            matches_adults += find_matches_adults(newword_addition)
            if i+1 == len(input_word):
                newword_addition = input_word[:i+1]+j
                matches_children += find_matches_children(newword_addition)
                matches_adults += find_matches_adults(newword_addition)
            if j != input_word[i]:
                if i == 0:
                    newword_substitution = j+input_word[i+1:]
                    matches_children += find_matches_children(newword_substitution)
                    matches_adults += find_matches_adults(newword_substitution)
                else:
                    newword_substitution = input_word[:i]+j+input_word[i+1:]
                    matches_children += find_matches_children(newword_substitution)
                    matches_adults += find_matches_adults(newword_substitution)

    for i, c in enumerate(input_word):
        if i == 0:
            newword_deletion = input_word[i+1:]
            matches_children += find_matches_children(newword_deletion)
            matches_adults += find_matches_adults(newword_deletion)
        else:
            newword_deletion = input_word[:i]+input_word[i+1:]
            matches_children += find_matches_children(newword_deletion)
            matches_adults += find_matches_adults(newword_deletion)

    print('# of neighbors (children): '+str(matches_children))

    print('# of neighbors (adults): '+str(matches_adults))

    return

# User input

user_input = input("Enter space-separated list of words: ")
user_input_list = user_input.split(' ')

for word in user_input_list:

#This is where we will add up our collated_output dictionary of dictionaries
    return_values(word)

#### NOTES/TESTING BELOW:

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
