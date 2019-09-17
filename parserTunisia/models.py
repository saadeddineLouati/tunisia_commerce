from mongoengine import *



class Product(DynamicDocument):
    meta = {'collection':'Product','strict': False}


class Hotel(DynamicDocument):
    meta = {'collection':'Hotel','strict': False}


class Restaurant(DynamicDocument):
    meta = {'collection':'Restaurant','strict': False}


class Activity(DynamicDocument):
    meta = {'collection':'Activity','strict': False}

class VolOneWay(DynamicDocument):
    meta = {'collection':'VolOneWay','strict': False}

class VolRoundTrip(DynamicDocument):
    meta = {'collection':'VolRoundTrip','strict': False}


class Bien(DynamicDocument):
    meta = {'collection':'Bien','strict': False}
