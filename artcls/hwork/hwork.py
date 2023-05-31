import bs4
import requests
import os
import pandas as pd
import numpy as np


class HabrArtickleWorker:
    def __init__(self, baseurl: str = 'https://habr.com') -> None:
        """Initialize HabrArtickleWorker object.

        Args:
            baseurl (str): base domain for parsing.

        Returns:
            None
        """
        self.baseurl = baseurl

    @staticmethod
    def ret_arciles(url: str, headers: dict) -> list[str]:
        """Function for parsing the site and extracting articles. ##

        Args:
            url (str): The URL of the website to parse.
            headers (str): Headers.

        Returns:
            articles (list[str]): html content.
        """
        response = requests.get(url, headers=headers)
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all('article', class_='tm-articles-list__item')
        return articles

    @staticmethod
    def rw_last(flag: str, path_file: str,
                last_span_title: str = None) -> str:
        """Write the first processed article or read the last processed.

        Args:
            flag (str): flag to write or read.
            last_span_title (str): The first article to be the last on the next launch.
            path_file (str): Path to the file containing the file to be written/read.

        Returns:
            str / None: Returns the last processed article / does not return anything when writing.
        """
        with open(os.path.join(path_file, r'..\Article-Manager\data\raw\last_ref.txt'), flag) as file:
            if flag == 'r':
                last_artname = file.read()
                return last_artname
            else:
                file.write(last_span_title)

    @staticmethod
    def base_path(base_dir: str = 'Article-Manager') -> str:
        """Return base path for this dir.

        Args:
            base_dir (str): base dir for this git.

        Returns:
            path (str): returns the path to the base directory of this git
        """
        path = os.getcwd()
        while not path.endswith(base_dir):
            path = os.path.split(path)[0]
        return path

    @staticmethod
    def save_csv(data: list[tuple], path_to_save: str) -> None:
        """This function saves the data to a csv file.

        Args:
            data (list[tuple]): data for write.
            path_to_save (str): path to save directory.

        Returns:
            None
        """
        full_path = os.path.join(path_to_save, r'..\Article-Manager\data\saves csv\powebi_utf8.csv')
        data_art = pd.DataFrame(np.array(data), columns=['name', 'href', 'tags', 'class'])
        data_art.to_csv(full_path)
        print('Data written successfully CSV')
