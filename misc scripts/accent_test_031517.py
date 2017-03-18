wordlist = ["es.kon'de.mos","po'nia.mos","po'nia.mos"]
vowels = ["a","e","i","o","u","A","E","I","O","U"]
changed_words = []
output = []

stress = False

for word in wordlist:
    for i, c in enumerate(list(word)):
        if stress:
            if c in vowels:
                output.append(c.upper())
                stress = False
            else:
                output.append(c)
        else:
            output.append(c)
        if c == "'":
            stress = True
    changed_words.append("".join(output))
    output = []
    
print(changed_words)

# Moving accents: need to return all possible stress versions except for the one entered
# (1): store word in temp with all vowels lowercase
# (2): when encountering a vowel, uppercase, add to list but don't change temp word
# (3): before adding to list, make sure candidate word is not the same as input word

def move_accent(word):
    
    accentlist = []
    stressoutput = []
   
    for i, c in enumerate(list(word)):
        if c in vowels:
            stressoutput.append(c.lower())
        else:
            stressoutput.append(c)
    wordtemp = "".join(stressoutput)
    print(wordtemp)
    stressoutput = []
    
    for i, c in enumerate(list(wordtemp)):
        if c in vowels:
            if wordtemp[:i]+c.upper()+wordtemp[i+1:] != word:
                accentlist.append(wordtemp[:i]+c.upper()+wordtemp[i+1:])
    
    return accentlist

for word in changed_words:
    print(move_accent(word))  
