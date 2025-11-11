import os
from glob import glob
from PIL import Image, ImageEnhance

# === Variáveis ===

divisoes = ["train", "valid", "test"]
datasetPath = "./dataset/3"
dark_factor = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
bright_factor = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]

# === Funções ===

def loadLabels(lp):
  with open(lp, "r") as f:
    return f.read().strip().splitlines()

def saveLabels(lines, lp):
  with open(lp, "w") as f:
    for line in lines:
      f.write(line + "\n")

def invertLabelLines(lines):
  fixed = []

  for line in lines:
    parts = line.strip().split()

    match len(parts):
      case 5:
        classe, x, y, w, h = parts
        fixed.append(f"{classe} {1.0 - float(x)} {y} {w} {h}")
      
      case 9:
        classe, x1, y1, x2, y2, x3, y3, x4, y4 = parts
        fixed.append(f"{classe} {1.0 - float(x1)} {y1} {1.0 - float(x2)} {y2} {1.0 - float(x3)} {y3} {1.0 - float(x4)} {y4}")
  
  return fixed

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
      
      image = Image.open(imagePath).convert("RGB")

      versions = {
        "original": [image, labelLines],
        "espelhada": [image.transpose(Image.FLIP_LEFT_RIGHT), invertLabelLines(labelLines)]
      }

      for name, [img, labels] in versions.items():
        newName = f"{imageName}_{name}"

        img.save(os.path.join(imagesDir, newName + ".jpg"))
        saveLabels(labels, os.path.join(labelsDir, newName + ".txt"))

        for i, darkness in enumerate(dark_factor):
          darkName = f"{newName}_dark_{i}"
          darkImg = ImageEnhance.Brightness(img).enhance(darkness)
          darkImg.save(os.path.join(imagesDir, darkName + ".jpg"))
          saveLabels(labels, os.path.join(labelsDir, darkName + ".txt"))
        
        for i, brightness in enumerate(bright_factor):
          brightName = f"{newName}_bright_{i}"
          brightImg = ImageEnhance.Brightness(img).enhance(brightness)
          brightImg.save(os.path.join(imagesDir, brightName + ".jpg"))
          saveLabels(labels, os.path.join(labelsDir, brightName + ".txt"))

print("✅ Dataset aumentado com sucesso dentro das pastas train, valid e test.")