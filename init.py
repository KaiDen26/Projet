# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 20:08:47 2022

@author: Thomas NICOLAS
"""

from Sibra import *
from data2py import *
from data22 import *
from datetime import date

date_jour = datetime.today().strftime("%d/%m/%Y")

ligne1_PDG = Ligne("Ligne 1 Direction PARC_DES_GLAISINS", "PARC_DES_GLAISINS")
ligne2_CAMPUS = Ligne("Ligne 2 Direction CAMPUS", "CAMPUS")
ligne1_Lycee = Ligne("Ligne 1 Direction Lycée de Poisy", "LYCÃ‰E_DE_POISY")
ligne2_PP = Ligne("Ligne 2 Direction Piscine-patinoire", "PISCINE-PATINOIRE")
ligne1_PDG_V = Ligne("Ligne 1 Direction PARC_DES_GLAISINS", "PARC_DES_GLAISINS")
ligne2_CAMPUS_V = Ligne("Ligne 2 Direction CAMPUS", "CAMPUS")
ligne1_Lycee_V = Ligne("Ligne 1 Direction Lycée de Poisy", "LYCÃ‰E_DE_POISY")
ligne2_PP_V = Ligne("Ligne 2 Direction Piscine-patinoire", "PISCINE-PATINOIRE")


liste_lignes_cours = [ligne1_PDG, ligne1_Lycee, ligne2_CAMPUS, ligne2_PP]
liste_lignes_vac = [ligne1_PDG_V, ligne1_Lycee_V, ligne2_CAMPUS_V, ligne2_PP_V]

liste_vacation = { 1023: 1108, 1218: 1231, 101: 103, 212: 228, 416: 502, 526: 530, 707: 901, 1225: 1225, 101: 101, 418: 418, 501: 501, 508: 508, 606: 606, 1101: 1101, 1111: 1111 }


def isInVacation(day):
    d = datetime.strptime(day, "%d/%m/%Y")
    dd = d.strftime('%m%d')

    for day in liste_vacation.keys():
        if (int(dd) >= int(day)) & (int(dd) <= liste_vacation.get(day)):
            return True

    if isSunday(date(d.year, d.month, d.day)) :
        return True 

    return False

def isSunday(d = datetime.today()):
  return d.weekday() == 6


def initArret(ligne, date):
    
    liste_arret = getListOfStop(date)
    
    for idx, arret in enumerate(liste_arret): 
        
        infos = {}
        
        if arret in dict_arret:
            a = dict_arret[arret]
            
            infos = a.infos
        
        if (idx + 1) >= len(liste_arret):
            infos[ligne] = ["Terminus", getListOfHours(date, arret)]
        else:
            infos[ligne] = [liste_arret[idx + 1], getListOfHours(date, arret)]
        
        currentArret = Arret(arret, infos)
        dict_arret[arret] = currentArret

        if idx == 0:
            ligne.setDepart(currentArret)

def init():
    initArret(ligne1_PDG, regular_date_go)
    initArret(ligne2_CAMPUS, regular_date_go2)
    initArret(ligne1_Lycee, regular_date_back)
    initArret(ligne2_PP, regular_date_back2) 
    initArret(ligne1_PDG_V, regular_date_go)
    initArret(ligne2_CAMPUS_V, regular_date_go2)
    initArret(ligne1_Lycee_V, regular_date_back)
    initArret(ligne2_PP_V, regular_date_back2) 

def hasToChangeLine(arret1, arret2, function, time=getCurrentTime()):
        
        arret1_ligne = None
        arret2_ligne = None
        
        commun = None
        
        if isInVacation(date_jour):
            liste_lignes = liste_lignes_vac
        else:
            liste_lignes = liste_lignes_cours

        liste = [ligne1_PDG, ligne2_CAMPUS]
        
        for ligne in liste:
            
            index = liste.index(ligne)
            
            if index < (len(liste)  - 1):
                ligne_suivante = liste[index + 1]
                
                if commun == None:
                    commun = ligne.hasCommonStop(ligne_suivante)
            
        if function == "shortest":
            commun = dict_arret["VIGNIÃˆRES"]

        for ligne in liste_lignes:
           
           
            if arret1.containsLigne(ligne):
                d = getClosestTime(arret1, ligne, to_timestamp(time))
                
                index = arret1.HoraireFromLigne(ligne).index(d)
                a = commun.HoraireFromLigne(ligne)[index]
                
                if to_timestamp(d) < to_timestamp(a):
                    arret1_ligne = ligne
                
            elif arret2.containsLigne(ligne):
                d = getClosestTime(arret2, ligne, to_timestamp(time))
                
                index = arret2.HoraireFromLigne(ligne).index(d)
                a = commun.HoraireFromLigne(ligne)[index]
                
                if to_timestamp(d) > to_timestamp(a):
                    arret2_ligne = ligne
            else:
                print("Cet arrêt n'est pas répertorié pour les lignes disponibles.")
                return;
        
            
        meilleure_horaire_depart = getClosestTime(arret1, arret1_ligne, to_timestamp(time))
        index = arret1.HoraireFromLigne(arret1_ligne).index(meilleure_horaire_depart)
        
        arret_commun = arret1_ligne.hasCommonStop(arret2_ligne)
        
        arret_commun_horaire1 = arret_commun.HoraireFromLigne(arret1_ligne)[index]
        
        arret_commun_horaire2 = getClosestTime(arret_commun, arret2_ligne, to_timestamp(arret_commun_horaire1))
        index2 = arret_commun.HoraireFromLigne(arret2_ligne).index(arret_commun_horaire2)
        
        meilleure_horaire_arrivee = arret2.HoraireFromLigne(arret2_ligne)[index2]

        while meilleure_horaire_arrivee == "-":
            index2 +=1;
            meilleure_horaire_arrivee = arret2.HoraireFromLigne(arret2_ligne)[index2]
            
        
        if function == "foremost":  
            print("\n---------------------------- Foremost Function -------------------------------\n")    
            afficherHoraire(arret1_ligne.nom, arret1.nom, meilleure_horaire_depart, arret_commun.nom, arret_commun_horaire1)
            afficherHoraire(arret2_ligne.nom, arret_commun.nom, arret_commun_horaire2, arret2.nom, meilleure_horaire_arrivee)
            
        if function == "fastest":
                       
            temps1 = arret1_ligne.getTimeBetween(arret1, commun, time)
            temps2 = arret2_ligne.getTimeBetween(commun, arret2, time)
            
            print("\n---------------------------- Fastest Function -------------------------------\n")
            afficherTempsTrajet(arret1_ligne.nom, arret1.nom, commun.nom, temps1)
            afficherTempsTrajet(arret2_ligne.nom, commun.nom, arret2.nom, temps2)
        
        if function == "shortest":
            
            nb1 = arret1_ligne.getArretBetween(arret1, commun, time)
            nb2 = arret2_ligne.getArretBetween(commun, arret2, time)

            afficherNombreArret(arret1.nom, arret2.nom, nb1 + nb2)

            
            

def afficherHoraire(ligne, arret1, horaire1, arret2, horaire2): 
    print("{} : {} [{}] -> {} [{}]".format(ligne, arret1, horaire1, arret2, horaire2))

def afficherNombreArret(arret1, arret2, nb):
    print("\n---------------------------- Shortest Function -------------------------------\n")  
    print("Le nombre d'arrêts entre {} et {} est : {}".format(arret1, arret2, nb))

def afficherTempsTrajet(ligne, arret1, arret2, temps):
    print("{} : {} -> {} = {} minutes.".format(ligne, arret1, arret2, temps))
      
def shortest(arret1, arret2, time=getCurrentTime()):
    
    result = 100000
    ligne_result = ""
    
    nb_ligne = 0
    
    for ligne in [ligne1_PDG, ligne2_CAMPUS]:
        
        if (arret1.containsLigne(ligne) == True) & (arret2.containsLigne(ligne) == True):
        
            nb_ligne += 1
            
            nb = ligne.getArretBetween(arret1, arret2, time)
           
            print(nb)
            
            if nb < result:
                result = nb
                ligne_result = ligne.nom 
                
    if nb_ligne == 0:
        hasToChangeLine(arret1, arret2, "shortest", time)
    else:                       
        afficherNombreArret(arret1.nom, arret2.nom, result)

def fastest(arret1, arret2, time=getCurrentTime()):
         
    
     result = 100000
     ligne_result = ""
     
     nb_ligne = 0
     
     for ligne in [ligne1_PDG, ligne2_CAMPUS]:
         
         if (arret1.containsLigne(ligne) == True) & (arret2.containsLigne(ligne) == True):
         
             nb_ligne += 1
             
             nb = ligne.getTimeBetween(arret1, arret2, time)
            

             if int(nb) < result:
                 result = int(nb)
                 
                 ligne_result = ligne.nom 
     
     if nb_ligne == 0:
         hasToChangeLine(arret1, arret2, "fastest", time)
     else:    
         afficherTempsTrajet(ligne_result, arret1.nom, arret2.nom, result)
   

def foremost(arret1, arret2, time=getCurrentTime()):
    
    ligne_result = ""
    
    meilleure_horaire_depart = None
    meilleure_horaire_arrivee = None 
    
    nb_ligne = 0
    
    if isInVacation(date_jour):
            liste_lignes = liste_lignes_vac
    else:
            liste_lignes = liste_lignes_cours

    for ligne in liste_lignes:
         
         if (arret1.containsLigne(ligne) == True) & (arret2.containsLigne(ligne) == True):
             
             if ligne.isFirst(arret1, arret2):
        
                nb_ligne += 1
                
                horaire_depart = getClosestTime(arret1, ligne, to_timestamp(time))         
        
                index = arret1.HoraireFromLigne(ligne).index(horaire_depart)
                
                horaire_arrivee = arret2.HoraireFromLigne(ligne)[index]
                
                while horaire_arrivee == "-":
                    index += 1;
                    horaire_arrivee = arret2.HoraireFromLigne(ligne)[index]
                
                
                if (to_timestamp(horaire_arrivee) - to_timestamp(horaire_depart)) > 0:
                    
                    if (meilleure_horaire_arrivee == None):
                        meilleure_horaire_arrivee = horaire_arrivee
                        meilleure_horaire_depart = horaire_depart
                        ligne_result = ligne.nom
                    else:
                        if to_timestamp(horaire_arrivee) < to_timestamp(meilleure_horaire_arrivee):
                            meilleure_horaire_arrivee = horaire_arrivee
                            meilleure_horaire_depart = horaire_depart
                            ligne_result = ligne.nom
     
    if nb_ligne == 0:
        hasToChangeLine(arret1, arret2, "foremost", time)
    else:   
        print("\n---------------------------- Foremost Function -------------------------------\n")  
        afficherHoraire(ligne_result, arret1.nom, meilleure_horaire_depart, arret2.nom, meilleure_horaire_arrivee)
                    


