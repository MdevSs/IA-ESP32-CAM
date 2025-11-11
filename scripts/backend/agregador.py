import socket as skt

def agregador_a1():
  host1 = "localhost"
  porta1 = 12346
  host2 = "localhost"
  porta2 = 12345

  with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as sr:
    sr.bind((host1, porta1))
    sr.listen()
    print("1 esperando por dados...")
    
    while True:
      con, end = sr.accept()

      with con:
        print(f"Conexão recebida de: {end}")

        while True:
          dados = con.recv(1024)
          
          if not dados:
            break

          vetor = dados

          with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as se:
            se.connect((host2, porta2))
            se.sendall(vetor)
            print(f"Dados recebidos: {vetor}")

agregador_a1()