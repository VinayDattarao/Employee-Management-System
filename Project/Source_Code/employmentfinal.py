import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from PIL import Image, ImageTk  # Add this import statement

# Function to close the login window when register is clicked
def open_register_window(login_window):
    login_window.destroy()  # Close the login window
    register_window()

# Function to register and create a unique user-based database
def register_user(username, password):
    # Create a new database for the user
    conn = sqlite3.connect(f"{username}_employees.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL,
            gender TEXT NOT NULL,
            salary REAL NOT NULL,
            email TEXT NOT NULL,
            dob DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to handle login with "Remember Me" functionality
def login_user(username, password, remember_me_var):
    # For simplicity, let's assume we only check if the user exists
    try:
        conn = sqlite3.connect(f"{username}_employees.db")
        conn.close()

        if remember_me_var.get():
            save_login_details(username, password)  # Save login details if Remember Me is checked
        else:
            clear_login_details()  # Clear saved login details

        return True
    except sqlite3.Error:
        return False

# Save login details (username and password)
def save_login_details(username, password):
    with open("login_details.txt", "w") as f:
        f.write(f"{username}\n{password}")

# Load saved login details if "Remember Me" was checked previously
def load_login_details():
    if os.path.exists("login_details.txt"):
        with open("login_details.txt", "r") as f:
            username = f.readline().strip()
            password = f.readline().strip()
        return username, password
    return None, None

# Clear login details when logging out
def clear_login_details():
    if os.path.exists("login_details.txt"):
        os.remove("login_details.txt")

# Function for the main employee management system window
def main_app(username):
    def setup_database():
        conn = sqlite3.connect(f"{username}_employees.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                role TEXT NOT NULL,
                gender TEXT NOT NULL,
                salary REAL NOT NULL,
                email TEXT NOT NULL,
                dob DATE NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_employee():
        if name_var.get() == "" or phone_var.get() == "" or email_var.get() == "" or dob_var.get() == "":
            messagebox.showerror("Error", "Name, Phone, Email, and Date of Birth are required")
            return
        conn = sqlite3.connect(f"{username}_employees.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (name, phone, role, gender, salary, email, dob)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            name_var.get(), phone_var.get(), role_var.get(), gender_var.get(),
            salary_var.get(), email_var.get(), dob_var.get()
        ))
        conn.commit()
        conn.close()
        load_employees()
        clear_inputs()

    # Update Employee
    def update_employee():
        if id_var.get() == "":
            messagebox.showerror("Error", "Select an employee to update")
            return
        conn = sqlite3.connect(f"{username}_employees.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE employees
            SET name=?, phone=?, role=?, gender=?, salary=?, email=?, dob=?
            WHERE id=?
        ''', (
            name_var.get(), phone_var.get(), role_var.get(), gender_var.get(),
            salary_var.get(), email_var.get(), dob_var.get(), id_var.get()
        ))
        conn.commit()
        conn.close()
        load_employees()
        clear_inputs()

    def delete_employee():
        if id_var.get() == "":
            messagebox.showerror("Error", "Select an employee to delete")
            return
        conn = sqlite3.connect(f"{username}_employees.db")
        cursor = conn.cursor()
        cursor.execute(''' DELETE FROM employees WHERE id=? ''', (id_var.get(),))
        conn.commit()
        conn.close()
        load_employees()
        clear_inputs()

    def delete_all_employees():
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all employees?"):
            conn = sqlite3.connect(f"{username}_employees.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees")
            conn.commit()
            conn.close()
            load_employees()

    def load_employees(query="", search_by="name"):
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect(f"{username}_employees.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM employees WHERE {search_by} LIKE ?",
                       ('%' + query + '%',))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            values = item["values"]
            id_var.set(values[0])
            name_var.set(values[1])
            phone_var.set(values[2])
            role_var.set(values[3])
            gender_var.set(values[4])
            salary_var.set(values[5])
            email_var.set(values[6])
            dob_var.set(values[7])  # Set DOB value when selecting an employee

    def clear_inputs():
        id_var.set("")
        name_var.set("")
        phone_var.set("")
        role_var.set("")
        gender_var.set("")
        salary_var.set("")
        email_var.set("")
        dob_var.set("")  # Clear DOB input field

    def search_employee():
        search_term = search_var.get()
        search_by = search_by_var.get()
        load_employees(search_term, search_by)

    def logout():
        clear_login_details()
        root.destroy()  # Close the main app
        login_window()  # Show login window

    root = tk.Tk()
    root.title(f"Employee Management System - {username}")
    root.geometry("1077x390")
    root.resizable(True, True)

    # Settings menu (Dropdown with Logout option)
    menu_bar = tk.Menu(root)
    settings_menu = tk.Menu(menu_bar, tearoff=0)
    settings_menu.add_command(label="Logout", command=logout)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    root.config(menu=menu_bar)

    # Variables
    id_var = tk.StringVar()
    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    role_var = tk.StringVar()
    gender_var = tk.StringVar()
    salary_var = tk.StringVar()
    email_var = tk.StringVar()
    dob_var = tk.StringVar()  # Date of Birth Variable
    search_var = tk.StringVar()
    search_by_var = tk.StringVar(value="name")  # Default search by 'name'

    # Role and Gender Options
    roles = ["Web Developer", "Front-end Developer", "Back-end Developer", "Full-stack Developer",
             "Software Architect", "UI/UX Designer", "Quality Assurance Engineer", "Project Manager",
             "Business Analyst", "DevOps Engineer", "Data Scientist", "Security Engineer",
             "Product Manager", "Database Administrator"]
    genders = ["Male", "Female", "Other"]
    search_options = ["name", "phone", "role", "gender", "email"]  # Search options

    # Frames
    top_frame = tk.Frame(root, padx=10, pady=10, bg="#1f2a38")
    top_frame.place(x=10, y=10, width=1058, height=330)

    bottom_frame = tk.Frame(root, bg="#1f2a38")
    bottom_frame.place(x=10, y=335, width=1058, height=45)

    # Search Bar (Top of employee list)
    search_frame = tk.Frame(top_frame, bg="#1f2a38", pady=10)
    search_frame.grid(row=0, column=1, sticky="ew")

    # Search Dropdown
    tk.Label(search_frame, text="Search By:", fg="white", bg="#1f2a38").grid(row=0, column=0, padx=5)
    search_by_dropdown = ttk.Combobox(search_frame, textvariable=search_by_var, values=search_options, state="readonly")
    search_by_dropdown.grid(row=0, column=1, padx=5)

    # Search Input Field
    tk.Label(search_frame, text="Search:", fg="white", bg="#1f2a38").grid(row=0, column=2, padx=5)
    tk.Entry(search_frame, textvariable=search_var, width=30).grid(row=0, column=3, padx=5)
    tk.Button(search_frame, text="Search", command=search_employee, bg="#2196f3", fg="white").grid(row=0, column=4,
                                                                                                   padx=5)

    # Form Inputs (Inside top_frame)
    form_frame = tk.Frame(top_frame, padx=10, pady=10, bg="#1f2a38", width=380)
    form_frame.grid(row=1, column=0, rowspan=2)

    # Employee Table (Inside top_frame)
    table_frame = tk.Frame(top_frame, bg="white", width=480)
    table_frame.grid(row=1, column=1)

    # Form fields
    tk.Label(form_frame, text="ID:", fg="white", bg="#1f2a38").grid(row=0, column=0, sticky="w", pady=5)
    tk.Entry(form_frame, textvariable=id_var, state="readonly").grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Name:", fg="white", bg="#1f2a38").grid(row=1, column=0, sticky="w", pady=5)
    tk.Entry(form_frame, textvariable=name_var).grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Phone:", fg="white", bg="#1f2a38").grid(row=2, column=0, sticky="w", pady=5)
    tk.Entry(form_frame, textvariable=phone_var).grid(row=2, column=1, pady=5)

    tk.Label(form_frame, text="Role:", fg="white", bg="#1f2a38").grid(row=3, column=0, sticky="w", pady=5)
    ttk.Combobox(form_frame, textvariable=role_var, values=roles, state="readonly").grid(row=3, column=1, pady=5)

    tk.Label(form_frame, text="Gender:", fg="white", bg="#1f2a38").grid(row=4, column=0, sticky="w", pady=5)
    ttk.Combobox(form_frame, textvariable=gender_var, values=genders, state="readonly").grid(row=4, column=1, pady=5)

    tk.Label(form_frame, text="Salary:", fg="white", bg="#1f2a38").grid(row=5, column=0, sticky="w", pady=5)
    tk.Entry(form_frame, textvariable=salary_var).grid(row=5, column=1, pady=5)

    tk.Label(form_frame, text="Email:", fg="white", bg="#1f2a38").grid(row=6, column=0, sticky="w", pady=5)
    tk.Entry(form_frame, textvariable=email_var).grid(row=6, column=1, pady=5)

    tk.Label(form_frame, text="Date of Birth:", fg="white", bg="#1f2a38").grid(row=7, column=0, sticky="w", pady=5)
    tk.Entry(form_frame, textvariable=dob_var).grid(row=7, column=1, pady=5)

    # Employee Table
    columns = ("ID", "Name", "Phone", "Role", "Gender", "Salary", "Email", "DOB")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind("<ButtonRelease-1>", on_tree_select)

    # Button Row
    button_frame = tk.Frame(bottom_frame, bg="#1f2a38")
    button_frame.pack(fill=tk.X)

    button_width = 15  # Adjust button width to make them more uniform
    gap = 10  # Space between buttons
    tk.Button(button_frame, text="Add Employee", command=add_employee, width=button_width, bg="#00bcd4").grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=gap)
    tk.Button(button_frame, text="Update Employee", command=update_employee, width=button_width, bg="#4caf50").grid(
        row=0, column=1, padx=gap)
    tk.Button(button_frame, text="Delete Employee", command=delete_employee, width=button_width, bg="#f44336").grid(
        row=0, column=2, padx=gap)
    tk.Button(button_frame, text="Delete All", command=delete_all_employees, width=button_width, bg="#9e9e9e").grid(
        row=0, column=3, padx=gap)
    tk.Button(button_frame, text="Logout", command=logout, width=button_width, bg="#e91e63").grid(row=0, column=4,
                                                                                               padx=gap)

    setup_database()
    load_employees()  # Load employee data into the treeview
    root.mainloop()

# Main login window
def login_window():
    def on_login_click():
        username = username_entry.get()
        password = password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username and Password are required")
            return

        if login_user(username, password, remember_me_var):
            root.destroy()  # Close the login window before opening the main app
            main_app(username)  # Start the employee management system for the user
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    def on_register_click():
        root.destroy()
        register_window()

    root = tk.Tk()
    root.title("Employee Management System")
    root.geometry("400x400")
    root.resizable(False, False)

    # Load and set background image
    bg_image = Image.open("m1.jpeg")
    bg_image = bg_image.resize((400, 400), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(root, text="Login", font=("Arial", 20, "bold"), fg="black", bg="light blue").pack(pady=20)

    # Username Field
    tk.Label(root, text="Username:", fg="black", bg="light blue", font=("Arial", 10, "bold")).pack(pady=5)
    username_entry = tk.Entry(root, width=30)
    username_entry.pack(pady=5)

    # Password Field
    tk.Label(root, text="Password:", fg="black", bg="light blue", font=("Arial", 10, "bold")).pack(pady=5)
    password_entry = tk.Entry(root, width=30, show="*")
    password_entry.pack(pady=5)

    # Remember Me Checkbox
    remember_me_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Remember Me", variable=remember_me_var, fg="black", bg="light blue", font=("Arial", 10, "bold")).pack(pady=10)

    # Buttons
    tk.Button(root, text="Login", command=on_login_click, width=20, bg="yellow").pack(pady=5)
    tk.Button(root, text="Register", command=on_register_click, width=20, bg="lavender").pack(pady=5)

    root.mainloop()

# Register window
def register_window():
    def on_register_click():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if username == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        register_user(username, password)
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        root.destroy()  # Close the register window
        login_window()  # Open the login window

    root = tk.Tk()
    root.title("Employee Management System")
    root.geometry("400x400")
    root.config(bg="#34495e")
    root.resizable(False, False)

    tk.Label(root, text="Register", font=("Arial", 20), fg="white", bg="#34495e").pack(pady=20)

    # Username Field
    tk.Label(root, text="Username:", fg="white", bg="#34495e").pack(pady=5)
    username_entry = tk.Entry(root, width=30)
    username_entry.pack(pady=5)

    # Password Field
    tk.Label(root, text="Password:", fg="white", bg="#34495e").pack(pady=5)
    password_entry = tk.Entry(root, width=30, show="*")
    password_entry.pack(pady=5)

    # Confirm Password Field
    tk.Label(root, text="Confirm Password:", fg="white", bg="#34495e").pack(pady=5)
    confirm_password_entry = tk.Entry(root, width=30, show="*")
    confirm_password_entry.pack(pady=5)

    # Buttons
    tk.Button(root, text="Register", command=on_register_click, width=20, bg="#3498db").pack(pady=20)

    root.mainloop()


login_window()  # Start the login window