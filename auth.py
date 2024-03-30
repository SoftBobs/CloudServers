from openstack import connection
import configparser
import pymysql


# Функция для подключения к базе данных MySQL
def db_connect():
    # Чтение конфигурационного файла для получения данных о подключении к базе данных
    config = configparser.ConfigParser()
    config.read('auth_config.ini')

    # Извлечение данных о подключении из файла конфигурации и попытка подключения к базе
    db_config = {
        "host": config['database']['host'],
        "user": config['database']['user'],
        "password": config['database']['password'],
        "database": config['database']['database'],
    }

    try:
        # Создание подключения к базе данных
        connection = pymysql.connect(**db_config)
        # Создание курсора для выполнения SQL-запросов
        cursor = connection.cursor()
        # Возвращаем курсор и подключение
        return cursor, connection
    except pymysql.MySQLError as e:
        # В случае ошибки подключения, выводим сообщение об ошибке
        print(f"Ошибка подключения к базе данных: {e}")
        # Возвращаем None для обоих значений, чтобы указать на ошибку
        return None, None


# Функция для аутентификации в OpenStack
def openstack_auth():
    # Получаем курсор и подключение к базе данных
    cursor, db_connection = db_connect()
    if cursor is None:
        # Если подключение не удалось, возвращаем None
        return None

    try:
        # Выполняем запрос на выборку данных для аутентификации в OpenStack
        cursor.execute(
            "SELECT auth_url, project_name, project_domain_name, user_domain_name, username, password, auth_type FROM AuthConfigs LIMIT 1")
        auth_data = cursor.fetchone()

        # Закрываем курсор и соединение с базой данных
        cursor.close()
        db_connection.close()

        # Если данные аутентификации найдены
        if auth_data:
            # Формируем словарь с параметрами для подключения к OpenStack
            auth = {
                "auth_url": auth_data[0],
                "project_name": auth_data[1],
                "project_domain_name": auth_data[2],
                "user_domain_name": auth_data[3],
                "username": auth_data[4],
                "password": auth_data[5],
                "auth_type": auth_data[6]
            }

            try:
                # Инициализация подключения к OpenStack
                conn = connection.Connection(**auth)
                # Авторизация в OpenStack
                conn.authorize()
                # Возвращаем объект подключения, если аутентификация прошла успешно
                return conn
            except Exception as e:
                # В случае ошибки аутентификации, выводим сообщение об ошибке
                print(f"Ошибка аутентификации: {e}")
                return None
    except pymysql.MySQLError as e:
        # В случае ошибки выполнения запроса, выводим сообщение об ошибке
        print(f"Ошибка при выполнении запроса к базе данных: {e}")
        return None

def authenticate_user(login, password):
    # Пытаемся установить соединение с базой данных
    cursor, db_connection = db_connect()
    if cursor is None:
        # Если соединение не установлено, возвращаем None
        return None

    try:
        # Выполняем запрос к базе данных для проверки существования пользователя с данным логином и паролем
        cursor.execute(
            "SELECT first_name FROM students WHERE login=%s AND password=%s "
            "UNION "
            "SELECT first_name FROM teachers WHERE login=%s AND password=%s",
            (login, password, login, password)
        )
        # Получаем результат выполнения запроса
        user_data = cursor.fetchone()
        # Закрываем соединение с базой данных
        cursor.close()
        db_connection.close()

        # Проверяем, получены ли данные пользователя
        if user_data:
            # Если учетные данные верны, пытаемся выполнить аутентификацию в OpenStack
            if openstack_auth():
                # В случае успешной аутентификации возвращаем имя пользователя
                return user_data[0]
    except pymysql.MySQLError as e:
        # В случае ошибки выполнения запроса выводим сообщение об ошибке
        print(f"Ошибка при выполнении запроса к базе данных: {e}")
    # Если аутентификация не удалась, возвращаем None
    return None

def authenticate():
    # Пытаемся выполнить аутентификацию в OpenStack и возвращаем результат в виде булева значения
    conn = openstack_auth()
    return bool(conn)

