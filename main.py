import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from UIComponents import show_main_window
from auth import authenticate_user

# Функция для обработки аутентификации пользователя
def handle_authentication():
    # Получение логина и пароля из текстовых полей
    login = login_entry.get()
    password = password_entry.get()
    # Попытка аутентификации пользователя
    user_name = authenticate_user(login, password)
    # Если аутентификация успешна
    if user_name:
        # Показать приветственное сообщение
        messagebox.showinfo("Аутентификация", f"{user_name}, добро пожаловать!")
        # Закрыть текущее окно
        root.destroy()
        # Создать и показать новое окно
        new_root = tk.Tk()
        new_root.geometry("300x300")
        new_root.title("CloudServer")
        show_main_window(new_root)
        new_root.mainloop()
    # Если аутентификация не удалась
    else:
        # Показать сообщение об ошибке
        messagebox.showerror("Ошибка аутентификации", "Неверные учетные данные или ошибка аутентификации OpenStack")

# Инициализация главного окна приложения
root = tk.Tk()
root.geometry("300x300")
root.title("CloudServer")

# Создание и размещение виджетов для ввода логина и пароля
login_frame = ttk.Frame(root)
login_frame.pack(pady=10)

ttk.Label(login_frame, text="Логин:").pack()
login_entry = ttk.Entry(login_frame)
login_entry.pack()

ttk.Label(login_frame, text="Пароль:").pack()
password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack()

# Кнопка для входа в систему
auth_button = ttk.Button(root, text="Войти", command=handle_authentication)
auth_button.pack(pady=10)

# Запуск главного цикла Tkinter
root.mainloop()

