import argparse
import configparser
import os
import random
import re
import time
from datetime import datetime

import praw
from apscheduler.schedulers.background import BackgroundScheduler
from requests import get
from slack_sdk.webhook import WebhookClient


def load_arguments():
    global args, posts_replied_to_file, logs_file
    parser = argparse.ArgumentParser(
        prog='karma_farm.py', description='A bot that farms karma on reddit')
    parser.add_argument('username', help='The username of the bot')
    parser.add_argument(
        "-s", "--sendSlackAlerts",
        help="Send slack alerts when an error occurs", action="store_true"
    )
    args = parser.parse_args()
    posts_replied_to_file = "posts_replied_to-" + str(args.username) + ".txt"
    logs_file = "logs-" + str(args.username) + ".txt"


def setup():
    global ip_address, beginning_of_message
    if not os.path.isfile(posts_replied_to_file):
        file = open(posts_replied_to_file, 'w')
        file.write('')
        file.close()
    if not os.path.isfile(logs_file):
        file = open(logs_file, 'w')
        file.write('')
        file.close()
    ip_address = get('https://ipecho.net/plain').text
    beginning_of_message = f"{ip_address} - {args.username} - "


def load_reddit_bot():
    global reddit_bot, slack_token
    config = configparser.ConfigParser()
    config.read('praw.ini')
    # reddit_bot = praw.Reddit(args.username)
    reddit_bot = praw.Reddit(
        client_id=config.get("username", "client_id"),
        client_secret=config.get("username", "client_secret"),
        password=config.get("username", "password"),
        user_agent=config.get("username", "user_agent"),
        username=config.get("username", "username"),
    )
    print("Logged in as: " + reddit_bot.user.me().name)
    print_to("Logged in as: " + reddit_bot.user.me().name)
    get_karma()


def get_karma():
    config = configparser.ConfigParser()
    config.read('praw.ini')
    karma_reddit_bot = praw.Reddit(
        client_id=config.get("username", "client_id"),
        client_secret=config.get("username", "client_secret"),
        password=config.get("username", "password"),
        user_agent=config.get("username", "user_agent"),
        username=config.get("username", "username"),
    )
    print_to("Karma: " + str(karma_reddit_bot.user.me().comment_karma + karma_reddit_bot.user.me().link_karma))


def load_scheduler():
    global sched
    sched = BackgroundScheduler()
    sched.add_job(get_karma, 'interval', hours=1)
    sched.start()


def slack_alert(message):
    if args.sendSlackAlerts:
        try:
            slack_token = open("slackWebHook.txt").read()
            client = WebhookClient(slack_token)
            response = client.send(text=message)
            assert response.status_code == 200
            assert response.body == "ok"
        except Exception as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print_to("Error sending slack alert: " + e.response["error"], slack=False, error=True)


def do_comment():
    subreddit = reddit_bot.subreddit("FreeKarma4All")
    random_posts = open("randomposts.txt").read()
    random_posts = random_posts.split('\n')
    for submission in subreddit.stream.submissions():
        done = open(posts_replied_to_file, 'r').read().split(',')
        if submission.id not in done:
            rand = random.randint(0, len(random_posts) - 1)
            random_post = random_posts[rand]
            print_to("Replying to post: " + submission.title, slack=False)
            submission.reply(random_post)
            time.sleep(80)
            with open(posts_replied_to_file, "a") as posts_replied_to:
                posts_replied_to.write(submission.id + ",")
            done = open(posts_replied_to_file, 'r').read().split(',')


def print_to(message, slack=True, error=False):
    if not error:
        message = beginning_of_message + message
    else:
        message = beginning_of_message + f"*ERROR*: {message}"
    date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    with open(logs_file, "a") as file:
        file.write(date + " - " + message + "\n")
    if slack:
        slack_alert(message)


def go():
    global is_init
    try:
        if not is_init:
            is_init = True
            load_arguments()
            setup()
            load_reddit_bot()
            load_scheduler()
            print_to("Bot started - Commenting every 80 seconds")
        do_comment()
    except KeyboardInterrupt:
        sched.shutdown()
        print_to("Stopping Bot...")
        exit(0)
    except Exception as error:
        if (re.search(r"Looks like you've been doing that a lot.", str(error))):
            breakTime = 2
            if (re.search(r"minutes", str(error))):
                breakTime += int(re.findall(r"\d+ minutes", str(error))[0].split(" ")[0])
            print_to(f"Restarting Bot in {breakTime} minutes...", slack=True)
            time.sleep(60 * breakTime)
            go()
        else:
            print_to(error, error=True)


is_init = False
go()
