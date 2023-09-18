# gloc

>> Count lines of code in github repos

## Example usage

```bash
py gloc.py USERNAME
```

Output:

```
Total LoC for USERNAME (25 repos): 170539.
Breakdown:
------------------------------------------
  Vue:                      108411 (63.57%)
  Java:                      40153 (23.54%)
  JavaScript:                 8059 (4.73%)
  Python:                     4367 (2.56%)
  Swift:                      2277 (1.34%)
  TypeScript:                 2274 (1.33%)
```

You can also get lines of code for a single repo:

```bash
py gloc.py USERNAME --repo=REPO_NAME
```

## Command Line Arguments

Optional command line arguments include:

1. `--extended` or `-e` to list all languages, even those comprising less than 1% of total lines.
2. `--repo=REPOSITORY_NAME` to only count lines of code in REPOSITORY_NAME.
3. `--token=TOKEN` to include an authentication TOKEN to avoid GitHub's rate limits.
