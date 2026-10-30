# D-ND Physics Lab

**Esplorare come un’occorrenza di ricerca cambia il campo delle domande,
delle relazioni e delle competenze.** Il compagno pubblico del Lab di fisica
rigenerativo sviluppato in MM-DND da Graziano Guiducci.

[Aprire il Lab attuale](https://d-nd.com/ai-lab) · [English](README.md) ·
[Guida al corpus](docs/CORPUS.md) · [Architettura](docs/ARCHITECTURE.md)

Il Lab riceve il campo presente, forma un’attenzione temporanea e registra una
risultante completa. Quando ciò che accade trasforma il riconoscimento, quella
trasformazione può partecipare come competenza al campo successivo. La storia
esatta resta raggiungibile; l’attenzione non deve contenere tutto l’archivio.

Qui sono disponibili strumenti funzionanti per leggere e verificare il corpus
pubblico, una spiegazione dei meccanismi correnti, un esempio sintetico e gli
esperimenti storici. Ricercatore operativo, sorgenti private e controlli
amministrativi restano in MM-DND. Gli strumenti leggono la proiezione già
pubblica senza avviare il laboratorio.

## Provare il lettore offline

Serve Python 3.11 o successivo. Dalla cartella del repository clonato:

```bash
git clone https://github.com/GrazianoGuiducci/dnd-lab-physics.git
cd dnd-lab-physics
python -m physics_lab summary examples/synthetic-corpus.json
python -m physics_lab event examples/synthetic-corpus.json --index 2
python -m physics_lab trace examples/synthetic-corpus.json --index 2
python -m physics_lab report examples/synthetic-corpus.json --output esempio.html
```

Aprire `esempio.html` nel browser. Le due occorrenze mostrano un contatto
registrato: sono sintetiche e non costituiscono misure del Lab. I record
conservano lingua e forma sorgente; il lettore non aggiunge una traduzione
automatica. Non servono account, chiavi API, pacchetti aggiuntivi o Docker.

## Leggere il corpus reale

```bash
python -m physics_lab fetch --output corpus.json
python -m physics_lab verify corpus.json
python -m physics_lab summary corpus.json
python -m physics_lab event corpus.json --index 1
python -m physics_lab report corpus.json --output corpus.html
```

Solo `fetch` accede alla rete, mediante una richiesta in lettura alla
proiezione pubblica HTTPS. Conserva i byte esatti e una ricevuta SHA-256.
Gli altri comandi lavorano sul file locale. Un file già esistente resta
preservato; per un’altra acquisizione si sceglie un nome diverso.

Nel controllo del **30 ottobre 2026** il corpus conteneva 726 occorrenze;
l’ultima aveva data 24 settembre. La [ricevuta](docs/VALIDATION_2026-10-30.md)
identifica questo campione e il contatto registrato E726 → E018.

## Comprendere risultante, memoria e prova

Un’**occorrenza** si apre e si completa una volta. La **risultante** conserva
la forma in cui è accaduta. Gli effetti sul campo e sulla memoria restano
distinti: una relazione può aprirsi, conservarsi, raffreddarsi o non lasciare
residuo attivo. Raffreddare permette a una forma di uscire dall’attenzione,
mantenendone la storia recuperabile.

La prima impressione e l’interrogazione autologica possono trasformare ciò che
il Lab diventa capace di riconoscere. Una competenza conserva questa capacità,
senza imporre al seguito la ripetizione della conclusione precedente. Il
termine dell’occorrenza lascia aperto il campo delle possibilità.

Le registrazioni rendono il percorso ispezionabile. La validità di
un’affermazione fisica richiede sorgenti, strumenti, controlli, misure e
possibili controprove pertinenti. Un checksum verifica l’identità dei byte;
un contatto registrato non dimostra da solo un beneficio causale.

## Raggiungere le diverse superfici

| Superficie | Funzione |
| --- | --- |
| **MM-DND** | Implementazione rigenerativa, sorgenti private, depositi, memoria e controlli del Lab operativo. |
| **[AI Lab](https://d-nd.com/ai-lab)** | Workspace pubblico, occorrenze, corpus e lettura con THIA. |
| **dnd-lab-physics** | Documentazione pubblica, strumenti offline, esempi e pacchetto storico. |
| **[D-ND_LAB](https://github.com/GrazianoGuiducci/D-ND_LAB)** | Motore installabile separato, con il proprio dominio physics e un bootstrap storico. |

Il Lab rigenerativo è indipendente dal vecchio orchestratore D-ND_LAB.
La [guida di compatibilità](docs/DND_LAB_COMPATIBILITY.md) rende esplicita la
genealogia e corregge il precedente percorso d’installazione. Le cartelle
`domain/` e `tools/exp_*.py` mantengono il pacchetto di maggio; non sono il
prompt corrente o una nuova convalida scientifica delle sue affermazioni.

Il sistema comprende anche l'operatore umano, Codex come assistente situato,
le scelte sui modelli e sui controlli, e il ritorno osservabile degli interventi.
Rigenerazione scientifica, manutenzione e relazione umana sono circuiti connessi,
descritti nell'[architettura](docs/ARCHITECTURE.md#operator-situated-assistant-and-operational-controls).
Il corpus pubblico rende leggibile una parte di questa relazione complessiva.

Nel seguito del 30 ottobre, la correzione del confine di esportazione ha reso
pubbliche tutte le 729 occorrenze già depositate, con ultima occorrenza del
25 settembre. Un riferimento sorgente riservato in E727 è sostituito nella
vista pubblica con una dichiarazione esplicita; il deposito originale rimane
intatto. La pubblicazione non ha avviato un nuovo ciclo. Identità e confronto
sono nella [ricevuta di verifica](docs/VALIDATION_2026-10-30.md).

La documentazione tecnica collegata è in inglese:
[architettura](docs/ARCHITECTURE.md), [comandi](docs/CORPUS.md),
[ricerca e prove](docs/RESEARCH.md), [fonti](docs/SOURCES.md),
[contributi](CONTRIBUTING.md), [privacy e licenze](docs/PRIVACY_AND_LICENSE.md).

## Licenza e citazione

Codice e documentazione conservano la [licenza MIT](LICENSE) esistente.
Il corpus scaricato mantiene i diritti delle proprie sorgenti: la MIT del
repository non lo rilicenzia. Per il software è disponibile
[CITATION.cff](CITATION.cff).

Il preprint matematico **Paper Zero**, revisione del 28 ottobre 2026, conserva
il proprio DOI [10.5281/zenodo.23735742](https://doi.org/10.5281/zenodo.23735742)
e la licenza specifica CC BY 4.0, distinti dal software e dai depositi storici.
