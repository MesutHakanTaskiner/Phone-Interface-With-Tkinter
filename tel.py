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

directory_image = ImageTk.PhotoImage(Image.open(r"C:\Users\Hakan\Desktop\Hakan\Software\Github\Phone-Interface-With-Tkinter\Image List\Directory.png"))
photos_image =  ImageTk.PhotoImage(Image.open(r"C:\Users\Hakan\Desktop\Hakan\Software\Github\Phone-Interface-With-Tkinter\Image List\Photos.png"))

cursor.execute("""CREATE TABLE IF NOT EXISTS user_informations (
        User_name text PRIMARY KEY,
        password text
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS contact_list (
        namee text,
        persons text,
        phone_number text,
        FOREIGN KEY(namee) REFERENCES user_informations(User_name)
)""")

def login():

    conn = sqlite3.connect('Telephone.db')
    cursor = conn.cursor()

    user = user_name.get()
    password = user_password.get()

    def add():
        def add_db():
            conn = sqlite3.connect('Telephone.db')
            cursor = conn.cursor()
            
            person = person_name.get()
            call_number = phone_number.get()
            name = user_name.get()

            cursor.execute('INSERT INTO contact_list VALUES (?,?,?)', (name, person, call_number))

            person_name.delete(0, END)
            phone_number.delete(0, END)

            conn.commit()
            conn.close()        

        add_screen = Toplevel()
        add_screen.title('Add')
        add_screen.geometry("250x150")

        person_name_label = Label(add_screen, text = "Name")
        person_name_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        person_name = Entry(add_screen)
        person_name.grid(row = 0, column = 1, padx = 10, pady = 10)

        phone_number_label = Label(add_screen, text = "No.")
        phone_number_label.grid(row = 1, column = 0, padx = 10, pady = 10)

        phone_number = Entry(add_screen)
        phone_number.grid(row = 1, column = 1, padx = 10, pady = 10)

        add_db_button = Button(add_screen, text = "Add", command = add_db)
        add_db_button.grid(row = 2, column = 1)

    def directory():
        conn = sqlite3.connect('Telephone.db')
        cursor = conn.cursor()

        directory_screen = Toplevel()
        directory_screen.title('Directory')
        
        my_menu = Menu(directory_screen)
        directory_screen.config(menu = my_menu)

        my_listbox = Listbox(directory_screen, bg="#92badc")
        my_listbox.grid(row = 0, column = 0, padx = 100, ipadx = 100)

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label = "File", menu = file_menu)
        file_menu.add_command(label = "Add", command = add)
        file_menu.add_separator()
        file_menu.add_command(label = "Exit...", command = directory_screen.quit)

        cursor.execute("SELECT * FROM contact_list WHERE namee = ?", (user,))
        records = cursor.fetchall()

        print_records = ''
        for record in records:
            print_records += str(record[1]) + " " + str(record[2]) + "\n"        
            my_listbox.insert(END, record[1] +  " " + record[2])

        #query_label = Label(directory_screen, text = print_records)
        #query_label.grid(row = 0, column = 0, sticky = W, pady = 3)

        conn.commit()
        conn.close()
    
    cursor.execute("SELECT * FROM user_informations WHERE User_name = ? and password = ?", (user, password))
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

    directory_button = Button(main_screen, image = directory_image, command = directory)
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