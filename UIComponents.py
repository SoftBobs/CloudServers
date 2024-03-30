from ServerOperations import stop_server, check_server_status, create_server, get_configurations, get_images, delete_server
from tkinter import messagebox, ttk, Tk
import tkinter as tk

# Флаг успешной аутентификации
authenticated = False

# Отображение главного окна приложения
def show_main_window(root):
    # Создаем меню для выбора конфигурации и образов сервера и другие элементы интерфейса
    create_configuration_menu(root)
    create_image_menu(root)
    create_status_label(root)
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

def create_status_label(root):
    # Создаем метку без текста, которая может быть использована для отображения статусных сообщений
    status_label = ttk.Label(root, text="")
    status_label.pack(pady=20)

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
        server_window.geometry("610x310")
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
        status_label = ttk.Label(server_info_frame, text="Статус сервера", style='My.TLabel')
        status_label.pack(side='top', pady=10)
        delete_button = ttk.Button(server_info_frame, text="Удалить сервер", style='My.TButton',
                                   command=lambda: delete_server_and_check_status_gui(server_id, server_info_frame))
        delete_button.pack(side='bottom', pady=10, fill='x')
        stop_button = ttk.Button(server_info_frame, text="Выключить сервер", style='My.TButton',
                                 command=lambda: stop_server_and_check_status_gui(server_id, status_label))
        stop_button.pack(side='bottom', pady=10, fill='x')

        # Запуск главного цикла обработки событий интерфейса
        server_window.mainloop()
    else:
        # Если сервер создать не удалось, показываем сообщение об ошибке
        messagebox.showerror("Ошибка", "Не удалось создать сервер.")



def stop_server_and_check_status_gui(server_id, server_info_frame):
    # Создаем метку в интерфейсе для информирования пользователя о начале процесса выключения сервера
    stop_status_label = ttk.Label(server_info_frame, text="Выключение сервера...", style='My.TLabel')
    stop_status_label.pack(side='bottom', pady=10)

    # Проверяем текущий статус сервера
    status = check_server_status(server_id)
    if status == "SHUTOFF":
        # Если сервер уже выключен, информируем пользователя и удаляем метку статуса
        messagebox.showinfo("Информация", "Сервер уже выключен.")
        stop_status_label.destroy()
    elif status == "ACTIVE":
        # Если сервер активен, запускаем процедуру его выключения
        stop_server(server_id)
        # Запланировать проверку статуса сервера через 5 секунд
        server_info_frame.after(5000, lambda: verify_stop_gui(server_id, stop_status_label))
    else:
        # Если сервер находится в промежуточном состоянии (например, еще создается),
        # информируем пользователя и удаляем метку статуса
        messagebox.showinfo("Информация", "Сервер ещё создаётся или находится в промежуточном состоянии.")
        stop_status_label.destroy()

def delete_server_and_check_status_gui(server_id, server_info_frame):
    # Проверяем текущий статус сервера перед попыткой его удаления
    status = check_server_status(server_id)
    if status == "ACTIVE" or status == "SHUTOFF":
        # Если сервер активен или уже выключен, пытаемся его удалить
        if delete_server(server_id):
            # Успешное удаление сервера
            messagebox.showinfo("Информация", "Сервер успешно удален.")
            # Закрываем окно управления сервером и возвращаем пользователя к главному окну приложения
            server_info_frame.master.destroy()
            new_root = tk.Tk()
            new_root.geometry("300x300")
            new_root.title("OpenStack Управление")
            show_main_window(new_root)
            new_root.mainloop()
        else:
            # Не удалось удалить сервер
            messagebox.showerror("Ошибка", "Не удалось удалить сервер.")
    else:
        # Сервер находится в промежуточном состоянии, невозможно удалить
        messagebox.showinfo("Информация", "Сервер ещё создаётся или находится в промежуточном состоянии.")

def verify_stop_gui(server_id, stop_status_label):
    # Повторная проверка статуса сервера после попытки его выключить
    final_status = check_server_status(server_id)
    if final_status == "SHUTOFF":
        # Сервер успешно выключен
        messagebox.showinfo("Сервер выключен", "Сервер успешно выключен.")
    else:
        # Сервер все еще выключается
        messagebox.showinfo("Информация", "Сервер все еще выключается.")

    # Удаление метки статуса независимо от результата
    stop_status_label.destroy()

