import re
import math

scratchcards_document_path = "/home/rodrigo/PycharmProjects/AdventOfCode2023/venv/day_4/scratchcards_document"

def scratchcard_parser(txt):
    scratchcard_match = re.search("Card\s+([0-9]+): ([0-9\s]+) \| ([0-9\s]+)",txt)
    card_id = scratchcard_match.groups()[0]
    winning_numbers_list = scratchcard_match.groups()[1].split()
    played_numbers_list = scratchcard_match.groups()[2].split()
    return (card_id , winning_numbers_list, played_numbers_list)

def get_victories_number(winning_numbers_list, played_numbers_list):
    number_of_victories = 0
    for winning_number in winning_numbers_list:
        if winning_number in played_numbers_list:
            number_of_victories += 1
    return number_of_victories


def main():

    scratchcards_document = open(scratchcards_document_path, "r")
    cards_record_dict = {}
    total_points = 0
    while True:
        # Get next line from file
        line = scratchcards_document.readline()
        # if line is empty end of file is reached
        if not line:
            break
        card_id, winning_numbers_list, played_numbers_list = scratchcard_parser(line)
        num_of_victories = get_victories_number(winning_numbers_list, played_numbers_list)
        # For the first part solution
        if num_of_victories>0:
            total_points += math.pow(2, num_of_victories-1)
        # For the second part solution we initialise our record
        cards_record_dict[card_id]={"victories":num_of_victories, "count":1}

    # For the first part solution
    print("The solution to part 1 is {points}".format(points=int(total_points)))
    scratchcards_document.close()

    # For the second part solution
    # First we count the original scratchcards
    num_of_scratchcards = len(cards_record_dict.keys())
    for card_id in cards_record_dict.keys():
        num_of_victories = cards_record_dict[card_id]["victories"]
        cards_count=cards_record_dict[card_id]["count"]
        for i in range(1,num_of_victories+1):
            cards_record_dict[str(int(card_id)+i)]["count"]+=cards_count
        num_of_scratchcards += num_of_victories*cards_count
    # For the first part solution
    print("The solution to part 2 is {scratchcards}".format(scratchcards=int(num_of_scratchcards)))

if __name__ == "__main__":
    main()