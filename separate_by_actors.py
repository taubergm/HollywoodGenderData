import csv
import sys
reload(sys)  
sys.setdefaultencoding('UTF8')
import re
#import networkx as nx
#import matplotlib.pyplot as plt
import io

filename = sys.argv[1]



csvOutFile = "all_actors_movies.csv"
outCsv = open(csvOutFile, 'wb')
fieldnames = ['year','wiki_ref','wiki_query','producer','distributor','name','country','director','cinematography','editing','studio','budget','gross',
                    'runtime','music','writer','starring','language','released']

csv_writer = csv.DictWriter(outCsv, fieldnames=fieldnames)
csv_writer.writeheader()

i = 0
with io.open(filename, encoding='utf-8', errors='ignore') as csvfile:

    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        #print type(row[16])
    
        actors = row[16].split(",")

        #print actors
        for actor in actors:
            actor = re.sub("\[", "", actor) 
            actor = re.sub("\]", "", actor) 
            actor = re.sub("\'", "", actor) 
            actor = actor.strip()
    
            #row[16] = actor

            new_csv_row = {}

            new_csv_row['year'] = row[0]
            new_csv_row['wiki_ref'] = row[1]
            new_csv_row['wiki_query'] = row[2]
            new_csv_row['producer'] = row[3]
            new_csv_row['distributor'] = row[4]
            new_csv_row['name'] = row[5]
            new_csv_row['country'] = row[6]
            new_csv_row['director'] = row[7]
            new_csv_row['cinematography'] = row[8]
            new_csv_row['editing'] = row[9]
            new_csv_row['studio'] = row[10]
            new_csv_row['budget'] = row[11]
            new_csv_row['gross'] = row[12]
            new_csv_row['runtime'] = row[13]
            new_csv_row['music'] = row[14]
            new_csv_row['writer'] = row[15]
            new_csv_row['starring'] = actor
            new_csv_row['language'] = row[17]
            new_csv_row['released'] = row[18]

            csv_writer.writerow(new_csv_row)

        i = i + 1
        #if (i == 3):
        #    import sys
        #    sys.exit()
