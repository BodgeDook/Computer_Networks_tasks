Структура проекта:

- main.py && parser.py (основные файлы программы)
- geckodriver.exe (нужен для парсинга сайта на Firefox, используется последняя версия 0.36.0)
- cnn_news.dump (база данных, полученных с помощью парсинга API точки сайта, служит как пример работы программы)
- news_data.json (json - форат "пропарсенных" данных)
- results.txt (обычный показл полученных данных во время парсинга сайта)
- requirements.txt (файл зависимостей проекта)
- README.md (подробная инструкция к работе с программой для парсинга сайтов через API точку и PostgreSQL)

Для начала работы вы должны скачать PostgreSQL, сделать там свой пароль админа и создать первую базу данных для
хранения полученной информации с сайта:
	
	psql postgres -U
	
	CREATE DATABASE cnn_news
	
	\l # чтобы убедиться, что база данных существует

	\q # чтобы выйти из PostgreSQL

После этого базу данных можно закрыть. Далее Вы должны зарегистироваться на CNN (нашем сайте для парсинга), и Ваши
пароль и почту нужно будет внести в переменные PASSWORD и EMAIL в файле parser.py. Также все данные Вашей СУБД Вы
должны внести в файл main.py в словарь DATABASE, чтобы API точка успешно подключилась к Вашей локальной базе данных.

Затем нужно запустить основной файл программы с помощью следующей программы (асинхр. работа API точки):
	
	uvicorn main:app --reload

Парсим мы новостной американский сайт CNN news, поэтому вызовем парсинг через curl, пройдя несложную авторизацию:

	curl "http://127.0.0.1:8000/parse?url=https://edition.cnn.com/account/log-in"

После того, как нам придёт статут об успешном окончании работы в консоль, можно будет получить json-формат полученных
данных (они лежат в самой cnn_news):
	
	curl http://127.0.0.1:8000/news -o news_data.json

/news вызовет метд извлечения данных из СУБД, а -o news_data.json сформирует эти данные в json-формате.
чтобы посмотреть результат, можно просмотреть саму базу данных. для этого можете написать:
	
	psql -U username -d cnn_news
	SELECT * FROM cnn_news;
	\q

Также я приложу файл requirements.txt со всеми зависимостями для проекта, который Вы должны будете установить с
помощью команды:

	pip install -r requirements.txt

Для работы всего проекта можете использовать PyCharm, но я рекомендую просто создать обычное виртуальное окружение
через virtualenv, дабы проект не занимал много места на диске компьютера (проекты PyCharm бывают довольно 'жирными'
из-за капризности и тяжести самой среды разработки).
