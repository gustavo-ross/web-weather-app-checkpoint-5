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
            url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
            try:
                resposta = requests.get(url)
                if resposta.status_code == 200:
                    clima = resposta.json()

                    fuso = clima['timezone']
                    nascer_sol = datetime.utcfromtimestamp(clima['sys']['sunrise'] + fuso).strftime('%H:%M')
                    por_sol = datetime.utcfromtimestamp(clima['sys']['sunset'] + fuso).strftime('%H:%M')
                    
                    cidade_formatada = f"{clima['name']}, {clima['sys']['country']}"
                    historico = salvar_historico(cidade_formatada)

                    main_weather = clima['weather'][0]['main']
                    icone = clima['weather'][0]['icon']

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

                else:
                    erro = "Cidade não encontrada! Tente novamente."
            except requests.exceptions.RequestException:
                erro = "Não foi possível conectar ao servidor de clima."

    return render_template("index.html", clima=clima, erro=erro, bg_image=bg_image, nascer_sol=nascer_sol, por_sol=por_sol, historico=historico)

if __name__ == "__main__":
    app.run(debug=True)