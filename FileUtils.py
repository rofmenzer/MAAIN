import pickle

class FileUtils(object):
    

    @staticmethod
    def createStopWords():
        file1 = open('stop_words_french.txt', 'r')
        Lines = file1.readlines()
        stop_wordsList = []
        for line in Lines:
            stop_wordsList.append(line.strip())
        return stop_wordsList
    
    @staticmethod
    def write(obj, name):
        pickle.dump( obj, open('../dump/' + name +'.p', "wb" ) )

    @staticmethod
    def read(name):
        return pickle.load( open('../dump/' + name +'.p', "rb" ) )
