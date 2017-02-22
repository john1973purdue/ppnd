# Note: to open this in python shell: exec(open('SpanPPND.py').read())

# Loading corpus words: https://pythonprogramming.net/reading-csv-files-python-3/

# Special spelling cases: double letters (ll, rr), ü vs u (gue, que vs. güe, qüe), ch, ??
# These need to be coded differently, or we need to handle them internally

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
                    

# PS / B / ND return

input_word = input("Enter one word: ")

print("Positional segment frequency")

PS_avg = 0

for i, c in enumerate(input_word):
    newkey = c+str(i+1)
    print(newkey)
    if newkey in children_PS:
        print(children_PS[newkey]/children_P1[i])
        PS_avg += children_PS[newkey]/children_P1[i]
    else:
        print("N/A")
    
print("Positional segment frequency average")
 
print(PS_avg/len(input_word))

print("Biphone frequency")

B_avg = 0

for i, c in enumerate(input_word):
    if len(input_word) != 1:
        if len(input_word) != i+1:
            newkey = c+input_word[i+1]+str(i+1)
            print(newkey)
            if newkey in children_B:
                print(children_B[newkey]/children_P2[i])
                B_avg += children_B[newkey]/children_P2[i]
            else:
                print("N/A")
    else:
        print("No biphone frequency")
        
print("Biphone frequency average")
 
print(B_avg/len(input_word))

print("Neighborhood density")

# ND candidate generation

# Possible phonemes

phonemes = ('a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú', 'y', 'ñ', 'b', 'c', 'C', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'L', 'm', 'n', 'p', 'q', 'r', 'R', 's', 't', 'v', 'w', 'x', 'z')

# For each word, cycle through each of the following processes, searching through the wordlists and adding up matches

# 1. Addition: cycle through each position, adding each of the possible phonemes around that position (before and after for initial position, after only for all others)
# 2. Deletion: cycle through each position, deleting a phoneme
# 3. Substitution: cycle through each position, changing it to any dissimilar phoneme

matches = 0

for j in phonemes:
    #print(j)
    for i, c in enumerate(input_word):
        #print(i)
        newword_addition = input_word[:i]+j+input_word[i:]
        #print(newword_addition)
        if i+1 == len(input_word):
            newword_addition = input_word[:i+1]+j
            #print(newword_addition)
            ## look for matches
        if j != input_word[i]:
            if i == 0:
                    newword_substitution = j+input_word[i+1:]
                    # look for matches
            else:
                newword_substitution = input_word[:i]+j+input_word[i+1:]
                # look for matches
            #print(newword_substitution)
       

for i, c in enumerate(input_word):
    #print(i)
    if i == 0:
        newword_deletion = input_word[i+1:]
        # look for matches
    else:
        newword_deletion = input_word[:i]+input_word[i+1:]
        # look for matches
    #print(newword_deletion)

#### NOTES/TESTING BELOW:
    
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
