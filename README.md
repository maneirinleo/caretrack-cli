# 🔗 [Acesse o App no Streamlit](https://caretrack-cli-lvfkqt5dyejhqvf5a2fbbw.streamlit.app/)

# CareTrack CLI 💊💧
![Versão](https://img.shields.io/badge/version-1.0.0-blue.svg)
![GitHub Actions](https://img.shields.io/badge/build-passing-brightgreen)

## 📌 O Problema
O envelhecimento da população aumenta a necessidade de ferramentas simples que auxiliem idosos e cuidadores na organização da rotina de autocuidado, reduzindo esquecimentos relacionados a medicamentos e hidratação.

## 💡 A Solução
O **CareTrack CLI** é uma aplicação de linha de comando desenvolvida para auxiliar no gerenciamento dessa rotina diária de forma simples e direta, registrando medicamentos e acompanhando o consumo de água.

## 🚀 Tecnologias Utilizadas
* **Python 3.12**
* **PostgreSQL (Supabase)** - Armazenamento de dados centralizado e persistente na nuvem
* **Psycopg2** - Driver de conexão entre o Python e o banco de dados PostgreSQL
* **Python-dotenv** - Gerenciamento seguro de variáveis de ambiente locais
* **Pytest** - Testes Automatizados
* **Ruff** - Linting e Análise Estática
* **GitHub Actions** - Integração Contínua (CI)

---

## ⚙️ Como Instalar e Rodar na Máquina Local

### 1. Clonar o Repositório
Abra o seu terminal e execute os comandos abaixo para baixar o projeto e entrar na pasta dele:
```bash
git clone https://github.com/maneirinleo/caretrack-cli
cd caretrack-cli
```
### 2. Criar e ativar ambiente virtual (venv)
```bash
python -m venv venv
```
Libere a permissão de execução de scripts no PowerShell (apenas para esta sessão)
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```
Ative o ambiente virtual
```bash
.\venv\Scripts\Activate.ps1
```
### 3. Instalar as Dependências
Com o ambiente virtual ativado (você verá um (venv) antes do prompt do terminal), instale os pacotes necessários rodando:

```bash
pip install -r requirements.txt
```
### 4. Executar a CLI
Agora basta iniciar a aplicação informando o caminho do script principal:

```bash
python src/main.py
```