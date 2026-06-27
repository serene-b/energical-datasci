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
DATA_DIR = os.path.join(os.path.dirname(r"C:\Users\PCPRODZ\Desktop\energical-datasci\Data"), "data")

@st.cache_data
def load_all():
    clean   = pd.read_csv(os.path.join(DATA_DIR, r"C:\Users\PCPRODZ\Desktop\energical-datasci\Data\data_clean.csv"),   parse_dates=["date_commande"])
    returns = pd.read_csv(os.path.join(DATA_DIR, r"C:\Users\PCPRODZ\Desktop\energical-datasci\Data\data_returns.csv"), parse_dates=["date_commande"])
    loyalty = pd.read_csv(os.path.join(DATA_DIR, r"C:\Users\PCPRODZ\Desktop\energical-datasci\Data\customer_loyalty.csv"))
    return clean, returns, loyalty

try:
    df, df_ret, df_loyalty = load_all()
    DATA_OK = True
except FileNotFoundError:
    DATA_OK = False

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — global filters
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚡ Energical")
    st.markdown("**Sales Intelligence Dashboard**")
    st.markdown("---")

    if not DATA_OK:
        st.error("Data files not found.\nPlace `df_clean.csv`, `df_returns.csv`, `customer_loyalty.csv` in the `/data` folder.")
        st.stop()

    st.markdown("### Filters")

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
    st.caption("DataFest 2026 · The Outliers")

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
st.markdown(f"<span style='color:{C['text_dim']};font-size:0.85rem'>"
            f"{len(dff):,} transactions · "
            f"{dff['wilaya'].nunique()} wilayas · "
            f"{dff['id_client'].nunique()} clients · "
            f"{dff['date_commande'].min().strftime('%b %Y')} → "
            f"{dff['date_commande'].max().strftime('%b %Y')}"
            f"</span>", unsafe_allow_html=True)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Overview",
    "🗺️  Wilayas",
    "👥  Clients",
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

    # ── Revenue over time ─────────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<p class="section-label">Revenue over time</p>', unsafe_allow_html=True)

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
                         hole=0.55, color_discrete_sequence=QUAL)
        fig_pie.update_traces(textposition="outside", textinfo="percent+label",
                              textfont_size=10)
        fig_pie.update_layout(**PLOT, showlegend=False, height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ── Top products + YoY ───────────────────────────────────────────────────
    col_c, col_d = st.columns([1, 1])

    with col_c:
        st.markdown('<p class="section-label">Top 10 products by revenue</p>', unsafe_allow_html=True)
        top10 = (
            dff.groupby("produit")["montant_da"].sum()
            .sort_values(ascending=False).head(10).reset_index()
        )
        top10["label"] = top10["produit"].str[:30]
        fig_top = px.bar(top10, x="montant_da", y="label", orientation="h",
                         color="montant_da", color_continuous_scale=SEQ,
                         labels={"montant_da": "Revenue (DA)", "label": ""})
        fig_top.update_layout(**PLOT, showlegend=False, height=340,
                              yaxis=dict(categoryorder="total ascending"),
                              coloraxis_showscale=False)
        st.plotly_chart(fig_top, use_container_width=True)

    with col_d:
        st.markdown('<p class="section-label">Quarterly revenue — year over year</p>', unsafe_allow_html=True)
        qtr = dff.copy()
        qtr["year"]    = qtr["date_commande"].dt.year
        qtr["quarter"] = "Q" + qtr["date_commande"].dt.quarter.astype(str)
        qtr_agg = qtr.groupby(["year", "quarter"])["montant_da"].sum().reset_index()
        fig_qtr = px.bar(qtr_agg, x="quarter", y="montant_da", color="year",
                         barmode="group", color_discrete_sequence=QUAL,
                         labels={"montant_da": "Revenue (DA)", "quarter": "", "year": "Year"},
                         text_auto=".2s")
        fig_qtr.update_layout(**PLOT, height=340,
                              legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)"),
                              xaxis=dict(showgrid=False),
                              yaxis=dict(gridcolor=C["border"]))
        st.plotly_chart(fig_qtr, use_container_width=True)

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

    # ── Return rate ───────────────────────────────────────────────────────────
    # Use full df (not filtered) for totals so rate is accurate
    total_by_wilaya  = df.groupby("wilaya").size().reset_index(name="total")
    return_by_wilaya = df_ret.groupby("wilaya").size().reset_index(name="returns")
    wilaya_ret = total_by_wilaya.merge(return_by_wilaya, on="wilaya", how="left").fillna(0)
    wilaya_ret["return_rate"] = (wilaya_ret["returns"] / wilaya_ret["total"] * 100).round(2)

    # Merge into wilaya_rev
    wilaya_rev = wilaya_rev.merge(wilaya_ret[["wilaya", "return_rate"]], on="wilaya", how="left").fillna(0)

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

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CLIENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:

    # ── KPIs ──────────────────────────────────────────────────────────────────
    at_risk = df_loyalty[df_loyalty["Retention Level"] == "Low"]
    ltv_at_risk = at_risk["total_spent"].sum()
    n_at_risk   = len(at_risk)
    pct_at_risk = n_at_risk / len(df_loyalty) * 100 if len(df_loyalty) > 0 else 0

    ck1, ck2, ck3, ck4 = st.columns(4)
    ck1.metric("Total Clients",      f"{df_loyalty.shape[0]:,}")
    ck2.metric("At-Risk Clients",    f"{n_at_risk:,}",
               delta=f"{pct_at_risk:.1f}% of base", delta_color="inverse")
    ck3.metric("LTV at Risk",        f"{ltv_at_risk/1e6:.2f}M DA",
               delta="requires immediate action", delta_color="inverse")
    ck4.metric("Avg Retention Score",f"{df_loyalty['Retention Score'].mean():.2f}")

    st.markdown("---")

    # ── B2B vs B2C ────────────────────────────────────────────────────────────
    col_e, col_f = st.columns([1, 1])

    with col_e:
        st.markdown('<p class="section-label">B2B vs B2C — revenue split</p>', unsafe_allow_html=True)
        seg = dff.groupby("type_client").agg(
            revenue=("montant_da", "sum"),
            clients=("id_client", "nunique"),
            avg_order=("montant_da", "mean"),
        ).reset_index()
        fig_seg = px.bar(seg, x="type_client", y="revenue",
                         color="type_client", color_discrete_sequence=[C["primary"], C["accent"]],
                         text=seg["revenue"].apply(lambda x: f"{x/1e6:.1f}M DA"),
                         labels={"revenue": "Revenue (DA)", "type_client": ""})
        fig_seg.update_traces(textposition="outside")
        fig_seg.update_layout(**PLOT, showlegend=False, height=280,
                              xaxis=dict(showgrid=False), yaxis=dict(gridcolor=C["border"]))
        st.plotly_chart(fig_seg, use_container_width=True)

    with col_f:
        st.markdown('<p class="section-label">New vs returning — revenue over time</p>', unsafe_allow_html=True)
        cohort = dff.copy()
        cohort["period"] = cohort["date_commande"].dt.to_period("M").dt.to_timestamp()
        cohort_agg = cohort.groupby(["period", "nouveau_ou_fidele"])["montant_da"].sum().reset_index()
        fig_cohort = px.line(cohort_agg, x="period", y="montant_da",
                             color="nouveau_ou_fidele",
                             color_discrete_sequence=[C["primary"], C["accent"]],
                             markers=True,
                             labels={"montant_da": "Revenue (DA)", "period": "",
                                     "nouveau_ou_fidele": "Client type"})
        fig_cohort.update_layout(**PLOT, height=280,
                                 legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)"),
                                 xaxis=dict(showgrid=False), yaxis=dict(gridcolor=C["border"]))
        st.plotly_chart(fig_cohort, use_container_width=True)

    st.markdown("---")

    # ── Retention distribution ─────────────────────────────────────────────────
    col_g, col_h = st.columns([1, 1])

    with col_g:
        st.markdown('<p class="section-label">Retention level breakdown</p>', unsafe_allow_html=True)
        ret_counts = df_loyalty["Retention Level"].value_counts().reset_index()
        ret_counts.columns = ["level", "count"]
        color_map  = {"High": C["success"], "Medium": C["accent"], "Low": C["danger"]}
        fig_ret_pie = px.pie(ret_counts, values="count", names="level",
                             hole=0.55, color="level", color_discrete_map=color_map)
        fig_ret_pie.update_traces(textposition="outside", textinfo="percent+label")
        fig_ret_pie.update_layout(**PLOT, showlegend=False, height=260)
        st.plotly_chart(fig_ret_pie, use_container_width=True)

    with col_h:
        st.markdown('<p class="section-label">Retention score distribution</p>', unsafe_allow_html=True)
        fig_hist = px.histogram(df_loyalty, x="Retention Score", nbins=30,
                                color_discrete_sequence=[C["primary"]])
        fig_hist.update_layout(**PLOT, height=260,
                               xaxis=dict(showgrid=False), yaxis=dict(gridcolor=C["border"]))
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # ── At-risk client table ───────────────────────────────────────────────────
    st.markdown('<p class="section-label">⚠️ At-risk clients — Low retention (sorted by LTV)</p>',
                unsafe_allow_html=True)

    at_risk_display = (
        at_risk
        .sort_values("total_spent", ascending=False)
        [[
            "id_client", "wilaya", "type_client", "favorite_category",
            "total_orders", "total_spent", "days_since_last_order",
            "Retention Score", "Recommended Strategy"
        ]]
        .rename(columns={
            "id_client":            "Client",
            "wilaya":               "Wilaya",
            "type_client":          "Type",
            "favorite_category":    "Top Category",
            "total_orders":         "Orders",
            "total_spent":          "LTV (DA)",
            "days_since_last_order":"Days Inactive",
            "Retention Score":      "Score",
            "Recommended Strategy": "Strategy",
        })
        .reset_index(drop=True)
    )
    at_risk_display["LTV (DA)"]  = at_risk_display["LTV (DA)"].apply(lambda x: f"{x:,.0f}")
    at_risk_display["Score"]     = at_risk_display["Score"].apply(lambda x: f"{x:.2f}")

    st.dataframe(at_risk_display, use_container_width=True, height=320)

    # ── So what — Clients ─────────────────────────────────────────────────────
    top_at_risk_cat = at_risk["favorite_category"].value_counts().idxmax() if len(at_risk) > 0 else "—"
    st.markdown(
        f'<div class="so-what">💡 <b>{n_at_risk} clients</b> are at risk of churning, '
        f'representing <b>{ltv_at_risk/1e6:.2f}M DA</b> in potential lost revenue. '
        f'The most common category among at-risk clients is <b>{top_at_risk_cat}</b>. '
        f'A targeted win-back campaign for these clients should be the first commercial priority.</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.download_button(
        "⬇ Export at-risk clients",
        at_risk_display.to_csv(index=False).encode(),
        "at_risk_clients.csv", "text/csv"
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ALERTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:

    # ── Restock alerts ────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">🔔 Restock alerts</p>', unsafe_allow_html=True)
    st.caption("Products approaching restock deadline based on lead time + seasonal demand peaks.")

    if "delai_reappro_jours" in dff.columns and "produit" in dff.columns:

        # Seasonal peak: find each product's top month by avg quantity
        seasonal = (
            dff.groupby(["produit", dff["date_commande"].dt.month])["quantite"]
            .mean()
            .reset_index()
        )
        seasonal.columns = ["produit", "peak_month", "avg_qty"]
        peak_month_per_product = (
            seasonal.loc[seasonal.groupby("produit")["avg_qty"].idxmax()]
            [["produit", "peak_month"]]
        )

        restock = (
            dff.groupby("produit")
            .agg(
                delai=("delai_reappro_jours", "mean"),
                total_qty=("quantite", "sum"),
                revenue=("montant_da", "sum"),
            )
            .reset_index()
            .merge(peak_month_per_product, on="produit", how="left")
        )

        today        = pd.Timestamp.today()
        current_month= today.month

        # Alert if peak month is within delai_reappro_jours days from now
        restock["days_to_peak"] = restock["peak_month"].apply(
            lambda m: ((int(m) - current_month) % 12) * 30
        )
        restock["needs_restock"] = restock["days_to_peak"] <= restock["delai"]
        alerts = restock[restock["needs_restock"]].sort_values("days_to_peak")

        if alerts.empty:
            st.success("No restock alerts at this time.")
        else:
            for _, row in alerts.head(10).iterrows():
                urgency = "alert-card" if row["days_to_peak"] <= 30 else "alert-card-warn"
                icon    = "🔴" if row["days_to_peak"] <= 30 else "🟡"
                st.markdown(
                    f'<div class="{urgency}">'
                    f'{icon} <b>{row["produit"][:40]}</b> — '
                    f'Peak month: <b>M{int(row["peak_month"])}</b> · '
                    f'Lead time: <b>{int(row["delai"])} days</b> · '
                    f'Order now — <b>{int(row["days_to_peak"])} days</b> to peak'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with st.expander("View full restock table"):
                st.dataframe(
                    alerts[["produit", "delai", "peak_month", "days_to_peak", "total_qty", "revenue"]]
                    .rename(columns={
                        "produit":      "Product",
                        "delai":        "Lead time (days)",
                        "peak_month":   "Peak month",
                        "days_to_peak": "Days to peak",
                        "total_qty":    "Avg qty sold",
                        "revenue":      "Revenue (DA)",
                    }),
                    use_container_width=True
                )
    else:
        st.info("Restock data requires `delai_reappro_jours` column from catalogue merge.")

    st.markdown("---")

    # ── Anomaly detection ─────────────────────────────────────────────────────
    st.markdown('<p class="section-label">🚨 Transaction anomalies</p>', unsafe_allow_html=True)
    st.caption("Transactions with unusually high or low amounts (> 3 std deviations from product mean).")

    anomaly_df = dff.copy()
    product_stats = (
        anomaly_df.groupby("produit")["montant_da"]
        .agg(mean_amt="mean", std_amt="std")
        .reset_index()
    )
    anomaly_df = anomaly_df.merge(product_stats, on="produit", how="left")
    anomaly_df["z_score"] = (
        (anomaly_df["montant_da"] - anomaly_df["mean_amt"]) /
        anomaly_df["std_amt"].replace(0, np.nan)
    ).abs()
    anomalies = anomaly_df[anomaly_df["z_score"] > 3].sort_values("z_score", ascending=False)

    if anomalies.empty:
        st.success("No anomalies detected in the current selection.")
    else:
        st.warning(f"{len(anomalies)} anomalous transactions detected.")
        cols_show = ["id_transaction", "date_commande", "wilaya", "produit",
                     "montant_da", "quantite", "type_client", "z_score"]
        anom_display = anomalies[cols_show].head(50).copy()
        anom_display["z_score"]    = anom_display["z_score"].round(2)
        anom_display["montant_da"] = anom_display["montant_da"].apply(lambda x: f"{x:,.0f} DA")
        st.dataframe(anom_display.reset_index(drop=True), use_container_width=True, height=300)

        st.download_button(
            "⬇ Export anomalies",
            anomalies[cols_show].to_csv(index=False).encode(),
            "anomalies.csv", "text/csv"
        )

    st.markdown("---")

    # ── Global so-what ────────────────────────────────────────────────────────
    n_anom = len(anomalies) if "anomalies" in dir() else 0
    n_rest = len(alerts)    if "alerts"    in dir() else 0
    st.markdown(
        f'<div class="so-what">💡 <b>Action summary:</b> '
        f'<b>{n_rest} products</b> need to be reordered before their seasonal peak. '
        f'<b>{n_anom} transactions</b> show statistical anomalies and should be reviewed by the ops team. '
        f'Combining these signals with the <b>{n_at_risk} at-risk clients</b> from the Clients tab '
        f'gives a complete picture of immediate commercial risks.</div>',
        unsafe_allow_html=True
    )