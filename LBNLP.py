from lbnlp.models.load.matscholar_2020v1 import load

ner_model = load("ner")
doc = " "

tags = ner_model.tag_doc(doc)

flattened_tags = []
for sentence in tags:
    flattened_tags.extend(sentence)
print(flattened_tags)