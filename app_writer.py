# PROMPT EVOLUTIVO COM FOCO EM ENGAJAMENTO
            prompt_evolutivo = f"""
            VOCÊ É UM ESCRITOR DE WEBNOVELS E DIRETOR DE VÍDEOS CURTOS.
            ESTA É A IDEIA GERAL: {ideia_geral}
            ESTE É O CONTEXTO DO QUE JÁ FOI ESCRITO: {st.session_state['contexto_acumulado']}
            
            SUA TAREFA:
            1. Escreva a PARTE {num_parte} da história (Romance/Drama). 
            2. Transforme em kit de produção:
               - Cenas com legendas (máx 15 palavras).
               - Para cada cena: 2 Prompts Flux (Inglês) + 1 Prompt Grok (Movimento em Inglês).
            
            3. FINALIZAÇÃO DE ENGAJAMENTO (MANDATÓRIO):
               Ao final da última cena desta parte, crie uma "Legenda de Fechamento" para o narrador. 
               Deve ser algo que instigue o público a interagir e seguir para não perder o desfecho.
               Exemplos de tom: "O que você faria no lugar dela? Comente e siga para a Parte {num_parte + 1}", "O segredo foi revelado... Curta e siga para ver o confronto final."

            DNA VISUAL: {dna_visual}
            
            FORMATO DE SAÍDA:
            [TEXTO NARRATIVO DA PARTE {num_parte}]
            (Texto aqui)

            [KIT DE PRODUÇÃO]
            Cena 1 | Legenda: "..." | Flux 1: "..." | Flux 2: "..." | Grok: "..."
            ...
            [FINALIZAÇÃO/CTA]
            Legenda Final: "(Texto de engajamento aqui)" | Flux: "(Imagem de impacto/suspense)" | Grok: "(Zoom lento dramático)"
            """
