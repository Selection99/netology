from requests import get
from pprint import pprint
from time import sleep
from json import dumps
# from logging import info, basicConfig, INFO
# basicConfig(level=INFO)
SLEEP_TIME = 0.8
# token = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'
# target_id = 171691064

token = '6111587315a08f76f5820f4084cdeb1cb97666a87e999b2800e23af16aef0151c957b11d479ac2590f075'
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


def ask_till_answer(default_answer, max_tries=6, start_msg=''):
    def decorator(func):
        def wrapped(*args, **kwargs):
            if start_msg:
                print(start_msg, end='')
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
                        return default_answer
            raise RuntimeError("\nПревышено количество запросов")
        return wrapped
    return decorator


@ask_till_answer(list(), start_msg='Получение списка друзей цели')
def friends():
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
    print('Получение списка групп цели', end='')
    target_groups = groups(target_id)
    if people_list:
        print('Получение списка групп каждого друга:')
        for i, person in enumerate(people_list):
            print(f'  {len(people_list) - i}.', end='')
            data = data.union(groups(person))
    return target_groups - data


@ask_till_answer(0)
def get_count_of_group_members(group_id):
    global response
    response = API.groups.getMembers(
        group_id=group_id,
        count=0
    )
    return response.json()['response']['count']


def get_json_groups(file, set_of_groups):
    @ask_till_answer(list())
    def get_groups_by_id():
        global response
        response = API.groups.getById(
            group_ids=','.join([str(group_id) for group_id in set_of_groups]),
        )
        return response.json()['response']

    data = []
    if set_of_groups:
        print("Сбор информации о найденных группах:")
        print(' Получение глобальной информации о группах', end='')
        group_print_list = get_groups_by_id()
        print(" Получение подробной информации о каждой группе:")
        for i, group in enumerate(group_print_list):
            print(f"  {len(group_print_list)-i}.", end='')
            data.append(dict(
                    name=group['name'],
                    gid=group['screen_name'],
                    members_count=get_count_of_group_members(group['id'])
                )
            )
        print('Результат:')
        pprint(data)
    else:
        print('Список групп пуст.')
    with open(file, mode='w', encoding='utf-8') as f:
        f.write((dumps(data, ensure_ascii=False, indent='    ')))


try:
    get_json_groups('res.txt', make_set_of_groups(friends()))
except RuntimeError as err:
    print(*err.args)
