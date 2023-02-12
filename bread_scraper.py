import os
import random
import sys

from icrawler.builtin import BingImageCrawler

from english_words import get_english_words_set

import nltk

def make_return_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    return dirname

create_bread_dir = lambda: make_return_dir('bread')
create_not_bread_dir = lambda: make_return_dir('not_bread')

def gather_class(img_class, count=100):
    filters = dict(
            size='small',
            license='commercial,modify'
    )

    bing_crawler = BingImageCrawler(downloader_threads=4, storage={'root_dir': img_class})
    bing_crawler.crawl(keyword=img_class, filters=filters, offset=0, max_num=count)

def generate_nouns(count=100):
    # Some things we have to download for nltk first..
    #nltk.download('punkt')
    #nltk.download('averaged_perceptron_tagger')

    # Grab english words
    word_set = get_english_words_set(['web2'], lower=True)

    is_noun = lambda pos: pos[:2] == 'NN'

    # Hopefully this reduces the total number of words for performance, but not the total
    # number of nouns too much
    word_set = random.sample(word_set, count*100)

    # Combine words into a format for nltk
    long_str = ' '.join(word_set)
    tokenized = nltk.word_tokenize(long_str)

    # Tell nltk to infer which ones are nouns
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

    # Select and return a particular number of these identified nouns
    return random.sample(nouns, count)

def generate_not_bread(count=1000, count_per_class=10):
    filters = dict(
            size='small',
            license='commercial,modify'
    )

    word_count = count // count_per_class
    not_bread_dir = create_not_bread_dir()

    nouns = generate_nouns(count=word_count)

    bing_crawler = BingImageCrawler(downloader_threads=4, storage={'root_dir': not_bread_dir})

    for word in nouns:
        bing_crawler.crawl(keyword=word, filters=filters,
                           file_idx_offset=len(os.listdir(not_bread_dir)),
                           max_num=count_per_class)

if len(sys.argv) >= 2:
    if 'notbread' in sys.argv[1]:
        generate_not_bread()
    elif 'bread' in sys.argv[1]:
        gather_class(create_bread_dir())
        print('done')
    else:
        print(f'Unknown command {sys.argv[1]}')
