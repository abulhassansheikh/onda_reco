import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.cache_data.clear()
st.cache_resource.clear()

# ---- Load Data ----
reco = pd.read_csv('reco.csv')
surf_breaks = list(reco['surf_break'].unique())

image1 = Image.open("images/steamerlane.jpg")
image2 = Image.open("images/pleasurepoint.jpg")

# Wind speed and direction
reco['windy_speed'] = np.sqrt(reco['wind_u-surface']**2 + reco['wind_v-surface']**2) * 1.94384
reco['windy_direction'] = (270 - np.degrees(np.arctan2(reco['wind_v-surface'], reco['wind_u-surface']))) % 360

# Change swell height to feet
reco['swell1_height-surface'] = reco['swell1_height-surface'] * 3.28084
reco['swell2_height-surface'] = reco['swell2_height-surface'] * 3.28084

# Tide height in feet
reco['tide'] = reco['sg'] * 3.28084

# Exclude recos during sun down
reco = reco[(reco['time'] > '06:00:00') & (reco['time'] < '20:00:00')]

st_df = reco[reco['surf_break'] == 'Steamer Lane']
st_data = st_df['date'].unique()[1]
st_time = st_df[st_df['date'] == st_data]['time'].unique()[0]
st_record = st_df[(st_df['date'] == st_data) & (st_df['time'] == st_time)].reset_index(drop = True)
st_record = st_record[['swell1_height-surface', 'swell1_direction-surface','swell1_period-surface', 
                       'swell2_height-surface','swell2_direction-surface', 'swell2_period-surface', 
                       'date', 'time', 'surf_break', 'windy_speed',
                       'windy_direction', 'tide']]

st_record = st_record.loc[0].to_dict()
with open('images/steamerlane.txt', 'w') as f:
    f.write(str(st_record))
    
st_df = reco[reco['surf_break'] == 'Pleasure Point']
st_data = st_df['date'].unique()[1]
st_time = st_df[st_df['date'] == st_data]['time'].unique()[0]
st_record = st_df[(st_df['date'] == st_data) & (st_df['time'] == st_time)].reset_index(drop = True)
st_record = st_record[['swell1_height-surface', 'swell1_direction-surface','swell1_period-surface', 
                       'swell2_height-surface','swell2_direction-surface', 'swell2_period-surface', 
                       'date', 'time', 'surf_break', 'windy_speed',
                       'windy_direction', 'tide']]

st_record = st_record.loc[0].to_dict()
with open('images/pleasurepoint.txt', 'w') as f:
    f.write(str(st_record))
    

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
            margin: 8px;
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
selected_location = st.selectbox("Select a Surf Break:", surf_breaks)

# ---- Feedback Section ----
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSedrlvn74c_h_XAuj3LPQ-WV6H53KBly55heRqviqlMUDIWmQ/viewform?usp=sharing"
email_url = 'mailto:QUINCY@GETONDA.AI?subject=Surf%20Feedback'

st.markdown(f"""
    <div class='feedback-section'>
        <p>We'd love to hear your thoughts!</p>
        <a class='feedback-button' href="{email_url}" target="_blank">
            💬 Leave Feedback
        </a>
        <a class='feedback-button' href="{google_form_url}" target="_blank">
            🌊 Submit Surf Report
        </a>
    </div>
""", unsafe_allow_html=True)

# ---- Forecast Data Display ----
st.divider()

# Create two columns
col1, col2 = st.columns(2)

# Display the images side by side
with col1:
    st.image(image1, use_column_width=True)

with col2:
    st.image(image2, use_column_width=True)
    
    
# Filter based on location
data = reco[reco['surf_break'] == selected_location]

# Sort timestamps
date_list = sorted(data['date'].unique())

for d in date_list:
    st.subheader(f"📅 {d}")
    reco_data = data[data['date'] == d].reset_index(drop=True)

    time_list = list(reco_data['time'].unique())

    for time in time_list:
        current = reco_data[reco_data['time'] == time]
        if current.empty:
            continue

        try:
            swell = current.iloc[0]

            st.markdown(f"<div class='time-label'>🕒 {str(time).zfill(4)}</div>", unsafe_allow_html=True)

            st.markdown(f"""
                <div class='swell-line'>
                    🌊 <b>Swell One:</b> 
                    Height: <code>{round(swell['swell1_height-surface'], 2)}ft</code> —
                    Period: <code>{round(swell['swell1_period-surface'])}s</code> —
                    Direction: <code>{round(swell['swell1_direction-surface'])}°</code>
                </div> 
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='swell-line'>
                    🌊 <b>Swell Two:</b> 
                    Height: <code>{round(swell['swell2_height-surface'], 2)}ft</code> —
                    Period: <code>{round(swell['swell2_period-surface'])}s</code> —
                    Direction: <code>{round(swell['swell2_direction-surface'])}°</code>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='swell-line'>
                    🌊 <b>Tide:</b> 
                    Height: <code>{round(swell['tide'], 2)}ft</code> |
                    🌬️ <b>Wind:</b> 
                    Speed: <code>{round(swell['windy_speed'], 2)} knots</code> —
                    Direction: <code>{round(swell['windy_direction'])}°</code>
                </div>
                <br>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.warning(f"⚠️ Missing or invalid data for {d} at {str(time).zfill(4)}.")
