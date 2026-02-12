import streamlit as st
import os
import io
import zipfile
from google import genai
from google.genai import types
from supabase import create_client, Client

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Fábrica 22.0 - Processador", layout="wide", page_icon="⚙️")
st.title("⚙️ Fábrica 22.0 - Processador de Roteiro")
st.markdown("*Transforme seu roteiro em Legendas, Prompts Flux (Imagens) e Prompts Grok (Animação).*")

# --- CONEXÃO SEGURA ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    supa_url = st.secrets["supabase"]["url"]
    supa_key = st.secrets["supabase"]["key"]
    
    client_gemini = genai.Client(api_key=api_key)
    supabase: Client = create_client(supa_url, supa_key)
except Exception as e:
    st.error("Erro nas chaves! Verifique os Secrets do Streamlit.")
    st.stop()

# --- INTERFACE ---
st.header("📽️ Iniciar Processamento")

col_info, col_input = st.columns([1, 2])

with col_info:
    st.info("""
    **Como funciona:**
    1. Cole seu roteiro completo ao lado.
    2. Defina o DNA Visual dos personagens.
    3. Clique em 'Processar' para fatiar em cenas de 6s.
    """)
    dna_personagens = st.text_area("🧬 DNA Visual (Ficha dos Personagens):", height=200, placeholder="Ex: Julian é loiro, olhos azuis, veste terno vitoriano. Ayla tem cabelos ruivos longos...")

with col_input:
    roteiro_colado = st.text_area("✒️ Cole seu Roteiro aqui:", height=300, placeholder="Cole aqui o texto que você já escreveu...")

if st.button("🚀 Processar e Gerar Prompts"):
    if not roteiro_colado:
        st.warning("O roteiro está vazio!")
    else:
        with st.spinner("Desmembrando roteiro e criando engenharia de prompts..."):
            
            # PROMPT TÉCNICO
            prompt_tecnico = f"""
            VOCÊ É UM ASSISTENTE DE PRODUÇÃO CINEMATOGRÁFICA.
            Sua tarefa é pegar o roteiro abaixo e transformá-lo em um kit de produção.

            REGRAS:
            1. Divida o texto em cenas curtas (cada legenda deve ter no máximo 15 palavras).
            2. Para CADA CENA, gere DOIS prompts de imagem diferentes para o FLUX (para variação).
            3. Para CADA CENA, gere UM prompt de animação para o GROK (focado em movimento de 6 segundos).

            CONTEXTO VISUAL (DNA): {dna_personagens}
            ROTEIRO: "{roteiro_colado}"

            FORMATO DE SAÍDA:
            [CENA X]
            Legenda: "Texto da narração"
            Flux Prompt 1: "Descrição visual detalhada em inglês"
            Flux Prompt 2: "Descrição visual alternativa em inglês"
            Grok Prompt: "Instrução de movimento em inglês para 6 segundos"
            ---
            """
            
            try:
                response = client_gemini.models.generate_content(model="gemini-2.0-flash", contents=prompt_tecnico)
                resultado_texto = response.text
                
                st.divider()
                st.subheader("✅ Kit de Produção Gerado")
                st.text_area("Resultado (Pronto para copiar):", value=resultado_texto, height=500)
                
                # ZIP para baixar
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
                    zf.writestr("kit_producao_completo.txt", resultado_texto)
                
                st.download_button("📦 Baixar Kit (.txt)", zip_buffer.getvalue(), "kit_producao.zip")
                
            except Exception as e:
                st.error(f"Erro no processamento da IA: {e}")
