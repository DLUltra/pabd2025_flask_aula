# Sistema de Gerenciamento de Funcionários 👥

**Programação com Acesso a Banco de Dados**

## Informações da Instituição

- **Instituição:** IFRN - Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte
- **Campus:** Macau
- **Curso:** Técnico Integrado em Informática
- **Disciplina:** Programação com Acesso a Banco de Dados
- **Professor:** Guilherme Leal Santos
  - GitHub: [@guileals](https://www.github.com/guileals)

---

## 📋 Descrição do Projeto

Sistema web para gerenciamento de funcionários desenvolvido com Flask e Bootstrap, integrado com Supabase para persistência de dados.

---

## 🚀 Como Começar

### 1. Criar Ambiente Virtual

```bash
python3 -m venv venv
```

### 2. Ativar Ambiente Virtual

```bash
source /workspaces/codespaces-flask/.venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

```bash
flask --debug run
```

A aplicação estará disponível em `http://localhost:5000`

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **Frontend:** Bootstrap 5.3.0
- **Banco de Dados:** Supabase (PostgreSQL)
- **Ícones:** Font Awesome 6.4.0
- **Template Engine:** Jinja2

---

## 📁 Estrutura do Projeto

```
codespaces-flask/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
├── config/               # Configurações
│   └── database.py      # Conexão com Supabase
├── dao/                 # Data Access Objects
│   └── funcionario_dao.py
├── models/              # Modelos de dados
│   └── funcionario.py
├── static/              # Arquivos estáticos
│   ├── main.css
│   └── logo.jpg
└── templates/           # Templates HTML
    ├── base.html       # Template base
    ├── index.html      # Listagem de funcionários
    ├── details.html    # Detalhes do funcionário
    ├── create.html     # Criar funcionário
    └── edit.html       # Editar funcionário
```

---

## 📝 Recursos Principais

- ✅ Listagem de funcionários
- ✅ Visualizar detalhes do funcionário
- ✅ Criar novo funcionário
- ✅ Editar funcionário
- ✅ Deletar funcionário
- ✅ Formatação automática de CPF (XXX.XXX.XXX-XX)
- ✅ Responsivo em dispositivos móveis

---

## 📧 Contato

Para dúvidas ou sugestões sobre este projeto, entre em contato com o professor Guilherme Leal Santos.
