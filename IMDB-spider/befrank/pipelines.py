# -*- coding: utf-8 -*-
import six
from playhouse.sqlite_ext import SqliteExtDatabase
from items import *


class BefrankPipeline(object):
    def __init__(self):
        self.db = None
        self.setup_db_connection()
        self.create_tables()

    def setup_db_connection(self):
        self.db = SqliteExtDatabase('movies.db')
        self.db.connect()

    def create_tables(self):
        return self.db.create_tables[Movie, Star, Writer, Director, Genre, PlotKeyword]

    def close_db(self):
        self.db.close()

    def process_item(self, item, spider):
        for key, value in six.iteritems(item):
            if key == "CastMembers":
                continue

            if isinstance(value, list):
                if value:
                    templist = []
                    for obj in value:
                        temp = self.stripHTML(obj)
                        templist.append(temp)
                    item[key] = templist
                else:
                    item[key] = ""
            elif key is not 'MainPageUrl':
                item[key] = self.stripHTML(value)
            else:
                item[key] = value

        self.store_in_db(item)
        return item

    def store_in_db(self, item):
        self.storeFilmInfoInDb(item)
        film_id = self.cursor.lastrowid

        for cast in item['CastMembers']:
            self.storeActorInfoInDb(cast, film_id)

    def storeFilmInfoInDb(self, item):
        self.cur.execute("INSERT INTO Films(\
			title, \
			rating, \
			ranking, \
			release_date, \
			page_url, \
			director, \
			writers, \
			runtime, \
			sinopsis, \
			genres, \
			mpaa_rating, \
			budget, \
			language, \
			country, \
			gross_profit, \
			opening_weekend_profit, \
			aspect_ratio, \
			sound_mix, \
			color\
			) \
		VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", \
                         ( \
                             item.get('Title', ''),
                             float(item.get('Rating', 0.0)),
                             int(item.get('Ranking', 0)),
                             item.get('ReleaseDate', ''),
                             item.get('MainPageUrl', ''),
                             ', '.join(item.get('Director', '')),
                             ', '.join(item.get('Writers', '')),
                             item.get('Runtime', ''),
                             item.get('Sinopsis', '').strip(),
                             ', '.join(item.get('Genres', '')),
                             item.get('MpaaRating', ''),
                             self.cleanMoney(item.get('Budget', '')),
                             item.get('Language', ''),
                             item.get('Country', ''),
                             self.cleanMoney(item.get('GrossProfit', '')),
                             self.cleanMoney(item.get('OpeningWeekendProfit', '')),
                             item.get('AspectRatio', '').strip(),
                             ', '.join(item.get('SoundMix', '')),
                             item.get('Color', '')
                         ))
        self.con.commit()

    def storeActorInfoInDb(self, item, film_id):
        self.cur.execute("INSERT INTO Actors(\
			film_id, \
			actor_name, \
			charecter_name, \
			ranking \
			) \
		VALUES(?,?,?,?)",
                         (
                             film_id,
                             self.stripHTML(item.get('ActorName', '')).strip(),
                             self.stripHTML(item.get('CharacterName', '')).strip(),
                             item.get('Ranking', 0)
                         ))
        self.con.commit()

    def stripHTML(self, string):
        tagStripper = MLStripper()
        tagStripper.feed(string)
        return tagStripper.get_data()

    def cleanMoney(self, string):
        # you could add more simpbles to this, but it gets kinda complex with some of the symbles being unicode, so I skpped that for now.
        currencySymbles = "$"
        cleanMoneyString = ""
        stopAdding = False
        for index, char in enumerate(list(string)):
            if char in currencySymbles and not stopAdding:
                cleanMoneyString += char
            elif char == "," and not stopAdding:
                cleanMoneyString += char
            elif char.isdigit() and not stopAdding:
                cleanMoneyString += char
            elif char in ' ':
                # we know that numbers do not have spaces in them, so we can assume that once the number
                # has started there will be no spaces
                if len(cleanMoneyString) > 0:
                    stopAdding = True

        return cleanMoneyString


from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super(self).__init__()
        self.reset()
        self.fed = []

        def handle_data(self, d):
            self.fed.append(d)

        def get_data(self):
            return ''.join(self.fed)
