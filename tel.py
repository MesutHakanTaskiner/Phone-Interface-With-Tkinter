from tkinter import *
from PIL import Image, ImageTk

login_screen = Tk()
login_screen.title('Login Screen')
login_screen.geometry("250x250")
login_screen.configure(background = "#9fc2e0")

my_menu = Menu(login_screen)
login_screen.config(menu = my_menu)

def login():
    pass

def register():
    pass


file_menu = Menu(my_menu)
my_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Exit...", command = login_screen.quit)

user_name_label = Label(login_screen, text = "User Name", bg = "#9fc2e0")
user_name_label.grid(row = 0, column = 0, pady = 10, padx = 60)

user_name = Entry(login_screen)
user_name.grid(row = 1, column = 0, pady = 10, padx = 60)

user_password_label = Label(login_screen, text = "Password", bg = "#9fc2e0")
user_password_label.grid(row = 2, column = 0, pady = 10, padx = 60)

user_password = Entry(login_screen)
user_password.grid(row = 3, column = 0, pady = 10, padx = 60)

login_button = Button(login_screen, text = "Login", command = login, width = 10)
login_button.grid(row = 4, column = 0, pady = 10, padx = 60)

register_button = Button(login_screen, text = "Register", command = register)
register_button.grid(row = 5, column = 0, pady = 10, padx = 60)

mainloop()