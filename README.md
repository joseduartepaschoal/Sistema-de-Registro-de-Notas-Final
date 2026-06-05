# Sistema Acadêmico de Registro de Notas

## Descrição

Este projeto foi desenvolvido para a disciplina de Desenvolvimento Rápido de Aplicações em Python.

O sistema permite o gerenciamento de alunos por meio de operações CRUD (Create, Read, Update e Delete), utilizando interface gráfica desenvolvida com Tkinter e persistência de dados através do banco SQLite.

O objetivo é facilitar o cadastro, consulta, atualização e remoção de informações acadêmicas de forma simples, organizada e intuitiva.

---

## Tecnologias Utilizadas

* Python 3
* Tkinter
* SQLite
* SQL

---

## Funcionalidades

### Cadastro de Alunos

* Matrícula
* Nome
* Curso
* Nota

### Consulta de Alunos

* Listagem completa dos registros
* Busca por nome
* Busca por matrícula
* Busca por curso

### Atualização de Dados

* Edição das informações cadastradas

### Exclusão de Registros

* Remoção de alunos com confirmação prévia

### Recursos Adicionais

* Interface organizada por abas
* Modo claro e escuro
* Validação de campos obrigatórios
* Validação de notas (0 a 10)
* Cálculo automático da situação do aluno
* Cores indicativas para aprovado, recuperação e reprovado
* Barra de status para feedback ao usuário

---

## Estrutura do Projeto

```text
ProjetoPythonNotas/
│
├── main.py
├── database.py
├── escola.db
└── README.md
```

### Arquivos

**main.py**

* Responsável pela interface gráfica e interação com o usuário.

**database.py**

* Responsável pela comunicação com o banco de dados SQLite e implementação das operações CRUD.

**escola.db**

* Banco de dados utilizado para armazenar as informações dos alunos.

---

## Como Executar

### Pré-requisitos

* Python 3 instalado

### Passos

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

2. Acesse a pasta do projeto:

```bash
cd ProjetoPythonNotas
```

3. Execute o sistema:

```bash
python main.py
```

ou

```bash
py main.py
```

---

## Banco de Dados

O projeto utiliza SQLite, que armazena os dados em um único arquivo local chamado:

```text
escola.db
```

### Vantagens do SQLite

* Fácil instalação
* Não necessita servidor
* Leve e rápido
* Ideal para aplicações acadêmicas e de pequeno porte

### Limitações

* Menos adequado para sistemas com muitos usuários simultâneos
* Menor escalabilidade quando comparado ao PostgreSQL

---

## Conceitos Aplicados

* Programação Orientada a Objetos
* CRUD
* Interface Gráfica com Tkinter
* Banco de Dados Relacional
* SQL
* Validação de Dados
* Separação de Responsabilidades

---

## Autores

Projeto desenvolvido para a disciplina de Desenvolvimento Rápido de Aplicações em Python.

Integrantes:

* José Duarte Paschoal
* Annie
* Ellen
* Luciano

---

## Licença

Projeto desenvolvido exclusivamente para fins acadêmicos.
