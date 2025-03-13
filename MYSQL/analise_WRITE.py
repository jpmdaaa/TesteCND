#!/usr/bin/env python3
"""
teste_1.py - Análise de Dados de Filmes com Interface Gráfica

Este script analisa uma lista de filmes usando a API do The Movie Database (TMDB) para gerar:
1. Contagem de participação de atores
2. Frequência de gêneros
3. Top 5 atores por bilheteria total

Agora, conta com uma interface gráfica feita com Tkinter para facilitar a interação.

Requisitos:
    requests, mysql-connector-python, tkinter
"""

import json
import requests
import mysql.connector
from collections import Counter, defaultdict
import os
import tkinter as tk
from tkinter import messagebox

"208186528537a809a6f523c85826b5d3"
API_KEY = []
MOVIE_IDS = []
BASE_URL = "https://api.themoviedb.org/3"

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "jp@1234",
    "database": "filmes_db"
}

def executar_script_sql():
    """Executa o script Connect.sql para criar o banco e as tabelas se não existirem."""
    conn = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cursor = conn.cursor()

    caminho_sql = os.path.join("MYSQL", "Connect.sql")

    with open(caminho_sql, "r", encoding="utf-8") as f:
        script_sql = f.read()
        
    for comando in script_sql.split(";"):
        if comando.strip():
            cursor.execute(comando)

    conn.commit()
    cursor.close()
    conn.close()

def conectar_banco():
    """Garante que o banco de dados exista antes de conectar."""
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.errors.ProgrammingError:
        executar_script_sql()
        return mysql.connector.connect(**db_config)

def limpar_banco():
    """Remove todos os dados da tabela de análise de filmes."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analise_filmes")
    conn.commit()
    cursor.close()
    conn.close()

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "append_to_response": "credits"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def analyze_movies(movie_data_list):
    actor_appearances = Counter()
    genre_frequency = Counter()
    actor_box_office = defaultdict(int)

    for movie in movie_data_list:
        if not movie:
            continue
        for genre in movie.get("genres", []):
            genre_frequency[genre["name"]] += 1
        revenue = movie.get("revenue", 0)
        for cast_member in movie.get("credits", {}).get("cast", []):
            actor_name = cast_member["name"]
            actor_appearances[actor_name] += 1
            actor_box_office[actor_name] += revenue

    top_actors_by_revenue = sorted(actor_box_office.items(), key=lambda x: x[1], reverse=True)[:5]

    return actor_appearances, genre_frequency, top_actors_by_revenue

def salvar_no_banco(analise):
    conn = conectar_banco()
    cursor = conn.cursor()

    actor_appearances, genre_frequency, top_actors_by_revenue = analise

    # Salvando as participações dos atores
    for actor, count in actor_appearances.items():
        cursor.execute("INSERT INTO analise_filmes (ator, participacoes) VALUES (%s, %s)", (actor, count))

    # Salvando a frequência dos gêneros
    for genre, count in genre_frequency.items():
        cursor.execute("INSERT INTO analise_filmes (genero, frequencia_genero) VALUES (%s, %s)", (genre, count))

    # Salvando os top 5 atores por bilheteira
    for actor, revenue in top_actors_by_revenue:
        cursor.execute("INSERT INTO analise_filmes (ator, bilheteria_total) VALUES (%s, %s)", (actor, revenue))

    conn.commit()
    cursor.close()
    conn.close()

def executar_analise():
    global API_KEY, MOVIE_IDS
    API_KEY = api_key_entry.get().strip()
    MOVIE_IDS = list(map(int, movie_ids_entry.get().split(",")))
    
    if not API_KEY or not MOVIE_IDS:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        return
    
    if limpar_var.get():
        limpar_banco()
    
    movie_data_list = [get_movie_details(movie_id) for movie_id in MOVIE_IDS]
    analise = analyze_movies(movie_data_list)
    salvar_no_banco(analise)
    messagebox.showinfo("Sucesso", "Análise concluída e salva no banco de dados.")

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Análise de Filmes")

# API Key
tk.Label(root, text="API Key:").grid(row=0, column=0)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.grid(row=0, column=1)

# IDs dos filmes
tk.Label(root, text="IDs dos filmes (separados por vírgula):").grid(row=1, column=0)
movie_ids_entry = tk.Entry(root, width=50)
movie_ids_entry.grid(row=1, column=1)

# Checkbox para limpar banco
tk.Label(root, text="").grid(row=2, column=0)
limpar_var = tk.BooleanVar()
limpar_check = tk.Checkbutton(root, text="Limpar banco antes de executar", variable=limpar_var)
limpar_check.grid(row=3, columnspan=2)

# Botão de execução
executar_btn = tk.Button(root, text="Executar Análise", command=executar_analise)
executar_btn.grid(row=4, columnspan=2)

root.mainloop()