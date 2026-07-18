from os import system
from time import sleep
import json

init_data = {
    "notRTCProblem": False,
    "rangesExcluded": [],
    "rangesTried": [],
    "rangeHalf": [],
}

data = {}

try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(init_data, f, indent=4)
    data = init_data

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

        # Add 0x00-0xFF range to rangesExcluded
        def addRangeToRangesExcluded():
            if data["rangesExcluded"] == [0, 255]:
                return
            data["rangesExcluded"].append([0, 255])
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        addRangeToRangesExcluded()

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
