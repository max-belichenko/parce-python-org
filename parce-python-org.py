""" 
Тестовое задание:

Разработайте скрипт на Python, который будет выводить в консоль (STDOUT) информацию о предстоящих событиях анонсированных на главной странице python.org (Upcoming Events). 
Вывод информации оформите по своему усмотрению. 
Выбор библиотек на ваше усмотрение. 

Копия страницы python.org/index.html на 29.12.2019 прилагается.
"""

from bs4 import BeautifulSoup
import requests as r

url = 'http://www.python.org/'

page = r.get(url)
if page.status_code == 200:	# Check HTTP answer. 200 is OK
	print('GET {} successful {}'.format(url, str(page.status_code)))
else:	
	print('GET {} failed with status {}'.format(url, str(page.status_code)))
	sys.exit(1)

soup = BeautifulSoup(page.text, "html.parser")	# Parce page text with html parcer
events_div = soup.find(name='div', class_='medium-widget event-widget last')	# Find tag <div class="medium-widget event-widget last> 

print('{:^10} {:^30} {:<50}'.format('DATE', 'EVENT', 'LINK'))
for li in events_div.find_all('li'):	# Find <li> tags inside <div>
	date = li.find('time').get('datetime')	# From <time> tag get datetime value
	event = li.find('a').string	# From <a> tag get text string
	link = li.find('a').get('href')	# From <a> tag get href value
	print('{:<10} {:<30} {:<50}'.format(date[:10], event, url+link[1:]))

