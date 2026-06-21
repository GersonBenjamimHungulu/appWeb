import streamlit as st
import pandas as pd
import os


# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA WEB
# ==============================================================================
# Define o título da aba do navegador, o ícone e o alinhamento da página.
st.set_page_config(
    page_title="Portal de Notas de Computadores no Ensino - Consulta Privada",
    page_icon="🎓",
    layout="centered" # Garante que o conteúdo fique centralizado e focado
)

# ==============================================================================
# 2. FUNÇÃO PARA CARREGAR OS DADOS DO EXCEL
# ==============================================================================
# O decorador @st.cache_data evita que o Streamlit leia o arquivo Excel do zero
# toda vez que a página recarregar, tornando a aplicação muito mais rápida.
@st.cache_data
def carregar_dados_excel():
    import os
    caminho_atual = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    caminho_excel = os.path.join(caminho_atual, "notas.xlsx")
    
    try:
        # 1. Lê o arquivo Excel tratando os dados como texto
        dados = pd.read_excel(caminho_excel, dtype=str)
        
        # 2. Limpa os espaços invisíveis originais de todas as colunas
        dados.columns = dados.columns.str.strip()
        
        # CORREÇÃO: Altera apenas os 2 primeiros nomes de forma segura sem destruir os seguintes
        colunas_existentes = list(dados.columns)
        if len(colunas_existentes) >= 1:
            colunas_existentes[0] = "N.º Estudante"
        if len(colunas_existentes) >= 2:
            colunas_existentes[1] = "Nome do Estudante"
        if len(colunas_existentes) >= 3:
            colunas_existentes[2] = "TrabSubmetido"  
        if len(colunas_existentes) >= 4:
            colunas_existentes[3] = "NotaDefesa"
        if len(colunas_existentes) >= 5:
            colunas_existentes[4] = "NotaFinal(30%)"
        if len(colunas_existentes) >= 6:
            colunas_existentes[5] = "PParcelar(70%)"          
            
        dados.columns = colunas_existentes
        
        # 3. Limpa espaços em branco dentro dos dados de todas as colunas
        for col in dados.columns:
            dados[col] = dados[col].str.strip()
            
        return dados
    except Exception as e:
        st.error(f"Erro ao processar os dados do Excel: {e}")
        return None

# Executa a função e guarda a tabela de dados na variável 'df'
df = carregar_dados_excel()

# ==============================================================================
# 3. INTERFACE VISUAL (CABEÇALHO)
# ==============================================================================
st.title("🎓 Consulta de Notas Individual")
st.write("Bem-vindo ao portal do prof GERSON B HUNGULU para unidade curricular Computadores no Ensino")
st.write("Insira o seu número de estudante abaixo para verificar as suas notas")
# Verifica se o arquivo Excel foi carregado com sucesso antes de continuar
if df is None:
    st.error("⚠️ Erro crítico: O ficheiro 'notas.xlsx' não foi encontrado na pasta do projeto.")
    st.info("Por favor, certifique-se de colocar o seu ficheiro Excel com o nome exato de 'notas.xlsx' no mesmo diretório deste script.")
else:
    # ==============================================================================
    # 4. CAMPO DE PESQUISA (INPUT)
    # ==============================================================================
    # Cria uma caixa de texto para o estudante digitar o número. 
    # O .strip() remove espaços acidentais que o utilizador possa digitar antes ou depois.
# Caixa de pesquisa para o número de estudante
    # O número aparece apenas como uma sugestão cinzenta dentro da caixa
    numero_pesquisa = st.text_input("Digite o seu N.º de Estudante:", placeholder="Ex: 14106690").strip()
    

    if numero_pesquisa:
        if df is not None:
            # Garante que estamos a comparar texto com texto de forma segura
            df["N.º Estudante"] = df["N.º Estudante"].astype(str)
        
            # Faz a filtragem do aluno
            estudante_filtrado = df[df["N.º Estudante"] == numero_pesquisa]
        
            # Mostra os resultados se encontrar o aluno
            if not estudante_filtrado.empty:
                st.success(f"Notas encontradas para o número {numero_pesquisa}!")
                st.dataframe(estudante_filtrado)
            else:
                st.warning("Número de estudante não encontrado na base de dados. Verifique se digitou corretamente.")
        else:
            st.error("Não foi possível realizar a pesquisa porque a base de dados não foi carregada.")

# --- RODAPÉ DO PROJECTO DE EXTENSÃO ---
st.markdown("---")  # Linha horizontal divisória

# Cria três colunas alinhadas para os dados de contacto
col_autor, col_email, col_tel = st.columns(3)

with col_autor:
    st.caption("✍️ **Autor:**")
    st.write("Gerson B. Hungulu")

with col_email:
    st.caption("📧 **E-mail:**")
    # Link HTML 'mailto' para abrir o gestor de e-mail automaticamente
    st.markdown(
        '<a href="mailto:gersonbenjamim@gmail.com" target="_blank" style="color: #1F618D; text-decoration: none; font-weight: bold;">gersonbenjamim@gmail.com</a>', 
        unsafe_allow_html=True
    )

with col_tel:
    st.caption("📞 **Telefone / WhatsApp:**")
    # Link HTML 'wa.me' para abrir diretamente a conversa no WhatsApp
    st.markdown(
        '<a href="https://wa.me/244927527339" target="_blank" style="color: #239B56; text-decoration: none; font-weight: bold;">+244 927 527 339</a>', 
        unsafe_allow_html=True
    )