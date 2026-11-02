
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Restaurant Growth Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. THEME AND COLOR CONFIGURATION
# =========================================================

try:
    theme_base = st.get_option("theme.base")
except Exception:
    theme_base = "light"

is_dark = theme_base == "dark"

if is_dark:
    COLORS = {
        "navy": "#A9C5E5",
        "blue": "#75A9D6",
        "gold": "#E0BB76",
        "green": "#54B99A",
        "red": "#E27C7C",
        "text": "#E8EDF4",
        "muted": "#A8B3C2",
        "border": "#39485B",
        "card": "#202C3A",
        "surface": "#17212E",
        "chart_grid": "#39485B",
        "plot_bg": "#202C3A",
        "paper_bg": "#17212E"
    }
    PLOT_TEMPLATE = "plotly_dark"

else:
    COLORS = {
        "navy": "#172B4D",
        "blue": "#426B8A",
        "gold": "#C49A52",
        "green": "#27836B",
        "red": "#C65D5D",
        "text": "#26364A",
        "muted": "#75859A",
        "border": "#E2E8EF",
        "card": "#FFFFFF",
        "surface": "#F3F5F8",
        "chart_grid": "#E5EAF0",
        "plot_bg": "#FFFFFF",
        "paper_bg": "#FFFFFF"
    }
    PLOT_TEMPLATE = "plotly_white"

PLOT_COLORS = [
    COLORS["navy"],
    COLORS["blue"],
    COLORS["gold"],
    COLORS["green"],
    "#8297AD",
    "#AAB7C4"
]

px.defaults.template = PLOT_TEMPLATE
px.defaults.color_discrete_sequence = PLOT_COLORS

# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Main page */

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

/* Premium hero header */

.st-key-hero_header {
    background: linear-gradient(
        120deg,
        #172B4D 0%,
        #243F60 65%,
        #315674 100%
    );
    border: none !important;
    border-bottom: 5px solid #C49A52 !important;
    border-radius: 17px !important;
    padding: 28px 35px !important;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(23,43,77,0.16);
}

.st-key-hero_header h1 {
    color: #FFFFFF !important;
    font-size: 38px !important;
    font-weight: 750 !important;
    margin-bottom: 5px !important;
}

.st-key-hero_header h2 {
    color: #E0BB76 !important;
    font-size: 25px !important;
    margin-top: 0 !important;
}

.st-key-hero_header p {
    color: #E3EAF2 !important;
    line-height: 1.7;
}

.st-key-hero_header [data-testid="stCaptionContainer"] p {
    color: #E0BB76 !important;
    font-weight: 700;
    letter-spacing: 1.5px;
    font-size: 11px;
}

/* Section headings */

h1, h2, h3 {
    font-weight: 700 !important;
}

h2 {
    font-size: 24px !important;
}

h3 {
    font-size: 18px !important;
}

/* KPI cards */

[data-testid="stMetric"] {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color, #E2E8EF);
    border-radius: 14px;
    padding: 20px 22px;
    min-height: 120px;
    box-shadow: 0 4px 15px rgba(23,43,77,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 7px 20px rgba(23,43,77,0.11);
}

[data-testid="stMetricLabel"] {
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 750 !important;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
    border-right: 1px solid var(--border-color, #E2E8EF);
}

section[data-testid="stSidebar"] h1 {
    font-size: 23px !important;
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    line-height: 1.6;
}

/* Multiselect tags */

[data-baseweb="tag"] {
    border-radius: 6px !important;
}

/* Chart containers */

[data-testid="stPlotlyChart"] {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color, #E2E8EF);
    border-radius: 13px;
    padding: 8px;
}

/* Insight cards */

.insight-card {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color, #E2E8EF);
    border-left: 5px solid #C49A52;
    border-radius: 11px;
    padding: 17px 20px;
    margin-bottom: 13px;
    color: var(--text-color);
    line-height: 1.8;
}

/* Summary cards */

.summary-card {
    background: var(--secondary-background-color);
    border: 1px solid var(--border-color, #E2E8EF);
    border-left: 5px solid #426B8A;
    border-radius: 12px;
    padding: 20px;
    line-height: 1.8;
    margin: 15px 0;
    color: var(--text-color);
}

/* Buttons */

.stDownloadButton button {
    background-color: #243F60 !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 10px 18px !important;
    font-weight: 600 !important;
}

.stDownloadButton button:hover {
    background-color: #172B4D !important;
}

/* Dataframes */

[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color, #E2E8EF);
    border-radius: 12px;
    overflow: hidden;
}

/* Dividers */

hr {
    opacity: 0.3;
    margin-top: 28px;
    margin-bottom: 28px;
}

/* Footer */

.footer-text {
    text-align: center;
    padding: 22px 10px;
    color: var(--text-color);
    opacity: 0.75;
    line-height: 1.9;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. LOAD DATASET
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "Output"
    / "restaurant_growth_final_classification.csv"
)


@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    data.columns = data.columns.str.strip()
    return data


try:
    df = load_data(str(DATA_PATH))

except FileNotFoundError:
    st.error(
        "Final classification dataset not found. "
        "Check Output/restaurant_growth_final_classification.csv."
    )
    st.stop()

if df.empty:
    st.error("The dataset is empty.")
    st.stop()


# =========================================================
# 5. COLUMN DETECTION
# =========================================================

def find_column(candidates):
    for column in candidates:
        if column in df.columns:
            return column
    return None


name_col = find_column([
    "RestaurantName",
    "RestaurantID"
])

id_col = find_column(["RestaurantID"])

revenue_col = find_column(["TotalRevenue"])

profit_col = find_column(["TotalNetProfit"])

margin_col = find_column(["ProfitMargin"])

gpi_col = find_column([
    "GPI_Score",
    "GrowthPotentialIndex",
    "GPI",
    "GrowthPotentialScore"
])

category_col = find_column([
    "StrategicCategory",
    "Strategic_Classification",
    "GrowthCategory"
])

cluster_col = find_column(["KMeans_Cluster"])

growth_col = find_column(["GrowthFactor"])

orders_col = find_column(["MonthlyOrders"])

aov_col = find_column(["AOV"])

cuisine_col = find_column(["CuisineType"])

segment_col = find_column(["Segment"])

region_col = find_column(["Subregion"])

recommendation_col = find_column([
    "StrategicRecommendation",
    "Recommendation"
])


# =========================================================
# 6. HELPER FUNCTIONS
# =========================================================

def numeric_series(data, column):
    if column and column in data.columns:
        return pd.to_numeric(
            data[column],
            errors="coerce"
        )

    return pd.Series(
        np.nan,
        index=data.index,
        dtype=float
    )


def money_format(value):
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"


def number_format(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def make_plot(fig, height=420):

    fig.update_layout(
        template=PLOT_TEMPLATE,
        height=height,
        paper_bgcolor=COLORS["paper_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(
            color=COLORS["text"],
            family="Arial"
        ),
        title_font=dict(
            size=17,
            color=COLORS["text"]
        ),
        margin=dict(
            t=65,
            b=45,
            l=40,
            r=35
        ),
        xaxis=dict(
            showgrid=False,
            zerolinecolor=COLORS["chart_grid"]
        ),
        yaxis=dict(
            gridcolor=COLORS["chart_grid"],
            zerolinecolor=COLORS["chart_grid"]
        ),
        legend_title_text=""
    )

    return fig


def section_heading(title, subtitle):
    st.header(title)
    st.caption(subtitle)


# =========================================================
# 7. PREMIUM HERO HEADER
# =========================================================

with st.container(key="hero_header"):

    st.caption(
        "✦ RESTAURANT INTELLIGENCE  |  BUSINESS ANALYTICS"
    )

    st.title("Restaurant Growth Potential")

    st.subheader("& Strategic Classification")

    st.write(
        "A data-driven decision support dashboard to evaluate "
        "restaurant performance, identify growth opportunities, "
        "understand strategic business segments and support "
        "sustainable expansion decisions."
    )

    st.write("")

    footer_col1, footer_col2, footer_col3 = st.columns(3)

    with footer_col1:
        st.caption("PERFORMANCE ANALYSIS")

    with footer_col2:
        st.caption("MACHINE LEARNING")

    with footer_col3:
        st.caption("STRATEGIC INSIGHTS")


# =========================================================
# 8. SIDEBAR FILTERS
# =========================================================

st.sidebar.title("Restaurant Analytics")

st.sidebar.caption(
    "BUSINESS PERFORMANCE FILTERS"
)

st.sidebar.markdown("---")

st.sidebar.write(
    "Select the business dimensions to explore."
)

filtered_df = df.copy()

filter_columns = [
    ("Subregion", region_col),
    ("Cuisine Type", cuisine_col),
    ("Restaurant Segment", segment_col),
    ("Strategic Category", category_col),
    ("K-Means Cluster", cluster_col)
]

for label, column in filter_columns:

    if column:

        options = sorted(
            filtered_df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected = st.sidebar.multiselect(
            label,
            options,
            default=options,
            key=f"filter_{label}"
        )

        filtered_df = filtered_df[
            filtered_df[column]
            .astype(str)
            .isin(selected)
        ]

st.sidebar.markdown("---")

st.sidebar.metric(
    "Restaurants Selected",
    f"{len(filtered_df):,}"
)

st.sidebar.caption(
    f"Total restaurants in dataset: {len(df):,}"
)

if filtered_df.empty:
    st.warning(
        "No restaurants match the selected filters. "
        "Please change your filter selections."
    )
    st.stop()


# =========================================================
# 9. EXECUTIVE OVERVIEW
# =========================================================

section_heading(
    "Business Performance Overview",
    "A consolidated view of restaurant scale, revenue, profitability and growth readiness."
)

total_restaurants = len(filtered_df)

total_revenue = (
    numeric_series(filtered_df, revenue_col).sum()
    if revenue_col else np.nan
)

total_profit = (
    numeric_series(filtered_df, profit_col).sum()
    if profit_col else np.nan
)

average_gpi = (
    numeric_series(filtered_df, gpi_col).mean()
    if gpi_col else np.nan
)

average_margin = (
    numeric_series(filtered_df, margin_col).mean()
    if margin_col else np.nan
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Restaurants",
    number_format(total_restaurants)
)

k2.metric(
    "Total Revenue",
    money_format(total_revenue)
)

k3.metric(
    "Total Net Profit",
    money_format(total_profit)
)

k4.metric(
    "Average GPI",
    f"{average_gpi:.2f}"
    if pd.notna(average_gpi) else "N/A"
)

if pd.notna(average_margin):
    st.caption(
        f"Average profit margin across selected restaurants: "
        f"{average_margin:.2%}"
    )

st.divider()


# =========================================================
# 10. STRATEGIC CLASSIFICATION
# =========================================================

section_heading(
    "Restaurant Strategic Segments",
    "Understand how restaurants are distributed across strategic business categories."
)

if category_col:

    category_counts = (
        filtered_df[category_col]
        .fillna("Unclassified")
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "Category",
        "Restaurants"
    ]

    category_counts["Percentage"] = (
        category_counts["Restaurants"]
        / category_counts["Restaurants"].sum()
        * 100
    )

    largest = category_counts.iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            category_counts,
            names="Category",
            values="Restaurants",
            hole=0.58,
            title="Distribution of Strategic Categories",
            color_discrete_sequence=PLOT_COLORS
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            marker=dict(
                line=dict(
                    color=COLORS["paper_bg"],
                    width=3
                )
            )
        )

        fig = make_plot(fig, 430)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        bar_df = category_counts.sort_values(
            "Restaurants",
            ascending=True
        )

        fig = px.bar(
            bar_df,
            x="Restaurants",
            y="Category",
            orientation="h",
            text="Restaurants",
            color="Category",
            color_discrete_sequence=PLOT_COLORS,
            title="Restaurant Count by Strategic Category"
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="Number of Restaurants",
            yaxis_title=""
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0
        )

        fig = make_plot(fig, 430)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Strategic Category Summary")

    display_category = category_counts.copy()

    display_category["Percentage"] = (
        display_category["Percentage"]
        .map(lambda x: f"{x:.1f}%")
    )

    st.dataframe(
        display_category,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        f"""
        <div class="summary-card">
            <b>Largest Strategic Segment:</b>
            {largest['Category']}<br>
            <b>Restaurant Count:</b>
            {int(largest['Restaurants']):,}<br>
            <b>Share of Selected Restaurants:</b>
            {largest['Percentage']:.1f}%
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("Strategic category column is unavailable.")

st.divider()


# =========================================================
# 11. FINANCIAL PERFORMANCE ANALYSIS
# =========================================================

section_heading(
    "Financial Performance Analysis",
    "Compare average revenue and net profitability across restaurant segments."
)

if revenue_col and profit_col and category_col:

    financial_df = filtered_df.copy()

    financial_df["_Revenue"] = numeric_series(
        financial_df,
        revenue_col
    )

    financial_df["_Profit"] = numeric_series(
        financial_df,
        profit_col
    )

    grouped = (
        financial_df.groupby(
            category_col,
            dropna=False
        )
        .agg(
            Average_Revenue=("_Revenue", "mean"),
            Average_Profit=("_Profit", "mean")
        )
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            grouped,
            x=category_col,
            y="Average_Revenue",
            color_discrete_sequence=[COLORS["blue"]],
            text_auto=".2s",
            title="Average Revenue by Strategic Segment"
        )

        fig.update_traces(
            marker_line_width=0,
            marker_cornerradius=5
        )

        fig.update_layout(
            xaxis_title="Strategic Category",
            yaxis_title="Average Revenue"
        )

        fig = make_plot(fig, 430)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        profit_colors = [
            COLORS["green"] if value >= 0 else COLORS["red"]
            for value in grouped["Average_Profit"].fillna(0)
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=grouped[category_col],
                y=grouped["Average_Profit"],
                marker_color=profit_colors,
                text=grouped["Average_Profit"].apply(
                    lambda x: f"{x:,.0f}"
                    if pd.notna(x) else ""
                ),
                textposition="outside"
            )
        )

        fig.update_layout(
            title="Average Net Profit by Strategic Segment",
            xaxis_title="Strategic Category",
            yaxis_title="Average Net Profit"
        )

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color=COLORS["muted"]
        )

        fig = make_plot(fig, 430)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.caption(
        "Green indicates positive average profit; "
        "red indicates negative average profit."
    )

else:
    st.info(
        "Revenue, profit or strategic category column is unavailable."
    )

st.divider()


# =========================================================
# 12. GROWTH OPPORTUNITY RANKING
# =========================================================

section_heading(
    "Growth Opportunity Ranking",
    "Identify restaurants with the highest exploratory Growth Potential Index scores."
)

if gpi_col and name_col:

    ranking_df = filtered_df.copy()

    ranking_df["_GPI"] = numeric_series(
        ranking_df,
        gpi_col
    )

    ranking_df = (
        ranking_df.dropna(subset=["_GPI"])
        .nlargest(10, "_GPI")
    )

    if not ranking_df.empty:

        fig = px.bar(
            ranking_df.sort_values("_GPI"),
            x="_GPI",
            y=name_col,
            orientation="h",
            color="_GPI",
            color_continuous_scale=[
                "#DCE5F0",
                "#426B8A",
                "#172B4D"
            ],
            text="_GPI",
            title="Top 10 Restaurants by GPI Score"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Growth Potential Index",
            yaxis_title="Restaurant",
            coloraxis_showscale=False
        )

        fig = make_plot(fig, 470)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No valid GPI values are available.")

else:
    st.info("Restaurant name or GPI column is unavailable.")

st.divider()


# =========================================================
# 13. CLUSTER ANALYSIS
# =========================================================

section_heading(
    "Restaurant Cluster Insights",
    "Explore restaurant groupings identified through unsupervised K-Means clustering."
)

if cluster_col:

    cluster_counts = (
        filtered_df[cluster_col]
        .astype(str)
        .value_counts()
        .sort_index()
        .reset_index()
    )

    cluster_counts.columns = [
        "Cluster",
        "Restaurants"
    ]

    fig = px.bar(
        cluster_counts,
        x="Cluster",
        y="Restaurants",
        text="Restaurants",
        color="Cluster",
        color_discrete_sequence=PLOT_COLORS,
        title="Restaurant Distribution Across K-Means Clusters"
    )

    fig.update_layout(
        xaxis_title="K-Means Cluster",
        yaxis_title="Number of Restaurants"
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0
    )

    fig = make_plot(fig, 400)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if {"PCA_1", "PCA_2"}.issubset(filtered_df.columns):

        pca_df = filtered_df.copy()

        pca_df["PCA_1"] = numeric_series(
            pca_df, "PCA_1"
        )

        pca_df["PCA_2"] = numeric_series(
            pca_df, "PCA_2"
        )

        pca_df = pca_df.dropna(
            subset=["PCA_1", "PCA_2"]
        )

        if not pca_df.empty:

            fig = px.scatter(
                pca_df,
                x="PCA_1",
                y="PCA_2",
                color=cluster_col,
                hover_name=name_col if name_col else None,
                title="Restaurant Cluster Visualization Using PCA",
                color_discrete_sequence=PLOT_COLORS
            )

            fig.update_traces(
                marker=dict(size=9, opacity=0.75)
            )

            fig = make_plot(fig, 500)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.caption(
            "PCA coordinates were not exported. "
            "Cluster distribution is displayed instead."
        )

else:
    st.info("K-Means cluster column is unavailable.")

st.divider()


# =========================================================
# 14. GROWTH READINESS ASSESSMENT
# =========================================================

section_heading(
    "Growth Readiness Assessment",
    "Review restaurant scores across the exploratory GPI readiness bands."
)

if gpi_col:

    gpi_values = numeric_series(
        filtered_df,
        gpi_col
    ).dropna()

    if not gpi_values.empty:

        high_count = (gpi_values >= 70).sum()

        moderate_count = (
            (gpi_values >= 40)
            & (gpi_values < 70)
        ).sum()

        low_count = (gpi_values < 40).sum()

        total_scores = len(gpi_values)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "High GPI (70–100)",
            f"{high_count:,}",
            f"{high_count / total_scores:.1%} of scored restaurants"
        )

        c2.metric(
            "Moderate GPI (40–69)",
            f"{moderate_count:,}",
            f"{moderate_count / total_scores:.1%} of scored restaurants"
        )

        c3.metric(
            "Low GPI (Below 40)",
            f"{low_count:,}",
            f"{low_count / total_scores:.1%} of scored restaurants"
        )

        average_score = gpi_values.mean()

        st.markdown(
            f"""
            <div class="summary-card">
                <b>Average Growth Potential Index:</b>
                {average_score:.2f}<br><br>
                The Growth Potential Index provides an exploratory
                indication of restaurant growth readiness using
                selected business indicators. It supports comparison
                and strategic analysis, but does not guarantee
                future growth or expansion success.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.info("No valid GPI values are available.")

else:
    st.info("GPI column is unavailable.")

st.divider()


# =========================================================
# 15. RESTAURANT PROFILE EXPLORER
# =========================================================

section_heading(
    "Restaurant Profile Explorer",
    "Examine individual restaurant performance, business attributes and recommendations."
)

if name_col:

    explorer_df = filtered_df.copy()

    explorer_df["_Selection"] = (
        explorer_df[name_col].astype(str)
    )

    if id_col and id_col != name_col:

        explorer_df["_Selection"] += (
            " | ID: " + explorer_df[id_col].astype(str)
        )

    explorer_df = explorer_df.reset_index(drop=True)

    selected_label = st.selectbox(
        "Choose a restaurant to explore",
        explorer_df["_Selection"].tolist()
    )

    restaurant = explorer_df[
        explorer_df["_Selection"] == selected_label
    ].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    orders_value = (
        pd.to_numeric(
            restaurant[orders_col],
            errors="coerce"
        )
        if orders_col else np.nan
    )

    aov_value = (
        pd.to_numeric(
            restaurant[aov_col],
            errors="coerce"
        )
        if aov_col else np.nan
    )

    margin_value = (
        pd.to_numeric(
            restaurant[margin_col],
            errors="coerce"
        )
        if margin_col else np.nan
    )

    gpi_value = (
        pd.to_numeric(
            restaurant[gpi_col],
            errors="coerce"
        )
        if gpi_col else np.nan
    )

    c1.metric(
        "Monthly Orders",
        number_format(orders_value)
    )

    c2.metric(
        "Average Order Value",
        money_format(aov_value)
    )

    c3.metric(
        "Profit Margin",
        f"{margin_value:.2%}"
        if pd.notna(margin_value) else "N/A"
    )

    c4.metric(
        "GPI Score",
        f"{gpi_value:.2f}"
        if pd.notna(gpi_value) else "N/A"
    )

    st.subheader("Restaurant Details")

    detail_columns = [
        name_col,
        id_col,
        cuisine_col,
        segment_col,
        region_col,
        growth_col,
        gpi_col,
        cluster_col,
        category_col
    ]

    detail_columns = list(dict.fromkeys([
        column for column in detail_columns
        if column and column in explorer_df.columns
    ]))

    details = pd.DataFrame({
        "Attribute": detail_columns,
        "Value": [
            str(restaurant[column])
            for column in detail_columns
        ]
    })

    st.dataframe(
        details,
        use_container_width=True,
        hide_index=True
    )

    if recommendation_col:

        st.subheader("Strategic Recommendation")

        recommendation = restaurant[recommendation_col]

        if pd.notna(recommendation):
            st.info(str(recommendation))
        else:
            st.caption(
                "No strategic recommendation is available."
            )

else:
    st.info("Restaurant name or ID column is unavailable.")

st.divider()


# =========================================================
# 16. STRATEGIC BUSINESS INSIGHTS
# =========================================================

section_heading(
    "Strategic Business Insights",
    "Key observations from restaurant classification, revenue, profitability and growth scores."
)

if category_col:

    category_summary = (
        filtered_df[category_col]
        .fillna("Unclassified")
        .value_counts()
    )

    if not category_summary.empty:

        common_category = category_summary.index[0]

        percentage = (
            category_summary.iloc[0]
            / len(filtered_df)
            * 100
        )

        st.markdown(
            f"""
            <div class="insight-card">
                <b>01 | Strategic Classification</b><br>
                {common_category} is the largest strategic category,
                representing {percentage:.1f}% of the selected restaurants.
            </div>
            """,
            unsafe_allow_html=True
        )

if revenue_col and name_col:

    revenue_values = numeric_series(
        filtered_df,
        revenue_col
    )

    if revenue_values.notna().any():

        best_index = revenue_values.idxmax()

        best_restaurant = filtered_df.loc[
            best_index,
            name_col
        ]

        best_revenue = revenue_values.loc[best_index]

        st.markdown(
            f"""
            <div class="insight-card">
                <b>02 | Revenue Performance</b><br>
                {best_restaurant} has the highest total revenue
                among the selected restaurants, at {money_format(best_revenue)}.
            </div>
            """,
            unsafe_allow_html=True
        )

if profit_col:

    profit_values = numeric_series(
        filtered_df,
        profit_col
    )

    if profit_values.notna().any():

        loss_count = (profit_values < 0).sum()

        st.markdown(
            f"""
            <div class="insight-card">
                <b>03 | Profitability Analysis</b><br>
                {loss_count:,} selected restaurants have negative net profit.
                These restaurants may require further cost and
                revenue analysis.
            </div>
            """,
            unsafe_allow_html=True
        )

if gpi_col:

    gpi_values = numeric_series(
        filtered_df,
        gpi_col
    )

    if gpi_values.notna().any():

        st.markdown(
            f"""
            <div class="insight-card">
                <b>04 | Growth Readiness</b><br>
                The average GPI of selected restaurants is
                {gpi_values.mean():.2f}. Use this indicator together
                with profitability and operational performance
                before making expansion decisions.
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()


# =========================================================
# 17. DATA TABLE AND DOWNLOAD
# =========================================================

section_heading(
    "Restaurant Classification Data",
    "Review and export the restaurant records matching the selected filters."
)

st.caption(
    f"Displaying {len(filtered_df):,} restaurants."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Restaurant Data",
    data=csv_data,
    file_name="restaurant_growth_analysis.csv",
    mime="text/csv"
)


# =========================================================
# 18. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer-text">
        <b>Restaurant Growth Potential Modeling &amp;
        Strategic Classification System</b><br>
        Business Analytics &nbsp; | &nbsp;
        Machine Learning &nbsp; | &nbsp;
        Strategic Decision Support
    </div>
    """,
    unsafe_allow_html=True
)
