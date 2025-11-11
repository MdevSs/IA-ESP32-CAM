import socket as skt

def servidor_central():
  host = "localhost"
  porta = 12345

  with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as s:
    s.bind((host, porta))
    s.listen()
    print("Servidor central esperando por dados...")
    
    while True:
      con, end = s.accept()

      with con:
        print(f"Conexão recebida de: {end}")

        while True:  
          dados = con.recv(1024).decode("utf-8")

          if not dados:
            break

          vetor = dados
          print(f"Dados recebidos do semáforo {end}: {vetor}")

servidor_central()