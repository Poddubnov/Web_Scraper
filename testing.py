import unittest
from avito_parcer_cars import *


class MyTestCase(unittest.TestCase):
    def testResponse(self, url='https://www.avito.ru/volgograd/avtomobili?radius=200&q=toyota&p=7'):
        """
        Тест на ответ сервера
        :param url: ссылка
        :return: None
        """
        self.assertEqual(requests.get(url).status_code, 200, msg="Нет ответа от сервера")

    def testCountPages(self, url='https://www.avito.ru/volgograd/avtomobili?radius=200&q=toyota&p=7'):
        """
        Тест на актуальное количество страниц
        :param url: ссылка
        :return: None
        """
        self.assertEqual(get_total_pages(get_html(url)), 12, msg="Ожидалось другое количество страниц на сайте")


if __name__ == '__main__':
    unittest.main()
