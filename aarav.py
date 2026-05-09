import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import math

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="NimbusAI", page_icon="🌤️", layout="centered")

# ── All CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<div style="display:none">
<style>
* { font-family: 'Outfit', sans-serif !important; }

.stApp { background: linear-gradient(160deg, #1a6eff 0%, #38b6ff 55%, #87ceeb 100%) !important; min-height: 100vh; }
[data-testid="stAppViewContainer"] { background: transparent !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMain"] { background: transparent !important; }
section[data-testid="stSidebar"] { background: rgba(255,255,255,0.1) !important; }

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
.dual-temp { font-size: 13px; color: rgba(255,255,255,0.6); font-weight: 400; margin-left: 6px; }
.chat-container { border-radius: 16px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); padding: 16px; margin-bottom: 12px; }
.chat-msg-user { background: rgba(255,255,255,0.25); border-radius: 12px 12px 4px 12px; padding: 10px 14px; margin: 8px 0; font-size: 14px; color: white; text-align: right; }
.chat-msg-bot  { background: rgba(0,0,0,0.2); border-radius: 12px 12px 12px 4px; padding: 10px 14px; margin: 8px 0; font-size: 14px; color: white; }
.chat-name-user { font-size: 10px; color: rgba(255,255,255,0.5); text-align: right; margin-bottom: 2px; letter-spacing: 1px; }
.chat-name-bot  { font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 2px; letter-spacing: 1px; }

@keyframes float-cloud { 0%{transform:translateX(-120px)} 100%{transform:translateX(110vw)} }
@keyframes fall-rain   { 0%{transform:translateY(-20px);opacity:0.7} 100%{transform:translateY(110vh);opacity:0} }
@keyframes fall-snow   { 0%{transform:translateY(-20px) rotate(0deg);opacity:0.8} 100%{transform:translateY(110vh) rotate(360deg);opacity:0} }
@keyframes flash       { 0%,90%,100%{opacity:0} 92%,98%{opacity:1} }
.weather-particles { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; overflow:hidden; }
.cloud-particle { position:absolute; animation: float-cloud linear infinite; opacity:0.18; }
.rain-particle  { position:absolute; width:2px; border-radius:2px; background:rgba(200,230,255,0.6); animation: fall-rain linear infinite; }
.snow-particle  { position:absolute; font-size:14px; animation: fall-snow linear infinite; color:white; }
.lightning      { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(255,255,200,0.15); pointer-events:none; z-index:1; animation: flash 4s infinite; }

.stTextInput > div > div > input { background: rgba(255,255,255,0.2) !important; border: 1px solid rgba(255,255,255,0.35) !important; border-radius: 12px !important; color: white !important; font-size: 15px !important; }
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.55) !important; }
.stTextInput label { color: white !important; }
.stButton > button { background: rgba(255,255,255,0.2) !important; border: 1px solid rgba(255,255,255,0.35) !important; border-radius: 12px !important; color: white !important; font-weight: 600 !important; }
.stButton > button:hover { background: rgba(255,255,255,0.32) !important; }
.stRadio label, .stRadio div { color: white !important; }
.stSpinner p { color: white !important; }
.stToggle label { color: white !important; }
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

# ── Helpers ───────────────────────────────────────────────────────────────────
def to_c(f): return round((f - 32) * 5 / 9)
def to_f(c): return round(c * 9 / 5 + 32)
def dual(temp_f_val): return f"{round(temp_f_val)}°F / {to_c(temp_f_val)}°C"

def feel_good_index(temp_f, humidity, wind_mph):
    temp_score = max(0, 100 - abs(temp_f - 72) * 2.5)
    hum_score  = max(0, 100 - abs(humidity - 45) * 1.2)
    wind_score = max(0, 100 - max(0, wind_mph - 10) * 3)
    score = round(temp_score * 0.5 + hum_score * 0.3 + wind_score * 0.2)
    if score >= 80:   label, color = "Excellent 😄", "#4ade80"
    elif score >= 60: label, color = "Good 🙂",      "#a3e635"
    elif score >= 40: label, color = "Fair 😐",       "#facc15"
    elif score >= 20: label, color = "Poor 😟",       "#fb923c"
    else:             label, color = "Bad 😣",        "#f87171"
    return score, label, color

def pollen_label(val, kind):
    if val is None: return "N/A"
    if kind == "grass":
        if val < 10:   return f"{val:.0f} — Low"
        if val < 50:   return f"{val:.0f} — Moderate"
        if val < 200:  return f"{val:.0f} — High"
        return f"{val:.0f} — Very High"
    if kind == "tree":
        if val < 15:   return f"{val:.0f} — Low"
        if val < 90:   return f"{val:.0f} — Moderate"
        if val < 1500: return f"{val:.0f} — High"
        return f"{val:.0f} — Very High"
    return f"{val:.0f}"

def what_to_wear(temp_f, condition, wind_mph):
    cond = condition.lower()
    if temp_f <= 32:
        items = [f"🧥 Heavy coat — it's {dual(temp_f)}, freezing!", "🧤 Gloves", "🧣 Scarf", "🥾 Insulated boots", "🎿 Thermal layers"]
    elif temp_f <= 50:
        items = [f"🧥 Jacket — it's {dual(temp_f)}, very cold!", "👖 Jeans", "🧤 Gloves recommended", "👟 Closed-toe shoes"]
    elif temp_f <= 65:
        items = [f"🧶 Hoodie or light jacket — it's {dual(temp_f)}, cool.", "👖 Jeans or light pants", "👟 Sneakers"]
    elif temp_f <= 77:
        items = [f"👕 T-shirt — it's {dual(temp_f)}, comfortable!", "👖 Light pants", "👟 Any shoes"]
    elif temp_f <= 91:
        items = [f"🩳 Shorts — it's {dual(temp_f)}, warm!", "👕 Light shirt", "🧢 Cap", "🕶️ Sunglasses", "🧴 Sunscreen!"]
    else:
        items = [f"🩳 Shorts — it's {dual(temp_f)}, extremely hot!", "👕 Lightest shirt", "🧢 Sun hat!", "🕶️ Sunglasses", "🧴 High SPF sunscreen", "💧 Carry water"]
    if "rain" in cond or "drizzle" in cond or "shower" in cond:
        items += ["☔ Umbrella", "👟 Waterproof shoes"]
    if "snow" in cond:
        items += ["❄️ Snow boots", "🧦 Thick socks & layers"]
    if "thunder" in cond:
        items.append("🏠 Consider staying indoors")
    if wind_mph > 5:
        items.append("🌬️ Windbreaker")
    return items

def ai_comment(temp_f, condition, wind_mph):
    cond = condition.lower()
    if temp_f <= 32:  return f"🥶 Extreme cold ({dual(temp_f)}) — frost risk, heavy winter gear needed."
    if temp_f <= 50:  return f"🧊 Very cold ({dual(temp_f)}) — winter jacket recommended."
    if temp_f <= 65:  return f"🌬️ Cool weather ({dual(temp_f)}) — light jacket or hoodie works well."
    if temp_f <= 79:  return f"🌤️ Perfect weather ({dual(temp_f)}) — comfortable and balanced."
    if temp_f <= 91:  return f"🔥 Hot weather ({dual(temp_f)}) — stay hydrated and wear light clothes."
    if temp_f > 91:   return f"☀️ Extreme heat ({dual(temp_f)}) — avoid long outdoor exposure."
    if "rain" in cond:    return f"☔ Rain expected ({dual(temp_f)}) — carry umbrella or raincoat."
    if "thunder" in cond: return f"⛈️ Storm alert ({dual(temp_f)}) — stay indoors if possible."
    if wind_mph > 19:     return f"🌬️ Windy conditions ({dual(temp_f)}) — secure loose items."
    return f"🌡️ Normal weather conditions ({dual(temp_f)})."

def aqi_label(aqi):
    if aqi is None: return "N/A", "rgba(255,255,255,0.4)"
    if aqi <= 50:   return f"{aqi} Good", "#4ade80"
    if aqi <= 100:  return f"{aqi} Moderate", "#facc15"
    if aqi <= 150:  return f"{aqi} Unhealthy for Sensitive", "#fb923c"
    if aqi <= 200:  return f"{aqi} Unhealthy", "#f87171"
    if aqi <= 300:  return f"{aqi} Very Unhealthy", "#c084fc"
    return f"{aqi} Hazardous", "#ef4444"

def get_moon_phase(date):
    year, month, day = date.year, date.month, date.day
    if month < 3: year -= 1; month += 12
    a = year // 100; b = a // 4; c = 2 - a + b
    e = int(365.25 * (year + 4716)); f = int(30.6001 * (month + 1))
    jd = c + day + e + f - 1524.5
    phase = ((jd - 2451549.5) % 29.53058867) / 29.53058867
    if phase < 0.0625:   return "🌑", "New Moon"
    elif phase < 0.1875: return "🌒", "Waxing Crescent"
    elif phase < 0.3125: return "🌓", "First Quarter"
    elif phase < 0.4375: return "🌔", "Waxing Gibbous"
    elif phase < 0.5625: return "🌕", "Full Moon"
    elif phase < 0.6875: return "🌖", "Waning Gibbous"
    elif phase < 0.8125: return "🌗", "Last Quarter"
    else:                return "🌘", "Waning Crescent"

# ── Rule-based chat bot ───────────────────────────────────────────────────────
def weather_chat(question, ctx):
    q         = question.lower()
    temp_f    = ctx["temp_f"]
    cond      = ctx["condition"].lower()
    wind_mph  = ctx["wind_mph"]
    rain_pct  = ctx["rain_pct"]
    hi_f      = ctx["hi_f"]
    lo_f      = ctx["lo_f"]
    city      = ctx["city"]
    uv        = ctx["uv"]
    t_cond    = ctx.get("tomorrow_cond", "").lower()
    t_hi      = ctx.get("tomorrow_hi_f", hi_f)
    t_rain    = ctx.get("tomorrow_rain_pct", rain_pct)
    t_code    = ctx.get("tomorrow_code", 0)

    if any(w in q for w in ["hik", "trail", "nature walk"]):
        bad  = "thunder" in t_cond or "snow" in t_cond or t_rain > 60
        good = t_rain < 25 and "thunder" not in t_cond
        if good:   return f"✅ Tomorrow looks great for hiking in {city}! {WMO_CODES.get(t_code,'Nice weather')} with a high of {dual(t_hi)}. Bring water and sunscreen!"
        elif bad:  return f"❌ I'd skip the hike tomorrow — {t_cond} and {t_rain}% rain chance. Pick another day!"
        else:      return f"⚠️ Risky for hiking tomorrow — {t_rain}% rain chance. Bring a rain jacket just in case."

    if any(w in q for w in ["umbrella", "rain", "rainy", "raining", "wet"]):
        if rain_pct > 60 or any(x in cond for x in ["rain","drizzle","shower"]):
            return f"☔ Yes, definitely bring an umbrella — {rain_pct}% rain chance in {city} today."
        elif rain_pct > 30:
            return f"🌂 Maybe pack a light umbrella — {rain_pct}% chance of rain."
        else:
            return f"🌤️ Probably not needed — only {rain_pct}% rain chance today."

    if any(w in q for w in ["jacket", "coat", "layer", "warm enough"]):
        if temp_f <= 50:   return f"🧥 Absolutely — it's {dual(temp_f)} in {city}, you'll need a proper coat."
        elif temp_f <= 65: return f"🧶 A light jacket would be smart — it's {dual(temp_f)}, could feel cool."
        else:              return f"👕 No jacket needed — comfortable {dual(temp_f)} in {city}!"

    if any(w in q for w in ["beach", "swim", "pool"]):
        if temp_f >= 77 and rain_pct < 30:
            return f"🏖️ Perfect beach day in {city}! {dual(temp_f)}, {rain_pct}% rain chance. UV index {uv} — wear sunscreen!"
        elif temp_f < 65:
            return f"🥶 Too cold for the beach — only {dual(temp_f)} in {city}."
        else:
            return f"🌤️ Could work! {dual(temp_f)} but {rain_pct}% rain chance — watch the sky."

    if any(w in q for w in ["run", "jog", "cycle", "bike", "exercise", "workout"]):
        if "thunder" in cond:  return f"⛈️ Skip the outdoor workout today — thunderstorm in {city}!"
        elif temp_f <= 32:     return f"🥶 Very cold at {dual(temp_f)} — layer up well or hit the gym."
        elif temp_f >= 95:     return f"🔥 {dual(temp_f)} is dangerously hot for outdoor exercise. Go early or gym."
        elif rain_pct > 50:    return f"🌧️ {rain_pct}% rain chance — treadmill day unless you don't mind getting wet!"
        else:                  return f"🏃 Great conditions for a run in {city}! {dual(temp_f)}, {wind_mph:.0f} mph winds."

    if any(w in q for w in ["picnic", "bbq", "barbecue", "park"]):
        if rain_pct < 20 and temp_f >= 65 and "thunder" not in cond:
            return f"🧺 Perfect picnic weather in {city}! {dual(temp_f)}, {rain_pct}% rain. Enjoy!"
        elif "thunder" in cond or rain_pct > 60:
            return f"⛈️ I'd reschedule — {cond} and {rain_pct}% rain chance."
        else:
            return f"🌤️ Decent for a picnic but keep it short — {rain_pct}% rain chance."

    if any(w in q for w in ["sunscreen", "uv", "sun protection", "sunburn"]):
        if uv >= 8:   return f"🧴 Definitely — UV index is {uv} (very high) in {city}. SPF 50+ recommended."
        elif uv >= 5: return f"🌞 UV index is {uv} — sunscreen is a good idea for extended outdoor time."
        else:         return f"🌤️ UV index only {uv} today — low risk, but SPF never hurts!"

    if any(w in q for w in ["how hot", "how cold", "temperature", "degrees", "temp"]):
        return f"🌡️ Right now in {city}: {dual(temp_f)}, feels like {dual(ctx['feels_f'])}. High {dual(hi_f)}, low {dual(lo_f)}."

    if any(w in q for w in ["wind", "windy", "breezy", "gusty"]):
        gusts = ctx.get("gusts_mph", wind_mph)
        if wind_mph > 25:   return f"💨 Very windy in {city} — {wind_mph:.0f} mph, gusts up to {gusts:.0f} mph. Hold onto your hat!"
        elif wind_mph > 10: return f"🌬️ Some wind today — {wind_mph:.0f} mph. A windbreaker helps."
        else:               return f"😌 Calm winds in {city} — only {wind_mph:.0f} mph."

    if any(w in q for w in ["drive", "driving", "road", "car"]):
        if "snow" in cond or "ice" in cond: return f"🚗 Be careful — {cond} may affect roads in {city}. Slow down!"
        elif "thunder" in cond:             return f"🌧️ Reduced visibility from {cond}. Drive cautiously in {city}."
        else:                               return f"🚗 Roads should be fine in {city} today."

    if any(w in q for w in ["what to do", "activities", "suggestions", "bored", "plans"]):
        if temp_f >= 68 and rain_pct < 30 and "thunder" not in cond:
            return f"🌳 Great day to be outside in {city}! Try a walk, picnic, or bike ride. {dual(temp_f)} and mostly clear."
        elif "rain" in cond or rain_pct > 60:
            return f"🏠 Good day to stay in! Cozy up with a book or movie. {dual(temp_f)} and {cond} outside."
        else:
            return f"🤔 Mixed conditions in {city} ({dual(temp_f)}, {cond}). Light outdoor activities work — have a backup plan!"

    return (f"🤖 Here's what I know: it's {dual(temp_f)} in {city} with {cond}. "
            f"High {dual(hi_f)}, low {dual(lo_f)}, {rain_pct}% rain chance. "
            f"Try asking: hiking, umbrella, jacket, beach, run, picnic, UV, wind, or driving!")

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [("history",[]), ("city_input",""), ("chat_messages",[]),
                      ("weather_ctx",None), ("dark_mode",False)]:
    if key not in st.session_state:
        st.session_state[key] = default

def add_history(name):
    if name not in st.session_state.history:
        st.session_state.history.insert(0, name)
    st.session_state.history = st.session_state.history[:6]

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_dark = st.columns([5, 1])
with col_title:
    st.markdown('<p style="font-size:28px;font-weight:900;color:white;margin:0 0 4px;letter-spacing:-1px;">🌤️ NimbusAI</p>', unsafe_allow_html=True)
with col_dark:
    dark = st.toggle("🌙", value=st.session_state.dark_mode, help="Dark mode")
    st.session_state.dark_mode = dark

if dark:
    st.markdown("<style>.stApp { filter: brightness(0.6) saturate(0.7) !important; }</style>", unsafe_allow_html=True)

unit = st.radio("", ["°F", "°C"], horizontal=True, label_visibility="collapsed")

# ── Geolocation button ────────────────────────────────────────────────────────
import streamlit.components.v1 as components
geo_html = """
<div style="margin-bottom:10px;">
  <button onclick="getLocation()" style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.35);
    border-radius:12px;color:white;font-family:Outfit,sans-serif;font-size:13px;font-weight:600;
    padding:6px 16px;cursor:pointer;">📍 Use My Location</button>
  <span id="geo-status" style="color:rgba(255,255,255,0.6);font-size:12px;margin-left:10px;"></span>
</div>
<script>
function getLocation() {
  document.getElementById('geo-status').innerText = 'Detecting…';
  navigator.geolocation.getCurrentPosition(function(pos) {
    fetch('https://geocoding-api.open-meteo.com/v1/reverse?latitude='+pos.coords.latitude+'&longitude='+pos.coords.longitude+'&count=1')
      .then(r=>r.json()).then(data=>{
        if(data.results && data.results[0]){
          var city = data.results[0].name;
          document.getElementById('geo-status').innerText = '✅ ' + city;
          var input = window.parent.document.querySelectorAll('input[type="text"]')[0];
          if(input){
            var nv = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value');
            nv.set.call(input, city);
            input.dispatchEvent(new Event('input',{bubbles:true}));
          }
        }
      });
  }, function(){ document.getElementById('geo-status').innerText = '❌ Permission denied'; });
}
</script>"""
components.html(geo_html, height=50)

if st.session_state.history:
    chips = "".join(f'<span class="chip">🕐 {c}</span>' for c in st.session_state.history)
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

city_typed = st.text_input("", placeholder="Search a city...", label_visibility="collapsed",
                            value=st.session_state.city_input)
fetch_city = city_typed.strip()

# ── Fetch & display ───────────────────────────────────────────────────────────
if fetch_city:
    with st.spinner("Fetching real weather..."):
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={fetch_city}&count=1").json()
        if "results" not in geo or not geo["results"]:
            st.error("❌ City not found! Try a different spelling.")
            st.stop()
        r = geo["results"][0]
        lat, lon      = r["latitude"], r["longitude"]
        city_name     = r["name"]
        country       = r.get("country", "")

        wx_f = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
            f"wind_speed_10m,wind_gusts_10m,weather_code,precipitation_probability,uv_index"
            f"&hourly=temperature_2m,precipitation_probability"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset,precipitation_probability_max"
            f"&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=6"
        ).json()

        wx_display = wx_f
        if unit == "°C":
            wx_display = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,apparent_temperature"
                f"&hourly=temperature_2m"
                f"&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset"
                f"&temperature_unit=celsius&wind_speed_unit=mph&timezone=auto&forecast_days=6"
            ).json()

        aq = requests.get(
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
            f"&current=us_aqi,pm2_5,grass_pollen,tree_pollen"
        ).json()
        aqi          = aq.get("current",{}).get("us_aqi", None)
        pm25         = aq.get("current",{}).get("pm2_5", None)
        grass_pollen = aq.get("current",{}).get("grass_pollen", None)
        tree_pollen  = aq.get("current",{}).get("tree_pollen", None)

        cur_f        = wx_f["current"]
        cur_display  = wx_display["current"]
        daily_f      = wx_f["daily"]
        daily_disp   = wx_display["daily"]

        temp_f        = cur_f["temperature_2m"]
        feels_f       = cur_f["apparent_temperature"]
        wind_mph      = cur_f["wind_speed_10m"]
        gusts_mph     = cur_f.get("wind_gusts_10m", wind_mph)
        code          = cur_f["weather_code"]
        humidity      = cur_f["relative_humidity_2m"]
        rain_pct      = cur_f.get("precipitation_probability", 0)
        uv            = cur_f.get("uv_index", 0)
        condition_str = WMO_CODES.get(code, "Unknown")

        temp_display  = cur_display["temperature_2m"]
        feels_display = cur_display["apparent_temperature"]
        hi_display    = round(daily_disp["temperature_2m_max"][0])
        lo_display    = round(daily_disp["temperature_2m_min"][0])
        hi_f          = daily_f["temperature_2m_max"][0]
        lo_f          = daily_f["temperature_2m_min"][0]

        t_code  = daily_f["weather_code"][1]               if len(daily_f["weather_code"]) > 1       else code
        t_hi_f  = daily_f["temperature_2m_max"][1]         if len(daily_f["temperature_2m_max"]) > 1 else hi_f
        t_rain_arr = daily_f.get("precipitation_probability_max", [rain_pct]*6)
        t_rain  = t_rain_arr[1] if len(t_rain_arr) > 1 else rain_pct

        st.session_state.weather_ctx = {
            "temp_f": temp_f, "feels_f": feels_f, "condition": condition_str,
            "wind_mph": wind_mph, "gusts_mph": gusts_mph, "rain_pct": rain_pct,
            "hi_f": hi_f, "lo_f": lo_f, "city": city_name, "uv": round(uv),
            "code": code, "humidity": humidity,
            "tomorrow_cond": WMO_CODES.get(t_code,""),
            "tomorrow_hi_f": t_hi_f, "tomorrow_rain_pct": t_rain, "tomorrow_code": t_code,
        }

        sky_bg   = sky_class(code)
        gradient = SKY_GRADIENTS.get(sky_bg, SKY_GRADIENTS["sky-clear"])
        st.session_state.last_sky = sky_bg
        add_history(city_name)
        st.markdown(f"<style>.stApp {{ background: {gradient} !important; }}</style>", unsafe_allow_html=True)

        # ── Animated particles ────────────────────────────────────────────────
        import random
        particles = '<div class="weather-particles">'
        if sky_bg == "sky-clear":
            for _ in range(4):
                particles += f'<div class="cloud-particle" style="top:{random.randint(3,35)}%;font-size:{random.randint(32,56)}px;animation-duration:{random.randint(18,35)}s;animation-delay:-{random.randint(0,20)}s;">☁️</div>'
        elif sky_bg == "sky-rain":
            for _ in range(40):
                particles += f'<div class="rain-particle" style="left:{random.randint(0,100)}%;height:{random.randint(12,22)}px;animation-duration:{random.uniform(0.6,1.2):.2f}s;animation-delay:-{random.uniform(0,2):.2f}s;"></div>'
        elif sky_bg == "sky-snow":
            for _ in range(30):
                particles += f'<div class="snow-particle" style="left:{random.randint(0,100)}%;animation-duration:{random.uniform(3,7):.2f}s;animation-delay:-{random.uniform(0,5):.2f}s;">❄️</div>'
        elif sky_bg == "sky-thunder":
            particles += '<div class="lightning"></div>'
            for _ in range(25):
                particles += f'<div class="rain-particle" style="left:{random.randint(0,100)}%;height:{random.randint(15,28)}px;animation-duration:{random.uniform(0.5,0.9):.2f}s;animation-delay:-{random.uniform(0,1.5):.2f}s;background:rgba(180,210,255,0.7);"></div>'
        particles += '</div>'
        st.markdown(particles, unsafe_allow_html=True)

        tz_str    = wx_f.get("timezone","UTC")
        local_now = datetime.now(ZoneInfo(tz_str))
        now_time  = local_now.strftime("%I:%M %p")
        now_date  = local_now.strftime("%a, %b %d")

        alt_temp  = f"/ {to_c(temp_f)}°C"  if unit == "°F" else f"/ {to_f(temp_display)}°F"
        alt_feels = f"/ {to_c(feels_f)}°C" if unit == "°F" else f"/ {to_f(feels_display)}°F"

        # ── Hero card ─────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="hero-card {sky_bg}">
            <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px;">
                <span style="font-size:32px;font-weight:800;color:white;letter-spacing:-1px;">{now_time}</span>
                <span style="font-size:13px;color:rgba(255,255,255,0.6);">{now_date}</span>
            </div>
            <div class="hero-city">📍 {city_name}, {country}</div>
            <div class="hero-cond">{condition_str}</div>
            <div style="display:flex;align-items:flex-end;gap:16px;margin-top:8px;flex-wrap:wrap;">
                <div>
                    <div class="hero-temp">{round(temp_display)}{unit}</div>
                    <div class="dual-temp">{alt_temp}</div>
                </div>
                <div style="padding-bottom:10px;">
                    <div class="hero-feels">Feels like {round(feels_display)}{unit} <span style="font-size:12px;color:rgba(255,255,255,0.5);">{alt_feels}</span></div>
                    <div>
                        <span class="hilo-badge">🔴 {hi_display}{unit}</span>
                        <span class="hilo-badge">🔵 {lo_display}{unit}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if code in SEVERE_CODES:
            st.markdown(f'<div class="warn-box"><strong>⚠️ SEVERE WEATHER ALERT</strong><br>{SEVERE_MESSAGES.get(code,"Stay safe!")}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="ai-box"><div class="box-title">✨ Weather Summary</div>{ai_comment(temp_f, condition_str, wind_mph)}</div>', unsafe_allow_html=True)

        # ── Share button ──────────────────────────────────────────────────────
        share_text = (f"📍 {city_name}, {country} — {condition_str}\\n"
                      f"🌡️ {round(temp_display)}{unit} (feels {round(feels_display)}{unit})\\n"
                      f"🔴 High {hi_display}{unit}  🔵 Low {lo_display}{unit}\\n"
                      f"💧 {humidity}% humidity  💨 {round(wind_mph)} mph wind\\n"
                      f"🌧️ {rain_pct}% rain  🌞 UV {round(uv)}\\n"
                      f"Shared via NimbusAI 🌤️")
        st.markdown(f"""
        <button onclick="navigator.clipboard.writeText('{share_text}').then(()=>{{this.innerText='✅ Copied!';setTimeout(()=>this.innerText='📋 Share Weather',2000)}})"
          style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.35);border-radius:12px;
                 color:white;font-family:Outfit,sans-serif;font-size:13px;font-weight:600;
                 padding:8px 20px;cursor:pointer;margin-bottom:14px;">📋 Share Weather</button>
        """, unsafe_allow_html=True)

        # ── What to wear ──────────────────────────────────────────────────────
        wear_html = "<br>".join(what_to_wear(temp_f, condition_str, wind_mph))
        st.markdown(f'<div class="wear-box"><div class="box-title">👗 What to Wear Today</div>{wear_html}</div>', unsafe_allow_html=True)

        # ── Feel-good index ───────────────────────────────────────────────────
        fgi_score, fgi_label, fgi_color = feel_good_index(temp_f, humidity, wind_mph)
        st.markdown(f"""
        <div class="glass-card" style="display:flex;align-items:center;gap:20px;">
            <svg width="80" height="80" viewBox="0 0 80 80">
                <circle cx="40" cy="40" r="34" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="8"/>
                <circle cx="40" cy="40" r="34" fill="none" stroke="{fgi_color}" stroke-width="8"
                    stroke-dasharray="213.6" stroke-dashoffset="{213.6-(fgi_score/100)*213.6:.1f}"
                    stroke-linecap="round" transform="rotate(-90 40 40)"/>
                <text x="40" y="45" text-anchor="middle" font-size="18" font-weight="900" fill="white" font-family="Outfit,sans-serif">{fgi_score}</text>
            </svg>
            <div>
                <div class="box-title">😊 Feel-Good Index</div>
                <div style="font-size:20px;font-weight:700;color:{fgi_color};">{fgi_label}</div>
                <div class="glass-sub">Based on temp, humidity &amp; wind</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Stats grid ────────────────────────────────────────────────────────
        col1, col2, col3, col4 = st.columns(4)
        for col, (ico, lbl, val, sub) in zip([col1,col2,col3,col4], [
            ("💧","Humidity",  f"{humidity}%",""),
            ("💨","Wind",      f"{round(wind_mph)} mph",f"Gusts {round(gusts_mph)} mph"),
            ("🌧️","Rain",      f"{rain_pct}%","chance"),
            ("🌞","UV Index",  str(round(uv)),"out of 11"),
        ]):
            with col:
                st.markdown(f'<div class="glass-card"><div class="glass-label">{ico} {lbl}</div><div class="glass-value">{val}</div><div class="glass-sub">{sub}</div></div>', unsafe_allow_html=True)

        # ── Pollen ────────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="display:flex;gap:12px;margin-bottom:12px;">
            <div class="glass-card" style="flex:1;text-align:center;">
                <div class="glass-label">🌾 Grass Pollen</div>
                <div class="glass-value" style="font-size:16px;">{pollen_label(grass_pollen,"grass")}</div>
            </div>
            <div class="glass-card" style="flex:1;text-align:center;">
                <div class="glass-label">🌳 Tree Pollen</div>
                <div class="glass-value" style="font-size:16px;">{pollen_label(tree_pollen,"tree")}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 5-day forecast ────────────────────────────────────────────────────
        st.markdown('<p style="color:white;font-weight:700;font-size:14px;margin:10px 0 8px;">📅 5-DAY FORECAST</p>', unsafe_allow_html=True)
        fc = '<div class="forecast-row">'
        for i in range(5):
            d_name   = "Today" if i==0 else datetime.strptime(daily_f["time"][i],"%Y-%m-%d").strftime("%a")
            d_icon   = WMO_CODES.get(daily_f["weather_code"][i],"🌡️").split()[0]
            d_hi     = round(daily_disp["temperature_2m_max"][i])
            d_lo     = round(daily_disp["temperature_2m_min"][i])
            d_hi_f   = round(daily_f["temperature_2m_max"][i])
            d_lo_f   = round(daily_f["temperature_2m_min"][i])
            alt_u    = "°C" if unit=="°F" else "°F"
            d_hi_alt = to_c(d_hi_f) if unit=="°F" else to_f(d_hi)
            d_lo_alt = to_c(d_lo_f) if unit=="°F" else to_f(d_lo)
            fc += f'<div class="forecast-day"><div class="day-name">{d_name}</div><div class="day-icon">{d_icon}</div><div class="day-hi">{d_hi}{unit}</div><div class="day-lo">{d_lo}{unit}</div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:3px;">{d_hi_alt}/{d_lo_alt}{alt_u}</div></div>'
        st.markdown(fc + "</div>", unsafe_allow_html=True)

        # ── Sunrise/Sunset ────────────────────────────────────────────────────
        try:
            sr = datetime.strptime(daily_f.get("sunrise",[""])[0],"%Y-%m-%dT%H:%M").strftime("%I:%M %p")
            ss = datetime.strptime(daily_f.get("sunset", [""])[0],"%Y-%m-%dT%H:%M").strftime("%I:%M %p")
        except: sr, ss = "N/A","N/A"
        st.markdown(f"""
        <div style="display:flex;gap:12px;margin-bottom:12px;">
            <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌅 Sunrise</div><div class="glass-value">{sr}</div></div>
            <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌇 Sunset</div><div class="glass-value">{ss}</div></div>
        </div>""", unsafe_allow_html=True)

        # ── Shared SVG chart setup ────────────────────────────────────────────
        hourly_temps = wx_display["hourly"]["temperature_2m"][:24]
        hourly_times = wx_f["hourly"]["time"][:24]
        hourly_rain  = wx_f["hourly"]["precipitation_probability"][:24]
        hour_labels  = [datetime.strptime(t,"%Y-%m-%dT%H:%M").strftime("%-I%p").lower() for t in hourly_times]

        W, H = 680, 160
        PL, PR, PT, PB = 36, 10, 16, 32
        CW, CH = W-PL-PR, H-PT-PB

        def tx(i): return PL + (i/(len(hourly_temps)-1))*CW
        def ty(v, mn, mx): return PT + CH - ((v-mn)/(mx-mn or 1))*CH

        x_labels = "".join(
            f'<text x="{tx(i):.1f}" y="{PT+CH+18}" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.6)" font-family="Outfit,sans-serif">{hour_labels[i]}</text>'
            for i in range(0,24,3))

        now_h = local_now.hour

        # ── Hourly temp chart ─────────────────────────────────────────────────
        t_mn = min(hourly_temps)-2; t_mx = max(hourly_temps)+2
        t_pts  = " ".join(f"{tx(i):.1f},{ty(v,t_mn,t_mx):.1f}" for i,v in enumerate(hourly_temps))
        t_area = (f"M{tx(0):.1f},{ty(hourly_temps[0],t_mn,t_mx):.1f} " +
                  " ".join(f"L{tx(i):.1f},{ty(v,t_mn,t_mx):.1f}" for i,v in enumerate(hourly_temps)) +
                  f" L{tx(23):.1f},{PT+CH} L{tx(0):.1f},{PT+CH} Z")
        t_ylbls = "".join(
            f'<text x="{PL-4}" y="{ty(v,t_mn,t_mx):.1f}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{round(v)}{unit}</text>'
            for v in [t_mn+2,(t_mn+t_mx)/2,t_mx-2])
        t_dot  = f'<circle cx="{tx(now_h):.1f}" cy="{ty(hourly_temps[now_h],t_mn,t_mx):.1f}" r="5" fill="white" stroke="rgba(255,255,255,0.4)" stroke-width="3"/>'
        t_dlbl = f'<text x="{tx(now_h):.1f}" y="{ty(hourly_temps[now_h],t_mn,t_mx)-10:.1f}" text-anchor="middle" font-size="11" fill="white" font-weight="bold" font-family="Outfit,sans-serif">{round(hourly_temps[now_h])}{unit}</text>'

        st.markdown(f"""
        <div class="glass-card" style="padding:16px 12px 8px;margin-bottom:6px;">
            <div class="box-title">📊 Today's Hourly Temperature</div>
            <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
                <defs><linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="rgba(255,255,255,0.25)"/>
                    <stop offset="100%" stop-color="rgba(255,255,255,0.02)"/>
                </linearGradient></defs>
                <path d="{t_area}" fill="url(#areaGrad)"/>
                <polyline points="{t_pts}" fill="none" stroke="white" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
                {x_labels}{t_ylbls}{t_dot}{t_dlbl}
            </svg>
        </div>""", unsafe_allow_html=True)

        # ── Hourly rain chart ─────────────────────────────────────────────────
        r_pts  = " ".join(f"{tx(i):.1f},{ty(v,0,100):.1f}" for i,v in enumerate(hourly_rain))
        r_area = (f"M{tx(0):.1f},{ty(hourly_rain[0],0,100):.1f} " +
                  " ".join(f"L{tx(i):.1f},{ty(v,0,100):.1f}" for i,v in enumerate(hourly_rain)) +
                  f" L{tx(23):.1f},{PT+CH} L{tx(0):.1f},{PT+CH} Z")
        r_ylbls = "".join(
            f'<text x="{PL-4}" y="{ty(v,0,100):.1f}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{v}%</text>'
            for v in [0,50,100])
        r_dot  = f'<circle cx="{tx(now_h):.1f}" cy="{ty(hourly_rain[now_h],0,100):.1f}" r="5" fill="white" stroke="rgba(255,255,255,0.4)" stroke-width="3"/>'
        r_dlbl = f'<text x="{tx(now_h):.1f}" y="{ty(hourly_rain[now_h],0,100)-10:.1f}" text-anchor="middle" font-size="11" fill="white" font-weight="bold" font-family="Outfit,sans-serif">{hourly_rain[now_h]}%</text>'

        st.markdown(f"""
        <div class="glass-card" style="padding:16px 12px 8px;margin-bottom:12px;">
            <div class="box-title">🌧️ Hourly Rain Probability</div>
            <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
                <defs><linearGradient id="rainGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="rgba(100,180,255,0.4)"/>
                    <stop offset="100%" stop-color="rgba(100,180,255,0.02)"/>
                </linearGradient></defs>
                <path d="{r_area}" fill="url(#rainGrad)"/>
                <polyline points="{r_pts}" fill="none" stroke="rgba(150,210,255,0.9)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
                {x_labels}{r_ylbls}{r_dot}{r_dlbl}
            </svg>
        </div>""", unsafe_allow_html=True)

        # ── Moon + AQI ────────────────────────────────────────────────────────
        moon_icon, moon_name = get_moon_phase(datetime.now())
        aqi_text, aqi_color  = aqi_label(aqi)
        pm_text = f"{pm25:.1f} µg/m³" if pm25 is not None else "N/A"
        st.markdown(f"""
        <div style="display:flex;gap:12px;margin-bottom:12px;">
            <div class="glass-card" style="flex:1;text-align:center;">
                <div class="glass-label">🌙 Moon Phase</div>
                <div style="font-size:36px;margin:4px 0;">{moon_icon}</div>
                <div class="glass-value" style="font-size:16px;">{moon_name}</div>
            </div>
            <div class="glass-card" style="flex:1;text-align:center;">
                <div class="glass-label">💨 Air Quality (AQI)</div>
                <div class="glass-value" style="color:{aqi_color};font-size:20px;margin:6px 0;">{aqi_text}</div>
                <div class="glass-sub">PM2.5: {pm_text}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Map ───────────────────────────────────────────────────────────────
        st.markdown('<div class="box-title" style="color:rgba(255,255,255,0.6);margin-bottom:6px;">🗺️ WEATHER MAP</div>', unsafe_allow_html=True)
        components.html(f"""
        <div style="border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.25);margin-bottom:12px;">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="map" style="height:260px;width:100%;"></div>
        <script>
            var map=L.map('map',{{zoomControl:true,scrollWheelZoom:false}}).setView([{lat},{lon}],9);
            L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap',maxZoom:18}}).addTo(map);
            L.tileLayer('https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid=demo',{{opacity:0.5}}).addTo(map);
            var icon=L.divIcon({{html:'<div style="font-size:24px;">📍</div>',iconSize:[30,30],className:''}});
            L.marker([{lat},{lon}],{{icon:icon}}).addTo(map).bindPopup('<b>{city_name}</b>').openPopup();
        </script></div>""", height=270)

        st.markdown('<p class="footer">Open-Meteo API • Air Quality API • OpenStreetMap • No API key needed 😄</p>', unsafe_allow_html=True)

# ── Chat box ──────────────────────────────────────────────────────────────────
if st.session_state.weather_ctx:
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:4px;">💬 Ask NimbusAI</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:12px;margin-bottom:12px;">Try: "Should I go hiking tomorrow?" &bull; "Do I need an umbrella?" &bull; "Good day for a run?"</p>', unsafe_allow_html=True)

    if st.session_state.chat_messages:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_messages[-10:]:
            if msg["role"] == "user":
                chat_html += f'<div class="chat-name-user">YOU</div><div class="chat-msg-user">{msg["content"]}</div>'
            else:
                chat_html += f'<div class="chat-name-bot">🌤️ NIMBUS</div><div class="chat-msg-bot">{msg["content"]}</div>'
        st.markdown(chat_html + "</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([5,1])
    with c1:
        user_q = st.text_input("", placeholder="Ask about the weather...", label_visibility="collapsed", key="chat_input")
    with c2:
        send = st.button("Send ➤")

    if send and user_q.strip():
        answer = weather_chat(user_q.strip(), st.session_state.weather_ctx)
        st.session_state.chat_messages.append({"role":"user",     "content": user_q.strip()})
        st.session_state.chat_messages.append({"role":"assistant","content": answer})
        st.rerun()
