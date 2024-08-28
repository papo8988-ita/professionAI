#ifndef STRUCTS_H
#define STRUCTS_H

#include <string>
#include <fstream>

// struct base Evento
struct Evento {
    std::string codiceCliente;
    std::string cognomeCliente;
    std::string codiceVenditore;
    std::string cognomeVenditore;

    // salvataggi e caricamenti
    void serialize(std::ofstream& out) const {
        out << codiceCliente << "\n" << cognomeCliente << "\n" << codiceVenditore << "\n" << cognomeVenditore << "\n";
    }

    void deserialize(std::ifstream& in) {
        std::getline(in, codiceCliente);
        std::getline(in, cognomeCliente);
        std::getline(in, codiceVenditore);
        std::getline(in, cognomeVenditore);
    }
};

// struct derivata Appuntamento
struct Appuntamento : public Evento {
    std::string data;
    std::string luogo;
    std::string stato;
    std::string codiceAppuntamento;

    // salvataggi e caricamenti
    void serialize(std::ofstream& out) const {
        Evento::serialize(out); // serializza attributi della struttura padre
        out << data << "\n" << luogo << "\n" << stato << "\n" << codiceAppuntamento << "\n";
    }

    void deserialize(std::ifstream& in) {
        Evento::deserialize(in); // deserializza attributi della struttura padre
        std::getline(in, data);
        std::getline(in, luogo);
        std::getline(in, stato);
        std::getline(in, codiceAppuntamento);
    }
};

// struct derivata Contratto
struct Contratto : public Evento {
    std::string tipo;
    std::string valore;
    std::string dataInizio;
    std::string durata;
    std::string stato;
    std::string codiceContratto;

    // salvataggi e caricamenti
    void serialize(std::ofstream& out) const {
        Evento::serialize(out); // serializza attributi della struttura padre
        out << tipo << "\n" << valore << "\n" << dataInizio << "\n" << durata << "\n" << stato << "\n" << codiceContratto << "\n";
    }

    void deserialize(std::ifstream& in) {
        Evento::deserialize(in); // deserializza attributi della struttura padre
        std::getline(in, tipo);
        std::getline(in, valore);
        std::getline(in, dataInizio);
        std::getline(in, durata);
        std::getline(in, stato);
        std::getline(in, codiceContratto);
    }
};

#endif // STRUCTS_H

