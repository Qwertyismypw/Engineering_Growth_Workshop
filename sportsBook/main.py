# This is a sample Python script.

from bs4 import BeautifulSoup
import urllib.request
import re
from selenium import webdriver
import time
import sys

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

fanduel_url = 'https://pa.sportsbook.fanduel.com/navigation/nfl'
foxbetSB_url = 'https://mtairycasino.foxbet.com/#/american_football/competitions/8706524'
riversSB_url = 'https://pa.betrivers.com/?page=sportsbook&l=RiversPittsburgh&group=1000093656&type=prematch#home'

def fanduelSB(url):
    following_week = 'NFL Week 4'

    driver = webdriver.Chrome(executable_path=r'C:\Users\Josh\Downloads\chromedriver_win32\chromedriver.exe')

    try:
        driver.get(url)
        page = driver.page_source
        #page = urllib.request.urlopen(url)
    except:
        return('An error occured.')

    soup = BeautifulSoup(page, features="html.parser")
    #print(soup.prettify())

    odds = soup.find_all('span')
    textOdds = []
    first_index = 999
    for pos, i in enumerate(odds):
        odd2txt = str(i)

        #print (odd2txt, type(odd2txt))
        bet = odd2txt.split('>')[1].split('<')[0]
        textOdds.append(bet)
        #print (bet)
        if bet == following_week:
            last_index = pos
        if bet == 'Total':
            if pos < first_index:
                first_index = pos


    textOdds = textOdds[first_index:last_index]

    all_teams = []
    teams = []
    bettingOdds = []
    for j in textOdds:
        if j != 'More wagers' and not j.startswith('O ') and not j.startswith('U '):
            #print (j)
            try:
                if int(j) >= 100 or int(j) <= -100:
                    bettingOdd = int(j)
                    #print (bettingOdd)
                    bettingOdds.append(bettingOdd)
            except:
                try:
                    if j.split(' ')[0].isupper():
                        team = j
                        #print (team)
                        teams.append(team)
                except:
                    pass

    team_matches = list(chunks(teams, 2))
    match_odds = list(chunks(list(chunks(bettingOdds, 3)), 2))

    #print (match_odds)

    header = ['Spread', 'Moneyline', 'Total']
    for pos, i in enumerate(match_odds):
        yield (team_matches[pos], i)

def foxbetSB(url):
    following_week = 'NFL Week 4'

    driver = webdriver.Chrome(executable_path=r'C:\Users\Josh\Downloads\chromedriver_win32\chromedriver.exe')

    try:
        driver.get(url)
        page = driver.page_source
        #page = urllib.request.urlopen(url)
    except:
        return('An error occured.')

    time.sleep(3)

    soup = BeautifulSoup(page, features="html.parser")
    #print (soup.prettify())

    regex_odds = re.compile('button__bet__odds selectionOdds-event')
    odds = soup.find_all('em', attrs={'class': regex_odds})
    #print (odds)

    regex_teams = re.compile('formattedEventTitle')
    team_names = soup.find_all('em', attrs={'class': regex_teams})
    #print(team_names)

    team_name_list = []
    for i in team_names:
        team_name_list.extend(i.getText().replace("\n", "").replace("\t", "").strip().split(' @ '))
    #print (team_name_list)

    odds_list = []
    for i in odds:
        odds_list.append(i.getText().replace("\n", "").replace("\t", "").strip())
    #print(odds_list)

    match_odds = list(chunks(list(chunks(odds_list, 3)), 2))
    team_matches = list(chunks(team_name_list, 2))

    match_odds_reversed = []
    for i in match_odds:
        #print (i, type(i), i[::-1])
        match_odds_reversed.append(i[::-1])

    #print(team_matches_reversed)
    #print(match_odds)

    for pos, i in enumerate(match_odds_reversed):
        yield (team_matches[pos], i)

def riversSB(url):
    following_week = 'NFL Week 4'

    driver = webdriver.Chrome(executable_path=r'C:\Users\Josh\Downloads\chromedriver_win32\chromedriver.exe')

    try:
        driver.get(url)
        page = driver.page_source
        # page = urllib.request.urlopen(url)
    except:
        return ('An error occured.')

    time.sleep(5)

    soup = BeautifulSoup(page, features="html.parser")
    print (soup.prettify())

    regex_teams = re.compile('participant-name')
    team_names = soup.find_all('span', attrs={'class': regex_teams})

    regex_odds = re.compile('outcome-value')
    odds = soup.find_all('li', attrs={'class': regex_odds})

    #print (odds)
    print(team_names)

    team_name_list = []
    for i in team_names:
        team_name_list.extend(i.getText().replace("\n", "").strip())
    print (team_name_list)

    odds_list = []
    for i in odds:
        odds_list.append(i.getText().replace("\n", "").replace("\t", "").strip())
    print(odds_list)


"""
for i in fanduelSB(fanduel_url):
    print (i)

for i in foxbetSB(foxbetSB_url):
    print (i)

#riversSB(riversSB_url) #this still needs work
"""
#<span class="he hf db ct ho hp ed"> - spread
#<span class="he hf db ct ho hp ed"> - money line
#<span class="he hf db ct ho hp ed"> - over/under
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
