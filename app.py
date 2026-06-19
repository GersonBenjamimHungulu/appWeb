import streamlit as st
import pandas as pd

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
    try:
        # 1. Lê o arquivo normalmente
        dados = pd.read_excel("notas.xlsx")
        
        # TRUQUE DETECTIVE: Remove espaços invisíveis de TODOS os cabeçalhos do Excel
        dados.columns = dados.columns.str.strip()
        
        # 2. Agora que os cabeçalhos estão limpos, garantimos que o número vira texto
        dados["N.º Estudante"] = dados["N.º Estudante"].astype(str).str.strip()
        dados["Nome do Estudante"] = dados["Nome do Estudante"].str.strip()
        
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# Executa a função e guarda a tabela de dados na variável 'df'
df = carregar_dados_excel()

# ==============================================================================
# 3. INTERFACE VISUAL (CABEÇALHO)
# ==============================================================================
st.title("🎓 Consulta de Notas Individual")
st.write("Bem-vindo ao portal do prof Gerson B Hungulu. Insira o seu número de estudante abaixo para verificar as suas notas.")

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
    numero_pesquisa = st.text_input("Digite o seu N.º Estudante:", placeholder="Ex: 21184814").strip()

    # ==============================================================================
    # 5. LÓGICA DE PESQUISA E EXIBIÇÃO EM CASO DE SUCESSO
    # ==============================================================================
    # Se o utilizador tiver digitado algo no campo de pesquisa, entra nesta condição
    if numero_pesquisa:
        
        # Filtra a tabela (DataFrame) procurando onde o N.º Estudante é igual ao digitado
        estudante = df[df["N.º Estudante"] == numero_pesquisa]
        
        # Se o resultado não estiver vazio (.empty == False), significa que o aluno existe
        if not estudiante.empty:
            
            # Extrai os dados da primeira linha encontrada (índice 0)
            nome_aluno = estudante.iloc[0]["Nome do Estudante"]
            nota_trabalho = estudante.iloc[0]["Trabalho"]
            nota_defesa = estudante.iloc[0]["Defesa"]
            nota_final_trb = estudante.iloc[0]["Nota Final do Trabalho"]
            nota_parcelar = estudante.iloc[0]["Nota da última Parcelar"]
            
            # Mensagem de sucesso confirmando a identidade do estudante
            st.success(f"Resultados para: **{nome_aluno}**")
            st.markdown("---") # Linha horizontal divisória para organização visual
            
            # Criamos uma grelha de 2 colunas para exibir as notas lado a lado
            col1, col2 = st.columns(2)
            
            # Coluna 1: Notas de processo (Trabalho e Defesa)
            with col1:
                st.metric(label="📊 Nota do Trabalho", value=str(nota_trabalho))
                st.metric(label="🗣️ Nota da Defesa", value=str(nota_defesa))
            
            # Coluna 2: Notas finais (Nota do Trabalho Consolidada e Parcelar)
            with col2:
                st.metric(label="📝 Nota Final Trabalho", value=str(nota_final_trb))
                st.metric(label="🎯 Parcial / Parcelar", value=str(nota_parcelar))
                
            st.markdown("---")
            st.caption("Nota: 'F' indica falta ou não comparência à respetiva avaliação.")
            
        # Se o número digitado não corresponder a nenhuma linha do Excel
        else:
            st.error("❌ Número de estudante não encontrado no sistema. Verifique os dígitos e tente novamente.")