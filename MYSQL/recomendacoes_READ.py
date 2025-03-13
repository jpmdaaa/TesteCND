import mysql.connector
import tkinter as tk
from tkinter import scrolledtext

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "jp@1234",
    "database": "filmes_db"
}

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.errors.ProgrammingError:
        print("Banco de dados não encontrado.")
        return None

# Função para buscar recomendações salvas no banco
def buscar_recomendacoes():
    conn = conectar_banco()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT titulo, data_lancamento, nota FROM recomendacoes_filmes")
    recomendacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return recomendacoes

# Função para exibir recomendações na interface gráfica
def exibir_recomendacoes():
    recomendacoes = buscar_recomendacoes()
    resultado_texto.delete('1.0', tk.END)  # Limpa a tela
    
    if not recomendacoes:
        resultado_texto.insert(tk.END, "Nenhuma recomendação encontrada.\n")
        return
    
    resultado_texto.insert(tk.END, "--- Recomendações de Filmes ---\n")
    for rec in recomendacoes:
        resultado_texto.insert(tk.END, f"{rec['titulo']} ({rec['data_lancamento']}), Nota: {rec['nota']}\n")

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Recomendações de Filmes")
janela.geometry("600x400")

# Botão para exibir recomendações
btn_exibir = tk.Button(janela, text="Exibir Recomendações", command=exibir_recomendacoes)
btn_exibir.pack(pady=5)

# Área de texto rolável para exibir os resultados
resultado_texto = scrolledtext.ScrolledText(janela, width=70, height=20)
resultado_texto.pack(pady=10)

# Iniciar a interface gráfica
janela.mainloop()
