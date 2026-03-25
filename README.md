# 🐑 Sistema de Controle de Estoque de Ovinos

Este projeto é um sistema web desenvolvido com **Django** para o **controle de estoque de ovelhas**, permitindo o gerenciamento completo dos animais disponíveis, suas características detalhadas e consulta rápida antes e durante **leilões**.  

A aplicação facilita a organização e tomada de decisão ao disponibilizar informações essenciais de cada ovino em um só lugar.

---

## 🚀 Funcionalidades Principais

- 📋 **Cadastro completo** de ovinos com dados detalhados:  
  - Número do brinco  
  - Tipo (cor, peso, altura, sexo)  
  - Quantidade de crias (se for fêmea)  
  - Peso ao nascer  
  - Filiação (pai e mãe)  
  - Raça  
  - Foto do animal  

- 📦 **Listagem em cards** com imagem e informações principais.  
- ✏️ Edição e exclusão de registros.  
- 🔐 Autenticação de usuários (login e logout).  
- 👤 Somente usuários logados podem **adicionar, editar ou remover** animais.  
- 🔍 Consulta rápida dos animais disponíveis para **leilões**.  
- 📱 Interface responsiva com **Bootstrap 5**.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.13+](https://www.python.org/)  
- [Django 5+](https://www.djangoproject.com/)  
- [Bootstrap 5](https://getbootstrap.com/)  
- [Pillow](https://pillow.readthedocs.io/) – para upload e tratamento de imagens  

---

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório:

git clone https://github.com/seuusuario/controle_ovinos.git
cd controle_ovinos

### 2️⃣ Criar e ativar um ambiente virtual::
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 3️⃣ Instalar as dependências:
pip install -r requirements.txt


### 4️⃣ Aplicar as migrações e rodar o servidor:
python manage.py migrate
python manage.py runserver

Acesse o sistema em: http://127.0.0.1:8000/

🔐 Autenticação

/login/ – Página de login

/logout/ – Encerra a sessão e retorna à lista de ovinos

Somente usuários logados podem adicionar, editar ou remover animais.

📊 Campos do Cadastro de Ovinos
Campo	Tipo / Exemplo	Descrição
🏷️ Número do Brinco	12345	Identificador único do animal
🎨 Cor	Branco, Preto, Chitado	Cor predominante da pelagem
⚖️ Peso	45.3 kg	Peso atual do animal
📏 Altura	0.70 m	Altura na cernelha
🚻 Sexo	Macho / Fêmea	Gênero do animal
👶 Quantidade de crias	2	(Se fêmea) Número de crias geradas
🍼 Peso ao nascer	3.2 kg	Peso do animal ao nascer
👨‍👩‍👧 Filiação	Pai: 123, Mãe: 456	Número do brinco dos pais
🐑 Raça	Santa Inês, Morada Nova	Raça do ovino
📸 Foto	Upload de imagem	Foto do animal
📱 Interface de Uso

🗂️ Página inicial: Lista de ovinos em cards com foto e dados principais.

🔍 Detalhes: Ao clicar em um card, exibe todas as informações do animal.

✏️ Edição: Permite atualizar os dados cadastrados.

➕ Adicionar: Formulário completo para novo cadastro.

🗑️ Remover: Exclusão de um registro existente.

🧑‍💻 Autor

Desenvolvido por Ramonie Martins
🎓 Estudante de Análise e Desenvolvimento de Sistemas
📚 Projeto acadêmico voltado à aplicação de tecnologia no agronegócio.

📜 Licença

Este projeto é distribuído sob a licença MIT.
Sinta-se livre para usar, modificar e distribuir com os devidos créditos.
