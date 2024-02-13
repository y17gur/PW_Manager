from tkinter import *
import keyboard
from tkinter import messagebox
from tkinter.ttk import Combobox
from random import choice, randint, shuffle
import subprocess
import json
from tkinter import Tk, Canvas, PhotoImage
from logo_base64 import logo_base64


class PasswordManager:
    def __init__(self, master):
        self.master = master
        master.title("Password Manager")
        master.config(padx=15, pady=15)
        master.resizable(width=False, height=False)

        self.passwords = []
        self.all_websites = []

        # Create a PhotoImage object using the decoded image data
        self.logo_img = PhotoImage(data=logo_base64)

        # Create a canvas to display the logo image
        self.canvas = Canvas(height=155, width=170)
        self.canvas.create_image(100, 80, image=self.logo_img)
        self.canvas.grid(row=1, column=1, pady=(0, 15))

        self.website_label = Label(text="Website: ")
        self.website_label.grid(row=2, column=0, sticky="e", pady=(0, 5))

        self.email_label = Label(text="Email/Username: ")
        self.email_label.grid(row=3, column=0, sticky="e", pady=(0, 5))

        self.password_label = Label(text="Password: ")
        self.password_label.grid(row=4, column=0, sticky="e", pady=(0, 5))

        self.website_combobox = Combobox(width=30)
        self.website_combobox.grid(row=2, column=1, columnspan=2, sticky="w", pady=(0, 5))
        self.website_combobox.focus()

        self.email_combobox = Combobox(width=50)
        self.email_combobox.grid(row=3, column=1, columnspan=2, sticky="w", pady=(0, 5))

        self.password_entry = Entry(width=33)
        self.password_entry.grid(row=4, column=1, sticky="w", pady=(0, 5))

        self.account_listbox = Listbox(height=10, width=30)
        self.account_listbox.grid(row=1, column=3, columnspan=3, pady=(10, 5), sticky="ne")
        self.account_listbox.grid_remove()

        self.search_button = Button(text="Search Website", command=self.find_password, width=14, height=1)
        self.search_button.grid(row=2, column=2, sticky="e", pady=(0, 5))

        self.generate_password_button = Button(text="Generate Password", command=self.generate_password, width=14,
                                               height=1)
        self.generate_password_button.grid(row=4, column=2, sticky="e", pady=(0, 5))

        self.add_button = Button(text="Delete", width=8, command=self.delete_data)
        self.add_button.grid(row=5, column=1, sticky="n", pady=(0, 0))

        self.delete_button = Button(text="Add", width=8, command=self.add_data)
        self.delete_button.grid(row=5, column=1, sticky="w", pady=(0, 0))

        self.clear_button = Button(text="Clear", width=8, command=self.clear_fields)
        self.clear_button.grid(row=5, column=1, sticky="e", pady=(0, 0))

        self.show_selected_button = Button(text="Show Selected", command=self.show_selected_account, width=14, height=1)
        self.show_selected_button.grid(row=2, column=4, sticky="e", pady=(0, 5), padx=(0, 10))
        self.show_selected_button.grid_remove()

        self.show_hide_button = Button(text="Hide", command=self.hide_all, width=5, height=1)
        self.show_hide_button.grid(row=2, column=5, sticky="e", pady=(0, 5), padx=(0, 10))
        self.show_hide_button.grid_remove()

        self.load_data()

        # Keep track of the current text in the combobox
        self.current_text = ""

        # Bind the function to the combobox to update values dynamically
        self.website_combobox.bind("<KeyRelease>", lambda event: self.filter_websites(event))

        # Bind FocusOut event to website_combobox to check for focus
        self.website_combobox.bind("<FocusOut>", lambda event: self.check_combobox_focus)

        # Bind mouse click event to remove focus from website_combobox
        self.email_combobox.bind("<Button-1>", self.remove_combobox_focus)
        self.password_entry.bind("<Button-1>", self.remove_combobox_focus)
        self.website_combobox.bind("<Button-1>", self.remove_combobox_focus)

        # Schedule a check for focus after a short delay
        self.master.after(100, self.check_combobox_focus)

    def remove_combobox_focus(self, event):
        self.master.after(100, self.check_combobox_focus)  # Schedule a check for focus after a short delay
        self.website_combobox.selection_clear()  # Remove focus from the website_combobox
        self.canvas.focus_set()  # Set focus to another widget

    def check_combobox_focus(self):
        try:
            focused_widget = self.master.focus_get()
            if focused_widget == self.website_combobox:
                keyboard.on_press(self.on_key_press)  # Listen for key events
            else:
                keyboard.unhook_all()  # Stop listening for key events if focus is not on website_combobox
        except KeyError:
            pass

    def load_data(self):
        """Load email and website data from the JSON file."""
        self.current_text = ""  # Reset current text
        try:
            with open("data.json", "r") as data_file_email:
                data_email = json.load(data_file_email)
                # Use a set to store unique emails
                all_emails = {account['email'] for accounts in data_email.values() for account in accounts}
                # Convert set back to a list and assign to combobox values
                self.email_combobox['values'] = list(all_emails)
                self.all_websites = list(data_email.keys())  # Get all website keys from the data
                self.website_combobox['values'] = self.all_websites
        except FileNotFoundError:
            pass

    def on_key_press(self, event):
        if event.name.isalnum():  # Check if the pressed key is alphanumeric
            if self.current_text == "":
                self.website_combobox.focus_set()
            else:
                self.current_text += event.name  # Append the new character to the current text
                self.website_combobox.focus_set()
                self.website_combobox.delete(0, 'end')
                self.website_combobox.insert(0, self.current_text[:-1])

    def filter_websites(self, event):
        entered_text = self.website_combobox.get().lower()
        filtered_values = [website for website in self.all_websites if entered_text in website.lower()]
        self.website_combobox['values'] = filtered_values
        self.website_combobox.event_generate("<Down>")  # Open the dropdown list

    def copy2clip(self, txt):
        txt = txt.replace('\n', '').replace('\r', '')
        cmd = 'clip'
        subprocess.run(cmd, input=txt.strip(), text=True, shell=True)

    def show_popup(self, message):
        popup = Tk()
        popup.wm_title("Password Copied")
        label = Label(popup, text=message)
        label.pack(padx=10, pady=10)
        popup.after(2500, popup.destroy)
        popup.mainloop()

    def find_password(self):
        website = self.website_combobox.get()  # Retrieve selected website from the combobox

        # Check if the website field is empty
        if not website:
            messagebox.showinfo(title="Oops", message="Please select a website.")
            return

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                if website in data:
                    accounts = data[website]
                    if accounts:
                        if len(accounts) == 1:
                            self.hide_all()
                            email = accounts[0]['email']
                            password = accounts[0]['password']
                            self.email_combobox.set(email)
                            self.password_entry.delete(0, END)
                            self.password_entry.insert(0, password)
                            self.account_listbox.grid_remove()
                            self.show_selected_button.grid_remove()
                        else:
                            self.account_listbox.delete(0, END)
                            for account in accounts:
                                email = account['email']
                                self.account_listbox.insert(END, f"Email: {email}")
                                self.passwords.append(account['password'])
                            self.show_all()
                    else:
                        messagebox.showinfo(title="Oops", message="No Accounts Found for this Website!")
                else:
                    messagebox.showinfo(title="Oops", message="No Accounts Found for this Website!")
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="No Data File Found!")

    def show_selected_account(self):
        selected_index = self.account_listbox.curselection()
        if selected_index:
            selected_email = self.account_listbox.get(selected_index[0])
            email = selected_email.split("Email: ")[1].strip()
            password = self.passwords[selected_index[0]]
            self.password_entry.delete(0, END)
            self.password_entry.insert(0, password)
            self.email_combobox.set(email)
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
                    for website, accounts in data.items():
                        for account in accounts:
                            if account['email'] == email:
                                self.website_combobox.delete(0, END)
                                self.website_combobox.insert(0, website)
                                break
            except FileNotFoundError:
                messagebox.showinfo(title="Oops", message="No Data File Found!")

    def clear_fields(self):
        self.current_text = ""
        self.load_data()

        self.email_combobox.delete(0, END)
        self.password_entry.delete(0, END)
        self.website_combobox.delete(0, END)
        self.website_combobox.focus()

    def hide_all(self):
        self.show_selected_button.grid_remove()
        self.account_listbox.grid_remove()
        self.show_hide_button.grid_remove()
        self.website_combobox.focus()

    def show_all(self):
        self.show_selected_button.grid()
        self.account_listbox.grid()
        self.show_hide_button.grid()

    def generate_password(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_symbols = [choice(symbols) for _ in range(randint(3, 4))]
        password_numbers = [choice(numbers) for _ in range(randint(3, 4))]
        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, "".join(password_list))
        self.hide_all()

        password = self.password_entry.get()
        self.copy2clip(password)
        self.show_popup(f"'{password}' password is in clipboard.")

    def delete_data(self):
        website = self.website_combobox.get()
        email = self.email_combobox.get()

        # Check if both website and email fields are filled
        if not website or not email:
            messagebox.showinfo(title="Oops", message="Please select both website and email.")
            return

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            return

        if website in data:
            accounts = data[website]
            # Check if the entered email exists for the selected website
            if any(account['email'] == email for account in accounts):
                updated_accounts = [account for account in accounts if account['email'] != email]
                if updated_accounts:
                    data[website] = updated_accounts
                else:
                    del data[website]  # Remove the website entry if no accounts left
            else:
                messagebox.showinfo(title="Oops", message="The entered email does not exist for the selected website.")
                return
        else:
            messagebox.showinfo(title="Oops", message="The selected website does not exist.")
            return

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        # Update combobox values with updated list of websites
        self.website_combobox['values'] = list(data.keys())

        # Update combobox values with updated list of emails
        all_emails = {account['email'] for accounts in data.values() for account in accounts}
        self.email_combobox['values'] = list(all_emails)

        self.clear_fields()
        self.hide_all()

    def add_data(self):
        website = self.website_combobox.get()  # Retrieve selected website from the combobox
        email = self.email_combobox.get()
        password = self.password_entry.get()
        if len(website) == 0 or len(password) == 0 or len(email) == 0:
            messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
            return
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}

        if website in data:
            for account in data[website]:
                if account["email"] == email:
                    # If website and email combination exists, update the password
                    account["password"] = password
                    break
            else:
                # If email not found, add a new entry
                data[website].append({"email": email, "password": password})
        else:
            # If website doesn't exist, create a new entry
            data[website] = [{"email": email, "password": password}]

        # Update combobox values with updated list of websites
        self.website_combobox['values'] = list(data.keys())

        # Update combobox values with updated list of emails
        all_emails = {account['email'] for accounts in data.values() for account in accounts}
        self.email_combobox['values'] = list(all_emails)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        self.clear_fields()
        self.hide_all()
        self.website_combobox.focus()


def main():
    root = Tk()
    PasswordManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
