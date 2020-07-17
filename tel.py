from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import nltk
from tkcalendar import *

login_screen = Tk()
login_screen.title('Login Screen')
login_screen.geometry("250x300")
login_screen.configure(background = "#9fc2e0")

my_menu = Menu(login_screen)
login_screen.config(menu = my_menu)

conn = sqlite3.connect('Telephone.db')

cursor = conn.cursor()

directory_image = ImageTk.PhotoImage(Image.open("Directory.png"))
photos_image =  ImageTk.PhotoImage(Image.open("Photos.png"))
calendar_image =  ImageTk.PhotoImage(Image.open("Calendar.png"))

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

my_listbox = NONE
record = NONE
second_listbox = NONE
get_date_label = Label(login_screen, text = "")

def login():
    global record

    def add():
        # Add persons to contact_list
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

    # Directory Function specify contact_list
    def directory():
        global my_listbox
        global second_listbox

        conn = sqlite3.connect('Telephone.db')
        cursor = conn.cursor()

        directory_screen = Toplevel()
        directory_screen.title('Directory')
        directory_screen.geometry("300x300")

        my_menu = Menu(directory_screen)
        directory_screen.config(menu = my_menu)

        my_listbox = Listbox(directory_screen, bg="#92badc")
        my_listbox.grid(row = 0, column = 0, padx = 40, ipadx = 50)

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label = "File", menu = file_menu)
        file_menu.add_command(label = "Add", command = add)
        file_menu.add_separator()
        file_menu.add_command(label = "Exit...", command = directory_screen.quit)

        cursor.execute("SELECT * FROM contact_list WHERE namee = ?", (user,))
        records = cursor.fetchall()

        print_records = ''
        for record in records: 
            my_listbox.insert(END, record[1] + " " + record[2])

        delete_button = Button(directory_screen, text = "Delete", command = delete)
        delete_button.grid(row = 1, column = 1, pady = 10)
        delete_button.place(x = 130, y = 170)

        conn.commit()
        conn.close()
        
    # Delete Information From contact_list(Directory)
    def delete():
        global my_listbox
    
        conn = sqlite3.connect('Telephone.db')
        cursor = conn.cursor()

        item = my_listbox.get(ANCHOR).split()

        delete = "DELETE from contact_list WHERE persons = ? and phone_number = ?"

        cursor.execute(delete, (item[0], item[1]))

        my_listbox.delete(ANCHOR)
        
        conn.commit()
        conn.close()

    def calendar():
        def date():
            global get_date_label

            get_date_label.grid_forget()
            get_date_label = Label(calendar_screen, text = cal.get_date())
            get_date_label.grid(row = 2, column = 1)

        calendar_screen = Toplevel()
        calendar_screen.title('Calendar')
        calendar_screen.geometry("300x400")

        cal = Calendar(calendar_screen, selectmode = "day", year = 2020, manth = 7, day = 17)
        cal.grid(row = 0, column = 1, pady = 20, padx = 25)

        date_pick_button = Button(calendar_screen, text = "Get Date", command = date)
        date_pick_button.grid(row = 1, column = 1)

    # Login Function
    conn = sqlite3.connect('Telephone.db')
    cursor = conn.cursor()

    user = user_name.get()
    password = user_password.get()

    cursor.execute("SELECT * FROM user_informations WHERE User_name = ? and password = ?", (user, password))
    records = cursor.fetchall()

    print_records = ''
    for record in records:
        print_records += str(record) + "\n"

    if user == record[0] and password == record[1]:
        main_screen = Toplevel()
        main_screen.title(user + "'s Phone")
        main_screen.geometry("300x300")
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

    calendar_button = Button(main_screen, image = calendar_image, command = calendar)
    calendar_button.grid(row = 2, column = 0, padx = 10, pady = 10)

    calendar_label = Label(main_screen, text = "Calendar")
    calendar_label.grid(row = 3, column = 0, padx = 10, pady = 10)

    user_name.delete(0, END)
    user_password.delete(0, END)

    conn.commit()
    conn.close()

def register():
    conn = sqlite3.connect('Telephone.db')
    cursor = conn.cursor()

    user = user_name.get()
    password = user_password.get()

    if user != "" and password != "":
        cursor.execute('INSERT INTO user_informations VALUES (?,?)', (user, password) )
    else:
        login_screen.filename = messagebox.showwarning("Error", "Please Enter Your Name Or Password")
        my_label = Label(login_screen, text = login_screen.filename)

    conn.commit()
    conn.close()

    user_name.delete(0, END)
    user_password.delete(0, END)

def member():
    def member_delete():  
        conn = sqlite3.connect('Telephone.db')
        cursor = conn.cursor()

        item = member_listbox.get(ANCHOR).split()

        delete = "DELETE from user_informations WHERE User_name = ? and password = ?"

        cursor.execute(delete, (item[0], item[1]))

        member_listbox.delete(ANCHOR)
        
        conn.commit()
        conn.close()

    conn = sqlite3.connect('Telephone.db')
    cursor = conn.cursor()

    member_screen = Toplevel()
    member_screen.title('Members')
    member_screen.geometry("250x250")

    member_listbox = Listbox(member_screen)
    member_listbox.grid(row = 0, column = 0, padx = 50, pady = 10)

    cursor.execute('SELECT * from user_informations')    
    records = cursor.fetchall()

    print_records = ''
    for members_record in records: 
        member_listbox.insert(END, members_record[0] + " " + members_record[1])
    
    member_delete = Button(member_screen, text = "Delete", command = member_delete)
    member_delete.grid(row = 2, column = 1)
    member_delete.place(x = 90, y = 200)

    conn.commit()
    cursor.close()


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

registered_member = Button(login_screen, text = "Members", command = member)
registered_member.grid(row = 6, column = 0, pady = 10, padx = 60)

conn.commit()
conn.close()

mainloop()