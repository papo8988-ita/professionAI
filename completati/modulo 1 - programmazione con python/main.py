# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:16:20 2024

@author: JacopoBaldacci
"""

import logging as log 
from os import path
from argparse import ArgumentParser, RawTextHelpFormatter

from rubrica import Rubrica

help_file = open("helper.txt", encoding="utf-8")
help_text = help_file.read()
help_file.close()

def main(args_main):
    print("++++++  programma rubrica avviato  +++++++")
    try:
        rubrica = Rubrica(args_main.path)
        
        print(f"la rubrica contiene {rubrica.get_numero_contatti()} contatti")
        print("\n   Menu Principale  ")
        print("- Aggiungi nuovo contatto [add]")
        print("- Visualizza contatti presenti [viz]")
        print("- Cerca un contatto [src]")
        print("- Modifica un contatto [mod]")
        print("- Elimina un contatto [del]")
        print("- Esporta la rubrica in un file json [exp]")
        print("- Importa contatti da file json specificando il percorso [imp]")
        print("- Descrizione dettagliata delle operazioni [help]")
        print("- Esci dal programma e salva la rubrica [exit]")
        print("\n")
        while True:
            choice = input("Seleziona un'operazione: ")
            print("\n")
            if choice == "add":
                rubrica.aggiungi_contatto()
            elif choice == "viz":
                if rubrica.get_numero_contatti() == 0:
                    print("rubrica vuota")
                else:
                    rubrica.stampa_tutti_contatti()
            elif choice == "src":
                if rubrica.get_numero_contatti() == 0:
                    print("rubrica vuota")
                else:
                    rubrica.cerca_contatto()
            elif choice == "mod":
                if rubrica.get_numero_contatti() == 0:
                    print("rubrica vuota")
                else:
                    rubrica.modifica_contatto()
            elif choice == "del":
                if rubrica.get_numero_contatti() == 0:
                    print("rubrica vuota")
                else:
                    rubrica.elimina_contatto()
            elif choice == "exp":
                if rubrica.get_numero_contatti() == 0:
                    print("rubrica vuota")
                else:
                    rubrica.esporta_lista_contatti_in_json()
            elif choice == "imp":
                rubrica.importa_lista_contatti_da_json()
            elif choice == "help":
                print(help_text)
                print("\n   Menu Principale  ")
                print("- Aggiungi nuovo contatto [add]")
                print("- Visualizza contatti presenti [viz]")
                print("- Cerca un elemento per modificarlo o eliminarlo [src]")
                print("- Esporta la rubrica in un file json [exp]")
                print("- Importa contatti da file json specificando il percorso [imp]")
                print("- Descrizione completa delle operazioni [help]")
                print("- Esci dal programma e salva la rubrica [exit]")
                print("\n")
            elif choice == "exit":
                print("Uscita dal programma...")
                break
            else:
                print("Operazione non valida., inserisci una nuova operazione")
                
        rubrica.salva_lista_contatti()
    
    except Exception as err:
   
        print(err)

        return None

    return 0

if __name__ == '__main__':
    parser = ArgumentParser(description = 'descrizione:\n  rubrica telefonica',
                                      usage = '\n  __main__.py \n',
                                      formatter_class = RawTextHelpFormatter,
                                      add_help=False)
    parser.add_argument('-p', '--path',
                        default = path.dirname(path.abspath("__file__")),
                        help='percorso ai file da utilizzare. Di default è la cartella del file main')
    args_main = parser.parse_args()
    main(args_main)
