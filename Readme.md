# MediaSoft Python Test Task

### Выполнил Аксенов Иван - студент УлГУ 1 курса

## Задание

Реализовать сервис который принимает и отвечает на HTTP запросы

## Подготовка к запуску

1. __Установите Python, PIP и Postgresql__

    - ## Arch Linux
        
        ```bash
        pacman -Syuy python python-pip postgresql
        ```


2. __Запустите сервер Postgresql__
    
    Эту часть можно пропустить если вы планируете использовать SQLite

    - ## Настройка на Arch Linux
        ### Переключение в пользователя postgres
        
        ```bash
        sudo -iu postgres
        ```

        ### Инициализация кластера базы данных
        
        ```bash
        [postgres]$ initdb -D /var/lib/postgres/data
        ```

        ### Включение и запуск службы Postgresql

        ```bash
        [postgres]$ systemctl.enable postgresql
        [postgres]$ systemctl.start postgresql
        ```

        ### Создание пользователя 

        ```bash
        [postgres]$ createuser --interactive
        ```
       
        ### Создание базы данных

        ```bash
        [postgres]$ createdb <имя вашей базы данных>
        ```
        ### __ВНИМАНИЕ__
        Запомните имя юзера и имя базы данных, дальше оно нам пригодится для настройки .env файла


3. __Склонируйте репозиторий__

    ```bash
    git clone "https://github.com/itc1205/mediasoft_test_task.git"
    ```

4. __Перейдите в корень проекта__

    ```bash
    cd mediasoft_test_task
    ```


5. __Установите необходимые пакеты__
    
    ```bash
    pip install -r requirements.txt
    ```


## __Запуск__
1. Для первоначального запуска необходимо выставить .env переменные, это можно сделать с помощью небольшого скрпита
    ```bash
    python configure_env.py
    ```

    Либо можно самим создать в корне проекта .env файл

    Примеры .env:

    - Для SQLite
        ```env
        DB_TYPE=0
        ```
    - Для PostgreSQL
        ```env
        DB_TYPE=1
        USER=<имя пользователя в постгрес>
        DB_NAME=<имя базы данных>
        ```
        __ВНИМАНИЕ__
        
        Предпологается что PostgreSQL работает на сокете 
        `/run/postgresql/`, если используется что либо другое то необходимо поменять кейворд на строке 36 в файле `data/db_session.py` на необходимый

2. Для запуска приложения введите в консоли

    ```bash
    python main.py
    ```

3. Что бы получить доступ к приложению перейдите по ссылке

    http://127.0.0.1:8080

## Документация

Дополнительная документация по использованию находится в папке `routes`
