from nltk.metrics.distance import edit_distance
import re


def most_probable_command(cmd_robot, word):
    distance = [edit_distance(word.lower(), w_cmd.lower()) for w_cmd in cmd_robot]
    index = distance.index(min(distance))
    return cmd_robot[index]


def most_probable_number(word):
    match = re.search(r'\d+', word)
    if match:
        return int(match.group())
    else:
        return None
