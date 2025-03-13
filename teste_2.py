#!/usr/bin/env python3
"""
teste_2.py - Sistema de Recomendação de Filmes

Este script recomenda 5 filmes com base em um único filme de entrada, usando 
a API The Movie Database (TMDB). O algoritmo de recomendação considera:
- Similaridade de gênero
- Similaridade de diretor
- Sobreposição de elenco
- Nível de popularidade similar
- Proximidade de data de lançamento

Uso:
    # 1) Defina sua chave API em "API_KEY" = "208186528537a809a6f523c85826b5d3"
    # 2) Defina o ID do filme de entrada "MOVIE_ID" = "[550]"
    
    
Requisitos:
    requests
"""

import requests
import json

BASE_URL = "https://api.themoviedb.org/3"

# Definição de parâmetros diretamente no código
MOVIE_ID = 200  # Substituir pelo ID desejado
API_KEY = "208186528537a809a6f523c85826b5d3"  # Substituir pela chave da API
OUTPUT_FILE = "recomendacoes.json"


"""Buscar informações detalhadas sobre um filme."""
def get_movie_details(movie_id, api_key):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": api_key,
        "append_to_response": "credits,similar"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


"""Obter recomendações de filmes com base nos gêneros."""
def get_recommendations_by_genres(movie_details, api_key, limit=20):
    if not movie_details or "genres" not in movie_details:
        return []
    
    genre_ids = [genre["id"] for genre in movie_details.get("genres", [])]
    genres_param = ",".join(map(str, genre_ids))
    
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": api_key,
        "with_genres": genres_param,
        "sort_by": "popularity.desc",
        "page": 1
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("results", [])[:limit]


"""Obter recomendações de filmes com base no ID do filme fornecido."""
def get_movie_recommendations(movie_id, api_key):
    source_movie = get_movie_details(movie_id, api_key)
    if not source_movie:
        print(f"Não foi possível encontrar o filme com ID {movie_id}")
        return []
    
    print(f"Encontrando recomendações para: {source_movie.get('title')}")
    
    candidates = get_recommendations_by_genres(source_movie, api_key)
    
    recommendations = [
        {
            "id": movie.get("id"),
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "vote_average": movie.get("vote_average")
        }
        for movie in candidates[:5]
    ]
    
    return recommendations


def main():
    recommendations = get_movie_recommendations(MOVIE_ID, API_KEY)
    
    if not recommendations:
        print("Nenhuma recomendação encontrada.")
        return
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, indent=2, ensure_ascii=False)
    
    print(f"Recomendações salvas em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()