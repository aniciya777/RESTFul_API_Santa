from pprint import pprint

import requests

port = 8080
url = f'http://127.0.0.1:{port}'

group_1 = requests.post(url + '/group', json={
    "name": "first group",
    "description": "The best"
}).content.decode('utf-8')
group_1 = int(group_1.strip())

group_2 = requests.post(url + '/group', json={
    'name': 'second group',
}).content.decode('utf-8')
group_2 = int(group_2.strip())
print('Группы:', group_1, group_2)

print(requests.put(url + '/group/1', json={
    "name": "first group!!!",
}))
print(requests.put(url + '/group/1', json={
    "description": None,
}))

pprint(requests.get(url + '/groups').json())
print(requests.delete(url + '/group/2'))
pprint(requests.get(url + '/groups').json())

user_1 = requests.post(url + '/group/1/participant', json={
    "name": "Nastya",
    "wish": "Win olimpiada"
}).content.decode('utf-8')
user_1 = int(user_1.strip())
user_2 = requests.post(url + '/group/1/participant', json={
    "name": "Polkovnikov",
    "wish": "cursovaya"
}).content.decode('utf-8')
user_2 = int(user_2.strip())
user_3 = requests.post(url + '/group/1/participant', json={
    "name": "Sasha",
}).content.decode('utf-8')
user_3 = int(user_3.strip())
user_4 = requests.post(url + '/group/1/participant', json={
    "name": "Абыварлг",
}).content.decode('utf-8')
user_4 = int(user_4.strip())
print(user_1, user_2, user_3, user_4)

pprint(requests.get(url + '/group/1').json())
print(requests.delete(url + '/group/1/participant/4'))
pprint(requests.get(url + '/group/1').json())
