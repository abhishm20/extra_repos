# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
from peewee import *


class Star(Model):
    actor_name = CharField()
    character_name = CharField()
    ranking = CharField()  # list ranking from imdb
    movie = ForeignKeyField(Movie, related_name='stars')


class Director(Model):
    director_name = CharField()
    ranking = CharField()  # list ranking from imdb
    movie = ForeignKeyField(Movie, related_name='stars')


class Writer(Model):
    writer_name = CharField()
    ranking = CharField()  # list ranking from imdb
    movie = ForeignKeyField(Movie, related_name='stars')


class Genre(Model):
    genre = CharField()
    movie = ForeignKeyField(Movie, related_name='stars')


class PlotKeyword(Model):
    keyword = Field()
    movie = ForeignKeyField(Movie, related_name='stars')


class Movie(Model):
    title = CharField()
    rating = CharField()
    no_of_rating = CharField()
    content_rating = CharField()
    duration = CharField()
    reviews = CharField()
    critic = CharField()
    awards_won = CharField()
    awards_nominited = CharField()
    oscar_won = CharField()
    oscar_nominated = CharField()
    story_line = TextField()
    country = CharField()
    language = CharField()
    release_date = CharField()
    budget = CharField()
    aspect_ratio = CharField()
    meta_score = CharField()
    page_url = CharField()
    is_adult = CharField()
