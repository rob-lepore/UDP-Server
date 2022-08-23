# Progetto d'esame per il corso di Programmazione di Reti

##### Roberto Lepore - roberto.lepore2@studio.unibo.it - 0000970366

Ho svolto la traccia 2: architettura client-server UDP per trasferimento file.  

## Indicazioni per l'utilizzo

Una volta avviato il server eseguendo il file `Server/serverUDP.py`, si possono mandare richieste eseguendo il file `Client/clientUDP.py` in una seconda console.

Alla prima riga dopo gli import nel file `Client/clientUDP.py` è definita la stringa contente il messaggio da inviare al server. 

Per il comando LIST scrivere `message = "list"`.
Per il comando GET scrivere `message = "get nomefile"`. Inizialmente nomefile può essere sostituito con `file_server_1.txt`, `file_server_2.txt` , `image_server.png`, `pdf_server.pdf`.
Per il comando PUT scrivere `message = "put nomefile"`. Inizialmente nomefile può essere sostituito con `file_client_1.txt`, `file_client_2.txt` , `image_client.png`, `pdf_client.pdf` .

I file presenti sul server sono memorizzati nella cartella `Server/files/`, mentre quelli disponibili sul client sono in `Client/`.
