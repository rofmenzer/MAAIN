from Freq import Freq
from FileUtils import FileUtils


freq = Freq()


data = FileUtils.read('data')
#titles = FileUtils.read('titles')

#print(data[0])
dictionary = FileUtils.read('dictionary') ## most frequent 100 words (term frequency of words in the corpus)
#print(dictionary)
mot_page = FileUtils.read('mot_page')
#print(mot_page)

norms = FileUtils.read('norms')
#print(norms)


idf = FileUtils.read('idf')

v = FileUtils.read('page_rank')
#print(v)


#1. requete (3 mots (m1,m2,m3))
requete = "musique mélodie chant"
req_pages = freq.intersection(mot_page, v, requete)
print(req_pages)

#2. get idf of words
resultat = freq.calcul(mot_page ,idf, requete, req_pages, v, norms)

print(resultat)
#3.

for s in resultat:
    print(data[s]['title'])   
    #print(titles[s])
