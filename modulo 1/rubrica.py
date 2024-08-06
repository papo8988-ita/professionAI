# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 17:26:01 2024

@author: JacopoBaldacci
"""
from datetime import datetime
import pytz

tz = pytz.timezone('Europe/Rome')

from altre_classi import *

class Rubrica:
    def __init__(self, lista_contatti):
        self.lista_contatti = lista_contatti
        
    def aggiungi_contatto(self):
        cognome = input("inserisci Cognome")
        nome = input("inserisci Nome")
        mobile = self.richiedi_numero_telefono("mobile")
        fisso = self.richiedi_numero_telefono("fisso")
        data_inserimento = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
        nuovo_contatto = Contatto(cognome, nome, mobile, fisso, data_inserimento)
        
        
    def ordina_contatti(self, lista_contatti):
        self.lista_contatti = sorted(self.lista_contatti,
                                     key=lambda p: (p.get_data()["cognome"],
                                                    p.get_data()["nome"]))
        
    def richiedi_numero_telefono(self, tipo):
        """

        Parameters
        ----------
        numero_telefono : TYPE
            DESCRIPTION.

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        while True:
            numero_telefono = input(f"inserisci numero {tipo}")
            if not self.check_numero_telefono(numero_telefono, tipo):
                print("numero non valido")
            else:
                return numero_telefono
        
    def check_numero_telefono(self, numero_telefono, tipo):
        check = True
        if tipo == "fisso":
            if numero_telefono[0] != "0":
                print("il numero di telefono fisso deve iniziare con 0! ")
                check = False
        if tipo == "mobile":
            if numero_telefono[0] != "3": 
                print("il numero di telefono mobile deve iniziare con 3! ")
                check = False
            if len(numero_telefono) != 10:
                print("il numero di telefono mobile avere 10 cifre, di cui 3 per il prefisso! ")
                check = False
        return check
        