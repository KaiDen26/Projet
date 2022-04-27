# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:45:27 2022

@author: Thomas NICOLAS
"""

from re import A
from init import *

dictionnaire_arrets = {}

def addToDict():

    id = 1

    for stop in dict_arret.values():

        dictionnaire_arrets[stop] = id
        id += 1

def showStops():

    for stop in dictionnaire_arrets.keys():

        print("{} : {}".format(stop.nom, dictionnaire_arrets.get(stop)))

def getStopFromNumber(number):

    for stop in dictionnaire_arrets.keys():

        if dictionnaire_arrets.get(stop) == number:
            return stop
    return None

if __name__ == '__main__':

    init()

    addToDict()

    print("Voici la liste des arrêts : ")

    showStops()

    print('Choisissez un arrêt de départ : ')
    arret1 = input()

    print('Choisissez un arrêt d\'arrivée : ')
    arret2 = input()

    shortest(getStopFromNumber(int(arret1)), getStopFromNumber(int(arret2)), "8:10")
    fastest(getStopFromNumber(int(arret1)), getStopFromNumber(int(arret2)), "8:10")
    foremost(getStopFromNumber(int(arret1)), getStopFromNumber(int(arret2)), "8:10")