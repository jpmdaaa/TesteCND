
#!/usr/bin/env python3
"""
teste_1.py - Análise de Dados de Filmes

Este script analisa uma lista de filmes usando a API do The Movie Database (TMDB) para gerar:
1. Contagem de participação de atores
2. Frequência de gêneros
3. Top 5 atores por bilheteria total

Uso:
    # 1) Defina sua chave API em "API_KEY" = "208186528537a809a6f523c85826b5d3"
    # 2) Defina o IDS dos filmes a serem analisados em "MOVIE_IDS" = "[550, 11, 13]"
    # 2) Defina o formato em "OUTPUT_FORMAT" = "json" , "console" , "csv"
    
Requisitos:
    requests
"""


import json
import requests
from collections import Counter, defaultdict
import csv
import os
from concurrent.futures import ThreadPoolExecutor

# Configurações do script (defina os valores aqui)
API_KEY = "208186528537a809a6f523c85826b5d3"  # Sua chave da API TMDB
MOVIE_IDS = [100, 200, 300]  # IDs dos filmes a serem analisados
OUTPUT_FORMAT = "console"  # Opções: "console", "json", "csv"
OUTPUT_DIR = "."  # Diretório para salvar os arquivos

BASE_URL = "https://api.themoviedb.org/3"


"""Buscar detalhes do filme da API TMDB."""
def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,  
        "append_to_response": "credits"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados para o filme ID {movie_id}: {e}")
        return None



"""Analisar dados de filmes para extrair participação de atores, frequência de gêneros e bilheteria."""
def analyze_movies(movie_data_list): 
    actor_appearances = Counter()
    genre_frequency = Counter()
    actor_box_office = defaultdict(int)
    
    # Processar cada filme
    for movie in movie_data_list:
        if not movie:
            continue
            
        # Extrair gêneros
        for genre in movie.get("genres", []):
            genre_frequency[genre["name"]] += 1
        
        # Extrair elenco e dados de bilheteria
        revenue = movie.get("revenue", 0)
        for cast_member in movie.get("credits", {}).get("cast", []):
            actor_name = cast_member["name"]
            actor_appearances[actor_name] += 1
            actor_box_office[actor_name] += revenue
    
    # Obter top 5 atores por bilheteria
    top_actors_by_revenue = sorted(
        actor_box_office.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:5]
    
    return {
        "actor_appearances": actor_appearances,
        "genre_frequency": genre_frequency,
        "top_actors_by_revenue": top_actors_by_revenue
    }


"""Formatar e exibir os resultados da análise."""
def format_output(analysis_results):
    actor_appearances = analysis_results["actor_appearances"]
    genre_frequency = analysis_results["genre_frequency"]
    top_actors = analysis_results["top_actors_by_revenue"]
    
    if OUTPUT_FORMAT == "console":
        print("\n=== PARTICIPAÇÃO POR ATOR ===")
        for actor, count in actor_appearances.most_common():
            print(f"{actor}: {count} filme(s)")
        
        print("\n=== FREQUÊNCIA DE GÊNEROS ===")
        for genre, count in genre_frequency.most_common():
            print(f"{genre}: {count} ocorrência(s)")
        
        print("\n=== TOP 5 ATORES POR BILHETERIA ===")
        for i, (actor, revenue) in enumerate(top_actors, 1):
            print(f"{i}. {actor}: ${revenue:,}")
    
    elif OUTPUT_FORMAT == "json":
        output = {
            "actor_appearances": dict(actor_appearances),
            "genre_frequency": dict(genre_frequency),
            "top_actors_by_revenue": [
                {"actor": actor, "revenue": revenue} 
                for actor, revenue in top_actors
            ]
        }
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, "analise_filmes.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Resultados salvos em {output_path}")
    
    elif OUTPUT_FORMAT == "csv":
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Participação de atores
        actor_path = os.path.join(OUTPUT_DIR, "participacao_atores.csv")
        with open(actor_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Ator", "Quantidade de Filmes"])
            writer.writerows(actor_appearances.most_common())
        
        # Frequência de gêneros
        genre_path = os.path.join(OUTPUT_DIR, "frequencia_generos.csv")
        with open(genre_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Gênero", "Frequência"])
            writer.writerows(genre_frequency.most_common())
        
        # Top atores por receita
        revenue_path = os.path.join(OUTPUT_DIR, "top_atores_bilheteria.csv")
        with open(revenue_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Posição", "Ator", "Bilheteria Total (USD)"])
            for i, (actor, revenue) in enumerate(top_actors, 1):
                writer.writerow([i, actor, revenue])
        
        print(f"Resultados salvos no diretório {OUTPUT_DIR}")


def main():
    print(f"Analisando {len(MOVIE_IDS)} filmes...")

    # Buscar detalhes dos filmes usando pool de threads para eficiência
    with ThreadPoolExecutor(max_workers=10) as executor:
        movie_data_list = list(executor.map(get_movie_details, MOVIE_IDS))

    # Analisar os dados de filmes coletados
    analysis_results = analyze_movies(movie_data_list)

    # Exibir os resultados no formato solicitado
    format_output(analysis_results)


if __name__ == "__main__":
    main()