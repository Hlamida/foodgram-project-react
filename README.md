# praktikum_new_diplom

# foodgram


### Документация проекта:


http://localhost/api/docs/


### Предназначение проекта:

Ваш проект — сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Как запустить проект:

Клонировать репозиторий:

```
git clone https://git@github.com:Hlamida/foodgram-project-react.git
```

Создать secrets в своём репозитории: 
1. Перейти в настройки репозитория Settings, выбрать на панели слева Secrets, нажать New secret.
2. Сохранить переменные с необходимыми значениями.

Для работы с Docker Hub:
- DOCKER_USERNAME;
- DOCKER_PASSWORD.

Для деплоя и авторизации на удалённом сервере:
- HOST;
- USER;
- SSH_KEY;
- PASSPHRASE.

Для работы базы данных:
- DB_ENGINE;
- DB_NAME;
- POSTGRES_USER;
- POSTGRES_PASSWORD;
- DB_HOST;
- DB_PORT;
- SECRET_KEY.

3. Скорректировать значения соответствующих переменных в файле foodgram-project-react/infra/.env

4. Подготовить удалённый сервер к работе:
- войти на свой сервер;
- остановить службу nginx:
```
sudo systemctl stop nginx 
```
- установить docker:
```
sudo apt install docker.io 
```
- установить docker-compose в соответствии с документацией
https://docs.docker.com/compose/install/

- скопировать файлы docker-compose.yaml и nginx/ngnix.conf из проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/ngnix.conf соответственно.


6. Загрузить тестовую базу можно подключившись к терминалу сервера и выполнив команду: 
```
sudo docker-compose exec -T web python manage.py loaddata fixtures.json 
```

7. Адрес сервера 158.160.27.175
   Логин / пароль администратора: kulagin / kulagin
   
### Технологии:

Проект сделан на Django и DRF.

### Об авторах:

Автор: Александр Кулагин
