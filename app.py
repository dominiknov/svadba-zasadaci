import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

# 1. Nastavenie stránky a dát
st.set_page_config(layout="wide", page_title="Svadobný Plánovač")
st.title("👑 Dynamický Svadobný Plánovač s Ukladaním Verzií")

@st.cache_data
def load_guests():
    return {
        # MLADOMANŽELIA (Zlatá)
        "Dominik (Ženích)": "Mladomanzelia", "Kika (Nevesta)": "Mladomanzelia",

        # MOJA STRANA (Modrá)
        "Mamka (Dominik)": "Moja strana", "Janko (Dominik)": "Moja strana", "Tomas (Dominik)": "Moja strana", 
        "Eva (Dominik)": "Moja strana", "Babulka (Dominik)": "Moja strana", "Pato (Dominik)": "Moja strana", 
        "Ivetka (Dominik)": "Moja strana", "Patko (Dominik)": "Moja strana", "Mato (Dominik)": "Moja strana", 
        "Stefi (Dominik)": "Moja strana", "Brigita (Dominik)": "Moja strana", "Brigitka (Dominik)": "Moja strana", 
        "Nilay (Dominik)": "Moja strana",
        
        # KIKA STRANA (Ružová)
        "Mamka (Kika)": "Kika strana", "Ivka (Kika)": "Kika strana", "Palo (Kika)": "Kika strana", 
        "Ivka Stevo (Kika)": "Kika strana", "Gretka (Kika)": "Kika strana", "Pepe (Kika)": "Kika strana", 
        "Jozko (Kika)": "Kika strana", "Inga (Kika)": "Kika strana", "Babka thc (Kika)": "Kika strana", 
        "Babka (Kika)": "Kika strana", "Noi (Kika)": "Kika strana", "Arne (Kika)": "Kika strana", 
        "Sara (Kika)": "Kika strana", "Kekemama (Kika)": "Kika strana", "Gretka doprovod (Kika)": "Kika strana", 
        "Viki Inga (Kika)": "Kika strana", "Paľo ocko (Kika)": "Kika strana", "Paľo mamka (Kika)": "Kika strana",
        
        # KAMOŠI (Zelená)
        "Ila": "Kamosi", "Marek": "Kamosi", "Kaja": "Kamosi", "Oli": "Kamosi", "Nika": "Kamosi", 
        "Jozocko": "Kamosi", "Sasocko": "Kamosi", "Dusan": "Kamosi", "Peta": "Kamosi", "Ada": "Kamosi", 
        "Sofia": "Kamosi", "Tomas Sofi": "Kamosi", "Beki": "Kamosi", "Tomas Beki": "Kamosi", 
        "Dominik S.": "Kamosi", "Lucka": "Kamosi", "Viki B.": "Kamosi", "Viki B. BF": "Kamosi", 
        "Rasto": "Kamosi", "Vlado": "Kamosi", "Marko": "Kamosi", "Ivana": "Kamosi", "Danko Kocak": "Kamosi", 
        "Danova Naty": "Kamosi", "Biba": "Kamosi", "Jaro": "Kamosi"
    }

guest_dict = load_guests()
all_guests = sorted(list(guest_dict.keys()))

tables_config = {
    "Hlavný Stôl": 6, 
    "Stôl 3": 10, "Stôl 2": 10, "Stôl 1": 10, 
    "Stôl 6": 10, "Stôl 5": 10, "Stôl 4": 10
}

# --- SYSTÉM UKLADANIA DO SÚBORU ---
DB_FILE = "svadba_verzie.json"

def naciataj_vsetky_verzie():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def uloz_verziu(nazov, data):
    vsetky = naciataj_vsetky_verzie()
    vsetky[nazov] = data
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(vsetky, f, ensure_ascii=False, indent=4)

# Definícia základného fixného stavu (Hlavný stôl)
def get_default_seating():
    default = {}
    default["Hlavný Stôl_Miesto_1"] = "Janko (Dominik)"
    default["Hlavný Stôl_Miesto_2"] = "Mamka (Dominik)"
    default["Hlavný Stôl_Miesto_3"] = "Dominik (Ženích)"
    default["Hlavný Stôl_Miesto_4"] = "Kika (Nevesta)"
    default["Hlavný Stôl_Miesto_5"] = "Mamka (Kika)"
    default["Hlavný Stôl_Miesto_6"] = "Palo (Kika)"
    return default

# Inicializácia sedadiel v session state
if 'seating' not in st.session_state:
    st.session_state.seating = get_default_seating()

# --- SIDEBAR: LOGIKA UKLADANIA ---
st.sidebar.header("💾 Správa Variácií")
verzie = naciataj_vsetky_verzie()

# Uloženie verzie
novy_nazov = st.sidebar.text_input("Názov novej variácie (napr. Verzia A):")
if st.sidebar.button("💾 Uložiť aktuálny stav"):
    if novy_nazov:
        uloz_verziu(novy_nazov, st.session_state.seating)
        st.sidebar.success(f"Uložené ako: {novy_nazov}")
        st.rerun()
    else:
        st.sidebar.error("Zadaj názov verzie!")

st.sidebar.markdown("---")

# Načítanie verzie
if verzie:
    vybrana_verzia = st.sidebar.selectbox("Vyber uloženú variáciu:", list(verzie.keys()))
    if st.sidebar.button("📂 Načítať túto variáciu"):
        # OPRAVA: Premažeme staré widget kľúče, aby selectboxy neskočili na staré hodnoty
        for k in list(st.session_state.keys()):
            if k.startswith("w_"):
                del st.session_state[k]
        
        # Priradíme načítané usadenie
        st.session_state.seating = verzie[vybrana_verzia].copy()
        st.sidebar.success(f"Načítaná verzia: {vybrana_verzia}")
        st.rerun()
else:
    st.sidebar.info("Zatiaľ nemáš žiadne uložené variácie.")

st.sidebar.markdown("---")

# Zoznam neusadených hostí
st.sidebar.header("👥 Kto ešte nesedí?")
used_guests = [val for val in st.session_state.seating.values() if val != "-- Voľné --"]
unassigned_guests = ["-- Voľné --"] + [g for g in all_guests if g not in used_guests]

for ug in unassigned_guests:
    if ug != "-- Voľné --":
        skupina = guest_dict[ug]
        icon = "👑" if skupina == "Mladomanzelia" else "💙" if skupina == "Moja strana" else "💗" if skupina == "Kika strana" else "💚"
        st.sidebar.write(f"{icon} {ug}")

# --- OVLÁDACÍ PANEL STOLOV ---
st.subheader("🪑 Priraďovanie hostí k stolom")

st.markdown("### 👑 Hlavná zóna (Fixne nastavené)")
h_cols = st.columns(6)
for seat in range(1, 7):
    with h_cols[seat - 1]:
        key = f"Hlavný Stôl_Miesto_{seat}"
        widget_key = f"w_{key}" # Unikátny kľúč pre widget
        current_val = st.session_state.seating.get(key, "-- Voľné --")
        
        options = [current_val] + [g for g in unassigned_guests if g != current_val] if current_val != "-- Voľné --" else unassigned_guests
        options = list(dict.fromkeys(options)) # Zachovanie poradia a odstránenie duplicít
        index = options.index(current_val) if current_val in options else 0
        
        selected = st.selectbox(f"Hlavný M.{seat}", options, index=index, key=widget_key)
        if selected != current_val:
            st.session_state.seating[key] = selected
            st.rerun()

st.markdown("---")

st.markdown("### 🧮 Okrúhle stoly")
cols = st.columns(3)
round_tables = ["Stôl 3", "Stôl 2", "Stôl 1", "Stôl 6", "Stôl 5", "Stôl 4"]

for idx, t_name in enumerate(round_tables):
    with cols[idx % 3]:
        st.markdown(f"#### {t_name}")
        for seat in range(1, 11):
            key = f"{t_name}_Miesto_{seat}"
            widget_key = f"w_{key}" # Unikátny kľúč pre widget
            current_val = st.session_state.seating.get(key, "-- Voľné --")
            
            options = [current_val] + [g for g in unassigned_guests if g != current_val] if current_val != "-- Voľné --" else unassigned_guests
            options = list(dict.fromkeys(options))
            index = options.index(current_val) if current_val in options else 0
            
            selected = st.selectbox(f"{t_name} M.{seat}", options, index=index, key=widget_key)
            if selected != current_val:
                st.session_state.seating[key] = selected
                st.rerun()

# --- ŽIVÁ VIZUÁLNA MAPA SÁLY ---
st.markdown("---")
st.subheader("🗺️ Živá Vizuálna Mapa Sály")

fig, ax = plt.subplots(figsize=(15, 8))
ax.set_xlim(0, 20)
ax.set_ylim(0, 10)
ax.axis('off')

def get_color(name):
    if name == "-- Voľné --": return '#ffffff'
    skupina = guest_dict.get(name, "")
    if skupina == "Mladomanzelia": return '#ffe599'
    if skupina == "Moja strana": return '#c9daf8'
    if skupina == "Kika strana": return '#f4cccc'
    return '#d9ead3'

# Hlavný stôl
ax.add_patch(plt.Rectangle((5, 0.4), 10, 1.0, color='#e0e0e0', ec='#666666', lw=2))
ax.text(10, 0.9, "👑 HLAVNÝ STÔL", ha='center', fontweight='bold', fontsize=11)

for s_idx in range(6):
    px = 5.8 + s_idx * 1.6
    p_name = st.session_state.seating.get(f"Hlavný Stôl_Miesto_{s_idx+1}", "-- Voľné --")
    ax.text(px, 0.6, p_name, fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='square,pad=0.2', facecolor=get_color(p_name), edgecolor='#999999'))

# 6 Okrúhlych stolov rozložených symetricky (3,2,1 vpredu a 6,5,4 vzadu)
coords = {
    "Stôl 3": (4.5, 4.2), "Stôl 2": (10.0, 4.2), "Stôl 1": (15.5, 4.2),
    "Stôl 6": (4.5, 7.8), "Stôl 5": (10.0, 7.8), "Stôl 4": (15.5, 7.8)
}

for t_name, (x, y) in coords.items():
    ax.add_patch(plt.Circle((x, y), 1.1, color='#f7f7f7', ec='#aaaaaa', lw=2))
    ax.text(x, y, t_name, ha='center', va='center', fontweight='bold', fontsize=10)
    
    angles = np.linspace(0, 2*np.pi, 10, endpoint=False) + np.pi/2
    for s_idx, angle in enumerate(angles):
        sx = x + 1.55 * np.cos(angle)
        sy = y + 1.45 * np.sin(angle)
        
        person = st.session_state.seating.get(f"{t_name}_Miesto_{s_idx+1}", "-- Voľné --")
        if person != "-- Voľné --":
            ax.text(sx, sy, person, fontsize=7.5, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=get_color(person), edgecolor='#cccccc'))

st.pyplot(fig)
