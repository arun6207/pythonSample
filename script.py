# importing the module
import os

# sets the text colour to green
os.system("tput setaf 2")

print("Launching Bluetooth Terminal User Interface")

# sets the text color to red
os.system("tput setaf 1")

print("\t\tWELCOME TO BT Terminal User Interface\t\t\t")

# sets the text color to white
os.system("tput setaf 7")

print("\t-------------------------------------------------")
print("Entering local device")
while True:
    print(""" 
        1.List BT Controllers 
        2.Auto enable BT Controllers  
        3.Remove Bluetooth Cache 
        4.Configure docker 
        5.Add user 
        6.Delete user 
        7.Create a file 
        8.Create a folder 
        9.Exit""")

    ch = int(input("Enter your choice: "))

    if (ch == 1):
        os.system("hcitool dev | sed '1 d'")



    elif ch == 2:

        os.system("sudo sed -i 's/AutoEnable=false/AutoEnable=true/g' /etc/bluetooth/main.conf")

    elif ch == 3:
        print("SELECT CONTOLLER TO PROCEED")
        os.system("hcitool dev | sed '1 d'")
        os.system("echo ''")
        os.system("")

    elif ch == 4:
        os.system("")
        os.system("")
        os.system("")


    elif ch == 5:
        new_user = input("Enter the name of new user: ")
        os.system("sudo useradd {}".format(new_user))
        os.system("id -u {}".format(new_user))

    elif ch == 6:
        del_user = input("Enter the name of the user to delete: ")
        os.system("sudo userdel {}".format(del_user))

    elif ch == 7:
        filename = input("Enter the filename: ")
        f = os.system("sudo touch {}".format(filename))
        if f != 0:
            print("Some error occurred")
        else:
            print("File created successfully")

    elif ch == 8:
        foldername = input("Enter the foldername: ")
        f = os.system("sudo mkdir {}".format(foldername))
        if f != 0:
            print("Some error occurred")
        else:
            print("Folder created successfully")

    elif ch == 9:
        print("Exiting application")
        exit()
    else:
        print("Invalid entry")

    input("Press enter to continue")
    os.system("clear")