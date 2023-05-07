import os
import random
import sys
import threading
import requests

from icrawler.builtin import BingImageCrawler

from english_words import get_english_words_set

import nltk

def make_return_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    return dirname

DATA_DIR = 'data'

create_bread_dir = lambda: make_return_dir(f'{DATA_DIR}/bread')
create_non_bread_dir = lambda: make_return_dir(f'{DATA_DIR}/not_bread')

def _download_and_save_picsum(file_nm: str, height: int =150, width: int =150):
    MASTER_LOREM_PICSUM_URL = f"https://picsum.photos/{width}/{height}"

    with open(file_nm, 'wb') as img_file:
        response = requests.get(MASTER_LOREM_PICSUM_URL, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            img_file.write(block)

def _download_and_save_picsum_thread(dirname: str, some_range = tuple[int, int]):
    a, b = some_range
    for n in range(a, b):
        file_nm = dirname + "/{:06d}.jpg".format(n+1)
        print(file_nm)
        _download_and_save_picsum(file_nm)

def picsum(start_num: int, dirname: str, n_examples: int = 201, n_threads: int=5):
    pics_per_thread = n_examples // n_threads
    left_over = n_examples % n_threads

    thread_list = \
            list(map(
                lambda some_range: threading.Thread(
                    target=_download_and_save_picsum_thread,
                    args=(dirname, some_range,)),
                map(
                    lambda t_num: (start_num + t_num * pics_per_thread,
                                   start_num + (t_num + 1) * pics_per_thread),
                    range(n_threads)
                    )
                ))

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    print('NON BREAD DONE')

def gather_class(img_class, dirname=None, count=100):
    #filters = dict(
    #        size='small',
    #        license='commercial,modify'
    #)

    if dirname is None:
        dirname = img_class

    bing_crawler = BingImageCrawler(downloader_threads=4, storage={'root_dir': dirname})
    bing_crawler.crawl(keyword=img_class, offset=0, max_num=count,
                       file_idx_offset=len(os.listdir(dirname)))

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
    #filters = dict(
    #        size='small',
    #        license='commercial,modify'
    #)

    not_bread_dir = create_non_bread_dir()

    bing_crawler = BingImageCrawler(downloader_threads=4, storage={'root_dir': not_bread_dir})

    while len(os.listdir(not_bread_dir)) < count:
        # Generate nouns in batches.  Even if we are scraping for 10 images each,
        # sometimes we don't et that many
        word_count = count // count_per_class
        nouns = generate_nouns(count=word_count)

        for word in nouns:
            bing_crawler.crawl(keyword=word, #filters=filters,
                               file_idx_offset=len(os.listdir(not_bread_dir)),
                               max_num=count_per_class)

if len(sys.argv) >= 2:
    non_bread_dir = create_non_bread_dir()
    start_num = len(os.listdir(non_bread_dir))

    if 'raynotbread' in sys.argv[1]:
        picsum(start_num, 'test/not_bread')
    elif 'notbread' in sys.argv[1]:
        generate_not_bread()
    elif 'bread' in sys.argv[1]:
        if len(sys.argv) > 2:
            img_class = sys.argv[2]
        else:
            img_class = create_bread_dir()

        #for img_class in ['banana_bread', 'baguette', 'cibatta', 'cornbread', 'focaccia',
        #                  'multigrain_bread', 'pumpernickel', 'rye_bread', 'soda_bread',
        #                  'whole_wheat_bread']:
        for img_class in ['bread_slice', 'sliced_bread', 'piece_of_bread']:
            gather_class(img_class, dirname='test/bread')
        print('done')
    else:
        print(f'Unknown command {sys.argv[1]}')
