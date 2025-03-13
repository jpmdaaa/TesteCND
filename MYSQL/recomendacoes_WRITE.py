import os
import requests
import mysql.connector
import tkinter as tk
from tkinter import messagebox

API_KEY = "208186528537a809a6f523c85826b5d3"
MOVIE_ID = 500
BASE_URL = "https://api.themoviedb.org/3"

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "jp@1234",
    "database": "filmes_db"
}

def executar_script_sql():
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
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.errors.ProgrammingError:
        executar_script_sql()
        return mysql.connector.connect(**db_config)

def limpar_banco():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recomendacoes_filmes")
    conn.commit()
    cursor.close()
    conn.close()

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "append_to_response": "credits,similar"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def get_recommendations_by_genres(movie_details):
    if not movie_details or "genres" not in movie_details:
        return []
    
    genre_ids = [genre["id"] for genre in movie_details.get("genres", [])]
    genres_param = ",".join(map(str, genre_ids))

    url = f"{BASE_URL}/discover/movie"
    params = {"api_key": API_KEY, "with_genres": genres_param, "sort_by": "popularity.desc", "page": 1}

    response = requests.get(url, params=params)
    return response.json().get("results", [])[:5]

def salvar_no_banco(recomendacoes, limpar):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    if limpar:
        limpar_banco()
    
    for rec in recomendacoes:
        cursor.execute(
            "INSERT INTO recomendacoes_filmes (filme_id, titulo, data_lancamento, nota) VALUES (%s, %s, %s, %s)",
            (rec["id"], rec["title"], rec["release_date"], rec["vote_average"])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def executar_recomendacao():
    limpar = limpar_var.get()
    movie_details = get_movie_details(MOVIE_ID)
    if not movie_details:
        messagebox.showerror("Erro", "Filme não encontrado.")
        return
    
    recomendacoes = get_recommendations_by_genres(movie_details)
    salvar_no_banco(recomendacoes, limpar)
    messagebox.showinfo("Sucesso", "Recomendações salvas no banco de dados!")

# Interface Tkinter
root = tk.Tk()
root.title("Sistema de Recomendação de Filmes")

tk.Label(root, text="Clique para executar a recomendação de filmes:").pack(pady=10)

limpar_var = tk.BooleanVar()
limpar_checkbox = tk.Checkbutton(root, text="Limpar banco antes de salvar", variable=limpar_var)
limpar_checkbox.pack()

tk.Button(root, text="Executar", command=executar_recomendacao).pack(pady=10)

root.mainloop()