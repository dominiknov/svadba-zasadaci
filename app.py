import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Nastavenie stránky a načítanie dát
st.set_page_config(layout="wide", page_title="Svadobný Plánovač")
st.title("👑 Dynamický Zasadací Poriadok")

# Tu si načítaj svoj skutočný Excel (predpokladáme stĺpec 'Meno')
# Pre ukážku vytvoríme testovací zoznam na základe tvojich dát
@st.cache_data
def load_guests():
    # V reálnom behu nahraď: return pd.read_excel('svadba ludia-final.xlsx')['Meno'].tolist()
    return [
        "Dominik", "Kika", "Mamka (D)", "Janko (D)", "Mamka (K)", "Paľo (K)",
        "Tomas", "Eva", "Babulka", "Pato", "Ivetka", "Patko", "Mato", "Stefi",
        "Inga", "Babka thc", "Babka", "Noi", "Arne", "Sara", "Kekemama",
        "Ivka", "Ivka Stevo", "Gretka", "Gretka doprovod", "Pepe", "Jozko",
        "Ila", "Marek", "Kaja", "Oli", "Nika", "Jozocko", "Sasocko", "Dušan",
        "Sofia", "Tomas Sofi", "Beki", "Tomas Beki", "Dominik S.", "Lucka"
    ]

all_guests = load_guests()

# 2. Inicializácia stavu (Session State) pre usadenie ľudí
if 'seating' not in st.session_state:
    st.session_state.seating = {}

# Definícia štruktúry sály (Hlavný stôl + 7 okrúhlych stolov po 10 miest)
tables_config = {
    "Hlavný Stôl": 6,
    "Stôl 1": 10,
    "Stôl 2": 10,
    "Stôl 3": 10,
    "Stôl 4": 10,
    "Stôl 5": 10,
    "Stôl 6": 10,
    "Stôl 7": 10
}

# 3. Sidebar - Prehľad neusadených hostí
st.sidebar.header("👥 Hostia")
used_guests = [val for val in st.session_state.seating.values() if val != "-- Voľné --"]
unassigned_guests = ["-- Voľné --"] + [g for g in all_guests if g not in used_guests]

st.sidebar.subheader(f"Ešte neusadení ({len(unassigned_guests)-1}):")
for ug in unassigned_guests:
    if ug != "-- Voľné --":
        st.sidebar.write(f"🛑 {ug}")

# 4. Hlavná zóna - Výber hostí pre stoly (Ovládací panel)
st.subheader("🪑 Priradenie miest k stolom")
cols = st.columns(4) # Rozdelíme ovládanie do 4 stĺpcov na obrazovke

for idx, (table_name, max_seats) in enumerate(tables_config.items()):
    with cols[idx % 4]:
        st.markdown(f"### {table_name}")
        for seat in range(1, max_seats + 1):
            key = f"{table_name}_Miesto_{seat}"
            current_val = st.session_state.seating.get(key, "-- Voľné --")
            
            # Ak človek už sedí tu, chceme, aby bol v zozname možností dostupný
            options = [current_val] + [g for g in unassigned_guests if g != current_val] if current_val != "-- Voľné--" else unassigned_guests
            options = list(set(options))
            if current_val in options:
                index = options.index(current_val)
            else:
                index = 0
                
            selected = st.selectbox(f"Miesto {seat}", options, index=index, key=key)
            st.session_state.seating[key] = selected

# 5. Živá Vizualizácia sály pomocou Matplotlib
st.subheader("🗺️ Živá Mapa Sály")

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 20)
ax.set_ylim(0, 10)
ax.axis('off')

# Vykreslenie hlavného stola (obdĺžnik dole)
ax.add_patch(plt.Rectangle((6, 0.5), 8, 1, color='#d9d9d9', ec='#666666', lw=2))
ax.text(10, 1.0, "HLAVNÝ STÔL", ha='center', va='center', fontweight='bold')

# Vykreslenie okrúhlych stolov (Súradnice x, y kopírujú tvoj nákres sály)
coords = {
    "Stôl 3": (4, 4), "Stôl 2": (10, 4), "Stôl 1": (16, 4),
    "Stôl 7": (2.5, 7.5), "Stôl 6": (7.5, 7.5), "Stôl 5": (12.5, 7.5), "Stôl 4": (17.5, 7.5)
}

for t_name, (x, y) in coords.items():
    # Stôl
    ax.add_patch(plt.Circle((x, y), 1.0, color='#f0f0f0', ec='#999999', lw=2))
    ax.text(x, y, t_name, ha='center', va='center', fontweight='bold')
    
    # Miesta okolo stola
    angles = np.linspace(0, 2*np.pi, 10, endpoint=False) + np.pi/2
    for s_idx, angle in enumerate(angles):
        sx = x + 1.4 * np.cos(angle)
        sy = y + 1.4 * np.sin(angle)
        
        person = st.session_state.seating.get(f"{t_name}_Miesto_{s_idx+1}", "-- Voľné --")
        if person != "-- Voľné --":
            ax.text(sx, sy, person, fontsize=8, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#c9daf8', edgecolor='#999999', alpha=0.9))

st.pyplot(fig)
