# 🐑 AuctionEAJ – Sistema Web de Gerenciamento de Leilões de Animais

<p align="center">
  <strong>Plataforma digital para organização e gerenciamento de leilões de animais da Escola Agrícola de Jundiaí (EAJ/UFRN).</strong>
</p>

---

## 📖 Sobre o Projeto

O **AuctionEAJ** é um sistema web desenvolvido utilizando Python e Django, com o propósito de auxiliar no gerenciamento e na realização de leilões de animais da Escola Agrícola de Jundiaí (EAJ), vinculada à Universidade Federal do Rio Grande do Norte (UFRN).

A plataforma foi concebida para informatizar e otimizar os processos relacionados à organização de leilões, centralizando informações sobre os animais, permitindo a formação de lotes e facilitando a consulta dos eventos e das negociações.

O sistema possibilita o cadastro individual dos animais, armazenando informações relacionadas às suas características físicas, identificação, raça, histórico reprodutivo e filiação. Posteriormente, os animais podem ser agrupados em lotes, que são organizados e disponibilizados para participação nos leilões.

O AuctionEAJ busca proporcionar maior organização, praticidade e transparência no acesso às informações, contribuindo para a modernização dos processos de comercialização de animais por meio da utilização de tecnologias da informação.

## 🎯 Objetivo Geral

Desenvolver um sistema web para o gerenciamento e a realização de leilões de animais da Escola Agrícola de Jundiaí (EAJ/UFRN), utilizando tecnologias web para facilitar o cadastro dos animais, a formação de lotes, a organização dos eventos e o acompanhamento das negociações.

## 🎯 Objetivos Específicos

- Desenvolver uma plataforma web para gerenciamento de leilões de animais.
- Implementar funcionalidades para cadastro e gerenciamento dos animais.
- Permitir o armazenamento de informações individuais e genealógicas dos animais.
- Possibilitar a criação de lotes compostos por um ou mais animais.
- Facilitar a organização e disponibilização dos lotes nos leilões.
- Permitir a consulta pública das informações dos animais e dos leilões.
- Implementar mecanismos de autenticação e controle de acesso.
- Disponibilizar recursos para acompanhamento e registro das negociações.
- Contribuir para a modernização dos processos de comercialização de animais na instituição.

---

## 🚀 Funcionalidades do Sistema

### 🐑 1. Gerenciamento de Animais

O módulo de gerenciamento de animais permite cadastrar e administrar os exemplares que poderão participar dos leilões.

**Principais funcionalidades:**

- Cadastro individual de animais;
- Identificação por número de brinco;
- Registro da raça;
- Identificação do sexo;
- Registro da cor predominante da pelagem;
- Cadastro do peso atual;
- Registro da altura;
- Cadastro da data de nascimento;
- Registro da quantidade de crias, quando aplicável;
- Registro do peso ao nascer;
- Identificação da filiação (pai e mãe);
- Upload de fotografias dos animais;
- Listagem dos animais cadastrados;
- Visualização detalhada das informações;
- Edição e exclusão de registros.

### 📦 2. Gerenciamento de Lotes

O gerenciamento de lotes permite organizar os animais que participarão dos leilões.

**Principais funcionalidades:**

- Cadastro de lotes;
- Identificação e numeração dos lotes;
- Associação de um ou mais animais a um mesmo lote;
- Cadastro de descrição dos lotes;
- Definição das informações comerciais;
- Visualização dos animais pertencentes a cada lote;
- Apresentação das fotografias e características dos animais;
- Organização dos lotes para participação nos leilões.

Um lote pode ser composto por apenas um animal ou por vários animais, conforme a organização estabelecida para cada leilão.

### 🔨 3. Gerenciamento de Leilões

O módulo de gerenciamento de leilões tem como finalidade organizar os eventos de comercialização dos animais.

**Funcionalidades previstas no sistema:**

- Cadastro e organização de leilões;
- Registro das informações dos eventos;
- Associação dos lotes aos respectivos leilões;
- Disponibilização dos lotes para consulta;
- Visualização dos detalhes dos leilões;
- Organização dos animais participantes;
- Consulta das informações relacionadas aos eventos;
- Registro dos resultados das negociações.

### 💰 4. Gerenciamento de Lances

O módulo de lances está relacionado ao acompanhamento das ofertas realizadas durante as negociações dos lotes.

**Recursos contemplados na proposta:**

- Registro das ofertas realizadas pelos participantes;
- Identificação do participante responsável pelo lance;
- Associação dos lances aos respectivos lotes;
- Consulta do histórico de ofertas;
- Identificação do maior lance;
- Registro do resultado do arremate.

### 🔐 5. Gerenciamento de Usuários

O sistema utiliza mecanismos de autenticação para controlar o acesso às funcionalidades administrativas.

**Principais funcionalidades:**

- Autenticação de usuários;
- Login e logout;
- Controle de acesso às funcionalidades;
- Restrição das operações administrativas;
- Proteção das operações de cadastro, edição e exclusão.

### 🌐 6. Consulta Pública

A plataforma disponibiliza interfaces para que visitantes possam consultar as informações públicas.

**Principais funcionalidades:**

- Visualização dos animais cadastrados;
- Consulta dos detalhes dos animais;
- Visualização dos lotes;
- Consulta dos leilões disponíveis;
- Acesso às informações e fotografias dos animais;
- Navegação pelas principais páginas da plataforma sem necessidade de autenticação, conforme as permissões configuradas.

---

## 🖥️ Interfaces do Sistema

O AuctionEAJ possui interfaces desenvolvidas para facilitar a navegação e proporcionar acesso organizado às funcionalidades da plataforma.

| Interface | Descrição |
|---|---|
| Página inicial | Apresenta a plataforma e permite acessar as principais funcionalidades. |
| Listagem de animais | Exibe os animais cadastrados em cards com fotografias e informações principais. |
| Detalhes do animal | Apresenta as características completas do animal selecionado. |
| Cadastro de animais | Permite registrar novos animais no sistema. |
| Edição de animais | Possibilita atualizar as informações cadastradas. |
| Cadastro de lotes | Permite criar lotes e associar vários animais. |
| Listagem de lotes | Apresenta os lotes cadastrados e seus respectivos animais. |
| Detalhes dos lotes | Exibe informações específicas dos lotes. |
| Gerenciamento de leilões | Permite organizar e consultar os eventos. |
| Autenticação | Disponibiliza os recursos de acesso ao sistema. |

---

## 🛠️ Tecnologias Utilizadas

O desenvolvimento do AuctionEAJ utiliza tecnologias voltadas à construção de aplicações web, gerenciamento de dados e desenvolvimento de interfaces responsivas.

| Tecnologia | Finalidade |
|---|---|
| [Python](https://www.python.org/) | Linguagem de programação utilizada no desenvolvimento. |
| [Django](https://www.djangoproject.com/) | Framework responsável pela estrutura e lógica da aplicação web. |
| [HTML5](https://developer.mozilla.org/pt-BR/docs/Web/HTML) | Estruturação das páginas. |
| [CSS3](https://developer.mozilla.org/pt-BR/docs/Web/CSS) | Estilização das interfaces. |
| [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript) | Implementação de interatividade. |
| [Bootstrap 5](https://getbootstrap.com/) | Desenvolvimento de interfaces responsivas. |
| [SQLite](https://www.sqlite.org/) | Banco de dados utilizado no desenvolvimento. |
| [Pillow](https://pillow.readthedocs.io/) | Processamento e gerenciamento de imagens. |
| [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) | Personalização de atributos e apresentação de campos dos formulários Django. |
| [Git](https://git-scm.com/) | Controle de versão. |
| [GitHub](https://github.com/) | Hospedagem e gerenciamento do código-fonte. |

---

## 🗄️ Organização das Informações

O sistema trabalha com três elementos centrais:

**1. Animais:** representam os exemplares cadastrados individualmente, contendo suas características e informações de identificação.

**2. Lotes:** representam o agrupamento de um ou mais animais que serão disponibilizados para negociação.

**3. Leilões:** representam os eventos nos quais os lotes são organizados e disponibilizados aos participantes.

Essa organização permite separar o cadastro dos animais da formação dos lotes e da realização dos leilões, proporcionando maior flexibilidade no gerenciamento das negociações.

### 📊 Informações dos Animais

| Campo | Exemplo | Descrição |
|---|---|---|
| Número do brinco | 12345 | Identificação individual do animal. |
| Cor | Branco | Cor predominante da pelagem. |
| Peso atual | 45,3 kg | Peso registrado do animal. |
| Altura | 0,70 m | Altura na cernelha. |
| Sexo | Macho/Fêmea | Identificação sexual. |
| Quantidade de crias | 2 | Quantidade de crias geradas, quando aplicável. |
| Peso ao nascer | 3,2 kg | Peso registrado ao nascimento. |
| Filiação | Pai: 123 / Mãe: 456 | Identificação dos genitores. |
| Raça | Santa Inês | Raça do animal. |
| Data de nascimento | 10/05/2024 | Data de nascimento. |
| Fotografia | Imagem | Registro visual do animal. |

---

## 🔄 Fluxo de Funcionamento

O funcionamento geral do AuctionEAJ pode ser representado pelas seguintes etapas:

1. **Cadastro dos animais:** os animais são registrados individualmente, com suas características e informações.
2. **Formação dos lotes:** os animais são agrupados conforme a organização definida para o leilão.
3. **Organização do evento:** os lotes são associados ao respectivo leilão.
4. **Disponibilização:** os lotes são apresentados para consulta dos participantes.
5. **Negociação:** são realizadas e acompanhadas as ofertas pelos lotes, conforme as regras do evento.
6. **Finalização:** os resultados das negociações e os respectivos arremates são registrados.

---

## ⚙️ Instalação e Execução

Para executar o projeto localmente, é necessário possuir Python e Git instalados no computador.

### 1. Clonar o repositório

Abra o terminal ou o prompt de comando e execute:

```bash
git clone https://github.com/Ramonie/controle_ovinos.git
```

Acesse a pasta do projeto:

```bash
cd controle_ovinos
```

### 2. Criar um ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Instalar as dependências

O projeto possui um arquivo `requirements.txt` com as principais dependências.

Execute:

```bash
pip install -r requirements.txt
```

As dependências declaradas são:

```text
Django>=5.0
Pillow>=10.0
django-widget-tweaks>=1.5
```

### 5. Aplicar as migrações

```bash
python manage.py migrate
```

Caso sejam realizadas alterações nos modelos do banco de dados, execute também:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Criar um usuário administrador

```bash
python manage.py createsuperuser
```

Informe os dados solicitados pelo Django para criar o usuário administrativo.

### 7. Executar o servidor

```bash
python manage.py runserver
```

Após iniciar o servidor, acesse a aplicação pelo navegador:

http://127.0.0.1:8000/

---

## 📂 Estrutura do Projeto

A organização principal do repositório está apresentada abaixo:

```text
controle_ovinos/
│
├── controle_ovinos/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── ovinos/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── media/
│
├── .vscode/
│
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

*Observação: a estrutura interna das pastas pode variar conforme a evolução do projeto. A representação acima apresenta os principais componentes esperados da aplicação Django.*

---

## 🔒 Segurança e Controle de Acesso

O AuctionEAJ utiliza os recursos de autenticação disponibilizados pelo Django para controlar o acesso dos usuários.

As operações administrativas devem ser protegidas por mecanismos de autenticação e autorização, evitando que usuários não autorizados realizem alterações nos registros.

Entre os recursos de segurança considerados estão:

- Autenticação de usuários;
- Gerenciamento de sessões;
- Proteção das operações administrativas;
- Controle de permissões;
- Validação dos dados enviados pelos formulários;
- Proteção contra requisições indevidas por meio dos mecanismos de segurança do Django.

---

## 🌱 Importância do Projeto para o Agronegócio

A utilização de tecnologias da informação no agronegócio permite modernizar processos, melhorar a organização de dados e proporcionar novas possibilidades para a comercialização de produtos e animais.

Nesse contexto, o AuctionEAJ busca contribuir para a transformação digital dos processos de leilões de animais da Escola Agrícola de Jundiaí.

A centralização das informações dos animais e dos lotes facilita a consulta dos dados e a organização dos eventos, reduzindo a dependência de controles manuais e proporcionando um ambiente digital para gerenciamento das negociações.

Além disso, o projeto representa a aplicação prática dos conhecimentos adquiridos durante a formação acadêmica em Análise e Desenvolvimento de Sistemas, integrando desenvolvimento web, banco de dados, interfaces e tecnologias aplicadas ao setor agropecuário.

---

## 🎓 Contexto Acadêmico

O AuctionEAJ é um projeto acadêmico desenvolvido no âmbito do curso de **Análise e Desenvolvimento de Sistemas da Universidade Federal do Rio Grande do Norte (UFRN)**, vinculado à **Escola Agrícola de Jundiaí (EAJ)**.

A proposta está relacionada à aplicação de soluções tecnológicas para apoiar atividades de gerenciamento e comercialização de animais, utilizando ferramentas de desenvolvimento de software para atender a uma necessidade do contexto agropecuário.

---

## 🧑‍💻 Autor

**Ramonie Martins**

🎓 Graduando em Análise e Desenvolvimento de Sistemas – UFRN.

💻 Desenvolvedor do AuctionEAJ.

🐑 Projeto acadêmico voltado à aplicação de tecnologias da informação no agronegócio.

- GitHub: [@Ramonie](https://github.com/Ramonie)
- Repositório: [AuctionEAJ](https://github.com/Ramonie/controle_ovinos)

---

## 📜 Licença

Este projeto está disponibilizado sob a licença MIT.

A utilização, modificação e distribuição do código-fonte devem respeitar as condições estabelecidas pela licença e os termos do arquivo `LICENSE`, quando disponibilizado no repositório.

---

<p align="center">
  <strong>🐑 AuctionEAJ</strong><br>
  Tecnologia e inovação aplicadas ao gerenciamento de leilões de animais.
</p>