from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox

login_screen = Tk()
login_screen.title('Login Screen')
login_screen.geometry("250x250")
login_screen.configure(background = "#9fc2e0")

my_menu = Menu(login_screen)
login_screen.config(menu = my_menu)

conn = sqlite3.connect('Telephone.db')

cursor = conn.cursor()

directory_image = ImageTk.PhotoImage(Image.open(r"C:\Users\Hakan\Desktop\Hakan\Software\Github\Telephone-Interface-With-Tkinter\Image List\Directory.png"))
photos_image =  ImageTk.PhotoImage(Image.open(r"C:\Users\Hakan\Desktop\Hakan\Software\Github\Telephone-Interface-With-Tkinter\Image List\Photos.png"))

cursor.execute("""CREATE TABLE IF NOT EXISTS user_informations (
        User_name text PRIMARY KEY,
        password text
)""")

def login():

    conn = sqlite3.connect('Telephone.db')

    cursor = conn.cursor()

    user = user_name.get()
    password = user_password.get()

    cursor.execute("SELECT * FROM user_informations")
    records = cursor.fetchall()

    print_records = ''
    for record in records:
        print_records += str(record) + "\n"

    if user == record[0] and password == record[1]:
        main_screen = Toplevel()
        main_screen.title("Main Screen")
    else:
        login_screen.filename = messagebox.showwarning("Error", "Wrong User Name Or Password")
        my_label = Label(login_screen, text = login_screen.filename)

    directory_button = Button(main_screen, image = directory_image)
    directory_button.grid(row = 0, column = 0, padx = 10, pady = 10)

    directory_label = Label(main_screen, text = "Directory")
    directory_label.grid(row = 1, column = 0, padx = 10)

    Photos_button = Button(main_screen, image = photos_image)
    Photos_button.grid(row = 0, column = 1, padx = 10, pady = 10)

    Photos_label = Label(main_screen, text = "Photos")
    Photos_label.grid(row = 1, column = 1, padx = 10)

    conn.commit()

    conn.close()


def register():
    conn = sqlite3.connect('Telephone.db')

    cursor = conn.cursor()

    user = user_name.get()
    password = user_password.get()

    cursor.execute('INSERT INTO user_informations VALUES (?,?)', (user, password) )

    conn.commit()

    conn.close()

    user_name.delete(0, END)
    user_password.delete(0, END)


file_menu = Menu(my_menu)
my_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Exit...", command = login_screen.quit)

user_name_label = Label(login_screen, text = "User Name", bg = "#9fc2e0")
user_name_label.grid(row = 0, column = 0, pady = 10, padx = 60)

user_name = Entry(login_screen)
user_name.grid(row = 1, column = 0, pady = 10, padx = 60)

user_password_label = Label(login_screen, text = "Password", bg = "#9fc2e0")
user_password_label.grid(row = 2, column = 0, pady = 10, padx = 60)

user_password = Entry(login_screen, show = "*")
user_password.grid(row = 3, column = 0, pady = 10, padx = 60)

login_button = Button(login_screen, text = "Login", command = login, width = 10)
login_button.grid(row = 4, column = 0, pady = 10, padx = 60)

register_button = Button(login_screen, text = "Register", command = register)
register_button.grid(row = 5, column = 0, pady = 10, padx = 60)

conn.commit()

conn.close()

mainloop()