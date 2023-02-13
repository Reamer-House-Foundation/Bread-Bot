
import requests
import os
from icrawler.builtin import BingImageCrawler
import threading

def make_return_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    return dirname

create_bread_dir = lambda: make_return_dir('bread')
create_non_bread_dir = lambda: make_return_dir('non_bread')

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

def picsum(dirname: str, n_examples: int = 100, n_threads: int=5):
    pics_per_thread = n_examples // n_threads
    left_over = n_examples % n_threads

    thread_list = \
            list(map(
                lambda some_range: threading.Thread(
                    target=_download_and_save_picsum_thread,
                    args=(dirname, some_range,)),
                map(
                    lambda t_num: (t_num * pics_per_thread, (t_num + 1) * pics_per_thread),
                    range(n_threads)
                    )
                ))

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    print('NON BREAD DONE')

# download non_bread
picsum(create_non_bread_dir())

print('done')




