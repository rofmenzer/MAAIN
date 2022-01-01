
from Parser import Parser

import xml.etree.ElementTree as ET
import re

parser = Parser()

#(data, titles) = parser.read_parse('corpus.xml') ## Read and parse the file
#(data, titles) = parser.read_parse2('../test2.xml') ## Read and parse the file
#(data, titles) = parser.read_parse2('../frwiki-latest-pages-articles.xml') ## Read and parse the file

#print(len(titles))
#print(data[0])


parser.read_parse2('test.xml') ## Read and parse the file
