from os import system
from time import sleep

exit = False
while not exit:
    system("clear")
    print("RTCRangeHelper\n")
    print("1. Init the process")
    print("2. Exit")
    
    option = input("\nChoose a option: ")

    # 1. Init the process
    if option == "1":
        system("clear")
        print("Init")
        sleep(2)
    # 2. Exit
    elif option == "2":
        print("Exiting")
        exit = True
    else:
        system("clear")
        print("Invalid option")
        sleep(2)
        continue
