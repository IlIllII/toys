import random

N = 2


def make_starting_prefix_array(n: int = N):
    return ["\n"] * N


def make_key(*args):
    key = ""
    for arg in args:
        key += str(arg)
    return key


def construct_prefix_map(filename: str) -> dict:
    prefix_map = dict()
    prefixes = make_starting_prefix_array()
    with open(filename) as f:
        for line in f.readlines():
            words = line.split()
            for word in words:
                prefix_map[make_key(*prefixes)] = prefix_map.get(make_key(*prefixes), []) + [word]
                prefixes[:-1] = prefixes[1:]
                prefixes[-1] = word
    prefix_map[make_key(*prefixes)] = prefix_map.get(make_key(*prefixes), []) + ["\n"]
    return prefix_map


def generate_text(n: int, prefix_map: dict):
    prefixes = make_starting_prefix_array()
    for i in range(n):
        suffixes = prefix_map[make_key(*prefixes)]
        word = random.choice(suffixes)
        print(word, end=" ")
        if word == "\n":
            prefixes = make_starting_prefix_array()
        prefixes[:-1] = prefixes[1:]
        prefixes[-1] = word


if __name__ == "__main__":
    prefix_map = construct_prefix_map("text.txt")
    generate_text(100, prefix_map)