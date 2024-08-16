import json

with open('genres.json', encoding='utf-8') as file:
    data = file.read()

res = json.loads(data)['result']
res_dict = dict()
for i in res:
    if 'subGenres' in i.keys():
        key, value = i['id'], i['title']
        res_dict[key] = value
        for j in i['subGenres']:
            key, value = j['id'], j['title']
            res_dict[key] = value
    else:
        key, value = i['id'], i['title']
        res_dict[key] = value
