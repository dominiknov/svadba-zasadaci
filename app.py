import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

# 1. Nastavenie stránky
st.set_page_config(layout="wide", page_title="Svadobný Plánovač")
st.title("👑 Profesionálny Svadobný Plánovač")

DB_VERZIE = "svadba_verzie.json"
DB_HOSTIA = "svadba_hostia.json"

# --- SYSTÉM NAČÍTANIA / UKLADANIA HOSTÍ ---
def nacitaj_hosti():
    if not os.path.exists(DB_HOSTIA):
        povodny_zoznam = {
            "Dominik (Ženích)": "Mladomanzelia", "Kika (Nevesta)": "Mladomanzelia",
            "Mamka (Dominik)": "Moja strana", "Janko (Dominik)": "Moja strana", "Tomas (Dominik)": "Moja strana", 
            "Eva (Dominik)": "Moja strana", "Babulka (Dominik)": "Moja strana", "Pato (Dominik)": "Moja strana", 
            "Ivetka (Dominik)": "Moja strana", "Patko (Dominik)": "Moja strana", "Mato (Dominik)": "Moja strana", 
            "Stefi (Dominik)": "Moja strana", "Brigita (Dominik)": "Moja strana", "Brigitka (Dominik)": "Moja strana", 
            "Nilay (Dominik)": "Moja strana",
            "Mamka (Kika)": "Kika strana", "Ivka (Kika)": "Kika strana", "Palo (Kika)": "Kika strana", 
            "Ivka Stevo (Kika)": "Kika strana", "Gretka (Kika)": "Kika strana", "Pepe (Kika)": "Kika strana", 
            "Jozko (Kika)": "Kika strana", "Inga (Kika)": "Kika strana", "Babka thc (Kika)": "Kika strana", 
            "Babka (Kika)": "Kika strana", "Noi (Kika)": "Kika strana", "Arne (Kika)": "Kika strana", 
            "Sara (Kika)": "Kika strana", "Kekemama (Kika)": "Kika strana", "Gretka doprovod (Kika)": "Kika strana", 
            "Viki Inga (Kika)": "Kika strana", "Paľo ocko (Kika)": "Kika strana", "Paľo mamka (Kika)": "Kika strana",
            "Ila": "Kamosi", "Marek": "Kamosi", "Kaja": "Kamosi", "Oli": "Kamosi", "Nika": "Kamosi", 
            "Jozocko": "Kamosi", "Sasocko": "Kamosi", "Dusan": "Kamosi", "Peta": "Kamosi", "Ada": "Kamosi", 
            "Sofia": "Kamosi", "Tomas Sofi": "Kamosi", "Beki": "Kamosi", "Tomas Beki": "Kamosi", 
            "Dominik S.": "Kamosi", "Lucka": "Kamosi", "Viki B.": "Kamosi", "Viki B. BF": "Kamosi", 
            "Rasto": "Kamosi", "Vlado": "Kamosi", "Marko": "Kamosi", "Ivana": "Kamosi", "Danko Kocak": "Kamosi", 
            "Danova Naty": "Kamosi", "Biba": "Kamosi", "Jaro": "Kamosi"
        }
        with open(DB_HOSTIA, "w", encoding="utf-8") as f:
            json.dump(povodny_zoznam, f, ensure_ascii=False, indent=4)
    
    with open(DB_HOSTIA, "r", encoding="utf-8") as f:
        return json.load(f)

def uloz_hosti(data):
    with open(DB_HOSTIA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

guest_dict = nacitaj_hosti()
all_guests = sorted(list(guest_dict.keys()))

# --- SYSTÉM UKLADANIA VERZIÍ ZASADANIA ---
def naciataj_vsetky_verzie():
    if os.path.exists(DB_VERZIE):
        with open(DB_VERZIE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def uloz_verziu(nazov, data):
    vsetky = naciataj_vsetky_verzie()
    vsetky[nazov] = data
    with open(DB_VERZIE, "w", encoding="utf-8") as f:
        json.dump(vsetky, f, ensure_ascii=False, indent=4)

def get_default_seating():
    default = {}
    default["Hlavny_Stol_Miesto_1"] = "Janko (Dominik)" if "Janko (Dominik)" in guest_dict else "-- Voľné --"
    default["Hlavny_Stol_Miesto_2"] = "Mamka (Dominik)" if "Mamka (Dominik)" in guest_dict else "-- Voľné --"
    default["Hlavny_Stol_Miesto_3"] = "Dominik (Ženích)" if "Dominik (Ženích)" in guest_dict else "-- Voľné --"
    default["Hlavny_Stol_Miesto_4"] = "Kika (Nevesta)" if "Kika (Nevesta)" in guest_dict else "-- Voľné --"
    default["Hlavny_Stol_Miesto_5"] = "Mamka (Kika)" if "Mamka (Kika)" in guest_dict else "-- Voľné --"
    default["Hlavny_Stol_Miesto_6"] = "Palo (Kika)" if "Palo (Kika)" in guest_dict else "-- Voľné --"
    return default

if 'seating' not in st.session_state:
    st.session_state.seating = get_default_seating()

# Čistenie neexistujúcich hostí zo session state
for k, v in list(st.session_state.seating.items()):
    if v != "-- Voľné --" and v not in guest_dict:
        st.session_state.seating[k] = "-- Voľné --"

tab1, tab2 = st.tabs(["🗺️ Zasadací Poriadok", "👥 Správa Hostí"])

# ==========================================
# KARTA 1: ZASADACÍ PORIADOK
# ==========================================
with tab1:
    st.sidebar.header("💾 Správa Variácií")
    verzie = naciataj_vsetky_verzie()

    novy_nazov = st.sidebar.text_input("Názov novej variácie:")
    if st.sidebar.button("💾 Uložiť aktuálny stav"):
        if novy_nazov:
            uloz_verziu(novy_nazov, st.session_state.seating)
            st.sidebar.success(f"Uložené: {novy_nazov}")
            st.rerun()

    if verzie:
        vybrana_verzia = st.sidebar.selectbox("Vyber uloženú variáciu:", list(verzie.keys()))
        if st.sidebar.button("📂 Načítať variáciu"):
            st.session_state.seating = verzie[vybrana_verzia]
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("👥 Kto ešte nesedí?")
    
    used_guests = [val for val in st.session_state.seating.values() if val != "-- Voľné --"]
    unassigned_guests = ["-- Voľné --"] + [g for g in all_guests if g not in used_guests]

    for ug in unassigned_guests:
        if ug != "-- Voľné --":
            skupina = guest_dict.get(ug, "Neznáme")
            icon = "👑" if skupina == "Mladomanzelia" else "💙" if skupina == "Moja strana" else "💗" if skupina == "Kika strana" else "💚"
            st.sidebar.write(f"{icon} {ug}")

    st.subheader("🪑 Priraďovanie hostí k stolom")
    
    # OPRAVENÁ FUNKCIA: Target určuje, kam sa má vykresliť (stĺpec alebo samotný st). Ak target nie je definovaný, kreslí priamo.
    def render_single_seat_selector(t_label, t_id, seat_number, target=None):
        key = f"wkey_{t_id}_Miesto_{seat_number}"
        db_key = f"{t_id}_Miesto_{seat_number}"
        current_val = st.session_state.seating.get(db_key, "-- Voľné --")
        
        valid_options = [current_val] if current_val != "-- Voľné --" else []
        valid_options += [g for g in all_guests if g not in used_guests]
        if "-- Voľné --" not in valid_options:
            valid_options.append("-- Voľné --")
        
        valid_options = list(dict.fromkeys(valid_options))
        
        try:
            idx = valid_options.index(current_val)
        except ValueError:
            idx = 0
            
        # Vykreslenie do správneho kontajnera
        if target is not None:
            selected = target.selectbox(f"{t_label} M.{seat_number}", valid_options, index=idx, key=key)
        else:
            selected = st.selectbox(f"{t_label} M.{seat_number}", valid_options, index=idx, key=key)
            
        if selected != current_val:
            st.session_state.seating[db_key] = selected
            st.rerun()

    # 1. Hlavný stôl (Vykreslenie do 6 stĺpcov vedľa seba)
    st.markdown("### 👑 Hlavná zóna")
    h_cols = st.columns(6)
    for seat in range(1, 7):
        render_single_seat_selector("Hlavný stôl", "Hlavny_Stol", seat, target=h_cols[seat-1])

    st.markdown("---")
    st.markdown("### 🧮 Okrúhle stoly")
    cols = st.columns(3)
    
    round_tables = [
        {"label": "Stôl 3", "id": "Stol_3"},
        {"label": "Stôl 2", "id": "Stol_2"},
        {"label": "Stôl 1", "id": "Stol_1"},
        {"label": "Stôl 6", "id": "Stol_6"},
        {"label": "Stôl 5", "id": "Stol_5"},
        {"label": "Stôl 4", "id": "Stol_4"}
    ]
    
    for idx, t in enumerate(round_tables):
        with cols[idx % 3]:
            st.markdown(f"#### {t['label']}")
            for seat in range(1, 11):
                # Target definujeme ako konkrétny stĺpec z poľa 'cols'
                render_single_seat_selector(t["label"], t["id"], seat, target=cols[idx % 3])
