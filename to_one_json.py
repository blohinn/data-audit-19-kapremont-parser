import json

result = []
with open('concat.txt', 'r') as f:
    for line in f.readlines()[:100]:
        result.append(json.loads(line))

with open('vseee_srez.json', 'w+') as vse:
    vse.write(json.dumps(result))
