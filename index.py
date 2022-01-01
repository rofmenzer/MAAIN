#!/usr/bin/env python3
# coding: utf-8

import cgi
from FileUtils import FileUtils
from Freq import Freq
from Parser import Parser



freq = Freq()
parser = Parser()

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")


html = """<!DOCTYPE html>
<head>
    <title>Moteur de recherche</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

</head>
<body>


<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    
    <form action="/index.py" method="post" class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" name="name"  />
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form> 

  </div>
</nav>





<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

</body>
</html>
"""

print(html)

"""
for i in range(5):
    if(form.getvalue("name") != None):
        print(form.getvalue("name") + '\n')
"""

requete = form.getvalue("name")
if(requete != None):
    requete = parser.stemme(parser.tokenize_text(requete))


    titles = FileUtils.read('titles') ## most frequent 100 words (term frequency of words in the corpus)
    dictionary = FileUtils.read('dictionary') ## most frequent 100 words (term frequency of words in the corpus)
    mot_page = FileUtils.read('mot_page')
    norms = FileUtils.read('norms')
    idf = FileUtils.read('idf')
    page_rank = FileUtils.read('page_rank')
    
    
    req_pages = freq.intersection(mot_page, page_rank, requete)

    #2. get idf of words
    result = freq.calcul(mot_page ,idf, requete, req_pages, page_rank, norms)

    url_prefix = 'https://fr.wikipedia.org/wiki/'
    print('<ul class="list-group">')
    
    for r in range(len(result)):
        print('<li class="list-group-item">')
        url =url_prefix + titles[result[r]].replace(' ', '_')
        print('<a target="_blank" href="' + url + '">' + titles[result[r]] + '</a>')
        print('</li>')

    print('</ul>')