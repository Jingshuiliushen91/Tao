import csv
import re
from web_crawler import words_crawler


class artical_analyzer:

    def single_word_counter(self, word, csv_url, col):
        counter = 0
        with open(csv_url) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                wordList = re.sub("[^\w]", " ", row[col]).split()
                for singleword in wordList:
                    if (singleword == word):
                        counter += 1

        return counter

    def list_words_counter(self, words, csv_url, col):
        counter = 0
        l = 0
        with open(csv_url) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                wordList = re.sub("[^\w]", " ", row[col]).split()
                print("**********************<" + l + " out of " + len(row) + ">**********************")
                for w in words:
                    for singleword in wordList:
                        if (singleword.lower() == w.lower()):
                            counter += 1
                print("counter: " + str(counter))
                l += 1;
        return counter


words_crawler = words_crawler()
possitive_words = words_crawler.getWords(
    'https://www3.nd.edu/~mcdonald/Data/Finance_Word_Lists/LoughranMcDonald_Positive.csv')
negative_words = words_crawler.getWords(
    'http://www3.nd.edu/~mcdonald/Data/Finance_Word_Lists/LoughranMcDonald_Negative.csv');

artical_analyzer = artical_analyzer()
number_possitive = artical_analyzer.list_words_counter(possitive_words, 'factiva1.csv', 'td')
number_negative = artical_analyzer.list_words_counter(negative_words, 'factiva1.csv', 'td')

print("possitive words are: " + possitive_words)
print("negative words are: " + negative_words)
print("Number of possitive words: " + number_possitive);
print("Number of negative words: " + number_negative);
