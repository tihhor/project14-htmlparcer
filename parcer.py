import requests
from bs4 import BeautifulSoup
import time


def curr_parcer(cur_to_print, date_to_print):

    cur_to_print = cur_to_print.split()

    try:
      valid_date = time.strptime(date_to_print, '%d.%m.%Y')
      url = 'http://cbr.ru/currency_base/daily/?date_req=' + date_to_print
    except ValueError:
      print('Неверная дата! Использую текущую дату.')
      url = 'http://cbr.ru/currency_base/daily/'


    response = requests.get(url)

    #print(response.status_code)

    #print(response.text)

    # Создаем суп для разбора html
    soup = BeautifulSoup(response.text, 'html.parser')

    answer = []

    # Поиск текста по тегу

    text_date = soup.find('h2').text
    text_date = ' '.join(text_date.split())
    # print(text_date)
    answer.append(text_date)

    #поиск таблицы курсов валют по классу

    table = soup.find('table', class_='data')

    currencies = table.find_all('tr')

    #разбираем строки таблицы
    for currency in currencies:
        data = currency.find_all('td')
        counter = 0
        for cur_data in data:
            if cur_data.text in cur_to_print:       # если код валюты в списке на печать
                counter += 1
                curr_code = cur_data.text           # запоминаем код валюты
                continue
            elif counter == 1:
                counter += 1
                curr_mult = int(cur_data.text)      # запоминаем количество единиц валюты
                continue
            elif counter == 2:
                counter += 1
                curr_name = cur_data.text           # запоминаем наименование валюты
                continue
            elif counter == 3:
                counter = 0
                cur_rate = round(float(cur_data.text.replace(',', '.'))/curr_mult, 4)   #приводим курс к единице валюты к рублю
                #print(curr_code, curr_name, cur_rate, 'руб.')
                answer.append(curr_code+' '+curr_name+' '+f'{cur_rate:.4f}'+' руб.')

    return answer


if __name__ == '__main__':

    cur_to_print = input('Введите коды валют для получения текущих курсов (USD EUR ...): ')
    date_to_print = input('Введите дату ДД.ММ.ГГГГ:')
    ans = curr_parcer(cur_to_print, date_to_print)
    for str_ans in ans:
        print(str_ans)
