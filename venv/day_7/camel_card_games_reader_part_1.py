import re
import functools

camel_card_games_document_path = "/home/rodrigo/PycharmProjects/AdventOfCode2023/venv/day_7/camel_card_games_document"

cardValueDict = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
}

@functools.total_ordering
class Game:

    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        # 7: Five of a kind, where all five cards have the same label: AAAAA
        # 6: Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        # 5: Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        # 4: Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        # 3: Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        # 2: One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        # 1: High card, where all cards' labels are distinct: 23456
        sorted_cards = sorted(list(cards))
        kinds = []
        kind = 1
        for i in range(1,len(sorted_cards)):
            if sorted_cards[i] == sorted_cards[i-1]:
                kind += 1
            else:
                kinds.append(kind)
                kind = 1
        kinds.append(kind)
        sorted_kinds = sorted(kinds,reverse=True)
        match sorted_kinds:
            case [1,1,1,1,1]:
                self.type = 1
            case [2,1,1,1]:
                self.type = 2
            case [2,2,1]:
                self.type = 3
            case [3,1,1]:
                self.type = 4
            case [3,2]:
                self.type = 5
            case [4,1]:
                self.type = 6
            case [5]:
                self.type = 7

    def __eq__(self, other_game):
        if self.type == other_game.type and self.cards == other_game.cards:
            return True
        else:
            return False

    def __gt__(self, other_game):
        if self.type > other_game.type:
            return True
        elif self.type == other_game.type:
            for i in range(5):
                if cardValueDict[self.cards[i]] > cardValueDict[other_game.cards[i]]:
                    return True
                elif cardValueDict[self.cards[i]] < cardValueDict[other_game.cards[i]]:
                    return False
        return False

    def __lt__(self, other_game):
        if self.type < other_game.type:
            return True
        elif self.type == other_game.type:
            for i in range(5):
                if cardValueDict[self.cards[i]] < cardValueDict[other_game.cards[i]]:
                    return True
                elif cardValueDict[self.cards[i]] > cardValueDict[other_game.cards[i]]:
                    return False
        return False

    def __ge__(self, other_game):
        if self.__eq__(other_game) or self.__gt__(other_game):
            return True
        else:
            return False

    def __le__(self, other_game):
        if self.__eq__(other_game) or self.__lt__(other_game):
            return True
        else:
            return False


def quickSort(games_list):
    quickSortHelper(games_list, 0, len(games_list) - 1)

def quickSortHelper(games_list, first, last):
    if first < last:
        splitpoint = partition(games_list, first, last)

        quickSortHelper(games_list, first, splitpoint - 1)
        quickSortHelper(games_list, splitpoint + 1, last)

def partition(alist,first,last):
   pivotvalue = alist[first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp

   return rightmark


def main():
    # First part
    camel_card_games_document = open(camel_card_games_document_path, "r")
    list_of_games = []
    while True:
        # Get next line from file
        line = camel_card_games_document.readline()
        # if line is empty end of file is reached
        if not line:
            break
        game_match = re.search("^([0-9TJQKA]+) ([0-9]+)$", line)
        list_of_games.append(Game(game_match.groups()[0], game_match.groups()[1]))
    camel_card_games_document.close()
    quickSort(list_of_games)
    winnings = 0
    for i in range (len(list_of_games)):
        game = list_of_games[i]
        winnings += int(game.bid)*(i+1)
        print("Range: {gamerange}, Cards: {gamecards}, Type, {gametype}, Bid: {gamebid}".format(gamerange=str(i+1), gamecards=game.cards, gametype=game.type, gamebid=game.bid))
    print("The solution to part 1 is {result}".format(result=winnings))

if __name__ == "__main__":
    main()