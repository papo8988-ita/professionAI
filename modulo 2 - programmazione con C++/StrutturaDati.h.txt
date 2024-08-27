#ifndef STRUTTURADATI_H
#define STRUTTURADATI_H

#include <vector>
#include <iostream>
#include <string>
#include <algorithm>
#include "VenditoriClienti.h"

class StrutturaDati {
public:
    std::vector<Venditore> venditori;
    std::vector<Cliente> clienti;

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
            std::cerr << "Errore nell'apertura del file di input.\n";
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

    void inserisciCliente() {
        Cliente c;
        std::cout << "Inserisci nome cliente: ";
        std::cin >> c.nome;
        std::cout << "Inserisci cognome cliente: ";
        std::cin >> c.cognome;

        clienti.push_back(c);
    }

    void inserisciVenditore() {
        Venditore v;
        std::cout << "Inserisci nome venditore: ";
        std::cin >> v.nome;
        std::cout << "Inserisci cognome venditore: ";
        std::cin >> v.cognome;

        venditori.push_back(v);
    }

    void inserisciAppuntamento() {
        if (clienti.empty() || venditori.empty()) {
            std::cerr << "Devi avere almeno un cliente e un venditore per inserire un appuntamento.\n";
            return;
        }

        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == -1) return;

        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == -1) return;

        Appuntamento app;
        std::cout << "Inserisci codice appuntamento: ";
        std::cin >> app.codice;
        std::cout << "Inserisci data appuntamento: ";
        std::cin >> app.data;
        std::cout << "Inserisci luogo appuntamento: ";
        std::cin >> app.luogo;
        app.cognomeCliente = clienti[indiceCliente].cognome;
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
        if (indiceCliente == -1) return;

        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == -1) return;

        Contratto con;
        std::cout << "Inserisci codice contratto: ";
        std::cin >> con.codice;
        std::cout << "Inserisci tipo contratto: ";
        std::cin >> con.tipo;
        std::cout << "Inserisci valore contratto: ";
        std::cin >> con.valore;
        con.cognomeCliente = clienti[indiceCliente].cognome;
        con.cognomeVenditore = venditori[indiceVenditore].cognome;

        clienti[indiceCliente].contratti.push_back(con);
        venditori[indiceVenditore].contratti.push_back(con);
    }

    void cercaVenditore() {
        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == -1) return;

        int scelta;
        std::cout << "Vuoi visualizzare (1) contratti o (2) appuntamenti? ";
        std::cin >> scelta;

        if (scelta == 1) {
            std::cout << "Contratti del venditore " << venditori[indiceVenditore].nome << " " << venditori[indiceVenditore].cognome << ":\n";
            for (const auto& con : venditori[indiceVenditore].contratti) {
                std::cout << "Codice: " << con.codice << ", Tipo: " << con.tipo << ", Valore: " << con.valore 
                          << ", Cliente: " << con.cognomeCliente << ", Venditore: " << con.cognomeVenditore << "\n";
            }
        } else if (scelta == 2) {
            std::cout << "Appuntamenti del venditore " << venditori[indiceVenditore].nome << " " << venditori[indiceVenditore].cognome << ":\n";
            for (const auto& app : venditori[indiceVenditore].appuntamenti) {
                std::cout << "Codice: " << app.codice << ", Data: " << app.data << ", Luogo: " << app.luogo 
                          << ", Cliente: " << app.cognomeCliente << ", Venditore: " << app.cognomeVenditore << "\n";
            }
        } else {
            std::cerr << "Scelta non valida.\n";
        }
    }

    void cercaCliente() {
        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == -1) return;

        int scelta;
        std::cout << "Vuoi visualizzare (1) contratti o (2) appuntamenti? ";
        std::cin >> scelta;

        if (scelta == 1) {
            std::cout << "Contratti del cliente " << clienti[indiceCliente].nome << " " << clienti[indiceCliente].cognome << ":\n";
            for (const auto& con : clienti[indiceCliente].contratti) {
                std::cout << "Codice: " << con.codice << ", Tipo: " << con.tipo << ", Valore: " << con.valore 
                          << ", Cliente: " << con.cognomeCliente << ", Venditore: " << con.cognomeVenditore << "\n";
            }
        } else if (scelta == 2) {
            std::cout << "Appuntamenti del cliente " << clienti[indiceCliente].nome << " " << clienti[indiceCliente].cognome << ":\n";
            for (const auto& app : clienti[indiceCliente].appuntamenti) {
                std::cout << "Codice: " << app.codice << ", Data: " << app.data << ", Luogo: " << app.luogo 
                          << ", Cliente: " << app.cognomeCliente << ", Venditore: " << app.cognomeVenditore << "\n";
            }
        } else {
            std::cerr << "Scelta non valida.\n";
        }
    }

    void modificaVenditore() {
        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == -1) return;

        int scelta;
        do {
            std::cout << "Modifica venditore " << venditori[indiceVenditore].nome << " " << venditori[indiceVenditore].cognome << ":\n";
            std::cout << "1. Modifica nome\n";
            std::cout << "2. Modifica cognome\n";
            std::cout << "0. Torna indietro\n";
            std::cout << "Scegli un'opzione: ";
            std::cin >> scelta;

            switch (scelta) {
                case 1:
                    std::cout << "Inserisci nuovo nome: ";
                    std::cin >> venditori[indiceVenditore].nome;
                    break;
                case 2:
                    std::cout << "Inserisci nuovo cognome: ";
                    std::cin >> venditori[indiceVenditore].cognome;
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
        if (indiceCliente == -1) return;

        int scelta;
        do {
            std::cout << "Modifica cliente " << clienti[indiceCliente].nome << " " << clienti[indiceCliente].cognome << ":\n";
            std::cout << "1. Modifica nome\n";
            std::cout << "2. Modifica cognome\n";
            std::cout << "0. Torna indietro\n";
            std::cout << "Scegli un'opzione: ";
            std::cin >> scelta;

            switch (scelta) {
                case 1:
                    std::cout << "Inserisci nuovo nome: ";
                    std::cin >> clienti[indiceCliente].nome;
                    break;
                case 2:
                    std::cout << "Inserisci nuovo cognome: ";
                    std::cin >> clienti[indiceCliente].cognome;
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

    void eliminaVenditore() {
        size_t indiceVenditore = selezionaVenditore();
        if (indiceVenditore == -1) return;

        venditori.erase(venditori.begin() + indiceVenditore);
        std::cout << "Venditore eliminato con successo.\n";
    }

    void eliminaCliente() {
        size_t indiceCliente = selezionaCliente();
        if (indiceCliente == -1) return;

        clienti.erase(clienti.begin() + indiceCliente);
        std::cout << "Cliente eliminato con successo.\n";
    }

private:
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
        std::cout << "Inserisci stringa da cercare nel nome o cognome del venditore (lascia vuoto per visualizzare tutti): ";
        std::cin.ignore();
        std::getline(std::cin, ricerca);

        std::vector<size_t> risultati = ricercaVenditori(ricerca);

        if (risultati.empty()) {
            std::cout << "Nessun venditore trovato.\n";
            return -1;
        }

        std::cout << "Venditori trovati:\n";
        for (size_t i = 0; i < risultati.size(); ++i) {
            std::cout << i + 1 << ". " << venditori[risultati[i]].nome << " " << venditori[risultati[i]].cognome << "\n";
        }
        std::cout << "Seleziona un venditore (numero): ";
        size_t indiceVenditore;
        std::cin >> indiceVenditore;
        return risultati[indiceVenditore - 1];
    }

    size_t selezionaCliente() {
        std::string ricerca;
        std::cout << "Inserisci stringa da cercare nel nome o cognome del cliente (lascia vuoto per visualizzare tutti): ";
        std::cin.ignore();
        std::getline(std::cin, ricerca);

        std::vector<size_t> risultati = ricercaClienti(ricerca);

        if (risultati.empty()) {
            std::cout << "Nessun cliente trovato.\n";
            return -1;
        }

        std::cout << "Clienti trovati:\n";
        for (size_t i = 0; i < risultati.size(); ++i) {
            std::cout << i + 1 << ". " << clienti[risultati[i]].nome << " " << clienti[risultati[i]].cognome << "\n";
        }
        std::cout << "Seleziona un cliente (numero): ";
        size_t indiceCliente;
        std::cin >> indiceCliente;
        return risultati[indiceCliente - 1];
    }
};

#endif // STRUTTURADATI_H

