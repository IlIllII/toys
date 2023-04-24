import random


def construct_prefix_map(filename: str):
    prefix_map = dict()
    first = second = "\n"
    with open(filename) as f:
        for line in f.readlines():
            words = line.split()
            for word in words:
                prefix_map[first + second] = prefix_map.get(first + second, []) + [word]
                first, second = second, word
    prefix_map[first + second] = prefix_map.get(first + second, []) + ["\n"]
    return prefix_map

def generate_text(n: int, prefix_map: dict):
    first = second = "\n"
    for i in range(n):
        suffixes = prefix_map[first + second]
        word = random.choice(suffixes)
        print(word, end=" ")
        if word == "\n":
            first = second = "\n"
        first, second = second, word

if __name__ == "__main__":
    prefix_map = construct_prefix_map("text.txt")
    generate_text(100, prefix_map)