# FILE: ai_strategy.py
# FUNZIONE: Connessione a Gemini AI e generazione dell'analisi tattica
# VERSIONE CLOUD: Sicurezza API tramite st.secrets

import google.generativeai as genai
import streamlit as st

# ==========================================
# CONFIGURAZIONE API GEMINI (MODALITÀ SICURA CLOUD)
# ==========================================
def genera_analisi_partita(partita_scelta):
    """
    Invia la partita a Gemini pescando la chiave segreta dalla cassaforte di Streamlit.
    """
    try:
        # 1. Il server cerca la chiave segreta nella cassaforte
        if "GEMINI_API_KEY" not in st.secrets:
            return "⚠️ Errore di Sicurezza: Manca la Chiave API di Gemini nella cassaforte di Streamlit (Secrets)."
            
        CHIAVE_API = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=CHIAVE_API)
        
        # 2. Connessione all'IA (Usiamo la versione pro, stabilissima)
        model = genai.GenerativeModel('gemini-pro')
        
        # 3. Il Prompt di addestramento
        prompt_addestramento = f"""
Sei il Match Analyst Capo dello staff tecnico del Napoli di Antonio Conte.
Scrivi un'analisi tattica clinica, oggettiva e altamente professionale per la partita: {partita_scelta}.

STRUTTURA OBBLIGATORIA (Usa esattamente questi 4 punti numerati e in grassetto):

1. **Lettura Strategica:** Analizza l'assetto (es. 3-4-2-1), le scelte iniziali, il pressing e la gestione degli spazi.
2. **Atteggiamento della Squadra:** Valuta l'intensità, la resilienza mentale e la tenuta difensiva.
3. **Comportamento dei Singoli:** (REGOLA DI FERRO: Devi ASSOLUTAMENTE nominare i giocatori reali dell'attuale rosa del Napoli, come Kvaratskhelia, Lukaku, McTominay, Lobotka, Anguissa, Di Lorenzo, Rrahmani, Buongiorno, Meret, Politano, ecc. NON usare MAI termini generici e anonimi come "un mediano", "un esterno" o "un difensore". Associa le giocate chiave, positive o negative, ai nomi reali degli atleti).
4. **Impatto Strategico:** Conclusioni sul lavoro di mister Conte e proiezioni per le prossime sfide.

TONO DI VOCE:
Serio, conciso, privo di frasi fatte. Usa un linguaggio calcistico tecnico di altissimo livello.
"""
        risposta = model.generate_content(prompt_addestramento)
        return risposta.text
        
    except Exception as e:
        return f"⚠️ Errore di comunicazione con il server AI.\n\nDettaglio tecnico: {e}"
