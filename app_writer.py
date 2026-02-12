import streamlit as st
import io
import zipfile
from google import genai
from google.genai import types
from supabase import create_client, Client

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Fábrica 23.2 - Final", layout="wide", page_icon="🧬")
st.title("🧬 Fábrica 23.2 - Gerador com Engajamento")
st.markdown("*Automação de Roteiro: Legendas, Flux, Grok e Chamada para Ação.*")

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

# --- ESTADO DA SESSÃO ---
if 'historia_partes' not in st.session_state:
    st.session_state['historia_partes'] = []
if 'contexto_acumulado' not in st.session_state:
    st.session_state['contexto_acumulado'] = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎬 O Plot")
    ideia_geral = st.text_area("Ideia Geral (Início, Meio e Fim):", height=150)
    dna_visual = st.text_area("🧬 DNA Visual:", placeholder="Julian é loiro... Ayla tem cabelos ruivos...")
    
    if st.button("🗑️ Resetar História"):
        st.session_state['historia_partes'] = []
        st.session_state['contexto_acumulado'] = ""
        st.rerun()

# --- ÁREA PRINCIPAL ---
st.header("🚀 Linha de Produção")

if not ideia_geral:
    st.info("👈 Comece descrevendo sua ideia geral na barra lateral.")
else:
    num_parte = len(st.session_state['historia_partes']) + 1
    
    if st.button(f"✨ Gerar Parte {num_parte}"):
        with st.spinner(f"Escrevendo e processando a Parte {num_parte}..."):
            
            # PROMPT MESTRE (INDENTAÇÃO CORRIGIDA)
            prompt_evolutivo = f"""
            VOCÊ É UM ESCRITOR DE WEBNOVELS E DIRETOR DE VÍDEOS CURTOS.
            ESTA É A IDEIA GERAL DA HISTÓRIA: {ideia_geral}
            CONTEXTO DO QUE JÁ FOI ESCRITO: {st.session_state['contexto_acumulado']}
            
            SUA TAREFA:
            1. Escreva a PARTE {num_parte} da história (Romance/Drama com plot twist).
            2. Transforme essa parte em um kit de produção técnica:
               - Divida em cenas com legendas (máx 15 palavras por cena).
               - Para cada cena: 2 Prompts Flux (Inglês) + 1 Prompt Grok (Movimento em Inglês).
            
            3. FINALIZAÇÃO DE ENGAJAMENTO (MANDATÓRIO):
               Ao final da última cena desta parte, crie uma "Legenda de Fechamento" para o narrador. 
               Deve ser algo que instigue o público a interagir e seguir para não perder o desfecho.
               Exemplo: "O que você faria? Comente e siga para ver a Parte {num_parte + 1}."

            DNA VISUAL: {dna_visual}
            
            FORMATO DE SAÍDA:
            [TEXTO NARRATIVO DA PARTE {num_parte}]
            (Texto aqui)

            [KIT DE PRODUÇÃO]
            Cena 1 | Legenda: "..." | Flux 1: "..." | Flux 2: "..." | Grok: "..."
            ...
            [FINALIZAÇÃO/CTA]
            Legenda Final: "..." | Flux: "..." | Grok: "..."
            """
            
            try:
                response = client_gemini.models.generate_content(model="gemini-2.0-flash", contents=prompt_evolutivo)
                output = response.text
                
                st.session_state['historia_partes'].append(output)
                st.session_state['contexto_acumulado'] += f"\n\nPARTE {num_parte}:\n{output}"
            except Exception as e:
                st.error(f"Erro na IA: {e}")

    # EXIBIÇÃO
    for i, conteudo in enumerate(st.session_state['historia_partes']):
        with st.expander(f"📦 CONTEÚDO DA PARTE {i+1}", expanded=True):
            st.markdown(conteudo)
            st.download_button(
                label=f"📥 Baixar Kit Parte {i+1}",
                data=conteudo,
                file_name=f"parte_{i+1}_producao.txt",
                key=f"btn_{i}"
            )
