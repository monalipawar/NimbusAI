import streamlit as st
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import math, random, json

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="NimbusAI", page_icon="🌤️", layout="centered")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<div style="display:none"><style>
* { font-family:'Outfit',sans-serif !important; }
.stApp { background:linear-gradient(160deg,#1a6eff 0%,#38b6ff 55%,#87ceeb 100%) !important; min-height:100vh; transition:background 1.2s ease !important; }
[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stMain"] { background:transparent !important; }

.hero-card   { border-radius:24px; padding:32px 28px 24px; color:white; margin-bottom:16px; background:rgba(0,0,0,0.15); box-shadow:0 8px 32px rgba(0,0,0,0.2); border:1px solid rgba(255,255,255,0.25); }
.hero-temp   { font-size:84px; font-weight:900; line-height:1; letter-spacing:-4px; text-shadow:0 4px 20px rgba(0,0,0,0.2); color:white; }
.hero-city   { font-size:20px; font-weight:600; color:white; margin-bottom:2px; }
.hero-cond   { font-size:15px; font-weight:300; color:rgba(255,255,255,0.85); }
.hilo-badge  { display:inline-flex; align-items:center; gap:6px; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.35); border-radius:30px; padding:5px 14px; font-size:14px; font-weight:600; color:white; margin-right:8px; margin-top:12px; }
.glass-card  { background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25); border-radius:16px; padding:16px 18px; color:white; margin-bottom:12px; }
.glass-label { font-size:11px; font-weight:700; letter-spacing:1.2px; color:rgba(255,255,255,0.65); text-transform:uppercase; margin-bottom:4px; }
.glass-value { font-size:22px; font-weight:700; color:white; }
.glass-sub   { font-size:12px; color:rgba(255,255,255,0.6); margin-top:2px; }
.ai-box      { border-radius:16px; padding:16px 20px; font-size:15px; font-weight:500; margin-bottom:12px; border:1px solid rgba(255,255,255,0.25); background:rgba(255,255,255,0.15); color:white; }
.wear-box    { border-radius:16px; padding:16px 20px; font-size:14px; line-height:1.9; margin-bottom:12px; border:1px solid rgba(255,255,255,0.25); background:rgba(255,255,255,0.12); color:white; }
.warn-box    { border-radius:16px; padding:16px 20px; background:rgba(180,20,20,0.35); border:1px solid rgba(255,120,120,0.5); color:white; margin-bottom:12px; font-size:14px; }
.info-box    { border-radius:16px; padding:14px 18px; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:white; margin-bottom:12px; font-size:14px; }
.box-title   { font-size:10px; letter-spacing:1.4px; color:rgba(255,255,255,0.6); font-weight:700; margin-bottom:8px; text-transform:uppercase; }
.tomorrow-card { border-radius:16px; padding:16px 20px; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:white; margin-bottom:12px; }
.forecast-row  { display:flex; gap:8px; margin-bottom:12px; }
.forecast-day  { flex:1; background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25); border-radius:14px; padding:12px 6px; text-align:center; color:white; min-width:52px; }
.day-name { font-size:11px; font-weight:700; color:rgba(255,255,255,0.7); margin-bottom:4px; }
.day-icon { font-size:22px; margin-bottom:4px; }
.day-hi   { font-size:13px; font-weight:700; color:white; }
.day-lo   { font-size:11px; color:rgba(255,255,255,0.55); margin-top:2px; }
.chip-row { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px; }
.chip     { background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.3); border-radius:20px; padding:4px 12px; font-size:12px; color:white; }
.footer   { font-size:11px; color:rgba(255,255,255,0.5); text-align:center; margin-top:8px; }
.dual-temp { font-size:13px; color:rgba(255,255,255,0.6); font-weight:400; margin-left:6px; }
.compare-col { background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:16px; margin-bottom:12px; }

/* Chat */
.chat-container { border-radius:16px; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.25); padding:16px; margin-bottom:12px; max-height:420px; overflow-y:auto; scroll-behavior:smooth; }
.chat-msg-user  { background:rgba(255,255,255,0.25); border-radius:12px 12px 4px 12px; padding:10px 14px; margin:8px 0; font-size:14px; color:white; text-align:right; }
.chat-msg-bot   { background:rgba(0,0,0,0.22); border-radius:12px 12px 12px 4px; padding:10px 14px; margin:8px 0; font-size:14px; color:white; line-height:1.6; }
.chat-name-user { font-size:10px; color:rgba(255,255,255,0.5); text-align:right; margin-bottom:2px; letter-spacing:1px; }
.chat-name-bot  { font-size:10px; color:rgba(255,255,255,0.5); margin-bottom:2px; letter-spacing:1px; }
.chat-typing    { font-size:13px; color:rgba(255,255,255,0.5); font-style:italic; padding:8px 14px; }

/* Sparkline row */
.sparkline-row { display:flex; gap:3px; align-items:flex-end; height:36px; margin-top:6px; }
.spark-bar { flex:1; border-radius:3px 3px 0 0; min-height:4px; }

/* Particles */
@keyframes float-cloud { 0%{transform:translateX(-120px)} 100%{transform:translateX(110vw)} }
@keyframes fall-rain   { 0%{transform:translateY(-20px);opacity:0.7} 100%{transform:translateY(110vh);opacity:0} }
@keyframes fall-snow   { 0%{transform:translateY(-20px) rotate(0deg);opacity:0.8} 100%{transform:translateY(110vh) rotate(360deg);opacity:0} }
@keyframes flash       { 0%,90%,100%{opacity:0} 92%,98%{opacity:1} }
.weather-particles { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; overflow:hidden; }
.cloud-particle { position:absolute; animation:float-cloud linear infinite; opacity:0.18; }
.rain-particle  { position:absolute; width:2px; border-radius:2px; background:rgba(200,230,255,0.6); animation:fall-rain linear infinite; }
.snow-particle  { position:absolute; font-size:14px; animation:fall-snow linear infinite; color:white; }
.lightning      { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(255,255,200,0.15); pointer-events:none; z-index:1; animation:flash 4s infinite; }

/* Widget overrides */
.stTextInput>div>div>input { background:rgba(255,255,255,0.2) !important; border:1px solid rgba(255,255,255,0.35) !important; border-radius:12px !important; color:white !important; font-size:15px !important; }
.stTextInput>div>div>input::placeholder { color:rgba(255,255,255,0.55) !important; }
.stTextInput label { color:white !important; }
.stButton>button { background:rgba(255,255,255,0.2) !important; border:1px solid rgba(255,255,255,0.35) !important; border-radius:12px !important; color:white !important; font-weight:600 !important; transition:all 0.2s; }
.stButton>button:hover { background:rgba(255,255,255,0.32) !important; transform:translateY(-1px); }
.stRadio label,.stRadio div { color:white !important; }
.stSpinner p { color:white !important; }
.stToggle label { color:white !important; }
.stForm { background:transparent !important; border:none !important; }
.stExpander { background:rgba(255,255,255,0.1) !important; border:1px solid rgba(255,255,255,0.2) !important; border-radius:12px !important; }
.stExpander summary { color:white !important; }

/* Mobile */
@media(max-width:600px){
  .hero-temp { font-size:56px !important; }
  .forecast-row { flex-wrap:wrap !important; }
  .forecast-day { min-width:56px !important; }
}
</style></div>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
WMO_CODES = {
    0:"☀️ Clear sky",1:"🌤️ Mainly clear",2:"⛅ Partly cloudy",3:"☁️ Overcast",
    45:"🌫️ Foggy",48:"🌫️ Icy fog",
    51:"🌦️ Light drizzle",53:"🌦️ Drizzle",55:"🌧️ Heavy drizzle",
    61:"🌧️ Light rain",63:"🌧️ Rain",65:"🌧️ Heavy rain",
    71:"🌨️ Light snow",73:"🌨️ Snow",75:"❄️ Heavy snow",
    80:"🌦️ Rain showers",81:"🌧️ Showers",82:"⛈️ Heavy showers",
    95:"⛈️ Thunderstorm",96:"⛈️ Thunderstorm + hail",99:"⛈️ Heavy thunderstorm"
}
SEVERE_CODES = {65,75,82,95,96,99}
SEVERE_MESSAGES = {
    65:"🚨 Heavy rain warning! Carry an umbrella and avoid flooded areas.",
    75:"🚨 Heavy snow warning! Roads may be slippery — be careful outside.",
    82:"🚨 Violent rain showers! Stay indoors if you can.",
    95:"⚡ Thunderstorm warning! Stay indoors and away from trees.",
    96:"⚡ Thunderstorm with hail! Do not go outside.",
    99:"⚡ Severe thunderstorm with hail! This is dangerous — stay inside."
}
SKY_GRADIENTS = {
    "sky-clear":   "linear-gradient(160deg,#1a6eff 0%,#38b6ff 55%,#87ceeb 100%)",
    "sky-cloudy":  "linear-gradient(160deg,#4b5e7a 0%,#7f97b8 55%,#b0c4d8 100%)",
    "sky-rain":    "linear-gradient(160deg,#1e3a5f 0%,#2d5986 55%,#4a7fa8 100%)",
    "sky-snow":    "linear-gradient(160deg,#6b8cae 0%,#a8c2d8 55%,#ddeeff 100%)",
    "sky-thunder": "linear-gradient(160deg,#1a1a2e 0%,#2d2d44 55%,#4a3f6b 100%)",
    "sky-fog":     "linear-gradient(160deg,#6b7a8d 0%,#9aabb8 55%,#c5d0d8 100%)",
}
WIND_DIRS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

def sky_class(code):
    if code in {95,96,99}: return "sky-thunder"
    if code in {61,63,65,51,53,55,80,81,82}: return "sky-rain"
    if code in {71,73,75}: return "sky-snow"
    if code in {45,48}: return "sky-fog"
    if code == 3: return "sky-cloudy"
    return "sky-clear"

def wind_dir_label(deg):
    if deg is None: return "—"
    return WIND_DIRS[round(deg/22.5)%16]

# ── Helpers ───────────────────────────────────────────────────────────────────
def to_c(f): return round((f-32)*5/9)
def to_f(c): return round(c*9/5+32)
def dual(f): return f"{round(f)}°F / {to_c(f)}°C"

def feel_good_index(temp_f, humidity, wind_mph):
    score=round(max(0,100-abs(temp_f-72)*2.5)*0.5+max(0,100-abs(humidity-45)*1.2)*0.3+max(0,100-max(0,wind_mph-10)*3)*0.2)
    if score>=80: return score,"Excellent 😄","#4ade80"
    if score>=60: return score,"Good 🙂","#a3e635"
    if score>=40: return score,"Fair 😐","#facc15"
    if score>=20: return score,"Poor 😟","#fb923c"
    return score,"Bad 😣","#f87171"

def pollen_label(val, kind):
    if val is None: return "N/A"
    t={"grass":[(10,"Low"),(50,"Moderate"),(200,"High")],"tree":[(15,"Low"),(90,"Moderate"),(1500,"High")]}
    for th,l in t.get(kind,[]):
        if val<th: return f"{val:.0f} — {l}"
    return f"{val:.0f} — Very High"

def what_to_wear(temp_f, condition, wind_mph):
    cond=condition.lower()
    if temp_f<=32:   items=[f"🧥 Heavy coat — {dual(temp_f)}, freezing!","🧤 Gloves","🧣 Scarf","🥾 Insulated boots","🎿 Thermal layers"]
    elif temp_f<=50: items=[f"🧥 Jacket — {dual(temp_f)}, very cold!","👖 Jeans","🧤 Gloves recommended","👟 Closed-toe shoes"]
    elif temp_f<=65: items=[f"🧶 Hoodie or light jacket — {dual(temp_f)}, cool.","👖 Jeans or light pants","👟 Sneakers"]
    elif temp_f<=77: items=[f"👕 T-shirt — {dual(temp_f)}, comfortable!","👖 Light pants","👟 Any shoes"]
    elif temp_f<=91: items=[f"🩳 Shorts — {dual(temp_f)}, warm!","👕 Light shirt","🧢 Cap","🕶️ Sunglasses","🧴 Sunscreen!"]
    else:            items=[f"🩳 Shorts — {dual(temp_f)}, extremely hot!","👕 Lightest shirt","🧢 Sun hat!","🕶️ Sunglasses","🧴 High SPF sunscreen","💧 Carry water everywhere"]
    if any(x in cond for x in ["rain","drizzle","shower"]): items+=["☔ Umbrella","👟 Waterproof shoes"]
    if "snow" in cond: items+=["❄️ Snow boots","🧦 Thick socks & layers"]
    if "thunder" in cond: items.append("🏠 Consider staying indoors")
    if wind_mph>5: items.append("🌬️ Windbreaker")
    return items

def outfit_svg(temp_f, cond):
    """Simple SVG figure showing outfit based on temperature."""
    c = cond.lower()
    shirt_color = "#3b82f6" if temp_f > 77 else "#6366f1"
    hat = ""
    if temp_f > 85:
        hat = '<ellipse cx="50" cy="22" rx="18" ry="5" fill="#fbbf24"/><rect x="38" y="10" width="24" height="14" rx="4" fill="#fbbf24"/>'
    elif temp_f < 50:
        hat = '<ellipse cx="50" cy="22" rx="18" ry="6" fill="#7c3aed"/><rect x="36" y="10" width="28" height="14" rx="6" fill="#7c3aed"/><rect x="34" y="20" width="32" height="5" rx="2" fill="#5b21b6"/>'
    scarf = '<rect x="38" y="52" width="24" height="8" rx="4" fill="#ef4444"/>' if temp_f < 45 else ""
    umbrella = ""
    if any(x in c for x in ["rain", "drizzle", "shower"]):
        umbrella = '<path d="M85 70 Q85 45 110 45 Q135 45 135 70" fill="#6366f1" stroke="white" stroke-width="1.5"/><line x1="110" y1="45" x2="110" y2="85" stroke="#4b5563" stroke-width="2"/><path d="M110 85 Q110 92 104 92" fill="none" stroke="#4b5563" stroke-width="2"/>'
    pants_color = "#1e40af" if temp_f < 68 else "#0ea5e9"
    pants_h = 35 if temp_f > 77 else 50
    return (
        f'<div style="display:flex;align-items:center;justify-content:center;padding:12px;">'
        f'<svg viewBox="0 0 160 130" xmlns="http://www.w3.org/2000/svg" style="width:120px;height:auto;">'
        f'{hat}'
        f'<circle cx="50" cy="35" r="14" fill="#fde68a" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>'
        f'<ellipse cx="50" cy="68" rx="16" ry="20" fill="{shirt_color}"/>'
        f'{scarf}'
        f'<line x1="34" y1="58" x2="22" y2="78" stroke="{shirt_color}" stroke-width="7" stroke-linecap="round"/>'
        f'<line x1="66" y1="58" x2="78" y2="78" stroke="{shirt_color}" stroke-width="7" stroke-linecap="round"/>'
        f'<rect x="36" y="84" width="12" height="{pants_h}" rx="4" fill="{pants_color}"/>'
        f'<rect x="52" y="84" width="12" height="{pants_h}" rx="4" fill="{pants_color}"/>'
        f'{umbrella}'
        f'</svg></div>'
    )

def ai_comment(temp_f, cond, wind_mph):
    c=cond.lower()
    if temp_f<=32:  return f"🥶 Extreme cold ({dual(temp_f)}) — frost risk, heavy winter gear needed."
    if temp_f<=50:  return f"🧊 Very cold ({dual(temp_f)}) — winter jacket recommended."
    if temp_f<=65:  return f"🌬️ Cool weather ({dual(temp_f)}) — light jacket or hoodie works well."
    if temp_f<=79:  return f"🌤️ Perfect weather ({dual(temp_f)}) — comfortable and balanced."
    if temp_f<=91:  return f"🔥 Hot weather ({dual(temp_f)}) — stay hydrated and wear light clothes."
    if temp_f>91:   return f"☀️ Extreme heat ({dual(temp_f)}) — avoid long outdoor exposure."
    if "rain" in c: return f"☔ Rain expected ({dual(temp_f)}) — carry umbrella or raincoat."
    if "thunder" in c: return f"⛈️ Storm alert ({dual(temp_f)}) — stay indoors if possible."
    if wind_mph>19: return f"🌬️ Windy ({dual(temp_f)}) — secure loose items."
    return f"🌡️ Normal conditions ({dual(temp_f)})."

def feels_like_reason(temp_f, humidity, wind_mph):
    if wind_mph>10 and temp_f<50: return f"🌬️ Wind chill: {wind_mph:.0f} mph winds make it feel colder than {to_c(temp_f)}°C / {round(temp_f)}°F."
    if humidity>70 and temp_f>75: return f"💧 Humidity: {humidity}% moisture traps heat, making it feel hotter."
    if humidity<30:               return f"🏜️ Low humidity ({humidity}%) lets sweat evaporate fast — feels cooler and drier."
    return f"🌡️ Feels close to actual temperature — comfortable humidity and calm winds."

def humidity_comfort(humidity):
    if humidity>80:   return "💦 Very humid — muggy and uncomfortable.", "#f87171"
    if humidity>70:   return "😓 Humid — may feel sticky and warm.", "#fb923c"
    if humidity<20:   return "🏜️ Very dry — skin and eyes may feel irritated.", "#f87171"
    if humidity<30:   return "😐 Dry air — consider staying hydrated.", "#facc15"
    return "✅ Comfortable humidity level.", "#4ade80"

def aqi_label(aqi):
    if aqi is None: return "N/A","rgba(255,255,255,0.4)"
    if aqi<=50:  return f"{aqi} Good","#4ade80"
    if aqi<=100: return f"{aqi} Moderate","#facc15"
    if aqi<=150: return f"{aqi} Unhealthy for Sensitive","#fb923c"
    if aqi<=200: return f"{aqi} Unhealthy","#f87171"
    if aqi<=300: return f"{aqi} Very Unhealthy","#c084fc"
    return f"{aqi} Hazardous","#ef4444"

def get_moon_phase(date):
    y,m,d=date.year,date.month,date.day
    if m<3: y-=1; m+=12
    a=y//100;b=a//4;c=2-a+b
    e=int(365.25*(y+4716));f=int(30.6001*(m+1))
    jd=c+d+e+f-1524.5
    phase=((jd-2451549.5)%29.53058867)/29.53058867
    if phase<0.0625:  return "🌑","New Moon"
    if phase<0.1875:  return "🌒","Waxing Crescent"
    if phase<0.3125:  return "🌓","First Quarter"
    if phase<0.4375:  return "🌔","Waxing Gibbous"
    if phase<0.5625:  return "🌕","Full Moon"
    if phase<0.6875:  return "🌖","Waning Gibbous"
    if phase<0.8125:  return "🌗","Last Quarter"
    return "🌘","Waning Crescent"

def best_outdoor_window(hourly_temps_f, hourly_rain, hourly_wind, hour_labels):
    """Find best 2-hour window to go outside."""
    best_score=-999; best_i=0
    for i in range(22):
        t=hourly_temps_f[i]; r=hourly_rain[i]; w=hourly_wind[i]
        score=(100-abs(t-72)*2)-(r*0.8)-(max(0,w-10)*1.5)
        if score>best_score: best_score=score; best_i=i
    t1=hour_labels[best_i]; t2=hour_labels[min(best_i+2,23)]
    temp_at=round(hourly_temps_f[best_i]); rain_at=hourly_rain[best_i]
    return best_i, f"🌟 Best time to go outside: **{t1} – {t2}** · {dual(temp_at)}, {rain_at}% rain chance"

def what_changed_yesterday(today_hi_f, today_lo_f, today_rain, yesterday_hi_f, yesterday_lo_f, yesterday_rain, unit):
    msgs=[]
    hi_diff=today_hi_f-yesterday_hi_f
    lo_diff=today_lo_f-yesterday_lo_f
    disp_hi=round(abs(hi_diff)*5/9) if unit=="°C" else round(abs(hi_diff))
    disp_lo=round(abs(lo_diff)*5/9) if unit=="°C" else round(abs(lo_diff))
    if abs(hi_diff)>=2: msgs.append(f"{'🌡️ Warmer' if hi_diff>0 else '❄️ Cooler'} today — high is {disp_hi}{unit} {'higher' if hi_diff>0 else 'lower'} than yesterday.")
    else: msgs.append("🌡️ Similar high temperature to yesterday.")
    rain_diff=today_rain-yesterday_rain
    if abs(rain_diff)>=15: msgs.append(f"{'🌧️ More rain' if rain_diff>0 else '☀️ Less rain'} expected vs yesterday ({abs(rain_diff):.0f}% {'more' if rain_diff>0 else 'less'}).")
    return " ".join(msgs) if msgs else "📅 Very similar conditions to yesterday."

# ── AI Chat using Anthropic API ───────────────────────────────────────────────
def build_weather_system_prompt(ctx):
    if not ctx: return "You are NimbusAI, a friendly weather assistant."
    return f"""You are NimbusAI, a friendly, knowledgeable, and concise weather assistant built into a weather app.

You have access to real-time weather data for {ctx['city']}:
- Current temperature: {dual(ctx['temp_f'])} (feels like {dual(ctx['feels_f'])})
- Condition: {ctx['condition']}
- Humidity: {ctx['humidity']}%
- Wind: {ctx['wind_mph']:.0f} mph {ctx['wind_dir']} (gusts {ctx['gusts_mph']:.0f} mph)
- Rain chance today: {ctx['rain_pct']}%
- UV index: {ctx['uv']}
- Visibility: {ctx.get('visibility_km','N/A')} km
- Today's high: {dual(ctx['hi_f'])}, low: {dual(ctx['lo_f'])}
- Tomorrow: {ctx.get('tomorrow_cond','N/A')}, high {dual(ctx.get('tomorrow_hi_f', ctx['hi_f']))}, {ctx.get('tomorrow_rain_pct',0)}% rain
- Feel-Good Index: {ctx.get('fgi',50)}/100
- AQI: {ctx.get('aqi','N/A')}
- Grass pollen: {ctx.get('grass_pollen','N/A')}, Tree pollen: {ctx.get('tree_pollen','N/A')}
- Moon phase: {ctx.get('moon_name','N/A')}
- Sunrise: {ctx.get('sunrise','N/A')}, Sunset: {ctx.get('sunset','N/A')}
- Best outdoor window today: {ctx.get('best_window','N/A')}

Answer ANY weather-related question using this data. Be helpful, friendly, and specific. Use emojis naturally.
Keep answers under 4 sentences unless the question truly requires more detail.
If asked about something not weather-related, politely redirect to weather topics.
Always use both °F and °C when mentioning temperatures."""

def chat_with_ai(messages, ctx):
    """Call Anthropic API for open-ended weather chat."""
    system = build_weather_system_prompt(ctx)
    api_messages = [{"role": m["role"], "content": m["content"]} for m in messages]
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 400,
                "system": system,
                "messages": api_messages
            },
            timeout=15
        )
        data = resp.json()
        if "content" in data and data["content"]:
            return data["content"][0].get("text","Sorry, I couldn't get a response.")
        return "⚠️ Sorry, I couldn't reach my AI brain right now. Try again!"
    except Exception as e:
        return f"⚠️ Connection issue: {str(e)[:60]}. Check your internet and try again."

# ── SVG chart helper ──────────────────────────────────────────────────────────
_chart_counter = [0]

def make_chart(values, color, grad_id, grad_color, unit_lbl, now_h, hour_labels,
               fixed_min=None, fixed_max=None, highlight_i=None):
    # Use a unique ID each call so duplicate gradient IDs don't conflict in the DOM
    _chart_counter[0] += 1
    uid = f"{grad_id}_{_chart_counter[0]}"

    W,H=680,160; PL,PR,PT,PB=36,10,16,32; CW,CH=W-PL-PR,H-PT-PB
    mn=(fixed_min if fixed_min is not None else min(values)-2)
    mx=(fixed_max if fixed_max is not None else max(values)+2)
    rng=mx-mn or 1

    def tx(i): return PL+(i/(len(values)-1))*CW
    def ty(v): return PT+CH-((v-mn)/rng)*CH

    pts=" ".join(f"{tx(i):.1f},{ty(v):.1f}" for i,v in enumerate(values))
    area=(f"M{tx(0):.1f},{ty(values[0]):.1f} "
          +" ".join(f"L{tx(i):.1f},{ty(v):.1f}" for i,v in enumerate(values))
          +f" L{tx(len(values)-1):.1f},{PT+CH} L{tx(0):.1f},{PT+CH} Z")

    xlbls="".join(
        f'<text x="{tx(i):.1f}" y="{PT+CH+18}" text-anchor="middle" font-size="10" '
        f'fill="rgba(255,255,255,0.6)" font-family="Outfit,sans-serif">{hour_labels[i]}</text>'
        for i in range(0,24,3))
    ylbls="".join(
        f'<text x="{PL-4}" y="{ty(v):.1f}" text-anchor="end" dominant-baseline="middle" '
        f'font-size="10" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{round(v)}{unit_lbl}</text>'
        for v in [mn+(mx-mn)*0.1, (mn+mx)/2, mx-(mx-mn)*0.1])

    dot  = (f'<circle cx="{tx(now_h):.1f}" cy="{ty(values[now_h]):.1f}" r="5" '
            f'fill="white" stroke="rgba(255,255,255,0.4)" stroke-width="3"/>')
    dlbl = (f'<text x="{tx(now_h):.1f}" y="{ty(values[now_h])-10:.1f}" '
            f'text-anchor="middle" font-size="11" fill="white" font-weight="bold" '
            f'font-family="Outfit,sans-serif">{round(values[now_h])}{unit_lbl}</text>')

    hi_rect=""
    if highlight_i is not None:
        x1=tx(highlight_i); x2=tx(min(highlight_i+2,23))
        hi_rect=(f'<rect x="{x1:.1f}" y="{PT}" width="{x2-x1:.1f}" height="{CH}" '
                 f'fill="rgba(255,255,255,0.08)" rx="4"/>')

    return (
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">'
        f'<defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{grad_color}"/>'
        f'<stop offset="100%" stop-color="rgba(0,0,0,0.01)"/>'
        f'</linearGradient></defs>'
        f'{hi_rect}'
        f'<path d="{area}" fill="url(#{uid})"/>'
        f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        f'{xlbls}{ylbls}{dot}{dlbl}'
        f'</svg>'
    )

def make_sparkline(values, color="#4ade80"):
    mn=min(values); mx=max(values); rng=mx-mn or 1
    bars=""
    for v in values:
        h=max(4,round(((v-mn)/rng)*32)+4)
        bars+=f'<div class="spark-bar" style="height:{h}px;background:{color};opacity:0.7;"></div>'
    return f'<div class="sparkline-row">{bars}</div>'

def make_sun_arc(now_dt, sunrise_str, sunset_str):
    """SVG arc showing sun position in the day."""
    try:
        sr=datetime.strptime(sunrise_str,"%I:%M %p"); ss=datetime.strptime(sunset_str,"%I:%M %p")
        now_mins=(now_dt.hour*60+now_dt.minute)
        sr_mins=(sr.hour*60+sr.minute); ss_mins=(ss.hour*60+ss.minute)
        day_len=ss_mins-sr_mins
        if day_len<=0: raise ValueError
        pct=max(0,min(1,(now_mins-sr_mins)/day_len))
        # arc: x from 20 to 280, y peaks at 20
        cx=20+pct*260
        cy=80-math.sin(pct*math.pi)*55
        is_day=(sr_mins<=now_mins<=ss_mins)
        icon="☀️" if is_day else "🌙"
        return f"""<div class="glass-card" style="margin-bottom:12px;">
            <div class="box-title">🌅 Sun Position</div>
            <svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
                <path d="M20 80 Q150 15 280 80" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="2" stroke-dasharray="6 4"/>
                <path d="M20 80 Q{20+pct*130:.0f} {80-math.sin(pct*math.pi/2)*55:.0f} {cx:.0f} {cy:.0f}" fill="none" stroke="rgba(255,220,80,0.7)" stroke-width="2.5"/>
                <text x="20" y="95" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{sunrise_str}</text>
                <text x="280" y="95" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{sunset_str}</text>
                <text x="{cx:.0f}" y="{cy-6:.0f}" text-anchor="middle" font-size="20">{icon}</text>
            </svg>
        </div>"""
    except: return ""

# ── Particles ─────────────────────────────────────────────────────────────────
def make_particles(sky_bg):
    p='<div class="weather-particles">'
    if sky_bg=="sky-clear":
        for _ in range(4): p+=f'<div class="cloud-particle" style="top:{random.randint(3,35)}%;font-size:{random.randint(32,56)}px;animation-duration:{random.randint(18,35)}s;animation-delay:-{random.randint(0,20)}s;">☁️</div>'
    elif sky_bg=="sky-rain":
        for _ in range(40): p+=f'<div class="rain-particle" style="left:{random.randint(0,100)}%;height:{random.randint(12,22)}px;animation-duration:{random.uniform(0.6,1.2):.2f}s;animation-delay:-{random.uniform(0,2):.2f}s;"></div>'
    elif sky_bg=="sky-snow":
        for _ in range(30): p+=f'<div class="snow-particle" style="left:{random.randint(0,100)}%;animation-duration:{random.uniform(3,7):.2f}s;animation-delay:-{random.uniform(0,5):.2f}s;">❄️</div>'
    elif sky_bg=="sky-thunder":
        p+='<div class="lightning"></div>'
        for _ in range(25): p+=f'<div class="rain-particle" style="left:{random.randint(0,100)}%;height:{random.randint(15,28)}px;animation-duration:{random.uniform(0.5,0.9):.2f}s;animation-delay:-{random.uniform(0,1.5):.2f}s;background:rgba(180,210,255,0.7);"></div>'
    return p+'</div>'

# ── Weather fetch ─────────────────────────────────────────────────────────────
def fetch_weather(city_name, unit):
    geo=requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1").json()
    if "results" not in geo or not geo["results"]: return None,None,None,None
    r=geo["results"][0]
    lat,lon=r["latitude"],r["longitude"]
    name=r["name"]; country=r.get("country","")

    # yesterday's date for comparison
    yesterday=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")

    wx_f=requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"wind_speed_10m,wind_gusts_10m,wind_direction_10m,weather_code,"
        f"precipitation_probability,uv_index,visibility"
        f"&hourly=temperature_2m,apparent_temperature,precipitation_probability,wind_speed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset,"
        f"precipitation_probability_max,precipitation_sum"
        f"&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=7"
        f"&past_days=1"
    ).json()

    wx_display=wx_f
    if unit=="°C":
        wx_display=requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature"
            f"&hourly=temperature_2m,apparent_temperature"
            f"&daily=temperature_2m_max,temperature_2m_min"
            f"&temperature_unit=celsius&wind_speed_unit=mph&timezone=auto&forecast_days=7"
            f"&past_days=1"
        ).json()

    aq=requests.get(
        f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
        f"&current=us_aqi,pm2_5,grass_pollen,tree_pollen"
    ).json()

    meta={"lat":lat,"lon":lon,"name":name,"country":country}
    return wx_f,wx_display,aq,meta

# ── Session state ─────────────────────────────────────────────────────────────
for k,v in [("history",[]),("city_input",""),("chat_messages",[]),
             ("weather_ctx",None),("dark_mode",False),("last_updated",None),
             ("outfit_memory",{})]:
    if k not in st.session_state: st.session_state[k]=v

def add_history(name):
    if name not in st.session_state.history: st.session_state.history.insert(0,name)
    st.session_state.history=st.session_state.history[:6]

import streamlit.components.v1 as components

# ── Header ────────────────────────────────────────────────────────────────────
c1,c2=st.columns([5,1])
with c1: st.markdown('<p style="font-size:28px;font-weight:900;color:white;margin:0 0 4px;letter-spacing:-1px;">🌤️ NimbusAI</p>',unsafe_allow_html=True)
with c2: st.session_state.dark_mode=st.toggle("🌙",value=st.session_state.dark_mode,help="Dark mode")

if st.session_state.dark_mode:
    st.markdown("<style>.stApp{filter:brightness(0.6) saturate(0.7) !important;}</style>",unsafe_allow_html=True)

unit=st.radio("",["°F","°C"],horizontal=True,label_visibility="collapsed")

# ── Geolocation (fast) ────────────────────────────────────────────────────────
components.html("""
<div style="margin-bottom:10px;">
  <button onclick="getLocation()" id="geo-btn" style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.35);
    border-radius:12px;color:white;font-family:Outfit,sans-serif;font-size:13px;font-weight:600;
    padding:6px 16px;cursor:pointer;">📍 Use My Location</button>
  <span id="gs" style="color:rgba(255,255,255,0.6);font-size:12px;margin-left:10px;"></span>
</div>
<script>
function setCity(name){
  var inp=window.parent.document.querySelectorAll('input[type="text"]')[0];
  if(inp){var nv=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value');nv.set.call(inp,name);inp.dispatchEvent(new Event('input',{bubbles:true}));}
}
function getLocation(){
  var btn=document.getElementById('geo-btn'),gs=document.getElementById('gs');
  btn.disabled=true; btn.innerText='⏳ Detecting…'; gs.innerText='';
  navigator.geolocation.getCurrentPosition(function(p){
    gs.innerText='📡 Looking up city…';
    fetch('https://api.bigdatacloud.net/data/reverse-geocode-client?latitude='+p.coords.latitude+'&longitude='+p.coords.longitude+'&localityLanguage=en')
    .then(r=>r.json()).then(d=>{
      var city=d.city||d.locality||d.principalSubdivision||'';
      if(city){gs.innerText='✅ '+city; setCity(city);}
      else{gs.innerText='⚠️ Could not find city name';}
      btn.innerText='📍 Use My Location'; btn.disabled=false;
    }).catch(function(){gs.innerText='⚠️ Lookup failed'; btn.innerText='📍 Use My Location'; btn.disabled=false;});
  },function(err){
    if(err.code===1) gs.innerText='❌ Permission denied';
    else gs.innerText='❌ Could not detect location';
    btn.innerText='📍 Use My Location'; btn.disabled=false;
  },{enableHighAccuracy:false,timeout:5000,maximumAge:60000});
}
</script>""",height=60)

if st.session_state.history:
    st.markdown(f'<div class="chip-row">'+''.join(f'<span class="chip">🕐 {c}</span>' for c in st.session_state.history)+'</div>',unsafe_allow_html=True)

city_typed=st.text_input("",placeholder="Search a city...",label_visibility="collapsed",value=st.session_state.city_input)
fetch_city=city_typed.strip()

# ── Main display ──────────────────────────────────────────────────────────────
if fetch_city:
    with st.spinner("Fetching real weather..."):
        result=fetch_weather(fetch_city,unit)
        if result[0] is None:
            st.error("❌ City not found! Try a different spelling.")
            st.stop()
        wx_f,wx_display,aq,meta=result
        lat,lon,city_name,country=meta["lat"],meta["lon"],meta["name"],meta["country"]

        aqi=aq.get("current",{}).get("us_aqi",None)
        pm25=aq.get("current",{}).get("pm2_5",None)
        grass_pollen=aq.get("current",{}).get("grass_pollen",None)
        tree_pollen=aq.get("current",{}).get("tree_pollen",None)

        cur_f=wx_f["current"]; cur_d=wx_display["current"]
        daily_f=wx_f["daily"]; daily_d=wx_display["daily"]

        temp_f=cur_f["temperature_2m"]; feels_f=cur_f["apparent_temperature"]
        wind_mph=cur_f["wind_speed_10m"]; gusts_mph=cur_f.get("wind_gusts_10m",wind_mph)
        wind_deg=cur_f.get("wind_direction_10m",None)
        code=cur_f["weather_code"]; humidity=cur_f["relative_humidity_2m"]
        rain_pct=cur_f.get("precipitation_probability",0); uv=cur_f.get("uv_index",0)
        vis_m=cur_f.get("visibility",None); vis_km=round(vis_m/1000,1) if vis_m else None
        condition_str=WMO_CODES.get(code,"Unknown")
        wind_dir_str=wind_dir_label(wind_deg)

        temp_d=cur_d["temperature_2m"]; feels_d=cur_d["apparent_temperature"]

        # past_days=1 means index 0 = yesterday, index 1 = today
        # daily arrays: [yesterday, today, tomorrow, ...]
        hi_d=round(daily_d["temperature_2m_max"][1]); lo_d=round(daily_d["temperature_2m_min"][1])
        hi_f_val=daily_f["temperature_2m_max"][1]; lo_f_val=daily_f["temperature_2m_min"][1]
        yest_hi_f=daily_f["temperature_2m_max"][0]; yest_lo_f=daily_f["temperature_2m_min"][0]
        yest_rain=daily_f.get("precipitation_probability_max",[0]*7)[0]

        t_code=daily_f["weather_code"][2] if len(daily_f["weather_code"])>2 else code
        t_hi_f=daily_f["temperature_2m_max"][2] if len(daily_f["temperature_2m_max"])>2 else hi_f_val
        t_rain_arr=daily_f.get("precipitation_probability_max",[rain_pct]*7)
        t_rain=t_rain_arr[2] if len(t_rain_arr)>2 else rain_pct
        t_hi_d=round(daily_d["temperature_2m_max"][2]) if len(daily_d.get("temperature_2m_max",[]))>2 else hi_d
        t_lo_d=round(daily_d["temperature_2m_min"][2]) if len(daily_d.get("temperature_2m_min",[]))>2 else lo_d

        # sunrise/sunset (index 1 = today with past_days=1)
        try:
            sr_raw=daily_f.get("sunrise",["",""])[1]
            ss_raw=daily_f.get("sunset",["",""])[1]
            sr_fmt=datetime.strptime(sr_raw,"%Y-%m-%dT%H:%M").strftime("%I:%M %p")
            ss_fmt=datetime.strptime(ss_raw,"%Y-%m-%dT%H:%M").strftime("%I:%M %p")
        except: sr_fmt,ss_fmt="N/A","N/A"

        tz_str=wx_f.get("timezone","UTC")
        local_now=datetime.now(ZoneInfo(tz_str))
        now_h=local_now.hour

        # hourly — with past_days=1, hourly has 48 hours; slice [24:48] for today
        h_slice=slice(24,48)
        hourly_temps_f=wx_f["hourly"]["temperature_2m"][h_slice]
        hourly_feels_f=wx_f["hourly"].get("apparent_temperature",wx_f["hourly"]["temperature_2m"])[h_slice]
        hourly_temps_d=wx_display["hourly"]["temperature_2m"][h_slice]
        hourly_feels_d=wx_display["hourly"].get("apparent_temperature",wx_display["hourly"]["temperature_2m"])[h_slice]
        hourly_rain_vals=wx_f["hourly"]["precipitation_probability"][h_slice]
        hourly_wind=wx_f["hourly"]["wind_speed_10m"][h_slice]
        hourly_times=wx_f["hourly"]["time"][h_slice]
        hour_labels=[datetime.strptime(t,"%Y-%m-%dT%H:%M").strftime("%-I%p").lower() for t in hourly_times]

        # weekly sparkline (today onward, indices 1-7)
        week_hi_f=daily_f["temperature_2m_max"][1:7]
        week_lo_f=daily_f["temperature_2m_min"][1:7]
        week_hi_d=daily_d["temperature_2m_max"][1:7]

        # best window
        best_i,best_window_str=best_outdoor_window(hourly_temps_f,hourly_rain_vals,hourly_wind,hour_labels)

        # yesterday comparison
        yesterday_change=what_changed_yesterday(hi_f_val,lo_f_val,t_rain_arr[1] if len(t_rain_arr)>1 else rain_pct,
                                                 yest_hi_f,yest_lo_f,yest_rain,unit)

        fgi,fgi_lbl,fgi_col=feel_good_index(temp_f,humidity,wind_mph)
        moon_icon,moon_name=get_moon_phase(datetime.now())
        aqi_text,aqi_color=aqi_label(aqi)

        # Store full context for chat
        st.session_state.weather_ctx={
            "temp_f":temp_f,"feels_f":feels_f,"condition":condition_str,
            "wind_mph":wind_mph,"gusts_mph":gusts_mph,"wind_dir":wind_dir_str,
            "rain_pct":rain_pct,"hi_f":hi_f_val,"lo_f":lo_f_val,
            "city":city_name,"uv":round(uv),"code":code,"humidity":humidity,
            "visibility_km":vis_km,"fgi":fgi,"aqi":aqi_text,
            "grass_pollen":pollen_label(grass_pollen,"grass"),
            "tree_pollen":pollen_label(tree_pollen,"tree"),
            "moon_name":moon_name,"sunrise":sr_fmt,"sunset":ss_fmt,
            "best_window":best_window_str,
            "tomorrow_cond":WMO_CODES.get(t_code,""),"tomorrow_hi_f":t_hi_f,
            "tomorrow_rain_pct":t_rain,"tomorrow_code":t_code,
        }

        sky_bg=sky_class(code)
        st.session_state.last_sky=sky_bg
        st.session_state.last_updated=local_now.strftime("%I:%M %p")
        add_history(city_name)
        st.markdown(f"<style>.stApp{{background:{SKY_GRADIENTS.get(sky_bg,SKY_GRADIENTS['sky-clear'])} !important;}}</style>",unsafe_allow_html=True)
        st.markdown(make_particles(sky_bg),unsafe_allow_html=True)

        alt_t=f"/ {to_c(temp_f)}°C" if unit=="°F" else f"/ {to_f(temp_d)}°F"
        alt_f2=f"/ {to_c(feels_f)}°C" if unit=="°F" else f"/ {to_f(feels_d)}°F"

        # ── Hero ──────────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="hero-card">
          <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px;">
            <span style="font-size:32px;font-weight:800;color:white;letter-spacing:-1px;">{local_now.strftime("%I:%M %p")}</span>
            <span style="font-size:13px;color:rgba(255,255,255,0.6);">{local_now.strftime("%a, %b %d")}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.4);margin-left:auto;">Updated {st.session_state.last_updated}</span>
          </div>
          <div class="hero-city">📍 {city_name}, {country}</div>
          <div class="hero-cond">{condition_str}</div>
          <div style="display:flex;align-items:flex-end;gap:16px;margin-top:8px;flex-wrap:wrap;">
            <div>
              <div class="hero-temp">{round(temp_d)}{unit}</div>
              <div class="dual-temp">{alt_t}</div>
            </div>
            <div style="padding-bottom:10px;">
              <div style="font-size:14px;color:rgba(255,255,255,0.7);margin-top:4px;">Feels like {round(feels_d)}{unit} <span style="font-size:12px;color:rgba(255,255,255,0.5);">{alt_f2}</span></div>
              <div><span class="hilo-badge">🔴 {hi_d}{unit}</span><span class="hilo-badge">🔵 {lo_d}{unit}</span></div>
            </div>
          </div>
        </div>""",unsafe_allow_html=True)

        rc1,rc2=st.columns([1,5])
        with rc1:
            if st.button("🔄 Refresh"): st.rerun()

        if code in SEVERE_CODES:
            st.markdown(f'<div class="warn-box"><strong>⚠️ SEVERE WEATHER ALERT</strong><br>{SEVERE_MESSAGES.get(code,"Stay safe!")}</div>',unsafe_allow_html=True)

        # ── Yesterday comparison ──────────────────────────────────────────────
        st.markdown(f'<div class="info-box"><div class="box-title">📅 What Changed Since Yesterday</div>{yesterday_change}</div>',unsafe_allow_html=True)

        # ── Best outdoor window ───────────────────────────────────────────────
        st.markdown(f'<div class="ai-box"><div class="box-title">🌟 Best Time to Go Outside</div>{best_window_str}</div>',unsafe_allow_html=True)

        # ── AI summary ────────────────────────────────────────────────────────
        st.markdown(f'<div class="ai-box"><div class="box-title">✨ Weather Summary</div>{ai_comment(temp_f,condition_str,wind_mph)}</div>',unsafe_allow_html=True)

        # ── Feels-like reason ─────────────────────────────────────────────────
        st.markdown(f'<div class="glass-card"><div class="box-title">🌡️ Why Does It Feel Like That?</div><div style="font-size:14px;color:white;">{feels_like_reason(temp_f,humidity,wind_mph)}</div></div>',unsafe_allow_html=True)

        # ── Tomorrow preview ──────────────────────────────────────────────────
        t_icon=WMO_CODES.get(t_code,"🌡️").split()[0]
        t_cond_str=WMO_CODES.get(t_code,"Unknown")
        t_alt_hi=f"/ {to_c(round(t_hi_f))}°C" if unit=="°F" else f"/ {to_f(t_hi_d)}°F"
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
        </div>""",unsafe_allow_html=True)

        # ── Share ─────────────────────────────────────────────────────────────
        share_text=(f"📍 {city_name}, {country} — {condition_str}\\n"
                    f"🌡️ {round(temp_d)}{unit} (feels {round(feels_d)}{unit})\\n"
                    f"🔴 High {hi_d}{unit}  🔵 Low {lo_d}{unit}\\n"
                    f"💧 {humidity}% humidity  💨 {round(wind_mph)} mph {wind_dir_str}\\n"
                    f"🌧️ {rain_pct}% rain  🌞 UV {round(uv)}\\n"
                    f"Shared via NimbusAI 🌤️")
        st.markdown(f"""<button onclick="navigator.clipboard.writeText('{share_text}').then(()=>{{this.innerText='✅ Copied!';setTimeout(()=>this.innerText='📋 Share Weather',2000)}})"
          style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.35);border-radius:12px;
                 color:white;font-family:Outfit,sans-serif;font-size:13px;font-weight:600;
                 padding:8px 20px;cursor:pointer;margin-bottom:14px;">📋 Share Weather</button>""",unsafe_allow_html=True)

        # ── What to wear + outfit SVG ─────────────────────────────────────────
        wear_items=what_to_wear(temp_f,condition_str,wind_mph)
        svg_fig=outfit_svg(temp_f,condition_str)
        wc1,wc2=st.columns([1,2])
        with wc1:
            st.markdown(
                f'<div class="glass-card" style="text-align:center;padding:12px;">'
                f'<div class="box-title">👤 Outfit Preview</div>'
                f'{svg_fig}</div>',
                unsafe_allow_html=True
            )
        with wc2:
            st.markdown(
                f'<div class="wear-box"><div class="box-title">👗 What to Wear</div>'
                f'{"<br>".join(wear_items)}</div>',
                unsafe_allow_html=True
            )

        # Outfit memory
        outfit_key=f"{round(temp_f//10)*10}"
        saved=st.session_state.outfit_memory.get(outfit_key)
        with st.expander("💾 Save Your Own Outfit for This Temperature Range"):
            outfit_input=st.text_input("What are you wearing today?",value=saved or "",placeholder="e.g. jeans, hoodie, sneakers",key="outfit_inp")
            if st.button("Save Outfit"):
                st.session_state.outfit_memory[outfit_key]=outfit_input
                st.success(f"✅ Saved for {round(temp_f//10)*10}–{round(temp_f//10)*10+9}°F!")
        if saved:
            st.markdown(f'<div class="glass-card"><div class="box-title">💡 Your Saved Outfit</div><div style="color:white;font-size:14px;">👕 {saved}</div></div>',unsafe_allow_html=True)

        # ── Feel-good index ───────────────────────────────────────────────────
        st.markdown(f"""<div class="glass-card" style="display:flex;align-items:center;gap:20px;">
          <svg width="80" height="80" viewBox="0 0 80 80">
            <circle cx="40" cy="40" r="34" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="8"/>
            <circle cx="40" cy="40" r="34" fill="none" stroke="{fgi_col}" stroke-width="8"
              stroke-dasharray="213.6" stroke-dashoffset="{213.6-(fgi/100)*213.6:.1f}"
              stroke-linecap="round" transform="rotate(-90 40 40)"/>
            <text x="40" y="45" text-anchor="middle" font-size="18" font-weight="900" fill="white" font-family="Outfit,sans-serif">{fgi}</text>
          </svg>
          <div>
            <div class="box-title">😊 Feel-Good Index</div>
            <div style="font-size:20px;font-weight:700;color:{fgi_col};">{fgi_lbl}</div>
            <div class="glass-sub">Temp 50% · Humidity 30% · Wind 20%</div>
          </div>
        </div>""",unsafe_allow_html=True)

        # ── Humidity comfort ──────────────────────────────────────────────────
        hum_msg,hum_col=humidity_comfort(humidity)
        st.markdown(f'<div class="glass-card"><div class="box-title">💧 Humidity Comfort</div><div style="font-size:14px;color:{hum_col};">{hum_msg}</div><div class="glass-sub">{humidity}% relative humidity</div></div>',unsafe_allow_html=True)

        # ── Stats grid ────────────────────────────────────────────────────────
        vis_str=f"{vis_km} km" if vis_km is not None else "N/A"
        c1,c2,c3,c4=st.columns(4)
        for col,(ico,lbl,val,sub) in zip([c1,c2,c3,c4],[
            ("💧","Humidity",f"{humidity}%",""),
            ("💨","Wind",f"{round(wind_mph)} mph",f"{wind_dir_str} · Gusts {round(gusts_mph)} mph"),
            ("🌧️","Rain",f"{rain_pct}%","chance today"),
            ("👁️","Visibility",vis_str,""),
        ]):
            with col: st.markdown(f'<div class="glass-card"><div class="glass-label">{ico} {lbl}</div><div class="glass-value" style="font-size:18px;">{val}</div><div class="glass-sub">{sub}</div></div>',unsafe_allow_html=True)

        c5,c6=st.columns(2)
        with c5: st.markdown(f'<div class="glass-card"><div class="glass-label">🌞 UV Index</div><div class="glass-value">{round(uv)}</div><div class="glass-sub">out of 11</div></div>',unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="glass-card"><div class="glass-label">🌬️ Wind Direction</div><div class="glass-value">{wind_dir_str}</div><div class="glass-sub">{round(wind_deg or 0)}°</div></div>',unsafe_allow_html=True)

        # ── Pollen ────────────────────────────────────────────────────────────
        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px;">
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌾 Grass Pollen</div><div class="glass-value" style="font-size:15px;">{pollen_label(grass_pollen,"grass")}</div></div>
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌳 Tree Pollen</div><div class="glass-value" style="font-size:15px;">{pollen_label(tree_pollen,"tree")}</div></div>
        </div>""",unsafe_allow_html=True)

        # ── 5-day forecast + weekly sparkline ─────────────────────────────────
        st.markdown('<p style="color:white;font-weight:700;font-size:14px;margin:10px 0 8px;">📅 5-DAY FORECAST</p>',unsafe_allow_html=True)
        fc='<div class="forecast-row">'
        for i in range(5):
            idx=i+1  # +1 because past_days=1 shifts daily arrays
            dn="Today" if i==0 else datetime.strptime(daily_f["time"][idx],"%Y-%m-%d").strftime("%a")
            di=WMO_CODES.get(daily_f["weather_code"][idx],"🌡️").split()[0]
            dh=round(daily_d["temperature_2m_max"][idx]); dl=round(daily_d["temperature_2m_min"][idx])
            dhf=round(daily_f["temperature_2m_max"][idx]); dlf=round(daily_f["temperature_2m_min"][idx])
            au="°C" if unit=="°F" else "°F"
            dha=to_c(dhf) if unit=="°F" else to_f(dh); dla=to_c(dlf) if unit=="°F" else to_f(dl)
            fc+=f'<div class="forecast-day"><div class="day-name">{dn}</div><div class="day-icon">{di}</div><div class="day-hi">{dh}{unit}</div><div class="day-lo">{dl}{unit}</div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px;">{dha}/{dla}{au}</div></div>'
        st.markdown(fc+"</div>",unsafe_allow_html=True)

        # Weekly trend sparkline
        trend_up=week_hi_f[-1]>week_hi_f[0]
        trend_label=f"📈 Warming trend this week" if trend_up else f"📉 Cooling trend this week"
        spark_color="#f87171" if trend_up else "#60a5fa"
        st.markdown(f'<div class="glass-card"><div class="box-title">📊 Weekly High Temperature Trend</div>{make_sparkline(week_hi_d,spark_color)}<div class="glass-sub" style="margin-top:6px;">{trend_label}</div></div>',unsafe_allow_html=True)

        # ── Sunrise / Sunset arc ──────────────────────────────────────────────
        st.markdown(make_sun_arc(local_now,sr_fmt,ss_fmt),unsafe_allow_html=True)

        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px;">
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌅 Sunrise</div><div class="glass-value">{sr_fmt}</div></div>
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌇 Sunset</div><div class="glass-value">{ss_fmt}</div></div>
        </div>""",unsafe_allow_html=True)

        # ── Charts ────────────────────────────────────────────────────────────
        chart_temp  = make_chart(hourly_temps_d,"white","ag","rgba(255,255,255,0.25)",unit,now_h,hour_labels,highlight_i=best_i)
        chart_feels = make_chart(hourly_feels_d,"rgba(255,200,100,0.9)","flg","rgba(255,180,60,0.3)",unit,now_h,hour_labels)
        chart_rain  = make_chart(hourly_rain_vals,"rgba(150,210,255,0.9)","rg","rgba(100,180,255,0.4)","%",now_h,hour_labels,fixed_min=0,fixed_max=100)
        chart_wind  = make_chart(hourly_wind,"rgba(200,240,200,0.9)","wg","rgba(150,220,150,0.3)"," mph",now_h,hour_labels)

        st.markdown(
            f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:6px;">'
            f'<div class="box-title">🌡️ Hourly Temperature '
            f'<span style="font-size:9px;color:rgba(255,255,255,0.4);">★ shaded = best outdoor window</span></div>'
            f'{chart_temp}</div>',
            unsafe_allow_html=True)
        st.markdown(
            f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:6px;">'
            f'<div class="box-title">🥵 Hourly Feels Like</div>{chart_feels}</div>',
            unsafe_allow_html=True)
        st.markdown(
            f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:6px;">'
            f'<div class="box-title">🌧️ Hourly Rain Probability</div>{chart_rain}</div>',
            unsafe_allow_html=True)
        st.markdown(
            f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:12px;">'
            f'<div class="box-title">💨 Hourly Wind Speed</div>{chart_wind}</div>',
            unsafe_allow_html=True)

        # ── Moon + AQI ────────────────────────────────────────────────────────
        pm_text=f"{pm25:.1f} µg/m³" if pm25 is not None else "N/A"
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
        </div>""",unsafe_allow_html=True)

        # ── Map ───────────────────────────────────────────────────────────────
        st.markdown('<div class="box-title" style="color:rgba(255,255,255,0.6);margin-bottom:6px;">🗺️ WEATHER MAP</div>',unsafe_allow_html=True)
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
        </script></div>""",height=270)

        # ── City comparison ───────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🆚 Compare With Another City</p>',unsafe_allow_html=True)
        compare_input=st.text_input("",placeholder="Enter another city to compare...",label_visibility="collapsed",key="compare_inp")
        if compare_input.strip():
            with st.spinner("Fetching comparison..."):
                res2=fetch_weather(compare_input.strip(),unit)
                if res2[0] is None:
                    st.warning("⚠️ Comparison city not found.")
                else:
                    wx2_f,wx2_d,_,meta2=res2
                    cur2_f=wx2_f["current"]; cur2_d=wx2_d["current"]
                    t2=cur2_f["temperature_2m"]; t2_d=cur2_d["temperature_2m"]
                    w2=cur2_f["wind_speed_10m"]; r2=cur2_f.get("precipitation_probability",0)
                    h2=cur2_f["relative_humidity_2m"]; u2=cur2_f.get("uv_index",0)
                    c2_code=cur2_f["weather_code"]
                    fgi2,fgi2_lbl,fgi2_col=feel_good_index(t2,h2,w2)
                    alt2=f"/ {to_c(t2)}°C" if unit=="°F" else f"/ {to_f(t2_d)}°F"
                    ca,cb=st.columns(2)
                    with ca:
                        st.markdown(f"""<div class="compare-col">
                          <div style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);margin-bottom:8px;">📍 {city_name}</div>
                          <div style="font-size:32px;font-weight:900;color:white;">{round(temp_d)}{unit}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);">{alt_t}</div>
                          <div style="font-size:13px;color:white;margin-top:6px;">{condition_str}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">💧{humidity}% &nbsp;💨{round(wind_mph)}mph &nbsp;🌧️{rain_pct}%</div>
                          <div style="font-size:12px;color:{fgi_col};margin-top:4px;">😊 {fgi}/100 — {fgi_lbl}</div>
                        </div>""",unsafe_allow_html=True)
                    with cb:
                        st.markdown(f"""<div class="compare-col">
                          <div style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.7);margin-bottom:8px;">📍 {meta2['name']}, {meta2['country']}</div>
                          <div style="font-size:32px;font-weight:900;color:white;">{round(t2_d)}{unit}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);">{alt2}</div>
                          <div style="font-size:13px;color:white;margin-top:6px;">{WMO_CODES.get(c2_code,'Unknown')}</div>
                          <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">💧{h2}% &nbsp;💨{round(w2)}mph &nbsp;🌧️{r2}%</div>
                          <div style="font-size:12px;color:{fgi2_col};margin-top:4px;">😊 {fgi2}/100 — {fgi2_lbl}</div>
                        </div>""",unsafe_allow_html=True)
                    winner=f"🏆 {city_name} has better weather!" if fgi>fgi2 else (f"🏆 {meta2['name']} has better weather!" if fgi2>fgi else "🤝 Both cities feel about the same!")
                    st.markdown(f'<div class="ai-box" style="margin-top:8px;">{winner}</div>',unsafe_allow_html=True)

        st.markdown('<p class="footer">Open-Meteo API • Air Quality API • OpenStreetMap • Anthropic Claude • No paid API keys needed 😄</p>',unsafe_allow_html=True)

# ── Chat box ──────────────────────────────────────────────────────────────────
if st.session_state.weather_ctx:
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:2px;">💬 Ask NimbusAI Anything</p>',unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.55);font-size:12px;margin-bottom:10px;">Powered by Claude AI · Ask anything about weather, forecasts, activities, science, climate — anything!</p>',unsafe_allow_html=True)

    # Export chat
    if st.session_state.chat_messages:
        export_text="\\n".join(f"{'You' if m['role']=='user' else 'NimbusAI'}: {m['content']}" for m in st.session_state.chat_messages)
        cb1,cb2,cb3=st.columns([4,1,1])
        with cb2:
            st.markdown(f"""<button onclick="navigator.clipboard.writeText(`{export_text.replace('`',"'")}`).then(()=>{{this.innerText='✅';setTimeout(()=>this.innerText='📋 Export',1500)}})"
              style="background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.3);border-radius:10px;
                     color:white;font-family:Outfit,sans-serif;font-size:12px;padding:5px 10px;cursor:pointer;width:100%;">📋 Export</button>""",unsafe_allow_html=True)
        with cb3:
            if st.button("🗑️ Clear"):
                st.session_state.chat_messages=[]
                st.rerun()

        # Chat history with auto-scroll
        chat_html='<div class="chat-container" id="chat-box">'
        for msg in st.session_state.chat_messages[-16:]:
            if msg["role"]=="user":
                chat_html+=f'<div class="chat-name-user">YOU</div><div class="chat-msg-user">{msg["content"]}</div>'
            else:
                chat_html+=f'<div class="chat-name-bot">🌤️ NIMBUS</div><div class="chat-msg-bot">{msg["content"]}</div>'
        chat_html+='</div><script>var cb=document.getElementById("chat-box");if(cb)cb.scrollTop=cb.scrollHeight;</script>'
        st.markdown(chat_html,unsafe_allow_html=True)

    with st.form(key="chat_form",clear_on_submit=True):
        fc1,fc2=st.columns([5,1])
        with fc1: user_q=st.text_input("",placeholder="Ask anything about weather...",label_visibility="collapsed")
        with fc2: send=st.form_submit_button("Send ➤")

    if send and user_q.strip():
        # Add user message
        st.session_state.chat_messages.append({"role":"user","content":user_q.strip()})
        # Get AI response
        with st.spinner("NimbusAI is thinking..."):
            answer=chat_with_ai(st.session_state.chat_messages,st.session_state.weather_ctx)
        st.session_state.chat_messages.append({"role":"assistant","content":answer})
        st.rerun()
