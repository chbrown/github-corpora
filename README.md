# GitHub corpora

Scripts for crawling the GitHub API and resulting data (which is all public).

    export GITHUB_TOKEN=YTaSQhwUqb5gyNKCOXfveplH4GVcEsLxBjW0rnio
    python repositories.py repositories.json

Objects in `repositories.json` are a slight modification of what you get from API v3 /repositories,
mostly deleting the redundant API

    # count number of repos with capitals in the name
    <repositories.json json -C name | grep [A-Z] | wc -l

    # count some other stuff like that
    repository_counts.sh

## License

Code is MIT Licensed, data is licensed with whatever the GitHub API is under.
