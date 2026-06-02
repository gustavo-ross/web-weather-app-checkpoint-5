from flask import Flask, render_template, request
import requests
from datetime import datetime
import json
import os

app = Flask(__name__)
API_KEY = "f82efcfb675400e8fc9ae17a2503eb3d"
ARQUIVO_HISTORICO = "historico.json"

def carregar_historico():
    """Lê o histórico salvo no arquivo JSON."""
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_historico(nova_cidade):
    """Adiciona uma nova cidade ao JSON mantendo apenas as 3 mais recentes."""
    historico = carregar_historico()
    
    if nova_cidade in historico:
        historico.remove(nova_cidade)
        
    historico.insert(0, nova_cidade)
    historico = historico[:3] 
    
    with open(ARQUIVO_HISTORICO, 'w', encoding='utf-8') as f:
        json.dump(historico, f, ensure_ascii=False)
        
    return historico

@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    erro = None
    bg_image = "pré-pesquisa.webp"
    nascer_sol = None
    por_sol = None
    
    historico = carregar_historico()

    if request.method == "POST":
        cidade = request.form.get("cidade")
        if cidade:
            # 1. Trocamos o endpoint para '/forecast'
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
            try:
                resposta = requests.get(url)
                if resposta.status_code == 200:
                    dados = resposta.json()

                    # 2. Separando os dados da cidade e a previsão
                    cidade_info = dados['city']
                    lista_previsao = dados['list']
                    
                    # O clima atual é o bloco de tempo mais recente (o primeiro da lista)
                    clima_atual = lista_previsao[0]

                    # 3. Tratamento de Fuso Horário e Sol
                    fuso = cidade_info['timezone']
                    nascer_sol = datetime.utcfromtimestamp(cidade_info['sunrise'] + fuso).strftime('%H:%M')
                    por_sol = datetime.utcfromtimestamp(cidade_info['sunset'] + fuso).strftime('%H:%M')
                    
                    # 4. Histórico de Busca
                    cidade_formatada = f"{cidade_info['name']}, {cidade_info['country']}"
                    historico = salvar_historico(cidade_formatada)

                    # 5. Background Dinâmico (Lido do clima atual)
                    main_weather = clima_atual['weather'][0]['main']
                    icone = clima_atual['weather'][0]['icon']

                    if main_weather == 'Clear':
                        bg_image = "clear-day.webp" if icone.endswith('d') else "clear-night.webp"
                    elif main_weather == 'Clouds':
                        bg_image = "clouds.webp"
                    elif main_weather == 'Rain':
                        bg_image = "rain.webp"
                    elif main_weather == 'Drizzle':
                        bg_image = "drizzle.webp"
                    elif main_weather == 'Thunderstorm':
                        bg_image = "thunderstorm.webp"
                    elif main_weather == 'Snow':
                        bg_image = "snow.webp"
                    else:
                        bg_image = "Atmosphere.webp"

                    # 6. A Mágica da Máxima e Mínima
                    # Pega os 8 primeiros blocos (3h * 8 = 24 horas)
                    proximas_24h = lista_previsao[:8]
                    # Busca o maior e o menor valor de temperatura dentro dessas 24h
                    temp_max_dia = max(item['main']['temp_max'] for item in proximas_24h)
                    temp_min_dia = min(item['main']['temp_min'] for item in proximas_24h)

                    # 7. Empacotando tudo no formato que o Front-end já espera
                    clima = {
                        'name': cidade_info['name'],
                        'sys': {'country': cidade_info['country']},
                        'weather': clima_atual['weather'],
                        'main': {
                            'temp': clima_atual['main']['temp'],
                            'feels_like': clima_atual['main']['feels_like'],
                            'humidity': clima_atual['main']['humidity'],
                            'temp_max': temp_max_dia,
                            'temp_min': temp_min_dia
                        },
                        'wind': clima_atual['wind']
                    }

                else:
                    erro = "Cidade não encontrada! Tente novamente."
            except requests.exceptions.RequestException:
                erro = "Não foi possível conectar ao servidor de clima."

    return render_template("index.html", clima=clima, erro=erro, bg_image=bg_image, nascer_sol=nascer_sol, por_sol=por_sol, historico=historico)

if __name__ == "__main__":
    app.run(debug=True)