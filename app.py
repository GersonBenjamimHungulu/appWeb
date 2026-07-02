import streamlit as st
import pandas as pd
import os

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA WEB E CORES DA UNIVERSIDADE (uninbelogo.jpeg)
# ==============================================================================
st.set_page_config(
    page_title="Portal de Notas - Consulta Privada",
    page_icon="🎓",
    layout="centered"
)

# Estilização baseada nas cores do logo da UNINBE (Azul Escuro e Ouro/Laranja)
custom_css = """
    <style>
        /* Cor dos títulos principais */
        h1, h2, h3 {
            color: #1A5276 !important; /* Azul Institucional */
            font-family: 'Helvetica Neue', sans-serif;
        }
        /* Linhas divisórias e detalhes */
        hr {
            border-top: 2px solid #D4AC0D !important; /* Ouro/Laranja */
        }
        /* Customização secundária de texto de sucesso */
        .stAlert {
            border-left: 5px solid #1A5276 !important;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==============================================================================
# 2. FUNÇÃO PARA CARREGAR OS DADOS (DINÂMICA POR FICHEIRO)
# ==============================================================================
@st.cache_data
def carregar_dados(tipo_pauta):
    caminho_atual = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    
    try:
        if tipo_pauta == "Resumo da Época de Frequência 2025/2026":
            caminho_excel = os.path.join(caminho_atual, "Pautas 2025-2026.xlsx")
            # Lê especificamente a folha correta do novo ficheiro
            dados = pd.read_excel(caminho_excel, sheet_name="Computadores no Ensino", dtype=str)
            
            dados.columns = dados.columns.str.strip()
            colunas_existentes = list(dados.columns)
            
            # Mapeamento exato com base na imagem image_93d3ac.png
            mapeamento_pauta = [
                "N.º Estudante", "Nome do Estudante", "MOA", "1ªP", "2ªP", 
                "3ªP", "4ªP", "MAC", "Exame", "N. Final", "Recurso", "OBSERVAÇÃO"
            ]
            for i, nome_col in enumerate(mapeamento_pauta):
                if len(colunas_existentes) > i:
                    colunas_existentes[i] = nome_col
            dados.columns = colunas_existentes

        else:
            # Opção para o ficheiro antigo "notas.xlsx"
            caminho_excel = os.path.join(caminho_atual, "notas.xlsx")
            dados = pd.read_excel(caminho_excel, dtype=str)
            
            dados.columns = dados.columns.str.strip()
            colunas_existentes = list(dados.columns)
            
            # Mapeamento antigo do protótipo
            if len(colunas_existentes) >= 1: colunas_existentes[0] = "N.º Estudante"
            if len(colunas_existentes) >= 2: colunas_existentes[1] = "Nome do Estudante"
            if len(colunas_existentes) >= 3: colunas_existentes[2] = "TrabSubmetido"  
            if len(colunas_existentes) >= 4: colunas_existentes[3] = "NotaDefesa"
            if len(colunas_existentes) >= 5: colunas_existentes[4] = "NotaFinal(30%)"
            if len(colunas_existentes) >= 6: colunas_existentes[5] = "PParcelar(70%)"
            dados.columns = colunas_existentes

        # Limpa espaços em branco dentro de todas as células
        for col in dados.columns:
            dados[col] = dados[col].str.strip()
            
        return dados
    except Exception as e:
        st.error(f"Erro ao processar o ficheiro Excel ({tipo_pauta}): {e}")
        return None

# ==============================================================================
# 3. INTERFACE VISUAL E SELEÇÃO DE PREFERÊNCIA
# ==============================================================================
st.title("🎓 Consulta de Notas Individual")
st.subheader("Curso de Matemática — Computadores no Ensino")

# Caixa de seleção com os nomes atualizados
opcao_pauta = st.selectbox(
    "Selecione o documento que deseja consultar:",
    ["Resumo da Época de Frequência 2025/2026", "Nota do Trabalho / 4ª Prova Parcelar"]
)

st.write("Insira o seu número de estudante abaixo para verificar os seus resultados.")

# Carrega os dados correspondentes à escolha do utilizador
df = carregar_dados(opcao_pauta)

# Verifica se o arquivo Excel foi carregado com sucesso antes de continuar
if df is None:
    st.error(f"⚠️ Erro crítico: O ficheiro correspondente a '{opcao_pauta}' não foi encontrado ou está mal estruturado.")
    st.info("Por favor, certifique-se de que ambos os ficheiros ('Pautas 2025-2026.xlsx' e 'notas.xlsx') estão guardados no mesmo diretório deste script.")
else:
    # ==============================================================================
    # 4. CAMPO DE PESQUISA (INPUT)
    # ==============================================================================
    numero_pesquisa = st.text_input("Digite o seu N.º de Estudante:", placeholder="Ex: 17106690").strip()
    
    if numero_pesquisa:
        # Garante a comparação segura como string
        df["N.º Estudante"] = df["N.º Estudante"].astype(str)
    
        # Faz a filtragem do aluno
        estudante_filtrado = df[df["N.º Estudante"] == numero_pesquisa].copy()
    
        # CORREÇÃO DE INDENTAÇÃO: O bloco abaixo agora só executa SE houver pesquisa ativa
        if not estudante_filtrado.empty:
            st.success(f"Resultados encontrados!")
            
            # --- CORTE SELETIVO DE COLUNAS ---
            colunas_atuais = list(estudante_filtrado.columns)
            coluna_alvo = "OBSERVAÇÃO"
            
            if coluna_alvo in colunas_atuais:
                # Descobre a posição da coluna "OBSERVAÇÃO"
                indice_alvo = colunas_atuais.index(coluna_alvo)
                # Filtra mantendo apenas as colunas do início até ao índice da "OBSERVAÇÃO"
                colunas_filtradas = colunas_atuais[:indice_alvo + 1]
                estudante_filtrado = estudante_filtrado[colunas_filtradas]
            
            # --- LIMPEZA DE CÉLULAS NULAS ---
            # Oculta valores "none", "nan" ou células vazias mudando para texto limpo ""
            estudante_filtrado = estudante_filtrado.fillna("")
            for col in estudante_filtrado.columns:
                estudante_filtrado[col] = estudante_filtrado[col].apply(
                    lambda x: "" if str(x).lower() in ["none", "nan", "null"] else x
                )
            
            # Exibe a tabela estruturada e delimitada com base na regra
            st.dataframe(estudante_filtrado.set_index("N.º Estudante"), use_container_width=True)
        else:
            st.warning("Número de estudante não encontrado nesta base de dados. Verifique se digitou corretamente ou mude o documento acima.")

# --- RODAPÉ DO PROJECTO DE EXTENSÃO ---
st.markdown("---")  # Linha horizontal divisória

col_autor, col_email, col_tel = st.columns(3)

with col_autor:
    st.caption("✍️ **Desenvolvido por:**")
    st.write("Gerson B. Hungulu")

with col_email:
    st.caption("📧 **E-mail:**")
    st.markdown(
        '<a href="mailto:gersonbenjamim@gmail.com" target="_blank" style="color: #1A5276; text-decoration: none; font-weight: bold;">gersonbenjamim@gmail.com</a>', 
        unsafe_allow_html=True
    )

with col_tel:
    st.caption("📞 **Telefone / WhatsApp:**")
    st.markdown(
        '<a href="https://wa.me/244927527339" target="_blank" style="color: #D4AC0D; text-decoration: none; font-weight: bold;">+244 927 527 339</a>', 
        unsafe_allow_html=True
    )