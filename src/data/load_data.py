from eventregistry import *
import json
import csv 
import os
import pandas as pd

def get_uri_list(source_uri,apiKey):
    e_reg = EventRegistry(apiKey = apiKey)
    e_qry = QueryEventsIter(lang = 'eng', dateStart = '2019-01-01', dateEnd = '2019-12-31', sourceUri = source_uri, categoryUri = 'news/Health')

    #to specify the event details to be included in the query
    #e_info = EventInfoFlags(title = True, summary = True, articleCounts = True, concepts = False, categories = True, location = True, date = True)

    #to specify the source details to be included in the query
    #articleCount: the number of articles from this news source that are stored in Event Registry
    #s_info = SourceInfoFlags(title = True, location = True, ranking = True, articleCount = True)

    #to specify the location details to be included in the query
    #l_info = LocationInfoFlags(countryContinent = True, placeCountry = True)

    #to specify the items returned from query
    #retrn_info = ReturnInfo(eventInfo = e_info, sourceInfo = s_info, locationInfo = l_info)

    #to execute the query
    #resutls = e_qry.execQuery(e_reg, sortBy = "date", maxItems = -1, returnInfo = retrn_info) maxItem=-1 for all events
    resutls = e_qry.execQuery(e_reg, sortBy = "date", maxItems = -1)

    uri_lst = []

    for result in resutls:
        uri_lst.append(result['uri'])

    return(uri_lst)

def create_datafiles(apiKey):

    #use 'https://eventregistry.org/documentation/api?tag=Event' to set more parameters
    url_endpoint = 'https://eventregistry.org/api/v1/event/getEvent'
    url_params = {  
                    'eventUri': '', 
                    'resultType': 'info', #use similarEvents info sourceExAggr
                    'includeEventTitle' : 'true',
                    'includeEventSummary' : 'true',
                    'includeEventSentiment' : 'true',
                    'includeEventLocation' : 'true',
                    'includeEventDate' : 'true',
                    'includeEventArticleCounts' : 'true',
                    'includeEventCategories' : 'true',
                    'includeSourceTitle' : 'true',
                    'includeSourceLocation' : 'true',
                    'includeSourceRanking' : 'true',
                    'includeLocationCountryArea' : 'true',
                    'includeLocationCountryContinent' : 'true',
                    'includeEventConcepts' : 'false',
                    'apiKey' : 'cbb094ef-cdf3-456e-82bd-f56c26cfb7e0'
                }
    #REST API call to get the event details
    # field names  
    fields = ['uri', 'title_eng', 'event_date', 'total_article_count', 'article_counts_eng', 'sentiment', 'categories', 'loc_country', 'loc_continent', 'summary', 'source_uri'] 

    #csv file 
    csvfile = open('data/raw/dataset.csv', 'a', newline='\n')

    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(fields)


    #to specify the query conditions
    source_uri_lst = []
    source_uri_lst.append('nytimes.com')
    source_uri_lst.append('indiatimes.com')
    source_uri_lst.append('washingtonpost.com')
    # source_uri_lst.append('usatoday.com')
    #source_uri_lst.append('chinadaily.com.cn')

    for source_uri in source_uri_lst:
        uri_lst = get_uri_list(source_uri,apiKey)

        for uri in uri_lst:
            url_params['eventUri'] = uri
            response = requests.get(url_endpoint, params=url_params)
            y = json.loads(response.text)

            for result in y: 
                row_text = []
                row_text.append(uri)
                row_text.append(y[uri]['info']['title']['eng'].replace('\n', ''))
                row_text.append(y[uri]['info']['eventDate'])
                row_text.append(y[uri]['info']['sentiment'])

                if y[uri]['info']['categories']:
                    cat_arr = ''
                    for category in y[uri]['info']['categories']:
                        cat_arr += category['label'] + ', '

                    row_text.append(cat_arr.rstrip(', '))
                else:
                    row_text.append('')
                    
                if y[uri]['info']['location']:

                    if y[uri]['info']['location']['country']:
                        row_text.append(y[uri]['info']['location']['country']['label']['eng'])
                    else:
                        row_text.append('')

                    if y[uri]['info']['location']['country']['continent']:
                        row_text.append(y[uri]['info']['location']['country']['continent'])
                    else:
                        row_text.append('')
                else:
                    row_text.append('')
                    row_text.append('')
                    
                row_text.append(y[uri]['info']['summary']['eng'].replace('\n', ' '))

                row_text.append(source_uri)

                writer.writerow(row_text)

def remove_duplicates():
    file_name_output = "data/raw/dataset-2.csv"

    #fields = ['uri', 'title_eng', 'event_date', 'total_article_count', 'article_counts_eng', 'sentiment', 'categories', 'loc_country', 'loc_continent', 'summary', 'indiatimes.com', 'washingtonpost.com', 'nytimes.com']
    df = pd.read_csv('data/raw/dataset.csv', sep=",")


    df.drop_duplicates(subset=['uri'], inplace=True)

    # Write the results to a different file
    df.to_csv(file_name_output, index=False) 

    rows = {}
    with open('data/raw/dataset-2.csv', 'r', newline='\n') as acsv:
        areader = csv.reader(acsv)
        for row in areader:
            # store the row based on the item1 and item2 columns
            key = row[0]
            y=row
            y.append('')
            rows[key] = y

    with open('data/raw/dataset.csv', 'r', newline='\n') as bcsv:
        breader = csv.reader(bcsv)
        for row in breader:
            # set the label of matching rows to 1 when present
            key = row[0]
            
            if key in rows:

                rows[key][10] = ''

                if row[10] == 'indiatimes.com':
                    rows[key][10] += ' indiatimes.com'
                    
                elif row[10] == 'washingtonpost.com':
                    rows[key][10] += ' washingtonpost.com'

                elif row[10] == 'nytimes.com': 
                    rows[key][10] += ' nytimes.com'

    with open('data/raw/dataset-3.csv', 'w', newline='\n') as result:
        writer = csv.writer(result)
        for x in rows:
            writer.writerow(rows[x])

    os.remove(r'data/raw/dataset.csv')
    os.remove(r'data/raw/dataset-2.csv')
    os.rename(r'data/raw/dataset-3.csv',r'data/raw/dataset.csv')


def main():
    if len(sys.argv) == 2: 
        apiKey = sys.argv[1]
        create_datafiles(apiKey)
        remove_duplicates()

    else: 
        print("Please provide the appropriate command line arguments")

if __name__ == "__main__":
    main()








    
