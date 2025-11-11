import os
from glob import glob

# == Variáveis == #

divisoes = ["train", "valid", "test"]
datasetPath = "./dataset/3"

# == Funções == #

def readLabels(lp):
  with open(lp, "r") as label:
    return label.read().strip().splitlines()
  
def writeLabels(lp, lines):
  with open(lp, "w") as label:
    label.write("\n".join(lines))

# == Main == #

for divisao in divisoes:
  labelsDir = os.path.join(datasetPath, divisao, "labels")
  labelsPath = glob(os.path.join(labelsDir, "*.txt"))

  for labelPath in labelsPath:
    newLines = []

    lines = readLabels(labelPath)
    
    for line in lines:
      modified = False
      parts = [float(word) for word in line.split()]

      if len(parts) == 9:
        classe = parts[0]
        coords = parts[1:]
        xs = parts[1::2]
        ys = parts[2::2]
        x_min = min(xs)
        y_min = min(ys)
        x_max = max(xs)
        y_max = max(ys)
        cX = (float(x_min) + float(x_max)) / 2
        cY = (float(y_min) + float(y_max)) / 2
        w = float(x_max) - float(x_min)
        h = float(y_max) - float(y_min)
        newLines.append(f"{(classe)} {cX} {cY} {w} {h}")
        modified = True
      else:
        newLines.append(line)

      if modified:
        print(f"Modificado: {os.path.basename(labelPath)}.")
      else:
        print(f"Não modificado: {os.path.basename(labelPath)}.")

    writeLabels(labelPath, newLines)

print("Transformação concluída.")