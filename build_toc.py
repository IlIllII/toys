import os


TITLE_KEY = "title"
TITLE_PREFIX = "# "

DESCRIPTION_KEY = "description"
DESCRIPTION_PREFIX = ">> "


def get_top_directory():
    top_dir = os.path.dirname(os.path.realpath(__file__))
    return top_dir


def get_subdirectories():
    top_dir = get_top_directory()
    print("top_dir: " + top_dir)
    print(os.listdir(top_dir))
    dirs = [d for d in os.listdir(top_dir) if os.path.isdir(os.path.join(top_dir, d))]
    return dirs


def capitalize_readmes():
    for d in get_subdirectories():
        print("subdir: " + d)
        for filename in os.listdir(os.path.join(get_top_directory(), d)):
            if filename.lower() == 'readme.md':
                current_path = os.path.join(get_top_directory(), d, filename)
                new_path = os.path.join(get_top_directory(), d, 'README.md')
                os.rename(current_path, new_path)
                break


def extract_metadata(readme):
    metadata = dict()
    print("Getting metadata for " + readme)
    with open(readme, 'r') as file:
        for line in file.readlines():
            print("Line: ")
            print(line)
            if line.startswith(TITLE_PREFIX):
                _, title = line.split(TITLE_PREFIX, 1)
                title = title.strip()
                metadata[TITLE_KEY] = title
            elif line.startswith(DESCRIPTION_PREFIX):
                _, description = line.split(DESCRIPTION_PREFIX, 1)
                description = description.strip()
                metadata[DESCRIPTION_KEY] = description

            print(TITLE_KEY in metadata)
            print(DESCRIPTION_KEY in metadata)
            if TITLE_KEY in metadata and DESCRIPTION_KEY in metadata:
                print('returning from extract _metadata')
                return metadata
        
    raise Exception(f"Could not parse metadata for {readme}")


def get_toc():
    entries = []
    
    for d in get_subdirectories():
        readme = os.path.join(get_top_directory(), d, 'README.md')
        if os.path.exists(readme):
            metadata = extract_metadata(readme)
            entry = f"| [{metadata[TITLE_KEY]}](./{d}/README.md) | {metadata[DESCRIPTION_KEY]} |"
            entries.append(entry)
    
    print("\nGenerating table of contents...")
    print(entries)
    toc = "\n".join(entries)
    print(toc)
    return toc


def main():
    capitalize_readmes()
    top_level_readme = os.path.join(get_top_directory(), "README.md")
    with open(top_level_readme, 'w') as main_readme:
        main_readme.write("# Toys\n\n")
        main_readme.write("A collection of toy programs.\n\n")
        main_readme.write("## Table of Contents\n\n")
        main_readme.write("| Title | Description |\n| --- | --- |\n")
        main_readme.write(get_toc())
        main_readme.write("\n")


if __name__ == "__main__":
    main()


