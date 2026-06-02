import requests
from datetime import datetime

API_KEY = "f82efcfb675400e8fc9ae17a2503eb3d"

def buscar_dados_clima(cidade):
    """Faz a chamada para a API e retorna um dicionário organizado."""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()

            cidade_info = dados['city']
            lista_previsao = dados['list']
            clima_atual = lista_previsao[0]

            fuso = cidade_info['timezone']
            nascer_sol = datetime.utcfromtimestamp(cidade_info['sunrise'] + fuso).strftime('%H:%M')
            por_sol = datetime.utcfromtimestamp(cidade_info['sunset'] + fuso).strftime('%H:%M')
            cidade_formatada = f"{cidade_info['name']}, {cidade_info['country']}"

            # Definindo o Background
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

            # Calculando Máximas e Mínimas (24h)
            proximas_24h = lista_previsao[:8]
            temp_max_dia = max(item['main']['temp_max'] for item in proximas_24h)
            temp_min_dia = min(item['main']['temp_min'] for item in proximas_24h)

            clima_processado = {
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

            return {
                'sucesso': True,
                'clima': clima_processado,
                'bg_image': bg_image,
                'cidade_formatada': cidade_formatada,
                'nascer_sol': nascer_sol,
                'por_sol': por_sol
            }
        else:
            return {'sucesso': False, 'erro': "Cidade não encontrada! Tente novamente."}
            
    except requests.exceptions.RequestException:
        return {'sucesso': False, 'erro': "Não foi possível conectar ao servidor de clima."}