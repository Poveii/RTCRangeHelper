from subprocess import call
from time import sleep
import json

init_data = {
    "notRTCProblem": False,
    "rangesExcludedInHex": "",
    "rangesExcluded": [],
    "rangesTried": [],
    "rangeHalf": [],
    "rangeCombination": 0,
    "rangeOriginal": [],
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
    call("clear")

    # If the process already started
    if data["rangesExcluded"] == [[0, 255]] or len(data["rangesTried"]) >= 1:
        print("\nRTCRangeHelper\n")

        print(f"Ranges Excluded: {data['rangesExcludedInHex']}\n")

        print("1. Continue the process")
        print("2. Start over the process")
        print("3. Exit")

        option = input("\nChoose a option: ")

        # 1. Continue the process
        if option == "1":
            errorQuestion = input("\nDid you still get the CMOS error? (y/n): ")
            if errorQuestion.lower() == "y":
                if data["rangesExcluded"] == [[0, 127], [128, 255]]:
                    print("So, these errors are not related to RTC Ranges. You can close this program and search something about CMOS errors.")

                    data["notRTCProblem"] = True

                    with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    sleep(4)
                    continue

                if data["rangesExcluded"] == [[0, 255]]:
                    call("clear")
                    print("You can try the 0x00-0x7F and 0x80-0xFF ranges together. The bit between these can be the RTC issue.")

                    print("Change the range to this in your boot-args: ")
                    print("\nrtcfx_exclude=00-7F,80-FF")

                    data["rangesTried"].append(data["rangesExcluded"][0])
                    data["rangesExcluded"] = [[0, 127], [128, 255]]
                    data["rangesExcludedInHex"] = "00-7F,80-FF"

                    with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    
                    sleep(2)
                    print("\nNow reboot.")
                    exit_option = input("\nPress enter to exit...")
                    call("clear")
                    exit = True

                if len(data["rangeHalf"]) >= 1:
                    call("clear")
                    print("So, the error is not in this range(s). Let's test the other half.")

                    if len(data["rangesExcluded"]) > 1:
                        print("We have multiple ranges excluded. Let's test the other half of one first.")

                    # Switch the rangeHalf with rangesExcluded
                    numberOfRanges = len(data["rangesExcluded"])
                    numberOfCombinations = 1 << numberOfRanges

                    if data["rangeCombination"] >= numberOfCombinations or data["rangesExcluded"] == data["rangeHalf"]:
                        print("All combinations of ranges have been tested. Let's try the last both together.")

                        data["rangesExcluded"] = data["rangeOriginal"] + data["rangeHalf"]
                        data["rangesExcluded"].sort()
                        data["rangeHalf"].clear()
                        data["rangeOriginal"].clear()
                        data["rangeCombination"] = 0

                        print("\nChange the range to this in your boot-args: ")

                        rangesResult = ','.join(["-".join(format(y, "02X") for y in x) for x in data["rangesExcluded"]])
                        print(f"\nrtcfx_exclude={rangesResult}")
                        data["rangesExcludedInHex"] = rangesResult

                        with open("data.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4)

                        sleep(2)
                        print("\nNow reboot.")
                        exit_option = input("\nPress enter to exit...")
                        call("clear")
                        exit = True
                        continue

                    data["rangeCombination"] += 1
                    combination = data["rangeCombination"]

                    data["rangesExcluded"] = [
                        data["rangeHalf"][index]
                        if combination & (1 << index)
                        else data["rangeOriginal"][index]
                        for index in range(numberOfRanges)
                    ]

                    print("\nChange the range to this in your boot-args: ")

                    rangesResult = ','.join(["-".join(format(y, "02X") for y in x) for x in data["rangesExcluded"]])
                    print(f"\nrtcfx_exclude={rangesResult}")
                    data["rangesExcludedInHex"] = rangesResult

                    with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)

                    sleep(2)
                    print("\nNow reboot.")
                    exit_option = input("\nPress enter to exit...")
                    call("clear")
                    exit = True

            elif errorQuestion.lower() == "n":
                if len(data["rangesExcluded"]) > 1:
                    call("clear")
                    hasRangeBetweenNumbers = []
                    for x in data["rangesExcluded"]:
                        firstNumber = x[0]
                        lastNumber = x[1]
                        hasRangeBetweenNumbers.append((lastNumber - firstNumber) > 1)
                    for rangeCheck in hasRangeBetweenNumbers:
                        if rangeCheck:
                            hasRangeBetweenNumbers = True
                        else:
                            hasRangeBetweenNumbers = False
                    if not(hasRangeBetweenNumbers):
                        sleep(2)
                        print("\nCongratulations! We found the range that is causing the error.\n")
                        print("You can close this program and add the range to rtc-blacklist in NVRAM -> Add -> 4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102 in your config.plist.")
                        sleep(2)

                        rtcBlacklist = "".join(format(y, "02X") for x in data["rangesExcluded"] for y in x)
                        print(f"\nrtc-blacklist={rtcBlacklist}\n")

                        sleep(3)
                        print("Thanks for using my program! God bless you!")

                        sleep(2)
                        exit_option = input("\nPress enter to exit...")
                        exit = True

                if not(exit):
                    call("clear")
                    print("We found the error. Let's mitigate!")

                    if len(data["rangesExcluded"]) > 1:
                        print("We have multiple ranges excluded. Let's split out one by one to mitigate the error.")

                    data["rangeHalf"].clear()
                    data["rangeCombination"] = 0

                    for i, rng in enumerate(data["rangesExcluded"]):
                        rangeHalf = int((rng[0] + rng[1]) / 2)
                        firstRangeHalfExcluded = [rng[0], rangeHalf]
                        data["rangesTried"].append(rng)
                        data["rangesExcluded"].remove(rng)
                        data["rangesExcluded"].insert(i, firstRangeHalfExcluded)
                        data["rangeHalf"].insert(i, [rangeHalf + 1, rng[1]])

                    data["rangeOriginal"] = data["rangesExcluded"].copy()

                    print("\nLet's split our RTC range. Test the first half.")
                    sleep(2)
                    print("\nChange the range to this in your boot-args: ")

                    rangesResult = ','.join(['-'.join(format(y, '02X') for y in x) for x in data['rangesExcluded']])
                    print(f"\nrtcfx_exclude={rangesResult}")
                    data["rangesExcludedInHex"] = rangesResult

                    with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)

                    sleep(2)
                    print("\nNow reboot.")
                    exit_option = input("\nPress enter to exit...")
                    exit = True
            else:
                call("clear")
                print("Invalid answer")
                sleep(2)
            continue
        # 2. Start over the process
        elif option == "2":
            important_option = input("Do you really want to start the process again? (y/n) ")

            if important_option == "y":
                print("Starting over the process...")
                data = init_data
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(init_data, f, indent=4)
                sleep(2)
                call("clear")
            elif important_option == "n":
                call("clear")
                continue
            else:
                call("clear")
                print("Invalid answer")
                sleep(2)
                continue
        # 3. Exit
        elif option == "3":
            print("Exiting")
            exit = True
            continue
        else:
            call("clear")
            print("Invalid option")
            sleep(2)
            continue

    print("\nRTCRangeHelper\n")
    print("1. Init the process")
    print("2. Exit")
    
    option = input("\nChoose a option: ")

    # 1. Init the process
    if option == "1":
        call("clear")
        print("Make sure that you already test the DisableRtcChecksum quirk in Kernel -> Quirks")
        sleep(3)
        call("clear")
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
            data["rangesExcludedInHex"] = "00-FF"
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
        call("clear")
        print("Invalid option")
        sleep(2)
        continue

if not_rtc_problem:
    print("It's not a RTC problem. So this helper can not help you.")
