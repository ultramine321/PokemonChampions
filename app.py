import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Pokemon Champions Season 2 League Dashboard",
    page_icon="⚡",
    layout="wide"
)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Pokemon_Champions_Clustered.csv")
    return df

df = load_data()

STAT_COLS = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
DISPLAY_STAT_COLS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

# ------------------ POKEMON TYPE COLORS ------------------
# Authentic Pokemon type color scheme for visually stunning distributions
TYPE_COLORS = {
    "Normal": "#A8A77A", "Fire": "#EE8130", "Water": "#6390F0", "Electric": "#F7D02C",
    "Grass": "#7AC74C", "Ice": "#96D9D6", "Fighting": "#C22E28", "Poison": "#A33EA1",
    "Ground": "#E2BF65", "Flying": "#A98FF3", "Psychic": "#F95587", "Bug": "#A6B91A",
    "Rock": "#B6A136", "Ghost": "#735797", "Dragon": "#6F35FC", "Dark": "#705746",
    "Steel": "#B7B7CE", "Fairy": "#D685AD"
}

# ------------------ CUSTOM CSS THEME ------------------
# Injecting premium custom styling to match a high-end Pokemon Championship arena
st.markdown("""
<style>
    /* Main App Container Styling */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%) !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(9, 13, 22, 0.4) !important;
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 215, 0, 0.15) !important;
    }
    
    /* Navigation radio button styling */
    .stRadio > label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 10px;
    }
    
    .stRadio div[role="radiogroup"] {
        background: rgba(17, 24, 39, 0.7);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid rgba(255, 215, 0, 0.1);
        gap: 6px;
    }
    
    .stRadio div[role="radiogroup"] label {
        background: rgba(30, 41, 59, 0.3);
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        cursor: pointer;
        width: 100%;
        margin-bottom: 4px;
    }
    
    .stRadio div[role="radiogroup"] label:hover {
        background: rgba(255, 215, 0, 0.05);
        border-color: rgba(255, 215, 0, 0.2);
    }
    
    .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: rgba(255, 215, 0, 0.15) !important;
        border-color: #FFD700 !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.1);
    }
    
    /* Input Elements (Selectbox, slider, etc.) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #111827 !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #FFD700 !important;
        box-shadow: 0 0 8px rgba(255, 215, 0, 0.15);
    }
    
    /* Tables and Dataframes */
    div.stDataFrame {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 5px;
    }
    
    /* Tabs custom styling */
    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 12px 20px !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFD700 !important;
        border-bottom: 3px solid #FFD700 !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #090d16;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #FFD70055;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ UI HELPERS ------------------
def champion_header(title, subtitle=None):
    """Generates a premium league header card."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #111827 0%, #1e1b4b 100%);
        border-left: 6px solid #FFD700;
        padding: 20px 25px;
        border-radius: 6px 16px 16px 6px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    ">
        <h1 style="color: #ffffff; margin: 0; font-weight: 800; letter-spacing: 0.5px; font-size: 2.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.4);">
            ⚡ {title}
        </h1>
        {f'<div style="color: #94a3b8; font-size: 1rem; margin-top: 8px; font-weight: 500;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def metric_card(title, value, subtitle=None, border_color="#FFD700"):
    """Generates a beautiful card to replace default Streamlit metrics."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(17, 24, 39, 0.5) 100%);
        border: 1px solid {border_color}22;
        border-left: 5px solid {border_color};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        margin-bottom: 15px;
    ">
        <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;">{title}</div>
        <div style="font-size: 2rem; font-weight: 800; color: #ffffff; margin-top: 6px; line-height: 1.1; text-shadow: 0 0 10px {border_color}33;">{value}</div>
        {f'<div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 6px; opacity: 0.75; font-weight: 500;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def apply_plotly_theme(fig):
    """Styles Plotly figures to perfectly integrate with the dark UI."""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#cbd5e1",
        title_font_color="#ffffff",
        title_font_size=16,
        legend_title_font_color="#ffffff",
        margin=dict(l=40, r=40, t=55, b=40),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)", 
            linecolor="rgba(255, 255, 255, 0.1)",
            title_font_color="#94a3b8"
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)", 
            linecolor="rgba(255, 255, 255, 0.1)",
            title_font_color="#94a3b8"
        ),
    )
    return fig

# ------------------ SIDEBAR NAV ------------------
st.sidebar.markdown("""
<div style="text-align: center; padding: 20px 0 10px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 15px;">
    <h1 style="color: #FFD700; font-size: 1.6rem; font-weight: 900; margin: 0; text-shadow: 0 0 15px rgba(255, 215, 0, 0.35); letter-spacing: 1px;">⚡ POKÉMON</h1>
    <p style="color: #94a3b8; font-size: 0.75rem; margin: 4px 0 0 0; text-transform: uppercase; letter-spacing: 3px; font-weight: 700;">Champions League</p>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Pilih Menu Dashboard:",
    [
        "Dashboard",
        "Top 10 Total Stats",
        "Pokemon Detail",
        "Compare Stats",
        "Type Recommendation",

    ]
)

# ==================================================
# 1. DASHBOARD
# ==================================================
if menu == "Dashboard":
    champion_header("Pokemon Champions Season 2 Dashboard", "Ringkasan statistik data liga dan sebaran kekuatan Pokemon.")
    
    total_pokemon = df["Pokemon"].nunique()

    # Metric Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Total Pokemon", f"{total_pokemon}", "Spesies Terdaftar", "#FF4B4B")
    with col2:
        metric_card("Rata-rata Stats", f"{df['Total'].mean():.0f}", "Kekuatan Rata-rata", "#FFD700")
    with col3:
        # Get highest stat pokemon
        highest_stat_idx = df['Total'].idxmax()
        highest_poke = df.loc[highest_stat_idx, 'Pokemon']
        highest_val = df.loc[highest_stat_idx, 'Total']
        metric_card("Total Stats Tertinggi", f"{highest_val}", f"Dipegang oleh {highest_poke}", "#06B6D4")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribusi Tipe Utama (Type I)")
        type_counts = df["Type I"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        
        # Plot with authentic type colors
        fig = px.bar(
            type_counts, 
            x="Type", 
            y="Count", 
            color="Type", 
            color_discrete_map=TYPE_COLORS,
            text_auto=True
        )
        apply_plotly_theme(fig)
        fig.update_layout(showlegend=False, height=400, yaxis_title="Jumlah Pokemon", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Distribusi Total Stats Kekuatan")
        fig2 = px.histogram(
            df, 
            x="Total", 
            nbins=25,
            color_discrete_sequence=["#FFD700"]
        )
        apply_plotly_theme(fig2)
        fig2.update_layout(height=400, yaxis_title="Jumlah Pokemon", xaxis_title="Total Stats")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Preview Data Pokemon")
    # Clean output headers for presentation
    preview_df = df.head(20).copy()
    st.dataframe(preview_df, use_container_width=True)

# ==================================================
# 2. TOP 10 TOTAL STATS
# ==================================================
elif menu == "Top 10 Total Stats":
    champion_header("Top 10 Pokemon dengan Total Stats Tertinggi", "Daftar elit Pokemon dengan daya tempur tertinggi di liga.")

    top10 = df.sort_values("Total", ascending=False).head(10).reset_index(drop=True)
    top10.index = top10.index + 1

    display_cols = ["Pokemon", "Type I", "Type II"] + STAT_COLS + ["Total"]
    st.dataframe(top10[display_cols], use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    fig = px.bar(
        top10.sort_values("Total"),
        x="Total",
        y="Pokemon",
        orientation="h",
        color="Total",
        color_continuous_scale="Plasma",
        text="Total"
    )
    apply_plotly_theme(fig)
    fig.update_layout(height=500, yaxis_title="", xaxis_title="Total Stats", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# 3. POKEMON DETAIL
# ==================================================
elif menu == "Pokemon Detail":
    champion_header("Pokemon Detail Profiler", "Cari dan analisis statistik mendalam dari setiap Pokemon.")

    pokemon_list = sorted(df["Pokemon"].unique().tolist())
    selected = st.selectbox("Cari nama Pokemon (Contoh: Venusaur atau Charizard)", pokemon_list)

    if selected:
        row = df[df["Pokemon"] == selected].iloc[0]

        # Thematic detail header cards
        type_a = row["Type I"]
        type_b = row["Type II"]
        badge_a = f'<span style="background-color: {TYPE_COLORS.get(type_a, "#777")}; color: white; padding: 5px 14px; border-radius: 20px; font-weight: bold; margin-right: 5px; font-size: 0.95rem;">{type_a}</span>'
        badge_b = f'<span style="background-color: {TYPE_COLORS.get(type_b, "#777")}; color: white; padding: 5px 14px; border-radius: 20px; font-weight: bold; font-size: 0.95rem;">{type_b}</span>' if pd.notna(type_b) else ""
        
        cluster_name = "Elite Specialist" if row["Cluster"] == 0 else "Physical Contender"
        cluster_color = "#FFD700" if row["Cluster"] == 0 else "#FF4B4B"

        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #111827 0%, rgba(30, 41, 59, 0.4) 100%); padding: 25px; border-radius: 12px; border: 1px solid rgba(255, 215, 0, 0.25); margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div style="display: flex; align-items: center; flex-wrap: wrap; gap: 15px;">
                <h2 style="margin: 0; color: #ffffff; font-size: 2.2rem; font-weight: 800;">{row['Pokemon']}</h2>
                <div>{badge_a} {badge_b}</div>
            </div>
            <div style="margin-top: 12px; color: #94a3b8; font-size: 1rem; font-weight: 600;">
                Klasifikasi Kluster ML: <span style="color: {cluster_color}; font-weight: 800;">Cluster {row['Cluster']} — {cluster_name}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("HP & Attack", f"{row['HP']} HP | {row['Atk']} Atk", "Statistik Fisik Dasar", "#FF4B4B")
        with c2:
            metric_card("Def & Speed", f"{row['Def']} Def | {row['Spe']} Spe", "Pertahanan & Kecepatan", "#F59E0B")
        with c3:
            metric_card("Special Stats", f"{row['SpA']} SpA | {row['SpD']} SpD", "Kekuatan & Pertahanan Spesial", "#3B82F6")
            
        st.markdown(f"""
        <div style="max-width: 300px; margin: 0 auto; text-align: center;">
            <div style="background: rgba(255,215,0,0.08); padding: 8px 15px; border-radius: 20px; border: 1px solid #FFD70055; font-size: 1.1rem; font-weight: 800; color: #FFD700;">
                 TOTAL STATS: {row['Total']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_charts_a, col_charts_b = st.columns([1.2, 1])
        
        with col_charts_a:
            st.subheader("Statistik Radar Chart")
            stats_values = [row[s] for s in STAT_COLS]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=stats_values + [stats_values[0]],
                theta=STAT_COLS + [STAT_COLS[0]],
                fill='toself',
                fillcolor='rgba(96, 165, 250, 0.3)',  # Light blue transparent fill like Image 2
                line=dict(color='#60A5FA', width=2.5),  # Light blue outline like Image 2
                name=row['Pokemon']
            ))
            apply_plotly_theme(fig)
            fig.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',  # Make circle background transparent to show dark app background
                    radialaxis=dict(
                        visible=True, 
                        range=[0, 250],
                        gridcolor="rgba(255, 255, 255, 0.2)",  # More visible grid lines like Image 2
                        linecolor="rgba(255, 255, 255, 0.2)"
                    ),
                    angularaxis=dict(
                        type='category',
                        categoryorder='array',
                        categoryarray=STAT_COLS,
                        gridcolor="rgba(255, 255, 255, 0.2)",  # More visible spoke lines like Image 2
                        linecolor="rgba(255, 255, 255, 0.2)"
                    )
                ),
                showlegend=False,
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_charts_b:
            st.subheader("Informasi Karakteristik Lainnya")
            info_cols = ["Ability I", "Ability II", "Hidden Ability", "EV Worth", "Gender",
                         "Egg Group I", "Egg Group II", "Catch", "Evolve"]
            info_data = {c: row[c] for c in info_cols if pd.notna(row[c])}
            st.table(pd.DataFrame(info_data.items(), columns=["Kategori Data", "Nilai Karakteristik"]))

# ==================================================
# 4. COMPARE STATS
# ==================================================
elif menu == "Compare Stats":
    champion_header("Battle Simulator & Stat Comparison", "Bandingkan dua Pokemon secara langsung untuk menganalisis keunggulan taktis.")

    pokemon_list = sorted(df["Pokemon"].unique().tolist())

    c_select_a, c_select_b = st.columns(2)
    with c_select_a:
        pokemon_a = st.selectbox("Pilih Pokemon A", pokemon_list, index=0, key="a")
    with c_select_b:
        pokemon_b = st.selectbox("Pilih Pokemon B", pokemon_list, index=1, key="b")

    if pokemon_a and pokemon_b:
        row_a = df[df["Pokemon"] == pokemon_a].iloc[0]
        row_b = df[df["Pokemon"] == pokemon_b].iloc[0]

        st.markdown("<br>", unsafe_allow_html=True)
        
        c_disp_a, c_disp_b = st.columns(2)
        with c_disp_a:
            type_a = row_a["Type I"] + (f" / {row_a['Type II']}" if pd.notna(row_a["Type II"]) else "")
            badge_a = "".join([f'<span style="background-color: {TYPE_COLORS.get(t.strip(), "#777")}; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; margin-right: 5px; font-size: 0.85rem;">{t.strip()}</span>' for t in type_a.split("/")])
            
            st.markdown(f"""
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
                <h3 style="margin: 0 0 10px 0; color: #ff6b6b; font-size: 1.8rem;">🛡️ {row_a['Pokemon']}</h3>
                <div style="margin-bottom: 10px;">{badge_a}</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #ffffff;">Total Stats: {row_a['Total']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c_disp_b:
            type_b = row_b["Type I"] + (f" / {row_b['Type II']}" if pd.notna(row_b["Type II"]) else "")
            badge_b = "".join([f'<span style="background-color: {TYPE_COLORS.get(t.strip(), "#777")}; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; margin-right: 5px; font-size: 0.85rem;">{t.strip()}</span>' for t in type_b.split("/")])
            
            st.markdown(f"""
            <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
                <h3 style="margin: 0 0 10px 0; color: #4ecdc4; font-size: 1.8rem;">⚔️ {row_b['Pokemon']}</h3>
                <div style="margin-bottom: 10px;">{badge_b}</div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #ffffff;">Total Stats: {row_b['Total']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Data Tabel Perbandingan")

        compare_df = pd.DataFrame({
            "Statistik": STAT_COLS + ["Total"],
            row_a["Pokemon"]: [row_a[s] for s in STAT_COLS] + [row_a["Total"]],
            row_b["Pokemon"]: [row_b[s] for s in STAT_COLS] + [row_b["Total"]],
            "Selisih": [abs(int(row_a[s]) - int(row_b[s])) for s in STAT_COLS] + [abs(int(row_a["Total"]) - int(row_b["Total"]))]
        })
        st.dataframe(compare_df, use_container_width=True, hide_index=True)

        c_graph_a, c_graph_b = st.columns(2)
        
        with c_graph_a:
            st.subheader("Grafik Perbandingan Stats")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=row_a["Pokemon"], 
                x=STAT_COLS, 
                y=[row_a[s] for s in STAT_COLS],
                marker_color='#FF4B4B',
                text=[row_a[s] for s in STAT_COLS],
                textposition='auto'
            ))
            fig.add_trace(go.Bar(
                name=row_b["Pokemon"], 
                x=STAT_COLS, 
                y=[row_b[s] for s in STAT_COLS],
                marker_color='#06B6D4',
                text=[row_b[s] for s in STAT_COLS],
                textposition='auto'
            ))
            apply_plotly_theme(fig)
            fig.update_layout(barmode='group', height=450, yaxis_title="Nilai Stats")
            st.plotly_chart(fig, use_container_width=True)

        with c_graph_b:
            st.subheader("Radar Chart Perbandingan")
            fig2 = go.Figure()
            vals_a = [row_a[s] for s in STAT_COLS]
            vals_b = [row_b[s] for s in STAT_COLS]
            
            fig2.add_trace(go.Scatterpolar(
                r=vals_a + [vals_a[0]], 
                theta=STAT_COLS + [STAT_COLS[0]],
                fill='toself', 
                fillcolor='rgba(255, 75, 75, 0.15)',
                line=dict(color='#FF4B4B', width=2.5), 
                name=row_a["Pokemon"]
            ))
            fig2.add_trace(go.Scatterpolar(
                r=vals_b + [vals_b[0]], 
                theta=STAT_COLS + [STAT_COLS[0]],
                fill='toself', 
                fillcolor='rgba(6, 182, 212, 0.15)',
                line=dict(color='#06B6D4', width=2.5), 
                name=row_b["Pokemon"]
            ))
            apply_plotly_theme(fig2)
            fig2.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',  # Make circle background transparent to show dark app background
                    radialaxis=dict(
                        visible=True, 
                        range=[0, 250],
                        gridcolor="rgba(255, 255, 255, 0.2)",
                        linecolor="rgba(255, 255, 255, 0.2)"
                    ),
                    angularaxis=dict(
                        type='category',
                        categoryorder='array',
                        categoryarray=STAT_COLS,
                        gridcolor="rgba(255, 255, 255, 0.2)",
                        linecolor="rgba(255, 255, 255, 0.2)"
                    )
                ),
                height=450
            )
            st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# 5. TYPE RECOMMENDATION (MERGED WITH FINDER)
# ==================================================
elif menu == "Type Recommendation":
    champion_header("Type Recommendation & Meta Explorer", "Dapatkan rekomendasi Pokemon terbaik berdasarkan tipe dan prioritas statistik.")

    all_types = sorted(pd.concat([df["Type I"], df["Type II"]]).dropna().unique().tolist())
    type_options = ["All"] + all_types

    c1, c2 = st.columns(2)
    with c1:
        selected_type = st.selectbox("Pilih Tipe Pokemon (Pilih 'All' untuk Semua)", type_options)
    with c2:
        selected_stat = st.selectbox("Pilih Prioritas Stat Utama", STAT_COLS + ["Total"])

    if selected_type == "All":
        # Behaviour similar to old Pokemon Finder from Stat (Top 10)
        top_data = df.sort_values(selected_stat, ascending=False).head(10).reset_index(drop=True)
        top_data.index = top_data.index + 1
        
        st.subheader(f"Top 10 Pokemon Terbaik (Berdasarkan {selected_stat})")
        display_cols = ["Pokemon", "Type I", "Type II"] + STAT_COLS + ["Total"]
        st.dataframe(top_data[display_cols], use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        fig = px.bar(
            top_data.sort_values(selected_stat),
            x=selected_stat,
            y="Pokemon",
            orientation="h",
            color=selected_stat,
            color_continuous_scale="Viridis",
            text=selected_stat
        )
        apply_plotly_theme(fig)
        fig.update_layout(height=500, yaxis_title="", xaxis_title=selected_stat, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        filtered = df[(df["Type I"] == selected_type) | (df["Type II"] == selected_type)]
        if filtered.empty:
            st.warning(f"Tidak ditemukan Pokemon dengan tipe {selected_type} dalam database.")
        else:
            top_n = min(10, len(filtered))
            top_data = filtered.sort_values(selected_stat, ascending=False).head(top_n).reset_index(drop=True)
            top_data.index = top_data.index + 1

            st.subheader(f"Top {top_n} Pokemon Tipe {selected_type} Terbaik (Berdasarkan {selected_stat})")
            display_cols = ["Pokemon", "Type I", "Type II"] + STAT_COLS + ["Total"]
            st.dataframe(top_data[display_cols], use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            fig = px.bar(
                top_data.sort_values(selected_stat),
                x=selected_stat,
                y="Pokemon",
                orientation="h",
                color=selected_stat,
                color_continuous_scale="Tealgrn",
                text=selected_stat
            )
            apply_plotly_theme(fig)
            fig.update_layout(height=450, yaxis_title="", xaxis_title=selected_stat, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

# ------------------ FOOTER ------------------
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.caption("⚡ Pokemon Champions League Season 2")
