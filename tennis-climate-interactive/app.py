import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------
# Page setup
# -------------------------

st.set_page_config(
    page_title="Tennis & Climate",
    page_icon="🎾",
    layout="wide"
)

st.markdown(
    """
    <style>

    /* Overall page */
    .stApp {
        background-color: #F7F8F3;
        color: #1F2926;
    }

    /* Top Streamlit header */
    header[data-testid="stHeader"] {
        background-color: #123C35;
    }

    /* Tennis-themed header */
.tennis-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem 1.5rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 3px solid #C7E84A;
}

.header-text h1 {
    font-size: 3rem;
    margin: 0;
    color: #123C35 !important;
    font-weight: 800;
}

.header-text h2 {
    font-size: 1.5rem;
    margin: 0.25rem 0 0.75rem 0;
    color: #123C35 !important;
    border: none;
}

.header-text p {
    font-size: 1.05rem;
    max-width: 700px;
    margin: 0;
    color: #1F2926;
}

/* Subtle tennis ball */
.tennis-ball {
    width: 70px;
    height: 70px;
    background: #C7E84A;
    border-radius: 50%;
    position: relative;
    flex-shrink: 0;
    margin-right: 3rem;
}

.ball-seam {
    position: absolute;
    width: 32px;
    height: 70px;
    border-right: 3px solid #F7F8F3;
    border-radius: 50%;
    left: 18px;
    top: 0;
    transform: rotate(25deg);
}

    /* Main title */
    h1 {
        color: #123C35 !important;
        font-weight: 800;
    }

    /* Section headings */
    h2, h3 {
        color: #123C35 !important;
    }

    h2 {
        border-bottom: 3px solid #C7E84A;
        padding-bottom: 0.35rem;
    }

    /* Body text */
    p {
        color: #1F2926;
    }

    /* Tournament selectboxes */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #E8F0E5 !important;
        background: #E8F0E5 !important;
        color: #123C35 !important;
        border: 1px solid #123C35 !important;
        border-radius: 6px !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #E8F0E5 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #123C35 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] input {
        color: #123C35 !important;
    }

    div[data-testid="stSelectbox"] svg {
        fill: #123C35 !important;
    }

    /* Dropdown menu */
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }

    div[role="option"] {
        background-color: #FFFFFF !important;
        color: #123C35 !important;
    }

    div[role="option"]:hover {
        background-color: #E8F0E5 !important;
        color: #123C35 !important;
    }

    /* Slider */
    [data-testid="stSlider"] {
        color: #1F2926;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: white;
        border-left: 5px solid #C7E84A;
        padding: 1rem;
        border-radius: 8px;
    }

    [data-testid="stMetricLabel"] {
        color: #1F2926 !important;
    }

    [data-testid="stMetricValue"] {
        color: #123C35 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #1F2926 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Load data
# -------------------------

file_path = "data/tennis_weather_dat.xlsx"

temperature = pd.read_excel(
    file_path,
    sheet_name="Temperature Data"
)

temperature.columns = temperature.columns.str.strip()

# -------------------------
# Title
# -------------------------

st.markdown(
    """
    <div class="tennis-header">
        <div class="header-text">
            <h1>Tennis & Climate</h1>
            <h2>Weather at the Grand Slams, 1970–2025</h2>
            <p>
                Explore how temperature and precipitation conditions have
                changed at tennis's four major tournaments during the Open Era.
            </p>
        </div>

        <div class="tennis-ball">
            <div class="ball-seam"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    **Data source:** [Climate Central](https://www.climatecentral.org/report/tennis),
    *Tennis players and fans are facing more extreme weather at the four Grand Slams*
    (2026). All temperature and precipitation data used in this interactive come
    from Climate Central's downloadable dataset.
    """
)

# =========================================================
# CHART 1 — TEMPERATURE TREND
# =========================================================

st.header("Average Maximum Temperature")

col1, col2 = st.columns(2)

with col1:

    tournament_options_1 = [
        "All Grand Slams"
    ] + sorted(temperature["Tournament"].unique().tolist())

    selected_tournament_1 = st.selectbox(
        "Tournament",
        tournament_options_1,
        key="temperature_tournament"
    )

with col2:

    min_year = int(temperature["Year"].min())
    max_year = int(temperature["Year"].max())

    year_range_1 = st.slider(
        "Year",
        min_year,
        max_year,
        (min_year, max_year),
        key="temperature_year"
    )

# Filter data for Chart 1

if selected_tournament_1 != "All Grand Slams":

    chart_data_1 = temperature[
        temperature["Tournament"] == selected_tournament_1
    ].copy()

else:

    chart_data_1 = temperature.copy()

chart_data_1 = chart_data_1[
    chart_data_1["Year"].between(
        year_range_1[0],
        year_range_1[1]
    )
]

# Create Chart 1

fig1 = px.line(
    chart_data_1,
    x="Year",
    y="Actual Tmax (F)",
    color="Tournament",
    markers=True,
    title="Average Maximum Temperature at the Grand Slams",
    labels={
        "Year": "Year",
        "Actual Tmax (F)": "Average Maximum Temperature (°F)",
        "Tournament": "Tournament"
    }
)

fig1.update_layout(
    template="plotly_white",
    paper_bgcolor="#F7F8F3",
    plot_bgcolor="#E8F0E5",
    font=dict(
        color="#1F2926"
    ),
    title=dict(
        font=dict(
            color="#123C35",
            size=20
        )
    ),
    xaxis=dict(
        title=dict(
            font=dict(color="#1F2926")
        ),
        tickfont=dict(color="#1F2926"),
        gridcolor="white"
    ),
    yaxis=dict(
        title=dict(
            font=dict(color="#1F2926")
        ),
        tickfont=dict(color="#1F2926"),
        gridcolor="white"
    ),
    legend=dict(
    title=dict(
        text="Tournament",
        font=dict(
            color="#123C35",
            size=14
        )
    ),
    font=dict(
        color="#123C35",
        size=12
    ),
    bgcolor="rgba(255,255,255,0.75)"
),
    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# =========================================================
# CHART 2 — CLIMATE CHANGE COMPARISON
# =========================================================

st.header("How Much Warmer Are Grand Slam Conditions?")

st.write(
    """
    **What is the counterfactual temperature?** The counterfactual represents
    the temperature that would have occurred in a world without human-caused
    climate change. Climate Central estimates these temperatures using its
    Climate Shift Index (CSI) system, comparing observed daily maximum
    temperatures with modeled counterfactual temperatures for the same
    dates and locations. The difference between the two represents the
    warming attributable to climate change.
    """
)

col3, col4 = st.columns(2)

with col3:

    tournament_options_2 = [
        "All Grand Slams"
    ] + sorted(temperature["Tournament"].unique().tolist())

    selected_tournament_2 = st.selectbox(
        "Tournament",
        tournament_options_2,
        key="counterfactual_tournament"
    )

with col4:

    year_range_2 = st.slider(
        "Year",
        min_year,
        max_year,
        (min_year, max_year),
        key="counterfactual_year"
    )

# Filter data for Chart 2

if selected_tournament_2 != "All Grand Slams":

    chart_data_2 = temperature[
        temperature["Tournament"] == selected_tournament_2
    ].copy()

else:

    chart_data_2 = temperature.copy()

chart_data_2 = chart_data_2[
    chart_data_2["Year"].between(
        year_range_2[0],
        year_range_2[1]
    )
]

# Create Chart 2

fig2 = px.line(
    chart_data_2,
    x="Year",
    y=[
        "Actual Tmax (F)",
        "Counterfactual Tmax (F)"
    ],
    markers=True,
    title="Actual Temperature vs. Counterfactual Temperature",
    labels={
        "Year": "Year",
        "value": "Average Maximum Temperature (°F)",
        "variable": "Temperature"
    },
    color_discrete_map={
        "Actual Tmax (F)": "#D1495B",
        "Counterfactual Tmax (F)": "#247BA0"
    }
)

fig2.update_layout(
    template="plotly_white",
    paper_bgcolor="#F7F8F3",
    plot_bgcolor="#E8F0E5",
    font=dict(
        color="#1F2926"
    ),
    title=dict(
        font=dict(
            color="#123C35",
            size=20
        )
    ),
    xaxis=dict(
        title=dict(
            font=dict(color="#1F2926")
        ),
        tickfont=dict(color="#1F2926"),
        gridcolor="white"
    ),
    yaxis=dict(
        title=dict(
            font=dict(color="#1F2926")
        ),
        tickfont=dict(color="#1F2926"),
        gridcolor="white"
    ),
  legend=dict(
    title=dict(
        text="Temperature",
        font=dict(
            color="#123C35",
            size=14
        )
    ),
    font=dict(
        color="#123C35",
        size=12
    ),
    bgcolor="rgba(255,255,255,0.75)"
),
    hovermode="x unified"
)

# -------------------------
# Climate change metrics
# -------------------------

average_warming = chart_data_2["Climate Change Warming (F)"].mean()
average_hot_days_added = chart_data_2["Hot Days added"].mean()

metric1, metric2 = st.columns(2)

with metric1:
    st.metric(
        "Climate-change warming",
        f"+{average_warming:.1f}°F"
    )

with metric2:
    st.metric(
        "Hot days added",
        f"+{average_hot_days_added:.1f}"
    )

st.plotly_chart(
    fig2,
    use_container_width=True
)