Correct_username="sudhakar"
Correct_password="sudhakar123"
Account_status=True

#Taking user input for login:
Username=input("Enter your username:")
Password=input("Enter your password:")

#Checking login credentials and account status:
if Username==Correct_username and Password==Correct_password:
    if Account_status:
        print("Login successful.")
    else:
        print("Your account is disabled.")
else:
    print("Wrong credentials.")


