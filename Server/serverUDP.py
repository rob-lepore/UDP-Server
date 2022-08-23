import socket as sk
import time
import glob
import os

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = ("localhost",10000)
print("\n\r starting up on %s port %s" % server_address)

sock.bind(server_address)

buffer = 4096

try:

    while True:
        print("\n\r waiting to receive message...\n")
        data, address = sock.recvfrom(buffer)
        print("received message from %s:%s" % address)
        
        message = data.decode("utf8")
        print("->  %s\n" % message)
        command = message.split(" ")[0]
        
        
        
        ## LIST COMMAND
        if command == "list":
            res = " ".join(glob.glob("files/*")).replace("files\\", "")
            sent = sock.sendto(res.encode(), address)
            print("sent %s bytes back to %s" % (sent, address))
            
            
            
            
            
        ## GET COMMAND
        # Funziona con file di dimensioni maggiori al buffer
        elif command == "get":
            
            # Controllo che il file esista
            try:
                f = open("files/" + message.split(" ")[1], "rb")
                sent = sock.sendto("ok".encode(), address)

                # Calcolo il numero di pacchetti da inviare
                npack = (os.path.getsize(f.name) / buffer).__ceil__()

                # Invio i pacchetti                
                cont = f.read(buffer)
                while cont:
                    sent = sock.sendto(cont, address)
                    print("sent %s bytes back to %s" % (sent, address))
                    cont = f.read(buffer)
                f.close()
                
                # Il client comunica quanti pacchetti ha ricevuto
                nreceived, address = sock.recvfrom(buffer)
                if int(nreceived.decode("utf8")) == npack:
                    print("Success!\n")
                    sent = sock.sendto("ok".encode(), address)
                else:
                    print("Error: not all packages were received\n")
                    sent = sock.sendto("error: not all packeges were received".encode(), address)
                
            except FileNotFoundError : # il file non esiste
                print("Error: requested file not found\n")
                sent = sock.sendto("error: file not found".encode(), address)
            
            
            
        ## PUT COMMAND
        elif command == "put":
            
            data, address = sock.recvfrom(buffer)
            if data.decode("utf8") == "ok":
                f = open("files/" + message.split(" ")[1],'wb')
                
                try:
                    npack = 0
                    
                    # Ricevo i pacchetti, contandoli
                    data, address = sock.recvfrom(buffer)
                    while data:
                        npack += 1
                        print("received %s bytes from %s" % (len(data), address))
                        f.write(data)
                        sock.settimeout(2)
                        data, server = sock.recvfrom(buffer)
                        
                except sk.timeout:
                    sock.settimeout(None)
                    print("closing file")
                    f.close()
                    
                    # Il client comunica quanti paccheti devono essere arrivati
                    ntotal, address = sock.recvfrom(buffer)
                    if int(ntotal.decode("utf8")) == npack:
                        print("Success!\n")
                        sent = sock.sendto("ok".encode(), address)
                    else:
                        print("Error: not all packages were received\n")
                        sent = sock.sendto("error: not all packeges were received".encode(), address)                
            else:
                print("Error: file not available\n")
                

        ## UNKOWN MESSAGE
        else: 
            print("Unkown message")
        
            
            
except Exception as info:
    print(info)
    sent = sock.sendto("server error".encode(), address)
    print("sent %s bytes back to %s" % (sent, address))