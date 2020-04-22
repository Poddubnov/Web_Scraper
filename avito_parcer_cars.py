import requests  # библиотека для работы с запросами
from bs4 import BeautifulSoup  # библиотека для работы с парсингом HTML
import csv  # библиотека для работы с CSV-файлами


# План работы:
# 1. Выяснить количество страниц
# 2. Сформировать список url-ов на страницы выдачи
# 3. Собрать данные

def get_html(url):
    """
    Функция получения html-кода страницы
    :param url: url-страницы, к которой надо обратиться
    :return: весь html-код страницы
    """
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    """
    Функция получения количества страниц для выбранной категории
    :param html: получаем html-код страницы
    :return: количество страниц
    """
    soup = BeautifulSoup(html, 'lxml')  # Создание объекта soup,
    # конструктор принимает сам html и парсер, который будет принимать и применяться

    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    # объект soup ищет контейнер div с классом 'pagination-pages', в котором ищем ссылку на последнюю страницу
    # оттуда берём аргумент 'href'

    total_pages = pages.split('=')[1].split('&')[0]
    # получившаеся строка разделяется по знаку "=", берётся второй элемент списка
    # затем вновь делится по знаку "&" и берётся первый элемент списка, где находится номер последней странциы

    return int(total_pages)


def write_csv(data):
    """
    Функция записи данных в файл .CSV
    :param data: "Распарсенная" информация со страницы
    :return: none
    """
    with open('avito_cars_vlg.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['title'],
                         data['price'],
                         data['params'],
                         data['url']))


def get_page_data(html):
    """
    Функция получения краткой информации об объявлении
    :param html: Сгенерированная ссылка html
    :return: none
    """
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='snippet-list').find_all('div', class_='item_table')
    # Получаем все доступные краткие объявления на странице
    for ad in ads:
        broken_car = ad.find('div', class_='description item_table-description').find('div',
                                                                                      class_='specific-params specific-params_block').text.strip()
        if 'Битый' not in broken_car:
            # Мы исключаем из парсинга все битые машины
            try:
                title = ad.find('h3', class_='snippet-title').text
            except:
                title = ''

            try:
                url = 'https://www.avito.ru' + ad.find('div', class_='description item_table-description').find('div',
                                                                                                                class_='snippet-title-row').find(
                    'a').get('href')
            except:
                url = ''

            try:
                price = \
                    ad.find('div', class_='description item_table-description').find('a', class_='snippet-link').get(
                        'title').split(',')[3].split('-')[0]
            except:
                price = ''

            try:
                params = ad.find('div', class_='description item_table-description').find('div',
                                                                                          class_='specific-params specific-params_block').text.strip()
            except:
                params = ''

            data = {'title': title,
                    'price': price,
                    'params': params,
                    'url': url}
            # Выводим информацию в словарь
            write_csv(data)
            # обращение к функции записи информации в файл .CSV
        else:
            continue


def main():
    url = 'https://www.avito.ru/volgograd/avtomobili?radius=200&q=toyota&p=7'
    base_url = 'https://www.avito.ru/volgograd/avtomobili?'  # неизменяемая часть url
    radius_part = 'radius=200'
    query_part = '&q=toyota&'
    page_part = 'p='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages + 1):
        url_generate = base_url + radius_part + query_part + page_part + str(i)
        html = get_html(url_generate)
        get_page_data(html)


if __name__ == '__main__':
    main()
