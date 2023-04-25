import sys

file_name = sys.argv[1]

lines = []

with open(file_name) as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        tokens = line.split(" ")
        if tokens[0] == "for":
            prefix = tokens[:3]
            suffix = tokens[3:]
            suffix.reverse()
            for j, token in enumerate(suffix):
                suffix[j] = token.strip("\n")
            tokens_merged = prefix + suffix
            edited_line = " ".join(tokens_merged)
            lines[i] = edited_line

with open(file_name, "w") as f:
    f.writelines(lines)