import os
import cv2
import ultralytics
from pathlib import Path

def ifc_video(ip, op):
  if not os.path.exists(ip):
    return print(f"Arquivo de vídeo [{ip}] não encontrado.")

  model = ultralytics.YOLO("./models/best.pt")

  cap = cv2.VideoCapture(ip)

  fcc = cv2.VideoWriter_fourcc(*"mp4v")
  fps = cap.get(cv2.CAP_PROP_FPS)
  res = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))]

  os.makedirs(os.path.dirname(op), exist_ok=True)
  out = cv2.VideoWriter(op, fcc, fps, res)

  while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
      break

    results = model(frame)
    annotated_frame = results[0].plot(conf=True)

    out.write(annotated_frame)
    cv2.imshow("Video Detection - Pressione 'q' para sair", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

  out.release()
  cap.release()
  cv2.destroyAllWindows()
  print(f"Vídeo salvo em: {op}")

def ifc_image(ip, op, model_path="./models/best.pt", show=False):
  """
  Faz inferência em uma imagem ou em todas as imagens de uma pasta.
  - ip: caminho para arquivo de imagem ou pasta de imagens.
  - op: caminho de saída (arquivo para uma imagem, ou pasta para múltiplas).
  - model_path: caminho para o .pt do modelo.
  - show: se True, exibe cada imagem anotada na tela.
  """
  model = ultralytics.YOLO(model_path)

  ip_path = Path(ip)
  op_path = Path(op)

  # Se ip é arquivo único
  if ip_path.is_file():
    if not op_path.parent.exists():
      os.makedirs(op_path.parent, exist_ok=True)

    img = cv2.imread(str(ip_path))
    if img is None:
      return print(f"Arquivo de imagem [{ip}] não pôde ser lido.")

    results = model(img)
    annotated = results[0].plot(conf=True)
    cv2.imwrite(str(op_path), annotated)
    if show:
      cv2.imshow("Image Detection - Pressione qualquer tecla para fechar", annotated)
      cv2.waitKey(0)
      cv2.destroyAllWindows()

    print(f"Imagem anotada salva em: {op_path}")
    return

  # Se ip é pasta, processa todos os arquivos de imagem comuns
  if ip_path.is_dir():
    if not op_path.exists():
      os.makedirs(op_path, exist_ok=True)

    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
    files = [p for p in ip_path.iterdir() if p.suffix.lower() in exts and p.is_file()]
    if not files:
      return print(f"Nenhuma imagem encontrada em: {ip}")

    for file in files:
      img = cv2.imread(str(file))
      if img is None:
        print(f"Pular arquivo inválido: {file.name}")
        continue

      results = model(img)
      annotated = results[0].plot(conf=True)
      out_file = op_path / file.name
      cv2.imwrite(str(out_file), annotated)
      if show:
        cv2.imshow(f"Anotado: {file.name}", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
          cv2.destroyAllWindows()
          print("Exibição interrompida pelo usuário.")
          break

      print(f"{file.name} -> salvo em {out_file}")

    if show:
      cv2.destroyAllWindows()

    print(f"Processamento concluído. Saída em: {op_path}")
    return

  print(f"Caminho de entrada [{ip}] não encontrado ou inválido.")

if __name__ == "__main__":
  while True:
    print("Escolha o tipo de inferência:")
    print("1. Imagem (arquivo único ou pasta)")
    print("2. Vídeo")
    print("0. Sair")
    escolha = input("Opção [1/2/0]: ").strip()

    if escolha == "0":
      print("Encerrando.")
      break

    if escolha == "1":
      ip = input("Caminho da imagem ou pasta de imagens: ").strip()
      default_op = "./inference/output"
      if Path(ip).is_file():
        suggested = os.path.join(default_op, Path(ip).stem + "_annotated" + Path(ip).suffix)
      else:
        suggested = default_op
      op = input(f"Caminho de saída (arquivo ou pasta) [{suggested}]: ").strip() or suggested
      show = input("Exibir imagens durante o processamento? [s/N]: ").strip().lower() == "s"
      ifc_image(ip, op, model_path="./models/best.pt", show=show)
      continue

    if escolha == "2":
      ip = input("Caminho do vídeo: ").strip()
      suggested = "./inference/output/output.mp4"
      op = input(f"Caminho de saída (arquivo) [{suggested}]: ").strip() or suggested
      ifc_video(ip, op)
      continue

    print("Opção inválida, tente novamente.")