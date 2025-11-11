# UrbanFlow  

## Sobre o Projeto
**Urban Flow** é um sistema de inteligência artificial baseado no **YOLOv8** e **PyTorch** para otimizar o funcionamento de semáforos em avenidas movimentadas. O projeto analisa o fluxo de veículos por meio de câmeras e ajusta os tempos dos semáforos em tempo real, reduzindo congestionamentos e melhorando a mobilidade urbana.  

## Tecnologias Utilizadas
- **Python** 
- **YOLOv8** (para detecção de veículos)  
- **PyTorch** (para treinamento e inferência do modelo)  
- **OpenCV** (para processamento de imagens)  
- **Flask/FastAPI** (para API backend)  
- **SQLite/PostgreSQL** (para armazenar dados do fluxo)  

## Estrutura do Projeto
```
urban-flow/
│── models/                # Modelos treinados YOLOv8
│── data/                  # Dados de treinamento e testes
│   ├── Train/		    # Dados para o treino
│   │   ├── images
│   │   ├── labels
│   ├── Validation/	    # Dados para validação
│       ├── images
│       ├── loabels
│── data.yaml/             # Localização das imagens, assim como o nome de suas classes
│── src/                   # Código-fonte principal
│   ├── detection.py       # Script de detecção de veículos
│   ├── traffic_control.py # Lógica de controle de semáforos
│   ├── api.py             # API para comunicação com o sistema
│── notebooks/             # Jupyter Notebooks para testes e análise
│── README.md              # Documentação do projeto
```

## Como Rodar o Projeto

### 1. Clone este repositório
```bash
git clone https://github.com/seu-usuario/urban-flow.git
cd urban-flow
```

### 2. Crie um ambiente virtual e instale as dependências
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Baixe e configure o modelo YOLOv8
```bash
mkdir models
cd models
wget https://github.com/ultralytics/assets/releases/download/v8/yolov8n.pt
```
Se estiver no Windows, utilize:  
```powershell
curl -o yolov8n.pt https://github.com/ultralytics/assets/releases/download/v8/yolov8n.pt
```

### 4. Execute o sistema  
```bash
python src/api.py
```

## Resultados Esperados
✔️ Redução no tempo de espera em semáforos 
✔️ Melhor fluidez no trânsito urbano  
✔️ Análise e previsão do fluxo de veículos 

## Equipe
- **Cayki Santos Gondim** (Programação)
- **Leandro Ramos de Oliveira** (Programação)
- **Juan Ramon Garcia Taeño Filho** (Programação)

## Licença
Este projeto é de código aberto sob a licença MIT.