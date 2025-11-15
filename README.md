[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/SHS1RZPp)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21672963&assignment_repo_type=AssignmentRepo)
# Classwork 2: Gestore di un'Agenzia Immobiliare con OOP e Database

Questo repository è il punto di partenza per l'homework "Gestore Agenzia Immobiliare con OOP e Database".
L'obiettivo è esercitarti con la Programmazione a Oggetti (OOP), le dataclasses, e l'interazione con
database SQLite, sviluppando un sistema completo per gestire agenzie immobiliari, agenti e proprietà.

In questa versione "starter" trovi lo scheletro delle classi da completare e un
setup di test basato su `pytest`.

---

## Cosa devi fare

Implementa le classi e i metodi nel file `immobiliare_manager.py`:

### 1. Dataclasses (già definite, da non modificare):
- `Agenzia`: Rappresenta un'agenzia immobiliare con `id_agenzia`, `nome`, `indirizzo`
- `Agente`: Rappresenta un agente con `id_agente`, `nome`, `email`, `id_agenzia` (FK)
- `Proprieta`: Rappresenta una proprietà con `id_proprieta`, `indirizzo`, `prezzo`, `stato`, `id_agente` (FK)

### 2. Classe `GestoreImmobiliare` (da implementare):

#### Costruttore:
- `__init__(self, db_path: str)`:
  - Crea la connessione al database SQLite
  - Crea le tabelle `agenzie`, `agenti` e `proprieta` se non esistono
  - **Importante**: Definisci PRIMARY KEY e FOREIGN KEY per mantenere l'integrità relazionale

#### Metodi di Inserimento:
- `add_agenzia(self, agenzia: Agenzia)`: Inserisce una nuova agenzia
- `add_agente(self, agente: Agente)`: Inserisce un nuovo agente
- `add_proprieta(self, proprieta: Proprieta)`: Inserisce una nuova proprietà

#### Metodi per Query Complesse:
- `get_proprieta_per_agente(self, id_agente: int) -> list[Proprieta]`:
  - Restituisce tutte le proprietà gestite da un agente specifico
  
- `get_agenti_per_agenzia(self, id_agenzia: int) -> list[Agente]`:
  - Restituisce tutti gli agenti che lavorano per un'agenzia
  
- `get_proprieta_per_agenzia(self, id_agenzia: int) -> list[Proprieta]`:
  - Restituisce tutte le proprietà gestite da un'intera agenzia
  - **Richiede un JOIN** tra le tabelle `proprieta` e `agenti`
  
- `aggiorna_stato_proprieta(self, id_proprieta: int, nuovo_stato: str)`:
  - Aggiorna lo stato di una proprietà (es. da "In vendita" a "Venduto")
  
- `get_best_agente_per_agenzia(self) -> dict`:
  - Restituisce un dizionario con `id_agenzia` come chiave e l'agente con il maggior numero di proprietà come valore
  - Se ci sono più agenti con lo stesso numero massimo di proprietà, restituisce uno qualsiasi di essi

#### Metodo di Chiusura:
- `close(self)`: Chiude la connessione al database

Mantieni le firme esattamente come sopra: i test le importano direttamente.

---

## Requisiti

- Python 3.10 o superiore (consigliato 3.11)
- `pytest` (viene installato da `requirements.txt`)
- SQLite3 (incluso in Python)

---

## Struttura del repository

```
hw2-database-classes/
├── tests/
│   ├── conftest.py                         # Fixtures pytest per i test
│   └── test_immobiliare_manager_public.py  # Test pubblici
├── immobiliare_manager.py                  # FILE DA COMPLETARE
├── requirements.txt                         # Dipendenze per i test
└── README.md
```

---

## Setup locale (consigliato)

1) Naviga nella directory del progetto:

```bash
cd hw2-database-classes
```

2) Crea ed attiva un ambiente virtuale con `uv` (consigliato):

```bash
uv venv  # solo la prima volta
source .venv/bin/activate  # su Linux/macOS
# oppure .venv\Scripts\activate su Windows
```

Da Visual Studio Code, puoi selezionare il virtual environment `.venv` come interprete Python
dalla barra di stato in basso a destra.

3) Installa le dipendenze con `uv`:

```bash 
uv pip install -r requirements.txt  # solo la prima volta
```

4) Esegui i test in locale con `uv`:

```bash
uv run pytest  # ogni volta che vuoi verificare le tue implementazioni
```

Finché non implementi i metodi, vedrai dei fallimenti nei test (FAIL).

---

## Dettagli di implementazione

### Schema del Database

Devi creare tre tabelle con le seguenti strutture (esempio):

**Tabella `agenzie`**:
```sql
CREATE TABLE IF NOT EXISTS agenzie (
    id_agenzia INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    indirizzo TEXT NOT NULL
)
```

**Tabella `agenti`**:
```sql
CREATE TABLE IF NOT EXISTS agenti (
    id_agente INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    id_agenzia INTEGER NOT NULL,
    FOREIGN KEY (id_agenzia) REFERENCES agenzie(id_agenzia)
)
```

**Tabella `proprieta`**:
```sql
CREATE TABLE IF NOT EXISTS proprieta (
    id_proprieta INTEGER PRIMARY KEY,
    indirizzo TEXT NOT NULL,
    prezzo REAL NOT NULL,
    stato TEXT NOT NULL,
    id_agente INTEGER NOT NULL,
    FOREIGN KEY (id_agente) REFERENCES agenti(id_agente)
)
```

### Gestione della Connessione

- Salva la connessione come attributo della classe nel costruttore (`self.conn = sqlite3.connect(...)`)
- Ricorda di fare `commit()` dopo le operazioni di scrittura (INSERT, UPDATE)
- Usa `cursor.execute()` per le query SQL
- Abilita le foreign keys: `PRAGMA foreign_keys = ON`

### Query con JOIN

Per `get_proprieta_per_agenzia`, devi fare un JOIN tra `proprieta` e `agenti`:

```sql
SELECT p.id_proprieta, p.indirizzo, p.prezzo, p.stato, p.id_agente
FROM proprieta p
JOIN agenti a ON p.id_agente = a.id_agente
WHERE a.id_agenzia = ?
```

### Conversione Row → Dataclass

Quando recuperi dati dal database, devi convertire le righe in oggetti dataclass:

```python
rows = cursor.fetchall()
risultato = [Proprieta(id_proprieta=row[0], indirizzo=row[1], 
                       prezzo=row[2], stato=row[3], id_agente=row[4]) 
             for row in rows]
```

### Query Aggregata per Best Agente

Per `get_best_agente_per_agenzia`, devi contare le proprietà per agente e trovare il massimo per agenzia:

```sql
SELECT a.id_agenzia, a.id_agente, a.nome, a.email, COUNT(p.id_proprieta) as num_proprieta
FROM agenti a
LEFT JOIN proprieta p ON a.id_agente = p.id_agente
GROUP BY a.id_agenzia, a.id_agente
ORDER BY a.id_agenzia, num_proprieta DESC
```

Poi, per ogni agenzia, prendi solo l'agente con il numero massimo di proprietà.

---

## Esempio di utilizzo

```python
from immobiliare_manager import Agenzia, Agente, Proprieta, GestoreImmobiliare

# Crea il gestore
gestore = GestoreImmobiliare("real_estate.db")

# Aggiungi un'agenzia
agenzia = Agenzia(id_agenzia=1, nome="Immobiliare Roma", indirizzo="Via Roma 1")
gestore.add_agenzia(agenzia)

# Aggiungi un agente
agente = Agente(id_agente=101, nome="Mario Rossi", 
                email="mario@example.com", id_agenzia=1)
gestore.add_agente(agente)

# Aggiungi una proprietà
proprieta = Proprieta(id_proprieta=1001, indirizzo="Via Garibaldi 10",
                      prezzo=250000.0, stato="In vendita", id_agente=101)
gestore.add_proprieta(proprieta)

# Query: proprietà per agente
proprieta_mario = gestore.get_proprieta_per_agente(101)
print(f"Mario gestisce {len(proprieta_mario)} proprietà")

# Query: tutte le proprietà dell'agenzia (con JOIN)
proprieta_agenzia = gestore.get_proprieta_per_agenzia(1)
print(f"L'agenzia ha {len(proprieta_agenzia)} proprietà in totale")

# Aggiorna stato
gestore.aggiorna_stato_proprieta(1001, "Venduto")

# Best agente per agenzia
best_agenti = gestore.get_best_agente_per_agenzia()
for id_agenzia, agente in best_agenti.items():
    print(f"Agenzia {id_agenzia}: miglior agente è {agente.nome}")

# Chiudi connessione
gestore.close()
```

---

## Come funziona la valutazione

- I test pubblici in `tests/test_immobiliare_manager_public.py` verificano:
  - Creazione corretta delle tabelle con PRIMARY KEY e FOREIGN KEY
  - Inserimento di dati
  - Query semplici (per agente, per agenzia)
  - Query complesse con JOIN
  - Aggiornamento dati
  - Query aggregate (best agente)
  
- L'insegnante può avere test privati aggiuntivi per casi edge

---

## Suggerimenti

### Chiavi Primarie e Esterne
- Definisci sempre `PRIMARY KEY` per gli ID
- Definisci sempre `FOREIGN KEY` per mantenere l'integrità referenziale
- Abilita le foreign keys con `PRAGMA foreign_keys = ON` subito dopo la connessione

### Gestione Errori
- Se una proprietà da aggiornare non esiste, non sollevare eccezioni (silenzioso)
- Se un'agenzia/agente non ha dati, restituisci liste vuote `[]`

### Query Parametrizzate
- Usa sempre parametri con `?` nelle query per evitare SQL injection:
  ```python
  cursor.execute("SELECT * FROM agenzie WHERE id_agenzia = ?", (id_agenzia,))
  ```

### Testing Incrementale
- Implementa un metodo alla volta
- Esegui i test frequentemente per verificare i progressi
- Usa `pytest -v` per output verboso
- Usa `pytest -k "nome_test"` per eseguire test specifici

### Debug del Database
- Puoi ispezionare il database con strumenti come DB Browser for SQLite
- Oppure usa query SQL dirette per verificare i dati:
  ```python
  cursor.execute("SELECT * FROM agenzie")
  print(cursor.fetchall())
  ```

---

## Test Principali

I test verificano:

1. **Struttura**: Importazione dataclasses, creazione tabelle, schema corretto
2. **Inserimento**: Aggiunta di agenzie, agenti, proprietà
3. **Query Semplici**: 
   - `get_proprieta_per_agente` con 0, 1, o più proprietà
   - `get_agenti_per_agenzia` con 0, 1, o più agenti
4. **Query con JOIN**: 
   - `get_proprieta_per_agenzia` che combina dati da più tabelle
   - Filtro corretto per agenzia
5. **Aggiornamento**: 
   - `aggiorna_stato_proprieta` modifica correttamente lo stato
   - Gestione proprietà inesistenti
6. **Query Aggregata**: 
   - `get_best_agente_per_agenzia` trova l'agente top per ogni agenzia
   - Gestione pareggi
7. **Integrità**: Verifica delle relazioni tra entità

---

## Domande frequenti (FAQ)

**Q: Devo modificare le dataclasses?**  
A: No, sono già definite correttamente. Concentrati sull'implementazione di `GestoreImmobiliare`.

**Q: Come gestisco i float per i prezzi?**  
A: SQLite usa il tipo `REAL` per i float. Nei test, usa comparazioni con tolleranza (`abs(a - b) < 0.01`).

**Q: Cosa succede se provo ad aggiungere un agente con id_agenzia inesistente?**  
A: Se hai definito correttamente le FOREIGN KEY, SQLite impedirà l'inserimento. Per i test, assumiamo che i dati siano sempre validi.

**Q: Come testo il mio codice localmente?**  
A: Esegui `uv run pytest` nella directory `hw2-database-classes`. Vedrai quali test passano e quali falliscono.

**Q: Devo gestire le eccezioni?**  
A: Per questo esercizio, non è richiesta gestione esplicita delle eccezioni, tranne per garantire che operazioni su entità inesistenti non causino crash.

---

## Valutazione

La soluzione è considerata corretta se:
- ✅ Tutte le dataclasses sono definite correttamente
- ✅ Le tabelle sono create con PRIMARY KEY e FOREIGN KEY
- ✅ Tutti i metodi di inserimento funzionano
- ✅ Tutte le query semplici restituiscono i dati corretti
- ✅ La query con JOIN (`get_proprieta_per_agenzia`) funziona correttamente
- ✅ L'aggiornamento dello stato funziona
- ✅ La query aggregata (`get_best_agente_per_agenzia`) funziona
- ✅ Tutti i test pubblici passano (`pytest`)

---

Buon lavoro! 💪 Se hai domande, controlla i test per capire esattamente cosa è richiesto.