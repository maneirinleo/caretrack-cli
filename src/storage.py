import os
import psycopg2
from dotenv import load_dotenv

# Configura o caminho absoluto para encontrar o arquivo .env na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Busca a string de conexão de forma segura
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Erro: A variável de ambiente DATABASE_URL não foi configurada!")

def get_connection():
    """Abre uma conexão criptografada com o banco de dados PostgreSQL na nuvem."""
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Cria as tabelas no Supabase caso elas ainda não existam."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Criação da tabela de água
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agua (
            id SERIAL PRIMARY KEY,
            quantidade_ml INTEGER NOT NULL,
            data_registro DATE DEFAULT CURRENT_DATE
        )
    """)
    
    # Criação da tabela de medicamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            horario VARCHAR(10) NOT NULL,
            concluido BOOLEAN DEFAULT FALSE
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def load_data():
    """Busca os dados direto da nuvem e os formata para as interfaces (CLI/Streamlit)."""
    init_db()  # Garante que as tabelas existem antes de rodar o SELECT
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Soma toda a água registrada na data de hoje
    cursor.execute("SELECT SUM(quantidade_ml) FROM agua WHERE data_registro = CURRENT_DATE")
    total_agua = cursor.fetchone()[0]
    total_agua = total_agua if total_agua is not None else 0
    
    # 2. Busca todos os medicamentos agendados organizados por horário
    cursor.execute("SELECT nome, horario, concluido FROM medicamentos ORDER BY horario ASC")
    rows = cursor.fetchall()
    
    medicamentos = []
    for row in rows:
        medicamentos.append({
            "nome": row[0],
            "horario": row[1],
            "concluido": row[2]
        })
        
    cursor.close()
    conn.close()
    
    return {
        "agua_ml": total_agua,
        "medicamentos": medicamentos
    }

def add_agua(ml):
    """Insere um novo registro de consumo de água no banco de dados na nuvem."""
    if ml <= 0:
        raise ValueError("A quantidade de água deve ser maior que zero.")
        
    init_db()  # Garante a existência da tabela antes do INSERT
    conn = get_connection()
    cursor = conn.cursor()
    
    # O uso do %s previne vulnerabilidades de SQL Injection
    cursor.execute("INSERT INTO agua (quantidade_ml) VALUES (%s)", (ml,))
    
    conn.commit()
    cursor.close()
    conn.close()

def add_medicamento(nome, horario):
    """Insere um novo medicamento agendado no banco de dados na nuvem."""
    init_db()  # Garante a existência da tabela antes do INSERT
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO medicamentos (nome, horario, concluido) VALUES (%s, %s, FALSE)",
        (nome, horario)
    )
    
    conn.commit()
    cursor.close()
    conn.close()