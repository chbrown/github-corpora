import sys

# 1e8 = 100MB
# 5e7 = %)MB
limit = 5e7

index = 0
current_bytes = 0


def next(old=None):
    global current_bytes, index
    current_bytes = 0
    if old:
        old.close()
    index += 1
    return open('respositories-%02d.json' % index, 'w')

current = next()

for line in sys.stdin:
    if current_bytes + len(line) > limit:
        # flush current file and start new one
        current = next(current)

    current.write(line)
    current_bytes += len(line)

current.close()
