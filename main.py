import streamlit as st
import pandas as pd

# ---- Load Data ----
reco = pd.read_csv('reco.csv')
surf_breaks = list(reco['surf_break'].unique())

# ---- Page Config ----
st.set_page_config(page_title="Surf Recommendations", layout="centered")

# ---- Custom Styling ----
st.markdown("""
    <style>
        .title {
            font-size: 42px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 0;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            margin-top: 0;
            color: #666;
        }
        .feedback-section {
            margin-top: 40px;
            text-align: center;
        }
        .feedback-button {
            padding: 12px 28px;
            font-size: 16px;
            border-radius: 10px;
            background-color: #00b894;
            color: white;
            border: none;
            text-decoration: none;
        }
        .time-label {
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        }
        .swell-line {
            margin-left: 10px;
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Logo and Title ----
col1, col2, col3 = st.columns([1, 2, 1])
    
with col2:
    st.image("logo.png", width=250)
st.markdown("<div class='title'>Surf Recommendations</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Choose your surf break and explore the wave details 🌊</div>", unsafe_allow_html=True)

# ---- Surf Break Selection ----
#surf_breaks = ['Steamer Lane 🌊', 'Pleasure Point 🏄‍♂️']
selected_location = st.selectbox("Select a Surf Break:", surf_breaks)

# ---- Feedback Section ----
google_form_url = "https://getonda.ai/"
st.markdown(f"""
    <div class='feedback-section'>
        <p>We'd love to hear your thoughts!</p>
        <a class='feedback-button' href="{google_form_url}" target="_blank">
            Leave Feedback
        </a>
    </div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
# ---- Forecast Data Display ----

# Filter based on location
data = reco[reco['surf_break'] == selected_location]


# Sort timestamps
date_list = sorted(data['date'].unique())

for d in date_list:
    st.subheader(f"📅 {d}")
    reco_data = data[data['date'] == d].reset_index(drop=True)
    
    time_list = list(reco_data['time'].unique())

    for time in time_list:
        if reco_data.empty:
            continue

        try:
            swell = reco_data.iloc[0]

            st.markdown(f"<div class='time-label'>🕒 {str(time).zfill(4)}</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='swell-line'>🌊 <b>Swell One:</b> Height: <code>{round(swell['swell1_height-surface'], 2)}</code> —
            Direction: <code>{round(swell['swell1_direction-surface'])}°</code> —
            Period: <code>{round(swell['swell1_period-surface'])}s</code></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='swell-line'>🌊 <b>Swell Two:</b> Height: <code>{round(swell['swell2_height-surface'], 2)}</code> —
            Direction: <code>{round(swell['swell2_direction-surface'])}°</code> —
            Period: <code>{round(swell['swell2_period-surface'])}s</code></div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.warning(f"⚠️ Missing or invalid data for {d} at {str(time).zfill(4)}.")
