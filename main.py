from tkinter import *
import tkinter.messagebox
from customtkinter import *
from random import choice, randint, shuffle
import pyperclip
import json




app = CTk()
app.geometry("700x400")
set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")
def checking_passwords():
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        tkinter.messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        open_new_window(data)

def open_new_window(data):
    new_window = CTk()
    new_window.geometry("500x400")
    new_window.title("New Tkinter Window")

    # Create a Text widget
    textbox = CTkTextbox(new_window,width=500,height=400,scrollbar_button_color="#FFCC70", corner_radius=16,
                     border_color="#FFCC70", border_width=2)
    textbox.place(relx=0.5, rely=0.5,anchor="center")

    for website, info in data.items():
        email = info["email"]
        password = info["password"]
        result_text = f"Website: {website}\nEmail: {email}\nPassword: {password}\n\n"
        textbox.insert(END, result_text)

    # Add more widgets to the new window as needed

    new_window.mainloop()
def change_appearance_mode_event(new_appearance_mode):
    set_appearance_mode(new_appearance_mode)
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        tkinter.messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        tkinter.messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            tkinter.messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            tkinter.messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

#ctk
sidebar_frame = CTkFrame(app,width=140 ,corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)
logo_label = CTkLabel(sidebar_frame, text="Password Generator", font=CTkFont(size=20, weight="bold"))
logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
sidebar_button_1 = CTkButton(sidebar_frame,command=checking_passwords, text="All Passwords")
sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
appearance_mode_label = CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = CTkOptionMenu(sidebar_frame, values=["Dark", "Light"],command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))


website_label = CTkLabel(app,text="Website:")
website_label.grid(row=3, column=1)
email_label = CTkLabel(app, text="Email/Username:")
email_label.grid(row=4, column=1)
password_label = CTkLabel(app, text="Password:")
password_label.grid(row=5, column=1)

#Entries
website_entry = CTkEntry(app,width=200)
website_entry.grid(row=3, column=2)
website_entry.focus()
email_entry = CTkEntry(app,width=200)
email_entry.grid(row=4, column=2)
password_entry = CTkEntry(app, width=200)
password_entry.grid(row=5, column=2)

# Buttons
search_button = CTkButton(app,text="Search", command=find_password)
search_button.grid(row=3, column=3)
generate_password_button = CTkButton(app,text="Generate Password",command=generate_password)
generate_password_button.grid(row=5, column=3)
add_button = CTkButton(app,text="Add", command=save)
add_button.grid(row=6, column=1, columnspan=3)



app.mainloop()