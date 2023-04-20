from _types.database_types import _DB_TYPE

def setup():

    print("Средство настройки проекта")
    print("Выберите бэкенд для базы данных\n1.SQLite\n2.PostgreSQL")



    type_of_db = _DB_TYPE.SQLite

    try:
        type_of_db = int(input("Введите тип базы данных (SQLite по умолчанию): "))
        assert(type_of_db in (1,2))
    except Exception:
        type_of_db = _DB_TYPE.SQLite
        print("Настраиваю .env для SQLite")

    lines = []

    if type_of_db == _DB_TYPE.SQLite:
        lines.append(f"DB_TYPE={type_of_db}")
    else:
        user = input("Введите имя пользователя Postgres: ")
        db_name = input("Введите название базы данных: ")
        
        lines.extend(
            [f"DB_TYPE={type_of_db}\n",
            f"USER={user}\n",
            f"DB_NAME={db_name}\n"]
        )

    with open(".env", "w") as env_file:
        env_file.writelines(lines)

if __name__ == "__main__":
    setup()