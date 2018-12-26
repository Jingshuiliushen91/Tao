# How to use

## words_crawler

* `Des`: Crawling from we url
* `Input`: Web URL
* `Output`: Word list, i.e., list of possitive or negative words

---

## class artical_analyzer:

* `Des`: Get how word counter, i.e., how many possitive word or negative words

#### *funtion: single_word_counter* 
* `Input`: 
    * word: A word you want to get, "happy" for example;
    * csv_url: relative path for your .csv file.
    * col: which csv column you want to analysis, 'id', 'td'...
* `Output`: Number of word in csv


#### *funtion: list_words_counter* 
* `Input`: 
    * words: A list of word you want to get, ["happy", "sad" ....], for example;
    * csv_url: relative path for your .csv file.
    * col: which csv column you want to analysis, 'id', 'td'...
* `Output`: sum(num(word in csv)) where word in words.