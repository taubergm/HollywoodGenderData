from nltk.corpus import names
import csv

#print(names.words('male.txt'))
#print(names.words('female.txt'))


#input_file_name = "all_actors_movies.csv"
#csvFile = "all_actors_movies_gender.csv"

input_file_name = "all_directors_movies.csv"
csvFile = "all_directors_gender.csv"

#input_file_name = "all_producers_movies.csv"
#csvFile = "all_producers_gender.csv"

#input_file_name = "all_writers_movies.csv"
#csvFile = "all_writers_gender.csv"

#input_file_name = "all_music_movies.csv"
#csvFile = "all_music_gender.csv"


outCsv = open(csvFile, 'w')
#fieldnames = ['year','wiki_ref','wiki_query','producer','distributor','name','country','director','cinematography','editing','studio','budget','gross', 'runtime','music','writer','starring','language','released','gender']


#fieldnames = ['year','name','country','budget','gross', 'runtime','starring','language','released','gender']

fieldnames = ['year','name','country','budget','gross', 'runtime','director','language','released','gender']


csv_writer = csv.DictWriter(outCsv, fieldnames=fieldnames)
csv_writer.writeheader()
csvfile = open(input_file_name)

readCSV = csv.reader(csvfile, delimiter=',')

def get_first_name(full_name):   
    try: 
        return full_name.split()[0]
    except:
        return ""

for row in readCSV:
    new_csv_row = {}

    #new_csv_row['year'] = row[0]
    #new_csv_row['wiki_ref'] = row[1]
    #new_csv_row['wiki_query'] = row[2]
    #new_csv_row['producer'] = row[3]
    #new_csv_row['distributor'] = row[4]
    #new_csv_row['name'] = row[5]
    #new_csv_row['country'] = row[6]
    #new_csv_row['director'] = row[7]
    #new_csv_row['cinematography'] = row[8]
    #new_csv_row['editing'] = row[9]
    #new_csv_row['studio'] = row[10]
    #new_csv_row['budget'] = row[11]
    #new_csv_row['gross'] = row[12]
    #new_csv_row['runtime'] = row[13]
    #new_csv_row['music'] = row[14]
    #new_csv_row['writer'] = row[15]
    #new_csv_row['starring'] = row[16]
    #new_csv_row['language'] = row[17]
    #new_csv_row['released'] = row[18]

    new_csv_row['year'] = row[0]
    new_csv_row['name'] = row[5]
    new_csv_row['country'] = row[6]
    new_csv_row['budget'] = row[11]
    new_csv_row['gross'] = row[12]
    new_csv_row['runtime'] = row[13]
    new_csv_row['director'] = row[7]

    new_csv_row['language'] = row[17]
    new_csv_row['released'] = row[18]


    first_name = get_first_name(row[7])

    if (first_name in names.words('male.txt')):
        new_csv_row['gender'] = "male"
    elif (first_name in names.words('female.txt')):
        new_csv_row['gender'] = "female"
    else:
        new_csv_row['gender'] = "unknown"


    csv_writer.writerow(new_csv_row)

