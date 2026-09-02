from subprocess import call
from time import sleep
import json

init_data = {
    "notRTCProblem": False,
    "rangesExcludedInHex": "",
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
                    with open("data.json", "w", encoding="utf-8") as f:
                        data["notRTCProblem"] = True
                        json.dump(data, f, indent=4)
                    sleep(4)
                    continue

                if data["rangesExcluded"] == [[0, 255]]:
                    call("clear")
                    print("You can try the 0x00-0x7F and 0x80-0xFF ranges together. The bit between these can be the RTC issue.")

                    print("Change the range to this in your boot-args: ")
                    print("\nrtcfx_exclude=00-7F,80-FF")

                    with open("data.json", "w", encoding="utf-8") as f:
                        data["rangesTried"].append(data["rangesExcluded"][0])
                        data["rangesExcluded"] = [[0, 127], [128, 255]]
                        data["rangesExcludedInHex"] = "00-7F,80-FF"
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
                    with open("data.json", "w", encoding="utf-8") as f:
                        if len(data["rangesExcluded"]) == len(data["rangeHalf"]):
                            data["rangesTried"].append(data["rangesExcluded"][0])
                            data["rangesExcluded"][0] = data["rangeHalf"][0]
                            data["rangeHalf"].pop(0)
                        elif len(data["rangesExcluded"]) > len(data["rangeHalf"]):
                            if len(data["rangeHalf"]) == 1:
                                data["rangesTried"].append(data["rangesExcluded"][-1])
                                data["rangesExcluded"][-1] = data["rangeHalf"][-1]
                                data["rangeHalf"].clear()
                            else:
                                data["rangesTried"].append(data["rangesExcluded"][-abs(len(data["rangeHalf"]))])
                                data["rangesExcluded"][-abs(len(data["rangeHalf"]))] = data["rangeHalf"][-abs(len(data["rangeHalf"]))]
                                data["rangeHalf"].pop(0)
                        else:
                            data["rangesTried"].append(data["rangesExcluded"][0])
                            data["rangesExcluded"] = data["rangeHalf"]
                            data["rangeHalf"].clear()
                        json.dump(data, f, indent=4)

                    print("\nChange the range to this in your boot-args: ")

                    rangesDivided = ["-".join(format(y, "02X") for y in x) for x in data["rangesExcluded"]]
                    print(f"\nrtcfx_exclude={','.join(rangesDivided)}")

                    with open("data.json", "w", encoding="utf-8") as f:
                        data["rangesExcludedInHex"] = ','.join(rangesDivided)
                        json.dump(data, f, indent=4)

                    sleep(2)
                    print("\nNow reboot.")
                    exit_option = input("\nPress enter to exit...")
                    call("clear")
                    exit = True
                else:
                    call("clear")
                    print("The error can be in multiple ranges. Let's try the last both together.")

                    # Come back the last Range tried to Range Excluded
                    with open("data.json", "w", encoding="utf-8") as f:
                        for i in range(len(data["rangesExcluded"])):
                            lastRangeTried = data["rangesTried"][-1]
                            data["rangesExcluded"].insert(0, lastRangeTried)
                            data["rangesTried"].remove(lastRangeTried)
                        data["rangesExcluded"].sort()
                        json.dump(data, f, indent=4)

                    print("\nChange the range to this in your boot-args: ")

                    rangesDivided = ["-".join(format(y, "02X") for y in x) for x in data["rangesExcluded"]]
                    print(f"\nrtcfx_exclude={','.join(rangesDivided)}")

                    with open("data.json", "w", encoding="utf-8") as f:
                        data["rangesExcludedInHex"] = ','.join(rangesDivided)
                        json.dump(data, f, indent=4)

                    sleep(2)
                    print("\nNow reboot.")
                    exit_option = input("\nPress enter to exit...")
                    call("clear")
                    exit = True

            elif errorQuestion.lower() == "n":
                if (len(data["rangesExcluded"]) > 1):
                    call("clear")
                    for x in data["rangesExcluded"]:
                        firstNumber = x[0]
                        lastNumber = x[1]
                        hasRangeBetweenNumbers = (lastNumber - firstNumber) > 1
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

                    rangesList = []
                    for i in range(len(data["rangesExcluded"])):
                        DIFF_BETWEEN_RANGES_NUMBER = 1
                        isFirstNumberRangeExcludedGreaterThanZero = True if data["rangesExcluded"][0][0] > 0 else False
                        firstNumberRangeExcludedDiffDivided = int((data["rangesExcluded"][i][-1] - data["rangesExcluded"][i][0]) / 2) + DIFF_BETWEEN_RANGES_NUMBER
                        firstHalfRangeExcluded = [data["rangesExcluded"][i][0], data["rangesExcluded"][i][-1] - firstNumberRangeExcludedDiffDivided if isFirstNumberRangeExcludedGreaterThanZero else int(data["rangesExcluded"][i][-1] / 2)]

                        otherHalfRangeExcluded = [(data["rangesExcluded"][i][-1] + DIFF_BETWEEN_RANGES_NUMBER) - firstNumberRangeExcludedDiffDivided if isFirstNumberRangeExcludedGreaterThanZero else data["rangesExcluded"][i][-1] - int(data["rangesExcluded"][i][-1] / 2), data["rangesExcluded"][i][-1]]

                        rangesList.append([firstHalfRangeExcluded, otherHalfRangeExcluded])
                        # Move the range excluded to rangesTried
                        rangeExcluded = data["rangesExcluded"][i]
                        data["rangesTried"].append(rangeExcluded)

                    print("\nLet's split our RTC range. Test the first half.")
                    sleep(2)
                    print("\nChange the range to this in your boot-args: ")

                    # Add current range excluded to rangesExcluded
                    with open("data.json", "w", encoding="utf-8") as f:
                        if len(data["rangesExcluded"]) > 1:
                            for x in rangesList:
                                data["rangesExcluded"].append(x[0])
                        else:
                            data["rangesExcluded"].append(firstHalfRangeExcluded)
                        json.dump(data, f, indent=4)

                    # Remove the rangesExcluded already moved to rangesTried
                    with open("data.json", "w", encoding="utf-8") as f:
                        for i in range(len(rangesList)):
                            data["rangesExcluded"].pop(0)
                        json.dump(data, f, indent=4)

                    if len(data["rangesExcluded"]) > 1:
                        rangesDivided = ["-".join(format(y, "02X") for y in x) for x in data["rangesExcluded"]]
                        print(f"\nrtcfx_exclude={','.join(rangesDivided)}")
                    else:
                        print(f"\nrtcfx_exclude={firstHalfRangeExcluded[0]:02X}-{firstHalfRangeExcluded[1]:02X}")

                    # Add the other half range excluded to rangeHalf
                    with open("data.json", "w", encoding="utf-8") as f:
                        data["rangeHalf"] = []
                        if len(data["rangesExcluded"]) > 1:
                            for x in rangesList:
                                data["rangeHalf"].append(x[1])
                        else:
                            data["rangeHalf"].append(otherHalfRangeExcluded)
                        json.dump(data, f, indent=4)

                    with open("data.json", "w", encoding="utf-8") as f:
                        if len(data["rangesExcluded"]) > 1:
                            data["rangesExcludedInHex"] = ','.join(rangesDivided)
                        else:
                            data["rangesExcludedInHex"] = f"{firstHalfRangeExcluded[0]:02X}-{firstHalfRangeExcluded[1]:02X}"
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
            with open("data.json", "w", encoding="utf-8") as f:
                data["rangesExcludedInHex"] = "00-FF"
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
