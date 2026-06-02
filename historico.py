import json
import os

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