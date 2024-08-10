# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 17:26:01 2024

@author: JacopoBaldacci
"""
from datetime import datetime
import pytz
import pickle
import os
import json

tz = pytz.timezone('Europe/Rome')

from altre_classi import Contatto

class Rubrica:
    def __init__(self, path):
        self.path = path
        self.lista_contatti = self._importa_lista_contatti()
        
    # %%=======================================================================
    #         METODI ESPOSTI
    # =========================================================================      
    def aggiungi_contatto(self):
        while True:
            data_inserimento = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
            nuovo_contatto = Contatto(data_inserimento=data_inserimento)
            nuovo_contatto.set_data("nome")
            nuovo_contatto.set_data("cognome")
            if self._check_nome_gia_esistente(nuovo_contatto):
                print(f"Un contatto con lo stesso nome e lo stesso cognome esiste già nella lista.")
            else: 
                nuovo_contatto.set_data("numero_mobile")
                nuovo_contatto.set_data("numero_fisso")
                self.lista_contatti.append(nuovo_contatto)
                self._ordina_contatti()
                print("nuovo contatto inserito\n")
                return True
    
    # i metodi esposti di ricerca, modifica e eliminazione di un contatto chiamano al loro interno un metodo non esposto che svolge l'operazione vera e propria   
    def cerca_contatto(self):
        while True:
            stringa_ricerca = input("inserisci nome o cognome (anche parziale) del contatto che cerchi (0 per tornare indietro): ")
            if stringa_ricerca == "":
                print("la stringa di ricerca non può essere vuota")
            elif stringa_ricerca == "0":
                print("\n")
                return False
            else:
                risultati = self._cerca_contatto(stringa_ricerca)
                if risultati:
                   print("\nRisultati trovati:")
                   for i, contatto in enumerate(risultati):
                       nome_temp = contatto['contatto'].get_data()["nome"]
                       cognome_temp = contatto['contatto'].get_data()["cognome"]
                       print(f"{i + 1}. {nome_temp} {cognome_temp}")
                   print("\n")
                   return risultati
                else:
                   print("nessun risultato trovato \n")
        
    def modifica_contatto(self):
        risultati = self.cerca_contatto()
        if risultati:
            while True:
                numero = int(input("Specifica il numero dell'elemento (inserisci 0 per tornare indietro): ")) - 1
                if 0 <= numero < len(risultati):
                    idx_originale = risultati[numero]["idx"]
                    while True:
                        campo_modifica = input("quale campo vuoi modificare? [n(nome), c(cognome), m(nro mobile), f(nro fisso), b(torna indietro)] ")
                        if campo_modifica in ['n', 'c', 'm', 'f']:
                            self._modifica_contatto(idx_originale, campo_modifica)
                            print("contatto modificato\n")
                            self._ordina_contatti()
                            return True
                        elif campo_modifica == "b":
                            print("\n")
                            return True
                        else:
                            print("campo non valida, inserisci un campo valido")
                elif numero < 0:
                    print("\n")
                    return True
                else:
                    print("numero non valido, inserisci un numro valido oppure inserisci 0 per tornare indietro")
                
    def elimina_contatto(self):
        risultati = self.cerca_contatto()
        if risultati:
            while True:
                numero = int(input("Specifica il numero dell'elemento (inserisci 0 per tornare indietro): ")) - 1
                if 0 <= numero < len(risultati):
                    idx_originale = risultati[numero]["idx"]
                    self._elimina_contatto(idx_originale)
                    print("contatto rimosso\n")
                    return True
                elif numero < 0:
                    print("\n")
                    return True
                else:
                    print("numero non valido, inserisci un numro valido oppure inserisci 0 per tornare indietro")
            
    def stampa_tutti_contatti(self):
        print("lista completa dei contatti: \n")
        for contatto in self.lista_contatti:
            dati = contatto.get_data()
            print(f'- {dati["cognome"]} {dati["nome"]}, mobile: {dati["numero mobile"]},' \
                  f' fisso: {dati["numero fisso"]}, data inserimento: {dati["data inserimento"]}')
        print("\n")
        
    def esporta_lista_contatti_in_json(self):
        lista_contatti_export = []
        for contatto in self.lista_contatti:
            dati_contatto = contatto.get_data()
            lista_contatti_export.append(dati_contatto)
        with open("lista_contatti_json.json", "w") as json_file:
            json.dump(lista_contatti_export, json_file, indent=4)
        print(f"lista contatti salvata in formato json nella cartella {self.path}\n")
        
    def importa_lista_contatti_da_json(self):
        percorso_file = input("inserisci il percorso del file: ")
        if os.path.exists(percorso_file):
            with open(percorso_file, 'r') as json_file:
                nuovi_dati = json.load(json_file)
            for nuovo_dato_temp in nuovi_dati:
                print(f'\n\n- {nuovo_dato_temp["cognome"]} {nuovo_dato_temp["nome"]}:')
                data_inserimento = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
                nuovo_contatto = Contatto(data_inserimento=data_inserimento)
                if not nuovo_contatto.set_data_da_esterno("nome", nuovo_dato_temp["nome"]):
                    pass
                else:
                    nuovo_contatto.set_data_da_esterno("cognome", nuovo_dato_temp["cognome"])
                    if self._check_nome_gia_esistente(nuovo_contatto):
                        print(f"Un contatto con lo stesso nome e lo stesso cognome esiste già nella lista.")
                    else: 
                        if not nuovo_contatto.set_data_da_esterno("numero_mobile", nuovo_dato_temp["numero mobile"]):
                            print(f"{nuovo_dato_temp['nome']} ha un numero mobile non valido")
                        else:
                            if not nuovo_contatto.set_data_da_esterno("numero_fisso", nuovo_dato_temp["numero fisso"]):
                                print(f"{nuovo_dato_temp['nome']} ha un numero fisso non valido")
                            else:
                                self.lista_contatti.append(nuovo_contatto)
                                print(f"contatto inserito correttamente")
            self._ordina_contatti()
            print("\n\ninserimento completato\n")
                    
        else:
            "file inesistente\n"
        
    def get_numero_contatti(self):
        return len(self.lista_contatti)
        
    def salva_lista_contatti(self):
        # salvataggio in file .pkl alla chiusura del programma
        with open('lista_contatti.pkl', 'wb') as file:
            pickle.dump(self.lista_contatti, file)
        
    
    # %%=======================================================================
    #         METODI NON ESPOSTI
    # =========================================================================
    def _check_nome_gia_esistente(self, nuovo_contatto):
        nuovo_nome = nuovo_contatto.get_data()["nome"]
        nuovo_cognome= nuovo_contatto.get_data()["cognome"]
        for contatto in self.lista_contatti:
            if contatto.get_data()["nome"] == nuovo_nome \
                and contatto.get_data()["cognome"] == nuovo_cognome:
                return True
        return False
        
    
    def _modifica_contatto(self, indice, campo_modifica):
        if campo_modifica == "n":
            campo_modifica_completo = "nome"
        elif campo_modifica == "c":
            campo_modifica_completo = "cognome"
        elif campo_modifica == "m":
            campo_modifica_completo = "numero_mobile"
        elif campo_modifica == "f":
            campo_modifica_completo = "numero_fisso"
        else:
            print("campo non valido")
            return True
        contatto_da_modificare = self.lista_contatti[indice]
        print(f"{campo_modifica_completo.replace('_', ' ')} attuale: " \
              f"{contatto_da_modificare.get_data()[campo_modifica_completo.replace('_', ' ')]}")
        contatto_da_modificare.set_data(campo_modifica_completo)
        self.lista_contatti[indice] = contatto_da_modificare
        

    def _elimina_contatto(self, indice):
        del self.lista_contatti[indice]
        
    def _cerca_contatto(self, stringa):
        risultati = []
        for i, c in enumerate(self.lista_contatti):
            if stringa.lower() in c.get_data()["nome"].lower() or stringa.lower() in c.get_data()["cognome"].lower():
                risultati.append({"idx": i, "contatto": c})
        return risultati
    
    def _importa_lista_contatti(self):
        # import del file .pkl ottenuto dopo l'ultimo salvataggio. Se non esiste viene inizializzata una lista vuota
        path_lista_contatti = self.path+"\\lista_contatti.pkl"
        if os.path.exists(path_lista_contatti):
            with open('lista_contatti.pkl', 'rb') as file:
                lista_contatti = pickle.load(file)
        else:
            lista_contatti = []
        return lista_contatti
    
    def _ordina_contatti(self):
        self.lista_contatti = sorted(self.lista_contatti,
                                     key=lambda p: (p.get_data()["cognome"].lower(),
                                                    p.get_data()["nome"].lower()))
    
    