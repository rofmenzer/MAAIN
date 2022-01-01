import itertools
import math
from nltk.stem import SnowballStemmer

class Freq(object):

    
    def global_term_frequency(self, data, limit): # todo- add log
        tf = {}
        for page in data:
            for word in page['words']:
                if(word not in tf):
                    tf[word] = 1
                else:
                    tf[word] = tf[word] + 1
            
        tf = {k: v for k, v in sorted(tf.items(), key=lambda item: item[1] , reverse=True)} # sort frequencies (desc)

        return (dict(itertools.islice(tf.items(), limit))) #subset

    def extract_dictionary(self, data, limit): # todo- add log
        tf = {}
        for page in data:
            for word in page['words']:
                if(word not in tf):
                    tf[word] = 1
                else:
                    tf[word] = tf[word] + 1
            
        tf = {k: v for k, v in sorted(tf.items(), key=lambda item: item[1] , reverse=True)} # sort frequencies (desc)
        tf = dict(itertools.islice(tf.items(), limit))

        return list(tf.keys()) #subset

    def term_frequency(self, data, limit):

        tf = {}
        for page in data:
            pageDict = {}
            for word in page['words']:
                if(word not in pageDict):
                    pageDict[word] = 1
                else:
                    pageDict[word] = pageDict[word] + 1
            
            # apply log 
            for term in pageDict:
                pageDict[term] = 1 + math.log10(pageDict[term])
            # normalize tf
            pageDict = self.normalize_vector(pageDict)

            pageDict = {k: v for k, v in sorted(pageDict.items(), key=lambda item: item[1] , reverse=True)} # sort frequencies (desc)
            
            tf[page['id']] = pageDict
            
        return tf

        #return (dict(itertools.islice(tf.items(), limit))) #subset

    
    def calculate_score(self, vreq, vdoc):
        score = 0
        vreq = self.normalize_vector(vreq)
        
        for i in range(len(vreq)):
            score += vreq[i] * vdoc[i]
        return score



    def normalize_vector(self, vec):
        somme = 0
        for i in range(len(vec)):
            somme = somme + math.pow(vec[i], 2)
        
        factor = math.sqrt(somme)
        for i in range(len(vec)):
            vec[i] = vec[i] / factor

        return vec

    def inversed_index_with_occurence(self, tf, data):
        inversed_index = {}
        for term in tf:
            tempArray = []
            for page in data:
                tempDict = {}
                for word in page['words']:
                    if (term == word):
                        if (page['id'] not in tempDict):
                            tempDict[page['id']] = 1
                        else:
                            tempDict[page['id']] = tempDict[page['id']] + 1

                if (tempDict):
                    tempDict[page['id']] = format(tempDict[page['id']] / len(page['words']), '.2f')
                    tempArray.append(tempDict)
            inversed_index[term] = tempArray
        return inversed_index

    def inversed_index(self, tf, data):
        inversed_index = {}
        for term in tf:
            tempArray = []
            for page in data:
                for word in page['words']:
                    if (term == word):
                        tempArray.append(page['id'])
                        break            
            if(tempArray):
                inversed_index[term] = tempArray
        return inversed_index

    def inversed_index_with_tf(self, dictionary, data):
        

        inversed_index = {}
        for term in dictionary:
            tempDict = {}
            for page in data:
                for word in page['words']:
                    if (term == word):                        
                        if (page['id'] not in tempDict):
                            tempDict[page['id']] = 1
                        else:
                            tempDict[page['id']] = tempDict[page['id']] + 1

                if (tempDict and page['id'] in tempDict):
                    tempDict[page['id']] = 1 + math.log10(tempDict[page['id']])
                                
            
            inversed_index[term] = tempDict
        return inversed_index

    def inversed_index_with_tf2(self, dictionary, data):
        

        inversed_index = {}


        for page in data:
            #print('mot_page',page['id'])
            for word in page['words']:
                if(word in dictionary):
                    tempDict = {}
                    if(word in inversed_index):
                        tempDict = inversed_index[word]
                    
                    if (page['id'] not in tempDict):
                            tempDict[page['id']] = 1
                    else:
                            tempDict[page['id']] = tempDict[page['id']] + 1
                    
                    inversed_index[word] = tempDict
        
        for mot in inversed_index:
            for page in inversed_index[mot]:
                #print(mot, page)
                inversed_index[mot][page] = 1 + math.log10(inversed_index[mot][page])


        return inversed_index

    def calculate_norm(self, mots_page, size, dictionary):
        norms = [0] * size
        for word in mots_page:
            for page in mots_page[word]:
                #if(page == 0):
                    #print(mots_page[word][page])
                norms[page] = norms[page] + math.pow(mots_page[word][page], 2)
        for i in range(size):
            norms[i] = math.sqrt(norms[i])
        return norms


    def tf_with_log(self,tf):
        for i in tf:
            tf[i] = 1 + math.log10(tf[i])
        return tf

    def idf(self,tf, data):
        idf = {}
        for term in tf:
            tempArray = []
            idf[term] = 0
            for page in data:
                tempDict = []
                for word in page['words']:
                    if (term == word):
                        if (page['id'] not in tempDict):
                            tempDict.append(page['id'])
                            idf[term] = idf[term] + 1
            idf[term] = math.log10(len(data) / (idf[term]))
        return idf

    def idf2(self, dictionary, data):
        idf = {}

        for page in data:
            #print('idf', page['id'])
            for word in page['words']:
                if(word in dictionary):
                    if(word not in idf):
                        idf[word] = 1              
                    else: 
                        idf[word] = idf[word] + 1              

        for term in idf:
            idf[term] = math.log10(len(data) / (idf[term]))

        return idf


    def fill_line(self, data, page):
        """

        Modifier la méthode de sorte qu'on appelle la fonction CLI pour chaque ligne
        Regrouper la matrice creuse et CLI dans une seule fonction
        Modifier les id des pages (id=indice de la liste)

        """
        #line = [0] * len(page['links'])
        line = [0] * len(data)


        for i in range(len(data)):
            #if(i != j):
                if(data[i]['title'] != page['title'] and data[i]['title'] in page['links']):
                    line[i] = 1/ len(page['links']) # wrong length (must be cleaned first) (remove links)
        #print(line)
        
        return line

    def CLI(self, data):
        C = []
        L = []
        I = []
        lval = 0

        n = len(data)

        for i in range(n): # loop over pages
            
            L.append(lval)
            ival = 0
            line = self.fill_line(data, data[i])
            for j in range(len(line)):
                if(line[j] != 0):
                    C.append(line[j])
                    
                    lval = lval + 1

                    I.append(ival)
                ival = ival + 1    

        L.append(lval)

        return (C,L,I)

    def prod(self, C,L,I, V, e):
        n = len(V)
        P = [0] * n
        s = 0

        somme = 0
        for cc in range(len(V)):
            somme += V[cc]
        #print(somme)
        for i in range (0, n):
            if (L[i] == L[i+1]):
                s = s + V[i]

            for j in range (L[i], L[i+1]):
                P[I[j]] += C[j] * V[i]
        
        s = s/n
        for i in range (0, n):
            P[i] = (1-e) * (P[i] + s) + e/n

        return P

    def exec_page_rank(self, C,L,I):
        k = 50
        e = 0.15
        n = len(L) - 1
        pi = [1/n] * n
        for i in range(0, k):
            pi = self.prod(C,L,I, pi, e)
        return pi

    def intersection(self, mots_page, v, requete):
       
        # get pages of each word
        pages = []
        intersection_pages = []
        for word in requete:
            #print(fr.stem(word), list(mots_page[fr.stem(word)].keys()))
            if(word in mots_page):
                temp_pages = list(mots_page[word].keys())
                pages.append(temp_pages)
            else:
                pages.append([])
        
        if(len(pages) > 1):
            intersection_pages = set(pages[0]).intersection(*pages[1:])
        elif(len(pages) == 1):
            intersection_pages = pages[0]
        
        return list(intersection_pages)


    def quick_sort(self, pages, ranks, start, end):
        #Sorts the list from indexes start to end - 1 inclusive
        if end - start > 1:
            p = self.partition(pages, ranks, start, end)
            self.quick_sort(pages, ranks, start, p)
            self.quick_sort(pages, ranks, p + 1, end)
    
    
    def partition(self, pages, ranks, start, end):
        pivot = ranks[start]
        i = start + 1
        j = end - 1
    
        while True:
            while (i <= j and ranks[i] >= pivot):
                i = i + 1
            while (i <= j and ranks[j] <= pivot):
                j = j - 1
    
            if i <= j:
                ranks[i], ranks[j] = ranks[j], ranks[i]
                pages[i], pages[j] = pages[j], pages[i]
            else:
                ranks[start], ranks[j] = ranks[j], ranks[start]
                pages[start], pages[j] = pages[j], pages[start]
                return j

    def calcul(self,mot_page, idf, requete, pages, page_rank, tf_norms):

        alfa = 0.8
        beta = 0.2
        req_idf = []
        scores = {}

        words = requete
        # set req vector
        for word in words:
            if(word in idf):
                req_idf.append(idf[word])
        #print('idf req', req_idf)

        for page in pages:
            
            req_tf = []
            # page vector
            for word in words:
                if(word in mot_page and page in mot_page[word]):
                    req_tf.append(mot_page[word][page] / tf_norms[page])

            #print('tf_page', page, req_tf)
            
            s1 = self.calculate_score(req_idf, req_tf)
            s = alfa * s1 + beta * page_rank[page]

            scores[page] = s

        

        scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1] , reverse=True)} # sort frequencies (desc)
        print('pages totale : ',len(pages))
        return list(scores.keys())
        #return scores
