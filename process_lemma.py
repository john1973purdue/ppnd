## Process lemma information

import json

child_lemmas = {} 

with open("lemmas_children.txt") as f:
    for line in f:
        lemma_temp = {}
        lemma_temp = json.loads(line)
        child_lemmas[lemma_temp["form"]] = {}
        child_lemmas[lemma_temp["form"]]["lemma"] = lemma_temp["lemma"]
        child_lemmas[lemma_temp["form"]]["ctag"] = lemma_temp["ctag"]
        print(child_lemmas[lemma_temp["form"]])

with open("lemmas_children_processed.txt", "w") as f:
    for word in child_lemmas:
        f.write(word+"\t"+child_lemmas[word]["lemma"]+"\t"+child_lemmas[word]["ctag"]+"\n")


