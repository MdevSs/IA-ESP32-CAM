import os
import cv2
import requests
import numpy as np
from ultralytics import YOLO

def run_capture_inference(
    url="http://192.168.15.110/capture", 
    model_paths=None
):
    if model_paths is None:
        model_paths = [
            r"c:\github\IA-ESP32-CAM\models\bm\best.pt",  # modelo 1
            r"c:\github\IA-ESP32-CAM\models\ct\best.pt",  # modelo 2
        ]
    
    models = []
    for path in model_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Modelo não encontrado em: {path}")
        models.append(YOLO(path))

    while True:
        try:
            # requisita uma imagem
            resp = requests.get(url, timeout=5)
            img_array = np.frombuffer(resp.content, np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is None:
                print("Falha ao decodificar frame")
                continue

            annotated_frame = frame.copy()

            # roda inferência em cada modelo
            for model in models:
                results = model(frame)
                annotated_frame = results[0].plot()  # só chama o plot
                print(results[0].boxes)

                # if(results[0].boxes>1):
                #   requisição para o backend

            # mostra na tela
            cv2.imshow("Inferência ESP32-CAM (/capture)", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        except Exception as e:
            print("Erro ao capturar imagem:", e)
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_capture_inference()
