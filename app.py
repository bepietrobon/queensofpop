import streamlit as st

# Configuração Inicial
st.set_page_config(page_title="🎧 Popularidade no Spotify: Beyoncé vs. Taylor Swift", layout="wide")

import pandas as pd
import plotly.express as px
from spotify_utils import (
    get_artist_id, get_artist_albums, get_album_tracks,
    get_tracks_popularity, get_artist_followers, get_artist_image
)

import streamlit as st

# CSS para centralizar os títulos e conteúdo das tabelas
st.markdown("""
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            text-align: center !important;
            font-weight: bold;
            padding: 10px;
            background-color: #f0f0f0;
        }
        td {
            text-align: center;
            padding: 8px;
        }
        /* CSS para personalizar a sidebar */
        [data-testid="stSidebar"] {
            background-color: #e9d5da;
        }
    </style>
""", unsafe_allow_html=True)

# Inserindo o logo na sidebar
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="font-size: 24px;">▶︎ •၊၊||၊|။|||| |</h1>
    </div>
""", unsafe_allow_html=True)

# Sidebar: Título e opções de análise
st.sidebar.title("Menu de Análises")
analise = st.sidebar.radio(
    "Escolha uma análise:", 
    ["🏠 Home", "📀 Top Álbuns", "✨ Top Músicas", "📈 Evolução"]
)

# ------------------------------------------------------------------------------
# FUNÇÃO PARA CARREGAR DADOS
# ------------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    artistas = ["Beyoncé", "Taylor Swift"]
    dados_albuns, dados_musicas, dados_evolucao = [], [], []

    for artista in artistas:
        artista_id = get_artist_id(artista)
        albuns = get_artist_albums(artista_id)

        for album in albuns:
            ano = int(album["release_date"][:4])
            
            # Se não houver imagens, usamos um placeholder
            album_image_url = album["images"][0]["url"] if album.get("images") else "https://via.placeholder.com/64"

            faixas = get_album_tracks(album["id"])
            popularidades = get_tracks_popularity([faixa["id"] for faixa in faixas])
            media_pop = sum(popularidades) / len(popularidades)

            dados_albuns.append({
                "Artista": artista,
                "Álbum": album["name"],
                "Ano": ano,
                "Popularidade": round(media_pop, 2),
                "Imagem": album_image_url
            })

            for faixa, pop in zip(faixas, popularidades):
                dados_musicas.append({
                    "Artista": artista,
                    "Música": faixa["name"],
                    "Álbum": album["name"],
                    "Ano": ano,
                    "Popularidade": round(pop, 2),
                    "Imagem": album_image_url
                })

            dados_evolucao.append({
                "Artista": artista,
                "Ano": ano,
                "Popularidade": round(media_pop, 2)
            })

    albuns_df = pd.DataFrame(dados_albuns)
    musicas_df = pd.DataFrame(dados_musicas)
    evolucao_df = pd.DataFrame(dados_evolucao)

    return albuns_df, musicas_df, evolucao_df

albuns_df, musicas_df, evolucao_df = carregar_dados()

# ------------------------------------------------------------------------------
# PÁGINAS DO DASHBOARD
# ------------------------------------------------------------------------------
# Página Inicial
# ------------------------------------------------------------------------------
if analise == "🏠 Home":
    st.title("🎧 Beyoncé vs. Taylor Swift")
    st.subheader("Comparativos de Popularidade no Spotify")

    st.markdown("""
Este dashboard utiliza dados extraídos diretamente da API oficial do Spotify para comparar álbuns, músicas e tendências de popularidade das artistas **Beyoncé** e **Taylor Swift**.

##### 🔍 O que é a métrica de Popularidade do Spotify?

A **popularidade** é uma métrica oficial do Spotify que varia entre **0 e 100**. Ela é calculada considerando não apenas o número total de reproduções de uma faixa ou álbum, mas também a frequência recente com que foi tocado. Quanto mais recente e frequente a reprodução, maior será a pontuação de popularidade.

##### 📌 Por que usar a popularidade do Spotify?

Essa métrica oferece uma visão precisa e dinâmica das tendências atuais, permitindo análises detalhadas sobre o desempenho recente das artistas. Isso ajuda a identificar sucessos emergentes e a comparar o impacto das músicas ao longo do tempo.

👉 Confira a documentação [**aqui!**](https://developer.spotify.com/documentation/web-api/reference/get-track)
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TOP ÁLBUNS
# ------------------------------------------------------------------------------
elif analise == "📀 Top Álbuns":
    st.header("Comparativo de Álbuns")

    # Filtros para seleção de múltiplos álbuns
    col1, col2 = st.columns(2)
    with col1:
        beyonce_albums = albuns_df[albuns_df["Artista"] == "Beyoncé"]["Álbum"].unique()
        beyonce_selected = st.multiselect(
            "Selecione um(s) álbum(ns) da Beyoncé",
            sorted(beyonce_albums),
            default=sorted(beyonce_albums)[:1]
        )
    with col2:
        taylor_albums = albuns_df[albuns_df["Artista"] == "Taylor Swift"]["Álbum"].unique()
        taylor_selected = st.multiselect(
            "Selecione um(s) álbum(ns) da Taylor Swift",
            sorted(taylor_albums),
            default=sorted(taylor_albums)[:1]
        )

    # Filtra os álbuns selecionados para ambas as artistas
    filtrado = albuns_df[
        ((albuns_df["Artista"] == "Beyoncé") & (albuns_df["Álbum"].isin(beyonce_selected))) |
        ((albuns_df["Artista"] == "Taylor Swift") & (albuns_df["Álbum"].isin(taylor_selected)))
    ].copy()

    # 1) Coluna para o gráfico (texto puro, sem HTML)
    filtrado["AlbumChart"] = filtrado["Álbum"]

    # 2) Coluna HTML para a TABELA (com a imagem embutida)
    filtrado["AlbumHTML"] = filtrado.apply(
        lambda row: (
            f'<img src="{row["Imagem"]}" style="width:25px; border-radius:50%; margin-right:5px; vertical-align:middle" /> {row["Álbum"]}'
        ),
        axis=1
    )

    # GRÁFICO (usando "AlbumChart" para não exibir HTML)
    fig = px.bar(
        filtrado,
        x="AlbumChart",
        y="Popularidade",
        color="Artista",
        barmode="group",
        text="Popularidade",
        color_discrete_map={"Beyoncé": "#1f77b4", "Taylor Swift": "#9467bd"}
    )
    fig.update_xaxes(type="category")  # Força o eixo X a ser categórico
    fig.update_layout(yaxis_title="Popularidade", xaxis_title="Álbum")
    st.plotly_chart(fig, use_container_width=True)

    # TABELA (usando "AlbumHTML")
    df_tabela = filtrado[["Artista", "AlbumHTML", "Ano", "Popularidade"]].copy()
    df_tabela.rename(columns={"AlbumHTML": "Álbum"}, inplace=True)
    df_tabela.drop(columns=["Imagem", "AlbumChart"], inplace=True, errors="ignore")

    # Ordena a tabela por Popularidade de forma decrescente
    df_tabela.sort_values("Popularidade", ascending=False, inplace=True)

    st.write(df_tabela.to_html(index=False, escape=False), unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TOP MÚSICAS
# ------------------------------------------------------------------------------
elif analise == "✨ Top Músicas":
    st.header("Comparativo de Músicas")

    # Filtros de Álbum
    col1, col2 = st.columns(2)
    with col1:
        beyonce_albums = musicas_df[musicas_df["Artista"] == "Beyoncé"]["Álbum"].unique()
        beyonce_selected_album = st.selectbox(
            "Selecione um álbum da Beyoncé",
            sorted(beyonce_albums)
        )

    with col2:
        taylor_albums = musicas_df[musicas_df["Artista"] == "Taylor Swift"]["Álbum"].unique()
        taylor_selected_album = st.selectbox(
            "Selecione um álbum da Taylor Swift",
            sorted(taylor_albums)
        )

    # Filtros de Músicas (multiselect)
    col3, col4 = st.columns(2)
    with col3:
        beyonce_musicas = musicas_df[
            (musicas_df["Artista"] == "Beyoncé") &
            (musicas_df["Álbum"] == beyonce_selected_album)
        ]
        beyonce_song_names = beyonce_musicas["Música"].unique()
        beyonce_selected_songs = st.multiselect(
            "Selecione músicas da Beyoncé",
            sorted(beyonce_song_names)
        )

    with col4:
        taylor_musicas = musicas_df[
            (musicas_df["Artista"] == "Taylor Swift") &
            (musicas_df["Álbum"] == taylor_selected_album)
        ]
        taylor_song_names = taylor_musicas["Música"].unique()
        taylor_selected_songs = st.multiselect(
            "Selecione músicas da Taylor Swift",
            sorted(taylor_song_names)
        )

    # Concatena as músicas selecionadas
    filtrado = pd.concat([
        beyonce_musicas[beyonce_musicas["Música"].isin(beyonce_selected_songs)],
        taylor_musicas[taylor_musicas["Música"].isin(taylor_selected_songs)]
    ], ignore_index=True).copy()

    if filtrado.empty:
        st.warning("Nenhuma música selecionada.")
    else:
        # 1) Coluna para o gráfico (Música pura, sem HTML)
        filtrado["MusicChart"] = filtrado["Música"]

        # 2) Coluna HTML para a TABELA (imagem do álbum ao lado do nome do ÁLBUM)
        filtrado["AlbumHTML"] = filtrado.apply(
            lambda row: (
                f'<img src="{row["Imagem"]}" '
                'style="width:25px; border-radius:50%; margin-right:5px; vertical-align:middle" />'
                f'{row["Álbum"]}'
            ),
            axis=1
        )

        # GRÁFICO (sem imagens, usando "MusicChart")
        fig = px.bar(
            filtrado,
            y="MusicChart",
            x="Popularidade",
            color="Artista",
            orientation='h',
            text="Popularidade",
            color_discrete_map={"Beyoncé": "#1f77b4", "Taylor Swift": "#9467bd"}
        )
        fig.update_layout(
            yaxis_title="Música",
            xaxis_title="Popularidade",
            yaxis={"categoryorder": "total ascending"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # TABELA (exibe a imagem do álbum ao lado do nome do álbum)
        # Remove "Imagem" e "MusicChart" para não exibir colunas extras
        df_tabela = filtrado[["Artista", "AlbumHTML", "Música", "Ano", "Popularidade"]].copy()
        df_tabela.rename(columns={"AlbumHTML": "Álbum"}, inplace=True)
        df_tabela.drop(columns=["Imagem", "MusicChart"], inplace=True, errors="ignore")

        st.write(df_tabela.to_html(index=False, escape=False), unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# EVOLUÇÃO TEMPORAL
# ------------------------------------------------------------------------------
elif analise == "📈 Evolução":
    st.header("Evolução de Popularidade")
    
    # Filtra dados apenas depois de 2017
    evolucao_filtrado = evolucao_df[evolucao_df["Ano"] > 2017].copy()
    
    # Remove a dimensão "Álbum" agrupando por Ano e Artista (agregando a popularidade)
    evolucao_filtrado = evolucao_filtrado.groupby(["Ano", "Artista"], as_index=False).agg({"Popularidade": "mean"})
    
    # Para o gráfico, ordena por ano (crescente)
    evolucao_chart = evolucao_filtrado.sort_values("Ano")
    fig = px.line(
        evolucao_chart,
        x="Ano",
        y="Popularidade",
        color="Artista",
        markers=True,
        title="Evolução da Popularidade",
        color_discrete_map={"Beyoncé": "#1f77b4", "Taylor Swift": "#9467bd"}
    )
    fig.update_layout(yaxis_title="Popularidade", xaxis_title="Ano")
    st.plotly_chart(fig, use_container_width=True)
    
    # Para a tabela, ordena de forma decrescente por Popularidade
    evolucao_tabela = evolucao_filtrado.sort_values("Popularidade", ascending=False)
    
    # Arredonda a coluna de Popularidade para 2 casas decimais
    evolucao_tabela["Popularidade"] = evolucao_tabela["Popularidade"].round(2)
    
    st.write(evolucao_tabela.to_html(index=False, escape=False), unsafe_allow_html=True)

