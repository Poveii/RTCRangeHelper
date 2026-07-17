from os import system
from time import sleep

exit = False
while not exit:
    system("clear")
    print("\nRTCRangeHelper\n")
    print("1. Init the process")
    print("2. Exit")
    
    option = input("\nChoose a option: ")

    # 1. Init the process
    if option == "1":
        system("clear")
        print("Make sure that you already test the DisableRtcChecksum quirk in Kernel -> Quirks")
        sleep(3)
        system("clear")
        print("Let's get start with the 0x00-0xFF range to see if your CMOS problem is related to RTC ranges.")
        sleep(2)
        print("\nPut this in your boot-args: ")
        print("rtcfx_exclude=00-FF")
        sleep(2)
        print("\nMake sure to have RTCMemoryFixup.kext in your kexts")
        print("https://github.com/acidanthera/RTCMemoryFixup/releases")
        sleep(2)

        print("\nNow reboot.")
        exit_option = input("\nPress enter to exit...")
        system("clear")
        exit = True
    # 2. Exit
    elif option == "2":
        print("Exiting")
        exit = True
    else:
        system("clear")
        print("Invalid option")
        sleep(2)
        continue
