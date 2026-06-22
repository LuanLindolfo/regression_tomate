import streamlit as st
import pandas as pd
import numpy as np
import os
import kagglehub
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Inteligência Agrícola",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CARREGAMENTO E TREINAMENTO (COM CACHE)
# ==========================================
# O @st.cache_data evita que o Streamlit baixe e treine a IA toda vez que você clica em um botão
@st.cache_data
def carregar_e_treinar_dados():
    # 1. Download do Kaggle
    caminho_pasta = kagglehub.dataset_download("mathurinache/agricultura-digital")
    caminho_arquivo = os.path.join(caminho_pasta, "dataset_tomate.csv")
    
    # 2. Preparação
    df = pd.read_csv(caminho_arquivo)
    
    # Previsores (Dia 01) e Alvo (Dia 28)
    X = df.iloc[:, 7:10].values # NDVI_d01, SAVI_d01, GNDVI_d01
    Y = df.iloc[:, 2].values    # NDVI_d28
    
    X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, Y, test_size=0.3, random_state=42)
    
    # 3. Treinamento do Modelo Principal (Random Forest) para o Simulador
    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_rf.fit(X_treino, Y_treino)
    
    return df, modelo_rf, X_treino, X_teste, Y_treino, Y_teste

# Carrega os dados e o modelo na memória
df_tomate, modelo_principal, X_train, X_test, y_train, y_test = carregar_e_treinar_dados()

# ==========================================
# 3. BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("🍅 Painel Agtech")
    st.markdown("*Agricultura de Precisão*")
    st.divider()
    st.info("Plataforma de previsão de saúde do tomateiro para prevenção da Requeima (*Phytophthora infestans*).")
    st.metric("Lavouras Monitoradas", "12 Fazendas")
    st.metric("Economia Estimada de Defensivos", "32%")

# ==========================================
# 4. CABEÇALHO PRINCIPAL
# ==========================================
st.title("Painel de Previsão de Safra")
st.markdown("Transformando índices de vegetação em decisões estratégicas para o agronegócio.")
st.divider()

# ==========================================
# 5. ORGANIZAÇÃO EM ABAS
# ==========================================
aba1, aba2, aba3 = st.tabs(["📊 Visão Geral da Lavoura", "🤖 Simulador Preditivo", "⚙️ Desempenho da IA"])

# --- ABA 1: VISÃO GERAL ---
with aba1:
    st.header("Histórico de Leituras - Sensores Multiespectrais")
    
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    col_metric1.metric(label="Média NDVI Inicial (Dia 01)", value=f"{df_tomate['NDVI_d01'].mean():.2f}")
    col_metric2.metric(label="Média NDVI Final (Dia 28)", value=f"{df_tomate['NDVI_d28'].mean():.2f}")
    col_metric3.metric(label="Registros no Banco", value=f"{len(df_tomate)} plantas")
    
    st.write("---")
    
    col_tabela, col_grafico = st.columns([1, 2])
    with col_tabela:
        st.subheader("Base de Dados")
        st.dataframe(df_tomate[['id', 'NDVI_d01', 'SAVI_d01', 'GNDVI_d01', 'NDVI_d28']], height=300)
        
    with col_grafico:
        st.subheader("Evolução: Dia 01 vs Dia 28")
        st.scatter_chart(data=df_tomate, x='NDVI_d01', y='NDVI_d28', color='#ff4b4b')

# --- ABA 2: SIMULADOR PREDITIVO ---
with aba2:
    st.header("Previsão de Saúde da Planta (Regressão)")
    st.write("Insira as leituras de voo de drone de hoje (Dia 01) para prever a saúde da planta no Dia 28.")
    
    with st.form("form_previsao"):
        col_input1, col_input2, col_input3 = st.columns(3)
        
        with col_input1:
            ndvi_input = st.slider("NDVI (Dia 01)", min_value=0.50, max_value=0.90, value=0.75, step=0.01)
        with col_input2:
            savi_input = st.slider("SAVI (Dia 01)", min_value=0.80, max_value=1.30, value=1.10, step=0.01)
        with col_input3:
            gndvi_input = st.slider("GNDVI (Dia 01)", min_value=0.50, max_value=0.80, value=0.65, step=0.01)
            
        botao_prever = st.form_submit_button("Gerar Previsão para o Dia 28", type="primary")
        
        if botao_prever:
            # Organiza os dados de entrada
            entrada = np.array([[ndvi_input, savi_input, gndvi_input]])
            
            # Faz a previsão usando o Random Forest treinado
            previsao = modelo_principal.predict(entrada)[0]
            
            st.divider()
            st.subheader("Resultado da Previsão")
            
            col_res1, col_res2 = st.columns(2)
            col_res1.metric(label="NDVI Previsto (Dia 28)", value=f"{previsao:.4f}", delta=f"{(previsao - ndvi_input):.4f} em relação a hoje")
            
            # Lógica de negócio baseada no resultado
            with col_res2:
                if previsao > 0.75:
                    st.success("✅ Risco Baixo de Requeima. A planta manterá bom vigor. Não é necessária aplicação preventiva pesada.")
                elif previsao > 0.65:
                    st.warning("⚠️ Risco Moderado. Monitore o talhão. Recomendada aplicação localizada (Pulverização de Precisão).")
                else:
                    st.error("🚨 Alto Risco de Degradação (Requeima severa). Aplicação de defensivo urgente recomendada neste quadrante.")

# --- ABA 3: AVALIAÇÃO DE MODELOS ---
with aba3:
    st.header("Engenharia por Trás da Plataforma")
    st.write("Para garantir a precisão para o produtor rural, testamos vários algoritmos de Machine Learning. O erro absoluto médio (MAE) indica o quanto a previsão desvia da realidade.")
    
    if st.button("Executar Teste de Modelos (Benchmark)"):
        with st.spinner("Treinando e comparando algoritmos..."):
            
            # 1. Linear
            reg_lin = LinearRegression().fit(X_train, y_train)
            mae_lin = mean_absolute_error(y_test, reg_lin.predict(X_test))
            
            # 2. Árvore
            reg_tree = DecisionTreeRegressor().fit(X_train, y_train)
            mae_tree = mean_absolute_error(y_test, reg_
