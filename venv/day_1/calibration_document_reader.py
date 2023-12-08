import re

calibration_document_path = "./day_1/calibration_document"
dict_of_digits_spelled = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def getCalibrationFromStringPureDigits(txt):
    # First we remove all the chars from the line
    line_cleaned = re.sub("[a-zA-Z]", "", txt).strip()
    # Then, we calculate the value with the first and last characters in the cleaned line.
    return int(line_cleaned[0]) * 10 + int(line_cleaned[-1])


def getCalibrationFromStringSpelledDigits(txt):
    firstDigit = 0
    lastDigit = 0
    # We need to check if there are pure digits in the text
    digitRegexSearch = re.search("[0-9]", txt)
    if digitRegexSearch is None:
        spelledDigitsDict = lookForSpelledDigits(txt)
        firstDigit = spelledDigitsDict[min(spelledDigitsDict.keys())]
        lastDigit = spelledDigitsDict[max(spelledDigitsDict.keys())]
    else:
        # We need to determine the first digit.
        # There might be a spelled part before the first digit
        firstDigitRegexSearchGroups = re.search("^([a-zA-Z]*)([0-9])", txt).groups()
        firstSpelledPart = firstDigitRegexSearchGroups[0]
        firstPureDigit = int(firstDigitRegexSearchGroups[1])
        # We look for spelled digits in the spelled part
        firstSpelledDigitsDict = lookForSpelledDigits(firstSpelledPart)
        # If there are no spelled digits, the first pure digit is the first digit
        # Otherwise, the first digit is the spelled digit at the lowest position
        if len(firstSpelledDigitsDict) == 0:
            firstDigit = firstPureDigit
        else:
            firstDigit = firstSpelledDigitsDict[min(firstSpelledDigitsDict.keys())]
        # We need to determine the last digit.
        # There might be a spelled part after the last digit
        lastDigitRegexSearchGroups = re.search("([0-9])([a-zA-Z]*)$", txt).groups()
        lastPureDigit = int(lastDigitRegexSearchGroups[0])
        lastSpelledPart = lastDigitRegexSearchGroups[1]
        # We look for spelled digits in the spelled part
        lastSpelledDigitsDict = lookForSpelledDigits(lastSpelledPart)
        # If there are no spelled digits, the last pure digit is the last digit
        # Otherwise, the last digit is the spelled digit at the highest position
        if len(lastSpelledDigitsDict) == 0:
            lastDigit = lastPureDigit
        else:
            lastDigit = lastSpelledDigitsDict[max(lastSpelledDigitsDict.keys())]

    return firstDigit * 10 + lastDigit


def lookForSpelledDigits(txt):
    spelledDigitsDict = {}
    # For each cipher, we find all matches in the txt and we add them to the dictionary
    for cipher in dict_of_digits_spelled.keys():
        cipherPattern = re.compile(cipher)
        for match in cipherPattern.finditer(txt):
            position = match.start()
            spelledDigitsDict[position] = dict_of_digits_spelled[cipher]
    return spelledDigitsDict


def main():
    calibration_document = open(calibration_document_path, "r")
    total_calibration_pure = 0
    total_calibration_spelled = 0
    while True:
        # Get next line from file
        line = calibration_document.readline()
        # if line is empty end of file is reached
        if not line:
            break
        total_calibration_pure += getCalibrationFromStringPureDigits(line)
        total_calibration_spelled += getCalibrationFromStringSpelledDigits(line)
    calibration_document.close()
    print("The solution for the first part is: {pure}".format(pure=str(total_calibration_pure)))
    print("The solution for the second part is: {spelled}".format(spelled=str(total_calibration_spelled)))


if __name__ == "__main__":
    main()

'''
def getCalibrationFromStringSpelledDigitsSimplified(txt):
    txt = txt.replace("one","o1ne")
    txt = txt.replace("two", "t2wo")
    txt = txt.replace("three", "t3hree")
    txt = txt.replace("four", "f4our")
    txt = txt.replace("five", "f5ive")
    txt = txt.replace("six", "s6ix")
    txt = txt.replace("seven", "s7even")
    txt = txt.replace("eight", "e8ight")
    txt = txt.replace("nine", "n9ine")
    return getCalibrationFromStringPureDigits(txt)
'''
