import os
import json
import requests
import httplib
import filesequence


headers = dict(Authorization='token %s' % os.environ['GITHUB_TOKEN'])

filenames = filesequence.interpolator('data/repositories-%02d.json', xrange(1, 100))

with filesequence.open(filenames, 50000000, flag='a+') as output:
    # sequence.tail() may very well return an empty list
    entries = [dict(id=0)] + [json.loads(line) for line in output.tail()]

    # since = ['id'] if line else 0
    since = entries[-1]['id']

    while True:
        try:
            r = requests.get('https://api.github.com/repositories', headers=headers, params=dict(since=since))
        except httplib.IncompleteRead, exc:
            print exc
            print 'continuing'
            continue

        entries = r.json()

        remaining = r.headers.get('x-ratelimit-remaining', '0')
        limit = r.headers.get('x-ratelimit-limit', '0')
        print '%d since %d (%s/%s)' % (len(entries), since, remaining, limit)
        if 'message' in entries:
            print 'Error:', entries['message'], r
            continue

        if len(entries) < 10:
            print 'Too few entries'
            print entries

        for entry in entries:
            owner = entry['owner'] or {'login': 'N/A', 'id': 'N/A', 'type': 'N/A'}
            repo = {
                'id': entry['id'],
                'name': entry['name'],
                'full_name': entry['full_name'],
                'description': entry['description'],
                'fork': entry['fork'],
                'owner': owner['login'],
                'owner_id': owner['id'],
                'owner_type': owner['type'],
            }
            output.write('%s\n' % json.dumps(repo))

        since = entries[-1]['id']
