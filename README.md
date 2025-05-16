# Thesis

Для запуска требуется копировать данные из `.env.excample` в `.env` файл.
Если нужно использовать стандартную базу данных, то нужно закоментировать блок с базой данных

Для запуска в докере нужно выполнить эту команду
```shell
docker compose up --build -d
```

Если же нужно запустить само приложение, то нужно создать виртуальную среду и установить зависимости из `requirements.txt`
```shell
python -m venv .venv

.venv/Scripts/activate # для windows
source venv/bin/activate # для linux и mac

pip install -r requirements.txt
```

После чего нужно либо выключить режим отладки и запустить приложение, либо же запустить так
```shell
python manage.py runserver --insecure
```
