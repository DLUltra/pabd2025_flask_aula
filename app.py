# importação das bibliotecas necessárias
from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
from config.database import SupabaseConnection
# importando dos arquivos de modelo e dao
from dao.funcionario_dao import FuncionarioDAO
from models.funcionario import Funcionario

app = Flask(__name__)


# conectando ao supabase
client = SupabaseConnection().client

# rota da página inicial
@app.route("/")
def index():
    return render_template("index.html", title="Empresa", app_name="Controle & Gestão de Funcionarios", funcionarios=funcionario_dao.read_all())

# instanciando o dao de funcionário
funcionario_dao = FuncionarioDAO(client)

# filtro customizado para formatação de cpf
@app.template_filter('format_cpf')
def format_cpf(cpf):
    """Formata CPF no padrão XXX.XXX.XXX-XX"""
    if not cpf or len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

# filtro customizado para formatação de data/hora
@app.template_filter('format_datetime_br')
def format_datetime_br(value):
    """Formata datetime para o padrão brasileiro DD/MM/YYYY HH:MM:SS"""
    if not value:
        return ""
    if isinstance(value, str):
        try:
            # convertendo string iso para datetime
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    if isinstance(value, datetime):
        return value.strftime('%d/%m/%Y %H:%M:%S')
    return value

# filtro customizado para formatação de data
@app.template_filter('format_date_br')
def format_date_br(value):
    """Formata data para o padrão brasileiro DD/MM/YYYY"""
    if not value:
        return ""
    if isinstance(value, str):
        try:
            # convertendo string iso para datetime
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    if isinstance(value, datetime):
        return value.strftime('%d/%m/%Y')
    return value

@app.route("/funcionario/<string:pk>/<int:id>")
def details(pk, id):
    funcionario = funcionario_dao.read(pk, id)
    return render_template("details.html", funcionario=funcionario, datetime=datetime)

# rota para criação de novo funcionário
@app.route('/funcionario/novo', methods=['GET', 'POST'])
def create():
    try:
        if request.method == "POST":
            # criar novo objeto funcionário
            # aceita ponto ou vírgula como decimal
            salario_str = request.form.get("salario", "1518.01")
            salario_str = salario_str.replace(',', '.')
            
            funcionario_novo = Funcionario(
                _cpf = request.form["cpf"],
                _pnome = request.form["pnome"],
                _unome = request.form["unome"],
                _data_nasc = request.form["data_nasc"],
                _salario = float(salario_str),
                _sexo = request.form.get("sexo", "F"),
            )
            
            # atualizar no banco de dados
            resultado = funcionario_dao.create(funcionario_novo)
            
            if resultado:
                return redirect(url_for('index'))
            else:
                return "Erro ao atualizar"
    except:
        pass
    
    return render_template('create.html', datetime=datetime)

# rota para atualização de funcionário (get ou post)
@app.route('/funcionario/edit/<string:pk>', methods=['GET', 'POST'])
def update(pk):
    if request.method == 'POST':
        try:
            # obter dados do formulário
            dados = request.form
            
            # buscar funcionário atual no banco
            funcionario_atual = funcionario_dao.read('cpf', pk)
            if not funcionario_atual:
                return "Funcionário não encontrado", 404
            
            # converter tipos de dados
            from datetime import datetime as dt
            
            # data de nascimento
            data_nasc = funcionario_atual.data_nasc
            if dados.get('data_nasc'):
                try:
                    data_nasc = dt.strptime(dados['data_nasc'], '%Y-%m-%d').date()
                except:
                    pass  # mantém a atual se der erro
            
            # salário
            salario = funcionario_atual.salario
            try:
                # aceita ponto ou vírgula como separador decimal
                salario_str = dados.get('salario', salario)
                if isinstance(salario_str, str):
                    salario_str = salario_str.replace(',', '.')
                salario = float(salario_str)
            except:
                pass
            
            # número departamento
            num_depto = dados.get('numero_departamento')
            numero_departamento = None
            if num_depto and num_depto.strip():
                try:
                    numero_departamento = int(num_depto)
                except:
                    numero_departamento = funcionario_atual.numero_departamento
            
            # cpf supervisor
            cpf_supervisor = dados.get('cpf_supervisor')
            if cpf_supervisor and cpf_supervisor.strip():
                cpf_supervisor = cpf_supervisor.replace('.', '').replace('-', '')
                if len(cpf_supervisor) != 11:
                    cpf_supervisor = None
            else:
                cpf_supervisor = None
            
            # criar objeto com dados atualizados
            funcionario_atualizado = Funcionario(
                _cpf=pk,
                _pnome=dados.get('pnome', funcionario_atual.pnome),
                _unome=dados.get('unome', funcionario_atual.unome),
                _data_nasc=data_nasc,
                _endereco=dados.get('endereco', funcionario_atual.endereco),
                _salario=salario,
                _sexo=dados.get('sexo', funcionario_atual.sexo),
                _cpf_supervisor=cpf_supervisor,
                _numero_departamento=numero_departamento,
                _created_at=funcionario_atual.created_at
            )
            
            print(f"Criado objeto: {funcionario_atualizado}")
            
            # atualizar no banco de dados
            resultado = funcionario_dao.update('cpf', pk, funcionario_atualizado)
            
            if resultado:
                return redirect(url_for('index'))
            else:
                return "Erro ao atualizar"
                
        except Exception as e:
            # mostrar erro simples sem traceback
            import traceback
            print(traceback.format_exc())  # mostra stack trace completo
            return f"Erro: {str(e)}", 500
    
    # exibir formulário de edição
    funcionario = funcionario_dao.read('cpf', pk)
    
    if not funcionario:
        return "Funcionário não encontrado", 404
    
    return render_template('edit.html', funcionario=funcionario, datetime=datetime)

# rota para exclusão de funcionário (get ou post)
@app.route('/funcionario/delete/<string:pk>', methods=['GET', 'POST'])
def delete(pk):
    # processa a exclusão se for post
    if request.method == 'POST':
        try:
            # tentar excluir do banco de dados
            sucesso = funcionario_dao.delete('cpf', pk) # executa a exclusão
            
            if sucesso:
                return redirect(url_for('index'))
            else:
                return "Erro ao excluir funcionário", 500
                
        except Exception as e:
            return f"Erro: {str(e)}", 500
    
    # exibir funcionário a ser removido
    funcionario = funcionario_dao.read('cpf', pk)
    
    if not funcionario:
        return "Funcionário não encontrado", 404
        
    return render_template('delete.html', funcionario=funcionario, datetime=datetime)