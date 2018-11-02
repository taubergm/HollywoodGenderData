import csv
import sys
reload(sys)  
sys.setdefaultencoding('UTF8')
import re
#import networkx as nx
#import matplotlib.pyplot as plt
import io

filename = sys.argv[1]

# needed to remove carriage returns - %s/\r//g


i = 0
j = 0

# create set of all actors
seen_actors = set()


# remove <!.*|, [[ ]] , plainlist , ubl, * , {{ }}, | , plain list, <br />, br/>,<br> , (actor)
        # replace with spaces
#starring = re.sub("\[.*\|", " ", starring)
def clean_wiki_plainlist(list_data):
        list_data = re.sub("ref.*/ref>\|", "  ", list_data)
        list_data = re.sub("\|ref\|?", "  ", list_data)
        list_data = re.sub("name=.*\|", "  ", list_data)
        list_data = re.sub("<!.*\|", "  ", list_data)
        list_data = re.sub("<!.*\>", "  ", list_data)
        list_data = re.sub("\[\[", "  ", list_data)
        list_data = re.sub("\]\]", "  ", list_data)
        list_data = re.sub("\{\{cite.*\}\}", "  ", list_data)
        list_data = re.sub("\{\{nbsp\}\}", "  ", list_data)
        list_data = re.sub("\}\}", "  ", list_data)
        list_data = re.sub("\{\{", "  ", list_data)
        list_data = re.sub("plainlist", "  ", list_data, flags=re.IGNORECASE)
        list_data = re.sub("plain list", "  ", list_data, flags=re.IGNORECASE)
        list_data = re.sub("unbulleted list", "  ", list_data, flags=re.IGNORECASE)
        list_data = re.sub("ubl", "  ", list_data)
        list_data = re.sub("<br />", "  ", list_data)
        list_data = re.sub("<br/>", "  ", list_data)
        list_data = re.sub("<br>", "  ", list_data)
        list_data = re.sub("\(actor\)", "  ", list_data)
        list_data = re.sub("\(actress\)", "  ", list_data)
        list_data = re.sub("\(entertainer\)", "  ", list_data)
        list_data = re.sub("\(producer\)", "  ", list_data)
        list_data = re.sub("\|", "  ", list_data)
        list_data = re.sub("\*", "  ", list_data)
        list_data = re.sub("Hong Kong dollar.*br", "  ", list_data)
        list_data = re.sub("-", " ", list_data)
        list_data = re.sub("<br.*>", "  ", list_data)
        list_data = re.sub("\(.*\)", "  ", list_data)
        list_data = re.sub("\".*\"", "  ", list_data)
        list_data = re.sub("unbulleted list", "  ", list_data)
        list_data = re.sub("</ref>", "  ", list_data)
        list_data = re.sub("</small>", "  ", list_data)
        list_data = re.sub("<small>", "  ", list_data)
        list_data = re.sub("Executive:", "  ", list_data)
        list_data = re.sub("Uncredited:", "  ", list_data)
        list_data = re.sub("ref.*/ref>", "  ", list_data)
        list_data = re.sub("\|ref\|", "  ", list_data)
        list_data = re.sub("\#", "  ", list_data)
        list_data = re.sub("United States dollar", "  ", list_data)
        list_data = re.sub("nowrap", "  ", list_data)

        
        
        #list_data = re.sub("<br>", " ", list_data)
        #list_data = re.sub("<br />", " ", list_data)
        #list_data = re.sub("<br/>", " ", list_data)

        return list_data


def convert_wiki_date(date_string):

    date_nums = re.findall(r'date\|(\d+)\|(\d+)\|(\d+)', date_string)  
    try:
        date_string = str(date_nums[0][0]) + "/" + str(date_nums[0][1]) + "/" + str(date_nums[0][2]) 
    except:
        date_string = ""

    #for date_num in date_nums[0]
    #    print date_num
    return date_string


def convert_wiki_numbers(number_string):
    
    number_string = re.sub("\$.*\$", "$", number_string)
    number_string = re.sub(r".*\_(\d)", r"\1", number_string)
    number_string = re.sub(r".*\_ (\d)", r"\1", number_string)
    number_string = re.sub(r".*\_ (\d)", r"\1", number_string)
    number_string = re.sub(r".*- \$(\d)", r"\1", number_string)
    number_string = re.sub(r".*-\s+(\d)", r"\1", number_string)
    number_string = re.sub(r"\$.*-(\d)", r"\1", number_string)
    number_string = re.sub(r"_", r" ", number_string)
    number_string = re.sub("\$", "", number_string)
    number_string = re.sub("\,", "", number_string)
    number_string = re.sub("&nbsp;", "", number_string)
    number_string = re.sub("&nbsp", "", number_string)
    number_string = re.sub("nbsp;", "", number_string)
    number_string = re.sub("nbsp", "", number_string)
    number_string = re.sub(";", "", number_string)
    number_string = re.sub("\{\{nbsp\}\}", "", number_string)
    number_string = re.sub("billion.*", "billion", number_string)
    number_string = re.sub("million.*", "million", number_string)

    #number_string = re.sub("\.(\d)(\d)(\d)\s+billion","\1\2\3" + "000000", number_string)

    number_string = re.sub(r"\.(\d)(\d)(\d)(\d)\s+billion", r"\1,\2,\3,\4," + "00000", number_string)
    number_string = re.sub(r"\.(\d)(\d)(\d)(\d)billion", r"\1,\2,\3,\4," + "00000", number_string)
    number_string = re.sub(r"\.(\d)(\d)(\d)\s+billion", r"\1,\2,\3," + "000000", number_string)
    number_string = re.sub(r"\.(\d)(\d)(\d)billion", r"\1,\2,\3," + "000000", number_string)
    number_string = re.sub(r"\.(\d)(\d)\s+billion", r"\1,\2," + "0000000", number_string)
    number_string = re.sub(r"\.(\d)(\d)billion", r"\1,\2," + "0000000", number_string)
    number_string = re.sub(r"\.(\d)\s+billion", r"\1," + "00000000", number_string)
    number_string = re.sub(r"&.*billion", r"000000000", number_string)
    number_string = re.sub(r"billion", r"000000000", number_string)
    umber_string = re.sub(r"\.(\d)(\d)(\d)billion", r"\1,\2,\3," + "000000", number_string)
    number_string = re.sub(r"\.(\d)(\d)billion", r"\1,\2," + "0000000", number_string)
    number_string = re.sub(r"\.(\d)billion", r"\1," + "00000000", number_string)
    number_string = re.sub(r"billion", r"000000000", number_string)

    number_string = re.sub(r"\.(\d)(\d)(\d)(\d)\s+million", r"\1,\2,\3,\4," + "00", number_string)
    number_string = re.sub(r"\.(\d)(\d)(\d)(\d)million", r"\1,\2,\3,\4," + "00", number_string)
    number_string = re.sub(r"\.(\d)(\d)(\d)\s+million", r"\1,\2,\3," + "000", number_string)
    number_string = re.sub(r"\.(\d)(\d)(\d)million", r"\1,\2,\3," + "000", number_string)
    number_string = re.sub(r"\.(\d)(\d)\s+million", r"\1,\2," + "0000", number_string)
    number_string = re.sub(r"\.(\d)(\d)million", r"\1,\2," + "0000", number_string)
    number_string = re.sub(r"\.(\d)\s+million", r"\1," + "00000", number_string)
    number_string = re.sub(r"&.*million", r"000000", number_string)
    number_string = re.sub(r"million", r"000000", number_string)
    umber_string = re.sub(r"\.(\d)(\d)(\d)million", r"\1,\2,\3," + "000", number_string)
    number_string = re.sub(r"\.(\d)(\d)million", r"\1,\2," + "0000", number_string)
    number_string = re.sub(r"\.(\d)million", r"\1," + "00000", number_string)
    number_string = re.sub(r"million", r"000000", number_string)

    number_string = re.sub("\s+(\d)", r"\1,", number_string)
    number_string = re.sub("\s+C", r"C", number_string)
    number_string = re.sub(r".*USD", r"", number_string)
    number_string = re.sub(r".*US", r"", number_string)
    number_string = re.sub(r",", r"", number_string)
    number_string = re.sub(r"small", r"", number_string)
    number_string = re.sub(r"minutes", r"", number_string)
    number_string = re.sub(r"min.", r"", number_string)


    number_string = number_string.strip()
    #print number_string


    return number_string




def clean_python_list(list_data):
    list_data = re.split(r'\s{2,}', list_data)
    if '' in list_data:
        list_data.remove('')
    if '' in list_data:
        list_data.remove('')
    if '' in list_data:
        list_data.remove('')
    if '' in list_data:
        list_data.remove('')
    if '' in list_data:
        list_data.remove('')
    if 'small' in list_data:
        list_data.remove('small')
    if 'Small' in list_data:
        list_data.remove('Small')
    if 'ref' in list_data:
        list_data.remove('ref')
    if 'ref 1 1' in list_data:
        list_data.remove('ref 1 1')


    clean_list_data = []
    for list_item in list_data:
        list_item = list_item.strip()
        clean_list_data.append(list_item)

    return clean_list_data




#with io.open(filename, encoding='latin-1', errors='ignore') as csvfile:

csvFile = sys.argv[2]
outCsv = open(csvFile, 'wb')
fieldnames = ['year','wiki_ref','wiki_query','producer','distributor','name','country','director','cinematography','editing','studio','budget','gross',
                    'runtime','music','writer','starring','language','released']

csv_writer = csv.DictWriter(outCsv, fieldnames=fieldnames)
csv_writer.writeheader()

with io.open(filename, encoding='utf-8', errors='ignore') as csvfile:

    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:



        # get movie name
        movie_name = row[5]

        if (movie_name == "name"):
            continue
        #print movie_name


        # fix up the bad formatting of wiki plainlist data - replace with whitespace
        starring = row[16].encode('utf8')        
        starring = clean_wiki_plainlist(starring)

        producer = row[3].encode('utf8')        
        producer = clean_wiki_plainlist(producer)

        distributor = row[4].encode('utf8')        
        distributor = clean_wiki_plainlist(distributor)

        country = row[6].encode('utf8')        
        country = clean_wiki_plainlist(country)

        director = row[7].encode('utf8')        
        director = clean_wiki_plainlist(director)

        cinematographer = row[8].encode('utf8')        
        cinematographer = clean_wiki_plainlist(cinematographer)

        editor = row[9].encode('utf8')        
        editor = clean_wiki_plainlist(cinematographer)

        studio = row[10].encode('utf8')        
        studio = clean_wiki_plainlist(studio)

        gross = row[12].encode('utf8')        
        gross = clean_wiki_plainlist(gross)

        budget = row[11].encode('utf8')        
        budget = clean_wiki_plainlist(budget)


        music = row[14].encode('utf8')        
        music = clean_wiki_plainlist(music)

        runtime = row[13].encode('utf8')        
        runtime = clean_wiki_plainlist(runtime)

        writer = row[15].encode('utf8')        
        writer = clean_wiki_plainlist(writer)

        language = row[17].encode('utf8')  
        language = clean_wiki_plainlist(language)


        clean_writers = clean_python_list(writer)
        clean_actors = clean_python_list(starring)
        clean_producers = clean_python_list(producer)
        clean_directors = clean_python_list(director)
        clean_country = clean_python_list(country)
        clean_cinematographers = clean_python_list(cinematographer)
        clean_editor = clean_python_list(editor)
        clean_studios = clean_python_list(studio)
        clean_musicians = clean_python_list(music)
        clean_distributora = clean_python_list(distributor)
        clean_budget = convert_wiki_numbers(budget)
        clean_gross = convert_wiki_numbers(gross)
        clean_runtime = convert_wiki_numbers(runtime)
        clean_language = clean_python_list(language)



        #print "%s - %s" % (i,clean_runtime)
           
        new_csv_row = {}

        new_csv_row['year'] = row[0]
        new_csv_row['wiki_ref'] = row[1]
        new_csv_row['wiki_query'] = row[2]
        new_csv_row['producer'] = clean_producers
        new_csv_row['distributor'] = clean_distributors
        new_csv_row['name'] = row[5]
        new_csv_row['country'] = clean_country
        new_csv_row['director'] = clean_directors
        new_csv_row['cinematography'] = clean_cinematographers
        new_csv_row['editing'] = clean_editor
        new_csv_row['studio'] = clean_studios
        new_csv_row['budget'] = clean_budget
 
        new_csv_row['gross'] = clean_gross
        new_csv_row['runtime'] = clean_runtime
        new_csv_row['music'] = clean_musicians
        new_csv_row['writer'] = clean_writers
        new_csv_row['starring'] = clean_actors
        new_csv_row['language'] = clean_language
        new_csv_row['released'] = convert_wiki_date(row[18])


        #print new_csv_row

        csv_writer.writerow(new_csv_row)


        
        #write to new csv in utf8 - also parse movie name


         # fix up the bad formatting of directors, producers



        # now create a graph in nx, where each actor is a node and we add edges between them with movie name



