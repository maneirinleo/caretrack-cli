import os
import psycopg2
from dotenv import load_dotenv

#use caso precise apagar as tabelas do db (geralmente em por causa de erros)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def resetar_banco():
    print("Conectando ao banco de dados Supabase...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("Apagando tabelas antigas (DROP TABLE)...")
    cursor.execute("DROP TABLE IF EXISTS medicamentos CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS agua CASCADE;")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Banco de dados limpo com sucesso! Agora as tabelas serão recriadas corretamente.")

if __name__ == "__main__":
    resetar_banco()