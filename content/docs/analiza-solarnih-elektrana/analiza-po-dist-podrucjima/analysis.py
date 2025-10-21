# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 09:32:03 2025

@author: Lara Buljan
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

INPUT_FILE = "Proizvođači_30042025_v2.XLSX"
DP_COLUMN = "DP"  # zamijeni ako se zove drugačije
POWER_COLUMN = "EES proizvodnje"  # zamijeni prema točnom nazivu

# === UČITAVANJE ===
df = pd.read_excel(INPUT_FILE)

# === ČIŠĆENJE ===
df = df[df[DP_COLUMN].notna()]  # makni prazne DP-ove
df[POWER_COLUMN] = pd.to_numeric(df[POWER_COLUMN], errors='coerce')  # ako ima tekstualnih

# === SAŽETAK ===
summary = df.groupby(DP_COLUMN).agg(
    Broj_proizvodaca=("DP", "count"),
    Ukupna_snaga_kW=(POWER_COLUMN, "sum")
).reset_index()

summary["Ukupna_snaga_MW"] = round(summary["Ukupna_snaga_kW"] / 1000, 2)

print(summary)


dp_map = {
    "4001": "Elektra Zagreb",
    "4002": "Elektra Zabok",
    "4003": "Elektra Varaždin",
    "4004": "Elektra Čakovec",
    "4005": "Elektra Koprivnica",
    "4006": "Elektra Bjelovar",
    "4007": "Elektra Križ",
    "4008": "Elektroslavonija Osijek",
    "4009": "Elektra Vinkovci",
    "4010": "Elektra Slavonski Brod",
    "4011": "Elektroistra Pula",
    "4012": "Elektroprimorje Rijeka",
    "4013": "Elektrodalmacija Split",
    "4014": "Elektra Zadar",
    "4015": "Elektra Šibenik",
    "4016": "Elektrojug Dubrovnik",
    "4017": "Elektra Karlovac",
    "4018": "Elektra Sisak",
    "4019": "Elektrolika Gospić",
    "4020": "Elektra Virovitica",
    "4021": "Elektra Požega"
    }


# === PLOTLY GRAFOVI ===
# Broj proizvođača po DP-u
fig1 = px.bar(summary, 
              x=DP_COLUMN, 
              y="Broj_proizvodaca",
              text="Broj_proizvodaca",
              labels={DP_COLUMN: "Distribucijsko područje",
                      "Broj_proizvodaca": "Broj instaliranih OIE"},
              title="Broj proizvođača po DP-u")

fig1.update_layout(width=900, height=600,
                   xaxis=dict(tickmode='linear'),
                   xaxis_tickangle=-45,
                   uniformtext_minsize=6,
                   uniformtext_mode="hide")
fig1.write_image("Broj proizvodaca po DP.svg")
fig1.write_html("Broj proizvodaca po DP.html")


# Ukupna instalirana snaga po DP-u
fig2 = px.bar(summary, 
              x=DP_COLUMN, 
              y="Ukupna_snaga_MW", 
              text= "Ukupna_snaga_MW",
              title="Ukupna instalirana snaga DI po DP-u [MW]",
              labels={"Ukupna_snaga_MW": "Snaga (MW)",
                      DP_COLUMN: "Distribucijsko područje"})
fig2.update_layout(width=900, height=600,
                   xaxis=dict(tickmode='linear'),
                   xaxis_tickangle=-45,
                   uniformtext_minsize=7,
                   uniformtext_mode="hide")
fig2.write_image("Snaga po DP.svg")
fig2.write_html("Snaga po DP.html")


summary["DP Name"] = summary[DP_COLUMN].astype(str).map(dp_map)

# Kružni graf postotnog udjela snage
fig3 = px.pie(summary, 
              names="DP Name", 
              values="Ukupna_snaga_MW", 
              title="Udio instalirane snage po DP-u [%]",
              labels={"Ukupna_snaga_MW": "Snaga (MW)",
                      "DP Name": "Distribucijsko područje"})
fig3.update_layout(width=900, height=600,
                   xaxis=dict(tickmode='linear'),
                   xaxis_tickangle=-45,
                   uniformtext_minsize=7,
                   uniformtext_mode="hide")

fig3.write_image("Pie chart snage po DP.svg")
fig3.write_html("Pie chart snage po DP.html")



