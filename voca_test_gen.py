import requests
from bs4 import BeautifulSoup
import getopt
import sys
import random

def help():
    print("Usage: %s [options..] [files..]" % sys.argv[0])
    print("Author: Kiyoon Kim (yoonkr33@gmail.com)")
    print("Description: Pick word list files. It will shuffle the list, search for the meaning at Naver English Dictionary, and make vocabulary tests.")
    print()
    print("Options:")
    print(" -h, --help\t\t\tprint this help list")
    print(" -d, --days=NUMBER,NUMBER,.. or NUMBER~NUMBER\tload word list from day{NUMBER}.txt")
    print(" -l, --loads=FILE,FILE,..\tload word list from file")
    print(" -c, --count=COUNT\t\tspecify how many words to sample. set 0 to sample all. (default 0)")
    print(" -t, --try=TRY\t\t\tspecify how many different sampled sets to generate. (default 1)")

def search_endic(word_to_search):
    search = requests.get('https://endic.naver.com/search.nhn?sLn=kr&isOnlyViewEE=N&searchOption=entry_idiom&query=' + word_to_search)
    html = search.text
    soup = BeautifulSoup(html, 'html.parser')
    search_res = soup.select('#content > div > dl > dt > span.fnt_e30 > a')
    #print(search_res)

    ret_text = ""
    for res in search_res:
        if res.text in (word_to_search, word_to_search + "1", word_to_search + "2", word_to_search + "3") or word_to_search == res.text.replace("something ", ""):
            specific_search = requests.get('https://endic.naver.com' + res.get('href'))
            html = specific_search.text
            soup = BeautifulSoup(html, 'html.parser')
            type_res = soup.select('span.fnt_syn')
#            meaning_res = soup.select('#zoom_content > div > dl > dt.first.mean_on.meanClass > em > span.fnt_k06')
#            if not meaning_res:
#                meaning_res = soup.select('#zoom_content > div.box_wrap24 > dl > dt > em > span.fnt_k06')

            all_meanings = soup.select('#zoom_content > div > dl > dt > em > span.fnt_k06')
            #print(all_meanings)
            numbers = soup.select('#zoom_content > div > dl > dt > span.fnt_e11')
            #print(numbers)
            
            if not type_res:
                for meaning in all_meanings:
                    ret_text += meaning.text + "\n"
            else:
                idx_type = 0
                if numbers:
                    for (number, meaning) in zip(numbers, all_meanings):
                        if number.text in ('1.', '1-a.', ''):
                            ret_text += type_res[idx_type].text + ": " + meaning.text + "\n"
                            idx_type += 1
                        else:
                            ret_text += meaning.text + "\n"
                else:
                    for (word_type, meaning) in zip(type_res, all_meanings):
                        ret_text += word_type.text + ": " + meaning.text + "\n"

            ret_text += "\n"
    return ret_text

if __name__ == "__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:], "hd:l:c:t:", ["help", "days=", "loads=", "count=", "try="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    days = None
    loads = None
    count = 0
    trys = 1
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()
        elif opt in ('-d', '--day'):
            if arg.find('~') >= 0:
                range_list = list(map(int, arg.split('~')))
                range_list[1] += 1
                days = list(range(*range_list))
            else:
                days = map(int, arg.split(','))
            days_str = arg
        elif opt in ('-l', '--loads'):
            loads = arg.split(',')
            days_str = '0'
        elif opt in ('-c', '--count'):
            count = int(arg)
        elif opt in ('-t', '--try'):
            trys = int(arg)

    if not days and not loads:
        raise ValueError('You must set the file by -d or -l option.')

    words = []
    if days:
        for day in days:
            with open('voca_data\\day%d.txt' % day, 'r') as f:
                words.extend(list(filter(None, f.read().splitlines())))
    if loads:
        for load in loads:
            with open(load, 'r') as f:
                words.extend(list(filter(None, f.read().splitlines())))

    if count == 0:
        count = len(words)

#    print(search_endic('managerial'))
    meanings = []
    for word in words:
#        print(word)
#        print(search_endic(word))
        naver_meaning = search_endic(word)
        if naver_meaning is None:
            raise ValueError(word + " not found")
        meanings.append(naver_meaning)

    word_and_meanings = list(zip(words, meanings))

    for i in range(trys):
        sampled = random.sample(word_and_meanings, count)
        with open('day%s_test%d_stripped.txt' % (days_str, i+1), 'w', encoding = 'utf-8-sig') as f_test_stripped:
            with open('day%s_test%d.txt' % (days_str, i+1), 'w', encoding = 'utf-8-sig') as f_test:
                with open('day%s_test%d_answer.txt' % (days_str, i+1), 'w', encoding = 'utf-8-sig') as f_answer:
                    for sample in sampled:
                        f_test_stripped.write(sample[0] + "\n")
                        f_test.write(sample[0] + "\n\n")
                        f_answer.write(sample[0] + "\n" + sample[1])



