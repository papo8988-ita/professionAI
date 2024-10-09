#ifndef VENDITORI_CLIENTI_H
#define VENDITORI_CLIENTI_H

#include <string>
#include <vector>
#include <fstream>
#include "Structs.h"

// Classe base Persona
class Persona {
public:
    std::string nome;
    std::string cognome;
    std::vector<Appuntamento> appuntamenti;
    std::vector<Contratto> contratti;

    virtual ~Persona() = default;

    // salvataggi e caricamenti
    virtual void serialize(std::ofstream& out) const {
        out << nome << "\n" << cognome << "\n";
        out << appuntamenti.size() << "\n";
        for (const auto& app : appuntamenti) {
            app.serialize(out);
        }
        out << contratti.size() << "\n";
        for (const auto& con : contratti) {
            con.serialize(out);
        }
    }

    virtual void deserialize(std::ifstream& in) {
        std::getline(in, nome);
        std::getline(in, cognome);
        size_t appuntamentiSize, contrattiSize;
        in >> appuntamentiSize; in.ignore();
        appuntamenti.resize(appuntamentiSize);
        for (auto& app : appuntamenti) {
            app.deserialize(in);
        }
        in >> contrattiSize; in.ignore();
        contratti.resize(contrattiSize);
        for (auto& con : contratti) {
            con.deserialize(in);
        }
    }
};

// Classe derivata Venditore
class Venditore : public Persona {
public:
    std::string numeroMatricola;

    // salvataggi e caricamenti
    void serialize(std::ofstream& out) const override {
        Persona::serialize(out); // Serializza attributi della classe base
        out << numeroMatricola << "\n";
    }

    void deserialize(std::ifstream& in) override {
        Persona::deserialize(in); // Deserializza attributi della classe base
        std::getline(in, numeroMatricola);
    }
};

// Classe derivata Cliente
class Cliente : public Persona {
public:
    std::string codiceCliente;

    // salvataggi e caricamenti
    void serialize(std::ofstream& out) const override {
        Persona::serialize(out); // Serializza attributi della classe base
        out << codiceCliente << "\n";
    }

    void deserialize(std::ifstream& in) override {
        Persona::deserialize(in); // Deserializza attributi della classe base
        std::getline(in, codiceCliente);
    }
};

#endif // VENDITORI_CLIENTI_H

