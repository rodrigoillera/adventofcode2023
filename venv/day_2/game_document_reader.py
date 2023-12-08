import re

game_document_path = "/home/rodrigo/PycharmProjects/AdventOfCode2023/venv/day_2/cube_games"

colors_dict = {
    "red": 12,
    "green": 13,
    "blue": 14
}
def game_is_possible(txt):
    # We find all the occurrences of every color and we check if the number exceed the predefined number for the color
    for color in colors_dict.keys():
        color_pattern = re.compile("([0-9]+) " + color)
        for match in color_pattern.finditer(txt):
            num = int(match.groups()[0])
            if num > colors_dict[color]:
                return False
    return True

def get_game_power(txt):
    # We find all the occurrences of every color and we find the highest number of cubes
    power = 1
    for color in colors_dict.keys():
        color_pattern = re.compile("([0-9]+) " + color)
        required_balls = 0
        for match in color_pattern.finditer(txt):
            num = int(match.groups()[0])
            if num > required_balls:
                required_balls = num
        power = power*required_balls
    return power


def main():
    game_document = open(game_document_path, "r")
    sum_part_1 = 0
    sum_part_2 = 0
    while True:
        # Get next line from file
        line = game_document.readline()
        # if line is empty end of file is reached
        if not line:
            break
        game_id = re.search("Game ([0-9]+):", line).groups()[0]
        if game_is_possible(line):
            sum_part_1 += int(game_id)
        sum_part_2 += get_game_power(line)
    print("The solution for the first part is: {solution}".format(solution=sum_part_1))
    print("The solution for the second part is: {solution}".format(solution=sum_part_2))
    game_document.close()


if __name__ == "__main__":
    main()
