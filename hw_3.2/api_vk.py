from requests import get
"""
https://oauth.vk.com/authorize?client_id=6652484&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.8
"""

token = '6111587315a08f76f5820f4084cdeb1cb97666a87e999b2800e23af16aef0151c957b11d479ac2590f075'
v = 5.80
app_id = 6652484
id_1 = 26549682
id_2 = 266645095


class VkUser:
    def __init__(self, id):
        self.id = id
        super().__init__()

    @property
    def friends(self):
        response = get('https://api.vk.com/method/friends.get', params=dict(
            user_id=self.id,
            access_token=token,
            fields='id',
            v=v
            )
        )
        return [f"{person['first_name']} {person['last_name']}" for person in response.json()['response']['items']]

    def __and__(self, other):
        friends_1, friends_2 = self.friends, other.friends
        return [i for i in friends_1 if i in friends_2]

    def __str__(self):
        return f"https://vk.com/{self.id}"


# Seva = VkUser(id_1)
# Katya = VkUser(id_2)
# print(Seva)
# print(Seva & Katya)

for i in range(10):
    response = get('https://api.vk.com/method/friends.get', params=dict(
        user_id=26549682,
        access_token=token,
        fields='id',
        v=v
    )
    )
    print(response.text)


