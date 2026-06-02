# 🌤️ Web Weather App (Checkpoint 5)

O Web Weather App é uma aplicação web dinâmica desenvolvida como projeto de conclusão do Bloco 3 da Formação Python & Django. O sistema integra uma interface web moderna (estilo *Glassmorphism*) a dados climáticos em tempo real consumidos diretamente da API global do OpenWeatherMap.

O projeto consolida conceitos avançados de desenvolvimento Full-Stack, como o consumo de APIs REST, manipulação de rotas dinâmicas, arquitetura modular de serviços, leitura/escrita em ficheiros JSON e renderização reativa no front-end com herança de templates.

Documentação da API (5 Day / 3 Hour Forecast): https://openweathermap.org/forecast5

---

## 🚀 Funcionalidades

* **Busca Global em Tempo Real:** Permite pesquisar as condições climáticas de qualquer cidade do mundo.
* **Dashboard Detalhado:** Exibe o nome da cidade, país, descrição do clima, temperatura atual, umidade, velocidade do vento, sensação térmica e as horas do nascer e pôr do sol.
* **Lógica de Previsão 24h:** O sistema processa blocos de previsão futuros para calcular com precisão a verdadeira Temperatura Máxima e Mínima do dia.
* **Backgrounds Dinâmicos:** A imagem de fundo e os componentes reagem automaticamente ao clima local (Chuva, Neve, Céu Limpo de Dia/Noite, etc.).
* **Histórico Inteligente:** O sistema memoriza as últimas 3 cidades procuradas pelo utilizador com integração de clique rápido.
* **Tratamento de Erros:** Exibe alertas amigáveis caso a cidade não seja encontrada.
* **Interface Responsiva:** Design moderno escuro adaptável a dispositivos móveis e desktops.

---

## 🛠️ Tecnologias Utilizadas

### **Back-end**
* **Python** (Linguagem base)
* **Flask** (Microframework para rotas e servidor web)
* **Requests** (Biblioteca HTTP para consumo da API externa)
* **JSON & OS** (Para persistência de dados do histórico)
* **Datetime** (Para conversão de formatos *Unix timestamp* e fusos horários)

### **Front-end**
* **HTML5**
* **Bootstrap 5** (Estilização responsiva via CDN)
* **Jinja2** (Motor de templates para lógica, herança de blocos e exibição dinâmica)
* **Design System Customizado:** Implementação de efeitos visuais *Glassmorphism* usando CSS nativo e assets vetoriais (.SVG).

---

## 📁 Estrutura do Projeto

A arquitetura foi escalada para o padrão modular, separando a lógica de negócio dos componentes visuais:

```text
/weather_app
├── venv/             # Ambiente virtual Python
├── app.py            # Servidor Flask e roteador principal
├── clima.py          # Serviço de integração com a API e cálculos meteorológicos
├── historico.py      # Serviço de gestão do ficheiro de histórico
├── historico.json    # Ficheiro de persistência de dados (criado automaticamente)
├── static/
│   └── assets/       # Ícones SVG e imagens dinâmicas (.webp) para o front-end
└── templates/
    ├── base.html     # Esqueleto estrutural (Herança Jinja2)
    ├── home.html     # Ecrã inicial (Empty state e histórico)
    └── resultado.html# Dashboard de visualização do clima


---

## 🔧 Como Executar o Projeto

### 1. Clonar o Repositório e Configurar o Ambiente

```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/web-weather-app.git](https://github.com/seu-usuario/web-weather-app.git)
cd web-weather-app

# Crie e ative o ambiente virtual (venv)
python -m venv venv

# Ativação no Linux/macOS:
source venv/bin/activate
# Ativação no Windows:
venv\Scripts\activate

```

### 2. Instalar as Dependências

```bash
pip install flask requests
# ou, se tiver o requirements.txt:
pip install -r requirements.txt

```

### 3. Configurar a Chave da API

1. Aceda ao site oficial do [OpenWeatherMap](https://openweathermap.org/) e crie uma conta gratuita.
2. Copie a chave gerada na secção *My API Keys*.
3. Abra o ficheiro `clima.py` na raiz do projeto e insira a sua chave na variável correspondente:

```python
API_KEY = "SUA_API_KEY_AQUI"

```

### 4. Iniciar o Servidor

```bash
python app.py

```

Aceda a `http://127.0.0.1:5000/` no seu navegador para testar a aplicação.

---

## 🏆 Desafios Implementados (Modo Hardcore)

Para além da estrutura básica do Checkpoint, todos os desafios avançados foram concluídos e aprimorados:

* [x] **Desafio 1:** Interface dinâmica alterando cores e fundos com base nas condições do clima (Imagens `.webp` de alta qualidade acionadas via back-end).
* [x] **Desafio 2:** Exibição do horário do nascer e pôr do sol formatados através do timestamp Unix da API (incluindo cálculo de fuso horário local).
* [x] **Desafio 3:** Inclusão da sensação térmica na interface principal (*feels_like*).
* [x] **Desafio 4:** Histórico de buscas persistente, guardando as últimas 3 cidades pesquisadas num ficheiro `JSON` com atalhos funcionais num clique.
* [x] **Desafio Extra (Arquitetura):** Refatorização completa para módulos separados (`clima.py`, `historico.py`) e transição do endpoint `/weather` para `/forecast` visando calcular máximas e mínimas reais baseadas num ciclo de 24 horas.

```

```