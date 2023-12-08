import re
import math

boat_race_records_document_path = "/home/rodrigo/PycharmProjects/AdventOfCode2023/venv/day_6/boat_race_records_document"

def get_possible_distance_travelled(race_time):
    time = range(race_time+1)
    distance_travelled = [((race_time - time_holding_button) * time_holding_button) for time_holding_button in time]
    return distance_travelled

def main():
    # First part
    boat_race_records_document = open(boat_race_records_document_path, "r")
    race_times_list = list(
        map(int,re.search("^Time: ([0-9\s]+)$",boat_race_records_document.readline()).groups()[0].split())
    )
    record_distances_list = list(
        map(int, re.search("^Distance: ([0-9\s]+)$", boat_race_records_document.readline()).groups()[0].split())
    )
    boat_race_records_document.close()
    power = 1
    for i in range(len(race_times_list)):
        race_time = race_times_list[i]
        record_distance = record_distances_list[i]
        possible_distance_travelled = get_possible_distance_travelled(race_time)
        ways_to_win = list(filter(lambda d: d>record_distance, possible_distance_travelled))
        power = power*len(ways_to_win)
    print("The solution to part 1 is {pow}".format(pow=power))

    # Second part
    boat_race_records_document = open(boat_race_records_document_path, "r")
    race_time = int("".join(re.search("^Time: ([0-9\s]+)$", boat_race_records_document.readline()).groups()[0].split()))
    record_distance = int("".join(re.search("^Distance: ([0-9\s]+)$", boat_race_records_document.readline()).groups()[0].split()))
    boat_race_records_document.close()
    time_holding_button = ((race_time-math.sqrt(math.pow(race_time,2)-4*record_distance))/2)
    print("The solution to part 2 is {result}".format(result=int(race_time-2*time_holding_button)))

if __name__ == "__main__":
    main()