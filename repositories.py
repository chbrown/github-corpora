import os
import sys
import json
import requests


filename = sys.argv[1]

headers = dict(Authorization='token %s' % os.environ['GITHUB_TOKEN'])

line = None
with open(filename, 'r') as repos_in:
    for line in repos_in:
        pass

since = json.loads(line)['id'] if line else 0

with open(filename, 'a') as repos_out:
    while True:
        r = requests.get('https://api.github.com/repositories', headers=headers, params=dict(since=since))
        entries = r.json()
        print '%d since %d' % (len(entries), since)
        for entry in entries:
            repo = {
                'id': entry['id'],
                'name': entry['name'],
                'full_name': entry['full_name'],
                'description': entry['description'],
                'fork': entry['fork'],
                'owner': entry['owner']['login'],
                'owner_id': entry['owner']['id'],
                'owner_type': entry['owner']['type'],
            }
            repos_out.write('%s\n' % json.dumps(repo))
        since = entries[-1]['id']
