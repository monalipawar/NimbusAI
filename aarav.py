import streamlit as st

st.set_page_config(
    page_title="NimbusAI",
    page_icon="🌤️",
    layout="centered"
)

import requests
import math
import random
import json
import urllib.parse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

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
    65: "🚨 Heavy rain warning! Carry an umbrella and avoid flooded areas.",
    75: "🚨 Heavy snow warning! Roads may be slippery — be careful outside.",
    82: "🚨 Violent rain showers! Stay indoors if you can.",
    95: "⚡ Thunderstorm warning! Stay indoors and away from trees.",
    96: "⚡ Thunderstorm with hail! Do not go outside.",
    99: "⚡ Severe thunderstorm with hail! This is dangerous — stay inside."
}
WIND_DIRS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]


# ═══════════════════════════════════════════════════════════════════════════════
# CSS & STYLES
# ═══════════════════════════════════════════════════════════════════════════════

def inject_base_css(bg_gradient):
    st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <style>
    * {{ font-family:'Outfit',sans-serif !important; }}
    .stApp {{ background: {bg_gradient} !important; color: white; min-height:100vh; }}
    [data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stMain"] {{ background:transparent !important; }}
    .main .block-container {{ position:relative; z-index:10; }}
    [data-testid="stVerticalBlock"] {{ position:relative; z-index:10; }}
    [data-testid="stHorizontalBlock"] {{ position:relative; z-index:10; }}
    .hero-card {{ border-radius:24px; padding:32px 28px 24px; color:white; margin-bottom:16px;
                  background:rgba(0,0,0,0.30); box-shadow:0 8px 32px rgba(0,0,0,0.3);
                  border:1px solid rgba(255,255,255,0.25); backdrop-filter:blur(10px);
                  -webkit-backdrop-filter:blur(10px); position:relative; z-index:10; }}
    .hero-temp {{ font-size:84px; font-weight:900; line-height:1; letter-spacing:-4px;
                  text-shadow:0 4px 20px rgba(0,0,0,0.2); color:white; }}
    .hero-city {{ font-size:20px; font-weight:600; color:white; margin-bottom:2px; }}
    .hero-cond {{ font-size:15px; font-weight:300; color:rgba(255,255,255,0.85); }}
    .hilo-badge {{ display:inline-flex; align-items:center; gap:6px; background:rgba(255,255,255,0.2);
                   border:1px solid rgba(255,255,255,0.35); border-radius:30px; padding:5px 14px;
                   font-size:14px; font-weight:600; color:white; margin-right:8px; margin-top:12px; }}
    .glass-card {{ background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2);
                   border-radius:16px; padding:16px 18px; color:white; margin-bottom:12px;
                   backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10;
                   box-shadow:0 4px 24px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.1);
                   transition:transform 0.2s, box-shadow 0.2s; }}
    .glass-card:hover {{ transform:translateY(-1px); box-shadow:0 8px 32px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.15); }}
    .glass-label {{ font-size:11px; font-weight:700; letter-spacing:1.2px; color:rgba(255,255,255,0.65); text-transform:uppercase; margin-bottom:4px; }}
    .glass-value {{ font-size:22px; font-weight:700; color:white; }}
    .glass-sub {{ font-size:12px; color:rgba(255,255,255,0.6); margin-top:2px; }}
    .ai-box {{ border-radius:16px; padding:16px 20px; font-size:15px; font-weight:500; margin-bottom:12px;
               border:1px solid rgba(255,255,255,0.25); background:rgba(0,0,0,0.28); color:white;
               backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }}
    .wear-box {{ border-radius:16px; padding:16px 20px; font-size:14px; line-height:1.9; margin-bottom:12px;
                 border:1px solid rgba(255,255,255,0.25); background:rgba(0,0,0,0.28); color:white;
                 backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }}
    .warn-box {{ border-radius:16px; padding:16px 20px; background:rgba(180,20,20,0.35);
                 border:1px solid rgba(255,120,120,0.5); color:white; margin-bottom:12px; font-size:14px; }}
    .info-box {{ border-radius:16px; padding:14px 18px; background:rgba(0,0,0,0.25);
                 border:1px solid rgba(255,255,255,0.2); color:white; margin-bottom:12px; font-size:14px;
                 backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }}
    .box-title {{ font-size:10px; letter-spacing:1.4px; color:rgba(255,255,255,0.6); font-weight:700; margin-bottom:8px; text-transform:uppercase; }}
    .tomorrow-card {{ border-radius:16px; padding:16px 20px; background:rgba(0,0,0,0.25);
                      border:1px solid rgba(255,255,255,0.2); color:white; margin-bottom:12px;
                      backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }}
    .forecast-row {{ display:flex; gap:8px; margin-bottom:12px; }}
    .forecast-day {{ flex:1; background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2);
                     border-radius:14px; padding:12px 6px; text-align:center; color:white; min-width:52px;
                     backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px); }}
    .day-name {{ font-size:11px; font-weight:700; color:rgba(255,255,255,0.7); margin-bottom:4px; }}
    .day-icon {{ font-size:22px; margin-bottom:4px; }}
    .day-hi {{ font-size:13px; font-weight:700; color:white; }}
    .day-lo {{ font-size:11px; color:rgba(255,255,255,0.55); margin-top:2px; }}
    .chip-row {{ display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px; }}
    .chip {{ background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.25); border-radius:20px;
             padding:4px 12px; font-size:12px; color:white; position:relative; z-index:10; }}
    .footer {{ font-size:11px; color:rgba(255,255,255,0.5); text-align:center; margin-top:8px; }}
    .compare-col {{ background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2);
                    border-radius:16px; padding:16px; margin-bottom:12px;
                    backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }}
    .sparkline-row {{ display:flex; gap:3px; align-items:flex-end; height:36px; margin-top:6px; }}
    .spark-bar {{ flex:1; border-radius:3px 3px 0 0; min-height:4px; }}
    .main-content {{ animation:fade-in 0.5s ease; }}
    @keyframes fade-in {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:translateY(0); }} }}
    .stTextInput>div>div>input {{ background:rgba(255,255,255,0.2) !important; border:1px solid rgba(255,255,255,0.35) !important;
                                   border-radius:12px !important; color:white !important; font-size:15px !important; }}
    .stTextInput>div>div>input::placeholder {{ color:rgba(255,255,255,0.55) !important; }}
    .stTextInput label {{ color:white !important; }}
    .stButton>button {{ background:rgba(255,255,255,0.2) !important; border:1px solid rgba(255,255,255,0.35) !important;
                        border-radius:12px !important; color:white !important; font-weight:600 !important; transition:all 0.2s; }}
    .stButton>button:hover {{ background:rgba(255,255,255,0.32) !important; transform:translateY(-1px); }}
    .stRadio label,.stRadio div {{ color:white !important; }}
    .stSpinner p {{ color:white !important; }}
    .stToggle label {{ color:white !important; }}
    .stExpander {{ background:rgba(255,255,255,0.1) !important; border:1px solid rgba(255,255,255,0.2) !important; border-radius:12px !important; }}
    .stExpander summary {{ color:white !important; }}
    .stSelectbox label {{ color:white !important; }}
    .stSelectbox>div>div {{ background:rgba(255,255,255,0.15) !important; color:white !important; border:1px solid rgba(255,255,255,0.3) !important; border-radius:10px !important; }}
    .stSlider label {{ color:white !important; }}
    @keyframes skeleton-shimmer {{ 0% {{ background-position:-400px 0; }} 100% {{ background-position:400px 0; }} }}
    .skeleton {{ background:linear-gradient(90deg,rgba(255,255,255,0.08) 25%,rgba(255,255,255,0.18) 50%,rgba(255,255,255,0.08) 75%);
                 background-size:400px 100%; animation:skeleton-shimmer 1.4s ease-in-out infinite; border-radius:12px; margin-bottom:12px; }}
    @media(max-width:600px) {{ .hero-temp {{ font-size:56px !important; }} .forecast-row {{ flex-wrap:wrap !important; }} .forecast-day {{ min-width:56px !important; }} }}
    </style>
    """, unsafe_allow_html=True)


SKELETON_CSS = """
<style>
@keyframes skeleton-shimmer { 0% { background-position:-400px 0; } 100% { background-position:400px 0; } }
.skeleton { background:linear-gradient(90deg,rgba(255,255,255,0.08) 25%,rgba(255,255,255,0.18) 50%,rgba(255,255,255,0.08) 75%);
            background-size:400px 100%; animation:skeleton-shimmer 1.4s ease-in-out infinite; border-radius:12px; margin-bottom:12px; }
</style>
"""

KEYBOARD_JS = """
<script>
document.addEventListener('keydown', function(e) {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'r' || e.key === 'R') {
    var btns = window.parent.document.querySelectorAll('button');
    for (var b of btns) { if (b.innerText.includes('Refresh')) { b.click(); break; } }
  }
  if (e.key === '1' || e.key === '2' || e.key === '3') {
    var idx = parseInt(e.key) - 1;
    var favBtns = window.parent.document.querySelectorAll('[data-testid="stButton"] button');
    var loadBtns = Array.from(favBtns).filter(b => b.innerText === 'Load');
    if (loadBtns[idx]) loadBtns[idx].click();
  }
});
</script>
<div style="position:fixed;bottom:16px;right:16px;background:rgba(0,0,0,0.5);color:rgba(255,255,255,0.6);
     font-size:10px;padding:6px 10px;border-radius:8px;z-index:100;pointer-events:none;backdrop-filter:blur(8px);">
  ⌨️ R=Refresh · 1/2/3=Load favourite
</div>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def to_c(f): return round((f - 32) * 5 / 9)
def to_f(c): return round(c * 9 / 5 + 32)
def dual(f): return f"{round(f)}°F / {to_c(f)}°C"

def sky_class(code):
    if code in {95, 96, 99}: return "sky-thunder"
    if code in {61, 63, 65, 51, 53, 55, 80, 81, 82}: return "sky-rain"
    if code in {71, 73, 75}: return "sky-snow"
    if code in {45, 48}: return "sky-fog"
    if code == 3: return "sky-cloudy"
    return "sky-clear"

def wind_dir_label(deg):
    if deg is None: return "—"
    return WIND_DIRS[round(deg / 22.5) % 16]

def temp_color(temp_f):
    if temp_f <= 32:  return "#93C5FD"
    if temp_f <= 50:  return "#60A5FA"
    if temp_f <= 65:  return "#34D399"
    if temp_f <= 77:  return "#4ADE80"
    if temp_f <= 90:  return "#FBBF24"
    if temp_f <= 100: return "#F97316"
    return "#EF4444"

def feel_good_index(temp_f, humidity, wind_mph):
    score = round(max(0, 100 - abs(temp_f - 72) * 2.5) * 0.5 +
                  max(0, 100 - abs(humidity - 45) * 1.2) * 0.3 +
                  max(0, 100 - max(0, wind_mph - 10) * 3) * 0.2)
    score = max(0, min(100, score))
    if score >= 80: return score, "Excellent 😄", "#4ade80"
    if score >= 60: return score, "Good 🙂", "#a3e635"
    if score >= 40: return score, "Fair 😐", "#facc15"
    if score >= 20: return score, "Poor 😟", "#fb923c"
    return score, "Bad 😣", "#f87171"

def pollen_label(val, kind):
    if val is None: return "N/A"
    t = {"grass": [(10,"Low"),(50,"Moderate"),(200,"High")], "tree": [(15,"Low"),(90,"Moderate"),(1500,"High")]}
    for th, l in t.get(kind, []):
        if val < th: return f"{val:.0f} — {l}"
    return f"{val:.0f} — Very High"

def what_to_wear(temp_f, condition, wind_mph):
    cond = condition.lower()
    if temp_f <= 32:    items = [f"🧥 Heavy coat — {dual(temp_f)}, freezing!", "🧤 Gloves", "🧣 Scarf", "🥾 Insulated boots", "🎿 Thermal layers"]
    elif temp_f <= 50:  items = [f"🧥 Jacket — {dual(temp_f)}, very cold!", "👖 Jeans", "🧤 Gloves recommended", "👟 Closed-toe shoes"]
    elif temp_f <= 65:  items = [f"🧶 Hoodie or light jacket — {dual(temp_f)}, cool.", "👖 Jeans or light pants", "👟 Sneakers"]
    elif temp_f <= 77:  items = [f"👕 T-shirt — {dual(temp_f)}, comfortable!", "👖 Light pants", "👟 Any shoes"]
    elif temp_f <= 91:  items = [f"🩳 Shorts — {dual(temp_f)}, warm!", "👕 Light shirt", "🧢 Cap", "🕶️ Sunglasses", "🧴 Sunscreen!"]
    else:               items = [f"🩳 Shorts — {dual(temp_f)}, extremely hot!", "👕 Lightest shirt", "🧢 Sun hat!", "🕶️ Sunglasses", "🧴 High SPF sunscreen", "💧 Carry water everywhere"]
    if any(x in cond for x in ["rain", "drizzle", "shower"]): items += ["☔ Umbrella", "👟 Waterproof shoes"]
    if "snow" in cond: items += ["❄️ Snow boots", "🧦 Thick socks & layers"]
    if "thunder" in cond: items.append("🏠 Consider staying indoors")
    if wind_mph > 5: items.append("🌬️ Windbreaker")
    return items

def outfit_svg(temp_f, cond):
    c = cond.lower()
    shirt_color = "#3b82f6" if temp_f > 77 else "#6366f1"
    hat = ""
    if temp_f > 85:
        hat = '<ellipse cx="50" cy="22" rx="18" ry="5" fill="#fbbf24"/><rect x="38" y="10" width="24" height="14" rx="4" fill="#fbbf24"/>'
    elif temp_f < 50:
        hat = '<ellipse cx="50" cy="22" rx="18" ry="6" fill="#7c3aed"/><rect x="36" y="10" width="28" height="14" rx="6" fill="#7c3aed"/><rect x="34" y="20" width="32" height="5" rx="2" fill="#5b21b6"/>'
    scarf = '<rect x="38" y="52" width="24" height="8" rx="4" fill="#ef4444"/>' if temp_f < 45 else ""
    umbrella = ""
    if any(x in c for x in ["rain","drizzle","shower"]):
        umbrella = '<path d="M85 70 Q85 45 110 45 Q135 45 135 70" fill="#6366f1" stroke="white" stroke-width="1.5"/><line x1="110" y1="45" x2="110" y2="85" stroke="#4b5563" stroke-width="2"/><path d="M110 85 Q110 92 104 92" fill="none" stroke="#4b5563" stroke-width="2"/>'
    pants_color = "#1e40af" if temp_f < 68 else "#0ea5e9"
    pants_h = 35 if temp_f > 77 else 50
    return (f'<div style="display:flex;align-items:center;justify-content:center;padding:12px;">'
            f'<svg viewBox="0 0 160 130" xmlns="http://www.w3.org/2000/svg" style="width:120px;height:auto;">'
            f'{hat}<circle cx="50" cy="35" r="14" fill="#fde68a" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>'
            f'<ellipse cx="50" cy="68" rx="16" ry="20" fill="{shirt_color}"/>{scarf}'
            f'<line x1="34" y1="58" x2="22" y2="78" stroke="{shirt_color}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="66" y1="58" x2="78" y2="78" stroke="{shirt_color}" stroke-width="7" stroke-linecap="round"/>'
            f'<rect x="36" y="84" width="12" height="{pants_h}" rx="4" fill="{pants_color}"/>'
            f'<rect x="52" y="84" width="12" height="{pants_h}" rx="4" fill="{pants_color}"/>'
            f'{umbrella}</svg></div>')

def ai_comment(temp_f, cond, wind_mph):
    c = cond.lower()
    if temp_f <= 32:  return f"🥶 Extreme cold ({dual(temp_f)}) — frost risk, heavy winter gear needed."
    if temp_f <= 50:  return f"🧊 Very cold ({dual(temp_f)}) — winter jacket recommended."
    if temp_f <= 65:  return f"🌬️ Cool weather ({dual(temp_f)}) — light jacket or hoodie works well."
    if temp_f <= 79:  return f"🌤️ Perfect weather ({dual(temp_f)}) — comfortable and balanced."
    if temp_f <= 91:  return f"🔥 Hot weather ({dual(temp_f)}) — stay hydrated and wear light clothes."
    if temp_f > 91:   return f"☀️ Extreme heat ({dual(temp_f)}) — avoid long outdoor exposure."
    if "rain" in c:   return f"☔ Rain expected ({dual(temp_f)}) — carry umbrella or raincoat."
    if "thunder" in c: return f"⛈️ Storm alert ({dual(temp_f)}) — stay indoors if possible."
    if wind_mph > 19: return f"🌬️ Windy ({dual(temp_f)}) — secure loose items."
    return f"🌡️ Normal conditions ({dual(temp_f)})."

def feels_like_reason(temp_f, humidity, wind_mph):
    if wind_mph > 10 and temp_f < 50: return f"🌬️ Wind chill: {wind_mph:.0f} mph winds make it feel colder than {to_c(temp_f)}°C / {round(temp_f)}°F."
    if humidity > 70 and temp_f > 75: return f"💧 Humidity: {humidity}% moisture traps heat, making it feel hotter."
    if humidity < 30:                 return f"🏜️ Low humidity ({humidity}%) lets sweat evaporate fast — feels cooler and drier."
    return f"🌡️ Feels close to actual temperature — comfortable humidity and calm winds."

def humidity_comfort(humidity):
    if humidity > 80: return "💦 Very humid — muggy and uncomfortable.", "#f87171"
    if humidity > 70: return "😓 Humid — may feel sticky and warm.", "#fb923c"
    if humidity < 20: return "🏜️ Very dry — skin and eyes may feel irritated.", "#f87171"
    if humidity < 30: return "😐 Dry air — consider staying hydrated.", "#facc15"
    return "✅ Comfortable humidity level.", "#4ade80"

def aqi_label(aqi):
    if aqi is None: return "N/A", "rgba(255,255,255,0.4)"
    if aqi <= 50:  return f"{aqi} Good", "#4ade80"
    if aqi <= 100: return f"{aqi} Moderate", "#facc15"
    if aqi <= 150: return f"{aqi} Unhealthy for Sensitive", "#fb923c"
    if aqi <= 200: return f"{aqi} Unhealthy", "#f87171"
    if aqi <= 300: return f"{aqi} Very Unhealthy", "#c084fc"
    return f"{aqi} Hazardous", "#ef4444"

def get_moon_phase(date):
    y, m, d = date.year, date.month, date.day
    if m < 3: y -= 1; m += 12
    a = y // 100; b = a // 4; c = 2 - a + b
    e = int(365.25 * (y + 4716)); f = int(30.6001 * (m + 1))
    jd = c + d + e + f - 1524.5
    phase = ((jd - 2451549.5) % 29.53058867) / 29.53058867
    if phase < 0.0625: return "🌑", "New Moon"
    if phase < 0.1875: return "🌒", "Waxing Crescent"
    if phase < 0.3125: return "🌓", "First Quarter"
    if phase < 0.4375: return "🌔", "Waxing Gibbous"
    if phase < 0.5625: return "🌕", "Full Moon"
    if phase < 0.6875: return "🌖", "Waning Gibbous"
    if phase < 0.8125: return "🌗", "Last Quarter"
    return "🌘", "Waning Crescent"

def best_outdoor_window(hourly_temps_f, hourly_rain, hourly_wind, hour_labels):
    best_score = -999; best_i = 0
    for i in range(22):
        t = hourly_temps_f[i]; r = hourly_rain[i]; w = hourly_wind[i]
        score = (100 - abs(t - 72) * 2) - (r * 0.8) - (max(0, w - 10) * 1.5)
        if score > best_score: best_score = score; best_i = i
    t1 = hour_labels[best_i]; t2 = hour_labels[min(best_i + 2, 23)]
    temp_at = round(hourly_temps_f[best_i]); rain_at = hourly_rain[best_i]
    return best_i, f"🌟 Best time to go outside: **{t1} – {t2}** · {dual(temp_at)}, {rain_at}% rain chance"

def what_changed_yesterday(today_hi_f, today_lo_f, today_rain, yesterday_hi_f, yesterday_lo_f, yesterday_rain, unit):
    msgs = []
    hi_diff = today_hi_f - yesterday_hi_f
    disp_hi = round(abs(hi_diff) * 5 / 9) if unit == "°C" else round(abs(hi_diff))
    if abs(hi_diff) >= 2:
        msgs.append(f"{'🌡️ Warmer' if hi_diff > 0 else '❄️ Cooler'} today — high is {disp_hi}{unit} {'higher' if hi_diff > 0 else 'lower'} than yesterday.")
    else:
        msgs.append("🌡️ Similar high temperature to yesterday.")
    rain_diff = today_rain - yesterday_rain
    if abs(rain_diff) >= 15:
        msgs.append(f"{'🌧️ More rain' if rain_diff > 0 else '☀️ Less rain'} expected vs yesterday ({abs(rain_diff):.0f}% {'more' if rain_diff > 0 else 'less'}).")
    return " ".join(msgs) if msgs else "📅 Very similar conditions to yesterday."

def dew_point_f(temp_f, humidity):
    temp_c = (temp_f - 32) * 5 / 9
    a = 17.27; b = 237.7
    if humidity <= 0: return temp_f
    alpha = (a * temp_c) / (b + temp_c) + math.log(humidity / 100)
    dp_c = (b * alpha) / (a - alpha)
    return round(dp_c * 9 / 5 + 32, 1)

def forecast_confidence(day_offset):
    scores = {0:98, 1:95, 2:90, 3:83, 4:74, 5:63, 6:50, 7:38}
    return scores.get(day_offset, 30)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA FETCHING
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_weather(city_name, unit):
    try:
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1",
            timeout=8
        ).json()
        if "results" not in geo or not geo["results"]: return None, None, None, None
        r = geo["results"][0]
        lat, lon = r["latitude"], r["longitude"]
        name = r["name"]; country = r.get("country", "")

        wx_f = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
            f"wind_speed_10m,wind_gusts_10m,wind_direction_10m,weather_code,"
            f"precipitation_probability,uv_index,visibility"
            f"&hourly=temperature_2m,apparent_temperature,precipitation_probability,"
            f"wind_speed_10m,uv_index"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset,"
            f"precipitation_probability_max,precipitation_sum"
            f"&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=7&past_days=1",
            timeout=8
        ).json()

        wx_display = wx_f
        if unit == "°C":
            wx_display = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,apparent_temperature"
                f"&hourly=temperature_2m,apparent_temperature"
                f"&daily=temperature_2m_max,temperature_2m_min"
                f"&temperature_unit=celsius&wind_speed_unit=mph&timezone=auto&forecast_days=7&past_days=1",
                timeout=8
            ).json()

        aq = requests.get(
            f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
            f"&current=us_aqi,pm2_5,grass_pollen,tree_pollen",
            timeout=8
        ).json()

        return wx_f, wx_display, aq, {"lat": lat, "lon": lon, "name": name, "country": country}
    except Exception as e:
        return None, None, None, None

def get_cached_or_fetch(city, unit):
    cache_key = f"cache_{city.lower()}_{unit}"
    time_key  = f"cache_time_{city.lower()}_{unit}"
    now = datetime.now()
    if cache_key in st.session_state and time_key in st.session_state:
        age = (now - st.session_state[time_key]).total_seconds()
        if age < 1800:
            return st.session_state[cache_key], True
    result = fetch_weather(city, unit)
    if result[0]:
        st.session_state[cache_key] = result
        st.session_state[time_key]  = now
    return result, False


# ═══════════════════════════════════════════════════════════════════════════════
# SVG / CHART BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

_chart_counter = [0]

def make_chart(values, color, grad_id, grad_color, unit_lbl, now_h, hour_labels,
               fixed_min=None, fixed_max=None, highlight_i=None):
    _chart_counter[0] += 1
    uid = f"{grad_id}_{_chart_counter[0]}"; cid = f"chart_{uid}"
    W, H = 680, 160; PL, PR, PT, PB = 36, 10, 16, 32; CW, CH = W - PL - PR, H - PT - PB
    mn = (fixed_min if fixed_min is not None else min(values) - 2)
    mx = (fixed_max if fixed_max is not None else max(values) + 2)
    rng = mx - mn or 1

    def tx(i): return PL + (i / (len(values) - 1)) * CW
    def ty(v): return PT + CH - ((v - mn) / rng) * CH

    pts = " ".join(f"{tx(i):.1f},{ty(v):.1f}" for i, v in enumerate(values))
    area = (f"M{tx(0):.1f},{ty(values[0]):.1f} " +
            " ".join(f"L{tx(i):.1f},{ty(v):.1f}" for i, v in enumerate(values)) +
            f" L{tx(len(values)-1):.1f},{PT+CH} L{tx(0):.1f},{PT+CH} Z")
    xlbls = "".join(
        f'<text x="{tx(i):.1f}" y="{PT+CH+18}" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.6)" font-family="Outfit,sans-serif">{hour_labels[i]}</text>'
        for i in range(0, 24, 3)
    )
    ylbls = "".join(
        f'<text x="{PL-4}" y="{ty(v):.1f}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{round(v)}{unit_lbl}</text>'
        for v in [mn + (mx - mn) * 0.1, (mn + mx) / 2, mx - (mx - mn) * 0.1]
    )
    dot  = f'<circle cx="{tx(now_h):.1f}" cy="{ty(values[now_h]):.1f}" r="5" fill="white" stroke="rgba(255,255,255,0.4)" stroke-width="3"/>'
    dlbl = f'<text x="{tx(now_h):.1f}" y="{ty(values[now_h])-10:.1f}" text-anchor="middle" font-size="11" fill="white" font-weight="bold" font-family="Outfit,sans-serif">{round(values[now_h])}{unit_lbl}</text>'
    hi_rect = ""
    if highlight_i is not None:
        x1 = tx(highlight_i); x2 = tx(min(highlight_i + 2, 23))
        hi_rect = f'<rect x="{x1:.1f}" y="{PT}" width="{x2-x1:.1f}" height="{CH}" fill="rgba(255,255,255,0.08)" rx="4"/>'

    xs_js   = "[" + ",".join(f"{tx(i):.1f}" for i in range(len(values))) + "]"
    ys_js   = "[" + ",".join(f"{ty(v):.1f}" for v in values) + "]"
    vals_js = "[" + ",".join(str(round(v, 1)) for v in values) + "]"
    labs_js = "[" + ",".join(f'"{l}"' for l in hour_labels) + "]"

    svg = (
        f'<div id="wrap_{cid}" style="position:relative;width:100%;">'
        f'<svg id="{cid}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;cursor:crosshair;display:block;">'
        f'<defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{grad_color}"/><stop offset="100%" stop-color="rgba(0,0,0,0.01)"/></linearGradient></defs>'
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="transparent" id="hit_{cid}"/>'
        f'{hi_rect}<path d="{area}" fill="url(#{uid})"/>'
        f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'
        f'{xlbls}{ylbls}{dot}{dlbl}'
        f'<line id="vline_{cid}" x1="0" y1="{PT}" x2="0" y2="{PT+CH}" stroke="rgba(255,255,255,0.5)" stroke-width="1.5" stroke-dasharray="4 3" visibility="hidden"/>'
        f'<circle id="dot_{cid}" cx="0" cy="0" r="5" fill="{color}" stroke="white" stroke-width="2" visibility="hidden"/>'
        f'<rect id="tbox_{cid}" x="0" y="0" width="90" height="36" rx="8" fill="rgba(0,0,0,0.75)" visibility="hidden"/>'
        f'<text id="tval_{cid}" x="0" y="0" font-size="12" font-weight="700" fill="white" font-family="Outfit,sans-serif" text-anchor="middle" visibility="hidden"/>'
        f'<text id="ttime_{cid}" x="0" y="0" font-size="10" fill="rgba(255,255,255,0.7)" font-family="Outfit,sans-serif" text-anchor="middle" visibility="hidden"/>'
        f'</svg>'
        f'<script>'
        f'(function(){{'
        f'var svg=document.getElementById("{cid}");'
        f'var xs={xs_js},ys={ys_js},vals={vals_js},labs={labs_js};'
        f'var vl=document.getElementById("vline_{cid}");'
        f'var dc=document.getElementById("dot_{cid}");'
        f'var tb=document.getElementById("tbox_{cid}");'
        f'var tv=document.getElementById("tval_{cid}");'
        f'var tt=document.getElementById("ttime_{cid}");'
        f'var W={W},PL={PL},PR={PR},PT={PT},CH={CH};'
        f'function getIdx(mx){{var best=0,bd=999;for(var i=0;i<xs.length;i++){{var d=Math.abs(xs[i]-mx);if(d<bd){{bd=d;best=i;}}}}return best;}}'
        f'svg.addEventListener("mousemove",function(e){{'
        f'var r=svg.getBoundingClientRect();var svgW=r.width;var scaleX=W/svgW;'
        f'var mx=(e.clientX-r.left)*scaleX;var idx=getIdx(mx);'
        f'var x=xs[idx],y=ys[idx],v=vals[idx],lab=labs[idx];'
        f'vl.setAttribute("x1",x);vl.setAttribute("x2",x);vl.setAttribute("visibility","visible");'
        f'dc.setAttribute("cx",x);dc.setAttribute("cy",y);dc.setAttribute("visibility","visible");'
        f'var tbw=88,tbh=36,tbx=x-tbw/2,tby=y-tbh-10;'
        f'if(tbx<2)tbx=2;if(tbx+tbw>W-2)tbx=W-tbw-2;if(tby<2)tby=y+12;'
        f'tb.setAttribute("x",tbx);tb.setAttribute("y",tby);tb.setAttribute("width",tbw);tb.setAttribute("visibility","visible");'
        f'tv.setAttribute("x",tbx+tbw/2);tv.setAttribute("y",tby+14);tv.setAttribute("visibility","visible");tv.textContent=v+"{unit_lbl}";'
        f'tt.setAttribute("x",tbx+tbw/2);tt.setAttribute("y",tby+27);tt.setAttribute("visibility","visible");tt.textContent=lab;'
        f'}});'
        f'svg.addEventListener("mouseleave",function(){{'
        f'vl.setAttribute("visibility","hidden");dc.setAttribute("visibility","hidden");'
        f'tb.setAttribute("visibility","hidden");tv.setAttribute("visibility","hidden");tt.setAttribute("visibility","hidden");'
        f'}});'
        f'}})();'
        f'</script>'
        f'</div>'
    )
    return svg

def make_sparkline(values, color="#4ade80"):
    mn = min(values); mx = max(values); rng = mx - mn or 1
    bars = "".join(
        f'<div class="spark-bar" style="height:{max(4, round(((v-mn)/rng)*32)+4)}px;background:{color};opacity:0.7;"></div>'
        for v in values
    )
    return f'<div class="sparkline-row">{bars}</div>'

def make_sun_arc(now_dt, sunrise_str, sunset_str):
    try:
        sr = datetime.strptime(sunrise_str, "%I:%M %p")
        ss = datetime.strptime(sunset_str, "%I:%M %p")
        now_mins = now_dt.hour * 60 + now_dt.minute
        sr_mins  = sr.hour * 60 + sr.minute
        ss_mins  = ss.hour * 60 + ss.minute
        day_len  = ss_mins - sr_mins
        if day_len <= 0: raise ValueError
        pct = max(0, min(1, (now_mins - sr_mins) / day_len))
        cx = 20 + pct * 260; cy = 80 - math.sin(pct * math.pi) * 55
        is_day = sr_mins <= now_mins <= ss_mins
        icon = "☀️" if is_day else "🌙"
        return (
            f'<div class="glass-card" style="margin-bottom:12px;"><div class="box-title">🌅 Sun Position</div>'
            f'<svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">'
            f'<path d="M20 80 Q150 15 280 80" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="2" stroke-dasharray="6 4"/>'
            f'<path d="M20 80 Q{20+pct*130:.0f} {80-math.sin(pct*math.pi/2)*55:.0f} {cx:.0f} {cy:.0f}" fill="none" stroke="rgba(255,220,80,0.7)" stroke-width="2.5"/>'
            f'<text x="20" y="95" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{sunrise_str}</text>'
            f'<text x="280" y="95" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{sunset_str}</text>'
            f'<text x="{cx:.0f}" y="{cy-6:.0f}" text-anchor="middle" font-size="20">{icon}</text>'
            f'</svg></div>'
        )
    except:
        return ""

def animated_weather_icon(code, size=64):
    c = WMO_CODES.get(code, "🌡️").lower()
    if "thunder" in c:
        return f"""<svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <style>.cloud-body{{animation:cloud-bob 3s ease-in-out infinite;}}.bolt{{animation:bolt-flash 1.5s ease-in-out infinite;}}
          @keyframes cloud-bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
          @keyframes bolt-flash{{0%,100%{{opacity:1}}50%{{opacity:0.2}}}}</style>
          <g class="cloud-body"><ellipse cx="32" cy="22" rx="18" ry="11" fill="rgba(100,120,160,0.9)"/>
          <ellipse cx="20" cy="26" rx="10" ry="8" fill="rgba(100,120,160,0.9)"/>
          <ellipse cx="44" cy="26" rx="10" ry="8" fill="rgba(100,120,160,0.9)"/>
          <rect x="16" y="26" width="32" height="10" rx="4" fill="rgba(100,120,160,0.9)"/></g>
          <g class="bolt"><polygon points="34,34 28,46 33,46 30,58 40,42 35,42 38,34" fill="#FFD700"/></g></svg>"""
    elif "snow" in c:
        return f"""<svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <style>.sf1{{animation:fall1 2s linear infinite;}}.sf2{{animation:fall2 2.5s linear infinite;}}.sf3{{animation:fall3 1.8s linear infinite;}}.cloud-s{{animation:cloud-bob 3s ease-in-out infinite;}}
          @keyframes fall1{{0%{{transform:translateY(-5px);opacity:0}}30%{{opacity:1}}100%{{transform:translateY(20px);opacity:0}}}}
          @keyframes fall2{{0%{{transform:translateY(-5px);opacity:0}}40%{{opacity:1}}100%{{transform:translateY(18px);opacity:0}}}}
          @keyframes fall3{{0%{{transform:translateY(-5px);opacity:0}}50%{{opacity:1}}100%{{transform:translateY(22px);opacity:0}}}}
          @keyframes cloud-bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}</style>
          <g class="cloud-s"><ellipse cx="32" cy="20" rx="16" ry="9" fill="rgba(200,220,255,0.95)"/>
          <ellipse cx="22" cy="24" rx="9" ry="7" fill="rgba(200,220,255,0.95)"/>
          <ellipse cx="42" cy="24" rx="9" ry="7" fill="rgba(200,220,255,0.95)"/>
          <rect x="18" y="24" width="28" height="8" rx="3" fill="rgba(200,220,255,0.95)"/></g>
          <text class="sf1" x="18" y="50" font-size="10" fill="white" text-anchor="middle">❄</text>
          <text class="sf2" x="32" y="52" font-size="10" fill="white" text-anchor="middle">❄</text>
          <text class="sf3" x="46" y="48" font-size="10" fill="white" text-anchor="middle">❄</text></svg>"""
    elif "rain" in c or "drizzle" in c or "shower" in c:
        return f"""<svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <style>.r1{{animation:drop1 1s linear infinite;}}.r2{{animation:drop2 1.2s linear infinite;}}.r3{{animation:drop3 0.9s linear infinite;}}.r4{{animation:drop4 1.1s linear infinite;}}.cloud-r{{animation:cloud-bob 3s ease-in-out infinite;}}
          @keyframes drop1{{0%{{transform:translateY(0);opacity:1}}100%{{transform:translateY(16px);opacity:0}}}}
          @keyframes drop2{{0%{{transform:translateY(-4px);opacity:0.5}}100%{{transform:translateY(14px);opacity:0}}}}
          @keyframes drop3{{0%{{transform:translateY(-2px);opacity:0.8}}100%{{transform:translateY(18px);opacity:0}}}}
          @keyframes drop4{{0%{{transform:translateY(-6px);opacity:0.3}}100%{{transform:translateY(12px);opacity:0}}}}
          @keyframes cloud-bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}</style>
          <g class="cloud-r"><ellipse cx="32" cy="20" rx="16" ry="9" fill="rgba(120,140,180,0.9)"/>
          <ellipse cx="22" cy="24" rx="9" ry="7" fill="rgba(120,140,180,0.9)"/>
          <ellipse cx="42" cy="24" rx="9" ry="7" fill="rgba(120,140,180,0.9)"/>
          <rect x="18" y="24" width="28" height="8" rx="3" fill="rgba(120,140,180,0.9)"/></g>
          <line class="r1" x1="22" y1="36" x2="19" y2="46" stroke="rgba(150,200,255,0.8)" stroke-width="2" stroke-linecap="round"/>
          <line class="r2" x1="32" y1="36" x2="29" y2="46" stroke="rgba(150,200,255,0.8)" stroke-width="2" stroke-linecap="round"/>
          <line class="r3" x1="42" y1="36" x2="39" y2="46" stroke="rgba(150,200,255,0.8)" stroke-width="2" stroke-linecap="round"/>
          <line class="r4" x1="27" y1="38" x2="24" y2="48" stroke="rgba(150,200,255,0.6)" stroke-width="1.5" stroke-linecap="round"/></svg>"""
    elif "cloud" in c or "overcast" in c:
        return f"""<svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <style>.cloud-main{{animation:cloud-float 4s ease-in-out infinite;}}@keyframes cloud-float{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(4px)}}}}</style>
          <g class="cloud-main"><ellipse cx="32" cy="28" rx="20" ry="12" fill="rgba(180,200,230,0.95)"/>
          <ellipse cx="20" cy="32" rx="11" ry="9" fill="rgba(180,200,230,0.95)"/>
          <ellipse cx="44" cy="32" rx="11" ry="9" fill="rgba(180,200,230,0.95)"/>
          <rect x="16" y="32" width="32" height="10" rx="4" fill="rgba(180,200,230,0.95)"/></g></svg>"""
    else:
        return f"""<svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
          <style>.sun{{animation:spin 12s linear infinite;transform-origin:32px 32px;}}.sun-core{{animation:pulse-sun 3s ease-in-out infinite;transform-origin:32px 32px;}}
          @keyframes spin{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
          @keyframes pulse-sun{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.08)}}}}</style>
          <g class="sun">
          <line x1="32" y1="4" x2="32" y2="14" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
          <line x1="32" y1="50" x2="32" y2="60" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
          <line x1="4" y1="32" x2="14" y2="32" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
          <line x1="50" y1="32" x2="60" y2="32" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
          <line x1="11" y1="11" x2="18" y2="18" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
          <line x1="46" y1="46" x2="53" y2="53" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
          <line x1="53" y1="11" x2="46" y2="18" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
          <line x1="18" y1="46" x2="11" y2="53" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/></g>
          <g class="sun-core"><circle cx="32" cy="32" r="14" fill="#FFD700"/><circle cx="32" cy="32" r="10" fill="#FFF176"/></g></svg>"""

def thermometer_svg(temp_f, unit, temp_d):
    pct = max(0, min(1, (temp_f - 0) / 120))
    fill_h = round(pct * 80)
    col = "#93C5FD" if temp_f < 40 else "#4ADE80" if temp_f < 70 else "#FB923C" if temp_f < 90 else "#EF4444"
    return f"""<div class="glass-card" style="text-align:center;padding:16px;">
      <div class="box-title">🌡️ Temperature Gauge</div>
      <svg viewBox="0 0 60 130" xmlns="http://www.w3.org/2000/svg" style="width:60px;height:130px;margin:0 auto;display:block;">
        <rect x="22" y="10" width="16" height="85" rx="8" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
        <rect x="24" y="{10 + (80 - fill_h)}" width="12" height="{fill_h + 15}" rx="6" fill="{col}" opacity="0.85"/>
        <circle cx="30" cy="105" r="12" fill="{col}" opacity="0.9"/>
        <circle cx="30" cy="105" r="7" fill="{col}"/>
        <text x="42" y="14" font-size="7" fill="rgba(255,255,255,0.5)" font-family="Outfit,sans-serif">120°</text>
        <text x="42" y="54" font-size="7" fill="rgba(255,255,255,0.5)" font-family="Outfit,sans-serif">60°</text>
        <text x="42" y="94" font-size="7" fill="rgba(255,255,255,0.5)" font-family="Outfit,sans-serif">0°</text>
      </svg>
      <div style="font-size:20px;font-weight:700;color:{col};margin-top:4px;">{round(temp_d)}{unit}</div>
    </div>"""

def wind_compass_svg(wind_deg, wind_mph, wind_dir_str):
    deg = wind_deg or 0
    return f"""<div class="glass-card" style="text-align:center;padding:16px;">
      <div class="box-title">🧭 Wind Direction Compass</div>
      <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" style="width:120px;height:120px;margin:0 auto;display:block;">
        <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
        <circle cx="60" cy="60" r="46" fill="rgba(0,0,0,0.2)"/>
        <text x="60" y="12" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.7)" font-family="Outfit,sans-serif" font-weight="700">N</text>
        <text x="60" y="114" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.5)" font-family="Outfit,sans-serif">S</text>
        <text x="8" y="64" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.5)" font-family="Outfit,sans-serif">W</text>
        <text x="112" y="64" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.5)" font-family="Outfit,sans-serif">E</text>
        {"".join(f'<line x1="60" y1="10" x2="60" y2="16" stroke="rgba(255,255,255,0.3)" stroke-width="1" transform="rotate({i*30} 60 60)"/>' for i in range(12))}
        <g transform="rotate({deg} 60 60)">
          <polygon points="60,18 56,62 60,58 64,62" fill="#EF4444"/>
          <polygon points="60,102 56,58 60,62 64,58" fill="rgba(255,255,255,0.4)"/>
          <circle cx="60" cy="60" r="5" fill="white"/>
        </g>
        <text x="60" y="74" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.8)" font-family="Outfit,sans-serif">{wind_dir_str}</text>
        <text x="60" y="86" text-anchor="middle" font-size="11" fill="white" font-weight="700" font-family="Outfit,sans-serif">{round(wind_mph)} mph</text>
      </svg>
    </div>"""

def visibility_gauge_svg(vis_km):
    if vis_km is None: return ""
    pct = min(1, vis_km / 10)
    angle = -140 + pct * 280
    col = "#EF4444" if vis_km < 1 else "#FB923C" if vis_km < 3 else "#FACC15" if vis_km < 6 else "#4ADE80"
    label = "Dense fog" if vis_km < 0.5 else "Fog" if vis_km < 2 else "Haze" if vis_km < 5 else "Good" if vis_km < 8 else "Excellent"
    rad = math.radians(angle)
    nx = 50 + 35 * math.cos(rad); ny = 60 + 35 * math.sin(rad)
    return f"""<div class="glass-card" style="text-align:center;padding:16px;">
      <div class="box-title">👁️ Visibility Gauge</div>
      <svg viewBox="0 0 100 80" xmlns="http://www.w3.org/2000/svg" style="width:120px;height:96px;margin:0 auto;display:block;">
        <path d="M10,60 A40,40 0 1,1 90,60" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="8" stroke-linecap="round"/>
        <path d="M10,60 A40,40 0 1,1 90,60" fill="none" stroke="{col}" stroke-width="8"
              stroke-linecap="round" stroke-dasharray="125.6" stroke-dashoffset="{125.6*(1-pct):.1f}"/>
        <line x1="50" y1="60" x2="{nx:.1f}" y2="{ny:.1f}" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="50" cy="60" r="4" fill="white"/>
        <text x="50" y="76" text-anchor="middle" font-size="8" fill="rgba(255,255,255,0.5)" font-family="Outfit,sans-serif">{label}</text>
      </svg>
      <div style="font-size:20px;font-weight:700;color:{col};">{vis_km} km</div>
    </div>"""

def make_particles(sky_bg):
    modes = {
        "sky-clear":   ("clear",   "#050d1a", "#1a6eff", "#87ceeb"),
        "sky-cloudy":  ("cloudy",  "#1a2a3a", "#4b5e7a", "#b0c4d8"),
        "sky-rain":    ("rain",    "#0d1b2a", "#1e3a5f", "#4a7fa8"),
        "sky-snow":    ("snow",    "#1a2a3a", "#6b8cae", "#ddeeff"),
        "sky-thunder": ("thunder", "#050510", "#1a1a2e", "#4a3f6b"),
        "sky-fog":     ("fog",     "#1a2030", "#6b7a8d", "#c5d0d8"),
    }
    mode, bg1, bg2, bg3 = modes.get(sky_bg, modes["sky-clear"])
    return f"""<canvas id="nimbusCanvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;pointer-events:none;"></canvas>
<script>
(function(){{
  var C=document.getElementById('nimbusCanvas');
  if(!C)return;
  var ctx=C.getContext('2d');
  var W,H,ps=[],clouds=[],stars=[];
  var mode='{mode}',bg1='{bg1}',bg2='{bg2}',bg3='{bg3}',t=0;
  var flashA=0,nextFlash=5000,lastFlash=0;
  function resize(){{W=C.width=window.innerWidth;H=C.height=window.innerHeight;init();}}
  function rnd(a,b){{return a+Math.random()*(b-a);}}
  function mkRain(){{return{{x:rnd(0,W),y:rnd(-H,0),len:rnd(10,25),spd:rnd(12,22),a:rnd(0.3,0.7),w:rnd(0.8,1.8)}};}}
  function mkSnow(){{return{{x:rnd(0,W),y:rnd(-H,0),r:rnd(2,5),spd:rnd(0.5,2),drift:rnd(-0.6,0.6),a:rnd(0.5,1),wob:rnd(0,6.28),ws:rnd(0.02,0.05)}};}}
  function mkStar(){{return{{x:rnd(0,W),y:rnd(0,H*0.65),r:rnd(0.4,1.8),a:rnd(0.3,0.9),ts:rnd(0.02,0.06),tp:rnd(0,6.28)}};}}
  function mkCloud(){{return{{x:rnd(-200,W),y:rnd(20,H*0.45),w:rnd(120,260),h:rnd(40,90),spd:rnd(0.15,0.6),a:rnd(0.08,0.22)}};}}
  function mkFog(y){{return{{x:0,y:y,h:rnd(80,140),spd:rnd(0.1,0.3),a:rnd(0.04,0.1)}};}}
  function init(){{
    ps=[];clouds=[];stars=[];
    var n={{clear:[0,5,80],cloudy:[0,14,0],rain:[220,9,0],snow:[160,7,0],thunder:[280,12,0],fog:[0,0,0]}}[mode]||[0,5,80];
    for(var i=0;i<n[0];i++)ps.push(mode==='snow'?mkSnow():mkRain());
    for(var i=0;i<n[1];i++){{var c=mkCloud();if(mode!=='clear')c.a*=1.6;clouds.push(c);}}
    for(var i=0;i<n[2];i++)stars.push(mkStar());
    if(mode==='fog')for(var i=0;i<8;i++)ps.push(mkFog(i*(H/8)));
  }}
  function drawBg(){{
    var g=ctx.createLinearGradient(0,0,0,H);
    g.addColorStop(0,bg1);g.addColorStop(0.55,bg2);g.addColorStop(1,bg3);
    ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  }}
  function drawSun(){{
    var sx=W*0.76,sy=H*0.17,pulse=1+0.018*Math.sin(t*0.022);
    for(var r=90;r>=18;r-=14){{ctx.beginPath();ctx.arc(sx,sy,r*pulse,0,6.28);ctx.fillStyle='rgba(255,210,60,'+(0.025+(90-r)*0.0012)+')';ctx.fill();}}
    var sg=ctx.createRadialGradient(sx,sy,0,sx,sy,24*pulse);
    sg.addColorStop(0,'#fffde0');sg.addColorStop(0.5,'#FFD700');sg.addColorStop(1,'rgba(255,140,0,0)');
    ctx.beginPath();ctx.arc(sx,sy,24*pulse,0,6.28);ctx.fillStyle=sg;ctx.fill();
    ctx.save();ctx.translate(sx,sy);ctx.rotate(t*0.004);
    for(var i=0;i<12;i++){{ctx.rotate(0.524);ctx.beginPath();ctx.moveTo(28,0);ctx.lineTo(42+4*Math.sin(t*0.06+i),0);ctx.strokeStyle='rgba(255,210,60,0.35)';ctx.lineWidth=2;ctx.stroke();}}
    ctx.restore();
  }}
  function drawMoon(){{
    var mx=W*0.78,my=H*0.14;
    var mg=ctx.createRadialGradient(mx,my,0,mx,my,30);
    mg.addColorStop(0,'rgba(220,230,255,0.95)');mg.addColorStop(0.6,'rgba(180,200,255,0.4)');mg.addColorStop(1,'rgba(100,120,200,0)');
    ctx.beginPath();ctx.arc(mx,my,30,0,6.28);ctx.fillStyle=mg;ctx.fill();
    ctx.beginPath();ctx.arc(mx+11,my-4,24,0,6.28);ctx.fillStyle=bg1;ctx.fill();
  }}
  function drawAurora(){{
    ctx.save();ctx.globalAlpha=0.045+0.02*Math.sin(t*0.009);
    var cols=['rgba(0,255,140,1)','rgba(0,140,255,1)','rgba(160,0,255,1)'];
    for(var i=0;i<3;i++){{
      var y0=H*0.28+i*50;
      var g2=ctx.createLinearGradient(0,y0,0,y0+70);
      g2.addColorStop(0,'rgba(0,0,0,0)');g2.addColorStop(0.5,cols[i]);g2.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=g2;ctx.beginPath();ctx.moveTo(0,y0);
      for(var x2=0;x2<=W;x2+=16)ctx.lineTo(x2,y0+35*Math.sin(x2/W*9.42+t*0.012+i*1.3));
      ctx.lineTo(W,y0+70);ctx.lineTo(0,y0+70);ctx.closePath();ctx.fill();
    }}
    ctx.restore();
  }}
  function drawCloud(c){{
    ctx.save();ctx.globalAlpha=c.a;
    var g=ctx.createRadialGradient(c.x+c.w/2,c.y+c.h/2,0,c.x+c.w/2,c.y+c.h/2,c.w*0.65);
    g.addColorStop(0,'rgba(255,255,255,0.95)');g.addColorStop(1,'rgba(200,220,255,0)');
    ctx.fillStyle=g;
    ctx.beginPath();
    ctx.ellipse(c.x+c.w*.5,c.y+c.h*.65,c.w*.48,c.h*.38,0,0,6.28);
    ctx.ellipse(c.x+c.w*.28,c.y+c.h*.42,c.w*.3,c.h*.36,0,0,6.28);
    ctx.ellipse(c.x+c.w*.68,c.y+c.h*.38,c.w*.26,c.h*.32,0,0,6.28);
    ctx.fill();ctx.restore();
  }}
  function drawStar(s){{
    s.tp+=s.ts;
    ctx.save();ctx.globalAlpha=s.a*(0.45+0.55*Math.sin(s.tp));
    ctx.fillStyle='white';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,6.28);ctx.fill();ctx.restore();
  }}
  function drawLightning(now){{
    if(mode!=='thunder')return;
    if(now-lastFlash>nextFlash){{
      flashA=0.3;lastFlash=now;nextFlash=rnd(4000,10000);
      ctx.save();ctx.strokeStyle='rgba(200,220,255,0.95)';ctx.lineWidth=2.5;
      ctx.shadowColor='rgba(150,180,255,1)';ctx.shadowBlur=25;ctx.globalAlpha=0.9;
      ctx.beginPath();
      var bx=rnd(W*0.15,W*0.85),by=0;ctx.moveTo(bx,by);
      while(by<H*0.75){{bx+=rnd(-55,55);by+=rnd(25,50);ctx.lineTo(bx,by);}}
      ctx.stroke();ctx.restore();
    }}
    if(flashA>0.01){{ctx.fillStyle='rgba(180,200,255,'+flashA+')';ctx.fillRect(0,0,W,H);flashA*=0.8;}}
  }}
  function animate(now){{
    t++;ctx.clearRect(0,0,W,H);drawBg();
    if(mode==='clear'){{
      var hg=ctx.createLinearGradient(0,H*0.55,0,H);
      hg.addColorStop(0,'rgba(255,160,60,0)');hg.addColorStop(1,'rgba(255,80,20,0.12)');
      ctx.fillStyle=hg;ctx.fillRect(0,H*0.55,W,H*0.45);
    }}
    if(mode==='clear')drawAurora();
    stars.forEach(drawStar);
    if(mode==='clear')drawSun();
    if(mode==='thunder'||mode==='fog')drawMoon();
    clouds.forEach(function(c){{drawCloud(c);c.x+=c.spd;if(c.x>W+300){{c.x=-300;c.y=rnd(20,H*0.45);}}}});
    ps.forEach(function(p,i){{
      if(mode==='rain'||mode==='thunder'){{
        ctx.save();ctx.globalAlpha=p.a;ctx.strokeStyle='rgba(180,220,255,0.8)';ctx.lineWidth=p.w;
        ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x-2.5,p.y+p.len);ctx.stroke();ctx.restore();
        p.y+=p.spd;p.x-=1.5;if(p.y>H){{ps[i]=mkRain();ps[i].y=-15;}}
      }} else if(mode==='snow'){{
        ctx.save();ctx.globalAlpha=p.a;ctx.fillStyle='rgba(225,240,255,0.95)';
        ctx.shadowColor='rgba(200,230,255,0.7)';ctx.shadowBlur=5;
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.28);ctx.fill();ctx.restore();
        p.y+=p.spd;p.wob+=p.ws;p.x+=Math.sin(p.wob)*p.drift;
        if(p.y>H){{ps[i]=mkSnow();ps[i].y=-10;}}
        if(p.x<0)p.x=W;if(p.x>W)p.x=0;
      }} else if(mode==='fog'){{
        ctx.save();ctx.globalAlpha=p.a*(0.6+0.4*Math.sin(t*0.012+p.y*0.01));
        var fg=ctx.createLinearGradient(0,p.y,0,p.y+p.h);
        fg.addColorStop(0,'rgba(200,210,220,0)');fg.addColorStop(0.5,'rgba(200,210,220,1)');fg.addColorStop(1,'rgba(200,210,220,0)');
        ctx.fillStyle=fg;ctx.fillRect(-W,p.y,W*4,p.h);ctx.restore();
        p.x-=p.spd;if(p.x<-W)p.x=0;
      }}
    }});
    drawLightning(now);
    requestAnimationFrame(animate);
  }}
  window.addEventListener('resize',resize);
  resize();
  requestAnimationFrame(animate);
}})();
</script>"""


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE RENDERERS
# ═══════════════════════════════════════════════════════════════════════════════

def render_favourites():
    if "favourites" not in st.session_state:
        st.session_state.favourites = []
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">⭐ Favourite Cities</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if i < len(st.session_state.favourites):
                city = st.session_state.favourites[i]
                st.markdown(f'<div class="chip" style="cursor:pointer;text-align:center;padding:8px;">⭐ {city}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Load", key=f"load_fav_{i}"):
                        st.session_state.city_input = city
                        st.rerun()
                with c2:
                    if st.button("❌", key=f"del_fav_{i}"):
                        st.session_state.favourites.pop(i)
                        st.rerun()
            else:
                new_fav = st.text_input("", placeholder=f"City {i+1}...", key=f"fav_input_{i}", label_visibility="collapsed")
                if st.button("+ Save", key=f"save_fav_{i}") and new_fav.strip():
                    st.session_state.favourites.append(new_fav.strip())
                    st.rerun()

def activity_scores(temp_f, humidity, wind_mph, rain_pct, uv, condition):
    cond = condition.lower()
    is_raining = any(x in cond for x in ["rain","drizzle","shower","thunder"])
    def score(base): return max(0, min(10, round(base)))
    running  = score(8 - abs(temp_f-60)/8 - rain_pct/25 - max(0,wind_mph-15)/5)
    cycling  = score(8 - abs(temp_f-65)/8 - rain_pct/20 - max(0,wind_mph-12)/4)
    hiking   = score(9 - abs(temp_f-65)/7 - rain_pct/20 - max(0,uv-7)*0.5)
    picnic   = score(9 - abs(temp_f-72)/6 - rain_pct/15 - max(0,wind_mph-10)/4 - max(0,uv-8)*0.4)
    golf     = score(8 - abs(temp_f-68)/8 - rain_pct/20 - max(0,wind_mph-15)/5)
    swimming = score(7 + (temp_f-80)/5 - rain_pct/20 - (4 if is_raining else 0))
    skiing   = score(8 if temp_f < 35 else max(0, 8-(temp_f-35)/5))
    bbq      = score(9 - abs(temp_f-75)/6 - rain_pct/12 - max(0,wind_mph-12)/4)
    activities = [
        ("🏃 Running", running), ("🚴 Cycling", cycling), ("🥾 Hiking", hiking), ("🧺 Picnic", picnic),
        ("⛳ Golf", golf), ("🏊 Swimming", swimming), ("⛷️ Skiing", skiing), ("🔥 BBQ", bbq),
    ]
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🏅 Activity Weather Scores</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, (name, sc) in enumerate(activities):
        color = "#4ade80" if sc >= 7 else "#facc15" if sc >= 4 else "#f87171"
        with cols[idx % 4]:
            st.markdown(f"""<div class="glass-card" style="text-align:center;padding:12px 8px;">
              <div style="font-size:13px;font-weight:600;color:white;margin-bottom:6px;">{name}</div>
              <div style="font-size:28px;font-weight:900;color:{color};">{sc}/10</div>
              <div style="font-size:10px;color:rgba(255,255,255,0.5);">{"✅ Great" if sc>=7 else "⚠️ OK" if sc>=4 else "❌ Poor"}</div>
            </div>""", unsafe_allow_html=True)

def render_packing_list():
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🧳 Trip Packing List</p>', unsafe_allow_html=True)
    with st.expander("Generate a packing list for your trip"):
        dest   = st.text_input("Destination city", placeholder="e.g. Miami", key="pack_dest")
        nights = st.slider("How many nights?", 1, 14, 3, key="pack_nights")
        if st.button("📋 Generate Packing List", key="gen_pack") and dest.strip():
            with st.spinner("Fetching destination weather..."):
                result = fetch_weather(dest.strip(), "°F")
                if result[0] is None:
                    st.error("City not found.")
                else:
                    wx_f, _, _, meta = result
                    cur = wx_f["current"]
                    t = cur["temperature_2m"]; c = WMO_CODES.get(cur["weather_code"],""); w = cur["wind_speed_10m"]
                    cond = c.lower()
                    pack = ["📋 **Essentials:** Passport/ID, Phone charger, Headphones, Medications"]
                    pack.append(f"🌡️ **Weather at {meta['name']}:** {dual(t)}, {c}")
                    if t < 45:   pack += ["🧥 Heavy winter coat","🧤 Gloves + scarf",f"🥾 Warm boots","🧦 Thermal socks x"+str(nights)]
                    elif t < 65: pack += ["🧥 Light jacket","👖 Jeans x"+str(max(2,nights//2)),"👟 Closed-toe shoes"]
                    elif t < 80: pack += ["👕 T-shirts x"+str(nights),"👖 Light pants/shorts","👟 Comfortable sneakers"]
                    else:        pack += ["🩳 Shorts x"+str(nights),"👕 Light shirts x"+str(nights),"🕶️ Sunglasses","🧴 High SPF sunscreen","🧢 Hat"]
                    if any(x in cond for x in ["rain","drizzle","shower"]): pack += ["☔ Umbrella","🧥 Waterproof jacket"]
                    if "snow" in cond: pack += ["❄️ Snow boots","🧣 Scarf","🧤 Gloves"]
                    if t > 75: pack += ["💧 Reusable water bottle","🏊 Swimwear"]
                    pack.append(f"💼 **For {nights} nights:** {nights+1} outfits recommended")
                    for item in pack:
                        st.markdown(f'<div class="info-box" style="margin-bottom:6px;">{item}</div>', unsafe_allow_html=True)

def render_hourly_table(hourly_temps_d, hourly_feels_d, hourly_rain_vals, hourly_wind, hour_labels, unit, now_h):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🕐 Hourly Breakdown Table</p>', unsafe_allow_html=True)
    with st.expander("Show full 24-hour table"):
        html = '<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:12px;">'
        html += '<tr style="color:rgba(255,255,255,0.6);font-size:10px;text-transform:uppercase;letter-spacing:0.1em;">'
        html += '<th style="padding:6px 10px;text-align:left;">Time</th><th style="padding:6px 10px;">Temp</th><th style="padding:6px 10px;">Feels</th><th style="padding:6px 10px;">Rain %</th><th style="padding:6px 10px;">Wind</th><th style="padding:6px 10px;">Wear</th></tr>'
        for i in range(24):
            bg = "rgba(255,255,255,0.12)" if i == now_h else "transparent"
            t = hourly_temps_d[i]; f = hourly_feels_d[i]; r = hourly_rain_vals[i]; w = hourly_wind[i]
            if t < 35:    wear = "Heavy coat, thermals, gloves, scarf"
            elif t < 50:  wear = "Winter jacket, jeans, warm boots"
            elif t < 60:  wear = "Light jacket or fleece, jeans"
            elif t < 65:  wear = "Hoodie or sweater, jeans"
            elif t < 72:  wear = "Light hoodie, casual pants"
            elif t < 80:  wear = "T-shirt, light pants or jeans"
            elif t < 88:  wear = "Shorts, light t-shirt, sunglasses"
            else:         wear = "Shorts, tank top, sunscreen, hat"
            if r > 60:    wear += " + umbrella & waterproof shoes"
            elif r > 35:  wear += " + umbrella"
            if w > 20:    wear += " + windbreaker"
            html += f'<tr style="background:{bg};border-bottom:1px solid rgba(255,255,255,0.06);">'
            html += f'<td style="padding:6px 10px;color:{"#FCD34D" if i==now_h else "white"};font-weight:{"700" if i==now_h else "400"};">{"▶ " if i==now_h else ""}{hour_labels[i]}</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:white;">{round(t)}{unit}</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:rgba(255,200,100,0.9);">{round(f)}{unit}</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:{"#f87171" if r>60 else "#60a5fa" if r>30 else "rgba(255,255,255,0.6)"};">{r}%</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:rgba(200,240,200,0.9);">{round(w)} mph</td>'
            html += f'<td style="padding:6px 10px;font-size:11px;color:rgba(255,255,255,0.8);">{wear}</td></tr>'
        html += '</table></div>'
        st.markdown(html, unsafe_allow_html=True)

def render_rain_countdown(hourly_rain_vals, hour_labels, now_h):
    st.markdown("---")
    rain_hour = None
    for i in range(now_h, 24):
        if hourly_rain_vals[i] > 50:
            rain_hour = i; break
    stop_hour = None
    if hourly_rain_vals[now_h] > 50:
        for i in range(now_h + 1, 24):
            if hourly_rain_vals[i] <= 30:
                stop_hour = i; break
    if hourly_rain_vals[now_h] > 50:
        msg = "🌧️ **It's raining now!**"
        if stop_hour:
            hrs = stop_hour - now_h
            msg += f" Expected to clear around **{hour_labels[stop_hour]}** (~{hrs}h from now)"
        else:
            msg += " Rain likely continues through the evening."
    elif rain_hour:
        hrs = rain_hour - now_h
        msg = f"⏱️ **Rain expected in ~{hrs} hour{'s' if hrs>1 else ''}** — around **{hour_labels[rain_hour]}**. Get your umbrella ready!"
    else:
        msg = "☀️ **No significant rain expected** for the rest of today."
    st.markdown(f'<div class="ai-box"><div class="box-title">🌧️ Rain Countdown</div>{msg}</div>', unsafe_allow_html=True)

def render_historical(lat, lon, unit):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">📜 This Day Last Year</p>', unsafe_allow_html=True)
    try:
        yesterday = datetime.now() - timedelta(days=366)
        date_str = yesterday.strftime("%Y-%m-%d")
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code"
               f"&temperature_unit={'fahrenheit' if unit=='°F' else 'celsius'}"
               f"&timezone=auto&start_date={date_str}&end_date={date_str}")
        data = requests.get(url, timeout=8).json()
        if "daily" in data:
            hi = round(data["daily"]["temperature_2m_max"][0])
            lo = round(data["daily"]["temperature_2m_min"][0])
            rain = round(data["daily"].get("precipitation_sum",[0])[0], 1)
            code_h = data["daily"].get("weather_code",[0])[0]
            cond_h = WMO_CODES.get(code_h, "Unknown")
            st.markdown(f"""<div class="glass-card">
              <div class="box-title">📅 {yesterday.strftime("%B %d, %Y")} — One Year Ago</div>
              <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:6px;">
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Condition</div><div style="font-size:15px;color:white;">{cond_h}</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">High</div><div style="font-size:15px;color:#f87171;">{hi}{unit}</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Low</div><div style="font-size:15px;color:#60a5fa;">{lo}{unit}</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Rain</div><div style="font-size:15px;color:#93c5fd;">{rain} mm</div></div>
              </div>
            </div>""", unsafe_allow_html=True)
    except:
        st.markdown('<div class="info-box">📜 Historical data temporarily unavailable.</div>', unsafe_allow_html=True)

def render_severe_weather_map(lat, lon, city_name, code):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">⚠️ Regional Weather Map</p>', unsafe_allow_html=True)
    is_severe = code in SEVERE_CODES
    alert_color = "#DC2626" if is_severe else "#1D9E75"
    alert_msg = f"⚠️ SEVERE WEATHER ACTIVE — {WMO_CODES.get(code,'')}" if is_severe else "✅ No severe weather alerts in this region"
    components.html(f"""
    <div style="border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.25);margin-bottom:8px;">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <div id="smap" style="height:300px;width:100%;"></div>
    <script>
      var map=L.map('smap',{{zoomControl:true,scrollWheelZoom:false}}).setView([{lat},{lon}],5);
      L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap',maxZoom:18}}).addTo(map);
      var circle=L.circle([{lat},{lon}],{{color:'{alert_color}',fillColor:'{alert_color}',fillOpacity:0.15,radius:80000}}).addTo(map);
      var icon=L.divIcon({{html:'<div style="font-size:28px;">{"⚠️" if is_severe else "📍"}</div>',iconSize:[35,35],className:''}});
      L.marker([{lat},{lon}],{{icon:icon}}).addTo(map).bindPopup('<b>{city_name}</b><br>{WMO_CODES.get(code,"")}').openPopup();
    </script></div>""", height=310)
    st.markdown(f'<div class="{"warn-box" if is_severe else "info-box"}">{alert_msg}</div>', unsafe_allow_html=True)

def render_trip_planner():
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">✈️ Trip Weather Planner</p>', unsafe_allow_html=True)
    with st.expander("Plan your trip weather"):
        dest = st.text_input("Where are you going?", placeholder="e.g. Paris", key="trip_dest")
        col1, col2 = st.columns(2)
        with col1: start = st.date_input("Departure date", key="trip_start")
        with col2: end   = st.date_input("Return date", key="trip_end")
        if st.button("🗺️ Check Trip Weather", key="trip_go") and dest.strip():
            if end <= start:
                st.error("Return date must be after departure date.")
            else:
                with st.spinner("Fetching trip forecast..."):
                    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={dest.strip()}&count=1", timeout=6).json()
                    if "results" not in geo or not geo["results"]:
                        st.error("Destination not found.")
                    else:
                        r2 = geo["results"][0]; lat2, lon2 = r2["latitude"], r2["longitude"]
                        days = min((end - start).days + 1, 16)
                        wx = requests.get(
                            f"https://api.open-meteo.com/v1/forecast?latitude={lat2}&longitude={lon2}"
                            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max"
                            f"&temperature_unit=fahrenheit&timezone=auto&forecast_days={days}&start_date={start}",
                            timeout=8
                        ).json()
                        if "daily" not in wx:
                            st.error("Could not fetch forecast.")
                        else:
                            st.markdown(f'<div class="ai-box"><div class="box-title">✈️ {r2["name"]} Trip Forecast</div>Your {days}-day trip weather summary</div>', unsafe_allow_html=True)
                            fc = '<div class="forecast-row" style="flex-wrap:wrap;">'
                            for i in range(min(days, len(wx["daily"]["time"]))):
                                date_s = wx["daily"]["time"][i]
                                day_label = datetime.strptime(date_s, "%Y-%m-%d").strftime("%b %d")
                                di = WMO_CODES.get(wx["daily"]["weather_code"][i],"🌡️").split()[0]
                                dh = round(wx["daily"]["temperature_2m_max"][i])
                                dl = round(wx["daily"]["temperature_2m_min"][i])
                                dr = wx["daily"].get("precipitation_probability_max",[0]*days)[i]
                                fc += (f'<div class="forecast-day" style="min-width:70px;"><div class="day-name">{day_label}</div>'
                                       f'<div class="day-icon">{di}</div><div class="day-hi">{dh}°F</div>'
                                       f'<div class="day-lo">{dl}°F</div><div style="font-size:10px;color:rgba(255,255,255,0.5);">🌧️{dr}%</div></div>')
                            st.markdown(fc + "</div>", unsafe_allow_html=True)

def render_music_mood(condition, temp_f, fgi):
    cond = condition.lower()
    if "thunder" in cond:       mood, playlist, emoji, desc = "Dramatic & Intense",  "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U", "⛈️", "Thunderstorms call for epic, cinematic soundtracks."
    elif "snow" in cond:        mood, playlist, emoji, desc = "Cozy & Warm",          "https://open.spotify.com/playlist/37i9dQZF1DX6aTaZa0K6VA", "❄️", "Snow day vibes — curl up with hot cocoa and chill music."
    elif "rain" in cond or "drizzle" in cond: mood, playlist, emoji, desc = "Rainy Day Chill", "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO", "🌧️", "Perfect rainy day playlist — lofi, jazz, and mellow tunes."
    elif temp_f > 85:           mood, playlist, emoji, desc = "Summer Vibes",         "https://open.spotify.com/playlist/37i9dQZF1DX4dyzvuaRJ0n", "🔥", "Hot weather calls for beach beats and summer anthems."
    elif temp_f < 40:           mood, playlist, emoji, desc = "Winter Warmth",        "https://open.spotify.com/playlist/37i9dQZF1DX6aTaZa0K6VA", "🥶", "Cold outside — time for acoustic comfort music."
    elif fgi >= 70:             mood, playlist, emoji, desc = "Happy & Energetic",    "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0", "😄", "Perfect weather deserves perfect upbeat music!"
    else:                       mood, playlist, emoji, desc = "Easy Listening",       "https://open.spotify.com/playlist/37i9dQZF1DWYmmr74INQlb", "🎵", "Balanced weather, balanced tunes."
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">🎵 Weather Music Mood</div>
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
        <div style="font-size:40px;">{emoji}</div>
        <div style="flex:1;">
          <div style="font-size:16px;font-weight:700;color:white;">{mood}</div>
          <div style="font-size:13px;color:rgba(255,255,255,0.7);margin:4px 0;">{desc}</div>
          <a href="{playlist}" target="_blank" style="display:inline-block;background:#1DB954;color:white;
             text-decoration:none;border-radius:20px;padding:6px 16px;font-size:12px;font-weight:600;margin-top:4px;">
            ▶ Open in Spotify</a>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

def render_weather_photo(condition, city_name):
    st.markdown("---")
    cond = condition.lower()
    if "thunder" in cond:                         keyword = "thunderstorm lightning"
    elif "snow" in cond:                          keyword = "snowfall winter"
    elif "rain" in cond or "drizzle" in cond:     keyword = "rain city"
    elif "fog" in cond:                           keyword = "foggy morning"
    elif "cloud" in cond:                         keyword = "cloudy sky"
    elif "clear" in cond or "sunny" in cond:      keyword = "sunny day blue sky"
    else:                                         keyword = "weather sky"
    photo_url = f"https://source.unsplash.com/800x400/?{keyword.replace(' ',',')}"
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">📸 Weather Photo — {condition}</div>
      <img src="{photo_url}" style="width:100%;border-radius:10px;margin-top:6px;object-fit:cover;height:200px;" alt="Weather photo"/>
      <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:6px;">Photo via Unsplash · {keyword}</div>
    </div>""", unsafe_allow_html=True)

def render_aqi_health(aqi_text, pm25):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🫁 Air Quality Health Guide</p>', unsafe_allow_html=True)
    try: aqi_num = int(aqi_text.split()[0])
    except: aqi_num = 50
    if aqi_num <= 50:
        groups = [("🏃 Runners","✅ Perfect for outdoor runs. No restrictions."),("🧒 Children","✅ Safe for outdoor play all day."),("🫁 Asthma","✅ Air is clean. Inhaler still recommended as precaution."),("👴 Elderly","✅ Safe for all outdoor activities.")]
    elif aqi_num <= 100:
        groups = [("🏃 Runners","⚠️ Sensitive runners may want to reduce intensity."),("🧒 Children","✅ Generally safe. Watch for eye irritation."),("🫁 Asthma","⚠️ Keep rescue inhaler handy. Avoid heavy exertion."),("👴 Elderly","⚠️ Limit prolonged outdoor exposure.")]
    elif aqi_num <= 150:
        groups = [("🏃 Runners","❌ Move workout indoors. Outdoor running not advised."),("🧒 Children","⚠️ Limit outdoor play to short periods."),("🫁 Asthma","❌ Stay indoors. Use air purifier if available."),("👴 Elderly","❌ Avoid outdoor activity. Keep windows closed.")]
    else:
        groups = [("🏃 Runners","🚫 Do not exercise outdoors under any circumstances."),("🧒 Children","🚫 Keep children indoors. School outdoor activities should be cancelled."),("🫁 Asthma","🚫 Emergency risk. Stay indoors, use purifier, contact doctor if symptoms worsen."),("👴 Elderly","🚫 Stay indoors. Serious health risk.")]
    cols = st.columns(2)
    for i, (group, advice) in enumerate(groups):
        with cols[i % 2]:
            st.markdown(f'<div class="glass-card"><div class="box-title">{group}</div><div style="font-size:13px;color:white;">{advice}</div></div>', unsafe_allow_html=True)

def render_weather_diary(city_name, temp_d, unit, condition):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">📔 Weather Diary</p>', unsafe_allow_html=True)
    if "diary" not in st.session_state: st.session_state.diary = []
    with st.expander("📝 Log today's weather experience"):
        mood = st.selectbox("How does this weather make you feel?",
            ["😄 Happy","😊 Content","😐 Neutral","😟 Gloomy","🥶 Too cold","🥵 Too hot","😴 Sleepy","⚡ Energised"],
            key="diary_mood")
        note = st.text_area("Add a note (optional)", placeholder="e.g. Perfect day for a walk!", key="diary_note", height=80)
        if st.button("💾 Save to Diary", key="save_diary"):
            entry = {"date": datetime.now().strftime("%b %d, %Y %I:%M %p"), "city": city_name,
                     "temp": f"{round(temp_d)}{unit}", "cond": condition, "mood": mood, "note": note}
            st.session_state.diary.insert(0, entry)
            st.session_state.diary = st.session_state.diary[:30]
            st.success("✅ Logged!")
    if st.session_state.diary:
        st.markdown('<div class="box-title" style="color:rgba(255,255,255,0.6);margin-top:8px;">Recent Entries</div>', unsafe_allow_html=True)
        for entry in st.session_state.diary[:5]:
            st.markdown(f"""<div class="glass-card" style="margin-bottom:6px;">
              <div style="display:flex;justify-content:space-between;font-size:11px;color:rgba(255,255,255,0.5);margin-bottom:4px;">
                <span>{entry['date']} · {entry['city']}</span><span>{entry['temp']} · {entry['cond'].split(' ',1)[-1]}</span>
              </div>
              <div style="font-size:14px;color:white;">{entry['mood']}</div>
              {f'<div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:4px;">{entry["note"]}</div>' if entry['note'] else ''}
            </div>""", unsafe_allow_html=True)

def render_multi_city_dashboard(unit):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🌍 Multi-City Dashboard</p>', unsafe_allow_html=True)
    default_cities = ["New York","London","Tokyo","Sydney","Paris","Dubai"]
    with st.expander("📊 Show world cities weather"):
        custom = st.text_input("Add your own cities (comma separated)", placeholder="e.g. Mumbai, Toronto, Berlin", key="multi_city_inp")
        cities = default_cities.copy()
        if custom.strip():
            cities = [c.strip() for c in custom.split(",") if c.strip()][:6]
        if st.button("🌍 Load Cities", key="load_multi"):
            st.session_state.multi_city_data = []
            with st.spinner("Loading world weather..."):
                for city in cities[:6]:
                    try:
                        res = fetch_weather(city, unit)
                        if res[0]:
                            wx_f2, wx_d2, _, meta2 = res
                            cur2 = wx_f2["current"]; cur2d = wx_d2["current"]
                            fgi_v, fgi_l, fgi_c = feel_good_index(cur2["temperature_2m"], cur2["relative_humidity_2m"], cur2["wind_speed_10m"])
                            st.session_state.multi_city_data.append({
                                "name": meta2["name"], "country": meta2["country"],
                                "temp": round(cur2d["temperature_2m"]), "unit": unit,
                                "cond": WMO_CODES.get(cur2["weather_code"],"🌡️"),
                                "fgi": fgi_v, "fgi_col": fgi_c,
                                "rain": cur2.get("precipitation_probability", 0),
                                "wind": round(cur2["wind_speed_10m"])
                            })
                    except: pass
        if "multi_city_data" in st.session_state and st.session_state.multi_city_data:
            cols = st.columns(3)
            for i, city in enumerate(st.session_state.multi_city_data):
                with cols[i % 3]:
                    icon = city["cond"].split()[0]
                    st.markdown(f"""<div class="glass-card" style="text-align:center;padding:12px;">
                      <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.7);">{city['name']}, {city['country']}</div>
                      <div style="font-size:30px;margin:4px 0;">{icon}</div>
                      <div style="font-size:24px;font-weight:900;color:white;">{city['temp']}{city['unit']}</div>
                      <div style="font-size:11px;color:rgba(255,255,255,0.6);margin-top:2px;">{city['cond'].split(' ',1)[1] if ' ' in city['cond'] else city['cond']}</div>
                      <div style="font-size:11px;color:{city['fgi_col']};margin-top:4px;">😊 {city['fgi']}/100</div>
                      <div style="font-size:10px;color:rgba(255,255,255,0.5);">🌧️{city['rain']}% 💨{city['wind']}mph</div>
                    </div>""", unsafe_allow_html=True)

def render_golden_hour(sunrise_str, sunset_str, local_now):
    try:
        sr = datetime.strptime(sunrise_str, "%I:%M %p")
        ss = datetime.strptime(sunset_str, "%I:%M %p")
        sr_mins = sr.hour * 60 + sr.minute; ss_mins = ss.hour * 60 + ss.minute
        now_mins = local_now.hour * 60 + local_now.minute
        morning_start = sr_mins; morning_end = sr_mins + 60
        evening_start = ss_mins - 60; evening_end = ss_mins
        def fmt_mins(m):
            h = m // 60 % 24; mi = m % 60
            return datetime(2000,1,1,h,mi).strftime("%I:%M %p").lstrip("0")
        if morning_start <= now_mins <= morning_end:
            remaining = morning_end - now_mins
            msg = f"🌅 **Golden hour NOW!** Morning golden hour ends in {remaining} min · Until {fmt_mins(morning_end)}"
            color = "#FCD34D"
        elif evening_start <= now_mins <= evening_end:
            remaining = evening_end - now_mins
            msg = f"🌇 **Golden hour NOW!** Evening golden hour ends in {remaining} min · Until {fmt_mins(evening_end)}"
            color = "#F97316"
        elif now_mins < morning_start:
            wait = morning_start - now_mins
            msg = f"📸 Morning golden hour in **{wait} min** · {fmt_mins(morning_start)} – {fmt_mins(morning_end)}"
            color = "rgba(255,255,255,0.7)"
        elif now_mins < evening_start:
            wait = evening_start - now_mins
            h = wait // 60; m = wait % 60
            msg = f"📸 Evening golden hour in **{h}h {m}min** · {fmt_mins(evening_start)} – {fmt_mins(evening_end)}"
            color = "rgba(255,255,255,0.7)"
        else:
            msg = f"🌙 Golden hour passed for today. Tomorrow: {fmt_mins(morning_start)} – {fmt_mins(morning_end)}"
            color = "rgba(255,255,255,0.5)"
        st.markdown(f'<div class="glass-card"><div class="box-title">📸 Golden Hour Timer</div><div style="font-size:14px;color:{color};">{msg}</div></div>', unsafe_allow_html=True)
    except: pass

def render_pollen_tracker(grass_pollen, tree_pollen):
    month = datetime.now().month
    season_grass = {3:"Rising 📈",4:"Peak ⚠️",5:"Peak ⚠️",6:"High",7:"Declining 📉",8:"Low",9:"Low"}.get(month,"Low")
    season_tree  = {2:"Rising 📈",3:"Peak ⚠️",4:"Peak ⚠️",5:"Declining 📉",6:"Low",7:"Low"}.get(month,"Low")
    advice = []
    if grass_pollen and grass_pollen > 50: advice.append("🌾 High grass pollen — close windows, shower after outdoors")
    if tree_pollen  and tree_pollen  > 90: advice.append("🌳 High tree pollen — antihistamines may help, wear sunglasses")
    if not advice: advice.append("✅ Pollen levels manageable today")
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">🌿 Pollen Season Tracker</div>
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:10px;">
        <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Grass season</div><div style="font-size:14px;color:white;font-weight:600;">{season_grass}</div></div>
        <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Tree season</div><div style="font-size:14px;color:white;font-weight:600;">{season_tree}</div></div>
        <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Today's grass</div><div style="font-size:14px;color:#4ADE80;font-weight:600;">{f"{grass_pollen:.0f}" if grass_pollen else "N/A"}</div></div>
        <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Today's tree</div><div style="font-size:14px;color:#4ADE80;font-weight:600;">{f"{tree_pollen:.0f}" if tree_pollen else "N/A"}</div></div>
      </div>
      <div style="font-size:13px;color:rgba(255,255,255,0.85);">{"<br>".join(advice)}</div>
    </div>""", unsafe_allow_html=True)

def render_commute_advisor(hourly_temps_d, hourly_feels_d, hourly_rain_vals, hourly_wind, hour_labels, unit):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🚗 Commute Weather Advisor</p>', unsafe_allow_html=True)
    with st.expander("Check your commute window"):
        c1, c2 = st.columns(2)
        with c1: dep = st.slider("Departure hour", 0, 23, 8, key="commute_dep")
        with c2: arr = st.slider("Arrival hour",   0, 23, 9, key="commute_arr")
        if dep > arr: dep, arr = arr, dep
        window = list(range(dep, min(arr + 1, 24)))
        if window:
            avg_t = sum(hourly_temps_d[i] for i in window) / len(window)
            avg_f = sum(hourly_feels_d[i] for i in window) / len(window)
            max_r = max(hourly_rain_vals[i] for i in window)
            max_w = max(hourly_wind[i] for i in window)
            tips  = []
            if max_r > 60: tips.append("☔ Bring an umbrella — rain likely during commute")
            if max_r > 30: tips.append("🌂 Light rain possible — consider waterproof jacket")
            if max_w > 20: tips.append("💨 Strong winds — extra commute time likely")
            if avg_t < 35: tips.append("🧊 Near freezing — watch for icy roads")
            if avg_t > 90: tips.append("🔥 Very hot — stay hydrated, use AC")
            if not tips:   tips.append("✅ Comfortable commute conditions")
            st.markdown(f"""<div class="ai-box">
              <div class="box-title">🚗 Your commute: {hour_labels[dep]} – {hour_labels[min(arr,23)]}</div>
              <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:10px;">
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Avg temp</div><div style="font-size:16px;color:white;font-weight:700;">{round(avg_t)}{unit}</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Feels like</div><div style="font-size:16px;color:white;font-weight:700;">{round(avg_f)}{unit}</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Max rain</div><div style="font-size:16px;color:#60A5FA;font-weight:700;">{max_r}%</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.6);">Max wind</div><div style="font-size:16px;color:rgba(200,240,200,0.9);font-weight:700;">{round(max_w)} mph</div></div>
              </div>
              {"<br>".join(tips)}
            </div>""", unsafe_allow_html=True)

def render_weekend_scorer(daily_f, daily_d, unit):
    try:
        today_wd   = datetime.now().weekday()
        days_to_sat = (5 - today_wd) % 7
        days_to_sun = (6 - today_wd) % 7
        sat_i = 1 + days_to_sat; sun_i = 1 + days_to_sun
        max_i = len(daily_f["temperature_2m_max"]) - 1
        if sat_i > max_i or sun_i > max_i: return
        def day_score(i):
            hi = daily_f["temperature_2m_max"][i]; lo = daily_f["temperature_2m_min"][i]
            rain = daily_f.get("precipitation_probability_max", [50]*8)[i]
            mid  = (hi + lo) / 2
            return max(0, min(10, round((100 - abs(mid-68)/5)*0.5 + (100-rain)*0.4 + 50*0.1) / 10))
        sat_s = day_score(sat_i); sun_s = day_score(sun_i)
        sat_hi = round(daily_d["temperature_2m_max"][sat_i]); sat_lo = round(daily_d["temperature_2m_min"][sat_i])
        sun_hi = round(daily_d["temperature_2m_max"][sun_i]); sun_lo = round(daily_d["temperature_2m_min"][sun_i])
        sat_r = daily_f.get("precipitation_probability_max",[0]*8)[sat_i]
        sun_r = daily_f.get("precipitation_probability_max",[0]*8)[sun_i]
        winner = "Saturday 🏆" if sat_s >= sun_s else "Sunday 🏆"
        st.markdown(f"""<div class="glass-card">
          <div class="box-title">📅 Weekend Weather Scorer</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px;">
            <div style="background:rgba({"255,255,255,0.12" if sat_s>=sun_s else "0,0,0,0.1"});border-radius:10px;padding:12px;border:1px solid rgba(255,255,255,{"0.3" if sat_s>=sun_s else "0.1"});">
              <div style="font-size:12px;font-weight:700;color:white;margin-bottom:6px;">Saturday {"🏆" if sat_s>=sun_s else ""}</div>
              <div style="font-size:28px;font-weight:900;color:{"#4ADE80" if sat_s>=7 else "#FACC15" if sat_s>=4 else "#f87171"};">{sat_s}/10</div>
              <div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:4px;">{sat_hi}/{sat_lo}{unit} · 🌧️{sat_r}%</div>
            </div>
            <div style="background:rgba({"255,255,255,0.12" if sun_s>sat_s else "0,0,0,0.1"});border-radius:10px;padding:12px;border:1px solid rgba(255,255,255,{"0.3" if sun_s>sat_s else "0.1"});">
              <div style="font-size:12px;font-weight:700;color:white;margin-bottom:6px;">Sunday {"🏆" if sun_s>sat_s else ""}</div>
              <div style="font-size:28px;font-weight:900;color:{"#4ADE80" if sun_s>=7 else "#FACC15" if sun_s>=4 else "#f87171"};">{sun_s}/10</div>
              <div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:4px;">{sun_hi}/{sun_lo}{unit} · 🌧️{sun_r}%</div>
            </div>
          </div>
          <div style="font-size:13px;color:#FCD34D;margin-top:10px;font-weight:600;">→ Better day for outdoor plans: {winner}</div>
        </div>""", unsafe_allow_html=True)
    except: pass

def render_feels_comparison(temp_f, feels_f, temp_d, feels_d, humidity, wind_mph, unit):
    reason = feels_like_reason(temp_f, humidity, wind_mph)
    diff   = feels_f - temp_f
    bar_col = "#f87171" if diff > 5 else "#60a5fa" if diff < -5 else "#4ADE80"
    feels_pct = max(10, min(90, round(60 + (diff / 30) * 40)))
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">Actual vs Feels Like</div>
      <div style="display:flex;align-items:center;gap:20px;margin:10px 0;flex-wrap:wrap;">
        <div style="flex:1;text-align:center;">
          <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-bottom:4px;">ACTUAL</div>
          <div style="font-size:36px;font-weight:900;color:white;">{round(temp_d)}{unit}</div>
        </div>
        <div style="font-size:28px;color:rgba(255,255,255,0.4);">→</div>
        <div style="flex:1;text-align:center;">
          <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-bottom:4px;">FEELS LIKE</div>
          <div style="font-size:36px;font-weight:900;color:{bar_col};">{round(feels_d)}{unit}</div>
        </div>
      </div>
      <div style="background:rgba(255,255,255,0.1);border-radius:8px;height:8px;margin:8px 0;overflow:hidden;">
        <div style="height:8px;width:{feels_pct}%;background:{bar_col};border-radius:8px;transition:width 0.8s;"></div>
      </div>
      <div style="font-size:13px;color:rgba(255,255,255,0.8);">{reason}</div>
    </div>""", unsafe_allow_html=True)

def render_day_progress(local_now, sunrise_str, sunset_str):
    try:
        sr    = datetime.strptime(sunrise_str, "%I:%M %p")
        ss    = datetime.strptime(sunset_str, "%I:%M %p")
        now_m = local_now.hour * 60 + local_now.minute
        sr_m  = sr.hour * 60 + sr.minute
        ss_m  = ss.hour * 60 + ss.minute
        day_len = ss_m - sr_m
        pct = max(0, min(100, round((now_m - sr_m) / day_len * 100)))
        is_day = sr_m <= now_m <= ss_m
        elapsed_h = (now_m - sr_m) // 60; elapsed_m = (now_m - sr_m) % 60
        remain_h  = (ss_m - now_m) // 60; remain_m  = (ss_m - now_m) % 60
        msg = f"☀️ {elapsed_h}h {elapsed_m}m since sunrise · {remain_h}h {remain_m}m until sunset" if is_day else "🌙 After sunset — night time"
        st.markdown(f"""<div class="glass-card">
          <div class="box-title">🌅 Day Progress</div>
          <div style="display:flex;justify-content:space-between;font-size:11px;color:rgba(255,255,255,0.6);margin-bottom:6px;">
            <span>🌅 {sunrise_str}</span><span>{pct}% of daylight</span><span>🌇 {sunset_str}</span>
          </div>
          <div style="background:rgba(255,255,255,0.1);border-radius:20px;height:14px;overflow:hidden;position:relative;">
            <div style="height:14px;width:{pct}%;background:linear-gradient(90deg,#FF6B35,#FFD700,#87CEEB);border-radius:20px;transition:width 1s;"></div>
            <div style="position:absolute;top:0;left:{pct}%;transform:translateX(-50%);font-size:12px;line-height:14px;">{"☀️" if is_day else "🌙"}</div>
          </div>
          <div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:8px;">{msg}</div>
        </div>""", unsafe_allow_html=True)
    except: pass

def render_wind_detail(wind_mph, gusts_mph, wind_dir_str):
    gust_pct = min(100, round(gusts_mph / 60 * 100))
    wind_pct = min(100, round(wind_mph   / 60 * 100))
    diff     = gusts_mph - wind_mph
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">💨 Wind Detail — Sustained vs Gusts</div>
      <div style="margin:10px 0;">
        <div style="display:flex;justify-content:space-between;font-size:12px;color:rgba(255,255,255,0.7);margin-bottom:4px;">
          <span>Sustained</span><span style="color:white;font-weight:700;">{round(wind_mph)} mph {wind_dir_str}</span>
        </div>
        <div style="background:rgba(255,255,255,0.1);border-radius:6px;height:10px;overflow:hidden;">
          <div style="height:10px;width:{wind_pct}%;background:#4ADE80;border-radius:6px;"></div>
        </div>
      </div>
      <div style="margin:10px 0;">
        <div style="display:flex;justify-content:space-between;font-size:12px;color:rgba(255,255,255,0.7);margin-bottom:4px;">
          <span>Gusts</span><span style="color:#FB923C;font-weight:700;">{round(gusts_mph)} mph</span>
        </div>
        <div style="background:rgba(255,255,255,0.1);border-radius:6px;height:10px;overflow:hidden;">
          <div style="height:10px;width:{gust_pct}%;background:#FB923C;border-radius:6px;"></div>
        </div>
      </div>
      <div style="font-size:12px;color:rgba(255,255,255,0.7);margin-top:8px;">
        {"⚠️ High gust differential — unexpected strong bursts possible" if diff > 15 else "✅ Gusts close to sustained — consistent wind conditions"}
        · Gust spike: +{round(diff)} mph
      </div>
    </div>""", unsafe_allow_html=True)

def render_dew_point(temp_f, humidity, unit):
    dp_f = dew_point_f(temp_f, humidity)
    dp_d = dp_f if unit == "°F" else to_c(dp_f)
    if dp_f < 50:   comfort, col = "Dry & comfortable", "#4ADE80"
    elif dp_f < 60: comfort, col = "Comfortable",       "#a3e635"
    elif dp_f < 65: comfort, col = "Slightly humid",    "#FACC15"
    elif dp_f < 70: comfort, col = "Humid & sticky",    "#FB923C"
    else:           comfort, col = "Very oppressive",   "#EF4444"
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">💦 Dew Point</div>
      <div style="font-size:28px;font-weight:700;color:{col};">{round(dp_d)}{unit}</div>
      <div style="font-size:13px;color:{col};margin-top:4px;">{comfort}</div>
      <div style="font-size:11px;color:rgba(255,255,255,0.5);margin-top:4px;">
        More reliable comfort indicator than humidity alone
      </div>
    </div>""", unsafe_allow_html=True)

def render_uv_timeline(hourly_uv, hour_labels, now_h):
    if not hourly_uv: return
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🌞 UV Index Timeline</p>', unsafe_allow_html=True)
    def uv_color(v):
        if v<=2: return "#4ADE80"
        if v<=5: return "#FACC15"
        if v<=7: return "#FB923C"
        if v<=10: return "#EF4444"
        return "#C084FC"
    def uv_label(v):
        if v<=2: return "Low"
        if v<=5: return "Moderate"
        if v<=7: return "High"
        if v<=10: return "Very High"
        return "Extreme"
    html = '<div class="glass-card"><div class="box-title">🌞 UV Index by Hour</div>'
    html += '<div style="display:flex;gap:3px;align-items:flex-end;height:60px;margin-bottom:6px;">'
    mx = max(hourly_uv) if hourly_uv else 11
    for i, v in enumerate(hourly_uv):
        h = max(4, round((v / max(mx,1)) * 55))
        html += f'<div title="{hour_labels[i]}: UV {round(v,1)}" style="flex:1;height:{h}px;background:{uv_color(v)};border-radius:3px 3px 0 0;opacity:{"1" if i==now_h else "0.7"};cursor:pointer;"></div>'
    html += '</div>'
    html += '<div style="display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,0.5);">'
    for i in range(0, 24, 4): html += f'<span>{hour_labels[i]}</span>'
    html += '</div>'
    cur_uv = hourly_uv[now_h] if now_h < len(hourly_uv) else 0
    html += f'<div style="margin-top:10px;font-size:13px;color:white;">Current: <strong style="color:{uv_color(cur_uv)};">UV {round(cur_uv,1)} — {uv_label(cur_uv)}</strong>'
    if cur_uv >= 3: html += ' · 🧴 Sunscreen recommended'
    if cur_uv >= 6: html += ' · 🧢 Hat required · Seek shade 10am–4pm'
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)

def render_30day_history(lat, lon, unit):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">📅 30-Day Temperature History</p>', unsafe_allow_html=True)
    with st.expander("Show last 30 days"):
        with st.spinner("Fetching historical data..."):
            try:
                end_d   = datetime.now()
                start_d = end_d - timedelta(days=30)
                url = (f"https://archive-api.open-meteo.com/v1/archive"
                       f"?latitude={lat}&longitude={lon}"
                       f"&start_date={start_d.strftime('%Y-%m-%d')}"
                       f"&end_date={end_d.strftime('%Y-%m-%d')}"
                       f"&daily=temperature_2m_max,temperature_2m_min"
                       f"&temperature_unit={'fahrenheit' if unit=='°F' else 'celsius'}"
                       f"&timezone=auto")
                data = requests.get(url, timeout=10).json()
                if "daily" not in data:
                    st.warning("Historical data unavailable."); return
                dates = data["daily"]["time"]
                highs = data["daily"]["temperature_2m_max"]
                lows  = data["daily"]["temperature_2m_min"]
                components.html(f"""
                <style>body{{margin:0;background:transparent;font-family:Outfit,sans-serif;}}</style>
                <div style="background:rgba(0,0,0,0.25);border:1px solid rgba(255,255,255,0.2);border-radius:16px;padding:14px;">
                  <div style="font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.6);font-weight:700;margin-bottom:8px;text-transform:uppercase;">High/Low temperatures — past 30 days</div>
                  <canvas id="hist" width="680" height="180" style="width:100%;height:auto;"></canvas>
                  <div id="hist-tip" style="font-size:11px;color:rgba(255,255,255,0.7);margin-top:4px;min-height:16px;"></div>
                </div>
                <script>
                var dates={json.dumps(dates)};
                var highs={json.dumps([round(h,1) if h else None for h in highs])};
                var lows={json.dumps([round(l,1) if l else None for l in lows])};
                var cv=document.getElementById('hist');var ctx=cv.getContext('2d');
                var W=680,H=180,PL=32,PR=10,PT=16,PB=28;var CW=W-PL-PR,CH=H-PT-PB;
                var allV=[...highs,...lows].filter(v=>v!=null);
                var mn=Math.min(...allV)-2,mx=Math.max(...allV)+2,rng=mx-mn||1;
                var N=dates.length;
                function px(i){{return PL+i/(N-1)*CW;}}
                function py(v){{return PT+CH-((v-mn)/rng)*CH;}}
                ctx.beginPath();ctx.moveTo(px(0),py(highs[0]));
                highs.forEach(function(h,i){{if(h!=null)ctx.lineTo(px(i),py(h));}});
                lows.slice().reverse().forEach(function(l,i){{if(l!=null)ctx.lineTo(px(N-1-i),py(l));}});
                ctx.closePath();
                var g=ctx.createLinearGradient(0,PT,0,PT+CH);
                g.addColorStop(0,'rgba(251,146,60,0.35)');g.addColorStop(1,'rgba(96,165,250,0.35)');
                ctx.fillStyle=g;ctx.fill();
                ctx.beginPath();ctx.strokeStyle='#FB923C';ctx.lineWidth=2;
                highs.forEach(function(h,i){{if(h!=null){{i===0?ctx.moveTo(px(i),py(h)):ctx.lineTo(px(i),py(h));}}}});
                ctx.stroke();
                ctx.beginPath();ctx.strokeStyle='#60A5FA';ctx.lineWidth=2;
                lows.forEach(function(l,i){{if(l!=null){{i===0?ctx.moveTo(px(i),py(l)):ctx.lineTo(px(i),py(l));}}}});
                ctx.stroke();
                ctx.fillStyle='rgba(255,255,255,0.5)';ctx.font='9px Outfit';
                for(var i=0;i<N;i+=5){{var d=new Date(dates[i]);var lbl=(d.getMonth()+1)+'/'+(d.getDate());ctx.fillText(lbl,px(i)-8,H-8);}}
                ctx.fillStyle='#FB923C';ctx.fillRect(PL,3,12,5);ctx.fillStyle='rgba(255,255,255,0.6)';ctx.fillText('High',PL+14,9);
                ctx.fillStyle='#60A5FA';ctx.fillRect(PL+55,3,12,5);ctx.fillStyle='rgba(255,255,255,0.6)';ctx.fillText('Low',PL+69,9);
                cv.addEventListener('mousemove',function(e){{
                  var r=cv.getBoundingClientRect();var mx2=(e.clientX-r.left)*(W/r.width);
                  var idx=Math.round((mx2-PL)/CW*(N-1));idx=Math.max(0,Math.min(N-1,idx));
                  if(dates[idx])document.getElementById('hist-tip').textContent=dates[idx]+' → High: '+(highs[idx]||'N/A')+'{unit}   Low: '+(lows[idx]||'N/A')+'{unit}';
                }});
                </script>
                """, height=240)
            except Exception as e:
                st.warning(f"Could not load historical data: {str(e)[:60]}")

def render_change_detector(temp_f, hi_f, lo_f, yest_hi_f, yest_lo_f, feels_f, wind_mph, condition_str, unit):
    alerts = []
    hi_diff = hi_f - yest_hi_f
    if hi_diff <= -10:  alerts.append(f"❄️ Much colder than yesterday — high is {abs(round(hi_diff))}{'°F' if unit=='°F' else '°C'} lower. Bundle up!")
    elif hi_diff >= 10: alerts.append(f"🌡️ Much warmer than yesterday — high is {round(hi_diff)}{'°F' if unit=='°F' else '°C'} higher. Dress light!")
    gap = abs(temp_f - feels_f)
    if gap >= 10: alerts.append(f"⚠️ Big difference between actual and feels-like ({round(gap)}°). {'Wind chill effect.' if feels_f < temp_f else 'Humidity making it feel hotter.'}")
    if wind_mph > 25: alerts.append(f"💨 Very windy today — {round(wind_mph)} mph. Secure loose items outside.")
    cond = condition_str.lower()
    if any(x in cond for x in ["thunder","heavy"]): alerts.append("⛈️ Severe weather conditions — consider rescheduling outdoor plans.")
    if not alerts: alerts.append("✅ Weather conditions are similar to yesterday — no surprises today.")
    st.markdown(f'<div class="ai-box"><div class="box-title">🔔 Weather Change Detector</div>{"<br>".join(alerts)}</div>', unsafe_allow_html=True)

def render_radar(lat, lon, city_name):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🌧️ Live Precipitation Radar</p>', unsafe_allow_html=True)
    components.html(f"""
    <div style="border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.2);">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <div id="radar-map" style="height:320px;width:100%;"></div>
    <script>
    (function(){{
      var map=L.map('radar-map',{{zoomControl:true,scrollWheelZoom:false}}).setView([{lat},{lon}],6);
      L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap',maxZoom:18,opacity:0.6}}).addTo(map);
      var radarLayer=null;
      fetch('https://api.rainviewer.com/public/weather-maps.json')
        .then(r=>r.json()).then(data=>{{
          var frames=data.radar.past;
          var i=0;
          setInterval(function(){{
            if(radarLayer)map.removeLayer(radarLayer);
            var frame=frames[Math.max(0,frames.length-5)+(i%Math.min(5,frames.length))];
            radarLayer=L.tileLayer('https://tilecache.rainviewer.com'+frame.path+'/256/{{z}}/{{x}}/{{y}}/2/1_1.png',{{opacity:0.6}}).addTo(map);
            i++;
          }},600);
        }}).catch(()=>{{
          L.tileLayer('https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid=demo',{{opacity:0.5}}).addTo(map);
        }});
      var icon=L.divIcon({{html:'<div style="font-size:20px;">📍</div>',iconSize:[24,24],className:''}});
      L.marker([{lat},{lon}],{{icon:icon}}).addTo(map).bindPopup('<b>{city_name}</b>').openPopup();
    }})();
    </script></div>
    <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:4px;text-align:center;">Live radar via RainViewer · Animating last 5 frames</div>
    """, height=340)

def render_sleep_forecast(hourly_temps_f, hourly_wind, hour_labels):
    night_temps = [hourly_temps_f[i] for i in range(20, 24)]
    night_winds = [hourly_wind[i]    for i in range(20, 24)]
    avg_t = sum(night_temps) / len(night_temps) if night_temps else 68
    avg_w = sum(night_winds) / len(night_winds) if night_winds else 0
    score = 10
    if avg_t < 60 or avg_t > 72: score -= round(abs(avg_t - 66) / 4)
    if avg_w > 15: score -= 2
    elif avg_w > 8: score -= 1
    score = max(0, min(10, score))
    col = "#4ADE80" if score >= 8 else "#FACC15" if score >= 5 else "#EF4444"
    tips = []
    if avg_t > 72:   tips.append("🔥 Warm night — use a fan or AC for better sleep")
    elif avg_t < 60: tips.append("❄️ Cool night — extra blanket recommended")
    else:            tips.append("✅ Ideal sleeping temperature tonight")
    if avg_w > 15:   tips.append("💨 Windy night — noise may disturb sleep")
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">😴 Sleep Quality Forecast — Tonight</div>
      <div style="display:flex;align-items:center;gap:16px;margin:8px 0;">
        <div style="font-size:48px;font-weight:900;color:{col};">{score}<span style="font-size:18px;">/10</span></div>
        <div>
          <div style="font-size:16px;font-weight:700;color:{col};">{"Excellent" if score>=8 else "Good" if score>=6 else "Fair" if score>=4 else "Poor"} sleeping conditions</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.6);">Tonight avg: {round(avg_t)}°F · Wind: {round(avg_w)} mph</div>
        </div>
      </div>
      <div style="font-size:13px;color:rgba(255,255,255,0.85);">{"<br>".join(tips)}</div>
    </div>""", unsafe_allow_html=True)

def render_gardening_advisor(temp_f, humidity, rain_pct, wind_mph, uv, t_rain):
    tips = []
    should_water = rain_pct < 30 and t_rain < 40 and humidity < 60
    if should_water: tips.append("🚿 Water your plants today — low rain expected")
    else:            tips.append("🌧️ Skip watering — rain expected to do the job")
    if temp_f > 90:  tips.append("🌡️ Extreme heat — water at dawn, not midday")
    if wind_mph > 20: tips.append("💨 High winds — stake tall plants and delay spraying")
    if uv > 7:       tips.append("☀️ High UV — check plants for sunscorch")
    if humidity > 80: tips.append("🍄 High humidity — watch for fungal diseases")
    if temp_f < 32:  tips.append("❄️ Frost risk — cover frost-sensitive plants tonight")
    if not tips:     tips.append("✅ Good gardening conditions — happy planting!")
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">🌱 Gardening Advisor</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.9);line-height:1.8;">{"<br>".join(tips)}</div>
    </div>""", unsafe_allow_html=True)

def render_running_advisor(temp_f, humidity, wind_mph, aqi_text, unit, temp_d):
    try: aqi_num = int(aqi_text.split()[0])
    except: aqi_num = 50
    adjust = 0
    if temp_f > 80:     adjust += (temp_f - 80) * 0.1
    if temp_f < 40:     adjust += (40 - temp_f) * 0.05
    if humidity > 70:   adjust += (humidity - 70) * 0.04
    if wind_mph > 10:   adjust += (wind_mph - 10) * 0.05
    if aqi_num > 100:   adjust += 1.5
    adjusted = 10 + adjust
    adj_min = int(adjusted); adj_sec = round((adjusted - adj_min) * 60)
    col = "#4ADE80" if adjust < 0.5 else "#FACC15" if adjust < 1.5 else "#FB923C" if adjust < 3 else "#EF4444"
    tips = []
    if temp_f > 80:   tips.append("💧 Carry water — risk of dehydration")
    if temp_f < 35:   tips.append("🧤 Warm up indoors first — cold muscles")
    if humidity > 75: tips.append("💦 High humidity — sweat less efficient, slow down")
    if wind_mph > 15: tips.append("🌬️ Run into wind first half — tailwind on the way back")
    if aqi_num > 100: tips.append("😷 Poor air quality — wear a mask or run indoors")
    if not tips:      tips.append("✅ Great running conditions!")
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">🏃 Running Pace Advisor</div>
      <div style="display:flex;align-items:center;gap:20px;margin:10px 0;flex-wrap:wrap;">
        <div style="text-align:center;"><div style="font-size:10px;color:rgba(255,255,255,0.5);">BASE PACE</div>
          <div style="font-size:24px;font-weight:700;color:white;">10:00<span style="font-size:12px;">/mi</span></div></div>
        <div style="font-size:24px;color:rgba(255,255,255,0.4);">→</div>
        <div style="text-align:center;"><div style="font-size:10px;color:rgba(255,255,255,0.5);">ADJUSTED</div>
          <div style="font-size:24px;font-weight:700;color:{col};">{adj_min}:{adj_sec:02d}<span style="font-size:12px;">/mi</span></div></div>
        <div style="font-size:12px;color:{col};">+{adjust:.1f} min added by weather</div>
      </div>
      <div style="font-size:13px;color:rgba(255,255,255,0.8);">{"<br>".join(tips)}</div>
    </div>""", unsafe_allow_html=True)

def render_windows_advisor(temp_f, aqi_text, grass_pollen, tree_pollen, wind_mph, condition_str):
    try: aqi_num = int(aqi_text.split()[0])
    except: aqi_num = 50
    cond = condition_str.lower()
    reasons_yes = []; reasons_no = []
    if 60 <= temp_f <= 80:  reasons_yes.append("🌡️ Perfect temperature for fresh air")
    else:                   reasons_no.append(f"🌡️ {'Too cold' if temp_f<60 else 'Too hot'} — AC/heat more efficient")
    if aqi_num <= 50:       reasons_yes.append("💨 Air quality is excellent outdoors")
    elif aqi_num <= 100:    reasons_no.append("💨 Moderate AQI — filtered air preferable")
    else:                   reasons_no.append(f"💨 Poor air quality (AQI {aqi_num}) — keep closed")
    if grass_pollen and grass_pollen > 50: reasons_no.append("🌾 High grass pollen — allergy risk")
    if tree_pollen  and tree_pollen  > 90: reasons_no.append("🌳 High tree pollen — allergy risk")
    if any(x in cond for x in ["rain","thunder","snow"]): reasons_no.append("🌧️ Precipitation — keep closed")
    if wind_mph > 20: reasons_no.append(f"💨 Very windy ({round(wind_mph)} mph) — may cause drafts")
    open_it = len(reasons_yes) > len(reasons_no)
    verdict = "✅ Yes — open your windows!" if open_it else "❌ No — keep them closed"
    col     = "#4ADE80" if open_it else "#EF4444"
    all_reasons = [f"✅ {r}" for r in reasons_yes] + [f"❌ {r}" for r in reasons_no]
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">🪟 Should I Open My Windows?</div>
      <div style="font-size:20px;font-weight:700;color:{col};margin:8px 0;">{verdict}</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.8);">{"<br>".join(all_reasons)}</div>
    </div>""", unsafe_allow_html=True)

def render_allergy_alert(grass_pollen, tree_pollen, aqi_text, wind_mph):
    try: aqi_num = int(aqi_text.split()[0])
    except: aqi_num = 50
    score = 0
    if grass_pollen:
        if grass_pollen > 200:  score += 4
        elif grass_pollen > 50: score += 2
        elif grass_pollen > 10: score += 1
    if tree_pollen:
        if tree_pollen > 1500:  score += 4
        elif tree_pollen > 90:  score += 2
        elif tree_pollen > 15:  score += 1
    if aqi_num > 150:   score += 3
    elif aqi_num > 100: score += 2
    elif aqi_num > 50:  score += 1
    if wind_mph > 20:   score += 2
    elif wind_mph > 10: score += 1
    score = min(10, score)
    col = "#4ADE80" if score<=2 else "#FACC15" if score<=4 else "#FB923C" if score<=7 else "#EF4444"
    lbl = "Low" if score<=2 else "Moderate" if score<=4 else "High" if score<=7 else "Very High"
    advice = []
    if score >= 3: advice.append("💊 Consider taking antihistamines before going outside")
    if score >= 5: advice.append("🕶️ Wear wraparound sunglasses to protect eyes")
    if score >= 5: advice.append("🚿 Shower after outdoor activity to remove pollen")
    if score >= 7: advice.append("😷 Consider wearing an N95 mask outdoors")
    if score >= 8: advice.append("🏠 Limit time outside — stay indoors if possible")
    if not advice: advice.append("✅ Low allergy risk — enjoy the outdoors!")
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">🌿 Allergy Alert Score</div>
      <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-size:48px;font-weight:900;color:{col};">{score}<span style="font-size:20px;">/10</span></div>
        <div><div style="font-size:16px;font-weight:700;color:{col};">{lbl} Risk</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.6);">Pollen + AQI + Wind combined score</div></div>
      </div>
      <div style="margin-top:10px;font-size:13px;color:rgba(255,255,255,0.85);">{"<br>".join(advice)}</div>
    </div>""", unsafe_allow_html=True)

def render_best_day(daily_f, daily_d, unit):
    try:
        best_score = -999; best_i = 1
        for i in range(1, min(8, len(daily_f["temperature_2m_max"]))):
            hi = daily_f["temperature_2m_max"][i]; lo = daily_f["temperature_2m_min"][i]
            rain = daily_f.get("precipitation_probability_max", [50]*8)[i]
            score = (100 - abs((hi+lo)/2 - 68) * 2) - rain * 0.8
            if score > best_score: best_score = score; best_i = i
        d = datetime.strptime(daily_f["time"][best_i], "%Y-%m-%d")
        lbl = "Today" if best_i == 1 else d.strftime("%A, %B %d")
        hi_d = round(daily_d["temperature_2m_max"][best_i]); lo_d = round(daily_d["temperature_2m_min"][best_i])
        rain = daily_f.get("precipitation_probability_max",[0]*8)[best_i]
        icon = WMO_CODES.get(daily_f["weather_code"][best_i],"🌡️").split()[0]
        st.markdown(f"""<div class="glass-card" style="border:1px solid rgba(74,222,128,0.4);">
          <div class="box-title">🏆 Best Day This Week for Outdoors</div>
          <div style="display:flex;align-items:center;gap:16px;margin-top:8px;">
            <div style="font-size:48px;">{icon}</div>
            <div><div style="font-size:18px;font-weight:700;color:#4ADE80;">{lbl}</div>
              <div style="font-size:14px;color:rgba(255,255,255,0.8);">{hi_d}/{lo_d}{unit} · 🌧️ {rain}% rain</div>
              <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:4px;">Score: {round(best_score)}/100</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    except: pass

def render_confidence_badges(daily_f):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🎯 Forecast Confidence</p>', unsafe_allow_html=True)
    html = '<div style="display:flex;gap:6px;flex-wrap:wrap;">'
    for i in range(min(7, len(daily_f.get("time", [])))):
        idx = i + 1
        try:
            d = datetime.strptime(daily_f["time"][idx], "%Y-%m-%d")
            lbl = "Today" if i == 0 else d.strftime("%a")
        except: lbl = f"Day {i}"
        conf = forecast_confidence(i)
        col = "#4ADE80" if conf >= 85 else "#FACC15" if conf >= 65 else "#FB923C" if conf >= 45 else "#EF4444"
        html += (f'<div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.15);border-radius:10px;'
                 f'padding:8px 12px;text-align:center;min-width:60px;">'
                 f'<div style="font-size:10px;color:rgba(255,255,255,0.6);">{lbl}</div>'
                 f'<div style="font-size:18px;font-weight:700;color:{col};">{conf}%</div>'
                 f'<div style="font-size:9px;color:{col};">{"High" if conf>=85 else "Good" if conf>=65 else "Fair" if conf>=45 else "Low"}</div></div>')
    html += '</div>'
    st.markdown(f'<div class="glass-card">{html}</div>', unsafe_allow_html=True)

def render_stats_summary(temp_f, humidity, wind_mph, uv, rain_pct, aqi_text, fgi, unit, temp_d, feels_d):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">📊 Complete Weather Stats</p>', unsafe_allow_html=True)
    def rate(val, low_bad, low_ok, hi_ok, hi_bad):
        if val <= low_bad or val >= hi_bad: return "🔴"
        if val <= low_ok  or val >= hi_ok:  return "🟡"
        return "🟢"
    stats = [
        ("🌡️ Temperature", f"{round(temp_d)}{unit}",   rate(temp_f, 32, 50, 85, 100)),
        ("🥵 Feels Like",  f"{round(feels_d)}{unit}",  rate(temp_f, 32, 50, 85, 100)),
        ("💧 Humidity",    f"{humidity}%",              rate(humidity, 20, 30, 60, 80)),
        ("💨 Wind Speed",  f"{round(wind_mph)} mph",   rate(wind_mph, 0, 0, 15, 30)),
        ("🌧️ Rain Chance", f"{rain_pct}%",             rate(rain_pct, 0, 0, 30, 70)),
        ("🌞 UV Index",    f"{round(uv)}/11",           rate(uv, 0, 0, 5, 8)),
        ("😊 Feel-Good",   f"{fgi}/100",                rate(100 - fgi, 0, 0, 30, 60)),
        ("💨 Air Quality", aqi_text.split()[0] if aqi_text != "N/A" else "N/A",
         "🟢" if "Good" in aqi_text else "🟡" if "Moderate" in aqi_text else "🔴"),
    ]
    html = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px;">'
    for label, val, dot in stats:
        html += (f'<div class="glass-card" style="padding:10px 12px;">'
                 f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                 f'<span style="font-size:12px;color:rgba(255,255,255,0.7);">{label}</span><span>{dot}</span></div>'
                 f'<div style="font-size:18px;font-weight:700;color:white;margin-top:4px;">{val}</div></div>')
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_qr_code(city_name):
    city_encoded = urllib.parse.quote(city_name)
    qr_url = f"https://quickchart.io/qr?text=NimbusAI%20weather%20for%20{city_encoded}&size=180&dark=ffffff&light=00000000"
    st.markdown(f"""<div class="glass-card" style="text-align:center;">
      <div class="box-title">📱 QR Code — Share This City's Weather</div>
      <img src="{qr_url}" style="width:150px;height:150px;margin:10px auto;display:block;border-radius:10px;background:rgba(255,255,255,0.1);padding:8px;" alt="QR Code for {city_name}"/>
      <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:6px;">Scan to open NimbusAI for {city_name}</div>
    </div>""", unsafe_allow_html=True)

def render_tweet_copy(city_name, temp_d, unit, condition_str, hi_d, lo_d, fgi, fgi_lbl):
    tweet = (f"Today in {city_name}: {condition_str} 🌡️ {round(temp_d)}{unit} "
             f"(H:{hi_d} L:{lo_d}) 😊 Feel-Good: {fgi}/100 — {fgi_lbl} "
             f"via #NimbusAI 🌤️")
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">🐦 Share on Twitter / X</div>
      <div style="font-size:13px;color:white;margin-bottom:10px;">{tweet}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button onclick="navigator.clipboard.writeText(`{tweet}`).then(()=>{{this.innerText='✅ Copied!';setTimeout(()=>this.innerText='📋 Copy Tweet',2000)}})"
          style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.3);border-radius:10px;
                 color:white;font-family:Outfit,sans-serif;font-size:12px;font-weight:600;padding:6px 16px;cursor:pointer;">
          📋 Copy Tweet</button>
        <a href="https://twitter.com/intent/tweet?text={tweet.replace(' ','%20').replace('#','%23')}"
           target="_blank"
           style="display:inline-block;background:#1DA1F2;color:white;text-decoration:none;
                  border-radius:10px;padding:6px 16px;font-size:12px;font-weight:600;">
          𝕏 Open in Twitter</a>
      </div>
    </div>""", unsafe_allow_html=True)

def render_friends_weather(unit):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">👥 Friends\' Weather</p>', unsafe_allow_html=True)
    with st.expander("See where your friends are and what weather they have"):
        if "friends" not in st.session_state: st.session_state.friends = []
        c1, c2 = st.columns([3,1])
        with c1: new_friend = st.text_input("", placeholder="Friend's city...", key="friend_inp", label_visibility="collapsed")
        with c2:
            if st.button("+ Add", key="add_friend") and new_friend.strip():
                if new_friend.strip() not in st.session_state.friends and len(st.session_state.friends) < 6:
                    st.session_state.friends.append(new_friend.strip()); st.rerun()
        if st.session_state.friends:
            if st.button("🌍 Fetch all friends' weather", key="fetch_friends"):
                st.session_state.friends_data = []
                with st.spinner("Fetching..."):
                    for city in st.session_state.friends:
                        try:
                            res = fetch_weather(city, unit)
                            if res[0]:
                                wx, wd, _, meta = res
                                cur = wx["current"]; curd = wd["current"]
                                fgi_v, fgi_l, fgi_c = feel_good_index(cur["temperature_2m"], cur["relative_humidity_2m"], cur["wind_speed_10m"])
                                st.session_state.friends_data.append({
                                    "city": meta["name"], "country": meta["country"],
                                    "temp": round(curd["temperature_2m"]),
                                    "cond": WMO_CODES.get(cur["weather_code"],"🌡️"),
                                    "fgi": fgi_v, "fgi_col": fgi_c,
                                    "rain": cur.get("precipitation_probability",0)
                                })
                        except: pass
            cols_f = st.columns(min(len(st.session_state.friends), 3))
            for i, city in enumerate(st.session_state.friends):
                with cols_f[i % 3]:
                    st.markdown(f'<div class="chip">📍 {city}</div>', unsafe_allow_html=True)
                    if st.button("✕", key=f"rm_friend_{i}"):
                        st.session_state.friends.pop(i); st.rerun()
            if "friends_data" in st.session_state and st.session_state.friends_data:
                cols_d = st.columns(min(len(st.session_state.friends_data), 3))
                for i, fd in enumerate(st.session_state.friends_data):
                    with cols_d[i % 3]:
                        icon = fd["cond"].split()[0]
                        st.markdown(f"""<div class="glass-card" style="text-align:center;padding:10px;">
                          <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.7);">{fd['city']}, {fd['country']}</div>
                          <div style="font-size:28px;margin:4px 0;">{icon}</div>
                          <div style="font-size:22px;font-weight:900;color:white;">{fd['temp']}{unit}</div>
                          <div style="font-size:11px;color:{fd['fgi_col']};">😊 {fd['fgi']}/100</div>
                          <div style="font-size:10px;color:rgba(255,255,255,0.5);">🌧️{fd['rain']}%</div>
                        </div>""", unsafe_allow_html=True)

def render_time_capsule(city_name, temp_d, unit, condition_str, fgi):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">⏳ Weather Time Capsule</p>', unsafe_allow_html=True)
    if "capsule" not in st.session_state: st.session_state.capsule = []
    with st.expander("📬 Seal a weather memory for future you"):
        msg = st.text_area("Write a message to your future self about today's weather:", height=80, key="capsule_msg",
                           placeholder="e.g. It's a perfect sunny day — I walked to the park and had lunch outside!")
        if st.button("📦 Seal Time Capsule", key="seal_capsule") and msg.strip():
            entry = {"sealed": datetime.now().strftime("%B %d, %Y"), "city": city_name,
                     "temp": f"{round(temp_d)}{unit}", "cond": condition_str, "fgi": fgi, "msg": msg,
                     "open_on": (datetime.now() + timedelta(days=365)).strftime("%B %d, %Y")}
            st.session_state.capsule.insert(0, entry)
            st.session_state.capsule = st.session_state.capsule[:10]
            st.success(f"✅ Sealed! You can open this on {entry['open_on']}")
    if st.session_state.capsule:
        for cap in st.session_state.capsule[:3]:
            st.markdown(f"""<div class="glass-card">
              <div style="display:flex;justify-content:space-between;font-size:11px;color:rgba(255,255,255,0.5);">
                <span>📦 Sealed {cap['sealed']} · {cap['city']} · {cap['temp']} · {cap['cond']}</span>
                <span>Open: {cap['open_on']}</span>
              </div>
              <div style="font-size:13px;color:white;margin-top:6px;font-style:italic;">"{cap['msg']}"</div>
            </div>""", unsafe_allow_html=True)

def render_currency_weather(unit):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">💱 Travel: Currency + Weather</p>', unsafe_allow_html=True)
    with st.expander("Check currency rate for your destination"):
        c1, c2, c3 = st.columns(3)
        currencies = ["USD","EUR","GBP","JPY","AUD","CAD","CHF","CNY","INR","MXN","SGD","HKD","NOK","SEK","DKK","NZD","KRW","BRL","ZAR","AED"]
        with c1: dest_city = st.text_input("Destination city", placeholder="e.g. Tokyo", key="curr_city")
        with c2: from_curr = st.selectbox("Your currency", currencies, key="from_curr")
        with c3: to_curr   = st.selectbox("Their currency", currencies, index=3, key="to_curr")
        if st.button("🔍 Check", key="curr_go") and dest_city.strip():
            with st.spinner("Fetching weather + currency..."):
                wx_result = fetch_weather(dest_city.strip(), unit)
                curr_data = None
                try:
                    r2 = requests.get(f"https://api.frankfurter.dev/v2/rates?base={from_curr}&quotes={to_curr}", timeout=6)
                    curr_data = r2.json()
                except: pass
                if wx_result[0]:
                    wx_f2, wx_d2, _, meta2 = wx_result
                    cur2 = wx_f2["current"]; curd2 = wx_d2["current"]
                    t2 = round(curd2["temperature_2m"]); cond2 = WMO_CODES.get(cur2["weather_code"],"🌡️")
                    icon2 = cond2.split()[0]
                    rate_str = "N/A"
                    if curr_data and "rates" in curr_data:
                        rate = curr_data["rates"].get(to_curr)
                        if rate: rate_str = f"1 {from_curr} = {rate:.4f} {to_curr}"
                    st.markdown(f"""<div class="ai-box">
                      <div class="box-title">✈️ {meta2['name']}, {meta2['country']}</div>
                      <div style="display:flex;gap:24px;flex-wrap:wrap;margin-top:8px;">
                        <div><div style="font-size:11px;color:rgba(255,255,255,0.5);">Weather</div>
                          <div style="font-size:22px;font-weight:700;color:white;">{icon2} {t2}{unit}</div>
                          <div style="font-size:13px;color:rgba(255,255,255,0.7);">{cond2}</div></div>
                        <div><div style="font-size:11px;color:rgba(255,255,255,0.5);">Exchange Rate</div>
                          <div style="font-size:18px;font-weight:700;color:#4ADE80;">{rate_str}</div>
                          <div style="font-size:10px;color:rgba(255,255,255,0.4);">Via ECB daily rate</div></div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.error("City not found")

def render_print_report(city_name, country, temp_d, unit, condition_str,
                        hi_d, lo_d, humidity, wind_mph, wind_dir_str,
                        rain_pct, uv, aqi_text, sr_fmt, ss_fmt, fgi, fgi_lbl):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🖨️ Print Weather Report</p>', unsafe_allow_html=True)
    with st.expander("Generate printable daily report"):
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        components.html(f"""
        <style>
        body {{ margin:0;font-family:Georgia,serif;background:white;color:#1a1a2e; }}
        .report {{ max-width:600px;margin:0 auto;padding:24px;border:2px solid #1a6eff;border-radius:12px; }}
        .header {{ text-align:center;border-bottom:1px solid #ddd;padding-bottom:16px;margin-bottom:16px; }}
        .title {{ font-size:24px;font-weight:bold;color:#1a6eff; }}
        .date {{ font-size:13px;color:#666;margin-top:4px; }}
        .temp {{ font-size:48px;font-weight:900;color:#1a1a2e;text-align:center;margin:16px 0 8px; }}
        .cond {{ text-align:center;font-size:16px;color:#444;margin-bottom:16px; }}
        .grid {{ display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:16px 0; }}
        .stat {{ background:#f8f9ff;border-radius:8px;padding:10px;text-align:center; }}
        .stat-label {{ font-size:10px;color:#888;text-transform:uppercase;letter-spacing:0.1em; }}
        .stat-val {{ font-size:18px;font-weight:bold;color:#1a1a2e;margin-top:4px; }}
        .footer {{ text-align:center;font-size:11px;color:#aaa;margin-top:16px;border-top:1px solid #eee;padding-top:12px; }}
        .print-btn {{ background:#1a6eff;color:white;border:none;border-radius:8px;padding:10px 24px;
                      font-size:14px;font-weight:600;cursor:pointer;display:block;margin:16px auto 0; }}
        @media print {{ .print-btn {{ display:none; }} }}
        </style>
        <div class="report">
          <div class="header"><div class="title">🌤️ NimbusAI Daily Weather Report</div>
            <div class="date">📍 {city_name}, {country} · {date_str}</div></div>
          <div class="temp">{round(temp_d)}{unit}</div>
          <div class="cond">{condition_str}</div>
          <div class="grid">
            <div class="stat"><div class="stat-label">🔴 High</div><div class="stat-val">{hi_d}{unit}</div></div>
            <div class="stat"><div class="stat-label">🔵 Low</div><div class="stat-val">{lo_d}{unit}</div></div>
            <div class="stat"><div class="stat-label">💧 Humidity</div><div class="stat-val">{humidity}%</div></div>
            <div class="stat"><div class="stat-label">💨 Wind</div><div class="stat-val">{round(wind_mph)} mph {wind_dir_str}</div></div>
            <div class="stat"><div class="stat-label">🌧️ Rain Chance</div><div class="stat-val">{rain_pct}%</div></div>
            <div class="stat"><div class="stat-label">🌞 UV Index</div><div class="stat-val">{round(uv)}/11</div></div>
            <div class="stat"><div class="stat-label">💨 Air Quality</div><div class="stat-val">{aqi_text.split()[0] if aqi_text!='N/A' else 'N/A'}</div></div>
            <div class="stat"><div class="stat-label">🌅 Sunrise</div><div class="stat-val">{sr_fmt}</div></div>
            <div class="stat"><div class="stat-label">🌇 Sunset</div><div class="stat-val">{ss_fmt}</div></div>
          </div>
          <div class="stat" style="text-align:center;"><div class="stat-label">😊 Feel-Good Index</div>
            <div class="stat-val">{fgi}/100 — {fgi_lbl}</div></div>
          <div class="footer">Generated by NimbusAI · {date_str} · Open-Meteo API</div>
          <button class="print-btn" onclick="window.print()">🖨️ Print This Report</button>
        </div>
        """, height=620)

def inject_pwa():
    st.markdown("""
    <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiTmltYnVzQUkiLCJzaG9ydF9uYW1lIjoiTmltYnVzIiwic3RhcnRfdXJsIjoiLyIsImRpc3BsYXkiOiJzdGFuZGFsb25lIiwiYmFja2dyb3VuZF9jb2xvciI6IiMxYTZlZmYiLCJ0aGVtZV9jb2xvciI6IiMxYTZlZmYifQ==">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="NimbusAI">
    <meta name="theme-color" content="#1a6eff">
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# THEME + SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

THEMES = {
    "Default":  "linear-gradient(160deg,#020617,#0f172a,#1e293b)",
    "Cyberpunk":"linear-gradient(160deg,#1a0030,#3333ff,#00ffee)",
    "Sunset":   "linear-gradient(160deg,#1a0a05,#ff5e62,#ffcc70)",
    "Ocean":    "linear-gradient(160deg,#0a1628,#2193b0,#38bdf8)",
    "Midnight": "linear-gradient(160deg,#000000,#0f172a,#020617)",
}

for k, v in [("history",[]), ("city_input",""), ("dark_mode",False),
             ("last_updated",None), ("outfit_memory",{})]:
    if k not in st.session_state:
        st.session_state[k] = v


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER & CONTROLS
# ═══════════════════════════════════════════════════════════════════════════════

col_h1, col_h2, col_h3 = st.columns([4, 2, 1])
with col_h1:
    st.markdown('<p style="font-size:28px;font-weight:900;color:white;margin:0 0 4px;letter-spacing:-1px;">🌤️ NimbusAI</p>', unsafe_allow_html=True)
with col_h2:
    theme = st.selectbox("", list(THEMES.keys()), key="theme_sel", label_visibility="collapsed")
with col_h3:
    st.session_state.dark_mode = st.toggle("🌙", value=st.session_state.dark_mode, help="Dark mode")

# Apply theme & base CSS
bg_gradient = THEMES[theme]
inject_base_css(bg_gradient)
if st.session_state.dark_mode:
    st.markdown("<style>.stApp{filter:brightness(0.55) saturate(0.7) !important;}</style>", unsafe_allow_html=True)

unit = st.radio("", ["°F","°C"], horizontal=True, label_visibility="collapsed")

# Geolocation button
components.html("""
<div style="margin-bottom:10px;">
  <button onclick="getLocation()" id="geo-btn" style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.35);
    border-radius:12px;color:white;font-family:Outfit,sans-serif;font-size:13px;font-weight:600;
    padding:6px 16px;cursor:pointer;">📍 Use My Location</button>
  <span id="gs" style="color:rgba(255,255,255,0.6);font-size:12px;margin-left:10px;"></span>
</div>
<script>
function setCity(name){
  var inputs=window.parent.document.querySelectorAll('input[type="text"]');
  for(var inp of inputs){
    var label=inp.closest('[data-testid="stTextInput"]');
    if(label){var nv=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value');
      nv.set.call(inp,name);inp.dispatchEvent(new Event('input',{bubbles:true}));break;}
  }
}
function getLocation(){
  var btn=document.getElementById('geo-btn'),gs=document.getElementById('gs');
  btn.disabled=true;btn.innerText='⏳ Detecting…';gs.innerText='';
  navigator.geolocation.getCurrentPosition(function(p){
    gs.innerText='📡 Looking up city…';
    fetch('https://api.bigdatacloud.net/data/reverse-geocode-client?latitude='+p.coords.latitude+'&longitude='+p.coords.longitude+'&localityLanguage=en')
    .then(r=>r.json()).then(d=>{
      var city=d.city||d.locality||d.principalSubdivision||'';
      if(city){gs.innerText='✅ '+city;setCity(city);}else{gs.innerText='⚠️ Could not find city name';}
      btn.innerText='📍 Use My Location';btn.disabled=false;
    }).catch(function(){gs.innerText='⚠️ Lookup failed';btn.innerText='📍 Use My Location';btn.disabled=false;});
  },function(err){
    gs.innerText=err.code===1?'❌ Permission denied':'❌ Could not detect location';
    btn.innerText='📍 Use My Location';btn.disabled=false;
  },{enableHighAccuracy:false,timeout:5000,maximumAge:60000});
}
</script>""", height=60)

# Recent history chips
if st.session_state.history:
    st.markdown(
        '<div class="chip-row">' +
        ''.join(f'<span class="chip">🕐 {c}</span>' for c in st.session_state.history) +
        '</div>',
        unsafe_allow_html=True
    )

# City input
saved_city = st.query_params.get("city", "")
city_typed = st.text_input(
    "",
    placeholder="Search a city...",
    label_visibility="collapsed",
    value=st.session_state.get("city_input", saved_city),
    key="main_city_input"
)
if city_typed.strip():
    try: st.query_params["city"] = city_typed.strip()
    except: pass

fetch_city = city_typed.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN WEATHER DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

if fetch_city:
    st.markdown(SKELETON_CSS, unsafe_allow_html=True)
    with st.spinner("Fetching real weather..."):
        result, from_cache = get_cached_or_fetch(fetch_city, unit)
        if from_cache:
            st.markdown('<div style="font-size:10px;color:rgba(255,255,255,0.4);text-align:right;">⚡ Loaded from cache</div>', unsafe_allow_html=True)
        if result[0] is None:
            st.error("❌ City not found! Try a different spelling.")
            st.stop()

        wx_f, wx_display, aq, meta = result
        lat, lon, city_name, country = meta["lat"], meta["lon"], meta["name"], meta["country"]

        # AQ data
        aqi        = aq.get("current",{}).get("us_aqi", None)
        pm25       = aq.get("current",{}).get("pm2_5", None)
        grass_pollen = aq.get("current",{}).get("grass_pollen", None)
        tree_pollen  = aq.get("current",{}).get("tree_pollen", None)

        # Current conditions
        cur_f = wx_f["current"]; cur_d = wx_display["current"]
        daily_f = wx_f["daily"]; daily_d = wx_display["daily"]
        temp_f   = cur_f["temperature_2m"]; feels_f = cur_f["apparent_temperature"]
        wind_mph = cur_f["wind_speed_10m"]; gusts_mph = cur_f.get("wind_gusts_10m", wind_mph)
        wind_deg = cur_f.get("wind_direction_10m", None)
        code     = cur_f["weather_code"]; humidity = cur_f["relative_humidity_2m"]
        rain_pct = cur_f.get("precipitation_probability", 0); uv = cur_f.get("uv_index", 0)
        vis_m    = cur_f.get("visibility", None); vis_km = round(vis_m / 1000, 1) if vis_m else None
        condition_str = WMO_CODES.get(code, "Unknown"); wind_dir_str = wind_dir_label(wind_deg)
        temp_d   = cur_d["temperature_2m"]; feels_d = cur_d["apparent_temperature"]

        # Daily data
        hi_d = round(daily_d["temperature_2m_max"][1]); lo_d = round(daily_d["temperature_2m_min"][1])
        hi_f_val  = daily_f["temperature_2m_max"][1];   lo_f_val  = daily_f["temperature_2m_min"][1]
        yest_hi_f = daily_f["temperature_2m_max"][0];   yest_lo_f = daily_f["temperature_2m_min"][0]
        yest_rain = daily_f.get("precipitation_probability_max",[0]*7)[0]
        t_rain_arr = daily_f.get("precipitation_probability_max",[rain_pct]*7)
        t_code = daily_f["weather_code"][2] if len(daily_f["weather_code"]) > 2 else code
        t_hi_f = daily_f["temperature_2m_max"][2] if len(daily_f["temperature_2m_max"]) > 2 else hi_f_val
        t_rain = t_rain_arr[2] if len(t_rain_arr) > 2 else rain_pct
        t_hi_d = round(daily_d["temperature_2m_max"][2]) if len(daily_d.get("temperature_2m_max",[])) > 2 else hi_d
        t_lo_d = round(daily_d["temperature_2m_min"][2]) if len(daily_d.get("temperature_2m_min",[])) > 2 else lo_d

        # Sunrise / sunset
        try:
            sr_raw = daily_f.get("sunrise",["",""])[1]; ss_raw = daily_f.get("sunset",["",""])[1]
            sr_fmt = datetime.strptime(sr_raw, "%Y-%m-%dT%H:%M").strftime("%I:%M %p")
            ss_fmt = datetime.strptime(ss_raw, "%Y-%m-%dT%H:%M").strftime("%I:%M %p")
        except: sr_fmt, ss_fmt = "N/A", "N/A"

        # Timezone & hourly
        tz_str    = wx_f.get("timezone","UTC"); local_now = datetime.now(ZoneInfo(tz_str)); now_h = local_now.hour
        h_slice   = slice(24, 48)
        hourly_temps_f  = wx_f["hourly"]["temperature_2m"][h_slice]
        hourly_temps_d  = wx_display["hourly"]["temperature_2m"][h_slice]
        hourly_feels_d  = wx_display["hourly"].get("apparent_temperature", wx_display["hourly"]["temperature_2m"])[h_slice]
        hourly_rain_vals = wx_f["hourly"]["precipitation_probability"][h_slice]
        hourly_wind      = wx_f["hourly"]["wind_speed_10m"][h_slice]
        hourly_times     = wx_f["hourly"]["time"][h_slice]
        hourly_uv_all    = wx_f["hourly"].get("uv_index", [0]*48)
        hourly_uv_today  = hourly_uv_all[24:48] if len(hourly_uv_all) >= 48 else hourly_uv_all[:24]
        hour_labels = [datetime.strptime(t, "%Y-%m-%dT%H:%M").strftime("%-I%p").lower() for t in hourly_times]
        week_hi_f = daily_f["temperature_2m_max"][1:7]; week_hi_d = daily_d["temperature_2m_max"][1:7]

        # Computed values
        best_i, best_window_str = best_outdoor_window(hourly_temps_f, hourly_rain_vals, hourly_wind, hour_labels)
        yesterday_change = what_changed_yesterday(hi_f_val, lo_f_val, t_rain_arr[1] if len(t_rain_arr) > 1 else rain_pct,
                                                  yest_hi_f, yest_lo_f, yest_rain, unit)
        fgi, fgi_lbl, fgi_col = feel_good_index(temp_f, humidity, wind_mph)
        moon_icon, moon_name   = get_moon_phase(datetime.now())
        aqi_text, aqi_color    = aqi_label(aqi)
        sky_bg = sky_class(code)

        # Update history + session state
        st.session_state.last_updated = local_now.strftime("%I:%M %p")
        if city_name not in st.session_state.history:
            st.session_state.history.insert(0, city_name)
        st.session_state.history = st.session_state.history[:6]
        st.session_state["preferred_unit"] = unit

        # Inject animated background canvas
        components.html(make_particles(sky_bg), height=0, scrolling=False)

        alt_t  = f"/ {to_c(temp_f)}°C"  if unit == "°F" else f"/ {to_f(temp_d)}°F"
        alt_f2 = f"/ {to_c(feels_f)}°C" if unit == "°F" else f"/ {to_f(feels_d)}°F"

        # ── HERO CARD ──────────────────────────────────────────────────────────
        st.markdown(f"""<div class="hero-card main-content">
          <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px;">
            <span style="font-size:32px;font-weight:800;color:white;letter-spacing:-1px;">{local_now.strftime("%I:%M %p")}</span>
            <span style="font-size:13px;color:rgba(255,255,255,0.6);">{local_now.strftime("%a, %b %d")}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.4);margin-left:auto;">Updated {st.session_state.last_updated}</span>
          </div>
          <div class="hero-city">📍 {city_name}, {country}</div>
          <div class="hero-cond" style="display:flex;align-items:center;gap:10px;">{animated_weather_icon(code,40)}<span>{condition_str}</span></div>
          <div style="display:flex;align-items:flex-end;gap:16px;margin-top:8px;flex-wrap:wrap;">
            <div>
              <div class="hero-temp">{round(temp_d)}{unit}</div>
              <div style="font-size:14px;color:rgba(255,255,255,0.55);">{alt_t}</div>
            </div>
            <div style="padding-bottom:10px;">
              <div style="font-size:14px;color:rgba(255,255,255,0.7);margin-top:4px;">Feels like {round(feels_d)}{unit} <span style="font-size:12px;color:rgba(255,255,255,0.5);">{alt_f2}</span></div>
              <div><span class="hilo-badge">🔴 {hi_d}{unit}</span><span class="hilo-badge">🔵 {lo_d}{unit}</span></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        rc1, rc2 = st.columns([1, 5])
        with rc1:
            if st.button("🔄 Refresh"): st.rerun()

        # Severe weather alert
        if code in SEVERE_CODES:
            st.markdown(f'<div class="warn-box"><strong>⚠️ SEVERE WEATHER ALERT</strong><br>{SEVERE_MESSAGES.get(code,"Stay safe!")}</div>', unsafe_allow_html=True)

        # Quick summary cards
        st.markdown(f'<div class="info-box"><div class="box-title">📅 What Changed Since Yesterday</div>{yesterday_change}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-box"><div class="box-title">🌟 Best Time to Go Outside</div>{best_window_str}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-box"><div class="box-title">✨ Weather Summary</div>{ai_comment(temp_f, condition_str, wind_mph)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card"><div class="box-title">🌡️ Why Does It Feel Like That?</div><div style="font-size:14px;color:white;">{feels_like_reason(temp_f, humidity, wind_mph)}</div></div>', unsafe_allow_html=True)

        # Tomorrow preview
        t_icon = WMO_CODES.get(t_code,"🌡️").split()[0]; t_cond_str = WMO_CODES.get(t_code,"Unknown")
        t_alt_hi = f"/ {to_c(round(t_hi_f))}°C" if unit=="°F" else f"/ {to_f(t_hi_d)}°F"
        st.markdown(f"""<div class="tomorrow-card">
          <div class="box-title">📅 Tomorrow's Preview</div>
          <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
            <div style="font-size:40px;">{t_icon}</div>
            <div>
              <div style="font-size:16px;font-weight:700;color:white;">{t_cond_str}</div>
              <div style="font-size:14px;color:rgba(255,255,255,0.75);">High {t_hi_d}{unit} <span style="font-size:12px;opacity:0.6;">{t_alt_hi}</span> · Low {t_lo_d}{unit}</div>
              <div style="font-size:13px;color:rgba(255,255,255,0.65);margin-top:4px;">🌧️ {t_rain}% rain chance</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Share button
        share_text = (f"📍 {city_name}, {country} — {condition_str}\\n"
                      f"🌡️ {round(temp_d)}{unit} (feels {round(feels_d)}{unit})\\n"
                      f"🔴 High {hi_d}{unit}  🔵 Low {lo_d}{unit}\\n"
                      f"💧 {humidity}% humidity  💨 {round(wind_mph)} mph {wind_dir_str}\\n"
                      f"🌧️ {rain_pct}% rain  🌞 UV {round(uv)}\\n"
                      f"Shared via NimbusAI 🌤️")
        st.markdown(f"""<button onclick="navigator.clipboard.writeText('{share_text}').then(()=>{{this.innerText='✅ Copied!';setTimeout(()=>this.innerText='📋 Share Weather',2000)}})"
          style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.35);border-radius:12px;
                 color:white;font-family:Outfit,sans-serif;font-size:13px;font-weight:600;
                 padding:8px 20px;cursor:pointer;margin-bottom:14px;">📋 Share Weather</button>""", unsafe_allow_html=True)

        # Outfit
        wear_items = what_to_wear(temp_f, condition_str, wind_mph); svg_fig = outfit_svg(temp_f, condition_str)
        wc1, wc2 = st.columns([1, 2])
        with wc1: st.markdown(f'<div class="glass-card" style="text-align:center;padding:12px;"><div class="box-title">👤 Outfit Preview</div>{svg_fig}</div>', unsafe_allow_html=True)
        with wc2: st.markdown(f'<div class="wear-box"><div class="box-title">👗 What to Wear</div>{"<br>".join(wear_items)}</div>', unsafe_allow_html=True)

        outfit_key = f"{round(temp_f//10)*10}"; saved_outfit = st.session_state.outfit_memory.get(outfit_key)
        with st.expander("💾 Save Your Own Outfit for This Temperature Range"):
            outfit_input = st.text_input("What are you wearing today?", value=saved_outfit or "", placeholder="e.g. jeans, hoodie, sneakers", key="outfit_inp")
            if st.button("Save Outfit"):
                st.session_state.outfit_memory[outfit_key] = outfit_input
                st.success(f"✅ Saved for {round(temp_f//10)*10}–{round(temp_f//10)*10+9}°F!")
        if saved_outfit:
            st.markdown(f'<div class="glass-card"><div class="box-title">💡 Your Saved Outfit</div><div style="color:white;font-size:14px;">👕 {saved_outfit}</div></div>', unsafe_allow_html=True)

        # Feel-Good Index
        st.markdown(f"""<div class="glass-card" style="display:flex;align-items:center;gap:20px;">
          <svg width="80" height="80" viewBox="0 0 80 80">
            <circle cx="40" cy="40" r="34" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="8"/>
            <circle cx="40" cy="40" r="34" fill="none" stroke="{fgi_col}" stroke-width="8"
              stroke-dasharray="213.6" stroke-dashoffset="{213.6-(fgi/100)*213.6:.1f}"
              stroke-linecap="round" transform="rotate(-90 40 40)"/>
            <text x="40" y="45" text-anchor="middle" font-size="18" font-weight="900" fill="white" font-family="Outfit,sans-serif">{fgi}</text>
          </svg>
          <div><div class="box-title">😊 Feel-Good Index</div>
          <div style="font-size:20px;font-weight:700;color:{fgi_col};">{fgi_lbl}</div>
          <div class="glass-sub">Temp 50% · Humidity 30% · Wind 20%</div></div>
        </div>""", unsafe_allow_html=True)

        # Humidity comfort
        hum_msg, hum_col = humidity_comfort(humidity)
        st.markdown(f'<div class="glass-card"><div class="box-title">💧 Humidity Comfort</div><div style="font-size:14px;color:{hum_col};">{hum_msg}</div><div class="glass-sub">{humidity}% relative humidity</div></div>', unsafe_allow_html=True)

        # Stats row
        vis_str = f"{vis_km} km" if vis_km is not None else "N/A"
        c1, c2, c3, c4 = st.columns(4)
        for col_w, (ico, lbl, val, sub) in zip([c1,c2,c3,c4], [
            ("💧","Humidity",  f"{humidity}%",          ""),
            ("💨","Wind",      f"{round(wind_mph)} mph", f"{wind_dir_str} · Gusts {round(gusts_mph)} mph"),
            ("🌧️","Rain",      f"{rain_pct}%",          "chance today"),
            ("👁️","Visibility",vis_str,                 ""),
        ]):
            with col_w: st.markdown(f'<div class="glass-card"><div class="glass-label">{ico} {lbl}</div><div class="glass-value" style="font-size:18px;">{val}</div><div class="glass-sub">{sub}</div></div>', unsafe_allow_html=True)

        c5, c6 = st.columns(2)
        with c5: st.markdown(f'<div class="glass-card"><div class="glass-label">🌞 UV Index</div><div class="glass-value">{round(uv)}</div><div class="glass-sub">out of 11</div></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="glass-card"><div class="glass-label">🌬️ Wind Direction</div><div class="glass-value">{wind_dir_str}</div><div class="glass-sub">{round(wind_deg or 0)}°</div></div>', unsafe_allow_html=True)

        # Pollen
        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px;">
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌾 Grass Pollen</div><div class="glass-value" style="font-size:15px;">{pollen_label(grass_pollen,"grass")}</div></div>
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌳 Tree Pollen</div><div class="glass-value" style="font-size:15px;">{pollen_label(tree_pollen,"tree")}</div></div>
        </div>""", unsafe_allow_html=True)

        # 5-day forecast
        st.markdown('<p style="color:white;font-weight:700;font-size:14px;margin:10px 0 8px;">📅 5-DAY FORECAST</p>', unsafe_allow_html=True)
        fc = '<div class="forecast-row">'
        for i in range(5):
            idx = i + 1
            dn = "Today" if i == 0 else datetime.strptime(daily_f["time"][idx],"%Y-%m-%d").strftime("%a")
            di = WMO_CODES.get(daily_f["weather_code"][idx],"🌡️").split()[0]
            dh = round(daily_d["temperature_2m_max"][idx]); dl = round(daily_d["temperature_2m_min"][idx])
            dhf = round(daily_f["temperature_2m_max"][idx]); dlf = round(daily_f["temperature_2m_min"][idx])
            au = "°C" if unit=="°F" else "°F"; dha = to_c(dhf) if unit=="°F" else to_f(dh); dla = to_c(dlf) if unit=="°F" else to_f(dl)
            fc += f'<div class="forecast-day"><div class="day-name">{dn}</div><div class="day-icon">{di}</div><div class="day-hi">{dh}{unit}</div><div class="day-lo">{dl}{unit}</div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px;">{dha}/{dla}{au}</div></div>'
        st.markdown(fc + "</div>", unsafe_allow_html=True)

        # Weekly trend sparkline
        trend_up = week_hi_f[-1] > week_hi_f[0]
        trend_label = "📈 Warming trend this week" if trend_up else "📉 Cooling trend this week"
        spark_color = "#f87171" if trend_up else "#60a5fa"
        st.markdown(f'<div class="glass-card"><div class="box-title">📊 Weekly High Temperature Trend</div>{make_sparkline(week_hi_d, spark_color)}<div class="glass-sub" style="margin-top:6px;">{trend_label}</div></div>', unsafe_allow_html=True)

        # Sun arc + sunrise/sunset
        st.markdown(make_sun_arc(local_now, sr_fmt, ss_fmt), unsafe_allow_html=True)
        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px;">
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌅 Sunrise</div><div class="glass-value">{sr_fmt}</div></div>
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌇 Sunset</div><div class="glass-value">{ss_fmt}</div></div>
        </div>""", unsafe_allow_html=True)

        # Hourly charts
        for chart, title in [
            (make_chart(hourly_temps_d,"white","ag","rgba(255,255,255,0.25)",unit,now_h,hour_labels,highlight_i=best_i), "🌡️ Hourly Temperature ★ shaded = best outdoor window"),
            (make_chart(hourly_feels_d,"rgba(255,200,100,0.9)","flg","rgba(255,180,60,0.3)",unit,now_h,hour_labels), "🥵 Hourly Feels Like"),
            (make_chart(hourly_rain_vals,"rgba(150,210,255,0.9)","rg","rgba(100,180,255,0.4)","%",now_h,hour_labels,fixed_min=0,fixed_max=100), "🌧️ Hourly Rain Probability"),
            (make_chart(hourly_wind,"rgba(200,240,200,0.9)","wg","rgba(150,220,150,0.3)"," mph",now_h,hour_labels), "💨 Hourly Wind Speed"),
        ]:
            components.html(
                f'<style>body{{margin:0;background:transparent;}}.gc{{background:rgba(0,0,0,0.25);border:1px solid rgba(255,255,255,0.2);border-radius:16px;padding:14px 10px 8px;backdrop-filter:blur(8px);}}.bt{{font-size:10px;letter-spacing:1.4px;color:rgba(255,255,255,0.6);font-weight:700;margin-bottom:8px;text-transform:uppercase;font-family:Outfit,sans-serif;}}</style>'
                f'<div class="gc"><div class="bt">{title}</div>{chart}</div>',
                height=210, scrolling=False
            )

        # Moon + AQI
        pm_text = f"{pm25:.1f} µg/m³" if pm25 is not None else "N/A"
        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px;">
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

        # Map
        st.markdown('<div class="box-title" style="color:rgba(255,255,255,0.6);margin-bottom:6px;">🗺️ WEATHER MAP</div>', unsafe_allow_html=True)
        components.html(f"""
        <div style="border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.25);margin-bottom:12px;">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="map" style="height:260px;width:100%;"></div>
        <script>
          var map=L.map('map',{{zoomControl:true,scrollWheelZoom:false}}).setView([{lat},{lon}],9);
          L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap',maxZoom:18}}).addTo(map);
          var icon=L.divIcon({{html:'<div style="font-size:24px;">📍</div>',iconSize:[30,30],className:''}});
          L.marker([{lat},{lon}],{{icon:icon}}).addTo(map).bindPopup('<b>{city_name}</b>').openPopup();
        </script></div>""", height=270)

        # Compare cities
        st.markdown("---")
        st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🆚 Compare With Another City</p>', unsafe_allow_html=True)
        compare_input = st.text_input("", placeholder="Enter another city to compare...", label_visibility="collapsed", key="compare_inp")
        if compare_input.strip():
            with st.spinner("Fetching comparison..."):
                res2 = fetch_weather(compare_input.strip(), unit)
                if res2[0] is None:
                    st.warning("⚠️ Comparison city not found.")
                else:
                    wx2_f, wx2_d, _, meta2 = res2
                    cur2_f = wx2_f["current"]; cur2_d = wx2_d["current"]
                    t2 = cur2_f["temperature_2m"]; t2_d = cur2_d["temperature_2m"]
                    w2 = cur2_f["wind_speed_10m"]; r2 = cur2_f.get("precipitation_probability",0)
                    h2 = cur2_f["relative_humidity_2m"]; c2_code = cur2_f["weather_code"]
                    fgi2, fgi2_lbl, fgi2_col = feel_good_index(t2, h2, w2)
                    alt2 = f"/ {to_c(t2)}°C" if unit=="°F" else f"/ {to_f(t2_d)}°F"
                    ca, cb = st.columns(2)
                    with ca:
                        st.markdown(f"""<div class="compare-col">
                          <div style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);margin-bottom:8px;">📍 {city_name}</div>
                          <div style="font-size:32px;font-weight:900;color:white;">{round(temp_d)}{unit}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);">{alt_t}</div>
                          <div style="font-size:13px;color:white;margin-top:6px;">{condition_str}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">💧{humidity}% &nbsp;💨{round(wind_mph)}mph &nbsp;🌧️{rain_pct}%</div>
                          <div style="font-size:12px;color:{fgi_col};margin-top:4px;">😊 {fgi}/100 — {fgi_lbl}</div>
                        </div>""", unsafe_allow_html=True)
                    with cb:
                        st.markdown(f"""<div class="compare-col">
                          <div style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);margin-bottom:8px;">📍 {meta2['name']}, {meta2['country']}</div>
                          <div style="font-size:32px;font-weight:900;color:white;">{round(t2_d)}{unit}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);">{alt2}</div>
                          <div style="font-size:13px;color:white;margin-top:6px;">{WMO_CODES.get(c2_code,'Unknown')}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">💧{h2}% &nbsp;💨{round(w2)}mph &nbsp;🌧️{r2}%</div>
                          <div style="font-size:12px;color:{fgi2_col};margin-top:4px;">😊 {fgi2}/100 — {fgi2_lbl}</div>
                        </div>""", unsafe_allow_html=True)
                    winner = f"🏆 {city_name} has better weather!" if fgi > fgi2 else (f"🏆 {meta2['name']} has better weather!" if fgi2 > fgi else "🤝 Both cities feel about the same!")
                    st.markdown(f'<div class="ai-box" style="margin-top:8px;">{winner}</div>', unsafe_allow_html=True)

        st.markdown('<p class="footer">Open-Meteo API · Air Quality API · OpenStreetMap · No API keys needed 😄</p>', unsafe_allow_html=True)

        # ── All feature blocks ─────────────────────────────────────────────────
        render_rain_countdown(hourly_rain_vals, hour_labels, now_h)
        activity_scores(temp_f, humidity, wind_mph, rain_pct, uv, condition_str)
        render_stats_summary(temp_f, humidity, wind_mph, uv, rain_pct, aqi_text, fgi, unit, temp_d, feels_d)
        render_hourly_table(hourly_temps_d, hourly_feels_d, hourly_rain_vals, hourly_wind, hour_labels, unit, now_h)
        render_music_mood(condition_str, temp_f, fgi)
        render_weather_photo(condition_str, city_name)
        render_aqi_health(aqi_text, pm25)
        render_historical(lat, lon, unit)
        render_severe_weather_map(lat, lon, city_name, code)
        render_trip_planner()
        render_packing_list()
        render_weather_diary(city_name, temp_d, unit, condition_str)
        render_multi_city_dashboard(unit)
        st.markdown(wind_compass_svg(wind_deg, wind_mph, wind_dir_str), unsafe_allow_html=True)
        render_radar(lat, lon, city_name)
        render_uv_timeline(hourly_uv_today, hour_labels, now_h)
        render_30day_history(lat, lon, unit)
        render_change_detector(temp_f, hi_f_val, lo_f_val, yest_hi_f, yest_lo_f, feels_f, wind_mph, condition_str, unit)
        render_golden_hour(sr_fmt, ss_fmt, local_now)
        render_pollen_tracker(grass_pollen, tree_pollen)
        render_commute_advisor(hourly_temps_d, hourly_feels_d, hourly_rain_vals, hourly_wind, hour_labels, unit)
        render_weekend_scorer(daily_f, daily_d, unit)
        render_tweet_copy(city_name, temp_d, unit, condition_str, hi_d, lo_d, fgi, fgi_lbl)
        render_friends_weather(unit)
        render_time_capsule(city_name, temp_d, unit, condition_str, fgi)
        render_sleep_forecast(hourly_temps_f, hourly_wind, hour_labels)
        render_gardening_advisor(temp_f, humidity, rain_pct, wind_mph, uv, t_rain)
        render_running_advisor(temp_f, humidity, wind_mph, aqi_text, unit, temp_d)
        render_windows_advisor(temp_f, aqi_text, grass_pollen, tree_pollen, wind_mph, condition_str)
        render_allergy_alert(grass_pollen, tree_pollen, aqi_text, wind_mph)
        render_best_day(daily_f, daily_d, unit)
        render_confidence_badges(daily_f)
        render_dew_point(temp_f, humidity, unit)
        st.markdown(visibility_gauge_svg(vis_km), unsafe_allow_html=True)
        render_currency_weather(unit)
        render_qr_code(city_name)
        render_print_report(city_name, country, temp_d, unit, condition_str,
                            hi_d, lo_d, humidity, wind_mph, wind_dir_str,
                            rain_pct, uv, aqi_text, sr_fmt, ss_fmt, fgi, fgi_lbl)

        # Thermometer + Feels comparison side by side
        bc1, bc2 = st.columns([1, 2])
        with bc1: st.markdown(thermometer_svg(temp_f, unit, temp_d), unsafe_allow_html=True)
        with bc2: render_feels_comparison(temp_f, feels_f, temp_d, feels_d, humidity, wind_mph, unit)

        render_day_progress(local_now, sr_fmt, ss_fmt)
        render_wind_detail(wind_mph, gusts_mph, wind_dir_str)

        # Auto-refresh countdown
        if "last_fetch_time" not in st.session_state:
            st.session_state.last_fetch_time = datetime.now()
        elapsed = (datetime.now() - st.session_state.last_fetch_time).total_seconds()
        if elapsed > 1800:
            st.session_state.last_fetch_time = datetime.now()
            st.rerun()
        else:
            remaining = max(0, 1800 - int(elapsed))
            st.markdown(f'<div style="font-size:10px;color:rgba(255,255,255,0.3);text-align:right;margin-bottom:4px;">🔄 Auto-refresh in {remaining//60}m {remaining%60:02d}s</div>', unsafe_allow_html=True)

# ── Weather Game ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p style="color:white;font-weight:700;font-size:18px;margin-bottom:8px;">🎮 Play Weather Game?</p>', unsafe_allow_html=True)
play_game = st.radio("", ["Yes, play!", "No thanks"], horizontal=True, label_visibility="collapsed", key="game_radio")

if play_game == "Yes, play!":
    weather_options = [("☀️","Sunny"),("🌧️","Rainy"),("❄️","Snowy"),("⛈️","Stormy")]
    if "game_weather" not in st.session_state:
        st.session_state.game_weather = random.choice(weather_options)
    emoji_g, answer_g = st.session_state.game_weather
    st.markdown(f"""<div style="text-align:center;padding:30px;border-radius:20px;background:rgba(255,255,255,0.08);margin:10px 0;">
        <div style="font-size:90px;">{emoji_g}</div>
        <div style="color:rgba(255,255,255,0.7);font-size:14px;margin-top:8px;">Guess the weather condition!</div>
    </div>""", unsafe_allow_html=True)
    guess_g = st.radio("Your guess:", ["Sunny","Rainy","Snowy","Stormy"], horizontal=True, key="game_guess")
    gc1, gc2 = st.columns(2)
    with gc1:
        if st.button("🎯 Submit Guess", key="game_submit"):
            if guess_g == answer_g: st.success("🎉 Correct! Well done!")
            else: st.error(f"❌ Wrong! It was {answer_g}")
    with gc2:
        if st.button("🔄 New Round", key="game_new"):
            st.session_state.game_weather = random.choice(weather_options); st.rerun()

# ── Logo Maker ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p style="color:white;font-weight:700;font-size:18px;margin-bottom:8px;">🎨 Quick Logo Creator</p>', unsafe_allow_html=True)
logo_text  = st.text_input("Business/App Name", placeholder="NimbusAI", key="logo_text_input")
logo_color = st.color_picker("Pick Logo Color", "#38b6ff", key="logo_color_picker")
logo_emoji = st.selectbox("Choose Logo Emoji",
    ["⚡","🚀","🌟","🔥","💎","🎯","🌊","🍀","🦋","🐉","🌈","🏆","💡","🎨","🔮","🦅","🌙","☀️","❄️","🎵","None"],
    key="logo_emoji_selectbox")
if logo_text:
    prefix = "" if logo_emoji == "None" else f"{logo_emoji} "
    st.markdown(f"""<div style="background:rgba(255,255,255,0.1);padding:40px;border-radius:20px;text-align:center;
        margin-top:15px;border:1px solid rgba(255,255,255,0.2);">
        <div style="font-size:48px;font-weight:900;color:{logo_color};letter-spacing:2px;">{prefix}{logo_text}</div>
    </div>""", unsafe_allow_html=True)

# ── Favourites + PWA + keyboard shortcuts ──────────────────────────────────────
render_favourites()
inject_pwa()
components.html(KEYBOARD_JS, height=0, scrolling=False)
