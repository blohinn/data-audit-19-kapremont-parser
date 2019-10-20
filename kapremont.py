import json
import time
from random import randint

from requests_html import HTMLSession

session = HTMLSession()
#
base_url = 'https://www.reformagkh.ru'
base_query = 'Республика Татарстан, {}'
# url = 'https://www.reformagkh.ru/search/houses?query={}'.format(query)
#
# r = session.get(url)
#
# print(r.html.find('td > a')[0].attrs['href'])

out = open("out.txt", "w+")

results = []

with open('2018.txt', 'r') as f:
    for i, line in enumerate(f.readlines()):
        print(i)
        try:
            address = line.strip()
            r = session.get(
                '{}/search/houses?query=Республика Татарстан, {}'.format(base_url, address),
            )
            url = r.html.find('td > a')[0].attrs['href']
            result = {
                'address': address,
                'url': url,
                'object_id': url.split('/')[-1],
            }
            out.write('{}|{}|{}\n'.format(address, url, url.split('/')[-1]))
            results.append(result)
        except KeyboardInterrupt:
            out.close()
            exit()
        except Exception as e:
            print(address)
            print(e)
            continue

out.close()

with open('output.txt', 'w') as out:
    out.write(json.dumps(results))
