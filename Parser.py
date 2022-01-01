
import nltk

import xml.etree.ElementTree as ET
import re
import itertools
import time


from nltk import word_tokenize
from nltk.stem import SnowballStemmer

from FileUtils import FileUtils

class Parser(object):


    def read_parse(self, fileName):
        """
        Read xml file and parse it
        Filter by theme(Music)

        """
        # theme word list
        """ TO-DO
        -match the exact word (done)
        -number of matched words (>1)
        """
        data = []
        titles = []
        pageId = 0


        for event, elem in ET.iterparse(fileName):   #, events=("start","end")     
            #tag = re.search('(?<=})(.*)', elem.tag).group()
            tag = elem.tag
            if (tag == 'title' and event == 'end' and elem.text is not None):
                title = elem.text
                #print(title)
            if (tag == 'text' and event == 'end' and elem.text is not None):
                text = elem.text
                #print(pageId)
                
                data.append({'id':pageId, 'title': title, 'words': title + ' ' + text})
                titles.append(title)
                pageId = pageId + 1
                    
            elem.clear() # Free memory
                    
        return (data, titles)

    def read_parse2(self, fileName):
        """
        Read xml file and parse it
        Filter by theme(Music)

        """
        # theme word list
        """ TO-DO
        -match the exact word (done)
        -number of matched words (>1)
        """
        theme = ['musique', 'mélodie', 'orchestre', 'partition', 'chant', 'musicien', 'musical','compositeur','opéra','disque','tube','enregistrement', 'refrain', 'mélodie', 'chant',
                'chanson', 'symphonie', 'cassette', 'bande', 'rengaine', 'air', 'ritournelle', 'romance', 'récital', 'concert', 'aubade', 'sérénade', 'accord', 'harmonie', 'rythme',
                'cadence', 'chœur', 'orchestre', 'couplet', 'berceuse', 'solfège', 'soprano', 'hymne', 'cantique', 'ténor', 'basse', 'baryton', 'cantatrice', 'opéra',
                'sonate', 'chantonner', 'chanter', 'fredonner'] 

        pageId = 0
        total = 0
        # result file
        output_root = ET.Element("mediawiki")


        for event, elem in ET.iterparse(fileName):   #, events=("start","end")     
            #tag = re.search('(?<=})(.*)', elem.tag).group()
            tag = elem.tag
            if (tag == 'title' and event == 'end' and elem.text is not None):
                title = elem.text
                total = total + 1
            if (tag == 'text' and event == 'end' and elem.text is not None):
                text = elem.text
                
                # filter theme (if one of the theme words exists --> accept the page)                
                i = 0
                occurence = 0
                while(i < len(theme)):
                    occurence += len(re.findall(r'\b({0})\b'.format(theme[i]), text))            
                    i = i + 1    

                if(occurence > 3): #
                    print(pageId)                    
                    output_page = ET.SubElement(output_root, "page")

                    ET.SubElement(output_page, "id").text = str(pageId)
                    ET.SubElement(output_page, "title").text = str(title)
                    ET.SubElement(output_page, "text").text = str(title + ' ' + text)
                    pageId = pageId + 1

                    #tree = ET.ElementTree(output_root)
                    #tree.write("corpus.xml")

            elem.clear() # Free memory

                    

        tree = ET.ElementTree(output_root)
        tree.write("corpus.xml")
        output_page.clear()
        output_root.clear()
        print('-------------------')        
        print(total)
        print(pageId)

    
    def clean_data(self, data, titles):
        """
        Apply regular expressions to clean text
        """
        accent = ['é', 'è', 'ê', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
        sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']

        for i in range(len(data)):      

            """
                Before cleaning the text, identify the intern links
                Keep the intersection between the present titles and links
            """
            data[i]['links'] = list(set(re.findall(r'\[\[(.*?)\]\]', data[i]['words'])) & set(titles))
            
            #temp = list(titles)
            #temp.remove(data[i]['title'])
            #data[i]['links'] = list(filter_links(list(re.findall(r'\[\[(.*?)\]\]', data[i]['words'])), list(temp)))

            #print(len(data[i]['links']), data[i]['title'], data[i]['links'])
            data[i]['words'] = data[i]['words'].replace('\n', ' ') # remove line return
            data[i]['words'] = data[i]['words'].lower() # to lowercase    
            data[i]['words'] = re.sub('[0-9_]', '', data[i]['words']) # remove numbers (!!!!!! (dates))
            data[i]['words'] = re.sub(r"\b[a-zA-Z]\b", "", data[i]['words']) # numbers single chars
            data[i]['words'] = re.sub(r"\b[a-zA-Z][a-zA-Z]\b", "", data[i]['words']) # numbers double chars   
            data[i]['words'] = re.sub(r'\bx\w+', '', data[i]['words']) # word starting with x"""
            data[i]['words'] = re.sub('http\S+\s*', ' ', data[i]['words'])  # remove URLs
            data[i]['words'] = re.sub('RT|cc', ' ', data[i]['words'])  # remove RT and cc
            data[i]['words'] = re.sub('#\S+', '', data[i]['words'])  # remove hashtags (!!!!!)
            data[i]['words'] = re.sub('@\S+', '  ', data[i]['words'])  # remove mentions 
            data[i]['words'] = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', data[i]['words'])  # remove punctuations        
            data[i]['words'] = re.sub('\s+', ' ', data[i]['words'])  # remove extra whitespace
            for j in range(len(accent)):
                data[i]['words'] = data[i]['words'].replace(accent[j], sans_accent[j]) # remove accents
        
            
            data[i]['words'] = self.stemme(self.tokenize_text(data[i]['words'])) # tokenize and stemm           

        return data




    
    def tokenize_text(self, text):
        """
            1- Tokenize the text (text --> words)
            2- Remove stop words
        """
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        stop_words = nltk.corpus.stopwords.words('french')
        stop_words.extend(FileUtils.createStopWords())
        text = [w for w in tokenizer.tokenize(text) if not w in stop_words]  
        text.sort()
        return text

    
    def stemme(self, words):
        fr = SnowballStemmer('french')
        words = [fr.stem(word) for word in words]
        return words

    
    def filter_links(self, links, titles):
        filtered_links = []
        i = 0
        j = 0
        print('-----')
        while(i < len(links) and j < len(titles)):
            links[i] = re.sub('\|\S+\s*', '', links[i])

            nbr = len(re.findall(r'\b({0})\b'.format(titles[j]), links[i]))  
            
            if(nbr != 0):
            #if(titles[j] == links[i]):
                filtered_links.append(titles[j])
                #print(titles[j], links[i])
                i = i + 1
                j = j + 1
            else:
                i = i + 1

        return filtered_links
