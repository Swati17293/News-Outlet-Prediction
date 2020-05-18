# morphological restoration, digit replacement, stop word deletion..
import os
import csv
import re

#used for lemmatization
from textblob import Word 

def get_stopwords():
    stops = []
    fstop = open('data/external/stopwords.txt','r')
    lines = fstop.readlines()
    for line in lines:
        line = line.strip()
        stops.append(line)
    fstop.close()
    return(stops)

def text_process(text, stops):

    text = re.sub(r"[^A-Za-z0-9 ']",'',text) #punctuation deletion
    text = ' '.join(text.split()) #remove extra spaces
    
    text_lst = text.lower().split(' ')

    wrd_lst = []

    for txt in text_lst: #Stop word deletion
        w = txt
        for div in stops: 
            if txt == div:
                w = ''
        wrd_lst.append(w)

    j = len(wrd_lst)
    for i in range(j):
        if re.match(r'[0-9]+', wrd_lst[i]):  #Digital replacement
            wrd_lst[i] = 'num'
        wrd_lst[i] = Word(wrd_lst[i]).lemmatize()

    text = ' '.join(wrd_lst)
    text = ' '.join(text.split()) #remove extra spaces

    return(text)

def category_process(text):
    
    text = text.replace('/',' ') #punctuation deletion
    text = text.replace(',',' ') #punctuation deletion
    text = text.lower().split(' ')
    
    text = ' '.join(set(text))
    text = ' '.join(text.split()) #remove extra spaces

    return(text)


def pretreat_data(data, stops):
    f = open('data/raw/' + data + '.csv')
    fw = open('data/processed/' + data + '.pre', 'a', newline='\n')

    writer = csv.writer(fw, delimiter=',')

    lines = csv.reader(f)
    #next(lines) #to skip the header of the csv

    for line in lines:
        row = []

        line_title = text_process(line[1], stops)
        line_category = category_process(line[4])
        line_summary = text_process(line[7], stops)

        row.append(line_title)
        row.append(line_category)
        row.append(line_summary)

        writer.writerow(row)

    f.close()
    fw.close()

def main():

    #warnings.filterwarnings("ignore", category=UserWarning)
    print('\n\nPreprocessing Text...')

    if os.path.isfile('data/processed/Test.pre') == False:
        stops = get_stopwords()
        pretreat_data('Train', stops)
        pretreat_data('Valid', stops)
        pretreat_data('Test', stops)

    print('\nPreprocessing Complete...\n\n')

if __name__ == "__main__":
    main()