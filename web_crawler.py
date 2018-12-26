import urllib.request
import ssl
import csv
import codecs


class words_crawler:

    def getWords(self, url):
        words = []
        context = ssl._create_unverified_context()
        for link in url:
            ftpstream = urllib.request.urlopen(url, context=context)
            csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
            for word in csvfile:
                words.append(word[0])
        return words

possitiveWord = words_crawler()
print(possitiveWord.getWords('https://www3.nd.edu/~mcdonald/Data/Finance_Word_Lists/LoughranMcDonald_Positive.csv'))
