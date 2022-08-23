import socket as sk
import time
import os

message = "get pdf_server.pdf"

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ("localhost", 10000)
buffer = 4096


command = message.split(" ")[0]
arg = "" if len(message.split(" ")) == 1 else message.split(" ")[1]

try:
        
    print("sending %s" % message)
    time.sleep(2)
    sent = sock.sendto(message.encode(), server_address)
    
    
    
    ## LIST
    if command == "list":
        data, server = sock.recvfrom(buffer)
        print("received message:\n\n%s\n" % data.decode("utf8"))

            
        
    ## GET
    elif command == "get":
        data, server = sock.recvfrom(buffer) # il server comunica se il file esiste
        
        if data.decode("utf8") == "ok": # il file esiste
            f = open(arg,'wb')

            try:
                npack = 0

                # Ricevo i pacchetti, contandoli
                data, server = sock.recvfrom(buffer)
                while data:
                    npack += 1
                    print("downloading...")
                    f.write(data)
                    sock.settimeout(2)
                    data, server = sock.recvfrom(buffer)
                    
            except sk.timeout:   
                print("closing file")
                f.close()
                sock.settimeout(None)
                
                # Controllo che siano stati ricevuti tutti i pacchetti
                sent = sock.sendto(str(npack).encode(), server_address)
                data, server = sock.recvfrom(buffer)
                if data.decode("utf8") == "ok":
                    print("\nDownload completed successfully!\n")
                else:
                    print(data.decode("utf8"))

        else : # il file non esiste
            print(data.decode("utf8"))
            
            
            
            
    ## PUT 
    elif command == "put":
        
        try:
            f = open(arg, "rb")
            sent = sock.sendto("ok".encode(), server_address)

            npack = (os.path.getsize(f.name) / buffer).__ceil__()
    
            cont = f.read(buffer)
            while cont:
                print("sending...")
                sent = sock.sendto(cont, server_address)
                cont = f.read(buffer)
            f.close()
            time.sleep(3)
            
            # comunico al server quanti pacchetti deve aver ricevuto
            sent = sock.sendto(str(npack).encode(), server_address)
            data, server = sock.recvfrom(buffer)
            if data.decode("utf8") == "ok":
                print("\nUpload completed successfully!\n")
            else:
                print(data.decode("utf8"))
        except FileNotFoundError:
            print("\nError: %s is not a file in your directory" %  arg)
            sent = sock.sendto("error: file not available".encode(), server_address)
            
    

            
except Exception as info:
    print(info)
finally:
    print("closing socket")
    sock.close()    

