
import wptools
import re
import pprint
import csv
from bs4 import BeautifulSoup
import requests


# create movie dictionary

movies = []
outfile = "movies_2018b.csv"

j = 0
with open(outfile, 'wb') as output_file:
    keys = ['year','wiki_ref','wiki_query','producer','distributor','name','country','director','cinematography','editing', 
            'studio','budget','gross','runtime','music','writer','starring','language', 'released']
                        
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()


    for y in range(0,17):
        year = str(2000 + y)  # get movvies from 1970 to 2018
        movie_page = "https://en.wikipedia.org/wiki/%s_in_film" % year
        #movie_page = "https://en.wikipedia.org/wiki/List_of_American_films_of_%s" % year
        print movie_page

        page = requests.get(movie_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.findAll('title')

        #print page.content
        #import sys
        #sys.exit()

 
        # get the list of movies from that year in wiki table
        #tables = soup.find_all(class_='wikitable sortable')   

        tables = soup.find_all(class_='wikitable') 
    
            

        # for each movie in the table, look it up on wikipedia, grab it's infobox data
        for item in tables:
            for td in item.findAll('td'): 
                for i in td.findAll('i'): 
                    for a in td.findAll('a'): 
                        movie = {}
                        movie['year'] = year
                        movie['wiki_ref'] = a['href']
                        movie['wiki_query'] = re.sub(r'\/wiki\/', '', a['href'])
                        page = wptools.page(movie['wiki_query']) # now got to the wiki page associated with the wiki link #use wptools
                
                        try: 
                         page.get_parse()
                        except:
                            print "%s movie data not found" % movie['wiki_query'] 
                            break
                        try:
                            movie['producer'] =  page.data['infobox']['producer'].encode('utf-8').strip()
                        except:
                            print "no editor data"
                        try:
                            movie['distributor'] =  page.data['infobox']['distributor'].encode('utf-8').strip()
                        except:
                            print "no distributor data"
                        try:
                            movie['name'] =  page.data['infobox']['name'].encode('utf-8').strip()
                        except:
                            print "no name data"
                        try:
                            movie['country'] =  page.data['infobox']['country'].encode('utf-8').strip()
                        except:
                            print "no country data"
                        try:
                            movie['director'] =  page.data['infobox']['director'].encode('utf-8').strip()
                        except:
                            print "no director data"
                        try:
                            movie['cinematography'] =  page.data['infobox']['cinematography'].encode('utf-8').strip()
                        except:
                            print "no cinematography data"
                        try:
                            movie['editing'] =  page.data['infobox']['editing'].encode('utf-8').strip()
                        except:
                            print "no editor data"
                        try:
                            movie['studio'] =  page.data['infobox']['studio'].encode('utf-8').strip()
                        except:
                            print "no studio found"
                        try:
                            movie['released'] =  page.data['infobox']['released'].encode('utf-8').strip()
                        except:
                            print "no released data"
                        try:
                            movie['budget'] =  page.data['infobox']['budget'].encode('utf-8').strip()
                        except:
                            print "no budget data"
                        try:
                            movie['gross'] =  page.data['infobox']['gross'].encode('utf-8').strip()  # box office
                        except:
                            print "no gross data"
                        try:
                            movie['runtime'] =  page.data['infobox']['runtime'].encode('utf-8').strip()
                        except:
                            print "no runtime data"
                        try:
                            movie['music'] =  page.data['infobox']['music'].encode('utf-8').strip()
                        except:
                            print "no music data"
                        try:
                            movie['writer'] =  page.data['infobox']['writer'].encode('utf-8').strip()
                        except:
                            print "no writer data"
                        try:
                            movie['starring'] =  page.data['infobox']['starring'].encode('utf-8').strip()
                        except:
                            print "no starring data"
                        try:
                            movie['language'] =  page.data['infobox']['language'].encode('utf-8').strip()
                        except:
                            print "no language data"


                        print movie
                        movies.append(movie)
                        
                        dict_writer.writerow(movie)

                        #import sys
                        #sys.exit()
                                       
                        
                        j = j + 1

print "processed %s films" % j
                
