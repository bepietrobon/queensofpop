# 🎧 **Spotify Data - Taylor vs. Beyoncé** 

📊 **Dashboard interativo** criado com **Streamlit**, que analisa a popularidade da discografia de **Taylor Swift** e **Beyoncé** usando a **API do Spotify**.

Acesse aqui: [queensofpop.streamlit.app/](https://queensofpop.streamlit.app/)


## 🎯 **Objetivo**  
O projeto visa criar uma **análise comparativa da popularidade** de **Taylor Swift e Beyoncé no Spotify**, explorando suas músicas e álbuns.

## 📍 **Funcionalidades Implementadas**  

### 🔹 **Configuração Básica**  
- Conexão com a API do Spotify  
- Configuração de credenciais no código  
- Funções de utilidade para extração de dados  

### 🔹 **Análises Básicas**   
- Comparação de popularidade entre álbuns  
- Comparação de popularidade entre músicas  
- Comparação da evolução de popularidade entre as artistas

## 💭 **Análises Futuras**  

- Matriz de correlação por características
- Análise de sentimento das letras
- Características técnicas por álbum
- Clustering de músicas por características
- Rankings específicos (dançantes, energéticas)
- Tendências temporais na popularidade

## 💻 **Tecnologias Utilizadas**  

- **Python**  
- **Streamlit** (Interface interativa)  
- **Spotipy** (Biblioteca para Spotify API)  
- **Pandas** (Manipulação de dados)  
- **Matplotlib & Seaborn** (Visualização de dados)  
- **NumPy** (Cálculos matemáticos)  
- **Plotly** (Gráficos interativos)  



## ⚠️ **Dependências**  

Para rodar o projeto localmente, instale as dependências com:

```sh
pip install streamlit spotipy pandas matplotlib seaborn numpy plotly
```



## 📙 **Como Usar**  

**1. Clone o repositório**  
```sh
git clone https://github.com/seu-usuario/spotify-data.git
cd spotify-data
```

**2. Instale as dependências**  
```sh
pip install -r requirements.txt
```

**3. Configure suas credenciais do Spotify**  
Crie um arquivo `.streamlit/secrets.toml` e adicione suas credenciais da API do Spotify:

```toml
CLIENT_ID = "seu_client_id"
SECRET_ID = "seu_client_secret"
```

**4. Execute o Streamlit**  
```sh
streamlit run app.py
```
O app abrirá automaticamente no navegador.



## 📂 **Notas**  

⚠️ **Limites da API do Spotify** – A API do Spotify possui restrições de taxa de requisição. Se você fizer muitas solicitações em pouco tempo, pode precisar aguardar um pouco antes de continuar.  

⚠️ **Credenciais seguras** – Nunca compartilhe suas credenciais públicas. Se estiver fazendo deploy no **Streamlit Community Cloud**, configure-as na aba **Secrets**.  

⚠️ **Dados dinâmicos** – A popularidade das músicas no Spotify muda constantemente, então os resultados podem variar ao longo do tempo.  



## 📝 **Licença**  

Este projeto está sob a licença **MIT** – veja o arquivo [`LICENSE`](LICENSE) para mais detalhes.  

---
