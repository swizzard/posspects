import logging
import json
import random
import time
import sys

from twython import Twython

from markov import MarkovNameGenerator


logging.basicConfig(filename='posspects.log')


class Posspects():
    def __init__(self, cfg_path, players_path, depth):
        with open(cfg_path) as f:
            cfg = json.load(f)
        self.client = Twython(app_key=cfg['consumer_key'],
                              app_secret=cfg['consumer_secret'],
                              oauth_token=cfg['token'],
                              oauth_token_secret=cfg['secret'])
        mng = MarkovNameGenerator(players_path, depth)
        self.names = mng.make_names()
        self.hands = ['Left-handed', 'Right-handed']
        self.pitchers = ['Starter', 'Reliever', 'Closer']
        self.positions = ['First Baseman', 'Second Baseman', 'Third Baseman',
                          'Shortstop', 'Left Fielder', 'Center Fielder',
                          'Right Fielder', 'Catcher']

    def make_text(self, name):
        if random.random() > 0.8:
            return self.pitcher(name)
        else:
            return self.position_player(name)

    def pitcher(self, name):
        return '{} {} {}'.format(random.choice(self.hands),
                                 random.choice(self.pitchers),
                                 name)

    def position_player(self, name):
        return '{} {}'.format(random.choice(self.positions),
                              name)

    def tweet(self):
        for name in self.names:
            text = self.make_text(name)
            if len(text) < 140:
                self.client.update_status(status=text)
                time.sleep(1800)
            else:
                continue


if __name__ == '__main__':
    cfg_path, players_path, depth = sys.argv[1:]
    posspects = Posspects(cfg_path, players_path, int(depth))
    posspects.tweet()

