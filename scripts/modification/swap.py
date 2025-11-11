import os
from glob import glob

# === Variáveis === #

divisoes = ["train", "valid", "test"]
datasetPath = "./dataset/1"
classes = ["3.0", "1.0"]

# == Funções == #

def readLabels(lp):
  with open(lp, "r") as f:
    return f.read().strip().splitlines()
  
def writeLabels(lp, lines):
  with open(lp, "w") as f:
    f.write("\n".join(lines))

# === Main === #

for divisao in divisoes:
  labelsDir = os.path.join(datasetPath, divisao, "labels")
  labelsPath = glob(os.path.join(labelsDir, "*.txt"))

  for labelPath in labelsPath:
    modified = False
    newLines = []
    lines = readLabels(labelPath)

    for line in lines:
      parts = line.split()

      if len(parts) == 5 and parts[0] == classes[0]:
        newLines.append(f"{classes[1]} {parts[1]} {parts[2]} {parts[3]} {parts[4]}")
        modified = True
      else:
        newLines.append(line)

    writeLabels(labelPath, newLines)

    if modified:
      print(f"Modificado: {os.path.basename(labelPath)}")
    else:
      print(f"Não modificado: {os.path.basename(labelPath)}")


print("✅ Modificações feitas.")