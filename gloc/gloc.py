import sys
import time

import requests

# command line arguments populate these variables
owner = None  # Required
repository = None  # optional
extended = False  # optional
token = None  # optional


def hit_endpoint(owner: str, endpoint_type: str, endpoint: str) -> dict or None:
    """Hit a GitHub API endpoint and return JSONified data.
    Endpoint is the path following `owner/` in the API URL, such as:
    \t`https://api.github.com/{endpoint_type}/{owner}{endpoint}`
    """

    response = None
    tries = 0
    wait = 0.5
    success = 200
    while response is None and tries < 4:
        if token is not None:
            response = requests.get(
                f"https://api.github.com/{endpoint_type}/{owner}{endpoint}",
                headers={
                    "Authorization": f"token {token}",
                },
                params={"visibility": "all"},
            )
        else:
            response = requests.get(
                f"https://api.github.com/{endpoint_type}/{owner}{endpoint}"
            )

        if response.status_code == success:
            break
        else:
            time.sleep(wait)
            response = None
        tries += 1

    if response is None:
        print(f"Error locating endpoint:{endpoint} from {owner}")
        return None

    return response.json()


def get_all_repos(owner: str):
    return hit_endpoint(owner, "users", "/repos")


def get_repo_languages(owner: str, repo: str):
    return hit_endpoint(owner, "repos", f"/{repo}/languages")


def get_repo_frequency(owner: str, repo: str):
    return hit_endpoint(owner, "repos", f"/{repo}/stats/code_frequency")


def get_repo_contents(owner: str, repo: str):
    return hit_endpoint(owner, "repos", f"/{repo}/contents")


def accumulate_loc(loc_data: list) -> int:
    """Take raw data from `stats/code_frequency` and return total LoC in repo.
    Args:
        loc_data (list): [[int, int, int]], where each inner list is a week of data: [timestamp, additions, deletions]
    Returns:
        int: total lines in the repo (including comments!)
    """

    total = 0
    for week in loc_data:
        total += week[1] + week[2]
    return total


def format_repo_data(languages: dict, total_loc: int):
    """Change byte values to raw lines of code."""

    total_bytes = 0
    for language in languages.keys():
        total_bytes += languages[language]

    for language in languages.keys():
        languages[language] = int((languages[language] / total_bytes) * total_loc)

    return languages, total_loc


def collect_repo_data(owner: str, repo: str):
    languages = get_repo_languages(owner, repo)
    loc_data = get_repo_frequency(owner, repo)

    if languages is not None and loc_data is not None:
        total_loc = accumulate_loc(loc_data)
        return format_repo_data(languages, total_loc)
    else:
        return None


def collect_user_level_data(owner: str):
    repos = get_all_repos(owner)
    data_collection = dict()

    for repo in repos:
        data = collect_repo_data(owner, repo["name"])
        if data is not None:
            formatted = format_repo_data(data[0], data[1])
            datum = {
                "languages": formatted[0],
                "total_loc": formatted[1],
            }
            data_collection[repo["name"]] = datum

    return data_collection


def print_language_breakdown(languages: dict, total_loc: int):
    print("-" * 42)
    for language in sorted(
        languages.keys(), key=lambda lang: languages[lang], reverse=True
    ):
        padding = 15
        percent = languages[language] / total_loc * 100
        lines = languages[language]
        if extended or percent >= 1:
            print(
                f"  {language}:{' ' * (padding - len(language))}{' ' * (padding - len(str(lines)))} {lines} ({percent:0.2f}%)"
            )


def print_repo_data(repo_name: str):
    data = collect_repo_data(owner, repo_name)
    if data is not None:
        languages, total_loc = data
    else:
        print(f"Something went wrong collecting information for {repo_name}")
        return

    print(f"Total LoC for {repo_name}: {total_loc}.\nBreakdown:")
    print_language_breakdown(languages, total_loc)


def print_user_level_data(owner: str):
    data = collect_user_level_data(owner)
    if data is None:
        print("Something went wrong!")
        return

    total_loc = 0
    languages = dict()
    for repo in data.keys():
        total_loc += data[repo]["total_loc"]
        for lang in data[repo]["languages"]:
            if lang in languages.keys():
                languages[lang] += data[repo]["languages"][lang]
            else:
                languages[lang] = data[repo]["languages"][lang]

    print(f"Total LoC for {owner} ({len(data.keys())} repos): {total_loc}.\nBreakdown:")
    print_language_breakdown(languages, total_loc)


if __name__ == "__main__":
    args = sys.argv

    if len(args) == 1:
        print("Must pass a username as a command line arg at minimum.")
        exit(0)

    for arg in args[1:]:
        if arg[0] != "-":
            owner = arg
        else:
            if "=" in arg:
                flag, value = arg.split("=")
                if flag == "--repo":
                    respository = value
                if flag == "--token":
                    token = value
            else:
                if arg == "--extended" or arg == "-e":
                    extended = True

    if owner == None:
        print("Must pass a username as a command line arg.")
        exit(0)

    print("Gathering data...\n", flush=True)
    if repository is not None:
        print_repo_data(repository)
    else:
        print_user_level_data(owner)