#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup, element
from datetime import datetime
from datetime import timedelta
import smtplib
from time import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Header import Header


def get_web_data(date):
    # get the score data from the nba website
    res = requests.get('https://data.nba.net/prod/v2/{}/scoreboard.json'.format(date))
    json_object = json.loads(res.text)
    # print json.dumps(json_object, indent=4)
    return json_object


def team_name(team_name_abbr):
    # get the NBA team names and Abbreviations
    res = requests.get('https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations')
    bs4_html = BeautifulSoup(res.text, "html.parser")
    table = bs4_html.find('table', {'class': 'wikitable sortable'})

    team_dict = dict()
    for team in table:
        if isinstance(team, element.Tag) and team.find('a'):
            team_abbr = team.find('td').text
            team_full = team.find('a')['title']
            team_dict[team_abbr] = team_full

    return team_dict[team_name_abbr]


def insert_sting_middle(str, word):
    return str[:2] + word + str[2:]


def get_daily_score(web):
    # get the score data from the nba website
    message.append('Date: {}'.format(date))
    message.append('--------------------Schedule-------------------\n')
    # get the data of daily games
    for index, game in enumerate(web['games']):
        host = game['hTeam']
        visitor = game['vTeam']
        text = game['nugget']
        location = game['arena']
        time = game['startTimeEastern']
        message.append('{}. Scores: {}({}) - {:>3} : {}({}) - {:>3}\nLocation: {}\nTime: {}\nInfo: {}\n'\
            .format(
                index+1,
                team_name(host['triCode']),
                host['triCode'],
                host['score'],
                team_name(visitor['triCode']),
                visitor['triCode'],
                visitor['score'],
                location['name'],
                time,
                text['text']))


def next_game(team):
    # find the following game
    message.append('--------------------Preview-------------------\n')
    i = 1
    while True:
        now = datetime.now()
        # date = datetime.now()
        aDay = timedelta(days=i)
        now = now + aDay
        date = now.strftime('%Y%m%d')

        for game in get_web_data(date)['games']:
            for x in game:
                host = game['hTeam']
                visitor = game['vTeam']
                if host['triCode'] == '{}'.format(team) or visitor['triCode'] == '{}'.format(team):
                    location = game['arena']
                    time = game['startTimeEastern']
                    team_A = team_name(host['triCode'])
                    team_B = team_name(visitor['triCode'])
                    message.append('The next game for the {}({}) will be on {}\n{} vs {}\nTime: {}\nLocation: {}'\
                        .format(team_name(team),
                                team,
                                date,
                                team_name(visitor['triCode']),
                                team_name(host['triCode']),
                                time,
                                location['name']))
                    return team_A, team_B
        i += 1


def get_hist_score(team_A, team_B):

    message.append('--------------------History of Two Teams-------------------\n')

    month = ['june', 'may', 'april', 'march', 'feburary', 'january', 'december', 'november', 'october']
    year = ['2018', '2017', '2016']

    for i in xrange(len(year)):
        for j in xrange(len(month)):
            try:
                res = requests.get('https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html'.format(year[i], month[j]))
                bs4_html = BeautifulSoup(res.text, "html.parser")
                history_games = bs4_html.find_all('tr')

                for game in history_games[1:]:
                    # put data into dictioners of home and visitor
                    home = {
                        'date': game.find('th', {'data-stat': 'date_game'}).text,
                        'name': game.find('td', {'data-stat': 'home_team_name'}).text,
                        'points': game.find('td', {'data-stat': 'home_pts'}).text
                        }

                    visitor = {
                        'name': game.find('td', {'data-stat': 'visitor_team_name'}).text,
                        'points': game.find('td', {'data-stat': 'visitor_pts'}).text
                        }

                    if (
                        (team_A == home['name'] and team_B == visitor['name']) or
                        (team_B == home['name'] and team_A == visitor['name'])
                    ):
                        message.append('{} : {} ({}) vs {} ({})'.format(
                            home['date'],
                            home['name'],
                            home['points'],
                            visitor['name'],
                            visitor['points']))
            except AttributeError:
                pass


if __name__ == "__main__":
    start_time = time()
    message = []
    # date = input('Please enter the date(Ex: 20180101): \n')
    date = 20180302
    # team_abbr = raw_input("Please enter the team abbreviation(Ex: CLE): \n")
    # team = insert_sting_middle('''''', team_abbr.upper())
    team = 'CLE'

    web = get_web_data(date)  # get the data from website
    get_daily_score(web)
    # print '\n'.join(message)
    # daily_score = get_daily_score(web)  # get the daily scores
    next_game = next_game(team)
    # print next_game[0]
    # print '\n'.join(message)
    get_hist_score(next_game[0], next_game[1])
    print '\n'.join(message)

    end_time = time()
    print 'Time: {0}'.format(end_time - start_time)


    with open('nba_report.txt', 'w') as f:
        for i in message:
            f.write(i)
            f.write('\n')

    # send NBA daily report from email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("luckymanyaya@gmail.com", "a45235187")

    FROM = 'monty@python.com'
    TO = ['jon@mycompany.com']  # must be a list
    msg = MIMEMultipart('alternative')
    SUBJECT = "NBA daily report!\n"
    msg['Subject'] = Header(SUBJECT)


    # msg = """
    # From: {0}
    # To: {1}
    # Subject: {2}
    #
    # """.format(FROM, ", ".join(TO), SUBJECT)
    msg.attach(MIMEText(open('nba_report.txt', 'rb').read()))
    server.sendmail("luckymanyay@gmail.com", "tsoliangwu0130@gmail.com", msg.as_string())
    server.quit()
