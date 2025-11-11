import os
from glob import glob

# === Variáveis ===

divisoes = ["train", "valid", "test"]
datasetPath = "./dataset/2"

# === Funções ===

def loadLabels(lp):
  with open(lp, "r") as f:
    return f.read().strip().splitlines()

# === Main ===

for divisao in divisoes:
  imagesDir = os.path.join(datasetPath, divisao, "images")
  labelsDir = os.path.join(datasetPath, divisao, "labels")
  
  imagesPath = glob(os.path.join(imagesDir, "*.jpg"))

  for imagePath in imagesPath:
    imageName = os.path.basename(imagePath).replace(".jpg", "")
    labelPath = os.path.join(labelsDir, imageName + ".txt")

    if os.path.exists(labelPath):
      labelLines = loadLabels(labelPath)

      if len(labelLines) == 0:
        os.remove(labelPath)
        os.remove(imagePath)
        print(f"{os.path.basename(imagePath)} removido")

print("✅ Concluído!")