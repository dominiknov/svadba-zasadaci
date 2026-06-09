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
    # Ak súbor neexistuje, vytvoríme ho s tvojím pôvodným zoznamom
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

# Načítanie aktuálneho stavu hostí z databázy
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
    default["Hlavný Stôl_Miesto_1"] = "Janko (Dominik)" if "Janko (Dominik)" in guest_dict else "-- Voľné --"
    default["Hlavný Stôl_Miesto_2"] = "Mamka (Dominik)" if "Mamka (Dominik)" in guest_dict else "-- Voľné --"
    default["Hlavný Stôl_Miesto_3"] = "Dominik (Ženích)" if "Dominik (Ženích)" in guest_dict else "-- Voľné --"
    default["Hlavný Stôl_Miesto_4"] = "Kika (Nevesta)" if "Kika (Nevesta)" in guest_dict else "-- Voľné --"
    default["Hlavný Stôl_Miesto_5"] = "Mamka (Kika)" if "Mamka (Kika)" in guest_dict else "-- Voľné --"
    default["Hlavný Stôl_Miesto_6"] = "Palo (Kika)" if "Palo (Kika)" in guest_dict else "-- Voľné --"
    return default

if 'seating' not in st.session_state:
    st.session_state.seating = get_default_seating()

# Ošetrenie, ak bol niekto vymazaný zo zoznamu, nech nesedí na stole neexistujúci človek
for k, v in list(st.session_state.seating.items()):
    if v != "-- Voľné --" and v not in guest_dict:
        st.session_state.seating[k] = "-- Voľné --"

# Vytvorenie dvoch hlavných záložiek v aplikácii
tab1, tab2 = st.tabs(["🗺️ Zasadací Poriadok", "👥 Správa Hostí"])

# ==========================================
# KARTA 1: ZASADACÍ PORIADOK
# ==========================================
with tab1:
    tables_config = {
        "Hlavný Stôl": 6, 
        "Stôl 3": 10, "Stôl 2": 10, "Stôl 1": 10, 
        "Stôl 6": 10, "Stôl 5": 10, "Stôl 4": 10
    }

    # Sidebar s ukladaním
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
            skupina = guest_dict[ug]
            icon = "👑" if skupina == "Mladomanzelia" else "💙" if skupina == "Moja strana" else "💗" if skupina == "Kika strana" else "💚"
            st.sidebar.write(f"{icon} {ug}")

    # Ovládanie stolov
    st.subheader("🪑 Priraďovanie hostí k stolom")
    st.markdown("### 👑 Hlavná zóna (Fixne nastavené)")
    h_cols = st.columns(6)
    for seat in range(1, 7):
        with h_cols[seat - 1]:
            key = f"Hlavný Stôl_Miesto_{seat}"
            current_val = st.session_state.seating.get(key, "-- Voľné --")
            options = [current_val] + [g for g in unassigned_guests if g != current_val] if current_val != "-- Voľné --" else unassigned_guests
            options = list(set(options))
            index = options.index(current_val) if current_val in options else 0
            selected = st.selectbox(f"Hlavný M.{seat}", options, index=index, key=key)
            st.session_state.seating[key] = selected

    st.markdown("---")
    st.markdown("### 🧮 Okrúhle stoly")
    cols = st.columns(3)
    round_tables = ["Stôl 3", "Stôl 2", "Stôl 1", "Stôl 6", "Stôl 5", "Stôl 4"]

    for idx, t_name in enumerate(round_tables):
        with cols[idx % 3]:
            st.markdown(f"#### {t_name}")
            for seat in range(1, 11):
                key = f"{t_name}_Miesto_{seat}"
                current_val = st.session_state.seating.get(key, "-- Voľné --")
                options = [current_val] + [g for g in unassigned_guests if g != current_val] if current_val != "-- Voľné --" else unassigned_guests
                options = list(set(options))
                index = options.index(current_val) if current_val in options else 0
                selected = st.selectbox(f"{t_name} M.{seat}", options, index=index, key=key)
                st.session_state.seating[key] = selected

    # Mapa sály
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

    ax.add_patch(plt.Rectangle((5, 0.4), 10, 1.0, color='#e0e0e0', ec='#666666', lw=2))
    ax.text(10, 0.9, "👑 HLAVNÝ STÔL", ha='center', fontweight='bold', fontsize=11)

    for s_idx in range(6):
        px = 5.8 + s_idx * 1.6
        p_name = st.session_state.seating.get(f"Hlavný Stôl_Miesto_{s_idx+1}", "-- Voľné --")
        ax.text(px, 0.6, p_name, fontsize=8, ha='center', va='center',
                bbox=dict(boxstyle='square,pad=0.2', facecolor=get_color(p_name), edgecolor='#999999'))

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

# ==========================================
# KARTA 2: SPRÁVA HOSTÍ (PRIDÁVANIE / MAZANIE)
# ==========================================
with tab2:
    st.subheader("➕ Pridať nového hosťa")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        nove_meno = st.text_input("Meno a priezvisko (alebo prezývka):", key="new_name")
    with col2:
        nova_skupina = st.selectbox("Priradiť do skupiny:", ["Moja strana", "Kika strana", "Kamosi"], key="new_group")
    with col3:
        st.write(" ")
        st.write(" ")
        if st.button("➕ Pridať hosťa", use_container_width=True):
            if nove_meno.strip():
                if nove_meno.strip() not in guest_dict:
                    guest_dict[nove_meno.strip()] = nova_skupina
                    uloz_hosti(guest_dict)
                    st.success(f"Hosť {nove_meno} bol pridaný!")
                    st.columns # Force clear cache visually
                    st.rerun()
                else:
                    st.error("Tento hosť už v zozname existuje!")
            else:
                st.error("Meno nemôže byť prázdne!")

    st.markdown("---")
    st.subheader("📋 Zoznam aktuálnych hostí a mazanie")
    st.write(f"Celkový počet registrovaných ľudí: **{len(guest_dict)}**")

    # Rozdelenie zobrazenia podľa kategórií pre prehľadnosť
    kat_cols = st.columns(3)
    kategorie = ["Moja strana", "Kika strana", "Kamosi"]
    
    for k_idx, kat in enumerate(kategorie):
        with kat_cols[k_idx]:
            st.markdown(f"### {kat}")
            ludia_v_kat = {k: v for k, v in guest_dict.items() if v == kat}
            for meno in sorted(ludia_v_kat.keys()):
                c_text, c_but = st.columns([3, 1])
                c_text.write(f"• {meno}")
                if c_but.button("🗑️", key=f"del_{meno}"):
                    del guest_dict[meno]
                    uloz_hosti(guest_dict)
                    st.rerun()
