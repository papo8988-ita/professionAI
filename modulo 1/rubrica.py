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
        nome = self._richiedi_nome("inserisci nome: ")
        cognome = input("inserisci cognome: ")
        mobile = self._richiedi_numero_telefono("mobile")
        fisso = self._richiedi_numero_telefono("fisso")
        data_inserimento = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
        nuovo_contatto = Contatto(nome, cognome, mobile, fisso, data_inserimento)
        self.lista_contatti.append(nuovo_contatto)
        self.ordina_contatti()
        
        
    def ordina_contatti(self):
        self.lista_contatti = sorted(self.lista_contatti,
                                     key=lambda p: (p.get_data()["cognome"],
                                                    p.get_data()["nome"]))
        
    def operazione_su_contatto(self):
        stringa_ricerca = self._richiedi_nome("inserisci nome o cognome (anche parziale) del contatto che cerchi: ")
        risultati = self.cerca_contatto(stringa_ricerca)
        if risultati:
           print("Risultati trovati:")
           lista_contatti_temp = []
           for i, contatto in enumerate(risultati):
               nome_temp = contatto['contatto'].get_data()["nome"]
               cognome_temp = contatto['contatto'].get_data()["cognome"]
               print(f"{i + 1}. {nome_temp} {cognome_temp}")
           scelta = input("Vuoi rimuovere (r) o modificare (m) un elemento? (r/m): ").strip().lower()
           if scelta in ['r', 'm']:
               numero = int(input("Specifica il numero dell'elemento: ")) - 1
               if 0 <= numero < len(risultati):
                   idx_originale = risultati[numero]["idx"]
                   if scelta == "r":
                       # metodo rimozione sui contatti
                       contatto_da_rimuovere = self.lista_contatti[idx_originale]
                       self.lista_contatti = contatto_da_rimuovere.elimina(self.lista_contatti)
                   elif scelta == "m":
                       pass
                       ## quale campo vuoi modificare??
                       
        else:
            print("nessun risultato trovato")
        
    def cerca_contatto(self, stringa):
        risultati = []
        for i, c in enumerate(self.lista_contatti):
            if stringa.lower() in c.get_data()["nome"].lower() or stringa.lower() in c.get_data()["cognome"].lower():
                risultati.append({"idx": i, "contatto": c})
        return risultati
    
    def rimuovi_persona(indice):
        del self.lista_contatti[indice]
        
    def _richiedi_nome(self, stringa_input):
        while True:
            nome = input(stringa_input)
            if nome == "":
                print("il nome non può essere vuoto")
            else:
                return nome
        
    def _richiedi_numero_telefono(self, tipo):
        while True:
            numero_telefono = input(f"inserisci numero {tipo}: ")
            if not self.check_numero_telefono(numero_telefono, tipo):
                print("numero non valido")
            else:
                return numero_telefono
        
    def _check_numero_telefono(self, numero_telefono, tipo):
        check = True
        if numero_telefono == "":
            return check
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
    
        