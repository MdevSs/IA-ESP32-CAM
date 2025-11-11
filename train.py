# 100 épocas = 8 h
# Treinamento (ct) = 400
# Treinamento (bm) = 100

# 100 épocas = 0.5 h
# Treinamento (toy) = 100

import torch, ultralytics, os, shutil, gc

def train():
  # Se o computador possuir CUDA, usamos ele.
  if torch.cuda.is_available():
    print("[Using CUDA.]")
    option = "cuda"
  else:
    print("[Using CPU.]")
    option = "cpu"

  # Se o best.pt existir, usamos ele.
  if os.path.exists("./models/best.pt"):
    print("[Using the best model.]")
    model = ultralytics.YOLO("./models/best.pt")
  else:
    print("[Creating a new model.]")
    model = ultralytics.YOLO("./models/yolov8n.pt")

  # Se a pasta anterior existir, apagamos ela.
  if os.path.exists("./models/vehicle-detector"): 
    print("[Deleting old train folder.]")
    shutil.rmtree("./models/vehicle-detector")

  # Parâmetros da CNN.
  model.train(
    name="vehicle-detector",
    project="./models",
    data="./dataset/3/data.yaml",
    device=option,
    epochs=100,
    batch=8,
    imgsz=640,
    cache=False,
    amp=True
  )

  # Se existir o novo best.pt, movemos ele para a pasta models.
  if os.path.exists("./models/vehicle-detector/weights/best.pt"):
    print("[Moving new best model.]")
    shutil.move("./models/vehicle-detector/weights/best.pt", "./models/best.pt")

  # Liberar a RAM.
  del model
  gc.collect()
  torch.cuda.empty_cache()

if __name__ == "__main__":
  train()