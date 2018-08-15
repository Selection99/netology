from requests import get
from pprint import pprint
from time import sleep
from json import dumps

v = 5.80
token = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'
target_id = 171691064

# token = '222670eb65a805357ee3b216972d99c8308d1ab9bc1ca0b1a082f10f3a8e5490deb013655f39f5c2962b8'
# target_id = 266645095
# target_id = 26549682


def friends():
    while True:
        response = get('https://api.vk.com/method/friends.get', params=dict(
            user_id=target_id,
            access_token=token,
            fields='id',
            v=v
            )
        )
        try:
            return [person['id'] for person in response.json()['response']['items'] if person['last_name']]
        except KeyError:
            print('', response.json()['error']['error_msg'])


def groups(user_id):
    while True:
        response = get('https://api.vk.com/method/groups.get', params=dict(
            user_id=user_id,
            access_token=token,
            fields='id',
            count=1000,
            v=v
            )
        )
        try:
            result = set(response.json()['response']['items'])
            print(' Ok')
            return result
        except KeyError:
            code_error = response.json()['error']['error_code']
            if code_error == 6:
                print('T', end='')
                sleep(0.35)
            else:
                print('', response.json()['error']['error_msg'])
                return set()


def make_set_of_groups(people_list):
    data = set()
    sleep(2)
    for i, person in enumerate(people_list):
        print(f'{len(people_list) - i}.', end='')
        data = data.union(groups(person))
        sleep(0.35)
    return groups(target_id) - data


def get_groups_by_id(set_of_groups):
    while True:
        print('Group research', end='')
        response = get('https://api.vk.com/method/groups.getById', params=dict(
            group_ids=','.join([str(group_id) for group_id in set_of_groups]),
            access_token=token,
            fields='id',
            v=v
            )
        )
        try:
            result = response.json()['response']
            print(' Ok')
            return result
        except KeyError:
            code_error = response.json()['error']['error_code']
            if code_error == 6:
                print('T', end='')
                sleep(0.35)
            else:
                print('', response.json()['error']['error_msg'])
                return list()


def get_count_of_group_members(group_id, index_to_print):
    print(f"{index_to_print}.", end='')
    while True:
        response = get('https://api.vk.com/method/groups.getMembers', params=dict(
            group_id=group_id,
            access_token=token,
            fields='id',
            count=0,
            v=v
            )
        )
        try:
            result = response.json()['response']['count']
            print(' Ok')
            return result
        except KeyError:
            code_error = response.json()['error']['error_code']
            if code_error == 6:
                print('T', end='')
                sleep(0.35)
            else:
                print('', response.json()['error']['error_msg'])
                return 0


def get_json_groups(file, group_info_list):
    data = [dict(
        name=group['name'],
        gid=group['screen_name'],
        members_count=get_count_of_group_members(group['id'], len(group_info_list)-i)
    ) for i, group in enumerate(group_info_list)]
    pprint(data)
    with open(file, mode='w', encoding='utf-8') as f:
        f.write((dumps(data, ensure_ascii=False, indent='    ')))


get_json_groups('res.txt', get_groups_by_id(make_set_of_groups(friends())))
