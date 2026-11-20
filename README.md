# PetCareNS
Progetto universitario - Alessandro Albuzzi - Pet Care No Stress. 
Prototipo in Python e SQLite per una startup che aiuta i clienti nella ricerca e organizzazione di servizi a domicilio per gli animali domestici.


Sequenza di esecuzione:
    #1 py db_init.py: Per inizializzare il database nella cartella db;
    #2 py crea_random_csv.py: Per creare i csv delle entità nella cartella csv;
    #3 py etl.py: Per lanciare la pipeline ETL che legge i csv, pulisce e trasforma i dati e li salva nel db;
    #4 py -m streamlit run dashboard.py: Per lanciare la dashboard interattiva.