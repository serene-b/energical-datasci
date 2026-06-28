import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Energical — Sales Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <h1 style='font-size:2.8rem; font-weight:800; color:#e2e8f0; margin-bottom:0;'>
        ⚡ Energical Sales Intelligence
    </h1>
    <p style='font-size:1rem; color:#94a3b8; margin-top:4px; letter-spacing:0.05em;'>
        DataFest 2026 · <b style='color:#f5a623;'>The Outliers</b>
    </p>
    <hr style='border-color:#1e2340; margin: 12px 0 20px 0;'>
""", unsafe_allow_html=True)


# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    "bg":        "#0b0e1a",
    "surface":   "#131729",
    "border":    "#1e2340",
    "primary":   "#4f8ef7",
    "accent":    "#f5a623",
    "danger":    "#e05c5c",
    "success":   "#3ecf8e",
    "muted":     "#6b7280",
    "text":      "#e2e8f0",
    "text_dim":  "#94a3b8",
}

SEQ   = ["#1e3a8a","#2563eb","#4f8ef7","#93c5fd","#bfdbfe"]
QUAL  = [C["primary"], C["accent"], C["success"], C["danger"],
         "#a78bfa", "#34d399", "#fb923c", "#f472b6"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {C['bg']};
    color: {C['text']};
}}
.stApp {{ background-color: {C['bg']}; }}

/* sidebar */
[data-testid="stSidebar"] {{
    background-color: {C['surface']};
    border-right: 1px solid {C['border']};
}}
[data-testid="stSidebar"] * {{ color: {C['text']} !important; }}

/* tabs */
.stTabs [data-baseweb="tab-list"] {{
    background: {C['surface']};
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border: 1px solid {C['border']};
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: {C['text_dim']};
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 6px 16px;
}}
.stTabs [aria-selected="true"] {{
    background: {C['primary']} !important;
    color: white !important;
}}

/* metrics */
[data-testid="metric-container"] {{
    background: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 18px 20px;
}}
[data-testid="metric-container"] label {{
    color: {C['text_dim']} !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-weight: 600;
}}
[data-testid="stMetricValue"] {{
    color: {C['text']} !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.8rem !important; }}

/* cards */
.card {{
    background: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
}}
.section-label {{
    font-size: 0.72rem;
    font-weight: 700;
    color: {C['text_dim']};
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: 12px;
}}
.so-what {{
    background: linear-gradient(135deg, #1e3a5f 0%, #1a2e4a 100%);
    border-left: 3px solid {C['primary']};
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    font-size: 0.9rem;
    color: {C['text']};
    margin: 12px 0;
    line-height: 1.6;
}}
.alert-card {{
    background: linear-gradient(135deg, #2d1a1a 0%, #1f1212 100%);
    border-left: 3px solid {C['danger']};
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.85rem;
}}
.alert-card-warn {{
    background: linear-gradient(135deg, #2d2210 0%, #1f1a0a 100%);
    border-left: 3px solid {C['accent']};
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.85rem;
}}
.risk-high   {{ color: {C['danger']}; font-weight:700; }}
.risk-medium {{ color: {C['accent']}; font-weight:700; }}
.risk-low    {{ color: {C['success']}; font-weight:700; }}
hr {{ border-color: {C['border']}; margin: 20px 0; }}

/* title fix — force full opacity */
h1, h2, h3, h4 {{
    color: {C['text']} !important;
    opacity: 1 !important;
}}
h1 {{ font-size: 1.9rem !important; font-weight: 700 !important; }}
</style>
""", unsafe_allow_html=True)

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=C["text"], family="Inter, sans-serif", size=12),
    margin=dict(l=0, r=0, t=28, b=0),
)

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
DATA_DIR = os.path.join(os.getcwd(), "Data")

@st.cache_data
def load_all():
    clean   = pd.read_csv(os.path.join(DATA_DIR, "data_clean.csv"),   parse_dates=["date_commande"])
    returns = pd.read_csv(os.path.join(DATA_DIR, "data_returns.csv"), parse_dates=["date_commande"])
    loyalty = pd.read_csv(os.path.join(DATA_DIR, "customer_loyalty.csv"))
    return clean, returns, loyalty

try:
    df, df_ret, df_loyalty = load_all()
    df["date_commande"] = pd.to_datetime(df["date_commande"], errors="coerce")
    df_ret["date_commande"] = pd.to_datetime(df_ret["date_commande"], errors="coerce")
    DATA_OK = True
except FileNotFoundError:
    DATA_OK = False

st.markdown(f"""
<div style='
    background: linear-gradient(135deg, #131729 0%, #0f1117 100%);
    border: 1px solid #1e2340;
    border-radius: 12px;
    padding: 18px 28px;
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 24px;
    flex-wrap: wrap;
'>
    <div style='flex:1; text-align:center; padding: 8px 20px; border-right: 1px solid #1e2340;'>
        <span style='font-size:1.7rem; font-weight:800; color:#4f8ef7;'>17,263</span>
        <div style='font-size:0.75rem; color:#94a3b8; text-transform:uppercase; letter-spacing:.1em; margin-top:2px;'>Transactions</div>
    </div>
    <div style='flex:1; text-align:center; padding: 8px 20px; border-right: 1px solid #1e2340;'>
        <span style='font-size:1.7rem; font-weight:800; color:#f5a623;'>4,112</span>
        <div style='font-size:0.75rem; color:#94a3b8; text-transform:uppercase; letter-spacing:.1em; margin-top:2px;'>Customers</div>
    </div>
    <div style='flex:1; text-align:center; padding: 8px 20px;'>
        <span style='font-size:1.7rem; font-weight:800; color:#3ecf8e;'>3 ans</span>
        <div style='font-size:0.75rem; color:#94a3b8; text-transform:uppercase; letter-spacing:.1em; margin-top:2px;'>2022 – 2024</div>
    </div>
</div>
""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — global filters
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("# ⚡ Energical")
    st.caption("DataFest 2026 · The Outliers")

    st.markdown("---")
    if not DATA_OK:
        st.error("Data files not found.\nPlace `df_clean.csv`, `df_returns.csv`, `customer_loyalty.csv` in the `/data` folder.")
        st.stop()

    st.markdown("# Filters")

    # Year
    years = sorted(df["date_commande"].dt.year.dropna().unique().astype(int))
    sel_years = st.multiselect("Year", years, default=years)

    # Wilaya
    wilayas = sorted(df["wilaya"].dropna().unique())
    sel_wilayas = st.multiselect("Wilaya", wilayas, default=wilayas)

    # Category
    cats = sorted(df["categorie_produit"].dropna().unique())
    sel_cats = st.multiselect("Category", cats, default=cats)

    # Client type
    client_types = sorted(df["type_client"].dropna().unique())
    sel_types = st.multiselect("Client type", client_types, default=client_types)

    st.markdown("---")
    

# ══════════════════════════════════════════════════════════════════════════════
# APPLY FILTERS
# ══════════════════════════════════════════════════════════════════════════════
mask = (
    df["date_commande"].dt.year.isin(sel_years) &
    df["wilaya"].isin(sel_wilayas) &
    df["categorie_produit"].isin(sel_cats) &
    df["type_client"].isin(sel_types)
)
dff = df[mask].copy()

if dff.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("# Sales Intelligence Dashboard")

st.markdown("---")
# ══════════════════════════════════════════════════════════════════════════════
# RFM SEGMENTATION — computed from filtered completed orders
# ══════════════════════════════════════════════════════════════════════════════
analysis_date = dff["date_commande"].max() + pd.Timedelta(days=1)

rfm = (
    dff.groupby("id_client")
    .agg(
        Recency=("date_commande", lambda x: (analysis_date - x.max()).days),
        Frequency=("id_commande_anon", "nunique"),
        Monetary=("montant_da", "sum"),
        Wilaya=("wilaya", lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]),
        Type=("type_client", lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]),
        Favorite_Category=("categorie_produit", lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]),
    )
    .reset_index()
)

def assign_rfm_segment(row):
    if row["Frequency"] >= 10 and row["Monetary"] >= rfm["Monetary"].quantile(0.90) and row["Recency"] <= rfm["Recency"].quantile(0.35):
        return "🟢 Champions"
    elif row["Recency"] <= rfm["Recency"].quantile(0.65):
        return "🟡 Occasional Customers"
    else:
        return "🔴 Low-Engagement Customers"

rfm["RFM Segment"] = rfm.apply(assign_rfm_segment, axis=1)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈  Overview",
    "🗺️  Wilayas",
    "👥  Clients",
    "📦  Products",
    "⚠️  Alerts",
    
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
     # ── KPIs ─────────────────────────────────────────────────────────────────
    total_rev    = dff["montant_da"].sum()
    total_orders = dff["id_commande_anon"].nunique()
    avg_order    = dff["montant_da"].mean()
    n_clients    = dff["id_client"].nunique()
    total_profit = dff["profit_estime"].sum() if "profit_estime" in dff.columns else None

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Revenue",       f"{total_rev/1e6:.2f}M DA")
    k2.metric("Total Orders",        f"{total_orders:,}")
    k3.metric("Avg Order Value",     f"{avg_order:,.0f} DA")
    k4.metric("Active Clients",      f"{n_clients:,}")
    k5.metric("Est. Profit",         f"{total_profit/1e6:.2f}M DA" if total_profit else "—")

    st.markdown("---")

     # ── Algeria revenue map ───────────────────────────────────────────────────
    st.markdown('<p class="section-label">Revenue across Algeria — by wilaya</p>',
                unsafe_allow_html=True)

    # Wilaya centroids (lat/lon) — all 48 wilayas
    WILAYA_COORDS = {
        "adrar": (27.87, -0.29), "chlef": (36.16, 1.33), "laghouat": (33.80, 2.87),
        "oum el bouaghi": (35.87, 7.11), "batna": (35.56, 6.17), "béjaïa": (36.75, 5.08),
        "biskra": (34.85, 5.73), "béchar": (31.62, -2.22), "blida": (36.47, 2.83),
        "bouira": (36.37, 3.90), "tamanrasset": (22.79, 5.52), "tébessa": (35.40, 8.12),
        "tlemcen": (34.88, -1.32), "tiaret": (35.37, 1.32), "tizi ouzou": (36.71, 4.05),
        "alger": (36.74, 3.06), "djelfa": (34.67, 3.26), "jijel": (36.82, 5.77),
        "sétif": (36.19, 5.41), "saïda": (34.83, 0.15), "skikda": (36.88, 6.91),
        "sidi bel abbès": (35.19, -0.63), "annaba": (36.90, 7.77), "guelma": (36.46, 7.43),
        "constantine": (36.37, 6.61), "médéa": (36.27, 2.75), "mostaganem": (35.93, 0.09),
        "msila": (35.70, 4.54), "mascara": (35.40, 0.14), "ouargla": (31.95, 5.33),
        "oran": (35.69, -0.64), "el bayadh": (33.68, 1.02), "illizi": (26.48, 8.48),
        "bordj bou arreridj": (36.07, 4.76), "boumerdès": (36.76, 3.47),
        "el tarf": (36.77, 8.31), "tindouf": (27.67, -8.15), "tissemsilt": (35.60, 1.81),
        "el oued": (33.37, 6.86), "khenchela": (35.43, 7.14), "souk ahras": (36.28, 7.95),
        "tipaza": (36.59, 2.45), "mila": (36.45, 6.26), "aïn defla": (36.26, 1.97),
        "naâma": (33.27, -0.31), "aïn témouchent": (35.30, -1.14),
        "ghardaïa": (32.49, 3.67), "relizane": (35.74, 0.56),
    }

    map_df = (
        dff.groupby("wilaya")["montant_da"].sum()
        .reset_index()
        .rename(columns={"montant_da": "revenue"})
    )
    map_df["wilaya_lower"] = map_df["wilaya"].str.lower().str.strip()
    map_df["lat"] = map_df["wilaya_lower"].map(lambda w: WILAYA_COORDS.get(w, (None, None))[0])
    map_df["lon"] = map_df["wilaya_lower"].map(lambda w: WILAYA_COORDS.get(w, (None, None))[1])
    map_df = map_df.dropna(subset=["lat", "lon"])
    map_df["revenue_label"] = map_df["revenue"].apply(lambda x: f"{x/1e6:.2f}M DA")

    if not map_df.empty:
        fig_map = px.scatter_map(
            map_df,
            lat="lat", lon="lon",
            size="revenue",
            color="revenue",
            hover_name="wilaya",
            hover_data={"revenue_label": True, "lat": False, "lon": False,
                        "revenue": False, "wilaya_lower": False},
            color_continuous_scale=["#4b3876", C["primary"], C["accent"]],
            size_max=55,
            zoom=4.5,
            center={"lat": 28.0, "lon": 2.5},
            map_style="carto-darkmatter",
            labels={"revenue": "Revenue (DA)", "revenue_label": "Revenue"},
        )
        fig_map.update_layout(
            **PLOT,
            height=480,
            coloraxis_colorbar=dict(
                title="Revenue (DA)",
                tickprefix="",
                tickformat=".2s",
            ),
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Map unavailable — wilaya names in your data didn't match the coordinate table. "
                "Check that wilayas are standardized in your cleaning step.")

   
    # ── Revenue over time ─────────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<p class="section-label">Revenue over time jul2021-jul2024</p>', unsafe_allow_html=True)

        monthly = (
            dff.groupby(dff["date_commande"].dt.to_period("M"))
            .agg(revenue=("montant_da", "sum"), orders=("id_commande_anon", "nunique"))
            .reset_index()
        )
        monthly["date"] = monthly["date_commande"].dt.to_timestamp()

        fig_time = make_subplots(specs=[[{"secondary_y": True}]])
        fig_time.add_trace(go.Bar(
            x=monthly["date"], y=monthly["revenue"],
            name="Revenue (DA)", marker_color=C["primary"], opacity=0.85,
        ), secondary_y=False)
        fig_time.add_trace(go.Scatter(
            x=monthly["date"], y=monthly["orders"],
            name="Orders", mode="lines+markers",
            line=dict(color=C["accent"], width=2), marker=dict(size=4),
        ), secondary_y=True)
        fig_time.update_layout(
            **PLOT,
            legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, color=C["text_dim"]),
            yaxis=dict(gridcolor=C["border"], color=C["text_dim"]),
            yaxis2=dict(gridcolor="rgba(0,0,0,0)", color=C["accent"]),
            height=300,
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-label">Revenue by category</p>', unsafe_allow_html=True)
        pie_df = dff.groupby("categorie_produit")["montant_da"].sum().reset_index()
        fig_pie = px.pie(pie_df, values="montant_da", names="categorie_produit",
                         hole=0.3, color_discrete_sequence=QUAL)
        fig_pie.update_traces(textposition="outside", textinfo="percent+label",
                              textfont_size=10)
        fig_pie.update_layout(**PLOT, showlegend=False, height=250)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ── So what sentence — Overview ───────────────────────────────────────────
    best_month = monthly.loc[monthly["revenue"].idxmax(), "date"].strftime("%B %Y")
    best_cat   = pie_df.loc[pie_df["montant_da"].idxmax(), "categorie_produit"]
    best_cat_pct = pie_df["montant_da"].max() / pie_df["montant_da"].sum() * 100
    st.markdown(
        f'<div class="so-what">💡 <b>Key insight:</b> Revenue peaked in <b>{best_month}</b>. '
        f'<b>{best_cat}</b> drives <b>{best_cat_pct:.0f}%</b> of total revenue across the selected filters — '
        f'prioritize stock availability for this category ahead of peak season.</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

   
# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — WILAYAS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:

    # ── Wilaya revenue ────────────────────────────────────────────────────────
    wilaya_rev = (
        dff.groupby("wilaya")
        .agg(
            revenue=("montant_da", "sum"),
            clients=("id_client", "nunique"),
            orders=("id_commande_anon", "nunique"),
        )
        .reset_index()
    )
    wilaya_rev["revenue_per_client"] = (wilaya_rev["revenue"] / wilaya_rev["clients"]).round(0)

        # ── Return rate ────────────────────────────────────────────────────────────
    # Normalize wilaya case in both dataframes
    df["wilaya_norm"]     = df["wilaya"].str.lower().str.strip()
    df_ret["wilaya_norm"] = df_ret["wilaya"].str.lower().str.strip()

    # Filter ONLY actual returns (not pending deliveries)
    RETURN_STATUTS = ["Retour NOEST", "Retournée"]
    df_actual_returns = df_ret[df_ret["statut_commande"].isin(RETURN_STATUTS)]

    # Compute return rate
    total_by_wilaya  = df.groupby("wilaya_norm").size().reset_index(name="total")
    return_by_wilaya = df_actual_returns.groupby(
        df_actual_returns["wilaya"].str.lower().str.strip()
    ).size().reset_index(name="returns")
    return_by_wilaya.columns = ["wilaya_norm", "returns"]

    wilaya_ret = total_by_wilaya.merge(return_by_wilaya, on="wilaya_norm", how="left").fillna(0)
    wilaya_ret["return_rate"] = (wilaya_ret["returns"] / wilaya_ret["total"] * 100).round(2)
    wilaya_ret["wilaya"] = wilaya_ret["wilaya_norm"]  # keep consistent name

    # Merge into wilaya_rev
    wilaya_rev["wilaya_norm"] = wilaya_rev["wilaya"].str.lower().str.strip()
    wilaya_rev = wilaya_rev.merge(
        wilaya_ret[["wilaya_norm", "return_rate"]], on="wilaya_norm", how="left"
    ).fillna(0)

    # Debug — remove after confirming it works
    st.caption(f"Returns found: {len(df_actual_returns)} | Wilayas with returns: {(wilaya_ret['returns']>0).sum()}")
    # ── Opportunity score ─────────────────────────────────────────────────────
    def norm(s):
        rng = s.max() - s.min()
        return (s - s.min()) / rng if rng > 0 else s * 0
    wilaya_rev["opp_score"] = (
        norm(wilaya_rev["revenue_per_client"]) * 0.5 +
        norm(wilaya_rev["orders"]) * 0.3 +
        (1 - norm(wilaya_rev["return_rate"])) * 0.2
    ).round(3)

    # ── Row 1: revenue bar + return rate ─────────────────────────────────────
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<p class="section-label">Revenue by wilaya — top 20</p>', unsafe_allow_html=True)
        top20 = wilaya_rev.sort_values("revenue", ascending=False).head(20)
        fig_wrev = px.bar(
            top20, x="revenue", y="wilaya", orientation="h",
            color="revenue", color_continuous_scale=SEQ,
            hover_data={"clients": True, "orders": True, "revenue_per_client": True},
            labels={"revenue": "Revenue (DA)", "wilaya": ""},
            text=top20["revenue"].apply(lambda x: f"{x/1e6:.1f}M"),
        )
        fig_wrev.update_traces(textposition="outside")
        fig_wrev.update_layout(**PLOT, showlegend=False, height=480,
                               yaxis=dict(categoryorder="total ascending"),
                               coloraxis_showscale=False)
        st.plotly_chart(fig_wrev, use_container_width=True)

    with col2:
        st.markdown('<p class="section-label">Return rate by wilaya — top 15 (%)</p>', unsafe_allow_html=True)
        top_ret = wilaya_ret[wilaya_ret["returns"] > 0].sort_values("return_rate", ascending=False).head(15)
        fig_ret = px.bar(
            top_ret, x="return_rate", y="wilaya", orientation="h",
            color="return_rate",
            color_continuous_scale=["#1e3a2e", C["accent"], C["danger"]],
            text=top_ret["return_rate"].apply(lambda x: f"{x:.1f}%"),
            labels={"return_rate": "Return rate (%)", "wilaya": ""},
        )
        fig_ret.update_traces(textposition="outside")
        fig_ret.update_layout(**PLOT, showlegend=False, height=480,
                              yaxis=dict(categoryorder="total ascending"),
                              coloraxis_showscale=False)
        st.plotly_chart(fig_ret, use_container_width=True)

    st.markdown("---")

    # ── Opportunity scatter ───────────────────────────────────────────────────
    st.markdown('<p class="section-label">Wilaya opportunity map — revenue/client vs order volume</p>',
                unsafe_allow_html=True)
    fig_opp = px.scatter(
        wilaya_rev, x="orders", y="revenue_per_client",
        size="revenue", color="opp_score",
        color_continuous_scale=["#1e2340", C["primary"], C["accent"]],
        text="wilaya",
        hover_data={"opp_score": ":.3f", "return_rate": ":.1f",
                    "revenue": ":,.0f", "clients": True},
        labels={
            "orders": "Number of orders",
            "revenue_per_client": "Revenue per client (DA)",
            "opp_score": "Opportunity score",
        },
        size_max=50,
    )
    fig_opp.update_traces(textposition="top center", textfont_size=10)
    fig_opp.update_layout(**PLOT, height=420,
                          xaxis=dict(gridcolor=C["border"]),
                          yaxis=dict(gridcolor=C["border"]),
                          coloraxis_colorbar=dict(title="Opp. score"))
    st.plotly_chart(fig_opp, use_container_width=True)

    # ── So what — Wilayas ─────────────────────────────────────────────────────
    top_opp   = wilaya_rev.nlargest(1, "opp_score").iloc[0]
    top_ret_w = top_ret.iloc[0] if len(top_ret) > 0 else None
    so_what_wilaya = (
        f'💡 <b>{top_opp["wilaya"]}</b> has the highest opportunity score '
        f'(<b>{top_opp["opp_score"]:.2f}</b>) with '
        f'<b>{top_opp["revenue_per_client"]:,.0f} DA</b> revenue per client.'
    )
    if top_ret_w is not None:
        so_what_wilaya += (
            f' Watch <b>{top_ret_w["wilaya"]}</b> — highest return rate at '
            f'<b>{top_ret_w["return_rate"]:.1f}%</b>. '
            f'Investigate logistics or product quality before scaling campaigns there.'
        )
    st.markdown(f'<div class="so-what">{so_what_wilaya}</div>', unsafe_allow_html=True)

    st.markdown("---")

    

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CLIENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:

    # ── KPIs ──────────────────────────────────────────────────────────────────
    low_retention = df_loyalty[df_loyalty["Retention Level"] == "Low"].copy()
    ltv_low_retention = low_retention["total_spent"].sum()
    n_low_retention = len(low_retention)
    pct_low_retention = (
        n_low_retention / len(df_loyalty) * 100 if len(df_loyalty) > 0 else 0
    )

    ck1, ck2, ck3, ck4 = st.columns(4)
    ck1.metric("Total Clients", f"{df_loyalty.shape[0]:,}")
    ck2.metric(
        "Low-Retention Clients",
        f"{n_low_retention:,}",
        delta=f"{pct_low_retention:.1f}% of base",
        delta_color="inverse",
    )
    ck3.metric(
        "Potential LTV to Recover",
        f"{ltv_low_retention/1e6:.2f}M DA",
        delta="reactivation opportunity",
        delta_color="inverse",
    )
    ck4.metric(
        "Avg Retention Score",
        f"{df_loyalty['Retention Score'].mean():.2f}",
    )

    st.markdown("---")

    # ── RFM SEGMENTATION ──────────────────────────────────────────────────────
    st.markdown(
        '<p class="section-label">RFM customer segmentation</p>',
        unsafe_allow_html=True,
    )

    rfm_counts = rfm["RFM Segment"].value_counts().reset_index()
    rfm_counts.columns = ["Segment", "Clients"]

    col_rfm1, col_rfm2 = st.columns([1, 1])

    with col_rfm1:
        fig_rfm = px.pie(
            rfm_counts,
            values="Clients",
            names="Segment",
            hole=0.5,
            color="Segment",
            color_discrete_map={
                "🟢 Champions": C["success"],
                "🟡 Occasional Customers": C["accent"],
                "🔴 Low-Engagement Customers": C["danger"],
            },
        )
        fig_rfm.update_traces(textposition="outside", textinfo="percent+label")
        fig_rfm.update_layout(**PLOT, showlegend=False, height=300)
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col_rfm2:
        rfm_summary = (
            rfm.groupby("RFM Segment")
            .agg(
                Clients=("id_client", "count"),
                Avg_Recency=("Recency", "mean"),
                Avg_Frequency=("Frequency", "mean"),
                Avg_Monetary=("Monetary", "mean"),
            )
            .reset_index()
        )

        rfm_summary["Avg_Recency"] = rfm_summary["Avg_Recency"].round(0)
        rfm_summary["Avg_Frequency"] = rfm_summary["Avg_Frequency"].round(1)
        rfm_summary["Avg_Monetary"] = rfm_summary["Avg_Monetary"].apply(
            lambda x: f"{x:,.0f} DA"
        )

        st.dataframe(rfm_summary, use_container_width=True, height=260)

    st.markdown("---")

    # ── RFM CUSTOMER ACTION LIST ───────────────────────────────────────────────
    st.markdown(
        '<p class="section-label">Customer action list — based on RFM segment</p>',
        unsafe_allow_html=True,
    )

    rfm_actions = rfm.copy()

    rfm_actions["Recommended Action"] = rfm_actions["RFM Segment"].map(
        {
            "🟢 Champions": "VIP retention: exclusive offers + priority service",
            "🟡 Occasional Customers": "Increase frequency: reminder campaign + product recommendation",
            "🔴 Low-Engagement Customers": "Reactivation: limited-time offer, then reduce marketing spend if inactive",
        }
    )

    rfm_display = rfm_actions[
        [
            "id_client",
            "Wilaya",
            "Type",
            "Favorite_Category",
            "Recency",
            "Frequency",
            "Monetary",
            "RFM Segment",
            "Recommended Action",
        ]
    ].rename(
        columns={
            "id_client": "Client",
            "Favorite_Category": "Top Category",
            "Recency": "Days Since Last Purchase",
            "Frequency": "Orders",
            "Monetary": "Total Spend (DA)",
        }
    )

    rfm_display["Total Spend (DA)"] = rfm_display["Total Spend (DA)"].apply(
        lambda x: f"{x:,.0f}"
    )

    st.dataframe(rfm_display, use_container_width=True, height=330)

    st.download_button(
        "⬇ Export RFM customer action list",
        rfm_display.to_csv(index=False).encode(),
        "rfm_customer_actions.csv",
        "text/csv",
    )

    # ── SO WHAT — RFM ─────────────────────────────────────────────────────────
    champions = rfm[rfm["RFM Segment"] == "🟢 Champions"]
    occasional = rfm[rfm["RFM Segment"] == "🟡 Occasional Customers"]
    low_engagement = rfm[rfm["RFM Segment"] == "🔴 Low-Engagement Customers"]

    st.markdown(
        f'<div class="so-what">💡 <b>RFM insight:</b> '
        f'<b>{len(champions)}</b> Champions should receive VIP retention actions. '
        f'<b>{len(occasional)}</b> Occasional Customers are the main growth opportunity. '
        f'<b>{len(low_engagement)}</b> Low-Engagement Customers should receive a reactivation campaign, '
        f'then reduced marketing spend if they remain inactive.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── B2B vs B2C ────────────────────────────────────────────────────────────
    col_e, col_f = st.columns([1, 1])

    with col_e:
        st.markdown(
            '<p class="section-label">B2B vs B2C — revenue split</p>',
            unsafe_allow_html=True,
        )

        seg = (
            dff.groupby("type_client")
            .agg(
                revenue=("montant_da", "sum"),
                clients=("id_client", "nunique"),
                avg_order=("montant_da", "mean"),
            )
            .reset_index()
        )

        fig_seg = px.bar(
            seg,
            x="type_client",
            y="revenue",
            color="type_client",
            color_discrete_sequence=[C["primary"], C["accent"]],
            text=seg["revenue"].apply(lambda x: f"{x/1e6:.1f}M DA"),
            labels={"revenue": "Revenue (DA)", "type_client": ""},
        )
        fig_seg.update_traces(textposition="outside")
        fig_seg.update_layout(
            **PLOT,
            showlegend=False,
            height=280,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor=C["border"]),
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    with col_f:
        st.markdown(
            '<p class="section-label">New vs returning clients — revenue over time</p>',
            unsafe_allow_html=True,
        )

        cohort = dff.copy()
        cohort["period"] = cohort["date_commande"].dt.to_period("M").dt.to_timestamp()

        cohort_agg = (
            cohort.groupby(["period", "nouveau_ou_fidele"])["montant_da"]
            .sum()
            .reset_index()
        )

        fig_cohort = px.line(
            cohort_agg,
            x="period",
            y="montant_da",
            color="nouveau_ou_fidele",
            color_discrete_sequence=[C["primary"], C["accent"]],
            markers=True,
            labels={
                "montant_da": "Revenue (DA)",
                "period": "",
                "nouveau_ou_fidele": "Client type",
            },
        )
        fig_cohort.update_layout(
            **PLOT,
            height=280,
            legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor=C["border"]),
        )
        st.plotly_chart(fig_cohort, use_container_width=True)

    st.markdown("---")

    # ── RETENTION MODEL OUTPUT ────────────────────────────────────────────────
    col_g, col_h = st.columns([1, 1])

    with col_g:
        st.markdown(
            '<p class="section-label">Retention model — level breakdown</p>',
            unsafe_allow_html=True,
        )

        ret_counts = df_loyalty["Retention Level"].value_counts().reset_index()
        ret_counts.columns = ["level", "count"]

        color_map = {
            "High": C["success"],
            "Medium": C["accent"],
            "Low": C["danger"],
        }

        fig_ret_pie = px.pie(
            ret_counts,
            values="count",
            names="level",
            hole=0.55,
            color="level",
            color_discrete_map=color_map,
        )
        fig_ret_pie.update_traces(textposition="outside", textinfo="percent+label")
        fig_ret_pie.update_layout(**PLOT, showlegend=False, height=260)
        st.plotly_chart(fig_ret_pie, use_container_width=True)

    with col_h:
        st.markdown(
            '<p class="section-label">Retention score distribution</p>',
            unsafe_allow_html=True,
        )

        fig_hist = px.histogram(
            df_loyalty,
            x="Retention Score",
            nbins=30,
            color_discrete_sequence=[C["primary"]],
        )
        fig_hist.update_layout(
            **PLOT,
            height=260,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor=C["border"]),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── LOW-RETENTION EXPORT ──────────────────────────────────────────────────
    if not low_retention.empty:
        st.markdown("---")
        st.markdown(
            '<p class="section-label">Low-retention clients — retention model output</p>',
            unsafe_allow_html=True,
        )

        low_display_cols = [
            "id_client",
            "wilaya",
            "type_client",
            "favorite_category",
            "total_orders",
            "total_spent",
            "days_since_last_order",
            "Retention Score",
            "Recommended Strategy",
        ]

        available_cols = [
            col for col in low_display_cols if col in low_retention.columns
        ]

        low_display = (
            low_retention[available_cols]
            .sort_values(
                "total_spent",
                ascending=False,
            )
            .rename(
                columns={
                    "id_client": "Client",
                    "wilaya": "Wilaya",
                    "type_client": "Type",
                    "favorite_category": "Top Category",
                    "total_orders": "Orders",
                    "total_spent": "LTV (DA)",
                    "days_since_last_order": "Days Inactive",
                    "Retention Score": "Score",
                    "Recommended Strategy": "Strategy",
                }
            )
            .reset_index(drop=True)
        )

        if "LTV (DA)" in low_display.columns:
            low_display["LTV (DA)"] = low_display["LTV (DA)"].apply(
                lambda x: f"{x:,.0f}"
            )

        if "Score" in low_display.columns:
            low_display["Score"] = low_display["Score"].apply(lambda x: f"{x:.2f}")

        st.dataframe(low_display, use_container_width=True, height=300)

        st.download_button(
            "⬇ Export low-retention clients",
            low_display.to_csv(index=False).encode(),
            "low_retention_clients.csv",
            "text/csv",
        )
# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ALERTS (Chaudière Winter Restock)
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
 
    CHAUDIERE_NAMES = [
        "Chaudière SL-DM24", "Chaudière SL-DM28", "Chaudière SL-DM18",
        "Chaudière SL-DL32", "Chaudière SL-DL36", "Chaudière SL-DT45",
        "Chaudière SL-DL24", "Chaudière à condensation QL-DO30",
        "Chaudière à condensation QL-DO24", "Chaudière chauffage seul SL-NM24",
        "Chaudière chauffage seul SL-NL36"
    ]
 
    df_chaud = df[df["produit"].isin(CHAUDIERE_NAMES)].copy()
 
    st.markdown('<p class="section-label">❄️ Chaudière winter restock alerts</p>',
                unsafe_allow_html=True)
    st.caption("Based on 3 years of historical sales data + supplier lead times. "
               "Chaudières peak in winter — orders must be placed before the season starts.")
 
    if df_chaud.empty:
        st.warning("No chaudière data found. Check that product names match exactly.")
    else:
        # ── Seasonal demand chart ─────────────────────────────────────────────
        st.markdown('<p class="section-label">Seasonal demand — all chaudière models (2022–2024)</p>',
                    unsafe_allow_html=True)
 
        monthly_pattern = (
            df_chaud.groupby(df_chaud["date_commande"].dt.month)
            .agg(qty=("quantite", "sum"), orders=("id_commande_anon", "nunique"))
            .reset_index()
        )
        monthly_pattern.columns = ["month_num", "qty", "orders"]
        monthly_pattern["month_name"] = pd.to_datetime(
            monthly_pattern["month_num"], format="%m"
        ).dt.strftime("%b")
 
        peak_month_num  = int(monthly_pattern.loc[monthly_pattern["qty"].idxmax(), "month_num"])
        peak_month_name = pd.to_datetime(str(peak_month_num), format="%m").strftime("%B")
 
        # highlight peak bar
        monthly_pattern["color"] = monthly_pattern["month_num"].apply(
            lambda m: C["danger"] if m == peak_month_num else C["primary"]
        )
 
        fig_season = go.Figure(go.Bar(
            x=monthly_pattern["month_name"],
            y=monthly_pattern["qty"],
            marker_color=monthly_pattern["color"],
            text=monthly_pattern["qty"],
            textposition="outside",
        ))
        fig_season.update_layout(
            **PLOT, height=300,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor=C["border"], title="Units sold"),
            annotations=[dict(
                x=peak_month_name[:3], y=monthly_pattern["qty"].max(),
                text=f"📌 Peak: {peak_month_name}",
                showarrow=True, arrowhead=2,
                font=dict(color=C["danger"], size=12),
                arrowcolor=C["danger"],
                ax=40, ay=-30,
            )]
        )
        st.plotly_chart(fig_season, use_container_width=True)
 
        st.markdown("---")
 
        # ── Per-model order deadline table ────────────────────────────────────
        st.markdown('<p class="section-label">Order deadline by chaudière model</p>',
                    unsafe_allow_html=True)
 
        today         = pd.Timestamp.today()
        current_month = today.month
        days_to_peak  = ((peak_month_num - current_month) % 12) * 30
 
        model_stats = (
            df_chaud.groupby("produit")
            .agg(
                total_sold=("quantite", "sum"),
                revenue=("montant_da", "sum"),
                delai=("delai_reappro_jours", "mean"),
            )
            .reset_index()
            .sort_values("revenue", ascending=False)
        )
 
        model_stats["order_by_date"] = model_stats["delai"].apply(
            lambda d: (today + pd.Timedelta(
                days=max(0, int(days_to_peak - d))
            )).strftime("%d %b %Y")
        )
        model_stats["status"] = model_stats["delai"].apply(
            lambda d: "🔴 ORDER NOW"  if days_to_peak <= d
            else ("🟡 PLAN SOON" if days_to_peak <= d + 30
            else "🟢 OK")
        )
 
        for _, row in model_stats.iterrows():
            if "🔴" in row["status"]:
                card = "alert-card"
            elif "🟡" in row["status"]:
                card = "alert-card-warn"
            else:
                card = ""
 
            if card:
                st.markdown(
                    f'<div class="{card}">'
                    f'{row["status"]} &nbsp;|&nbsp; <b>{row["produit"]}</b>'
                    f'<span style="float:right; color:#94a3b8; font-size:0.82rem;">'
                    f'Lead time: <b>{int(row["delai"])}j</b> &nbsp;·&nbsp; '
                    f'Order by: <b>{row["order_by_date"]}</b> &nbsp;·&nbsp; '
                    f'{int(row["total_sold"])} units sold &nbsp;·&nbsp; '
                    f'{row["revenue"]/1e6:.2f}M DA'
                    f'</span></div>',
                    unsafe_allow_html=True
                )
 
        # Green ones in expander
        green = model_stats[model_stats["status"] == "🟢 OK"]
        if not green.empty:
            with st.expander(f"🟢 {len(green)} models with sufficient time"):
                for _, row in green.iterrows():
                    st.markdown(
                        f'🟢 **{row["produit"]}** — '
                        f'Lead time: {int(row["delai"])}j · '
                        f'Order by: **{row["order_by_date"]}** · '
                        f'{int(row["total_sold"])} units · '
                        f'{row["revenue"]/1e6:.2f}M DA'
                    )
 
        st.markdown("---")
 
        # ── Full table ────────────────────────────────────────────────────────
        with st.expander("📋 Full model table"):
            display_tbl = model_stats[[
                "produit", "total_sold", "revenue",
                "delai", "order_by_date", "status"
            ]].rename(columns={
                "produit":       "Model",
                "total_sold":    "Units sold",
                "revenue":       "Revenue (DA)",
                "delai":         "Lead time (days)",
                "order_by_date": "Order by",
                "status":        "Status",
            }).copy()
            display_tbl["Revenue (DA)"] = display_tbl["Revenue (DA)"].apply(
                lambda x: f"{x:,.0f}"
            )
            st.dataframe(display_tbl.reset_index(drop=True), use_container_width=True)
 
        st.markdown("---")
 
        # ── So what ───────────────────────────────────────────────────────────
        n_urgent = (model_stats["status"].str.contains("🔴")).sum()
        n_soon   = (model_stats["status"].str.contains("🟡")).sum()
        top_model_rev = model_stats.iloc[0]["revenue"] if len(model_stats) > 0 else 0
        top_model_name = model_stats.iloc[0]["produit"] if len(model_stats) > 0 else ""
        avg_delai = int(model_stats["delai"].mean())
 
        st.markdown(
            f'<div class="so-what">💡 <b>Recommandation:</b> '
            f'Chaudière demand peaks every year in <b>{peak_month_name}</b>. '
            f'With an average supplier lead time of <b>{avg_delai} days</b>, '
            f'orders must be placed <b>by {(today + pd.Timedelta(days=max(0, days_to_peak - avg_delai))).strftime("%d %b %Y")}</b> at the latest. '
            f'<b>{n_urgent} model(s)</b> require immediate action — '
            f'starting with <b>{top_model_name}</b>, '
            f'Energical\'s top chaudière generating <b>{top_model_rev/1e6:.2f}M DA</b>.</div>',
            unsafe_allow_html=True
        )
 
# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PRODUCTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    # ── KPIs ──────────────────────────────────────────────────────────────────
    n_products   = dff["produit"].nunique()
    n_categories = dff["categorie_produit"].nunique()
    best_product = dff.groupby("produit")["montant_da"].sum().idxmax()
    best_product_rev = dff.groupby("produit")["montant_da"].sum().max()
    avg_margin = dff["marge_estimee_pct"].mean() if "marge_estimee_pct" in dff.columns else None

    pk1, pk2, pk3, pk4 = st.columns(4)
    pk1.metric("Unique Products",    f"{n_products:,}")
    pk2.metric("Categories",         f"{n_categories}")
    pk3.metric("Top Product Revenue",f"{best_product_rev/1e6:.2f}M DA")
    pk4.metric("Avg Margin",         f"{avg_margin:.1f}%" if avg_margin else "—")

    st.markdown("---")

    # ── TOP 10 BY REVENUE ─────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Top 10 products by revenue</p>', unsafe_allow_html=True)
    
    top10_rev = (
        dff.groupby("produit")["montant_da"].sum()
        .sort_values(ascending=False).head(10).reset_index()
    )
    top10_rev["label"] = top10_rev["produit"].str[:35]
    
    fig_top_rev = px.bar(
        top10_rev, x="montant_da", y="label", orientation="h",
        color="montant_da", color_continuous_scale=SEQ,
        text=top10_rev["montant_da"].apply(lambda x: f"{x/1e6:.2f}M DA"),
        labels={"montant_da": "Revenue (DA)", "label": ""}
    )
    fig_top_rev.update_traces(textposition="outside")
    fig_top_rev.update_layout(**PLOT, showlegend=False, height=380,
                              yaxis=dict(categoryorder="total ascending"),
                              coloraxis_showscale=False)
    st.plotly_chart(fig_top_rev, use_container_width=True)

    st.markdown("---")

    # ── TOP 10 BY QUANTITY ────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Top 10 products by quantity sold</p>', unsafe_allow_html=True)
    
    top10_qty = (
        dff.groupby("produit")["quantite"].sum()
        .sort_values(ascending=False).head(10).reset_index()
    )
    top10_qty["label"] = top10_qty["produit"].str[:35]
    
    fig_top_qty = px.bar(
        top10_qty, x="quantite", y="label", orientation="h",
        color="quantite", color_continuous_scale=["#1e3a8a", C["success"]],
        text=top10_qty["quantite"].apply(lambda x: f"{x:,.0f} units"),
        labels={"quantite": "Units sold", "label": ""}
    )
    fig_top_qty.update_traces(textposition="outside")
    fig_top_qty.update_layout(**PLOT, showlegend=False, height=380,
                              yaxis=dict(categoryorder="total ascending"),
                              coloraxis_showscale=False)
    st.plotly_chart(fig_top_qty, use_container_width=True)

    st.markdown("---")
    # ── Return rate by category ───────────────────────────────────────────────
    st.markdown('<p class="section-label">Return rate by product category</p>', unsafe_allow_html=True)
    total_by_cat  = df.groupby("categorie_produit").size().reset_index(name="total")
    return_by_cat = df_ret.groupby("categorie_produit").size().reset_index(name="returns")
    cat_ret = total_by_cat.merge(return_by_cat, on="categorie_produit", how="left").fillna(0)
    cat_ret["return_rate"] = (cat_ret["returns"] / cat_ret["total"] * 100).round(2)
    cat_ret = cat_ret.sort_values("return_rate", ascending=False)

    fig_catret = px.bar(
        cat_ret, x="categorie_produit", y="return_rate",
        color="return_rate",
        color_continuous_scale=["#1e3a2e", C["accent"], C["danger"]],
        text=cat_ret["return_rate"].apply(lambda x: f"{x:.1f}%"),
        labels={"return_rate": "Return rate (%)", "categorie_produit": ""},
    )
    fig_catret.update_traces(textposition="outside")
    fig_catret.update_layout(**PLOT, height=300, coloraxis_showscale=False,
                             xaxis=dict(showgrid=False), yaxis=dict(gridcolor=C["border"]))
    st.plotly_chart(fig_catret, use_container_width=True)
    # ── CATEGORY TREEMAP ──────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Revenue breakdown — category → subcategory</p>',
                unsafe_allow_html=True)

    if "sous_categorie" in dff.columns:
        tree_df = (
            dff.groupby(["categorie_produit", "sous_categorie"])
            .agg(revenue=("montant_da", "sum"), qty=("quantite", "sum"))
            .reset_index()
        )
        tree_df = tree_df[tree_df["revenue"] > 0]
        fig_tree = px.treemap(
            tree_df,
            path=["categorie_produit", "sous_categorie"],
            values="revenue",
            color="revenue",
            color_continuous_scale=SEQ,
            hover_data={"qty": True},
        )
        fig_tree.update_traces(textinfo="label+value+percent parent", textfont_size=12)
        fig_tree.update_layout(**PLOT, height=440)
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        tree_df = dff.groupby("categorie_produit")["montant_da"].sum().reset_index()
        fig_tree = px.treemap(tree_df, path=["categorie_produit"], values="montant_da",
                              color="montant_da", color_continuous_scale=SEQ)
        fig_tree.update_layout(**PLOT, height=380)
        st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("---")

    # ── MARGIN ANALYSIS ───────────────────────────────────────────────────────
    if "marge_estimee_pct" in dff.columns:
        st.markdown('<p class="section-label">Margin analysis by category</p>',
                    unsafe_allow_html=True)

        margin_df = (
            dff.groupby("categorie_produit")
            .agg(
                revenue=("montant_da", "sum"),
                avg_margin=("marge_estimee_pct", "mean"),
                orders=("id_commande_anon", "nunique"),
            )
            .reset_index()
        )

        fig_margin = px.scatter(
            margin_df, x="revenue", y="avg_margin", size="orders", color="avg_margin",
            color_continuous_scale=["#e05c5c", C["accent"], C["success"]],
            text="categorie_produit", hover_data={"orders": True, "revenue": ":,.0f"},
            size_max=50,
        )
        fig_margin.update_traces(textposition="top center", textfont_size=11)
        fig_margin.update_layout(**PLOT, height=400,
                                 xaxis=dict(gridcolor=C["border"]),
                                 yaxis=dict(gridcolor=C["border"]))
        fig_margin.add_hline(y=margin_df["avg_margin"].mean(), line_dash="dot", 
                            line_color=C["muted"], opacity=0.5)
        fig_margin.add_vline(x=margin_df["revenue"].mean(), line_dash="dot", 
                            line_color=C["muted"], opacity=0.5)
        st.plotly_chart(fig_margin, use_container_width=True)
        st.caption("Top-right = high revenue + high margin → focus here.")

    st.markdown("---")

    
    # ── So what — Products ────────────────────────────────────────────────────
    top_margin_cat = margin_df.loc[margin_df["avg_margin"].idxmax(), "categorie_produit"] \
        if "marge_estimee_pct" in dff.columns else "—"
    n_rupture = dff[dff["statut_stock"] == "Rupture"]["produit"].nunique() \
        if "statut_stock" in dff.columns else 0
 
    st.markdown(
        f'<div class="so-what">💡 <b>Top product:</b> <b>{best_product[:40]}</b> generated '
        f'<b>{best_product_rev/1e6:.2f}M DA</b>. '
        f'Highest margin category: <b>{top_margin_cat}</b>. '
        + (f'<b>{n_rupture} products</b> are in rupture de stock — '
           f'cross-check with the Alerts tab restock calendar.</div>'
           if n_rupture > 0 else '</div>'),
        unsafe_allow_html=True
    )
 