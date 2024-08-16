import aiohttp

from music.genres import res_dict
from pytils import numeral


async def get_songs_list(login_name):
    async with aiohttp.ClientSession() as session:
        if not login_name.startswith('https://'):
            template_link = f'https://api.music.yandex.net/users/{login_name}/playlists/3'
            async with session.get(template_link) as response:
                data = await response.json()
        else:
            if '?' in login_name:
                login_name = login_name.split('?')[0]
            async with session.get(
                    login_name.replace("https://music.yandex.ru/users/", "https://api.music.yandex.net/users/")
            ) as response:
                data = await response.json()

        if response.status == 200:
            track_count = data['result']['trackCount']
            album_dict = dict()
            genre_dict = dict()
            artist_dict = dict()
            res = []
            for i in data['result']['tracks']:
                track = i['track']
                name, artists = track['title'], [i['name'] for i in track['artists']]
                album = track['albums'][0]
                album_title = album['title']
                genre = 'all'
                if 'genre' in album.keys():
                    genre = album['genre']

                res.append((artists, name))

                if genre in genre_dict.keys():
                    genre_dict[genre] += 1
                else:
                    genre_dict[genre] = 1

                if album_title in album_dict.keys():
                    album_dict[album_title][0] += 1
                else:
                    album_dict[album_title] = [1, artists]

                for artist in artists:
                    if artist in artist_dict.keys():
                        artist_dict[artist] += 1
                    else:
                        artist_dict[artist] = 1

            return {
                'result': res,
                'artists': artist_dict,
                'albums': album_dict,
                'genres': genre_dict,
                'track_count': track_count,
                'owner': data['result']['owner']['login']
            }


async def get_stats(artist_dict, album_dict, genre_dict, track_count, owner):
    res = f'<b>{owner}</b>, вот твоя статистика: \n\n'
    res += '<b>Топ-3 исполнителя:</b>\n'
    for index, key in enumerate(sorted(artist_dict, key=lambda s: artist_dict[s])[::-1][:3]):
        res += f'{index + 1}. {key}: {numeral.get_plural(artist_dict[key], "песня, песни, песен")}\n'
    res += '\n'
    res += '<b>Топ-3 альбома:</b>\n'
    for index, key in enumerate(sorted(album_dict, key=lambda s: album_dict[s][0])[::-1][:3]):
        res += f'{index + 1}. {", ".join(album_dict[key][1])}: "{key}"\n'
    res += '\n'
    res += '<b>Топ-3 жанра:</b>\n'
    for index, key in enumerate(sorted(genre_dict, key=lambda s: genre_dict[s])[::-1][:3]):
        res += f'{index + 1}. {res_dict[key]}: {numeral.get_plural(genre_dict[key], "песня, песни, песен")}\n'
    res += '\n'
    res += '<i>Поделись результатом с другом, чтобы узнать общее ❤️</i>'
    return res


async def get_common_stats(user_login_1, user_login_2):
    ans = ''

    text_1 = await get_songs_list(user_login_1)
    text_2 = await get_songs_list(user_login_2)

    common_tracks = [f'{", ".join(i[0])} - {i[1]}' for i in text_1['result'] if i in text_2['result']]
    res = dict()
    for i in common_tracks:
        author, song = i.split(' - ')
        if author not in res:
            res[author] = [song]
        else:
            res[author].append(song)

    v1, v2, len_res = len(text_1['result']), len(text_2['result']), len(common_tracks)
    ans += f'<b>{user_login_1}</b> и <b>{user_login_2}</b>,\n\n'
    ans += f'Ваши плейлисты похожи на <b>{len_res / (v1 + v2 - len_res) * 100:.1f} %</b>\n\n'
    ans += f'Количество общих песен: <b>{len_res}</b>\n\n'
    ans += '<b>Топ-3 общих исполнителя:</b>\n'
    for index, i in enumerate((sorted(res, key=lambda s: len(res[s]))[::-1])[:3]):
        ans += f'{index + 1}. {i}: {numeral.get_plural(len(res[i]), "песня, песни, песен")}\n'
    return ans
