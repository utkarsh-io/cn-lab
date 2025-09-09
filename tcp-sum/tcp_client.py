import socket

name = "ADI"

while True:
    val = int(input("Enter Number between 1 and 100: "))
        
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('10.xx.x.xxx', 9999))
    print("Connected to server on port 9999")

    client_socket.sendall((name + "\n").encode())
    client_socket.sendall((str(val) + "\n").encode())

    if(val<=1 or val>=100):
        client_socket.close()
        print("Invalid Number. Server Closed")
        break

    sockfile = client_socket.makefile('r', encoding='utf-8')
    sname = sockfile.readline().strip()
    sval = int(sockfile.readline().strip())

    print(f"Client Name: {name}")
    print(f"Server Name: {sname}")
    print(f"Client Number: {val}")
    print(f"Server Number: {sval}")
    print(f"Sum: {val + sval}")

    sockfile.close()
    client_socket.close()

    again = input("Do you want to continue? (y/n): ").strip().lower()
    if again != "y":
        break
    else:
        print("\n\n")
