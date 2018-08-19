from requests import get
from pprint import pprint
from time import sleep
from json import dumps
# from logging import info, basicConfig, INFO
# basicConfig(level=INFO)
SLEEP_TIME = 0.8
# token = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'
# target_id = 171691064

token = '19d7aea6bb8cdd5c50bd35a1c7588d3db11adf1135f80cd218e9a103d518ce9337ea9bf438e82047e1a28'
target_id = 266645095
# target_id = 26549682


class VkApi:
    default_params = dict(
        access_token=token,
        v=5.80
    )
    methods = []

    def __getattr__(self, item):
        self.methods.append(item)
        return self

    def __call__(self, **kwargs):
        request = get(f'https://api.vk.com/method/{".".join(self.methods)}', params=dict(
            **self.default_params,
            **kwargs
            )
        )
        self.methods = []
        return request


API = VkApi()


def ask_till_answer(default_answer, max_tries=10):
    def decorator(func):
        def wrapped(*args, **kwargs):
            for i in range(max_tries):
                try:
                    result = func(*args, **kwargs)
                    print(' Ok')
                    return result
                except KeyError:
                    code_error = response.json()['error']['error_code']
                    if code_error == 6 or code_error == 10:  # Превышение запросов к API или внутренняя ошибка сервера
                        print('T', end='')
                        sleep(SLEEP_TIME)
                    else:
                        print('', response.json()['error']['error_msg'])
                        print(response.text)
                        return default_answer
            raise RuntimeError("\nПревышено количество запросов")
        return wrapped
    return decorator


@ask_till_answer(list())
def friends():
    print('Получение списка друзей цели:', end='')
    global response
    response = API.friends.get(
        user_id=target_id,
        fields='id'
    )
    return [person['id'] for person in response.json()['response']['items'] if person['last_name']]


@ask_till_answer(set())
def groups(user_id):
    global response
    response = API.groups.get(
        user_id=user_id,
        count=1000,
    )
    return set(response.json()['response']['items'])


def make_set_of_groups(people_list):
    data = set()
    for i, person in enumerate(people_list):
        print(f'{len(people_list) - i}.', end='')
        data = data.union(groups(person))
        # sleep(SLEEP_TIME)
    return groups(target_id) - data


@ask_till_answer(list())
def get_groups_by_id(set_of_groups):
    print('Group research', end='')
    global response
    response = API.groups.getById(
        group_ids=','.join([str(group_id) for group_id in set_of_groups]),
    )
    return response.json()['response']


@ask_till_answer(0)
def get_count_of_group_members(group_id):
    global response
    response = API.groups.getMembers(
        group_id=group_id,
        count=0
    )
    return response.json()['response']['count']


def get_json_groups(file, group_print_list):
    data = []
    print("Сбор информации о найденных группах:")
    for i, group in enumerate(group_print_list):
        print(f"{len(group_print_list)-i}.", end='')
        data.append(dict(
                name=group['name'],
                gid=group['screen_name'],
                members_count=get_count_of_group_members(group['id'])
            )
        )
    pprint(data)
    with open(file, mode='w', encoding='utf-8') as f:
        f.write((dumps(data, ensure_ascii=False, indent='    ')))


try:
    get_json_groups('res.txt', get_groups_by_id(make_set_of_groups(friends())))
except RuntimeError as err:
    print(*err.args)
