import numpy as np
from sklearn.metrics import jaccard_similarity_score


with open('text1.txt', 'r') as myfile:
    text1=myfile.read().replace('\n', ' ').split()

with open('text2.txt', 'r') as myfile:
    text2=myfile.read().replace('\n', ' ').split()

with open('text3.txt', 'r') as myfile:
    text3=myfile.read().replace('\n', ' ').split()

# print text1
# exit()
print jaccard_similarity_score(text1, text2)

print jaccard_similarity_score(text1, text2, normalize=False)