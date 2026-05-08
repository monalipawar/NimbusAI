import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import math
import streamlit.components.v1 as components

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="NimbusAI", page_icon="🌤️", layout="centered")

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">

<style>
* { font-family: 'Outfit', sans-serif !important; }

.stApp {
    background: linear-gradient(160deg, #1a6eff 0%, #38b6ff 55%, #87ceeb 100%);
    min-height: 100vh;
}

.hero-card{
    border-radius:24px;
    padding:32px;
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,0.2);
    color:white;
    margin-bottom:16px;
}

.hero-temp{
    font-size:84px;
    font-weight:900;
    line-height:1;
}

.hero-city{
    font-size:22px;
    font-weight:700;
}

.hero-cond{
    opacity:.85;
    margin-top:4px;
}

.glass-card{
    background:rgba(255,255,255,0.12);
    border:1px solid rgba(255,255,255,0.2);
    border-radius:18px;
    padding:18px;
    color:white;
    margin-bottom:12px;
}

.glass-label{
    font-size:11px;
    opacity:.7;
    text-transform:uppercase;
    letter-spacing:1px;
}

.glass-value{
    font-size:24px;
    font-weight:800;
}

.forecast-row{
    display:flex;
    gap:8px;
}

.forecast-day{
    flex:1;
    background:rgba(255,255,255,0.12);
    border:1px solid rgba(255,255,255,0.2);
    border-radius:16px;
    padding:12px;
    text-align:center;
    color:white;
}

.day-icon{
    font-size:24px;
}

.day-hi{
    font-weight:800;
}

.day-lo{
    opacity:.6;
}

.ai-box,.wear-box,.warn-box{
    border-radius:18px;
    padding:18px;
    color:white;
    margin-bottom:12px;
}

.ai-box,.wear-box{
    background:rgba(255,255,255,0.12);
    border:1px solid rgba(255,255,255,0.2);
}

.warn-box{
    background:rgba(255,0,0,0.22);
    border:1px solid rgba(255,100,100,0.4);
}

.box-title{
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1px;
    opacity:.7;
    margin-bottom:8px;
}

.stTextInput input{
    background:rgba(255,255,255,0.15)!important;
    color:white!important;
    border-radius:14px!important;
    border:1px solid rgba(255,255,255,0.2)!important;
}

.stButton button{
    background:rgba(255,255,255,0.15)!important;
    color:white!important;
    border-radius:14px!important;
    border:1px solid rgba(255,255,255,0.2)!important;
}

.footer{
    text-align:center;
    opacity:.5;
    color:white;
    font-size:12px;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

# ── WMO weather codes ────────────────────────────────────────────────────────
WMO_CODES = {
    0:"☀️ Clear sky",
    1:"🌤️ Mainly clear",
    2:"⛅ Partly cloudy",
    3:"☁️ Overcast",
    45:"🌫️ Fog",
    48:"🌫️ Icy fog",
    51:"🌦️ Drizzle",
    61:"🌧️ Rain",
    63:"🌧️ Heavy rain",
    71:"🌨️ Snow",
    75:"❄️ Heavy snow",
    80:"🌦️ Rain showers",
    95:"⛈️ Thunderstorm"
}

SEVERE_CODES = {63,75,95}

# ── Helpers ──────────────────────────────────────────────────────────────────
def ai_comment(temp, condition):
    if temp < 32:
        return "🥶 Freezing weather outside. Stay warm."
    elif temp < 55:
        return "🧥 Cool weather — a jacket is recommended."
    elif temp < 80:
        return "🌤️ Comfortable weather today."
    else:
        return "🔥 Hot weather — stay hydrated."

def what_to_wear(temp):
    if temp < 32:
        return ["🧥 Heavy coat", "🧤 Gloves", "🧣 Scarf"]
    elif temp < 55:
        return ["🧥 Jacket", "👖 Jeans"]
    elif temp < 80:
        return ["👕 T-shirt", "👟 Sneakers"]
    else:
        return ["🩳 Shorts", "🕶️ Sunglasses", "🧴 Sunscreen"]

def get_moon_phase(date):
    year, month, day = date.year, date.month, date.day

    if month < 3:
        year -= 1
        month += 12

    a = year // 100
    b = a // 4
    c = 2 - a + b

    e = int(365.25 * (year + 4716))
    f = int(30.6001 * (month + 1))

    jd = c + day + e + f - 1524.5
    days_since_new = (jd - 2451549.5) % 29.53058867
    phase = days_since_new / 29.53058867

    if phase < 0.0625:
        return "🌑", "New Moon"
    elif phase < 0.1875:
        return "🌒", "Waxing Crescent"
    elif phase < 0.3125:
        return "🌓", "First Quarter"
    elif phase < 0.4375:
        return "🌔", "Waxing Gibbous"
    elif phase < 0.5625:
        return "🌕", "Full Moon"
    elif phase < 0.6875:
        return "🌖", "Waning Gibbous"
    elif phase < 0.8125:
        return "🌗", "Last Quarter"
    else:
        return "🌘", "Waning Crescent"

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    '<p style="font-size:34px;font-weight:900;color:white;">🌤️ NimbusAI</p>',
    unsafe_allow_html=True
)

unit = st.radio("", ["°F", "°C"], horizontal=True)

city = st.text_input(
    "",
    placeholder="Search a city...",
    label_visibility="collapsed"
)

if city:

    with st.spinner("Fetching weather..."):

        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        ).json()

        if "results" not in geo:
            st.error("City not found.")
            st.stop()

        r = geo["results"][0]

        lat = r["latitude"]
        lon = r["longitude"]
        city_name = r["name"]
        country = r.get("country", "")

        temp_unit_api = "fahrenheit" if unit == "°F" else "celsius"

        wx = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset"
            f"&hourly=temperature_2m"
            f"&temperature_unit={temp_unit_api}"
            f"&wind_speed_unit=mph"
            f"&timezone=auto"
            f"&forecast_days=6"
        ).json()

        cur = wx["current"]
        daily = wx["daily"]

        temp = round(cur["temperature_2m"])
        feels = round(cur["apparent_temperature"])
        humidity = cur["relative_humidity_2m"]
        wind = round(cur["wind_speed_10m"])
        code = cur["weather_code"]

        condition = WMO_CODES.get(code, "Unknown")

        # ── FIXED TIMEZONE ────────────────────────────────────────────────────
        timezone_name = wx["timezone"]

        local_time = datetime.now(ZoneInfo(timezone_name))

        now_time = local_time.strftime("%I:%M %p")
        now_date = local_time.strftime("%a, %b %d")

        hi = round(daily["temperature_2m_max"][0])
        lo = round(daily["temperature_2m_min"][0])

        # ── Hero card ────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="hero-card">
            <div style="font-size:32px;font-weight:900;">
                {now_time}
            </div>

            <div style="opacity:.7;margin-bottom:12px;">
                {now_date}
            </div>

            <div class="hero-city">
                📍 {city_name}, {country}
            </div>

            <div class="hero-cond">
                {condition}
            </div>

            <div class="hero-temp">
                {temp}{unit}
            </div>

            <div>
                Feels like {feels}{unit}
            </div>

            <div style="margin-top:10px;">
                🔴 {hi}{unit} &nbsp;&nbsp; 🔵 {lo}{unit}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Severe warning ───────────────────────────────────────────────────
        if code in SEVERE_CODES:
            st.markdown("""
            <div class="warn-box">
                ⚠️ Severe weather alert. Stay safe outside.
            </div>
            """, unsafe_allow_html=True)

        # ── AI comment ───────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="ai-box">
            <div class="box-title">AI Weather Summary</div>
            {ai_comment(temp, condition)}
        </div>
        """, unsafe_allow_html=True)

        # ── Clothing ─────────────────────────────────────────────────────────
        wear = "<br>".join(what_to_wear(temp))

        st.markdown(f"""
        <div class="wear-box">
            <div class="box-title">What To Wear</div>
            {wear}
        </div>
        """, unsafe_allow_html=True)

        # ── Stats ────────────────────────────────────────────────────────────
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="glass-card">
                <div class="glass-label">Humidity</div>
                <div class="glass-value">{humidity}%</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="glass-card">
                <div class="glass-label">Wind</div>
                <div class="glass-value">{wind} mph</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="glass-card">
                <div class="glass-label">Condition</div>
                <div class="glass-value" style="font-size:18px;">
                    {condition}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Forecast ─────────────────────────────────────────────────────────
        st.markdown(
            '<p style="color:white;font-weight:700;">📅 5-Day Forecast</p>',
            unsafe_allow_html=True
        )

        forecast_html = '<div class="forecast-row">'

        for i in range(5):

            day_name = (
                "Today"
                if i == 0
                else datetime.strptime(
                    daily["time"][i],
                    "%Y-%m-%d"
                ).strftime("%a")
            )

            icon = WMO_CODES.get(
                daily["weather_code"][i],
                "🌡️"
            ).split()[0]

            dhi = round(daily["temperature_2m_max"][i])
            dlo = round(daily["temperature_2m_min"][i])

            forecast_html += f"""
            <div class="forecast-day">
                <div>{day_name}</div>
                <div class="day-icon">{icon}</div>
                <div class="day-hi">{dhi}{unit}</div>
                <div class="day-lo">{dlo}{unit}</div>
            </div>
            """

        forecast_html += "</div>"

        st.markdown(forecast_html, unsafe_allow_html=True)

        # ── Sunrise / Sunset ────────────────────────────────────────────────
        sunrise = datetime.strptime(
            daily["sunrise"][0],
            "%Y-%m-%dT%H:%M"
        ).strftime("%I:%M %p")

        sunset = datetime.strptime(
            daily["sunset"][0],
            "%Y-%m-%dT%H:%M"
        ).strftime("%I:%M %p")

        st.markdown(f"""
        <div style="display:flex;gap:12px;">
            <div class="glass-card" style="flex:1;text-align:center;">
                <div class="glass-label">🌅 Sunrise</div>
                <div class="glass-value">{sunrise}</div>
            </div>

            <div class="glass-card" style="flex:1;text-align:center;">
                <div class="glass-label">🌇 Sunset</div>
                <div class="glass-value">{sunset}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Moon Phase ───────────────────────────────────────────────────────
        moon_icon, moon_name = get_moon_phase(local_time)

        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div class="glass-label">Moon Phase</div>
            <div style="font-size:40px;">{moon_icon}</div>
            <div class="glass-value" style="font-size:18px;">
                {moon_name}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Map ──────────────────────────────────────────────────────────────
        map_html = f"""
        <link rel="stylesheet"
              href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

        <div id="map" style="height:260px;border-radius:18px;"></div>

        <script>
            var map = L.map('map').setView([{lat}, {lon}], 9);

            L.tileLayer(
                'https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
                {{
                    attribution: '© OpenStreetMap'
                }}
            ).addTo(map);

            L.marker([{lat}, {lon}]).addTo(map)
                .bindPopup('{city_name}')
                .openPopup();
        </script>
        """

        components.html(map_html, height=270)

        st.markdown(
            '<p class="footer">Powered by Open-Meteo + OpenStreetMap</p>',
            unsafe_allow_html=True
        )
