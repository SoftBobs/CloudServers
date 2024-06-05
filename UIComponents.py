from ServerOperations import stop_server, check_server_status, create_server, get_configurations, get_images, delete_server, start_server
from tkinter import messagebox, ttk, Tk, Canvas
import tkinter as tk
from resource_path_resolver import get_resource_path

# Предположим, что нужен путь к файлу 'service-types.json'
service_types_json_path = get_resource_path()

# Флаг успешной аутентификации
authenticated = False

# Отображение главного окна приложения
def show_main_window(root):
    # Создаем меню для выбора конфигурации и образов сервера и другие элементы интерфейса
    create_configuration_menu(root)
    create_image_menu(root)
    create_create_button(root)

# Создание меню выбора конфигурации сервера
def create_configuration_menu(root):
    global configuration_var, configurations_dict  # Глобальные переменные для хранения выбора пользователя

    # Добавляем метку и выпадающий список для выбора конфигурации
    configuration_label = ttk.Label(root, text="Выберите конфигурацию:")
    configuration_label.pack(pady=10)

    # Получаем конфигурации из базы данных
    configurations = get_configurations()
    configurations_dict = {"Конфигурация сервера": None}  # Инициализация словаря для хранения конфигураций
    for name, flavor_id in configurations:
        configurations_dict[name] = flavor_id

    configuration_var = tk.StringVar(root)
    configuration_var.set("Конфигурации серверов")  # Значение по умолчанию для выпадающего списка

    # Создаем выпадающий список с доступными конфигурациями
    configuration_menu = ttk.OptionMenu(root, configuration_var, *configurations_dict.keys())
    configuration_menu.pack(pady=5)

# Создание меню выбора образа сервера
def create_image_menu(root):
    global image_var, images_dict  # Глобальные переменные для хранения выбора пользователя

    # Добавляем метку и выпадающий список для выбора образа сервера
    image_label = ttk.Label(root, text="Выберите образ:")
    image_label.pack(pady=10)

    # Получаем образы из базы данных
    images = get_images()
    images_dict = {"Образ сервера": None}  # Инициализация словаря для хранения образов
    for name, image_id in images:
        images_dict[name] = image_id

    image_var = tk.StringVar(root)
    image_var.set("Образы серверов")  # Значение по умолчанию для выпадающего списка

    # Создаем выпадающий список с доступными образами
    image_menu = ttk.OptionMenu(root, image_var, *images_dict.keys())
    image_menu.pack(pady=5)

def update_status_label(status_label, server_id):
    try:
        status = check_server_status(server_id)
        if status == "ACTIVE":
            color = "green"
        elif status == "ERROR":
            color = "red"
        elif status == "SHUTOFF":
            color = "gray"
        else:
            color = "yellow"

        status_label.itemconfig(1, fill=color)
        after_id = status_label.after(3000, update_status_label, status_label, server_id)
        if not hasattr(status_label, 'after_ids'):
            status_label.after_ids = []
        status_label.after_ids.append(after_id)
    except Exception as e:
        print(f"Произошла ошибка при проверке статуса сервера: {e}")


def create_create_button(root):
    # Создаем кнопку "Создать сервер", при нажатии на которую будет вызвана функция show_server_window
    create_button = ttk.Button(root, text="Создать сервер", command=lambda: show_server_window(root, configuration_var.get(), image_var.get()))
    create_button.pack(pady=10)


def show_server_window(root, selected_configuration_name, selected_image_name):
    # Получение идентификаторов для выбранной конфигурации и образа сервера из глобальных словарей
    flavor_id = configurations_dict.get(selected_configuration_name)
    image_id = images_dict.get(selected_image_name)

    # Проверка, что пользователь выбрал и конфигурацию, и образ сервера
    if not flavor_id or not image_id:
        # Если одно из значений не выбрано, показываем ошибку и прерываем выполнение функции
        messagebox.showerror("Ошибка", "Конфигурация сервера или образ не выбран или не найден.")
        return

    # Попытка создать сервер с указанными параметрами
    server_info = create_server(flavor_id, image_id)
    # Если сервер успешно создан, получаем его данные: идентификатор, имя и IP-адрес
    if server_info:
        server_id, server_name, server_ip = server_info

        # Закрытие текущего окна интерфейса
        root.destroy()
        # Создание нового окна для управления сервером
        server_window = Tk()
        server_window.geometry("610x350")
        server_window.title("Управление сервером")

        # Настройка стилей элементов интерфейса
        s = ttk.Style()
        s.configure('My.TButton', font=('Verdana', 14))
        s.configure('My.TLabel', font=('Verdana', 14))

        # Создание и размещение элементов, отображающих информацию о сервере
        server_info_frame = ttk.Frame(server_window, padding=10)
        server_info_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(server_info_frame, text=f"Сервер: {server_name}", style='My.TLabel').pack(pady=10)
        ttk.Label(server_info_frame, text="IP адрес:", style='My.TLabel').pack()
        ttk.Label(server_info_frame, text=server_ip, foreground="blue", style='My.TLabel').pack(pady=10)

        # Размещение инструкций для пользователя о том, как подключиться к серверу
        instructions_frame = ttk.Frame(server_window, padding=10)
        instructions_frame.pack(side='left', fill='both', expand=True)
        instructions_label = ttk.Label(
            instructions_frame,
            text="Дождитесь создания сервера.\nПодключайтесь по RDP к Windows.\nИ по SSH к Linux.\nИспользуйте ваш логин и пароль.",
            style='My.TLabel'
        )
        instructions_label.pack(pady=10)

        # Создание и размещение кнопок для управления состоянием сервера (удаление, выключение)
        status_label = Canvas(server_info_frame, width=20, height=20)
        status_label.pack(side='top', pady=10)
        status_label.create_oval(2, 2, 18, 18, fill="yellow")  # Начальный цвет - жёлтый
        update_status_label(status_label, server_id)
        server_info_frame.status_label = status_label  # Сохраняем ссылку на status_label в server_info_frame

        start_button = ttk.Button(server_info_frame, text="Включить сервер", style='My.TButton',
                                  command=lambda: start_server_and_check_status_gui(server_id, server_info_frame))
        start_button.pack(side='top', pady=10, fill='x')
        stop_button = ttk.Button(server_info_frame, text="Выключить сервер", style='My.TButton',
                                 command=lambda: stop_server_and_check_status_gui(server_id, status_label))
        stop_button.pack(side='top', pady=10, fill='x')
        delete_button = ttk.Button(server_info_frame, text="Удалить сервер", style='My.TButton',
                                   command=lambda: delete_server_and_check_status_gui(server_id, server_info_frame))
        delete_button.pack(side='top', pady=10, fill='x')

        # Запуск главного цикла обработки событий интерфейса
        server_window.mainloop()
    else:
        # Если сервер создать не удалось, показываем сообщение об ошибке
        messagebox.showerror("Ошибка", "Не удалось создать сервер.")

def stop_server_and_check_status_gui(server_id, status_label):
    status = check_server_status(server_id)
    if status == "ACTIVE":
        messagebox.showinfo("Информация", "Сервер выключается...")
        stop_server(server_id)
        status_label.after(5000, lambda: verify_stop_gui(server_id, status_label))
    elif status == "SHUTOFF":
        messagebox.showinfo("Сервер выключен", "Сервер успешно выключен.")
    else:
        messagebox.showinfo("Информация", "Сервер все еще выключается.")
        status_label.after(20000, lambda: verify_stop_gui(server_id, status_label))

def verify_stop_gui(server_id, status_label):
    final_status = check_server_status(server_id)
    if final_status == "SHUTOFF":
        messagebox.showinfo("Сервер выключен", "Сервер успешно выключен.")
    else:
        messagebox.showinfo("Информация", "Сервер все еще выключается.")
        status_label.after(20000, lambda: verify_stop_gui(server_id, status_label))


def delete_server_and_check_status_gui(server_id, server_info_frame):
    # Проверяем текущий статус сервера перед попыткой его удаления
    status = check_server_status(server_id)
    if status == "ACTIVE" or status == "SHUTOFF":
        # Если сервер активен или уже выключен, пытаемся его удалить
        if delete_server(server_id):
            # Успешное удаление сервера
            messagebox.showinfo("Информация", "Сервер успешно удален.")

            # Отменяем запланированные вызовы update_status_label
            if hasattr(server_info_frame, 'status_label') and hasattr(server_info_frame.status_label, 'after_ids'):
                for after_id in server_info_frame.status_label.after_ids:
                    server_info_frame.status_label.after_cancel(after_id)

            # Закрываем окно управления сервером и возвращаем пользователя к главному окну приложения
            server_window = server_info_frame.master
            server_window.destroy()
            root = tk.Tk()
            root.geometry("300x300")
            root.title("OpenStack Управление")
            show_main_window(root)
        else:
            # Не удалось удалить сервер
            messagebox.showerror("Ошибка", "Не удалось удалить сервер.")
    else:
        # Сервер находится в промежуточном состоянии, невозможно удалить
        messagebox.showinfo("Информация", "Сервер ещё создаётся или находится в промежуточном состоянии.")

def start_server_and_check_status_gui(server_id, server_info_frame):
    status = check_server_status(server_id)
    if status == "ACTIVE":
        messagebox.showinfo("Информация", "Сервер уже работает.")
    elif status == "SHUTOFF":
        messagebox.showinfo("Информация", "Включение сервера...")
        start_status_label = ttk.Label(server_info_frame, text="Включение сервера...", style='My.TLabel')
        start_status_label.pack(side='bottom', pady=10)
        start_server(server_id)
        server_info_frame.after(5000, lambda: verify_start_gui(server_id, start_status_label))
    else:
        messagebox.showinfo("Информация", f"Сервер находится в состоянии {status}. Подождите завершения текущего процесса.")

def verify_start_gui(server_id, start_status_label):
    status = check_server_status(server_id)
    if status == "ACTIVE":
        messagebox.showinfo("Информация", "Сервер успешно запущен.")
        start_status_label.destroy()
    else:
        messagebox.showinfo("Информация", f"Сервер ещё включается")
        start_status_label.after(25000, lambda: verify_start_gui(server_id, start_status_label))

