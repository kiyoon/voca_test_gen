import csv
import getopt
import sys
import random
import os

def help():
    print("Usage: %s [options..] [files..]" % sys.argv[0])
    print("Author: Kiyoon Kim (yoonkr33@gmail.com)")
    print("Description: Load files of word and meaning list in CSV. It will shuffle the list and generate tests.")
    print()
    print("Options:")
    print(" -h, --help\t\t\tprint this help list")
    print(" -l, --load\t\t\tspecify a CSV file to load")
    #print(" -d, --days=NUMBER,NUMBER,..\tload word list from day{NUMBER}.txt")
    print(" -c, --count=COUNT\t\tspecify how many words to sample. set 0 to sample all. (default 0)")
    print(" -t, --try=TRY\t\t\tspecify how many different sampled sets to generate. (default 1)")

if __name__ == "__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:], "hl:c:t:", ["help", "load=", "count=", "try="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    load = None
    count = 0
    trys = 1
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()
        elif opt in ('-l', '--load'):
            load = arg
        elif opt in ('-c', '--count'):
            count = int(arg)
        elif opt in ('-t', '--try'):
            trys = int(arg)

    if not load:
        raise ValueError('You must set the file by -l option.')

    words = []
    meanings = []
    with open(load, 'r', encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for line in reader:
            words.append(line[0])
            meanings.append(line[1])

    if count == 0:
        count = len(words)

    word_and_meanings = list(zip(words, meanings))

    name_of_file = os.path.splitext(os.path.basename(load))[0]

    for i in range(trys):
        sampled = random.sample(word_and_meanings, count)
        with open('%s_test%d_stripped.txt' % (name_of_file, i+1), 'w', encoding = 'utf-8') as f_test_stripped:
            with open('%s_test%d.txt' % (name_of_file, i+1), 'w', encoding = 'utf-8') as f_test:
                with open('%s_test%d_answer.txt' % (name_of_file, i+1), 'w', encoding = 'utf-8') as f_answer:
                    for sample in sampled:
                        f_test_stripped.write(sample[0] + "\n")
                        f_test.write(sample[0] + "\n\n")
                        f_answer.write(sample[0] + "\n" + sample[1] + "\n\n")



