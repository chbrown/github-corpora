# GitHub corpora

Scripts for crawling the GitHub API and resulting data (which is all public).

    export GITHUB_TOKEN=YTaSQhwUqb5gyNKCOXfveplH4GVcEsLxBjW0rnio
    python repositories.py repositories.json

Objects in `repositories.json` are a slight modification of what you get from API v3 /repositories,
mostly deleting the redundant urls that can be predicted, presumably, given the `full_name` field.

    # count number of repos with capitals in the name
    <repositories.json json -C name | grep [A-Z] | wc -l

    # count some other stuff like that
    repository_counts.sh

Based on IDs, there are currently ~10 million Github repositories, about 52% of which are public.

## License

Code is MIT Licensed, data is licensed with whatever the GitHub API is under.
