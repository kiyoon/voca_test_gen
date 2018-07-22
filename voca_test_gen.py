import requests
from bs4 import BeautifulSoup
import getopt
import sys
import random

def help():
    print("Usage: %s [options..] [files..]" % sys.argv[0])
    print("Author: Kiyoon Kim (yoonkr33@gmail.com)")
    print("Description: Change file names based on their creation/modified date")
    print()
    print("Options:")
    print(" -h, --help\t\t\tprint this help list")
    print(" -d, --days=NUMBER,NUMBER,..\tload word list from day{NUMBER}.txt")
    print(" -c, --count=COUNT\t\tspecify how many words to sample. set 0 to sample all. (default 0)")
    print(" -t, --try=TRY\t\t\tspecify how many different sampled sets to generate. (default 1)")

def search_endic(word_to_search):
    search = requests.get('https://endic.naver.com/search.nhn?sLn=kr&isOnlyViewEE=N&searchOption=entry_idiom&query=' + word_to_search)
    html = search.text
    soup = BeautifulSoup(html, 'html.parser')
    search_res = soup.select('#content > div > dl > dt.first > span.fnt_e30 > a')

    ret_text = ""
    for res in search_res:
        if res.text == word_to_search:
            specific_search = requests.get('https://endic.naver.com' + res.get('href'))
            html = specific_search.text
            soup = BeautifulSoup(html, 'html.parser')
            type_res = soup.select('span.fnt_syn')
            meaning_res = soup.select('#zoom_content > div > dl > dt.first.mean_on.meanClass > em > span.fnt_k06')
            for (word_type, meaning) in zip(type_res, meaning_res):
                ret_text += word_type.text + ": " + meaning.text + "\n"
            return ret_text

if __name__ == "__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:], "hd:c:t:", ["help", "days=", "count=", "try="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    days = None
    count = 0
    trys = 1
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()
        elif opt in ('-d', '--day'):
            days = map(int, arg.split(','))
            days_str = arg
        elif opt in ('-c', '--count'):
            count = int(arg)
        elif opt in ('-t', '--try'):
            trys = int(arg)

    if not days:
        raise ValueError('You must set the day by -p option.')

    words = []
    for day in days:
        with open('voca_data\\day%d.txt' % day, 'r') as f:
            words.extend(list(filter(None, f.read().splitlines())))

    if count == 0:
        count = len(words)

#    print(search_endic('managerial'))
    meanings = []
    for word in words:
#        print(word)
#        print(search_endic(word))
        meanings.append(search_endic(word))

    word_and_meanings = list(zip(words, meanings))

    for i in range(trys):
        sampled = random.sample(word_and_meanings, count)
        with open('day%s_test%d_stripped.txt' % (days_str, i+1), 'w', encoding = 'utf-8') as f_test_stripped:
            with open('day%s_test%d.txt' % (days_str, i+1), 'w', encoding = 'utf-8') as f_test:
                with open('day%s_test%d_answer.txt' % (days_str, i+1), 'w', encoding = 'utf-8') as f_answer:
                    for sample in sampled:
                        f_test_stripped.write(sample[0] + "\n")
                        f_test.write(sample[0] + "\n\n")
                        f_answer.write(sample[0] + "\n" + sample[1] + "\n")



