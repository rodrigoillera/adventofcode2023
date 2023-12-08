import re

engine_document_path = "/home/rodrigo/PycharmProjects/AdventOfCode2023/venv/day_3/engine_document"
def get_symbols_coordinates(document_path):
    document = open(document_path, "r")
    symbols_coordinates_dict = {}
    count=0
    while True:
        # Get next line from file
        line = document.readline()
        # if line is empty end of file is reached
        if not line:
            break
        symbols_pattern = re.compile("[^0-9\.]")
        for match in symbols_pattern.finditer(line.strip()):
            if str(count) not in symbols_coordinates_dict:
                symbols_coordinates_dict[str(count)] = {}
            symbols_coordinates_dict[str(count)][str(match.span()[0])] = {"symbol": match.group(), "adjacents":[]}
        count += 1
    document.close()
    return symbols_coordinates_dict

def is_valid_number(row, first_position, last_position, symbols_coordinates, num):
    is_valid = False
    # First we check for symbols in the same row
    if str(row) in symbols_coordinates:
        # If the previous or the next characters of the match is a symbol, then this is a valid number.
        if str(first_position-1) in symbols_coordinates[str(row)]:
            symbols_coordinates[str(row)][str(first_position-1)]["adjacents"].append(int(num))
            is_valid = True
        if str(last_position + 1) in symbols_coordinates[str(row)]:
            symbols_coordinates[str(row)][str(last_position + 1)]["adjacents"].append(int(num))
            is_valid = True
    # Then, we check for symbols in the previous row
    if str(row-1) in symbols_coordinates:
        # For each symbol, we check its column
        for symbol_col in symbols_coordinates[str(row-1)].keys():
            if int(symbol_col) >= (first_position - 1) and int(symbol_col) <= (last_position+1):
                symbols_coordinates[str(row-1)][symbol_col]["adjacents"].append(int(num))
                is_valid = True
    # Then, we check for symbols in the next row
    if str(row+1) in symbols_coordinates:
        # For each symbol, we check its column
        for symbol_col in symbols_coordinates[str(row+1)].keys():
            if int(symbol_col) >= (first_position - 1) and int(symbol_col) <= (last_position+1):
                symbols_coordinates[str(row + 1)][symbol_col]["adjacents"].append(int(num))
                is_valid = True
    return is_valid

def main():
    symbols_coordinates = get_symbols_coordinates(engine_document_path)
    num_current_line = 0
    valid_numbers_list = []
    engine_document = open(engine_document_path, "r")
    while True:
        # Get next line from file
        line = engine_document.readline()
        # if line is empty end of file is reached
        if not line:
            break
        numbers_pattern = re.compile("[0-9]+")
        for match in numbers_pattern.finditer(line.strip()):
            if is_valid_number(num_current_line, match.span()[0], match.span()[1]-1, symbols_coordinates,match.group()):
                valid_numbers_list.append(int(match.group()))
        num_current_line += 1
    engine_document.close()
    print("The solution for the first part is: {solution}".format(solution=str(sum(valid_numbers_list))))
    gear_ratio_sum=0
    for row in symbols_coordinates.keys():
        for col in symbols_coordinates[row].keys():
            if symbols_coordinates[row][col]["symbol"] == "*" and len(symbols_coordinates[row][col]["adjacents"]) == 2:
                gear_ratio_sum += symbols_coordinates[row][col]["adjacents"][0]*symbols_coordinates[row][col]["adjacents"][1]

    print("The solution for the second part is: {solution}".format(solution=str(gear_ratio_sum)))


if __name__ == "__main__":
    main()