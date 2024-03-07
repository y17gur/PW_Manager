# MyPass - Password Manager

## About MyPass
MyPass is a user-friendly password manager designed to store and manage your login credentials. With MyPass, you can easily keep track of your various accounts and passwords in one centralized location. The app features a clean interface, allowing you to quickly add, retrieve, and manage your stored data.

## Features
- **Password Generator**: Create strong and unique passwords with a click.
- **Search Functionality**: Quickly find the login details for stored websites.
- **Clipboard Utility**: Copy passwords to the clipboard for easy pasting.
- **User-friendly Interface**: Easy to navigate UI with clear labels and buttons.

## Installation
To use MyPass, you have two options: run the Python script directly or use the standalone executable.

### Running the Python Script
Requirements:
- Python 3
- Tkinter library for Python (`pip install tk`)
- Keyboard library for Python (`pip install keyboard`)

### Using the Standalone Executable
For convenience, MyPass can be compiled into a standalone executable that does not require Python to be installed on the running system.
To build the executable yourself, use the provided build.py script.
Requirements:
- PyInstaller (pip install pyinstaller)

## How to Use
1. **Add Account Details**: Fill in the website, email/username, and password fields, and click the 'Add' button to store them.
2. **Search for Details**: Use the 'Search Website' button to find login details for a specific site.
3. **Generate Password**: Click on 'Generate Password' to create a secure, random password.
4. **Copy to Clipboard**: Use the generated password or copy existing ones to the clipboard.
5. **Delete Account Details**: Select an entry and click 'Delete' to remove it from the manager.
6. **Clear Fields**: Click 'Clear' to reset the input fields.

## Disclaimer
Please note that this application stores data in a local JSON file and does not implement advanced encryption for stored passwords. It is recommended to use this application for educational or demonstrational purposes only.

## Acknowledgements
- Tkinter library for providing the GUI components.
- Keyboard library for facilitating keyboard interaction within the application.

---

Enjoy managing your passwords with MyPass!

