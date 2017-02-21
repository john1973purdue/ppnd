# Loading corpus words

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



######

## Positional segment frequency initial calculation

# Set up 2xn array [A] for position :: phoneme --> contents: logfreq(word)

# Input corpus words

# For each word, cycle through each phoneme, add logfreq(word) to array at that position :: phoneme cell


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

## Biphone frequency initial calculation

# Set up 2xn array [C] for position :: biphone --> contents: logfreq(word)

# Input corpus words

# For each word, cycle through each biphone, add logfreq(word) to array at that position :: biphone cell


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
