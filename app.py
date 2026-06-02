from flask import Flask, render_template, request
from historico import carregar_historico, salvar_historico
from clima import buscar_dados_clima

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Inicializa as variáveis para a Home (vazia)
    historico = carregar_historico()
    bg_image = "pré-pesquisa.webp"

    if request.method == "POST":
        cidade = request.form.get("cidade")
        if cidade:
            resultado = buscar_dados_clima(cidade)
            
            if resultado['sucesso']:
                # Salva no histórico e envia para a tela de RESULTADO
                historico = salvar_historico(resultado['cidade_formatada'])
                return render_template(
                    "resultado.html",
                    clima=resultado['clima'],
                    bg_image=resultado['bg_image'],
                    nascer_sol=resultado['nascer_sol'],
                    por_sol=resultado['por_sol']
                )
            else:
                # Se der erro, volta para a tela VAZIA com a mensagem de erro
                return render_template("home.html", erro=resultado['erro'], bg_image=bg_image, historico=historico)

    # Acesso normal via GET
    return render_template("home.html", bg_image=bg_image, historico=historico)

if __name__ == "__main__":
    app.run(debug=True)