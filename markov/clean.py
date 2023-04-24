import os


def remove_passage_numbers(filename: str) -> None:
    tmp = "tmp.txt"
    with open(filename) as f:
        with open(tmp, "w") as f2:
            for line in f.readlines():
                words = line.split()
                words = [word for word in words if not word.isdigit() and not ":" in word]
                if len(words) > 0:
                    f2.write(" ".join(words) + "\n")

    os.remove(filename)
    os.rename(tmp, filename)
    os.remove(tmp)

if __name__ == "__main__":
    remove_passage_numbers("text.txt")
    print("Done!")