import bcrypt

# Store users in memory
users = {}

# Register Function
def register():
    username = input("Enter Username: ")

    if username in users:
        print("Username already exists!")
        return

    password = input("Enter Password: ")

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users[username] = hashed_password
    print("Registration Successful!")

# Login Function
def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username not in users:
        print("User not found!")
        return

    stored_password = users[username]

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        print("Login Successful!")
        session(username)
    else:
        print("Invalid Password!")

# Session Management
def session(username):
    while True:
        print(f"\nWelcome {username}")
        print("1. View Profile")
        print("2. Logout")

        choice = input("Choose: ")

        if choice == "1":
            print(f"Logged in as: {username}")
        elif choice == "2":
            print("Logged Out Successfully!")
            break
        else:
            print("Invalid Choice")

# Main Menu
while True:
    print("\n=== Secure Login System ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    option = input("Enter Choice: ")

    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid Option")
