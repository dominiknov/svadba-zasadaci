import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Nastavenie stránky a dát
st.set_page_config(layout="wide", page_title="Svadobný Plánovač")
st.title("👑 Dynamický Zasadací Poriadok (Farebné Rozlíšenie)")

@st.cache_data
def load_guests():
    # Stopercentne prečistený a rozdelený zoznam hostí podľa tvojho Excelu
    return {
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
        
        # KAMOŠI (Zelená) - Precízne rozdelení z Excelu
        "Ila": "Kamosi", "Marek": "Kamosi", "Kaja": "Kamosi", "Oli": "Kamosi", "Nika": "Kamosi", 
        "Jozocko": "Kamosi", "Sasocko": "Kamosi", "Dusan": "Kamosi", "Peta": "Kamosi", "Ada": "Kamosi", 
        "Sofia": "Kamosi", "Tomas Sofi": "Kamosi", "Beki": "Kamosi", "Tomas Beki": "Kamosi", 
        "Dominik S.": "Kamosi", "Lucka": "Kamosi", "Viki B.": "Kamosi", "Viki B. BF": "Kamosi", 
        "Rasto": "Kamosi", "Vlado": "Kamosi", "Marko": "Kamosi", "Ivana": "Kamosi", "Danko Kocak": "Kamosi", 
        "Danova Naty": "Kamosi", "Biba": "Kamosi", "Jaro": "Kamosi",
        
        # OSTATNÍ (Žltá)
        "Mikias (DJ)": "Ostatni", "Marista (fotografka)": "Ostatni"
    }

guest_dict = load_guests()
all_guests = sorted(list(guest_dict.keys()))

# Inicializácia sedadiel v session state
if 'seating' not in st.session_state:
    st.session_state.seating = {}

tables_config = {
    "Hlavný Stôl": 6, "Stôl 1": 10, "Stôl 2": 10, "Stôl 3": 10, 
    "Stôl 4": 10, "Stôl 5": 10, "Stôl 6": 10, "Stôl 7": 10
}

# Bočný panel s neusadenými
st.sidebar.header("👥 Kto ešte nesedí?")
used_guests = [val for val in st.session_state.seating.values() if val != "-- Voľné --"]
unassigned_guests = ["-- Voľné --"] + [g for g in all_guests if g not in used_guests]

for ug in unassigned_guests:
    if ug != "-- Voľné --":
        skupina = guest_dict[ug]
        icon = "💙" if skupina == "Moja strana" else "💗" if skupina == "Kika strana" else "💚" if skupina == "Kamosi" else "💛"
        st.sidebar.write(f"{icon} {ug}")

# Výberové menu pre stoly
st.subheader("🪑 Priraďovanie hostí k stolom")
cols = st.columns(4)
for idx, (table_name, max_seats) in enumerate(tables_config.items()):
    with cols[idx % 4]:
        st.markdown(f"### {table_name}")
        for seat in range(1, max_seats + 1):
            key = f"{table_name}_Miesto_{seat}"
            current_val = st.session_state.seating.get(key, "-- Voľné --")
            options = [current_val] + [g for g in unassigned_guests if g != current_val] if current_val != "-- Voľné --" else unassigned_guests
            options = list(set(options))
            index = options.index(current_val) if current_val in options else 0
            
            selected = st.selectbox(f"Miesto {seat}", options, index=index, key=key)
            st.session_state.seating[key] = selected

# 🗺️ VYKRESLENIE MAPY SÁLY
st.subheader("🗺️ Živá Vizuálna Mapa Sály")

fig, ax = plt.subplots(figsize=(15, 8))
ax.set_xlim(0, 20)
ax.set_ylim(0, 10)
ax.axis('off')

# Pomocná funkcia pre farby
def get_color(name):
    if name == "-- Voľné --": return '#ffffff'
    skupina = guest_dict.get(name, "")
    if skupina == "Moja strana": return '#c9daf8' # Modrá
    if skupina == "Kika strana": return '#f4cccc' # Ružová
    if skupina == "Kamosi": return '#d9ead3'      # Zelená
    return '#fff2cc'                              # Žltá (Ostatní)

# Hlavný stôl dole
ax.add_patch(plt.Rectangle((5, 0.4), 10, 1.0, color='#e0e0e0', ec='#666666', lw=2))
ax.text(10, 0.9, "👑 HLAVNÝ STÔL", ha='center', fontweight='bold', fontsize=11)

for s_idx in range(6):
    px = 5.8 + s_idx * 1.6
    p_name = st.session_state.seating.get(f"Hlavný Stôl_Miesto_{s_idx+1}", "-- Voľné --")
    ax.text(px, 0.6, p_name, fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='square,pad=0.2', facecolor=get_color(p_name), edgecolor='#999999'))

# Okrúhle stoly (Usporiadané presne podľa rozloženia sály)
coords = {
    "Stôl 3": (4, 4.2), "Stôl 2": (10, 4.2), "Stôl 1": (16, 4.2),
    "Stôl 7": (2.5, 7.8), "Stôl 6": (7.5, 7.8), "Stôl 5": (12.5, 7.8), "Stôl 4": (17.5, 7.8)
}

for t_name, (x, y) in coords.items():
    ax.add_patch(plt.Circle((x, y), 1.0, color='#f7f7f7', ec='#aaaaaa', lw=2))
    ax.text(x, y, t_name, ha='center', va='center', fontweight='bold', fontsize=10)
    
    angles = np.linspace(0, 2*np.pi, 10, endpoint=False) + np.pi/2
    for s_idx, angle in enumerate(angles):
        sx = x + 1.45 * np.cos(angle)
        sy = y + 1.35 * np.sin(angle)
        
        person = st.session_state.seating.get(f"{t_name}_Miesto_{s_idx+1}", "-- Voľné --")
        if person != "-- Voľné --":
            ax.text(sx, sy, person, fontsize=7.5, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=get_color(person), edgecolor='#cccccc'))

st.pyplot(fig)
