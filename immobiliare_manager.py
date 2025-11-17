"""
Classwork 2: Gestore di un'Agenzia Immobiliare con OOP e Database

Questo modulo definisce le classi per gestire un'agenzia immobiliare utilizzando
dataclasses per le entità (Agenzia, Agente, Proprieta) e una classe GestoreImmobiliare
per tutte le operazioni sul database SQLite.

Le classi principali sono:
- Agenzia: Rappresenta un'agenzia immobiliare
- Agente: Rappresenta un agente che lavora per un'agenzia
- Proprieta: Rappresenta una proprietà gestita da un agente
- GestoreImmobiliare: Gestisce tutte le operazioni sul database

Mantieni le classi esattamente come definite: i test automatici le importano direttamente.
"""

from dataclasses import dataclass
from typing import Optional
import sqlite3


__all__ = [
    "Agenzia",
    "Agente",
    "Proprieta",
    "GestoreImmobiliare",
]


@dataclass
class Agenzia:
    """Rappresenta un'agenzia immobiliare.
    
    Attributi
    ---------
    id_agenzia : int
        Identificatore univoco dell'agenzia
    nome : str
        Nome dell'agenzia
    indirizzo : str
        Indirizzo fisico dell'agenzia
    """
    id_agenzia: int
    nome: str
    indirizzo: str


@dataclass
class Agente:
    """Rappresenta un agente immobiliare.
    
    Attributi
    ---------
    id_agente : int
        Identificatore univoco dell'agente
    nome : str
        Nome completo dell'agente
    email : str
        Indirizzo email dell'agente
    id_agenzia : int
        Chiave esterna che collega l'agente a un'agenzia
    """
    id_agente: int
    nome: str
    email: str
    id_agenzia: int


@dataclass
class Proprieta:
    """Rappresenta una proprietà immobiliare.
    
    Attributi
    ---------
    id_proprieta : int
        Identificatore univoco della proprietà
    indirizzo : str
        Indirizzo della proprietà
    prezzo : float
        Prezzo della proprietà
    stato : str
        Stato corrente (es. "In vendita", "Venduto", "In affitto")
    id_agente : int
        Chiave esterna che collega la proprietà a un agente
    """
    id_proprieta: int
    indirizzo: str
    prezzo: float
    stato: str
    id_agente: int


class GestoreImmobiliare:
    """Gestisce tutte le operazioni sul database per l'agenzia immobiliare.
    
    Questa classe fornisce metodi per:
    - Creare e gestire la struttura del database
    - Inserire nuove entità (agenzie, agenti, proprietà)
    - Eseguire query complesse con JOIN tra tabelle
    - Aggiornare lo stato delle proprietà
    - Trovare statistiche sugli agenti
    
    Parametri
    ----------
    db_path : str
        Il percorso del file di database SQLite (es. "real_estate.db")
    """
    
    def __init__(self, db_path: str):
        """Inizializza il gestore e crea le tabelle se non esistono.
        
        Parametri
        ---------
        db_path : str
            Percorso al file database SQLite
            
        Comportamento
        -------------
        - Crea una connessione al database
        - Crea le tabelle agenzie, agenti e proprieta se non esistono
        - Definisce chiavi primarie e chiavi esterne per l'integrità referenziale
        """
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA foreign_keys = ON;")
        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS agenzie (
                      id_agenzia INTEGER PRIMARY KEY,
                      nome TEXT,
                      indirizzo TEXT
                  )
                  ''')
        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS agenti (
                      id_agente INTEGER PRIMARY KEY,
                      nome TEXT,
                      email TEXT,
                      id_agenzia INTEGER,                        
                      FOREIGN KEY (id_agenzia) REFERENCES agenzie(id_agenzia)
                    )
                  ''')
        self.c.execute('''
                    CREATE TABLE IF NOT EXISTS proprieta (
                        id_proprieta INTEGER PRIMARY KEY,
                        indirizzo TEXT,
                        prezzo REAL,
                        stato TEXT,
                        id_agente INTEGER,
                        FOREIGN KEY (id_agente) REFERENCES agenti(id_agente)
                    )
                    ''')
        self.conn.commit()
        
    def add_agenzia(self, agenzia: Agenzia) -> None:
        """Aggiunge una nuova agenzia al database.
        
        Parametri
        ---------
        agenzia : Agenzia
            L'oggetto Agenzia da inserire nel database
            
        Comportamento
        -------------
        Inserisce i dati dell'agenzia nella tabella agenzie.
        """
        self.c.execute('''
                INSERT INTO agenzie (id_agenzia, nome, indirizzo)
                VALUES (?, ?, ?)
                  ''', (agenzia.id_agenzia, agenzia.nome, agenzia.indirizzo))
        self.conn.commit()
    
    def add_agente(self, agente: Agente) -> None:
        """Aggiunge un nuovo agente al database.
        
        Parametri
        ---------
        agente : Agente
            L'oggetto Agente da inserire nel database
            
        Comportamento
        -------------
        Inserisce i dati dell'agente nella tabella agenti.
        La chiave esterna id_agenzia deve riferirsi a un'agenzia esistente.
        """
        self.c.execute('''
                INSERT INTO agenti (id_agente, nome, email, id_agenzia)
                VALUES (?, ?, ?, ?)
                  ''', (agente.id_agente, agente.nome, agente.email, agente.id_agenzia))
        self.conn.commit()

    
    def add_proprieta(self, proprieta: Proprieta) -> None:
        """Aggiunge una nuova proprietà al database.
        
        Parametri
        ---------
        proprieta : Proprieta
            L'oggetto Proprieta da inserire nel database
            
        Comportamento
        -------------
        Inserisce i dati della proprietà nella tabella proprieta.
        La chiave esterna id_agente deve riferirsi a un agente esistente.
        """
        self.c.execute('''
                INSERT INTO proprieta (id_proprieta, indirizzo, prezzo, stato, id_agente)
                VALUES (?, ?, ?, ?, ?)
                  ''', (proprieta.id_proprieta, proprieta.indirizzo, proprieta.prezzo, proprieta.stato, proprieta.id_agente))
        self.conn.commit()

    
    def get_proprieta_per_agente(self, id_agente: int) -> list[Proprieta]:
        """Restituisce tutte le proprietà gestite da un agente specifico.
        
        Parametri
        ---------
        id_agente : int
            L'ID dell'agente
            
        Ritorno
        -------
        list[Proprieta]
            Lista di oggetti Proprieta gestiti dall'agente.
            Lista vuota se l'agente non esiste o non ha proprietà.
        """
        self.c.execute('''
            SELECT * from proprieta
            WHERE id_agente = ?
            ''', (id_agente,))
        prop_agente = []
        for riga in self.c.fetchall():
            prop = Proprieta(id_proprieta=riga["id_proprieta"], indirizzo=riga["indirizzo"], prezzo=riga["prezzo"], stato=riga["stato"], id_agente=riga["id_agente"])
            prop_agente.append(prop)
        return prop_agente
    
    def get_agenti_per_agenzia(self, id_agenzia: int) -> list[Agente]:
        """Restituisce tutti gli agenti che lavorano per un'agenzia specifica.
        
        Parametri
        ---------
        id_agenzia : int
            L'ID dell'agenzia
            
        Ritorno
        -------
        list[Agente]
            Lista di oggetti Agente che lavorano per l'agenzia.
            Lista vuota se l'agenzia non esiste o non ha agenti.
        """
        self.c.execute('''
            SELECT * from agenti
            WHERE id_agenzia = ?
            ''', (id_agenzia,))
        agen_agenzia = []
        for riga in self.c.fetchall():
            agen = Agente(id_agente=riga["id_agente"], nome=riga["nome"], email=riga["email"], id_agenzia=riga["id_agenzia"])
            agen_agenzia.append(agen)
        return agen_agenzia
    
    def get_proprieta_per_agenzia(self, id_agenzia: int) -> list[Proprieta]:
        """Restituisce tutte le proprietà gestite da un'intera agenzia.
        
        Questa query richiede un JOIN tra le tabelle proprieta e agenti.
        
        Parametri
        ---------
        id_agenzia : int
            L'ID dell'agenzia
            
        Ritorno
        -------
        list[Proprieta]
            Lista di oggetti Proprieta gestiti dall'agenzia (attraverso i suoi agenti).
            Lista vuota se l'agenzia non esiste o non ha proprietà.
        """
        self.c.execute('''
            SELECT p.id_proprieta, p.indirizzo, p.prezzo, p.stato, p.id_agente
            FROM proprieta p
            JOIN agenti a ON p.id_agente = a.id_agente
            WHERE a.id_agenzia = ?
        ''', (id_agenzia,))
        prop_agenzia = []
        for riga in self.c.fetchall():
            prop_a = Proprieta(id_proprieta=riga["id_proprieta"], indirizzo=riga["indirizzo"], prezzo=riga["prezzo"], stato=riga["stato"], id_agente=riga["id_agente"])
            prop_agenzia.append(prop_a)
        return prop_agenzia
    
    def aggiorna_stato_proprieta(self, id_proprieta: int, nuovo_stato: str) -> None:
        """Aggiorna lo stato di una proprietà.
        
        Parametri
        ---------
        id_proprieta : int
            L'ID della proprietà da aggiornare
        nuovo_stato : str
            Il nuovo stato (es. "Venduto", "In affitto")
            
        Comportamento
        -------------
        Aggiorna il campo stato della proprietà specificata.
        Se la proprietà non esiste, non fa nulla.
        """
        self.c.execute('''
            UPDATE proprieta SET stato = ?
            WHERE id_proprieta = ?
                ''', (nuovo_stato, id_proprieta))
        self.conn.commit()
    
    def get_best_agente_per_agenzia(self) -> dict:
        """Trova l'agente con più proprietà per ogni agenzia.
        
        Ritorno
        -------
        dict
            Dizionario con id_agenzia come chiave e un oggetto Agente come valore.
            L'agente restituito è quello con il maggior numero di proprietà gestite.
            Se ci sono più agenti con lo stesso numero massimo di proprietà,
            ne restituisce uno qualsiasi.
            
        Esempio
        -------
        {
            1: Agente(id_agente=101, nome="Mario Rossi", email="mario@example.com", id_agenzia=1),
            2: Agente(id_agente=205, nome="Laura Bianchi", email="laura@example.com", id_agenzia=2)
        }
        """
        agenti_migliori = {}
        self.c.execute('''
            SELECT a.id_agenzia, a.id_agente, a.nome, a.email, COUNT(p.id_proprieta) as num_proprieta
            FROM agenti a
            LEFT JOIN proprieta p ON a.id_agente = p.id_agente
            GROUP BY a.id_agenzia, a.id_agente
            ORDER BY a.id_agenzia, num_proprieta DESC
        ''')
        for riga in self.c.fetchall():
            id_agenzia = riga["id_agenzia"]
            if id_agenzia not in agenti_migliori:
                agente = Agente(id_agente=riga["id_agente"], nome=riga["nome"], email=riga["email"], id_agenzia=riga["id_agenzia"])
                agenti_migliori[id_agenzia] = agente
        return agenti_migliori
    
    def close(self) -> None:
        """Chiude la connessione al database.
        
        Comportamento
        -------------
        Chiude la connessione SQLite per liberare le risorse.
        Dovrebbe essere chiamato quando si è finito di usare il gestore.
        """
        self.conn.close()