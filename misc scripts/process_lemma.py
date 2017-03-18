## Process lemma information

import json

lemmas = {} 

with open("lemmas_adults_030117_recoded.txt") as f:
    for line in f:
        lemma_temp = {}
        lemma_temp = json.loads(line)
        lemmas[lemma_temp["form"]] = {}
        lemmas[lemma_temp["form"]]["lemma"] = lemma_temp["lemma"]
        lemmas[lemma_temp["form"]]["ctag"] = lemma_temp["ctag"]
        print(lemmas[lemma_temp["form"]])

with open("lemmas_adults_030117_processed.txt", "w") as f:
    for word in lemmas:
        f.write(word+"\t"+lemmas[word]["lemma"]+"\t"+lemmas[word]["ctag"]+"\n")


