import dotenv
from artcls import hwork, maindb
import json
import os

if __name__ == '__main__':

    hworker = hwork.HabrArtickleWorker()
    base_path_work = hworker.base_path()

    with open(os.path.join(base_path_work, r'config\base_config.json'), encoding='utf-8') as file_config:
        config = json.load(file_config)
    keyword = config['KEYWORDS']
    headers = config['HEADERS']

    dotenv_path = os.path.join(base_path_work, '.env')
    dotenv.load_dotenv(dotenv_path)

    db_name = os.getenv('db_name')
    user = os.getenv('user')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    baseurl = 'https://habr.com'

    last_artname = hworker.rw_last('r', base_path_work)
    finish_art = True
    page_cicle = 1
    data_arr = []

    while finish_art:
        url = f'{baseurl}/ru/all/page{page_cicle}'
        articles = hworker.ret_arciles(url, headers)

        for article in articles:
            previews = set(x.span.text for x in article.find_all('span', class_="tm-article-snippet__hubs-item"))
            title = article.find('a', class_='tm-title__link')
            try:
                href = title['href']
            except TypeError:
                continue

            span_title = title.text

            if baseurl + href == last_artname:
                finish_art = False
                print('All new articles worked out')
                print('At the moment this article is on page', page_cicle)
                break

            for key, val in keyword.items():
                if not previews.isdisjoint(val):
                    data_arr.append((span_title, baseurl + href, ', '.join(previews), key))
                    break
        page_cicle += 1

    if len(data_arr) != 0:
        hworker.save_csv(data_arr, base_path_work)
        db_obj = maindb.DatabWorker(db_name, user, password, host, port)
        db_obj(data_arr)
    else:
        print('No new data found')

    new_last_title = hworker.ret_arciles(baseurl + '/ru/all/page1', headers)
    last_title = new_last_title[0].find('a', class_='tm-title__link')
    last_span_title = baseurl + last_title['href']
    hworker.rw_last('w', base_path_work, last_span_title)
