import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    if not DATABASE_URL:
        raise ValueError("Erro: A variável DATABASE_URL não foi encontrada no ficheiro .env!")
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            horario VARCHAR(10) NOT NULL,
            concluido BOOLEAN DEFAULT FALSE,
            data_registro DATE DEFAULT CURRENT_DATE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agua (
            id SERIAL PRIMARY KEY,
            quantidade_ml INTEGER NOT NULL,
            data_registro DATE DEFAULT CURRENT_DATE
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def salvar_medicamento(nome, horario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicamentos (nome, horario, concluido) VALUES (%s, %s, FALSE)",
        (nome, horario)
    )
    conn.commit()
    cursor.close()
    conn.close()

def listar_medicamentos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, horario, concluido FROM medicamentos WHERE data_registro = CURRENT_DATE ORDER BY horario ASC"
    )
    medicamentos = cursor.fetchall()
    cursor.close()
    conn.close()
    return medicamentos

def listar_medicamentos_pendentes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, horario FROM medicamentos WHERE data_registro = CURRENT_DATE AND concluido = FALSE ORDER BY horario ASC"
    )
    medicamentos = cursor.fetchall()
    cursor.close()
    conn.close()
    return medicamentos

def marcar_medicamento_tomado(medicamento_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE medicamentos SET concluido = TRUE WHERE id = %s",
        (medicamento_id,)
    )
    conn.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conn.close()
    return linhas_afetadas > 0

def salvar_agua(quantidade_ml):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO agua (quantidade_ml) VALUES (%s)",
        (quantidade_ml,)
    )
    conn.commit()
    cursor.close()
    conn.close()

def buscar_total_agua_hoje():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(quantidade_ml) FROM agua WHERE data_registro = CURRENT_DATE"
    )
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado[0] is not None else 0


def buscar_historico_agua_semanal():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data_registro, SUM(quantidade_ml) as total
        FROM agua
        WHERE data_registro >= CURRENT_DATE - INTERVAL '6 days'
        GROUP BY data_registro
        ORDER BY data_registro ASC
    """)
    historico = cursor.fetchall()
    cursor.close()
    conn.close()
    return historico

def buscar_historico_medicamentos_semanal():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT data_registro, concluido, COUNT(*) as contagem
        FROM medicamentos
        WHERE data_registro >= CURRENT_DATE - INTERVAL '6 days'
        GROUP BY data_registro, concluido
        ORDER BY data_registro ASC
    """)
    historico = cursor.fetchall()
    cursor.close()
    conn.close()
    return historico