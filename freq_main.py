from Parser import Parser
from Freq import Freq
from FileUtils import FileUtils
import time



parser = Parser()
freq = Freq()


(data, titles) = parser.read_parse('../corpus.xml') ## Read and parse the file
print('read completed')
data = parser.clean_data(data, titles)
print('data clean passed')
FileUtils.write(titles, 'titles') ## write
print('titles complete')
FileUtils.write(data, 'data') ## write
print('data completed')
"""

dictionary = freq.extract_dictionary(data, 10000) ## most frequent 100 words (term frequency of words in the corpus)
#print(dictionary)
print('dictionary passed')
FileUtils.write(dictionary, 'dictionary') ## write
print('write dictionary passed')



mot_page = freq.inversed_index_with_tf2(dictionary, data)
#print(mot_page)


print('mot_page passed')
FileUtils.write(mot_page, 'mot_page') ## write
print('write mot_page passed')


norms = freq.calculate_norm(mot_page, len(data), dictionary)
#print(norms)
print('norms passed')
FileUtils.write(norms, 'norms') ## write
print('write norms passed')


idf = freq.idf2(dictionary, data)
print('idf passed')
FileUtils.write(idf, 'idf') ## write
print('write idf passed')

(C,L,I) = freq.CLI(data)
#print (C,L,I)
v = freq.exec_page_rank(C,L,I)
#print(v)
print('page_rank passed')
FileUtils.write(v, 'page_rank') ## write
print('write page_rank passed')

#1. requete (3 mots (m1,m2,m3))
requete = "musique mélodie chant"
req_pages = freq.intersection(mot_page, v, requete)
print(req_pages)

#2. get idf of words
score = freq.calcul(mot_page ,idf, requete, req_pages, v, norms)

print(score)
#3.
# """