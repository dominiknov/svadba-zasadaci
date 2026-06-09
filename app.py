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
    default["Hlavný stôl M.1"] = "Adrianka (Dominik)" if "Adrianka (Dominik)" in guest_dict else "-- Voľné --"
    default["Hlavný stôl M.2"] = "Mamka (Dominik)" if "Mamka (Dominik)" in guest_dict else "-- Voľné --"
    default["Hlavný stôl M.3"] = "Dominik (Ženích)" if "Dominik (Ženích)" in guest_dict else "-- Voľné --"
    default["Hlavný stôl M.4"] = "Kika (Nevesta)" if "Kika (Nevesta)" in guest_dict else "-- Voľné --"
    default["Hlavný stôl M.5"] = "Mamka (Kika)" if "Mamka (Kika)" in guest_dict else "-- Voľné --"
    default["Hlavný stôl M.6"] = "Palo (Kika)" if "Palo (Kika)" in guest_dict else "-- Voľné --"
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
    
    # Opravené generovanie kľúčov presne podľa tvojho screenshotu z PC
    def render_single_seat_selector(t_label, prefix_db, seat_number, target):
        key = f"widget_{prefix_db.replace(' ', '_')}_{seat_number}"
        db_key = f"{prefix_db} M.{seat_number}"
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
            
        selected = target.selectbox(f"{t_label} M.{seat_number}", valid_options, index=idx, key=key)
            
        if selected != current_val:
            st.session_state.seating[db_key] = selected
            st.rerun()

    # 1. Hlavný stôl (Zjednotené na malé "s" -> "Hlavný stôl")
    st.markdown("### 👑 Hlavná zóna")
    h_cols = st.columns(6)
    for seat in range(1, 7):
        render_single_seat_selector("Hlavný stôl", "Hlavný stôl", seat, target=h_cols[seat-1])

    st.markdown("---")
    st.markdown("### 🧮 Okrúhle stoly")
    cols = st.columns(3)
    
    round_tables = [
        {"label": "Stôl 3", "prefix": "Stôl 3"},
        {"label": "Stôl 2", "prefix": "Stôl 2"},
        {"label": "Stôl 1", "prefix": "Stôl 1"},
        {"label": "Stôl 6", "prefix": "Stôl 6"},
        {"label": "Stôl 5", "prefix": "Stôl 5"},
        {"label": "Stôl 4", "prefix": "Stôl 4"}
    ]
    
    for idx, t in enumerate(round_tables):
        grid_col = cols[idx % 3]
        with grid_col:
            st.markdown(f"#### {t['label']}")
            for seat in range(1, 11):
                render_single_seat_selector(t["label"], t["prefix"], seat, target=grid_col)

    # Vizualizácia (Mapa)
    st.markdown("---")
    st.subheader("🗺️ Živá Vizuálna Mapa Sály")
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_xlim(0, 20); ax.set_ylim(0, 10); ax.axis('off')

    def get_color(name):
        if name == "-- Voľné --": return '#ffffff'
        skupina = guest_dict.get(name, "")
        if skupina == "Mladomanzelia": return '#ffe599'
        if skupina == "Moja strana": return '#c9daf8'
        if skupina == "Kika strana": return '#f4cccc'
        return '#d9ead3'

    ax.add_patch(plt.Rectangle((5, 0.4), 10, 1.0, color='#e0e0e0', ec='#666666', lw=2))
    ax.text(10, 0.9, "👑 HLAVNÝ STÔL", ha='center', fontweight='bold', fontsize=11)
    
    for s_idx in range(6):
        p_name = st.session_state.seating.get(f"Hlavný stôl M.{s_idx+1}", "-- Voľné --")
        ax.text(5.8 + s_idx * 1.6, 0.6, p_name, fontsize=8, ha='center', va='center',
                bbox=dict(boxstyle='square,pad=0.2', facecolor=get_color(p_name), edgecolor='#999999'))

    coords = [
        {"prefix": "Stôl 3", "label": "Stôl 3", "x": 4.5, "y": 4.2},
        {"prefix": "Stôl 2", "label": "Stôl 2", "x": 10.0, "y": 4.2},
        {"prefix": "Stôl 1", "label": "Stôl 1", "x": 15.5, "y": 4.2},
        {"prefix": "Stôl 6", "label": "Stôl 6", "x": 4.5, "y": 7.8},
        {"prefix": "Stôl 5", "label": "Stôl 5", "x": 10.0, "y": 7.8},
        {"prefix": "Stôl 4", "label": "Stôl 4", "x": 15.5, "y": 7.8}
    ]

    for c in coords:
        ax.add_patch(plt.Circle((c["x"], c["y"]), 1.1, color='#f7f7f7', ec='#aaaaaa', lw=2))
        ax.text(c["x"], c["y"], c["label"], ha='center', va='center', fontweight='bold')
        angles = np.linspace(0, 2*np.pi, 10, endpoint=False) + np.pi/2
        for s_idx, angle in enumerate(angles):
            person = st.session_state.seating.get(f"{c['prefix']} M.{s_idx+1}", "-- Voľné --")
            if person != "-- Voľné --":
                ax.text(c["x"] + 1.55 * np.cos(angle), c["y"] + 1.45 * np.sin(angle), person, fontsize=7.5, ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor=get_color(person), edgecolor='#cccccc'))
    st.pyplot(fig)

# --- KARTA 2: SPRÁVA HOSTÍ ---
with tab2:
    st.subheader("➕ Pridať nového hosťa")
    c1, c2, c3 = st.columns([2, 2, 1])
    n_meno = c1.text_input("Meno:", key="input_novy_host_meno")
    n_skupina = c2.selectbox("Skupina:", ["Moja strana", "Kika strana", "Kamosi"], key="input_novy_host_skupina")
    if c3.button("➕ Pridať", key="btn_pridat_hosta"):
        if n_meno and n_meno not in guest_dict:
            guest_dict[n_meno] = n_skupina
            uloz_hosti(guest_dict)
            st.success(f"Pridaný: {n_meno}")
            st.rerun()
    
    st.markdown("---")
    st.subheader("🗑️ Zoznam a mazanie")
    for kat in ["Moja strana", "Kika strana", "Kamosi"]:
        st.write(f"**{kat}**")
        ludia = [m for m, s in guest_dict.items() if s == kat]
        for m in sorted(ludia):
            col_m, col_b = st.columns([4, 1])
            col_m.write(m)
            if col_b.button("🗑️", key=f"del_g_{m}"):
                del guest_dict[m]
                uloz_hosti(guest_dict)
                st.rerun()
