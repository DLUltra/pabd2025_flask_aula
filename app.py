from flask import Flask, render_template

app = Flask(__name__)

# Lista de produtos
produtos = [
    {'id': 1, 'nome': 'PC', 'valor': 4000, 'qtd': 5},
    {'id': 2, 'nome': 'Macbook', 'valor': 7000, 'qtd': 23},
    {'id': 3, 'nome': 'Notebook', 'valor': 2000, 'qtd': 1},
    {'id': 4, 'nome': 'Watch', 'valor': 1500, 'qtd': 52},
    {'id': 5, 'nome': 'iPhone', 'valor': 4999, 'qtd': 35},
    {'id': 1, 'nome': 'PC', 'valor': 4000, 'qtd': 5},
    {'id': 2, 'nome': 'Macbook', 'valor': 7000, 'qtd': 23},
    {'id': 3, 'nome': 'Notebook', 'valor': 2000, 'qtd': 1},
    {'id': 4, 'nome': 'Watch', 'valor': 1500, 'qtd': 52},
    {'id': 5, 'nome': 'iPhone', 'valor': 4999, 'qtd': 35}
]

@app.route("/")
def hello_world():
    return render_template("index.html", title="3INF1M", app_name="Meu Flask App", produtos=produtos)
