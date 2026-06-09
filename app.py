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

# --- PEVNÝ PÔVODNÝ ZOZNAM HOSTÍ ---
guest_dict = {
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
    default["Hlavný stôl M.1"] = "Adrianka (Dominik)"
    default["Hlavný stôl M.2"] = "Mamka (Dominik)"
    default["Hlavný stôl M.3"] = "Dominik (Ženích)"
    default["Hlavný stôl M.4"] = "Kika (Nevesta)"
    default["Hlavný stôl M.5"] = "Mamka (Kika)"
    default["Hlavný stôl M.6"] = "Palo (Kika)"
    return default

if 'seating' not in st.session_state:
    st.session_state.seating = get_default_seating()

# Vynútenie statického usadenia hlavného stola v pamäti
st.session_state.seating["Hlavný stôl M.1"] = "Adrianka (Dominik)"
st.session_state.seating["Hlavný stôl M.2"] = "Mamka (Dominik)"
st.session_state.seating["Hlavný stôl M.3"] = "Dominik (Ženích)"
st.session_state.seating["Hlavný stôl M.4"] = "Kika (Nevesta)"
st.session_state.seating["Hlavný stôl M.5"] = "Mamka (Kika)"
st.session_state.seating["Hlavný stôl M.6"] = "Palo (Kika)"

# --- SIDEBAR (BOČNÝ PANEL) ---
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

# --- HLAVNÁ STRÁNKA ---
st.subheader("🪑 Priraďovanie hostí k stolom")

# STATICKÉ ZOBRAZENIE HLAVNÉHO STOLA
st.markdown("### 👑 Hlavná zóna")
st.write(f"**Miesto 1:** {st.session_state.seating['Hlavný stôl M.1']}")
st.write(f"**Miesto 2:** {st.session_state.seating['Hlavný stôl M.2']}")
st.write(f"**Miesto 3:** {st.session_state.seating['Hlavný stôl M.3']}")
st.write(f"**Miesto 4:** {st.session_state.seating['Hlavný stôl M.4']}")
st.write(f"**Miesto 5:** {st.session_state.seating['Hlavný stôl M.5']}")
st.write(f"**Miesto 6:** {st.session_state.seating['Hlavný stôl M.6']}")

st.markdown("---")
st.markdown("### 🧮 Okrúhle stoly")

def render_single_seat_selector(prefix_db, seat_number):
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
        
    selected = st.selectbox(f"{prefix_db} M.{seat_number}", valid_options, index=idx, key=key)
        
    if selected != current_val:
        st.session_state.seating[db_key] = selected
        st.rerun()

round_tables = ["Stôl 3", "Stôl 2", "Stôl 1", "Stôl 6", "Stôl 5", "Stôl 4"]
for t_name in round_tables:
    st.markdown(f"#### {t_name}")
    for seat in range(1, 11):
        render_single_seat_selector(t_name, seat)

# --- VIZUALIZÁCIA (MAPA SÁLY) ---
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
