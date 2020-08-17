import requests

URL = "https://api.vk.com/method/groups.getMembers?group_id=rambler&v=5.122&offset=100&count=10&access_token=d470286e91947afdc1208b5a540543fae4c2e1a784464993bb643ba74a95ac5a51788168454246d8e28ec"
response = requests.get(URL)

print(response.json()['response']['count'])