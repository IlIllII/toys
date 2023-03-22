# gloc

**Count lines of code in github repos.**

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

## Other Notes

First, unlike `cloc`, `gloc` doesn't actually parse the files that it reports lines of code for. Instead, `gloc` interfaces with GitHub's APIs and uses the provided metadata to calculate lines of code. Since the metadata doesn't provide exact counts or information about comments vs. actualy lines of code, the numbers reported by `gloc` should be properly regarded as upper bounds that are likely ~15% higher than actual line counts, though the percentages should be accurate.

To my knowledge, there is no way to get better data from the API. To tighten this bound, we could scrape `sloc` from each file in a repository, although this requires sending many more requests. To get truly accurate information we would need to fully parse the contents of the repos, which would entail transfering the contents of the repo over the network (or the contents of every repo belonging to a user!). I have added neither of these functions as of right now, so if you need this level of detail you should just clone the repos and run `cloc` yourself.

Second, as of March 2022 GitHub rate limits requests without authenticated tokens to 60/hour. To avoid this, you will have to pass a token as a command line arg. It is recommended not to type your token into the command line because then it will show up in the terminal's history. To keep it safe you can put it in an environment variable.

Finally, if fewer repos get reported than you expect after running the script, try running it again. GitHub calculates and caches some of the data provided through its API, so the first time you hit an endpoint it may return a `202` if it can't perform the calculation fast enough. The script retries multiple times, but for very large calculations it still may take too long. Rerunning the script should take care of it.