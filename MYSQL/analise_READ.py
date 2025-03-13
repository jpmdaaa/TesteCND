import mysql.connector
import tkinter as tk
from tkinter import scrolledtext

# Configuração da conexão com o MySQL
config = {
    "host": "localhost",
    "user": "root",
    "password": "jp@1234",
    "database": "filmes_db"
}

""" Função para executar consultas e exibir resultados"""
def executar_consulta(query, titulo):
    try:
        conexao = mysql.connector.connect(**config)
        cursor = conexao.cursor()

        cursor.execute(query)
        resultados = cursor.fetchall()

        """ Exibe os resultados na interface"""
        resultado_texto.delete('1.0', tk.END)  # Limpa o campo de texto
        resultado_texto.insert(tk.END, f"--- {titulo} ---\n\n")
        for linha in resultados:
            ator, valor = linha
            if valor is None:  # Garante que valores NULL não causem erro
                valor = 0
            resultado_texto.insert(tk.END, f"{ator}: {valor}\n")

        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        resultado_texto.delete('1.0', tk.END)
        resultado_texto.insert(tk.END, f"Erro ao conectar no MySQL: {erro}")

"""Funções associadas aos botões"""
def contagem_atores():
    query = """
        SELECT ator, SUM(participacoes) AS total_filmes 
        FROM analise_filmes 
        GROUP BY ator 
        ORDER BY total_filmes DESC;
    """
    executar_consulta(query, "Contagem de Participação dos Atores")

def frequencia_generos():
    query = """
        SELECT genero, SUM(frequencia_genero) AS total 
        FROM analise_filmes 
        GROUP BY genero 
        ORDER BY total DESC;
    """
    executar_consulta(query, "Frequência de Gêneros")

def top_5_atores_bilheteria():
    query = """
        SELECT ator, IFNULL(SUM(bilheteria_total), 0) AS total_bilheteria 
        FROM analise_filmes 
        GROUP BY ator 
        ORDER BY total_bilheteria DESC 
        LIMIT 5;
    """
    executar_consulta(query, "Top 5 Atores por Bilheteria Total")

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Análise de Filmes - MySQL")
janela.geometry("500x400")

# Botões para executar as funções
btn_atores = tk.Button(janela, text="Contagem de Atores", command=contagem_atores)
btn_atores.pack(pady=5)

btn_generos = tk.Button(janela, text="Frequência de Gêneros", command=frequencia_generos)
btn_generos.pack(pady=5)

btn_top5 = tk.Button(janela, text="Top 5 Atores por Bilheteria", command=top_5_atores_bilheteria)
btn_top5.pack(pady=5)

# Caixa de texto para exibir os resultados
resultado_texto = scrolledtext.ScrolledText(janela, width=60, height=15)
resultado_texto.pack(pady=10)

# Iniciando a interface gráfica
janela.mainloop()
