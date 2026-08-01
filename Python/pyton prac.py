import sys
Attempt_counter = 3

name =""

#user input name + password for login
def login():
    global Attempt_counter
    while Attempt_counter > 0:
        #username
        name=(input("Enter your user name: "))
        name=name.lower()
        #password
        password = input("Password: ")
        password=password.lower()

        #To check data base (txt)
        credential = name + "," + password

        #open file and seach for credentials
        with open("usernames.txt", 'r') as file:
            #goes line by line
            for line in file:
                #if it match one then loged in
                if line.strip() == credential:
                    print("Login successful!")
                    return True
        #if no match then attempts down
        Attempt_counter -= 1
        print(f"Invalid credentials. {Attempt_counter} attempts remaining.")
    print("Too many failed attempts.")
    sys.exit()


#welcome function to greet the user
def welcome():
    print("Welcome to the Python practice program "+ name)

#update files
def update_file(file):
    #asks the user if they want to update the file
    yn=input("Do you want to update the " + file + " file? (y/n): ")
    if yn.lower() == 'y':
        print("what do you want to add?")
        add=input()
        #adds the user input to the file
        with open(file, 'a') as file:
            file.write(add + "\n")
        print("Content added to " + file + ".")
    else:
        print("No changes made to " + file + ".")

def accessfile():
    #file list to read from
        file_list=["file1.txt","file2.txt","file3.txt", "allow_list.txt"]
    
        #prints the available files to read (this can look a little nicer)
        print("Available files to read:")
        for i in file_list:
            print(i)
    
        #user input to read a file
        file_name=input("Enter the file name to read: ")
    
        #finds the file name in the list
        if file_name in file_list:
    
            #if the user is not max or admin, they cannot read file1.txt
            if file_name == "file1.txt" and name not in ("max", "admin"):
                print("You can't read this file.")
            else:
                print("You can read this file.")
                if file_name == "allow_list.txt":
                    #looks at the file and prints the content
                    with open(file_name, 'r') as file:
                        content = file.read()
                        print("Content of the file:")
                        print(content)
                        #sees if the user wants to update the file
                        update_file(file)

def usermanagement():
    print("Would you like to edit, add or remove users?")
    opp=input()
    if opp == "edit":
        target_user = input("What is their username? ").strip()

        with open("usernames.txt", "r") as file:
            lines = file.readlines()

        user_found = False
        updated_lines = []

        for line in lines:
            if not line.strip():
                continue
            
            stored_user, stored_pass = line.strip().split(",")

            if stored_user == target_user:
                user_found = True
                opp2 = input("Change username or password? ").strip().lower()

                if opp2 in ("username", "user"):
                    new_user = input("Enter new username: ").strip()
                    updated_lines.append(f"{new_user},{stored_pass}\n")
                    print(f"Username changed from '{target_user}' to '{new_user}'.")

                elif opp2 in ("password", "pass"):
                    new_pass = input("Enter new password: ").strip()
                    updated_lines.append(f"{stored_user},{new_pass}\n")
                    print(f"Password updated for user '{target_user}'.")

                else:
                    print("Invalid choice. Keeping original details.")
                    updated_lines.append(line)
            else:
                updated_lines.append(line)


        if user_found:
            with open("usernames.txt", "w") as file:
                file.writelines(updated_lines)
        else:
            print(f"User '{target_user}' was not found.")

    elif opp == ("remove"or"rm"):
        print("What is their username?")
        username=input()
        yn=input("Are you sure you want to remove "+username+"?[y/n]").lower()
        if yn==("yes"or"y"):
            with open("usernames.txt", "r") as file:
                lines = file.readlines()

            updated_lines = [line for line in lines if line.strip() != username]

            if len(updated_lines) < len(lines):
                with open("usernames.txt", "w") as file:
                    file.writelines(updated_lines)
                print(f"User '{username}' removed successfully.")
            else:
                print(f"User '{username}' was not found in the file.")
        else:
            print("Operation cancelled.")

    elif opp=="add":
        newuser=input("New user username: ")
        password=input("New user password: ")
        user=newuser+" "+ password
        with open("usernames.txt", 'a') as file:
            file.write(user + "\n")
        print("User added.")
    pass

def choice():
    print("What would you like to do?")

    count=1

    choices= ["user management", "Access file"]
    options=[]

    for i in choices:
        print(str(count)+ ": "+i)
        count+=1

    for i in choices:
        op=i.replace(" ", "").lower()
        options.append(op)
    
    use=input("Chosen:").replace(" ", "").lower()

    if use in options:
        globals()[use]()

    elif use.isdigit():
        num=int(use)-1
        fun=options[num]
        globals()[fun]()

    elif use==exit:
        sys.exit()
    else:
        print("Please use a vaild number or option.")


login()
welcome()

#files to look or use
while True:
    choice()
    