#ifndef STRUTTURADATI_H
#define STRUTTURADATI_H

#include <vector>
#include <iostream>
#include <string>
#include <algorithm>
#include <fstream>
#include "VenditoriClienti.h"

class StrutturaDati {
public:
    std::vector<Venditore> venditori;
    std::vector<Cliente> clienti;

    // salvataggi e caricamenti
    void serialize(const std::string& filename) const {
        std::ofstream out(filename);
        if (!out) {
            std::cerr << "Errore nell'apertura del file di output.\n";
            return;
        }
        out << venditori.size() << "\n";
        for (const auto& venditore : venditori) {
            venditore.serialize(out);
        }
        out << clienti.size() << "\n";
        for (const auto& cliente : clienti) {
            cliente.serialize(out);
        }
    }

    void deserialize(const std::string& filename) {
        std::ifstream in(filename);
        if (!in) {
            std::cerr << "Dati non trovati, inizializzato programma vuoto.\n";
            return;
        }
        size_t venditoriSize, clientiSize;
        in >> venditoriSize; in.ignore();
        venditori.resize(venditoriSize);
        for (auto& venditore : venditori) {
            venditore.deserialize(in);
        }
        in >> clientiSize; in.ignore();
        clienti.resize(clientiSize);
        for (auto& cliente : clienti) {
            cliente.deserialize(in);
        }
    }

    // inserimento persone
    void inserisciCliente() {
        Cliente c;
        std::cout << "Inserisci nome cliente: ";
        std::cin >> c.nome;
        std::cout << "Inserisci cognome cliente: ";
        std::cin >> c.cognome;
        std::cout << "Inserisci codice cliente: ";
        std::cin >> c.codiceCliente;

        clienti.push_back(c);
    }

    void inserisciVenditore() {
        Venditore v;
        std::cout << "Inserisci nome venditore: ";
        std::cin >> v.nome;
        std::cout << "Inserisci cognome venditore: ";
        std::cin >> v.cognome;
        std::cout << "Inserisci numero di matricola del venditore: ";
        std::cin >> v.numeroMatricola;

        venditori.push_back(v);
    }

    // inserimento eventi
    void inserisciAppuntamento() {
        if (clienti.empty() || venditori.empty()) {
            std::cerr << "Devi avere almeno un cliente e un venditore per inserire un appuntamento.\n";
            return;
        }

        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == static_cast<size_t>(-1)) return;

        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == static_cast<size_t>(-1)) return;

        Appuntamento app;
        std::cout << "\nInserisci codice: ";
        std::cin >> app.codiceAppuntamento;
        // Controllo di eventuali duplicati
        if (isCodiceAppuntamentoDuplicato(app.codiceAppuntamento)) {
            std::cerr << "\nERRORE: Esiste già un appuntamento con questo codice.\n";
            return;
        }
        std::cout << "Inserisci data appuntamento: ";
        std::cin >> app.data;
        std::cout << "Inserisci luogo appuntamento (città): ";
        std::cin >> app.luogo;
        std::cout << "Inserisci stato appuntamento (annullato, previsto, avvenuto): ";
        std::cin >> app.stato;
        app.codiceCliente = clienti[indiceCliente].codiceCliente;
        app.cognomeCliente = clienti[indiceCliente].cognome;
        app.codiceVenditore = venditori[indiceVenditore].numeroMatricola;
        app.cognomeVenditore = venditori[indiceVenditore].cognome;

        clienti[indiceCliente].appuntamenti.push_back(app);
        venditori[indiceVenditore].appuntamenti.push_back(app);
    }

    void inserisciContratto() {
        if (clienti.empty() || venditori.empty()) {
            std::cerr << "Devi avere almeno un cliente e un venditore per inserire un contratto.\n";
            return;
        }

        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == static_cast<size_t>(-1)) return;

        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == static_cast<size_t>(-1)) return;

        Contratto con;
        std::cout << "\nInserisci codice: ";
        std::cin >> con.codiceContratto;
        // Controllo di eventuali duplicati
        if (isCodiceContrattoDuplicato(con.codiceContratto)) {
            std::cerr << "\nERRORE: Esiste già un contratto con questo codice.\n";
            return;
        }
        std::cout << "Inserisci tipo contratto: ";
        std::cin >> con.tipo;
        std::cout << "Inserisci valore contratto (in euro): ";
        std::cin >> con.valore;
        std::cout << "Inserisci data inizio contratto: ";
        std::cin >> con.dataInizio;
        std::cout << "Inserisci durata contratto (in mesi): ";
        std::cin >> con.durata;
        std::cout << "Inserisci lo stato del contratto (valido, scaduto, sospeso): ";
        std::cin >> con.stato;
        con.codiceCliente = clienti[indiceCliente].codiceCliente;
        con.cognomeCliente = clienti[indiceCliente].cognome;
        con.codiceVenditore = venditori[indiceVenditore].numeroMatricola;
        con.cognomeVenditore = venditori[indiceVenditore].cognome;

        clienti[indiceCliente].contratti.push_back(con);
        venditori[indiceVenditore].contratti.push_back(con);
    }

    // ricerca e visualizzazione
    void cercaVenditore() {
        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == static_cast<size_t>(-1)) return;

        int scelta;
        std::cout << "Vuoi visualizzare (1) contratti o (2) appuntamenti? ";
        std::cin >> scelta;

        if (scelta == 1) {
            std::cout << "\nContratti del venditore " << venditori[indiceVenditore].nome << " " << venditori[indiceVenditore].cognome << ":\n\n";
            for (const auto& con : venditori[indiceVenditore].contratti) {
                std::cout << "Codice: " << con.codiceContratto << "Tipo: " << con.tipo << ", Valore: " << con.valore << ", Stato: " << con.stato
                          << ", Cliente: " << con.codiceCliente << ", Venditore: " << con.codiceVenditore << "\n";
            }
        } else if (scelta == 2) {
            std::cout << "\nAppuntamenti del venditore " << venditori[indiceVenditore].nome << " " << venditori[indiceVenditore].cognome << ":\n\n";
            for (const auto& app : venditori[indiceVenditore].appuntamenti) {
                std::cout << "Codice: " << app.codiceAppuntamento << ", Data: " << app.data << ", Luogo: " << app.luogo << ", Stato: " << app.stato
                          << ", Cliente: " << app.codiceCliente << ", Venditore: " << app.codiceVenditore << "\n";
            }
        } else {
            std::cerr << "Scelta non valida.\n";
        }
    }

    void cercaCliente() {
        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == static_cast<size_t>(-1)) return;

        int scelta;
        std::cout << "Vuoi visualizzare (1) contratti o (2) appuntamenti? ";
        std::cin >> scelta;

        if (scelta == 1) {
            std::cout << "\nContratti del cliente " << clienti[indiceCliente].nome << " " << clienti[indiceCliente].cognome << ":\n\n";
            for (const auto& con : clienti[indiceCliente].contratti) {
                std::cout << "Codice: " << con.codiceContratto << ", Tipo: " << con.tipo << ", Valore: " << con.valore << ", Stato: " << con.stato
                          << ", Cliente: " << con.codiceCliente << ", Venditore: " << con.codiceVenditore << "\n";
            }
        } else if (scelta == 2) {
            std::cout << "\nAppuntamenti del cliente " << clienti[indiceCliente].nome << " " << clienti[indiceCliente].cognome << ":\n\n";
            for (const auto& app : clienti[indiceCliente].appuntamenti) {
                std::cout << "Codice: " << app.codiceAppuntamento << ", Data: " << app.data << ", Luogo: " << app.luogo << ", Stato: " << app.stato
                          << ", Cliente: " << app.codiceCliente << ", Venditore: " << app.codiceVenditore << "\n";
            }
        } else {
            std::cerr << "Scelta non valida.\n";
        }
    }

    // modifca
    void modificaVenditore() {
        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == static_cast<size_t>(-1)) return;

        int scelta;
        do {
            std::cout << "Modifica venditore " << venditori[indiceVenditore].nome << " " << venditori[indiceVenditore].cognome << ":\n";
            std::cout << "1. Modifica nome\n";
            std::cout << "2. Modifica cognome\n";
            std::cout << "3. Modifica numero di matricola\n";
            std::cout << "4. Modifica lo stato di un contratto\n";
            std::cout << "5. Modifica lo stato di un appuntamento\n";
            std::cout << "0. Torna indietro\n";
            std::cout << "Scegli un'opzione: ";
            std::cin >> scelta;

            switch (scelta) {
                case 1:
                    std::cout << "Inserisci nuovo nome (attuale: " << venditori[indiceVenditore].nome << "): ";
                    std::cin >> venditori[indiceVenditore].nome;
                    break;
                case 2:
                    std::cout << "Inserisci nuovo cognome (attuale: " << venditori[indiceVenditore].cognome << "): ";
                    std::cin >> venditori[indiceVenditore].cognome;
                    break;
                case 3:
                    std::cout << "Inserisci nuovo numero di matricola (attuale: " << venditori[indiceVenditore].numeroMatricola << "): ";
                    std::cin >> venditori[indiceVenditore].numeroMatricola;
                    break;
                case 4:
                    modificaContrattoVenditore(indiceVenditore);
                    break;
                case 5:
                    modificaAppuntamentoVenditore(indiceVenditore);
                    break;
                case 0:
                    std::cout << "Modifica annullata.\n";
                    break;
                default:
                    std::cerr << "Opzione non valida.\n";
                    break;
            }
        } while (scelta != 0);
    }

    void modificaCliente() {
        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == static_cast<size_t>(-1)) return;

        int scelta;
        do {
            std::cout << "Modifica cliente " << clienti[indiceCliente].nome << " " << clienti[indiceCliente].cognome << ":\n";
            std::cout << "1. Modifica nome\n";
            std::cout << "2. Modifica cognome\n";
            std::cout << "3. Modifica codice cliente\n";
            std::cout << "4. Modifica lo stato di un contratto\n";
            std::cout << "5. Modifica lo stato di un appuntamento\n";
            std::cout << "0. Torna indietro\n";
            std::cout << "Scegli un'opzione: ";
            std::cin >> scelta;

            switch (scelta) {
                case 1:
                    std::cout << "Inserisci nuovo nome (attuale: " << clienti[indiceCliente].nome << "): ";
                    std::cin >> clienti[indiceCliente].nome;
                    break;
                case 2:
                    std::cout << "Inserisci nuovo cognome (attuale: " << clienti[indiceCliente].cognome << "): ";
                    std::cin >> clienti[indiceCliente].cognome;
                    break;
                case 3:
                    std::cout << "Inserisci nuovo codice cliente (attuale: " << clienti[indiceCliente].codiceCliente << "): ";
                    std::cin >> clienti[indiceCliente].codiceCliente;
                    break;
                case 4:
                    modificaContrattoCliente(indiceCliente);
                    break;
                case 5:
                    modificaAppuntamentoCliente(indiceCliente);
                    break;
                case 0:
                    std::cout << "Modifica annullata.\n";
                    break;
                default:
                    std::cerr << "Opzione non valida.\n";
                    break;
            }
        } while (scelta != 0);
    }

    // eliminazione
    void eliminaVenditore() {
        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == static_cast<size_t>(-1)) return;

        venditori.erase(venditori.begin() + indiceVenditore);
        std::cout << "Venditore eliminato con successo.\n";
    }

    void eliminaCliente() {
        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == static_cast<size_t>(-1)) return;

        clienti.erase(clienti.begin() + indiceCliente);
        std::cout << "Cliente eliminato con successo.\n";
    }

private:
    // funzioni accessorie
    std::vector<size_t> ricercaVenditori(const std::string& ricerca) {
        std::vector<size_t> risultati;
        for (size_t i = 0; i < venditori.size(); ++i) {
            if (ricerca.empty() || venditori[i].nome.find(ricerca) != std::string::npos || venditori[i].cognome.find(ricerca) != std::string::npos) {
                risultati.push_back(i);
            }
        }
        return risultati;
    }

    std::vector<size_t> ricercaClienti(const std::string& ricerca) {
        std::vector<size_t> risultati;
        for (size_t i = 0; i < clienti.size(); ++i) {
            if (ricerca.empty() || clienti[i].nome.find(ricerca) != std::string::npos || clienti[i].cognome.find(ricerca) != std::string::npos) {
                risultati.push_back(i);
            }
        }
        return risultati;
    }

    size_t selezionaVenditore() {
        std::string ricerca;
        std::cout << "Inserisci stringa da cercare nel nome o cognome del venditore (lascia vuoto per visualizzare tutti): \n";
        std::cin.ignore();
        std::getline(std::cin, ricerca);

        std::vector<size_t> risultati = ricercaVenditori(ricerca);

        if (risultati.empty()) {
            std::cout << "Nessun venditore trovato.\n";
            return static_cast<size_t>(-1);
        }

        std::cout << "Venditori trovati:\n";
        for (size_t i = 0; i < risultati.size(); ++i) {
            std::cout << i + 1 << ". " << venditori[risultati[i]].nome << " " << venditori[risultati[i]].cognome <<  \
            ", matricola " << venditori[risultati[i]].numeroMatricola << "\n";
        }
        std::cout << "Seleziona un venditore (numero): ";
        size_t indiceVenditore;
        std::cin >> indiceVenditore;
        return risultati[indiceVenditore - 1];
    }

    size_t selezionaCliente() {
        std::string ricerca;
        std::cout << "Inserisci stringa da cercare nel nome o cognome del cliente (lascia vuoto per visualizzare tutti): \n";
        std::cin.ignore();
        std::getline(std::cin, ricerca);

        std::vector<size_t> risultati = ricercaClienti(ricerca);

        if (risultati.empty()) {
            std::cout << "Nessun cliente trovato.\n";
            return static_cast<size_t>(-1);
        }

        std::cout << "Clienti trovati:\n";
        for (size_t i = 0; i < risultati.size(); ++i) {
            std::cout << i + 1 << ". " << clienti[risultati[i]].nome << " " << clienti[risultati[i]].cognome << \
            ", codice " << clienti[risultati[i]].codiceCliente << "\n";
        }
        std::cout << "Seleziona un cliente (numero): ";
        size_t indiceCliente;
        std::cin >> indiceCliente;
        return risultati[indiceCliente - 1];
    }
    
    void modificaContrattoVenditore(size_t indiceVenditore) {
        if (venditori[indiceVenditore].contratti.empty()) {
            std::cout << "Nessun contratto disponibile.\n";
            return;
        }
    
        std::cout << "Seleziona un contratto da modificare:\n";
        for (size_t i = 0; i < venditori[indiceVenditore].contratti.size(); ++i) {
            std::cout << i + 1 << ". " << venditori[indiceVenditore].contratti[i].codiceContratto << " " <<
            venditori[indiceVenditore].contratti[i].stato << " con cliente " <<
            venditori[indiceVenditore].contratti[i].cognomeCliente << "\n";
        }
    
        size_t indiceContratto;
        std::cin >> indiceContratto;
        if (indiceContratto < 1 || indiceContratto > venditori[indiceVenditore].contratti.size()) {
            std::cerr << "Indice non valido.\n";
            return;
        }
    
        --indiceContratto; // Converti in indice zero-based
    
        std::cout << "Inserisci nuovo stato per il contratto: valido, scaduto, sospeso (attuale:  " << \
            venditori[indiceVenditore].contratti[indiceContratto].stato << "): ";
        std::cin >> venditori[indiceVenditore].contratti[indiceContratto].stato;
        
        // modifica contratto corrispondente anche nel cliente
        std::string codiceCliente = venditori[indiceVenditore].contratti[indiceContratto].codiceCliente;
        std::string nuovoStato = venditori[indiceVenditore].contratti[indiceContratto].stato;
        std::string codiceContratto = venditori[indiceVenditore].contratti[indiceContratto].codiceContratto;
    
        for (size_t i = 0; i < clienti.size(); ++i) {
            if (clienti[i].codiceCliente == codiceCliente) {
                for (size_t j = 0; j < clienti[i].contratti.size(); ++j) {
                    if (clienti[i].contratti[j].codiceContratto == codiceContratto) {
                        clienti[i].contratti[j].stato = nuovoStato;
                        break;
                    }
                }
                break;
            }
        }
    }
    
    void modificaAppuntamentoVenditore(size_t indiceVenditore) {
        if (venditori[indiceVenditore].appuntamenti.empty()) {
            std::cout << "Nessun appuntamento disponibile.\n";
            return;
        }
    
        std::cout << "Seleziona un appuntamento da modificare:\n";
        for (size_t i = 0; i < venditori[indiceVenditore].appuntamenti.size(); ++i) {
            std::cout << i + 1 << ". " << venditori[indiceVenditore].appuntamenti[i].codiceAppuntamento << " " << 
            venditori[indiceVenditore].appuntamenti[i].stato << " con cliente " <<
            venditori[indiceVenditore].appuntamenti[i].cognomeCliente << "\n";        }
    
        size_t indiceAppuntamento;
        std::cin >> indiceAppuntamento;
        if (indiceAppuntamento < 1 || indiceAppuntamento > venditori[indiceVenditore].appuntamenti.size()) {
            std::cerr << "Indice non valido.\n";
            return;
        }
    
        --indiceAppuntamento; // Converti in indice zero-based
    
        std::cout << "Inserisci nuovo stato per l'appuntamento: annulato, previsto, avvenuto (attuale:  " << \
            venditori[indiceVenditore].appuntamenti[indiceAppuntamento].stato << "): ";
        std::cin >> venditori[indiceVenditore].appuntamenti[indiceAppuntamento].stato;
        
        // modifica appuntamento corrispondente anche nel cliente
        std::string codiceCliente = venditori[indiceVenditore].appuntamenti[indiceAppuntamento].codiceCliente;
        std::string nuovoStato = venditori[indiceVenditore].appuntamenti[indiceAppuntamento].stato;
        std::string codiceAppuntamento = venditori[indiceVenditore].appuntamenti[indiceAppuntamento].codiceAppuntamento;
    
        for (size_t i = 0; i < clienti.size(); ++i) {
            if (clienti[i].codiceCliente == codiceCliente) {
                for (size_t j = 0; j < clienti[i].appuntamenti.size(); ++j) {
                    if (clienti[i].appuntamenti[j].codiceAppuntamento == codiceAppuntamento) {
                        clienti[i].appuntamenti[j].stato = nuovoStato;
                        break;
                    }
                }
                break;
            }
        }
    }
    
    void modificaContrattoCliente(size_t indiceCliente) {
        if (clienti[indiceCliente].contratti.empty()) {
            std::cout << "Nessun contratto disponibile.\n";
            return;
        }
    
        std::cout << "Seleziona un contratto da modificare:\n";
        for (size_t i = 0; i < clienti[indiceCliente].contratti.size(); ++i) {
            std::cout << i + 1 << ". " << clienti[indiceCliente].contratti[i].codiceContratto << " " <<
            clienti[indiceCliente].contratti[i].stato << " con venditore " <<
            clienti[indiceCliente].contratti[i].cognomeVenditore << "\n";
        }
    
        size_t indiceContratto;
        std::cin >> indiceContratto;
        if (indiceContratto < 1 || indiceContratto > clienti[indiceCliente].contratti.size()) {
            std::cerr << "Indice non valido.\n";
            return;
        }
    
        --indiceContratto; // Converti in indice zero-based
    
        std::cout << "Inserisci nuovo stato per il contratto: valido, scaduto, sospeso (attuale:  " << \
            clienti[indiceCliente].contratti[indiceContratto].stato << "): ";
        std::cin >> clienti[indiceCliente].contratti[indiceContratto].stato;
        
        // modifica contratto corrispondente anche nel venditore
        std::string codiceVenditore = clienti[indiceCliente].contratti[indiceContratto].codiceVenditore;
        std::string nuovoStato = clienti[indiceCliente].contratti[indiceContratto].stato;
        std::string codiceContratto = clienti[indiceCliente].contratti[indiceContratto].codiceContratto;
    
        for (size_t i = 0; i < venditori.size(); ++i) {
            if (venditori[i].numeroMatricola == codiceVenditore) {
                for (size_t j = 0; j < venditori[i].contratti.size(); ++j) {
                    if (venditori[i].contratti[j].codiceContratto == codiceContratto) {
                        venditori[i].contratti[j].stato = nuovoStato;
                        break;
                    }
                }
                break;
            }
        }
    }
    
    void modificaAppuntamentoCliente(size_t indiceCliente) {
        if (clienti[indiceCliente].appuntamenti.empty()) {
            std::cout << "Nessun appuntamento disponibile.\n";
            return;
        }
    
        std::cout << "Seleziona un appuntamento da modificare:\n";
        for (size_t i = 0; i < clienti[indiceCliente].appuntamenti.size(); ++i) {
            std::cout << i + 1 << ". " << clienti[indiceCliente].appuntamenti[i].codiceAppuntamento << " " <<
            clienti[indiceCliente].appuntamenti[i].stato << " con venditore " <<
            clienti[indiceCliente].appuntamenti[i].cognomeVenditore << "\n";
        }
    
        size_t indiceAppuntamento;
        std::cin >> indiceAppuntamento;
        if (indiceAppuntamento < 1 || indiceAppuntamento > clienti[indiceCliente].appuntamenti.size()) {
            std::cerr << "Indice non valido.\n";
            return;
        }
    
        --indiceAppuntamento; // Converti in indice zero-based
    
        std::cout << "Inserisci nuovo stato per l'appuntamento: annulato, previsto, avvenuto (attuale:  " << \
            clienti[indiceCliente].appuntamenti[indiceAppuntamento].stato << "): ";
        std::cin >> clienti[indiceCliente].appuntamenti[indiceAppuntamento].stato;
        
        // modifica apputnamento corrispondente anche nel venditore
        std::string codiceVenditore = clienti[indiceCliente].appuntamenti[indiceAppuntamento].codiceVenditore;
        std::string nuovoStato = clienti[indiceCliente].appuntamenti[indiceAppuntamento].stato;
        std::string codiceAppuntamento = clienti[indiceCliente].appuntamenti[indiceAppuntamento].codiceAppuntamento;
    
        for (size_t i = 0; i < venditori.size(); ++i) {
            if (venditori[i].numeroMatricola == codiceVenditore) {
                for (size_t j = 0; j < venditori[i].appuntamenti.size(); ++j) {
                    if (venditori[i].appuntamenti[j].codiceAppuntamento == codiceAppuntamento) {
                        venditori[i].appuntamenti[j].stato = nuovoStato;
                        break;
                    }
                }
                break;
            }
        }
    }
    
    bool isCodiceAppuntamentoDuplicato(const std::string& codice) const {
        for (const auto& cliente : clienti) {
            for (const auto& appuntamento : cliente.appuntamenti) {
                if (appuntamento.codiceAppuntamento == codice) {
                    return true;
                }
            }
        }
        for (const auto& venditore : venditori) {
            for (const auto& appuntamento : venditore.appuntamenti) {
                if (appuntamento.codiceAppuntamento == codice) {
                    return true;
                }
            }
        }
        return false;
    }
    
    bool isCodiceContrattoDuplicato(const std::string& codice) const {
        for (const auto& cliente : clienti) {
            for (const auto& contratto : cliente.contratti) {
                if (contratto.codiceContratto == codice) {
                    return true;
                }
            }
        }
        for (const auto& venditore : venditori) {
            for (const auto& contratto : venditore.contratti) {
                if (contratto.codiceContratto == codice) {
                    return true;
                }
            }
        }
        return false;
    }
};

#endif // STRUTTURADATI_H

