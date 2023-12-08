import re

almanac_document_path = "/home/rodrigo/PycharmProjects/AdventOfCode2023/venv/day_5/almanac_document"

def read_almanac_line(txt):
    line_match = re.search("^([0-9]+) ([0-9]+) ([0-9]+)$", txt)
    destination_start = int(line_match.groups()[0])
    source_start = int(line_match.groups()[1])
    range = int(line_match.groups()[2])
    return (destination_start, source_start, range)

def find_mapping(element,almanac_document):
    while True:
        # Get next line from file
        line = almanac_document.readline()
        # if line is empty end of file is reached
        if not line or line == "\n":
            return element
        destination_start, source_start, range = read_almanac_line(line)
        # If we have the match in this line return the destination
        if (element >= source_start) and (element < source_start + range):
            return destination_start + (element - source_start)

def find_location(seed):
    #print("seed: {myseed}".format(myseed=seed))
    almanac_document = open(almanac_document_path, "r")
    current_element = seed
    # We skip the first line that only contain the seeds
    almanac_document.readline()
    almanac_document.readline()
    while True:
        # Get next line from file
        line = almanac_document.readline()
        # if line is empty end of file is reached
        if not line:
            break
        if line == "":
            continue
        element_declaration_match = re.search("^([^\s]*) map:",line)
        if element_declaration_match:
            element_name = element_declaration_match.groups()[0]
            element_mapping = find_mapping(current_element, almanac_document)
            #print("\t{element} {mapping}".format(element=element_name, mapping=element_mapping))
            current_element = element_mapping
    almanac_document.close()
    return element_mapping

def find_subrange(element_start, element_range, destination_start, source_start, source_range):
    subrange_start=None
    subrange_range=None
    # First we make sure that we have subranges. If there is no intersection we do nothing
    if not ((element_start >= source_start + source_range) or (element_start+element_range <= source_start)):
        subrange_start = destination_start + (max([element_start,source_start]) - source_start)
        subrange_range = min([element_start+element_range,source_start+source_range])-(max([element_start,source_start]))
    return (subrange_start, subrange_range)

def update_current_subranges(current_subranges, source_start, source_range):
    current_subranges_updated = []
    for current_element_start, current_element_range in current_subranges:
        if (current_element_start < source_start):
            if (current_element_start + current_element_range <= source_start):
                current_subranges_updated.append((current_element_start, current_element_range))
            else:
                current_subranges_updated.append((current_element_start, source_start - current_element_start))
        if (current_element_start + current_element_range > source_start + source_range):
            if (source_start + source_range <= current_element_start):
                current_subranges_updated.append((current_element_start, current_element_range))
            else:
                current_subranges_updated.append((source_start + source_range, current_element_start + current_element_range - source_start - source_range))
    return current_subranges_updated

def find_location_subranges(seed, seed_range):
    #print("seed: {myseed}; seed rage: {myseedrange}".format(myseed=seed,myseedrange=seed_range))
    almanac_document = open(almanac_document_path, "r")
    current_subranges = [(seed, seed_range)]
    next_subranges = []
    # We skip the first line that only contain the seeds
    almanac_document.readline()
    almanac_document.readline()
    while True:
        # Get next line from file
        line = almanac_document.readline()
        # if line is empty end of file is reached
        if not line:
            if len(current_subranges) > 0:
                next_subranges.extend(current_subranges)
            current_subranges = next_subranges
            #print("\tSubranges : {subranges}".format(element=element_name, subranges=next_subranges))
            break

        if line == "\n":
            if len(current_subranges) > 0:
                next_subranges.extend(current_subranges)
            current_subranges = next_subranges
            #print("\tSubranges : {subranges}".format(element=element_name, subranges=next_subranges))
            next_subranges = []
            continue

        element_declaration_match = re.search("^([^\s]*) map:",line)
        if element_declaration_match:
            element_name = element_declaration_match.groups()[0]
            #print("{element} :".format(element=element_name))

        else:
            destination_start, source_start, source_range = read_almanac_line(line)
            # We check the intersection with new mappings defined by the line read from the almanac document.
            for current_element_start, current_element_range in current_subranges:
                new_element_start, new_element_range = find_subrange(current_element_start, current_element_range, destination_start, source_start, source_range)
                if new_element_start and new_element_range:
                    current_subranges = update_current_subranges(current_subranges, source_start, source_range)
                    next_subranges.append((new_element_start,new_element_range))

    almanac_document.close()
    return next_subranges

def main():
    # First part:
    # First we read the seeds.
    almanac_document = open(almanac_document_path, "r")
    seeds  = list(map(int,re.search("^seeds: ([0-9\s]+)$",almanac_document.readline()).groups()[0].split()))
    almanac_document.close()
    locations = []
    # For each seed, we need to find the combination
    for seed in seeds:
        locations.append(find_location(seed))
    # For the first part solution
    print("The solution to part 1 is {min_location}".format(min_location=min(locations)))

    # Second part
    # First we read the seed ranges.
    almanac_document = open(almanac_document_path, "r")
    seed_lines = almanac_document.readline().strip()
    numbers_pattern = re.compile("([0-9]+) ([0-9]+)")
    locations = []
    for match in numbers_pattern.finditer(seed_lines):
        locations.extend(find_location_subranges(int(match.groups()[0]), int(match.groups()[1])))
    print("The solution to part 2 is {min_location}".format(min_location=min(sorted(locations))[0]))
    almanac_document.close()

if __name__ == "__main__":
    main()