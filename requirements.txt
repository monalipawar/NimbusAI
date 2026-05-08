import streamlit as st
import requests
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="NimbusAI", page_icon="🌤️", layout="centered")

# ── All CSS in one clean block ────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<div style="display:none">
<style>
* { font-family: 'Outfit', sans-serif !important; }

/* Make the entire Streamlit page background a sky gradient */
.stApp { background: linear-gradient(160deg, #1a6eff 0%, #38b6ff 55%, #87ceeb 100%) !important; min-height: 100vh; }
[data-testid="stAppViewContainer"] { background: transparent !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMain"] { background: transparent !important; }
section[data-testid="stSidebar"] { background: rgba(255,255,255,0.1) !important; }

/* Sky variants — applied to a wrapper div to tint cards inside */
.sky-clear   { --sky1: #1a6eff; --sky2: #38b6ff; --sky3: #87ceeb; }
.sky-cloudy  { --sky1: #4b5e7a; --sky2: #7f97b8; --sky3: #b0c4d8; }
.sky-rain    { --sky1: #1e3a5f; --sky2: #2d5986; --sky3: #4a7fa8; }
.sky-snow    { --sky1: #6b8cae; --sky2: #a8c2d8; --sky3: #ddeeff; }
.sky-thunder { --sky1: #1a1a2e; --sky2: #2d2d44; --sky3: #4a3f6b; }
.sky-fog     { --sky1: #6b7a8d; --sky2: #9aabb8; --sky3: #c5d0d8; }

/* Cards & components */
.hero-card  { border-radius: 24px; padding: 32px 28px 24px; color: white; margin-bottom: 16px; background: rgba(0,0,0,0.15); box-shadow: 0 8px 32px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.25); }
.hero-temp  { font-size: 84px; font-weight: 900; line-height: 1; letter-spacing: -4px; text-shadow: 0 4px 20px rgba(0,0,0,0.2); color: white; }
.hero-city  { font-size: 20px; font-weight: 600; color: white; margin-bottom: 2px; }
.hero-cond  { font-size: 15px; font-weight: 300; color: rgba(255,255,255,0.85); }
.hero-feels { font-size: 14px; color: rgba(255,255,255,0.7); margin-top: 4px; }
.hilo-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.35); border-radius: 30px; padding: 5px 14px; font-size: 14px; font-weight: 600; color: white; margin-right: 8px; margin-top: 12px; }
.glass-card { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 16px; padding: 16px 18px; color: white; margin-bottom: 12px; }
.glass-label{ font-size: 11px; font-weight: 700; letter-spacing: 1.2px; color: rgba(255,255,255,0.65); text-transform: uppercase; margin-bottom: 4px; }
.glass-value{ font-size: 24px; font-weight: 700; color: white; }
.glass-sub  { font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 2px; }
.ai-box     { border-radius: 16px; padding: 16px 20px; font-size: 15px; font-weight: 500; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.25); background: rgba(255,255,255,0.15); color: white; }
.wear-box   { border-radius: 16px; padding: 16px 20px; font-size: 14px; line-height: 1.9; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.25); background: rgba(255,255,255,0.12); color: white; }
.warn-box   { border-radius: 16px; padding: 16px 20px; background: rgba(180,20,20,0.35); border: 1px solid rgba(255,120,120,0.5); color: white; margin-bottom: 12px; font-size: 14px; }
.box-title  { font-size: 10px; letter-spacing: 1.4px; color: rgba(255,255,255,0.6); font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }
.forecast-row { display: flex; gap: 8px; margin-bottom: 12px; }
.forecast-day { flex: 1; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 14px; padding: 12px 6px; text-align: center; color: white; }
.day-name { font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.7); margin-bottom: 4px; }
.day-icon { font-size: 24px; margin-bottom: 4px; }
.day-hi   { font-size: 14px; font-weight: 700; color: white; }
.day-lo   { font-size: 12px; color: rgba(255,255,255,0.55); margin-top: 2px; }
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.chip     { background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 4px 12px; font-size: 12px; color: white; }
.footer   { font-size: 11px; color: rgba(255,255,255,0.5); text-align: center; margin-top: 8px; }
.section-label { color: rgba(255,255,255,0.85) !important; font-weight: 700; font-size: 14px; letter-spacing: 0.4px; margin: 10px 0 8px; }

/* Streamlit widget overrides so they blend into the sky */
.stTextInput > div > div > input { background: rgba(255,255,255,0.2) !important; border: 1px solid rgba(255,255,255,0.35) !important; border-radius: 12px !important; color: white !important; font-size: 15px !important; }
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.55) !important; }
.stTextInput label { color: white !important; }
.stButton > button { background: rgba(255,255,255,0.2) !important; border: 1px solid rgba(255,255,255,0.35) !important; border-radius: 12px !important; color: white !important; font-weight: 600 !important; }
.stButton > button:hover { background: rgba(255,255,255,0.32) !important; }
.stRadio label, .stRadio div { color: white !important; }
.stSpinner p { color: white !important; }
</style>
</div>
""", unsafe_allow_html=True)

# ── WMO codes ─────────────────────────────────────────────────────────────────
WMO_CODES = {
    0:"☀️ Clear sky", 1:"🌤️ Mainly clear", 2:"⛅ Partly cloudy", 3:"☁️ Overcast",
    45:"🌫️ Foggy", 48:"🌫️ Icy fog",
    51:"🌦️ Light drizzle", 53:"🌦️ Drizzle", 55:"🌧️ Heavy drizzle",
    61:"🌧️ Light rain", 63:"🌧️ Rain", 65:"🌧️ Heavy rain",
    71:"🌨️ Light snow", 73:"🌨️ Snow", 75:"❄️ Heavy snow",
    80:"🌦️ Rain showers", 81:"🌧️ Showers", 82:"⛈️ Heavy showers",
    95:"⛈️ Thunderstorm", 96:"⛈️ Thunderstorm + hail", 99:"⛈️ Heavy thunderstorm"
}
SEVERE_CODES = {65, 75, 82, 95, 96, 99}
SEVERE_MESSAGES = {
    65:"🚨 Heavy rain warning! Carry an umbrella and avoid flooded areas.",
    75:"🚨 Heavy snow warning! Roads may be slippery — be careful outside.",
    82:"🚨 Violent rain showers! Stay indoors if you can.",
    95:"⚡ Thunderstorm warning! Stay indoors and away from trees.",
    96:"⚡ Thunderstorm with hail! Do not go outside.",
    99:"⚡ Severe thunderstorm with hail! This is dangerous — stay inside."
}

SKY_GRADIENTS = {
    "sky-clear":   "linear-gradient(160deg, #1a6eff 0%, #38b6ff 55%, #87ceeb 100%)",
    "sky-cloudy":  "linear-gradient(160deg, #4b5e7a 0%, #7f97b8 55%, #b0c4d8 100%)",
    "sky-rain":    "linear-gradient(160deg, #1e3a5f 0%, #2d5986 55%, #4a7fa8 100%)",
    "sky-snow":    "linear-gradient(160deg, #6b8cae 0%, #a8c2d8 55%, #ddeeff 100%)",
    "sky-thunder": "linear-gradient(160deg, #1a1a2e 0%, #2d2d44 55%, #4a3f6b 100%)",
    "sky-fog":     "linear-gradient(160deg, #6b7a8d 0%, #9aabb8 55%, #c5d0d8 100%)",
}

def sky_class(code):
    if code in {95,96,99}: return "sky-thunder"
    if code in {61,63,65,51,53,55,80,81,82}: return "sky-rain"
    if code in {71,73,75}: return "sky-snow"
    if code in {45,48}: return "sky-fog"
    if code == 3: return "sky-cloudy"
    return "sky-clear"

def what_to_wear(temp_f, condition, wind_mph):
    cond = condition.lower()
    if temp_f <= 32:
        items = ["🧥 Heavy coat", "🧤 Gloves", "🧣 Scarf", "🥾 Insulated boots", "🎿 Thermal layers underneath"]
    elif temp_f <= 50:
        items = ["🧥 Jacket", "👖 Jeans", "🧤 Gloves recommended", "👟 Closed-toe shoes"]
    elif temp_f <= 65:
        items = ["🧶 Hoodie or light jacket", "👖 Jeans or light pants", "👟 Sneakers work great"]
    elif temp_f <= 77:
        items = ["👕 T-shirt", "👖 Light pants", "👟 Any shoes work great"]
    elif temp_f <= 91:
        items = ["🩳 Shorts", "👕 Light shirt", "🧢 Cap", "🕶️ Sunglasses", "🧴 Sunscreen!"]
    else:
        items = ["🩳 Shorts", "👕 Lightest shirt you own", "🧢 Sun hat — a must!", "🕶️ Sunglasses", "🧴 High SPF sunscreen", "💧 Carry water everywhere"]
    if "rain" in cond or "drizzle" in cond or "shower" in cond:
        items.append("☔ Umbrella")
        items.append("👟 Waterproof shoes")
    if "snow" in cond:
        items.append("❄️ Snow boots")
        items.append("🧦 Thick socks & layers")
    if "thunder" in cond:
        items.append("🏠 Consider staying indoors")
    if wind_mph > 5:
        items.append("🌬️ Windbreaker")
    return items

def ai_comment(temp_f, condition, wind_mph):
    cond = condition.lower()
    if temp_f <= 32:  return "🥶 Extreme cold — frost risk, heavy winter gear needed."
    if temp_f <= 50:  return "🧊 Very cold — winter jacket recommended."
    if temp_f <= 65:  return "🌬️ Cool weather — light jacket or hoodie works well."
    if temp_f <= 79:  return "🌤️ Perfect weather — comfortable and balanced."
    if temp_f <= 91:  return "🔥 Hot weather — stay hydrated and wear light clothes."
    if temp_f > 91:   return "☀️ Extreme heat — avoid long outdoor exposure."
    if "rain" in cond:    return "☔ Rain expected — carry umbrella or raincoat."
    if "thunder" in cond: return "⛈️ Storm alert — stay indoors if possible."
    if wind_mph > 19:     return "🌬️ Windy conditions — secure loose items."
    return "🌡️ Normal weather conditions."


import math

def get_moon_phase(date):
    """Calculate moon phase (0=new, 0.5=full) using a simple formula."""
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
    if phase < 0.0625:   return "🌑", "New Moon"
    elif phase < 0.1875: return "🌒", "Waxing Crescent"
    elif phase < 0.3125: return "🌓", "First Quarter"
    elif phase < 0.4375: return "🌔", "Waxing Gibbous"
    elif phase < 0.5625: return "🌕", "Full Moon"
    elif phase < 0.6875: return "🌖", "Waning Gibbous"
    elif phase < 0.8125: return "🌗", "Last Quarter"
    else:                return "🌘", "Waning Crescent"

def aqi_label(aqi):
    if aqi is None: return "N/A", "rgba(255,255,255,0.4)"
    if aqi <= 50:   return f"{aqi} Good", "#4ade80"
    if aqi <= 100:  return f"{aqi} Moderate", "#facc15"
    if aqi <= 150:  return f"{aqi} Unhealthy for Sensitive", "#fb923c"
    if aqi <= 200:  return f"{aqi} Unhealthy", "#f87171"
    if aqi <= 300:  return f"{aqi} Very Unhealthy", "#c084fc"
    return f"{aqi} Hazardous", "#ef4444"

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "city_input" not in st.session_state:
    st.session_state.city_input = ""

def add_history(name):
    if name not in st.session_state.history:
        st.session_state.history.insert(0, name)
    st.session_state.history = st.session_state.history[:6]

sky = st.session_state.get("last_sky", "sky-clear")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p style="font-size:28px;font-weight:900;color:white;margin:0 0 16px;letter-spacing:-1px;">🌤️ NimbusAI</p>', unsafe_allow_html=True)

# Unit toggle (defaults to °F)
unit = st.radio("", ["°F", "°C"], horizontal=True, label_visibility="collapsed")
temp_unit_api = "fahrenheit" if unit == "°F" else "celsius"

# Search history chips
if st.session_state.history:
    chips = "".join(f'<span class="chip">🕐 {c}</span>' for c in st.session_state.history)
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

col_inp, col_loc = st.columns([3, 1])
with col_inp:
    city_typed = st.text_input("", placeholder="Search a city...",
                                label_visibility="collapsed",
                                value=st.session_state.city_input)
with col_loc:
    if st.button("📍 My Location"):
        try:
            loc_data = requests.get("https://ipinfo.io/json", timeout=5).json()
            detected = loc_data.get("city", "")
            if detected:
                st.session_state.city_input = detected
                st.rerun()
            else:
                st.warning("Couldn't detect city.")
        except Exception:
            st.warning("Location failed. Try typing your city.")


# ── Decide what to fetch ──────────────────────────────────────────────────────
fetch_mode = None
fetch_city = city_typed.strip()
if fetch_city:
    fetch_mode = "city"

# ── Fetch & display ───────────────────────────────────────────────────────────
if fetch_mode:
    with st.spinner("Fetching real weather..."):

        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={fetch_city}&count=1"
        ).json()
        if "results" not in geo or not geo["results"]:
            st.error("❌ City not found! Try a different spelling.")
            st.stop()
        r = geo["results"][0]
        lat, lon = r["latitude"], r["longitude"]
        city_name, country = r["name"], r.get("country", "")

        # Fetch display units
        wx = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
            f"wind_speed_10m,wind_gusts_10m,weather_code,precipitation_probability,uv_index"
            f"&hourly=temperature_2m,precipitation_probability"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset"
            f"&temperature_unit={temp_unit_api}&wind_speed_unit=mph&timezone=auto&forecast_days=6"
        ).json()

        # Fetch air quality (free, no key)
        aq = requests.get(
            f"https://air-quality-api.open-meteo.com/v1/air-quality"
            f"?latitude={lat}&longitude={lon}"
            f"&current=us_aqi,pm2_5,pm10"
        ).json()
        aqi      = aq.get("current", {}).get("us_aqi", None)
        pm25     = aq.get("current", {}).get("pm2_5", None)

        cur      = wx["current"]
        daily    = wx["daily"]
        temp_f   = cur["temperature_2m"]
        wind_mph = cur["wind_speed_10m"]
        code     = cur["weather_code"]
        condition_str = WMO_CODES.get(code, "Unknown")
        sky_bg = sky_class(code)

        st.session_state.last_sky = sky_bg
        add_history(city_name)

        # Dynamically update full page background to match weather
        gradient = SKY_GRADIENTS.get(sky_bg, SKY_GRADIENTS["sky-clear"])
        st.markdown(f"""
        <style>
        .stApp {{ background: {gradient} !important; }}
        </style>
        """, unsafe_allow_html=True)

        now_time = datetime.now().strftime("%I:%M %p")
        now_date = datetime.now().strftime("%a, %b %d")
        hi = round(daily["temperature_2m_max"][0])
        lo = round(daily["temperature_2m_min"][0])

        # Hero card
        st.markdown(f"""
        <div class="hero-card {sky_bg}">
            <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px;"><span style="font-size:32px;font-weight:800;color:white;letter-spacing:-1px;">{now_time}</span><span style="font-size:13px;color:rgba(255,255,255,0.6);">{now_date}</span></div>
            <div class="hero-city">📍 {city_name}, {country}</div>
            <div class="hero-cond">{condition_str}</div>
            <div style="display:flex;align-items:flex-end;gap:16px;margin-top:8px;flex-wrap:wrap;">
                <div class="hero-temp">{round(cur['temperature_2m'])}{unit}</div>
                <div style="padding-bottom:10px;">
                    <div class="hero-feels">Feels like {round(cur['apparent_temperature'])}{unit}</div>
                    <div>
                        <span class="hilo-badge">🔴 {hi}{unit}</span>
                        <span class="hilo-badge">🔵 {lo}{unit}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Severe warning
        if code in SEVERE_CODES:
            msg = SEVERE_MESSAGES.get(code, "Severe weather! Please stay safe.")
            st.markdown(f'<div class="warn-box"><strong>⚠️ SEVERE WEATHER ALERT</strong><br>{msg}</div>',
                        unsafe_allow_html=True)

        # AI comment
        comment = ai_comment(temp_f, condition_str, wind_mph)
        st.markdown(f'<div class="ai-box"><div class="box-title">✨ Weather Summary</div>{comment}</div>',
                    unsafe_allow_html=True)

        # What to wear
        wear_items = what_to_wear(temp_f, condition_str, wind_mph)
        wear_html = "<br>".join(wear_items)
        st.markdown(f'<div class="wear-box"><div class="box-title">👗 What to Wear Today</div>{wear_html}</div>',
                    unsafe_allow_html=True)

        # Stats grid
        col1, col2, col3, col4 = st.columns(4)
        stats = [
            ("💧", "Humidity",  f"{cur['relative_humidity_2m']}%", ""),
            ("💨", "Wind",      f"{round(cur['wind_speed_10m'])} mph", f"Gusts {round(cur.get('wind_gusts_10m', 0))} mph"),
            ("🌧️", "Rain",      f"{cur.get('precipitation_probability', 0)}%", "chance"),
            ("🌞", "UV Index",  str(round(cur.get('uv_index', 0))), "out of 11"),
        ]
        for col, (ico, lbl, val, sub) in zip([col1, col2, col3, col4], stats):
            with col:
                st.markdown(f"""
                <div class="glass-card">
                    <div class="glass-label">{ico} {lbl}</div>
                    <div class="glass-value">{val}</div>
                    <div class="glass-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)

        # 5-day forecast
        st.markdown('<p style="color:white;font-weight:700;font-size:14px;margin:10px 0 8px;letter-spacing:0.5px;">📅 5-DAY FORECAST</p>',
                    unsafe_allow_html=True)
        forecast_html = '<div class="forecast-row">'
        for i in range(5):
            d_name = "Today" if i == 0 else datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a")
            d_icon = WMO_CODES.get(daily["weather_code"][i], "🌡️").split()[0]
            d_hi   = round(daily["temperature_2m_max"][i])
            d_lo   = round(daily["temperature_2m_min"][i])
            forecast_html += f"""
            <div class="forecast-day">
                <div class="day-name">{d_name}</div>
                <div class="day-icon">{d_icon}</div>
                <div class="day-hi">{d_hi}{unit}</div>
                <div class="day-lo">{d_lo}{unit}</div>
            </div>"""
        forecast_html += "</div>"
        st.markdown(forecast_html, unsafe_allow_html=True)

        # ── Sunrise & Sunset ─────────────────────────────────────────────────
        sunrise_raw = daily.get("sunrise", [""])[0]
        sunset_raw  = daily.get("sunset",  [""])[0]
        try:
            sunrise_fmt = datetime.strptime(sunrise_raw, "%Y-%m-%dT%H:%M").strftime("%I:%M %p")
            sunset_fmt  = datetime.strptime(sunset_raw,  "%Y-%m-%dT%H:%M").strftime("%I:%M %p")
        except Exception:
            sunrise_fmt, sunset_fmt = "N/A", "N/A"

        st.markdown(f"""
        <div style="display:flex; gap:12px; margin-bottom:12px;">
            <div class="glass-card" style="flex:1; text-align:center;">
                <div class="glass-label">🌅 Sunrise</div>
                <div class="glass-value">{sunrise_fmt}</div>
            </div>
            <div class="glass-card" style="flex:1; text-align:center;">
                <div class="glass-label">🌇 Sunset</div>
                <div class="glass-value">{sunset_fmt}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Hourly temperature chart ──────────────────────────────────────────
        hourly_times = wx["hourly"]["time"][:24]
        hourly_temps = wx["hourly"]["temperature_2m"][:24]
        hourly_rain  = wx["hourly"]["precipitation_probability"][:24]

        # Build compact hour labels e.g. "6AM", "12PM"
        hour_labels = []
        for t in hourly_times:
            h = datetime.strptime(t, "%Y-%m-%dT%H:%M")
            hour_labels.append(h.strftime("%-I%p").lower())

        # Build SVG chart (white line on semi-transparent bg)
        w, h_svg = 680, 160
        pad_l, pad_r, pad_t, pad_b = 36, 10, 16, 32
        chart_w = w - pad_l - pad_r
        chart_h = h_svg - pad_t - pad_b

        t_min = min(hourly_temps) - 2
        t_max = max(hourly_temps) + 2
        t_range = t_max - t_min or 1

        def tx(i): return pad_l + (i / (len(hourly_temps) - 1)) * chart_w
        def ty(v): return pad_t + chart_h - ((v - t_min) / t_range) * chart_h

        # Polyline points
        points = " ".join(f"{tx(i):.1f},{ty(v):.1f}" for i, v in enumerate(hourly_temps))

        # Area fill path
        area = f"M{tx(0):.1f},{ty(hourly_temps[0]):.1f} " +                " ".join(f"L{tx(i):.1f},{ty(v):.1f}" for i, v in enumerate(hourly_temps)) +                f" L{tx(len(hourly_temps)-1):.1f},{pad_t+chart_h} L{tx(0):.1f},{pad_t+chart_h} Z"

        # X-axis labels every 3 hours
        x_labels = ""
        for i in range(0, 24, 3):
            x = tx(i)
            x_labels += f'<text x="{x:.1f}" y="{pad_t+chart_h+18}" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.6)" font-family="Outfit,sans-serif">{hour_labels[i]}</text>'

        # Y-axis labels
        y_labels = ""
        for v in [t_min+2, (t_min+t_max)/2, t_max-2]:
            y = ty(v)
            y_labels += f'<text x="{pad_l-4}" y="{y:.1f}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{round(v)}</text>'

        # Dot at current hour
        now_hour = datetime.now().hour
        dot = f'<circle cx="{tx(now_hour):.1f}" cy="{ty(hourly_temps[now_hour]):.1f}" r="5" fill="white" stroke="rgba(255,255,255,0.4)" stroke-width="3"/>'
        dot_label = f'<text x="{tx(now_hour):.1f}" y="{ty(hourly_temps[now_hour])-10:.1f}" text-anchor="middle" font-size="11" fill="white" font-weight="bold" font-family="Outfit,sans-serif">{round(hourly_temps[now_hour])}{unit}</text>'

        chart_svg = f"""
        <div class="glass-card" style="padding:16px 12px 8px;">
            <div class="box-title">📊 Today's Hourly Temperature</div>
            <svg viewBox="0 0 {w} {h_svg}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
                <defs>
                    <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="rgba(255,255,255,0.25)"/>
                        <stop offset="100%" stop-color="rgba(255,255,255,0.02)"/>
                    </linearGradient>
                </defs>
                <path d="{area}" fill="url(#areaGrad)"/>
                <polyline points="{points}" fill="none" stroke="white" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
                {x_labels}
                {y_labels}
                {dot}
                {dot_label}
            </svg>
        </div>
        """
        st.markdown(chart_svg, unsafe_allow_html=True)

        # ── Moon phase + Air Quality ─────────────────────────────────────────
        moon_icon, moon_name = get_moon_phase(datetime.now())
        aqi_text, aqi_color = aqi_label(aqi)
        pm_text = f"{pm25:.1f} µg/m³" if pm25 is not None else "N/A"

        st.markdown(f"""
        <div style="display:flex; gap:12px; margin-bottom:12px;">
            <div class="glass-card" style="flex:1; text-align:center;">
                <div class="glass-label">🌙 Moon Phase</div>
                <div style="font-size:36px; margin:4px 0;">{moon_icon}</div>
                <div class="glass-value" style="font-size:16px;">{moon_name}</div>
            </div>
            <div class="glass-card" style="flex:1; text-align:center;">
                <div class="glass-label">💨 Air Quality (AQI)</div>
                <div class="glass-value" style="color:{aqi_color}; font-size:20px; margin:6px 0;">{aqi_text}</div>
                <div class="glass-sub">PM2.5: {pm_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Weather Map ───────────────────────────────────────────────────────
        st.markdown('<div class="box-title" style="color:rgba(255,255,255,0.6);margin-bottom:6px;">🗺️ WEATHER MAP</div>', unsafe_allow_html=True)
        map_zoom = 9
        tile = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        # Embed a lightweight Leaflet map via HTML
        map_html = f"""
        <div style="border-radius:16px; overflow:hidden; border:1px solid rgba(255,255,255,0.25); margin-bottom:12px;">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="map" style="height:260px; width:100%;"></div>
        <script>
            var map = L.map('map', {{zoomControl:true, scrollWheelZoom:false}}).setView([{lat}, {lon}], {map_zoom});
            L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap',
                maxZoom: 18
            }}).addTo(map);
            L.tileLayer('https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid=demo', {{
                opacity: 0.5
            }}).addTo(map);
            var icon = L.divIcon({{html: '<div style="font-size:24px;">📍</div>', iconSize:[30,30], className:''}});
            L.marker([{lat}, {lon}], {{icon:icon}}).addTo(map).bindPopup('<b>{city_name}</b>').openPopup();
        </script>
        </div>
        """
        import streamlit.components.v1 as components
        components.html(map_html, height=270)

        st.markdown('<p class="footer">Open-Meteo API • Air Quality API • OpenStreetMap • No API key needed 😄</p>',
                    unsafe_allow_html=True)
