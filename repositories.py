import os
import sys
import json
import requests


headers = dict(Authorization='token %s' % os.environ['GITHUB_TOKEN'])


class FileSequence(object):
    # breaks only on newlines

    # indexes that come up in filenames start at 1
    index = 1

    # each file will contain no more than `limit` bytes
    limit = 5e7

    # the current file that's open
    current_file = None
    current_bytes = 0

    def __init__(self, pattern, flag='w'):
        if flag == 'r' or '+' in flag:
            raise NotImplemented('FileSequence is currently write-only')

        self.pattern = pattern
        self.flag = flag

        if flag == 'a':
            # seek to the end of the data
            # we want index to land on the last existing file
            for index in range(1, 1000):
                # e.g.: a-01.txt a-02.txt a-03.txt a-04.txt
                if not os.path.exists(self.pattern % index):
                    break
            else:
                raise Exception('Cannot write more than 1000 files')
            # e.g.: index is now = 5, so we backpedal to point at the last existing file
            self.index = index - 1

    def __enter__(self):
        self.next()
        return self

    def __exit__(self, type, value, traceback):
        self.current_file.close()

    def next(self):
        # close the current file if there is one
        if self.current_file:
            self.current_file.close()
        self.current_file = open(self.current_path, self.flag)
        self.current_bytes = self.current_file.tell()
        self.index += 1

    def write(self, line):
        if self.current_bytes + len(line) > self.limit:
            # flush current file and start new one
            self.next()

        self.current_file.write(line)
        self.current_bytes += len(line)

    @property
    def current_path(self):
        return self.pattern % self.index

    def tail(self, n=10):
        if os.path.exists(self.current_path):
            return [line for line in open(self.current_path, 'r')][-n:]
        else:
            return []


file_sequence = FileSequence('repositories-%02d.json', 'a')

# sequence.tail() may very well return an empty list
entries = [dict(id=0)] + [json.loads(line) for line in file_sequence.tail()]

# since = ['id'] if line else 0
since = entries[-1]['id']

# print since
# exit()

with file_sequence as output:
    while True:
        r = requests.get('https://api.github.com/repositories', headers=headers, params=dict(since=since))
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
