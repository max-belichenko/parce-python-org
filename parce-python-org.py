""" 
Тестовое задание:

Разработайте скрипт на Python, который будет выводить в консоль (STDOUT) информацию о предстоящих событиях анонсированных на главной странице python.org (Upcoming Events). 
Вывод информации оформите по своему усмотрению. 
Выбор библиотек на ваше усмотрение. 
"""

from bs4 import BeautifulSoup
import requests


# Адрес запрашиваемой страницы
URL = 'http://www.python.org/'

# Тег, содержащий необходимую информацию
TAG = 'div'

# Класс тега, содержащего необходимую информацию
TAG_CLASS = 'medium-widget event-widget last'


def get_page(url: str):
	"""
	Получает страницу по указанному URL.

	:param url: URL страницы
	:return: :class:`Response <Response>` object
	"""
	return requests.get(URL)


def parse_page(page, tag, tag_class):
	"""
	Проводит разбор HTML-страницы: ищет тег "tag" с параметром class="tag_class".

	:param page: :class:`Response <Response>` object
	:param tag: <str>
	:param tag_class: <str>
	:return: A PageElement.
	:rtype: bs4.element.Tag | bs4.element.NavigableString
	"""
	if page.status_code == 200:		# Страница получена успешно
		# Разобрать страницу как HTML
		soup = BeautifulSoup(page.text, "html.parser")

		# Найти тег <div class="medium-widget event-widget last">
		element = soup.find(name=tag, class_=tag_class)
	else:  							# При получении страницы возникла ошибка
		print(f'При получении страницы {URL} возникла ошибка {page.status_code}.')
		element = None

	return element


def print_python_org_events(element):
	"""
	Производит дополнительный разбор данных и вывод на экран.

	Пример HTML-данных:
		<li>
			<time datetime="2020-01-11T00:00:00+00:00"><span class="say-no-more">2020-</span>01-11</time>
			<a href="/events/python-user-group/886/">Yola Python Club 2020</a>
		</li>

	Пример вывода:
		   DATE                EVENT              LINK
		2020-08-28 PyCon JP 2020                  http://www.python.org/events/python-events/951/
		2020-09-05 PyCon TW 2020                  http://www.python.org/events/python-events/963/
		2020-09-11 PyCon SK 2020                  http://www.python.org/events/python-events/879/

	:param element: A PageElement.
	:return: None
	"""
	if element is not None:
		# Вывести заголовок таблицы
		print('{:^10} {:^30} {:<50}'.format('Дата', 'Событие', 'Ссылка на событие'))

		# Найти все теги <li>
		for li in element.find_all('li'):
			# Найти тег <time> и получить значение параметра datetime
			date = li.find('time').get('datetime')

			# Найти тег <a>
			a = li.find('a')

			# Получить текст, заключённый внутри тега <a>текст</a>
			event = a.string

			# Получить ссылку, указанную в параметре href
			link = a.get('href')

			# Сформировать строку и вывести её на экран
			print('{:<10} {:<30} {:<50}'.format(date[:10], event, URL[:-1] + link))


if __name__ == '__main__':
	# Получить страницу по заданному URL
	page = get_page(URL)

	# Разобрать страницу и получить необходимые данные
	data = parse_page(page, TAG, TAG_CLASS)

	# Вывести результат на экран
	print_python_org_events(data)



