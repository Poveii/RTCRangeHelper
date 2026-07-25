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

not_rtc_problem = data["notRTCProblem"]

exit = False
while not exit and not not_rtc_problem:
    system("clear")

    # If the process already started
    if data["rangesExcluded"] == [[0, 255]] or len(data["rangesTried"]) >= 1:
        print("\nRTCRangeHelper\n")
        print("1. Continue the process")
        print("2. Start over the process")
        print("3. Exit")

        option = input("\nChoose a option: ")

        # 1. Continue the process
        if option == "1":
            errorQuestion = input("\nDid you still get the CMOS error? (y/n): ")
            if errorQuestion.lower() == "y":
                if len(data["rangeHalf"]) >= 1:
                    system("clear")
                    print("So, the error is not in this range. Let's test the other half.")

                    print("\nChange the range to this in your boot-args: ")
                    print(f"\nrtcfx_exclude={data["rangeHalf"][0][0]:02X}-{data["rangeHalf"][0][1]:02X}")

                    with open("data.json", "w", encoding="utf-8") as f:
                        data["rangesTried"].append(data["rangesExcluded"][0])
                        data["rangesExcluded"] = data["rangeHalf"]
                        data["rangeHalf"] = []
                        json.dump(data, f, indent=4)

                    sleep(2)
                    print("\nNow reboot.")
                    exit_option = input("\nPress enter to exit...")
                    system("clear")
                    exit = True

                if data["rangesExcluded"] == [[0, 127], [128, 255]]:
                    print("So, these errors are not related to RTC Ranges. You can close this program and search something about CMOS errors.")
                    with open("data.json", "w", encoding="utf-8") as f:
                        data["notRTCProblem"] = True
                        json.dump(data, f, indent=4)
                    sleep(4)
                    continue

                if data["rangesExcluded"] == [[0, 255]]:
                    system("clear")
                    print("You can try the 0x00-0x7F and 0x80-0xFF ranges together. The bit between these can be the RTC issue.")

                    print("Change the range to this in your boot-args: ")
                    print("\nrtcfx_exclude=00-7F,80-FF")

                    with open("data.json", "w", encoding="utf-8") as f:
                        data["rangesTried"].append(data["rangesExcluded"][0])
                        data["rangesExcluded"] = [[0, 127], [128, 255]]
                        json.dump(data, f, indent=4)
                    
                    sleep(2)
                    print("\nNow reboot.")
                    exit_option = input("\nPress enter to exit...")
                    system("clear")
                    exit = True
            elif errorQuestion.lower() == "n":
                system("clear")
                print("We found the error. Let's mitigate!")

                isFirstNumberRangeExcludedGreaterThanZero = True if data["rangesExcluded"][0][0] > 0 else False
                firstNumberRangeExcludedDiffDivided = int((data["rangesExcluded"][0][-1] - data["rangesExcluded"][0][0]) / 2)
                firstHalfRangeExcluded = [data["rangesExcluded"][0][0], data["rangesExcluded"][0][-1] - firstNumberRangeExcludedDiffDivided if isFirstNumberRangeExcludedGreaterThanZero else int(data["rangesExcluded"][0][-1] / 2)]
                otherHalfRangeExcluded = [data["rangesExcluded"][0][-1] - firstNumberRangeExcludedDiffDivided if isFirstNumberRangeExcludedGreaterThanZero else data["rangesExcluded"][0][-1] - int(data["rangesExcluded"][0][-1] / 2), data["rangesExcluded"][0][-1]]

                # Move the first range excluded to rangesTried
                with open("data.json", "w", encoding="utf-8") as f:
                    firstRangeExcluded = data["rangesExcluded"][0]
                    data["rangesTried"].append(firstRangeExcluded)
                    data["rangesExcluded"].pop()
                    json.dump(data, f, indent=4)

                print("\nLet's split our RTC range. Test the first half.")
                sleep(2)
                print("\nChange the range to this in your boot-args: ")

                print(f"\nrtcfx_exclude={firstHalfRangeExcluded[0]:02X}-{firstHalfRangeExcluded[1]:02X}")

                # Add current range excluded to rangesExcluded
                with open("data.json", "w", encoding="utf-8") as f:
                    data["rangesExcluded"].append(firstHalfRangeExcluded)
                    json.dump(data, f, indent=4)

                # Add the other half range excluded to rangeHalf
                with open("data.json", "w", encoding="utf-8") as f:
                    data["rangeHalf"] = []
                    data["rangeHalf"].append(otherHalfRangeExcluded)
                    json.dump(data, f, indent=4)

                sleep(2)
                print("\nNow reboot.")
                exit_option = input("\nPress enter to exit...")
                exit = True
            else:
                system("clear")
                print("Invalid answer")
                sleep(2)
            continue
        # 2. Start over the process
        elif option == "2":
            important_option = input("Do you really want to start the process again? (y/n) ")

            if important_option == "y":
                print("Starting over the process...")
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(init_data, f, indent=4)
                sleep(2)
                system("clear")
            elif important_option == "n":
                system("clear")
                continue
            else:
                system("clear")
                print("Invalid answer")
                sleep(2)
                continue
        # 3. Exit
        elif option == "3":
            print("Exiting")
            exit = True
            continue
        else:
            system("clear")
            print("Invalid option")
            sleep(2)
            continue

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

if not_rtc_problem:
    print("It's not a RTC problem. So this helper can not help you.")
