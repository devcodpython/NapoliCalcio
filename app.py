# FILE: app.py
# FUNZIONE: Web-App Responsiva Streamlit - Tema Napoli
# GRAFICA PREMIUM AZZURRO TOTALE CON CSS PERSONALIZZATO E ICONA UFFICIALE

import streamlit as st
import ai_strategy
import requests
from bs4 import BeautifulSoup
import re

# ==========================================
# FUNZIONE: WEB SCRAPING "BISTURI" (LOGICA INVARIATA)
# ==========================================
def pulisci_nome_squadra(nome_sporco):
    parole = nome_sporco.strip().split()
    parole_pulite = list(dict.fromkeys(parole)) 
    parole_da_ignorare = ['serie', 'a', 'champions', 'league', 'coppa', 'italia', 'sabato', 'domenica']
    parole_filtrate = [p for p in parole_pulite if p.lower() not in parole_da_ignorare]
    return " ".join(parole_filtrate).strip()

@st.cache_data(ttl=3600)
def recupera_ultime_partite_online():
    siti_da_testare = [
        "https://www.tuttonapoli.net/calendario/",
        "https://sport.sky.it/calcio/squadre/napoli/risultati",
        "https://www.gazzetta.it/Calcio/Serie-A/squadre/napoli/calendario-risultati/"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for url in siti_da_testare:
        storico_completo = []
        competizione_corrente = "Altre"
        try:
            risposta = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(risposta.text, 'html.parser')
            for elemento in soup.find_all(['h2', 'h3', 'h4', 'tr', 'li', 'div', 'p', 'th']):
                testo_grezzo = elemento.get_text(separator=" ", strip=True)
                testo_lower = testo_grezzo.lower()
                
                if "serie a" in testo_lower: competizione_corrente = "Serie A"
                elif "coppa italia" in testo_lower: competizione_corrente = "Coppa Italia"
                elif "champions" in testo_lower: competizione_corrente = "Champions"
                
                if 'Napoli' in testo_grezzo and re.search(r'\d+\s*-\s*\d+', testo_grezzo) and len(testo_grezzo) < 100:
                    match = re.search(r'([A-Za-zÀ-ÿ\s\.\']+)\s+(\d+)\s*-\s*(\d+)\s+([A-Za-zÀ-ÿ\s\.\']+)', testo_grezzo)
                    if match:
                        sq_casa = pulisci_nome_squadra(match.group(1))
                        gol_casa = match.group(2)
                        gol_trasf = match.group(3)
                        sq_trasf = pulisci_nome_squadra(match.group(4))
                        partita_formattata = f"{sq_casa} {gol_casa} - {gol_trasf} {sq_trasf}"
                        
                        if "Napoli" in partita_formattata and sq_casa and sq_trasf:
                            voce = {"comp": competizione_corrente, "match": partita_formattata}
                            if voce not in storico_completo:
                                storico_completo.append(voce)
                                
            if len(storico_completo) >= 5:
                risultato_diviso = {"Tutte": [], "Serie A": [], "Champions": [], "Coppa Italia": []}
                storico_completo.reverse()
                for item in storico_completo:
                    match = item["match"]
                    comp = item["comp"]
                    if len(risultato_diviso["Tutte"]) < 5 and match not in risultato_diviso["Tutte"]:
                        risultato_diviso["Tutte"].append(match)
                    if comp in risultato_diviso and len(risultato_diviso[comp]) < 5 and match not in risultato_diviso[comp]:
                        risultato_diviso[comp].append(match)
                return risultato_diviso

        except Exception as e:
            continue 
            
    return {
        "Tutte": ["Verona 1 - 2 Napoli", "Napoli 2 - 1 Juventus", "Inter 1 - 1 Napoli"],
        "Serie A": ["Verona 1 - 2 Napoli", "Napoli 2 - 1 Juventus", "Inter 1 - 1 Napoli"],
        "Champions": ["Real Madrid 2 - 2 Napoli", "Napoli 1 - 0 Braga"],
        "Coppa Italia": ["Napoli 1 - 1 Como"]
    }

# ==========================================
# INTERFACCIA WEB: DESIGN PREMIUM AZZURRO
# ==========================================
def main():
    # MODIFICA APPORTATA QUI: Inserito logo_napoli.png al posto della pallina
    st.set_page_config(page_title="Napoli AI Analyst", page_icon="logo_napoli.png", layout="wide")

    # INIEZIONE CSS: Trucco da Web Designer per rivoluzionare i colori di Streamlit
    st.markdown("""
        <style>
        /* Sfondo totale azzurro Napoli */
        .stApp {
            background-color: #005DA8 !important;
        }
        .stApp header {
            background-color: transparent !important;
        }
        /* Forza tutti i testi al bianco */
        html, body, p, h1, h2, h3, h4, h5, h6, span, label, div {
            color: white !important;
        }
        
        /* Bordo bianco esclusivo per la PRIMA colonna (Sinistra) */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) {
            border: 2px solid white;
            border-radius: 15px;
            padding: 25px;
            background-color: rgba(255, 255, 255, 0.05); /* Leggera trasparenza */
        }

        /* Pulsante "Genera Analisi": Bianco con testo AZZURRO e hover elegante */
        [data-testid="stButton"] button {
            background-color: white !important;
            color: #005DA8 !important;
            font-weight: bold !important;
            font-size: 20px !important;
            border-radius: 10px !important;
            border: 2px solid white !important;
            padding: 15px !important;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
        }
        [data-testid="stButton"] button:hover {
            background-color: #f0f0f0 !important;
            transform: scale(1.02);
            transition: 0.2s;
        }

        /* Il Logo Matematico a Cerchi Concentrici (Solo bordi bianchi e sfondo trasparente) */
        .logo-n {
            width: 140px; height: 140px;
            background-color: transparent;
            border: 6px solid white;
            border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            color: white; font-size: 80px; font-weight: bold; font-family: Arial, sans-serif;
            margin: 0 auto;
            position: relative;
        }
        .logo-n::before {
            content: '';
            position: absolute;
            top: 6px; left: 6px; right: 6px; bottom: 6px;
            border: 2px solid white;
            border-radius: 50%;
        }
        
        /* Stile per i container con bordi (Box Analisi) */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 2px solid white !important;
            border-radius: 15px !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            padding: 20px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Divisione in due metà (Su PC fianco a fianco, su Smartphone impilate)
    colonna_sinistra, colonna_destra = st.columns([1, 2], gap="large")

    # ==========================================
    # COLONNA SINISTRA (MENU PARTITE)
    # ==========================================
    with colonna_sinistra:
        st.markdown("<h3 style='text-align: left; margin-top: 0;'>PARTITE GIOCATE</h3>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid white; margin-top: -10px;'>", unsafe_allow_html=True)
        
        dizionario_partite = recupera_ultime_partite_online()
        
        # Filtriamo le 3 voci richieste (mostra solo quelle che contengono dati)
        voci_richieste = ["Serie A", "Champions", "Coppa Italia"]
        voci_attive = [v for v in voci_richieste if len(dizionario_partite.get(v, [])) > 0]
        
        # Paracadute: se i siti non hanno i tag delle competizioni, mostriamo la voce Tutte
        if not voci_attive:
            voci_attive = ["Tutte"]
            
        competizione_scelta = st.radio("Seleziona la competizione:", voci_attive, horizontal=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        partita_selezionata = st.radio("Seleziona la partita:", dizionario_partite[competizione_scelta], label_visibility="collapsed")

    # ==========================================
    # COLONNA DESTRA/CENTRALE (LOGO, PULSANTE E ANALISI)
    # ==========================================
    with colonna_destra:
        st.markdown('<div class="logo-n">N</div>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-top: 15px; letter-spacing: 2px;'>NAPOLI CALCIO</h1>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Centriamo il pulsante nella colonna usando 3 sotto-colonne
        spazio_sx, col_bottone, spazio_dx = st.columns([1, 2, 1])
        with col_bottone:
            genera_cliccato = st.button("GENERA ANALISI", use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Il Box dell'Analisi (Appare solo se cliccato)
        if genera_cliccato:
            if partita_selezionata:
                with st.spinner("Analisi in corso..."):
                    analisi = ai_strategy.genera_analisi_partita(partita_selezionata)
                    
                    # Usa il container nativo di Streamlit, a cui abbiamo dato i bordi bianchi via CSS
                    with st.container(border=True):
                        st.markdown(f"### 📋 Report: {partita_selezionata}")
                        st.markdown("---")
                        st.write(analisi)
            else:
                st.warning("⚠️ Errore: Seleziona prima una partita dalla colonna di sinistra.")

if __name__ == "__main__":
    main()