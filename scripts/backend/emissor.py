import socket as skt
import time

def cliente_semaforo(dados_veiculos):
  host = "localhost"
  porta = 12346
  mensagem = f"[{",".join(map(str, dados_veiculos))}]".encode("utf-8")

  try:
    with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as s:
      print("Enviando dados...")
      s.connect((host, porta))

      while True:
        s.sendall(mensagem)
        print(f"Dados enviados: {mensagem}")
        time.sleep(5)
  except ConnectionRefusedError:
    print(f"({host}:{porta}) não está ativo.")

cliente_semaforo([5, 12, 3, 1])