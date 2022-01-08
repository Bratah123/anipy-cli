import requests
import sys
import re
from bs4 import BeautifulSoup
from src import query, url, play, history
from src.colors import colors
import main
import config
from threading import Thread
import time


def episode_selection(url):
    ep_count = []
    querys = requests.get(url)
    soup = BeautifulSoup(querys.content, "html.parser")
    for link in soup.find_all('a',
                              attrs={'ep_end': re.compile("^ *\d[\d ]*$")}):
        ep_count.append(link.get('ep_end'))

    episode_urls = []

    which_episode = input(colors.END + "Episode " + colors.GREEN + "[1-" +
                          ep_count[-1] + "]" + colors.END + ": " + colors.CYAN)

    list_of_episodes = which_episode.strip().split("-")

    if len(list_of_episodes) == 2:
        try:
            first_number = int(list_of_episodes[0])
            second_number = int(list_of_episodes[1])
        except:
            print(colors.ERROR + "Invalid Input")

        if first_number in list(range(1, int(ep_count[-1]) + 1)):
            start = first_number
        else:
            print(colors.ERROR + "Your first number is invalid.")
            sys.exit()

        if second_number in list(range(start, int(ep_count[-1]) + 1)):
            end = second_number
        else:
            print(colors.ERROR + "Your second number is invalid.")
            sys.exit()

        for i in list(range(start, end + 1)):
            url_with_episode = [
                url.replace("/category", "") + "-episode-" + str(i),
                url.replace('/category', '') + '-' + str(i)
            ]

            episode_urls.append(url_with_episode)

    elif len(list_of_episodes) == 1:

        if int(which_episode) in list(range(1, int(ep_count[-1]) + 1)):
            which_episode = which_episode
            url = [
                url.replace("/category", "") + "-episode-" + which_episode,
                url.replace('/category', '') + '-' + which_episode]

            episode_urls.append(url)

        else:
            print(colors.ERROR + "Invalid input.")
            sys.exit()
    else:
        print(colors.ERROR + "Invalid input.")

    return episode_urls


def main_activity():

    print(colors.GREEN + "***Binge Mode***" + colors.END)
    search = input("Search for Anime: " + colors.CYAN)
    link = query.query(search)
    episode_urls = episode_selection(link)

    embeded_urls = []
    count = 1
    for j in episode_urls:
        if count == 1:
            first_embed_url = url.get_embed_url(j[0])
            first_video_url = url.get_video_url(first_embed_url[0], first_embed_url[1], main.args.quality)

            t1 = Thread(
                target=play.play,
                args=(
                    first_embed_url[0],
                    first_video_url,
                    first_embed_url[1],
                    None,
                ),
            )
            t1.start()
        else:
            embeded_urls.append(url.get_embed_url(j))
        count += 1

    video_urls = []
    for x in embeded_urls:
        video_urls.append(url.get_video_url(x[0], x[1], main.args.quality))

    for k, l in zip(video_urls, embeded_urls):

        while play.stop == False:
            "do nothing"
        t1 = Thread(
            target=play.play,
            args=(
                l[0],
                k,
                l[1],
                None,
            ),
        )
        t1.start()
        time.sleep(7) # guessed player is open by then
    sys.exit()
