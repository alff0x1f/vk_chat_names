# -*- coding: utf-8 -*-
try:
    import ujson as json
except ImportError:
    import json

import vk_api

from config import vk_password, vk_username

vk_session = None


def get_chat_names():
    vk_session = vk_api.VkApi(vk_username, vk_password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    count = 10
    offset = 0
    convers = []

    while offset < count:
        conversations = vk.messages.getConversations(offset=offset, count=200)
        count = conversations['count']

        for conv in conversations['items']:
            if conv['conversation']['peer']['type'] == 'chat':
                c = {}
                c['local_id'] = conv['conversation']['peer']['local_id']
                if 'photo' in conv['conversation']['chat_settings']:
                    c['photo'] = conv['conversation']['chat_settings']['photo']
                c['members_count'] = conv['conversation']['chat_settings']['members_count']
                c['title'] = conv['conversation']['chat_settings']['title']
                convers.append(c)
        offset += 200

    with open("conversations.json", "w") as write_file:
        json.dump(convers, write_file, sort_keys=True, indent=4,
                  ensure_ascii=False)


if __name__ == '__main__':
    get_chat_names()
