import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuração da Página (Sempre o primeiro comando Streamlit)
st.set_page_config(
    page_title="Showcase Streamlit",
    page_icon="✨",
    layout="wide", # Usa a tela toda
    initial_sidebar_state="expanded"
)

# 2. Barra Lateral (Sidebar)
with st.sidebar:
    st.image("https://docs.streamlit.io/logo.svg", width=150)
    st.title("Menu de Controle")
    st.write("Use esta barra para filtros globais.")
    
    # Exemplo de widget na sidebar
    tema_escolhido = st.selectbox("Escolha um tema de dados:", ["Vendas", "Marketing", "RH"])
    st.info(f"Você está visualizando o módulo: **{tema_escolhido}**")

# 3. Cabeçalho Principal
st.title("🚀 Explorador de Comandos Streamlit")
st.markdown("Uma interface de exemplo baseada nos melhores comandos do **Cheat Sheet**.")
st.divider() # Linha horizontal elegante

# 4. Organização em Abas (Tabs)
aba1, aba2, aba3 = st.tabs(["📊 Dados & Métricas", "🎛️ Widgets Interativos", "💬 Status & Layouts"])

# --- ABA 1: Dados e Métricas ---
with aba1:
    st.header("Exibição de Dados")
    
    # Colunas para métricas (estilo Dashboard)
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Receita Total", value="R$ 1.2M", delta="15%")
    col2.metric(label="Novos Usuários", value="4,320", delta="-2%")
    col3.metric(label="Tempo de Sessão", value="4m 12s", delta="10%")
    
    st.write("---")
    
    # Gerando dados fictícios
    df = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Taxa A', 'Taxa B', 'Taxa C']
    )
    
    col_tabela, col_grafico = st.columns([1, 2]) # A segunda coluna é duas vezes maior
    
    with col_tabela:
        st.subheader("Dataframe Interativo")
        # st.dataframe permite ordenar e redimensionar colunas
        st.dataframe(df, use_container_width=True, height=250)
        
    with col_grafico:
        st.subheader("Gráfico Nativo Rápido")
        # Gráfico de linha nativo do Streamlit
        st.line_chart(df)

# --- ABA 2: Widgets Interativos ---
with aba2:
    st.header("Coletando inputs do usuário")
    st.write("O Streamlit atualiza a tela automaticamente quando você interage com um widget.")
    
    # Formulário para evitar recarregamento a cada clique
    with st.form("meu_formulario"):
        st.subheader("Cadastro Rápido")
        
        nome = st.text_input("Qual o seu nome?")
        idade = st.slider("Selecione sua idade", min_value=0, max_value=100, value=25)
        aceita_termos = st.checkbox("Aceito os termos e condições")
        
        # Botão de envio do formulário
        enviado = st.form_submit_button("Salvar Dados")
        
        if enviado:
            if aceita_termos:
                st.success(f"Dados salvos com sucesso, {nome}!")
                st.balloons() # Animação divertida na tela
            else:
                st.error("Você precisa aceitar os termos para continuar.")

# --- ABA 3: Status, Layouts e Expanders ---
with aba3:
    st.header("Organização Visual e Feedbacks")
    
    # Expander (Sanfona) para esconder detalhes opcionais
    with st.expander("Clique aqui para ver um segredo 🤫", expanded=False):
        st.write("Você pode colocar textos longos, gráficos ou explicações aqui dentro para não poluir a tela principal.")
        st.code("print('Hello World do Streamlit!')", language="python")
    
    st.write("---")
    st.subheader("Mensagens de Status")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("Operação realizada com sucesso! (st.success)")
        st.info("Aqui vai uma dica importante para o usuário. (st.info)")
    with col_b:
        st.warning("Cuidado: você está prestes a deletar um arquivo. (st.warning)")
        st.error("Erro crítico de conexão com o banco de dados. (st.error)")

    # Exemplo de carregamento (Spinner)
    if st.button("Simular Processamento Pesado"):
        import time
        with st.spinner('Aguarde, processando dados complexos...'):
            time.sleep(2) # Simula um delay de 2 segundos
        st.success("Processamento concluído!")
