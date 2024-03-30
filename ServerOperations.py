import random
import string
from auth import openstack_auth, db_connect

def get_images():
    # Установление соединения с базой данных
    cursor, db_connection = db_connect()
    # Проверка успешности установления соединения
    if cursor is None:
        # Возвращаем пустой список, если соединение не установлено
        return []

    try:
        # Выполнение SQL-запроса на получение имени и идентификатора образа из таблицы Images
        cursor.execute("SELECT image_name, openstack_id FROM Images")
        # Получение всех результатов запроса
        images = cursor.fetchall()
    except Exception as e:
        # В случае возникновения ошибки выводим сообщение об ошибке и возвращаем пустой список
        print(f"Ошибка при получении списка образов: {e}")
        images = []

    # Закрытие соединения с базой данных
    cursor.close()
    db_connection.close()
    # Возвращение списка образов
    return images

def get_configurations():
    # Установление соединения с базой данных
    cursor, db_connection = db_connect()
    # Проверка успешности установления соединения
    if cursor is None:
        # Возвращаем пустой список, если соединение не установлено
        return []

    try:
        # Выполнение SQL-запроса на получение имени и идентификатора конфигурации из таблицы Configurations
        cursor.execute("SELECT configuration_name, openstack_id FROM Configurations")
        # Получение всех результатов запроса
        configurations = cursor.fetchall()
    except Exception as e:
        # В случае возникновения ошибки выводим сообщение об ошибке и возвращаем пустой список
        print(f"Ошибка при получении списка конфигураций: {e}")
        configurations = []

    # Закрытие соединения с базой данных
    cursor.close()
    db_connection.close()
    # Возвращение списка конфигураций
    return configurations


def create_server(flavor_id, image_id):
    # Аутентификация в OpenStack для получения соединения
    conn = openstack_auth()
    # Проверяем, успешно ли была произведена аутентификация
    if conn is None:
        # Возвращаем тройку None, если соединение не установлено
        return None, None, None

    # Генерация случайного имени для сервера
    server_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    # Идентификатор образа для создания сервера
    image_uuid = image_id
    # UUID сети, к которой будет подключен сервер
    network_uuid = "75bbd2e4-42ea-4c3a-8319-ac6ae2db5633"

    # Словарь параметров для создания сервера
    create_kwargs = {
        'name': server_name,  # Имя сервера
        'flavorRef': flavor_id,  # Конфигурация
        'imageRef': image_uuid,  # Образ
        'networks': [{'uuid': network_uuid}],  # Сеть для подключения
        'key_name': "MyKeySSH",  # Имя SSH ключа для доступа
        'max_count': 1,  # Максимальное количество создаваемых экземпляров
        'min_count': 1,  # Минимальное количество создаваемых экземпляров
        'block_device_mapping_v2': [{  # Конфигурация хранилища
            "uuid": image_uuid,
            "source_type": "image",
            "destination_type": "volume",
            "boot_index": 0,
            "volume_size": "80",  # Размер виртуального диска в гигабайтах
            "delete_on_termination": True  # Удаление диска при удалении сервера
        }],
        'terminate_on_shutdown': True  # Автоматическое удаление сервера при выключении
    }

    try:
        # Создание сервера с указанными параметрами
        server = conn.compute.create_server(**create_kwargs)
        # Ожидание завершения создания сервера
        server = conn.compute.wait_for_server(server)

        # Получение публичного IP-адреса сервера
        server_ip = None
        for network in server.addresses.values():
            for address in network:
                if address['OS-EXT-IPS:type'] == 'fixed':  # Проверка типа адреса
                    server_ip = address['addr']
                    break
            if server_ip:
                break

        # Вывод информации о созданном сервере
        print(f"Сервер успешно создан: {server.name} с IP {server_ip}")
        # Возвращаем идентификатор, имя и IP-адрес сервера
        return server.id, server.name, server_ip
    except Exception as e:
        # В случае ошибки при создании сервера выводим сообщение об ошибке
        print(f"Произошла ошибка при создании сервера: {e}")
        return None, None, None  # Возвращаем тройку None в случае ошибки


def delete_server(server_id):
    try:
        # Попытка аутентификации в OpenStack для получения соединения
        conn = openstack_auth()
        if conn is not None:
            # Если соединение успешно, пытаемся удалить сервер по его идентификатору
            server = conn.compute.delete_server(server_id)
            print(f"Сервер {server_id} успешно удалён.")
            return True  # Возвращаем True в случае успешного удаления
        else:
            # Если соединение не удалось, выводим сообщение об ошибке
            print("Не удалось установить подключение к OpenStack.")
            return False  # Возвращаем False, если не удалось установить соединение
    except Exception as e:
        # Обработка возможных исключений и вывод сообщения об ошибке
        print(f"Произошла ошибка при удалении сервера: {e}")
        return False  # Возвращаем False в случае возникновения исключения

def stop_server(server_id):
    try:
        # Аутентификация в OpenStack для получения соединения
        conn = openstack_auth()
        if conn is not None:
            # Остановка сервера по его идентификатору
            conn.compute.stop_server(server_id)
            print("Сервер успешно остановлен.")
        else:
            # Сообщение об ошибке, если не удалось установить соединение
            print("Не удалось установить подключение к OpenStack.")
    except Exception as e:
        # Обработка возможных исключений и вывод сообщения об ошибке
        print(f"Произошла ошибка при остановке сервера: {e}")

def check_server_status(server_id):
    try:
        # Аутентификация в OpenStack для получения соединения
        conn = openstack_auth()
        if conn is not None:
            # Получение информации о сервере по его идентификатору
            server = conn.compute.get_server(server_id)
            # Возвращение статуса сервера, например, "SHUTOFF" для выключенного сервера
            return server.status
    except Exception as e:
        # Обработка возможных исключений и вывод сообщения об ошибке
        print(f"Произошла ошибка при проверке статуса сервера: {e}")
        return None  # Возвращаем None в случае ошибки


