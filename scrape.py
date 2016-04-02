from functools import reduce
from operator import add
import sys

from bs4 import BeautifulSoup as BS
import requests


class PlayerScraper():
    teams = ('bal', 'bos', 'nyy', 'tam', 'tor', 'atl', 'mia', 'nym', 'phi',
             'was', 'chw', 'cle', 'det', 'kan', 'min', 'chc', 'cin', 'mil',
             'pit', 'stl', 'hou', 'laa', 'oak', 'sea', 'tex', 'ari', 'col',
             'lad', 'sdg', 'sfo')
    root = 'http://espn.go.com/mlb/teams/roster'

    def __init__(self):
        pass

    def get_roster(self, team):
        roster = []
        req = requests.get(self.root, params={'team': team})
        if req.ok:
            soup = BS(req.content, 'html.parser')
            trs = soup.find_all('tr')
            for tr in trs:
                if any([classname.startswith('player') for classname in
                        tr.attrs['class']]) and tr.a:
                    roster.append(self.process_player(tr.a.text))
        return roster

    def process_player(self, player_str):
        names = player_str.upper().rsplit(' ', 1)
        if names[1] == 'JR.':
            name = names[0].split(' ')
            fname = name[0]
            lname = name[1] + ' ' + names[1][:-1]
            names = [fname, lname]
        return '\t'.join(names)

    def run(self, outfile):
        players = reduce(add, [self.get_roster(team) for team in self.teams], [])
        with open(outfile, 'w') as f:
            f.write('\n'.join(players))


if __name__ == '__main__':
    scraper = PlayerScraper()
    scraper.run(sys.argv[1])

