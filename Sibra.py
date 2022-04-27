# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 21:58:06 2022

@author: Thomas NICOLAS
"""

from datetime import datetime, timezone

dict_arret = {}

class Arret :
    
    def __init__(self, nom, informations):        
        
        self.nom = nom
        self.infos = informations
        
        # infos : '1 : ["nomArretSuivant", "listehoraire"]'


    def nom(self):
        return self.nom
    
    def infos(self):
        return self.infos
    
    def containsLigne(self, ligne):
        
        if ligne in self.infos:
            return True
        return False
        
    
    def HoraireFromLigne(self, ligne):
        if ligne in self.infos:
            return self.infos[ligne][1]
        else:
            print("Erreur, ligne inconnue pour cet arrêt.")
            
    def nextStop(self, ligne):
        if ligne in self.infos:
            
            next_stop_name = self.infos[ligne][0]
            
            if not self.infos[ligne][0] == "Terminus":
                return dict_arret[next_stop_name]

            
        else:
            print("Erreur, ligne inconnue pour cet arrêt.")
                
class Ligne :
    
   def __init__(self, nom, sens):
       
       self.nom = nom
       self.sens = sens
        
   def sens(self):
       return self.sens
   
   def nom(self):
       return self.nom
    
   def setDepart(self, arret):
       self.depart = arret
       self.arret = arret
   
   def isFirst(self, arret1, arret2, compteur=0):
      
       if self.arret.nextStop(self) != None:
            
            if self.arret.nom == arret1.nom:
                compteur += 1
            
            if self.arret.nextStop(self) == arret2:
                if compteur == 1:
                    compteur += 1
                    
            if compteur == 2:
                return True      
            
            self.arret = self.arret.nextStop(self)
            
            return self.isFirst(arret1, arret2, compteur)
            
       else:
            return False
           
   
   def showTrajet(self):
       print(self.arret.nom)  
       
       if self.arret.nextStop(self) != None:
           self.arret = self.arret.nextStop(self)
           self.showTrajet()
       else:
           self.arret = self.depart

   def setToTerminus(self):
       if self.arret.nextStop(self) != None:
           self.arret = self.arret.nextStop(self)
           self.setToTerminus()
       else:
           self.arret = self.depart
       
   def showTerminus(self):
       self.setToTerminus()
       print(self.arret.nom)
       self.arret = self.depart
       
   def getListeOfStop(self, liste=[]):
       
       if self.arret.nextStop(self) != None:
          self.arret = self.arret.nextStop(self)
          self.getListeOfStop(liste)
       else:
          self.arret = self.depart
          return liste
   
   def hasCommonStop(self, other_ligne):    
       
        if self.arret.nextStop(self) != None:
            
            if other_ligne.arret != None: 
                 
                 if other_ligne.arret == self.arret :
                     return self.arret
                 
                 other_ligne.arret = other_ligne.arret.nextStop(other_ligne)
                 return self.hasCommonStop(other_ligne)
            else:
                 other_ligne.arret = other_ligne.depart
                 self.arret = self.arret.nextStop(self)  
                 return self.hasCommonStop(other_ligne)
                 
        else:
          self.arret = self.depart
          return False
       
   def getArretBetween(self, arret1, arret2, time):
       
       compteur = 0
       start_cpt = False
           
       self.arret = self.depart
            
       if arret1.containsLigne(self) & arret2.containsLigne(self):
           
           while self.arret.nextStop(self) != None:
                              
                if self.arret.nom == arret1.nom:
                    start_cpt = True
                    
                 
                if self.arret.nextStop(self).nom == arret2.nom:
                    self.arret = self.depart
                    compteur += 1
                    return compteur
                    break
                
                self.arret = self.arret.nextStop(self)
                
                if start_cpt:             
                    compteur += 1
            
           
       else:
           
           print("Erreur, ligne(s) inconnue(s) pour cet arrêt.")
           
   
   def getTimeBetween(self, arret1, arret2, time):
        
        date_start = 0
        index_start = 0
        date_end = 0
        
        self.arret = self.depart
        
        if arret1.containsLigne(self) & arret2.containsLigne(self):
            
           while self.arret.nextStop(self) != None:
        
                if self.arret.nom == arret1.nom:
                    
                    date_start = getClosestTime(self.arret, self, to_timestamp(time));
                    index_start = self.arret.HoraireFromLigne(self).index(getClosestTime(self.arret, self, to_timestamp(time)))
                                       
                if self.arret.nextStop(self).nom == arret2.nom:
                    
                    horaire = self.arret.nextStop(self).HoraireFromLigne(self)[index_start]
                    while horaire == '-': 
                        index_start += 1
                        horaire = self.arret.nextStop(self).HoraireFromLigne(self)[index_start]
                        
                    date_end = self.arret.nextStop(self).HoraireFromLigne(self)[index_start];
                    break
                
                self.arret = self.arret.nextStop(self)
        
        result = datetime.fromtimestamp(abs(to_timestamp(date_start) - to_timestamp(date_end))) 
        
        self.arret = self.depart
        
        return f'{result.minute:02d}'
   
    
                   
def getClosestTime(arret, ligne, hour):
    
    time = 1000000000000.0
    
    result = ""
    
    for horaire in arret.HoraireFromLigne(ligne):
        if horaire != '-':
            calcule = to_timestamp(horaire) - hour
            if (calcule < time) & (calcule > 0.0):
                time = calcule
                result = horaire
    
    if result == "":
        result = arret.HoraireFromLigne(ligne)[0]
    
    return result 

   
def to_timestamp(date_str):
    if date_str == "-":
        return "-"
    date_obj = datetime.strptime(date_str, '%H:%M')
    date_obj = date_obj.replace(tzinfo=timezone.utc)

def getCurrentTime():
    
    now = datetime.now()
      
    return  f'{now.hour:02d}:{now.minute:02d}'                  
                  
        
       
       