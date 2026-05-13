import streamlit as st
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import math, random

st.set_page_config(page_title="NimbusAI", page_icon="🌤️", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<div style="display:none"><style>
* { font-family:'Outfit',sans-serif !important; }
.stApp { background:linear-gradient(160deg,#1a6eff 0%,#38b6ff 55%,#87ceeb 100%) !important; min-height:100vh; transition:background 1.2s ease !important; }
[data-testid="stAppViewContainer"],[data-testid="stHeader"],[data-testid="stMain"] { background:transparent !important; }
.hero-card   { border-radius:24px; padding:32px 28px 24px; color:white; margin-bottom:16px; background:rgba(0,0,0,0.30); box-shadow:0 8px 32px rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.25); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); position:relative; z-index:10; }
.hero-temp   { font-size:84px; font-weight:900; line-height:1; letter-spacing:-4px; text-shadow:0 4px 20px rgba(0,0,0,0.2); color:white; }
.hero-city   { font-size:20px; font-weight:600; color:white; margin-bottom:2px; }
.hero-cond   { font-size:15px; font-weight:300; color:rgba(255,255,255,0.85); }
.hilo-badge  { display:inline-flex; align-items:center; gap:6px; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.35); border-radius:30px; padding:5px 14px; font-size:14px; font-weight:600; color:white; margin-right:8px; margin-top:12px; }
.glass-card  { background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:16px 18px; color:white; margin-bottom:12px; backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }
.glass-label { font-size:11px; font-weight:700; letter-spacing:1.2px; color:rgba(255,255,255,0.65); text-transform:uppercase; margin-bottom:4px; }
.glass-value { font-size:22px; font-weight:700; color:white; }
.glass-sub   { font-size:12px; color:rgba(255,255,255,0.6); margin-top:2px; }
.ai-box      { border-radius:16px; padding:16px 20px; font-size:15px; font-weight:500; margin-bottom:12px; border:1px solid rgba(255,255,255,0.25); background:rgba(0,0,0,0.28); color:white; backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }
.wear-box    { border-radius:16px; padding:16px 20px; font-size:14px; line-height:1.9; margin-bottom:12px; border:1px solid rgba(255,255,255,0.25); background:rgba(0,0,0,0.28); color:white; backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }
.warn-box    { border-radius:16px; padding:16px 20px; background:rgba(180,20,20,0.35); border:1px solid rgba(255,120,120,0.5); color:white; margin-bottom:12px; font-size:14px; }
.info-box    { border-radius:16px; padding:14px 18px; background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2); color:white; margin-bottom:12px; font-size:14px; backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }
.box-title   { font-size:10px; letter-spacing:1.4px; color:rgba(255,255,255,0.6); font-weight:700; margin-bottom:8px; text-transform:uppercase; }
.tomorrow-card { border-radius:16px; padding:16px 20px; background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2); color:white; margin-bottom:12px; backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }
.forecast-row  { display:flex; gap:8px; margin-bottom:12px; }
.forecast-day  { flex:1; background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2); border-radius:14px; padding:12px 6px; text-align:center; color:white; min-width:52px; backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px); }
.day-name { font-size:11px; font-weight:700; color:rgba(255,255,255,0.7); margin-bottom:4px; }
.day-icon { font-size:22px; margin-bottom:4px; }
.day-hi   { font-size:13px; font-weight:700; color:white; }
.day-lo   { font-size:11px; color:rgba(255,255,255,0.55); margin-top:2px; }
.chip-row { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px; }
.chip     { background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.25); border-radius:20px; padding:4px 12px; font-size:12px; color:white; position:relative; z-index:10; }
.footer   { font-size:11px; color:rgba(255,255,255,0.5); text-align:center; margin-top:8px; }
.dual-temp { font-size:13px; color:rgba(255,255,255,0.6); font-weight:400; margin-left:6px; }
.compare-col { background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.2); border-radius:16px; padding:16px; margin-bottom:12px; backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); position:relative; z-index:10; }
.sparkline-row { display:flex; gap:3px; align-items:flex-end; height:36px; margin-top:6px; }
.spark-bar { flex:1; border-radius:3px 3px 0 0; min-height:4px; }
@keyframes float-cloud { 0%{transform:translateX(-120px)} 100%{transform:translateX(110vw)} }
@keyframes fall-rain   { 0%{transform:translateY(-20px);opacity:0.7} 100%{transform:translateY(110vh);opacity:0} }
@keyframes fall-snow   { 0%{transform:translateY(-20px) rotate(0deg);opacity:0.8} 100%{transform:translateY(110vh) rotate(360deg);opacity:0} }
@keyframes flash       { 0%,90%,100%{opacity:0} 92%,98%{opacity:1} }
.weather-particles { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; overflow:hidden; }
.cloud-particle { position:absolute; animation:float-cloud linear infinite; opacity:0.12; }
.rain-particle  { position:absolute; width:2px; border-radius:2px; background:rgba(200,230,255,0.5); animation:fall-rain linear infinite; }
.snow-particle  { position:absolute; font-size:14px; animation:fall-snow linear infinite; color:white; opacity:0.7; }
.lightning      { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(255,255,200,0.1); pointer-events:none; z-index:0; animation:flash 4s infinite; }
/* Ensure all Streamlit content sits above particles */
.main .block-container { position:relative; z-index:10; }
[data-testid="stVerticalBlock"] { position:relative; z-index:10; }
[data-testid="stHorizontalBlock"] { position:relative; z-index:10; }
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
@media(max-width:600px){ .hero-temp { font-size:56px !important; } .forecast-row { flex-wrap:wrap !important; } .forecast-day { min-width:56px !important; } }
</style></div>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
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

# ── Helpers ────────────────────────────────────────────────────────────────────
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
    if humidity>80: return "💦 Very humid — muggy and uncomfortable.","#f87171"
    if humidity>70: return "😓 Humid — may feel sticky and warm.","#fb923c"
    if humidity<20: return "🏜️ Very dry — skin and eyes may feel irritated.","#f87171"
    if humidity<30: return "😐 Dry air — consider staying hydrated.","#facc15"
    return "✅ Comfortable humidity level.","#4ade80"

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
    if phase<0.0625: return "🌑","New Moon"
    if phase<0.1875: return "🌒","Waxing Crescent"
    if phase<0.3125: return "🌓","First Quarter"
    if phase<0.4375: return "🌔","Waxing Gibbous"
    if phase<0.5625: return "🌕","Full Moon"
    if phase<0.6875: return "🌖","Waning Gibbous"
    if phase<0.8125: return "🌗","Last Quarter"
    return "🌘","Waning Crescent"

def best_outdoor_window(hourly_temps_f, hourly_rain, hourly_wind, hour_labels):
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
    disp_hi=round(abs(hi_diff)*5/9) if unit=="°C" else round(abs(hi_diff))
    if abs(hi_diff)>=2: msgs.append(f"{'🌡️ Warmer' if hi_diff>0 else '❄️ Cooler'} today — high is {disp_hi}{unit} {'higher' if hi_diff>0 else 'lower'} than yesterday.")
    else: msgs.append("🌡️ Similar high temperature to yesterday.")
    rain_diff=today_rain-yesterday_rain
    if abs(rain_diff)>=15: msgs.append(f"{'🌧️ More rain' if rain_diff>0 else '☀️ Less rain'} expected vs yesterday ({abs(rain_diff):.0f}% {'more' if rain_diff>0 else 'less'}).")
    return " ".join(msgs) if msgs else "📅 Very similar conditions to yesterday."

# ── SVG chart with interactive hover tooltip ───────────────────────────────────
_chart_counter = [0]
def make_chart(values, color, grad_id, grad_color, unit_lbl, now_h, hour_labels,
               fixed_min=None, fixed_max=None, highlight_i=None):
    _chart_counter[0]+=1; uid=f"{grad_id}_{_chart_counter[0]}"; cid=f"chart_{uid}"
    W,H=680,160; PL,PR,PT,PB=36,10,16,32; CW,CH=W-PL-PR,H-PT-PB
    mn=(fixed_min if fixed_min is not None else min(values)-2)
    mx=(fixed_max if fixed_max is not None else max(values)+2)
    rng=mx-mn or 1
    def tx(i): return PL+(i/(len(values)-1))*CW
    def ty(v): return PT+CH-((v-mn)/rng)*CH
    pts=" ".join(f"{tx(i):.1f},{ty(v):.1f}" for i,v in enumerate(values))
    area=(f"M{tx(0):.1f},{ty(values[0]):.1f} "+" ".join(f"L{tx(i):.1f},{ty(v):.1f}" for i,v in enumerate(values))
          +f" L{tx(len(values)-1):.1f},{PT+CH} L{tx(0):.1f},{PT+CH} Z")
    xlbls="".join(f'<text x="{tx(i):.1f}" y="{PT+CH+18}" text-anchor="middle" font-size="10" fill="rgba(255,255,255,0.6)" font-family="Outfit,sans-serif">{hour_labels[i]}</text>' for i in range(0,24,3))
    ylbls="".join(f'<text x="{PL-4}" y="{ty(v):.1f}" text-anchor="end" dominant-baseline="middle" font-size="10" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{round(v)}{unit_lbl}</text>' for v in [mn+(mx-mn)*0.1,(mn+mx)/2,mx-(mx-mn)*0.1])
    dot=f'<circle cx="{tx(now_h):.1f}" cy="{ty(values[now_h]):.1f}" r="5" fill="white" stroke="rgba(255,255,255,0.4)" stroke-width="3"/>'
    dlbl=f'<text x="{tx(now_h):.1f}" y="{ty(values[now_h])-10:.1f}" text-anchor="middle" font-size="11" fill="white" font-weight="bold" font-family="Outfit,sans-serif">{round(values[now_h])}{unit_lbl}</text>'
    hi_rect=""
    if highlight_i is not None:
        x1=tx(highlight_i); x2=tx(min(highlight_i+2,23))
        hi_rect=f'<rect x="{x1:.1f}" y="{PT}" width="{x2-x1:.1f}" height="{CH}" fill="rgba(255,255,255,0.08)" rx="4"/>'

    # Build JS data arrays for tooltip
    xs_js  = "[" + ",".join(f"{tx(i):.1f}" for i in range(len(values))) + "]"
    ys_js  = "[" + ",".join(f"{ty(v):.1f}" for v in values) + "]"
    vals_js= "[" + ",".join(str(round(v,1)) for v in values) + "]"
    labs_js= "[" + ",".join(f'"{l}"' for l in hour_labels) + "]"

    svg = (f'<div id="wrap_{cid}" style="position:relative;width:100%;">'
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
           f'var xs={xs_js}, ys={ys_js}, vals={vals_js}, labs={labs_js};'
           f'var vl=document.getElementById("vline_{cid}");'
           f'var dc=document.getElementById("dot_{cid}");'
           f'var tb=document.getElementById("tbox_{cid}");'
           f'var tv=document.getElementById("tval_{cid}");'
           f'var tt=document.getElementById("ttime_{cid}");'
           f'var W={W},PL={PL},PR={PR},PT={PT},CH={CH};'
           f'function getIdx(mx){{'
           f'  var best=0,bd=999;'
           f'  for(var i=0;i<xs.length;i++){{var d=Math.abs(xs[i]-mx);if(d<bd){{bd=d;best=i;}}}}'
           f'  return best;'
           f'}}'
           f'svg.addEventListener("mousemove",function(e){{'
           f'  var r=svg.getBoundingClientRect();'
           f'  var svgW=r.width,svgH=r.height;'
           f'  var scaleX=W/svgW;'
           f'  var mx=(e.clientX-r.left)*scaleX;'
           f'  var idx=getIdx(mx);'
           f'  var x=xs[idx],y=ys[idx],v=vals[idx],lab=labs[idx];'
           f'  vl.setAttribute("x1",x);vl.setAttribute("x2",x);vl.setAttribute("visibility","visible");'
           f'  dc.setAttribute("cx",x);dc.setAttribute("cy",y);dc.setAttribute("visibility","visible");'
           f'  var tbw=88,tbh=36,tbx=x-tbw/2,tby=y-tbh-10;'
           f'  if(tbx<2)tbx=2; if(tbx+tbw>W-2)tbx=W-tbw-2;'
           f'  if(tby<2)tby=y+12;'
           f'  tb.setAttribute("x",tbx);tb.setAttribute("y",tby);tb.setAttribute("width",tbw);tb.setAttribute("visibility","visible");'
           f'  tv.setAttribute("x",tbx+tbw/2);tv.setAttribute("y",tby+14);tv.setAttribute("visibility","visible");tv.textContent=v+"{unit_lbl}";'
           f'  tt.setAttribute("x",tbx+tbw/2);tt.setAttribute("y",tby+27);tt.setAttribute("visibility","visible");tt.textContent=lab;'
           f'}}); '
           f'svg.addEventListener("mouseleave",function(){{'
           f'  vl.setAttribute("visibility","hidden");'
           f'  dc.setAttribute("visibility","hidden");'
           f'  tb.setAttribute("visibility","hidden");'
           f'  tv.setAttribute("visibility","hidden");'
           f'  tt.setAttribute("visibility","hidden");'
           f'}});'
           f'}})();'
           f'</script>'
           f'</div>')
    return svg

def make_sparkline(values, color="#4ade80"):
    mn=min(values); mx=max(values); rng=mx-mn or 1
    bars="".join(f'<div class="spark-bar" style="height:{max(4,round(((v-mn)/rng)*32)+4)}px;background:{color};opacity:0.7;"></div>' for v in values)
    return f'<div class="sparkline-row">{bars}</div>'

def make_sun_arc(now_dt, sunrise_str, sunset_str):
    try:
        sr=datetime.strptime(sunrise_str,"%I:%M %p"); ss=datetime.strptime(sunset_str,"%I:%M %p")
        now_mins=now_dt.hour*60+now_dt.minute
        sr_mins=sr.hour*60+sr.minute; ss_mins=ss.hour*60+ss.minute
        day_len=ss_mins-sr_mins
        if day_len<=0: raise ValueError
        pct=max(0,min(1,(now_mins-sr_mins)/day_len))
        cx=20+pct*260; cy=80-math.sin(pct*math.pi)*55
        is_day=sr_mins<=now_mins<=ss_mins
        icon="☀️" if is_day else "🌙"
        return (f'<div class="glass-card" style="margin-bottom:12px;"><div class="box-title">🌅 Sun Position</div>'
                f'<svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">'
                f'<path d="M20 80 Q150 15 280 80" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="2" stroke-dasharray="6 4"/>'
                f'<path d="M20 80 Q{20+pct*130:.0f} {80-math.sin(pct*math.pi/2)*55:.0f} {cx:.0f} {cy:.0f}" fill="none" stroke="rgba(255,220,80,0.7)" stroke-width="2.5"/>'
                f'<text x="20" y="95" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{sunrise_str}</text>'
                f'<text x="280" y="95" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.55)" font-family="Outfit,sans-serif">{sunset_str}</text>'
                f'<text x="{cx:.0f}" y="{cy-6:.0f}" text-anchor="middle" font-size="20">{icon}</text>'
                f'</svg></div>')
    except: return ""

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

# ── Weather fetch ──────────────────────────────────────────────────────────────
def fetch_weather(city_name, unit):
    geo=requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1").json()
    if "results" not in geo or not geo["results"]: return None,None,None,None
    r=geo["results"][0]; lat,lon=r["latitude"],r["longitude"]; name=r["name"]; country=r.get("country","")
    wx_f=requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"wind_speed_10m,wind_gusts_10m,wind_direction_10m,weather_code,"
        f"precipitation_probability,uv_index,visibility"
        f"&hourly=temperature_2m,apparent_temperature,precipitation_probability,wind_speed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset,"
        f"precipitation_probability_max,precipitation_sum"
        f"&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=7&past_days=1"
    ).json()
    wx_display=wx_f
    if unit=="°C":
        wx_display=requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature&hourly=temperature_2m,apparent_temperature"
            f"&daily=temperature_2m_max,temperature_2m_min"
            f"&temperature_unit=celsius&wind_speed_unit=mph&timezone=auto&forecast_days=7&past_days=1"
        ).json()
    aq=requests.get(
        f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
        f"&current=us_aqi,pm2_5,grass_pollen,tree_pollen"
    ).json()
    return wx_f,wx_display,aq,{"lat":lat,"lon":lon,"name":name,"country":country}


# ═══════════════════════════════════════════════════════════════
# FEATURE 1 — FAVOURITE CITIES (3 slots)
# ═══════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════
# FEATURE 2 — ACTIVITY WEATHER SCORES
# ═══════════════════════════════════════════════════════════════
def activity_scores(temp_f, humidity, wind_mph, rain_pct, uv, condition):
    cond = condition.lower()
    is_raining = any(x in cond for x in ["rain","drizzle","shower","thunder"])
    is_sunny = "clear" in cond or "mainly clear" in cond

    def score(base): return max(0, min(10, round(base)))

    running  = score(8 - abs(temp_f-60)/8 - rain_pct/25 - max(0,wind_mph-15)/5)
    cycling  = score(8 - abs(temp_f-65)/8 - rain_pct/20 - max(0,wind_mph-12)/4)
    hiking   = score(9 - abs(temp_f-65)/7 - rain_pct/20 - max(0,uv-7)*0.5)
    picnic   = score(9 - abs(temp_f-72)/6 - rain_pct/15 - max(0,wind_mph-10)/4 - max(0,uv-8)*0.4)
    golf     = score(8 - abs(temp_f-68)/8 - rain_pct/20 - max(0,wind_mph-15)/5)
    swimming = score(7 + (temp_f-80)/5 - rain_pct/20 - (1 if is_raining else 0)*4)
    skiing   = score(8 if temp_f < 35 else max(0, 8-(temp_f-35)/5))
    bbq      = score(9 - abs(temp_f-75)/6 - rain_pct/12 - max(0,wind_mph-12)/4)

    activities = [
        ("🏃 Running",  running),
        ("🚴 Cycling",  cycling),
        ("🥾 Hiking",   hiking),
        ("🧺 Picnic",   picnic),
        ("⛳ Golf",     golf),
        ("🏊 Swimming", swimming),
        ("⛷️ Skiing",   skiing),
        ("🔥 BBQ",      bbq),
    ]

    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🏅 Activity Weather Scores</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, (name, sc) in enumerate(activities):
        color = "#4ade80" if sc>=7 else "#facc15" if sc>=4 else "#f87171"
        with cols[idx % 4]:
            st.markdown(f"""<div class="glass-card" style="text-align:center;padding:12px 8px;">
              <div style="font-size:13px;font-weight:600;color:white;margin-bottom:6px;">{name}</div>
              <div style="font-size:28px;font-weight:900;color:{color};">{sc}/10</div>
              <div style="font-size:10px;color:rgba(255,255,255,0.5);">{"✅ Great" if sc>=7 else "⚠️ OK" if sc>=4 else "❌ Poor"}</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 3 — WHAT TO PACK (trip packing list)
# ═══════════════════════════════════════════════════════════════
def render_packing_list():
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🧳 Trip Packing List</p>', unsafe_allow_html=True)
    with st.expander("Generate a packing list for your trip"):
        dest = st.text_input("Destination city", placeholder="e.g. Miami", key="pack_dest")
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
                    if t < 45:   pack += ["🧥 Heavy winter coat","🧤 Gloves + scarf","🥾 Warm boots","🧦 Thermal socks x" + str(nights)]
                    elif t < 65: pack += ["🧥 Light jacket","👖 Jeans x" + str(max(2,nights//2)),"👟 Closed-toe shoes"]
                    elif t < 80: pack += ["👕 T-shirts x" + str(nights),"👖 Light pants/shorts","👟 Comfortable sneakers"]
                    else:        pack += ["🩳 Shorts x" + str(nights),"👕 Light shirts x" + str(nights),"🕶️ Sunglasses","🧴 High SPF sunscreen","🧢 Hat"]
                    if any(x in cond for x in ["rain","drizzle","shower"]): pack += ["☔ Umbrella","🧥 Waterproof jacket"]
                    if "snow" in cond: pack += ["❄️ Snow boots","🧣 Scarf","🧤 Gloves"]
                    if t > 75:   pack += ["💧 Reusable water bottle","🏊 Swimwear"]
                    pack.append(f"💼 **For {nights} nights:** {nights+1} outfits recommended")
                    for item in pack:
                        st.markdown(f'<div class="info-box" style="margin-bottom:6px;">{item}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 4 — HOURLY FEELS-LIKE TABLE
# ═══════════════════════════════════════════════════════════════
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
            wear = "🧥" if t < 50 else "🧶" if t < 65 else "👕" if t < 80 else "🩳"
            if r > 50: wear += "☔"
            html += f'<tr style="background:{bg};border-bottom:1px solid rgba(255,255,255,0.06);">'
            html += f'<td style="padding:6px 10px;color:{"#FCD34D" if i==now_h else "white"};font-weight:{"700" if i==now_h else "400"};">{"▶ " if i==now_h else ""}{hour_labels[i]}</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:white;">{round(t)}{unit}</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:rgba(255,200,100,0.9);">{round(f)}{unit}</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:{"#f87171" if r>60 else "#60a5fa" if r>30 else "rgba(255,255,255,0.6)"};">{r}%</td>'
            html += f'<td style="padding:6px 10px;text-align:center;color:rgba(200,240,200,0.9);">{round(w)} mph</td>'
            html += f'<td style="padding:6px 10px;text-align:center;">{wear}</td></tr>'
        html += '</table></div>'
        st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 5 — RAIN COUNTDOWN
# ═══════════════════════════════════════════════════════════════
def render_rain_countdown(hourly_rain_vals, hour_labels, now_h):
    st.markdown("---")
    # Find next hour where rain > 50%
    rain_hour = None
    for i in range(now_h, 24):
        if hourly_rain_vals[i] > 50:
            rain_hour = i
            break
    # Find when rain stops if currently raining
    stop_hour = None
    if hourly_rain_vals[now_h] > 50:
        for i in range(now_h+1, 24):
            if hourly_rain_vals[i] <= 30:
                stop_hour = i
                break

    if hourly_rain_vals[now_h] > 50:
        msg = f"🌧️ **It's raining now!**"
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


# ═══════════════════════════════════════════════════════════════
# FEATURE 6 — HISTORICAL WEATHER (same day last year)
# ═══════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════
# FEATURE 7 — WEATHER PHOTO OF THE DAY (Unsplash)
# ═══════════════════════════════════════════════════════════════
def render_weather_photo(condition, city_name):
    st.markdown("---")
    cond = condition.lower()
    if "thunder" in cond:   keyword = "thunderstorm lightning"
    elif "snow" in cond:    keyword = "snowfall winter"
    elif "rain" in cond or "drizzle" in cond: keyword = "rain city"
    elif "fog" in cond:     keyword = "foggy morning"
    elif "cloud" in cond:   keyword = "cloudy sky"
    elif "clear" in cond or "sunny" in cond: keyword = "sunny day blue sky"
    else:                   keyword = "weather sky"
    # Use Unsplash source (free, no API key)
    photo_url = f"https://source.unsplash.com/800x400/?{keyword.replace(' ',',')}"
    st.markdown(f"""<div class="glass-card">
      <div class="box-title">📸 Weather Photo — {condition}</div>
      <img src="{photo_url}" style="width:100%;border-radius:10px;margin-top:6px;object-fit:cover;height:200px;" alt="Weather photo"/>
      <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:6px;">Photo via Unsplash · {keyword}</div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 8 — AIR QUALITY HEALTH ADVICE
# ═══════════════════════════════════════════════════════════════
def render_aqi_health(aqi_text, pm25):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🫁 Air Quality Health Guide</p>', unsafe_allow_html=True)

    try: aqi_num = int(aqi_text.split()[0])
    except: aqi_num = 50

    if aqi_num <= 50:
        groups = [("🏃 Runners","✅ Perfect for outdoor runs. No restrictions."),
                  ("🧒 Children","✅ Safe for outdoor play all day."),
                  ("🫁 Asthma","✅ Air is clean. Inhaler still recommended as precaution."),
                  ("👴 Elderly","✅ Safe for all outdoor activities.")]
    elif aqi_num <= 100:
        groups = [("🏃 Runners","⚠️ Sensitive runners may want to reduce intensity."),
                  ("🧒 Children","✅ Generally safe. Watch for eye irritation."),
                  ("🫁 Asthma","⚠️ Keep rescue inhaler handy. Avoid heavy exertion."),
                  ("👴 Elderly","⚠️ Limit prolonged outdoor exposure.")]
    elif aqi_num <= 150:
        groups = [("🏃 Runners","❌ Move workout indoors. Outdoor running not advised."),
                  ("🧒 Children","⚠️ Limit outdoor play to short periods."),
                  ("🫁 Asthma","❌ Stay indoors. Use air purifier if available."),
                  ("👴 Elderly","❌ Avoid outdoor activity. Keep windows closed.")]
    else:
        groups = [("🏃 Runners","🚫 Do not exercise outdoors under any circumstances."),
                  ("🧒 Children","🚫 Keep children indoors. School outdoor activities should be cancelled."),
                  ("🫁 Asthma","🚫 Emergency risk. Stay indoors, use purifier, contact doctor if symptoms worsen."),
                  ("👴 Elderly","🚫 Stay indoors. Serious health risk.")]

    cols = st.columns(2)
    for i, (group, advice) in enumerate(groups):
        with cols[i % 2]:
            st.markdown(f'<div class="glass-card"><div class="box-title">{group}</div><div style="font-size:13px;color:white;">{advice}</div></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 9 — TRIP WEATHER PLANNER
# ═══════════════════════════════════════════════════════════════
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
                    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={dest.strip()}&count=1").json()
                    if "results" not in geo or not geo["results"]:
                        st.error("Destination not found.")
                    else:
                        r = geo["results"][0]; lat2 = r["latitude"]; lon2 = r["longitude"]
                        days = (end - start).days + 1
                        if days > 16: st.warning("⚠️ Forecast only available up to 16 days. Showing first 16 days.")
                        days = min(days, 16)
                        wx = requests.get(
                            f"https://api.open-meteo.com/v1/forecast?latitude={lat2}&longitude={lon2}"
                            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max"
                            f"&temperature_unit=fahrenheit&timezone=auto&forecast_days={days}"
                            f"&start_date={start}"
                        ).json()
                        if "daily" not in wx:
                            st.error("Could not fetch forecast.")
                        else:
                            st.markdown(f'<div class="ai-box" style="margin-bottom:10px;"><div class="box-title">✈️ {r["name"]} Trip Forecast</div>Your {days}-day trip weather summary</div>', unsafe_allow_html=True)
                            fc = '<div class="forecast-row" style="flex-wrap:wrap;">'
                            for i in range(min(days, len(wx["daily"]["time"]))):
                                date_str = wx["daily"]["time"][i]
                                day_label = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d")
                                di = WMO_CODES.get(wx["daily"]["weather_code"][i],"🌡️").split()[0]
                                dh = round(wx["daily"]["temperature_2m_max"][i])
                                dl = round(wx["daily"]["temperature_2m_min"][i])
                                dr = wx["daily"].get("precipitation_probability_max",[0]*days)[i]
                                fc += (f'<div class="forecast-day" style="min-width:70px;">'
                                       f'<div class="day-name">{day_label}</div>'
                                       f'<div class="day-icon">{di}</div>'
                                       f'<div class="day-hi">{dh}°F</div>'
                                       f'<div class="day-lo">{dl}°F</div>'
                                       f'<div style="font-size:10px;color:rgba(255,255,255,0.5);">🌧️{dr}%</div></div>')
                            st.markdown(fc + "</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 10 — WEATHER-BASED MUSIC MOOD
# ═══════════════════════════════════════════════════════════════
def render_music_mood(condition, temp_f, fgi):
    st.markdown("---")
    cond = condition.lower()
    if "thunder" in cond:
        mood, playlist, emoji = "Dramatic & Intense", "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U", "⛈️"
        desc = "Thunderstorms call for epic, cinematic soundtracks."
    elif "snow" in cond:
        mood, playlist, emoji = "Cozy & Warm", "https://open.spotify.com/playlist/37i9dQZF1DX6aTaZa0K6VA", "❄️"
        desc = "Snow day vibes — curl up with hot cocoa and chill music."
    elif "rain" in cond or "drizzle" in cond:
        mood, playlist, emoji = "Rainy Day Chill", "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO", "🌧️"
        desc = "Perfect rainy day playlist — lofi, jazz, and mellow tunes."
    elif temp_f > 85:
        mood, playlist, emoji = "Summer Vibes", "https://open.spotify.com/playlist/37i9dQZF1DX4dyzvuaRJ0n", "🔥"
        desc = "Hot weather calls for beach beats and summer anthems."
    elif temp_f < 40:
        mood, playlist, emoji = "Winter Warmth", "https://open.spotify.com/playlist/37i9dQZF1DX6aTaZa0K6VA", "🥶"
        desc = "Cold outside — time for acoustic comfort music."
    elif fgi >= 70:
        mood, playlist, emoji = "Happy & Energetic", "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0", "😄"
        desc = "Perfect weather deserves perfect upbeat music!"
    else:
        mood, playlist, emoji = "Easy Listening", "https://open.spotify.com/playlist/37i9dQZF1DWYmmr74INQlb", "🎵"
        desc = "Balanced weather, balanced tunes."

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


# ═══════════════════════════════════════════════════════════════
# FEATURE 11 — MULTI-CITY DASHBOARD
# ═══════════════════════════════════════════════════════════════
def render_multi_city_dashboard(unit):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">🌍 Multi-City Dashboard</p>', unsafe_allow_html=True)
    default_cities = ["New York", "London", "Tokyo", "Sydney", "Paris", "Dubai"]
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
                            wx_f, wx_d, _, meta = res
                            cur = wx_f["current"]; cur_d = wx_d["current"]
                            fgi_v, fgi_l, fgi_c = feel_good_index(cur["temperature_2m"], cur["relative_humidity_2m"], cur["wind_speed_10m"])
                            st.session_state.multi_city_data.append({
                                "name": meta["name"], "country": meta["country"],
                                "temp": round(cur_d["temperature_2m"]), "unit": unit,
                                "cond": WMO_CODES.get(cur["weather_code"],"🌡️"),
                                "fgi": fgi_v, "fgi_col": fgi_c,
                                "rain": cur.get("precipitation_probability", 0),
                                "wind": round(cur["wind_speed_10m"])
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


# ═══════════════════════════════════════════════════════════════
# FEATURE 12 — PERSONAL WEATHER DIARY
# ═══════════════════════════════════════════════════════════════
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
            entry = {
                "date": datetime.now().strftime("%b %d, %Y %I:%M %p"),
                "city": city_name, "temp": f"{round(temp_d)}{unit}",
                "cond": condition, "mood": mood, "note": note
            }
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


# ═══════════════════════════════════════════════════════════════
# FEATURE 13 — SEVERE WEATHER MAP (region alerts)
# ═══════════════════════════════════════════════════════════════
def render_severe_weather_map(lat, lon, city_name, code):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">⚠️ Regional Weather Map</p>', unsafe_allow_html=True)
    is_severe = code in SEVERE_CODES
    alert_color = "#DC2626" if is_severe else "#1D9E75"
    alert_msg = f"⚠️ SEVERE WEATHER ACTIVE — {WMO_CODES.get(code,'')}" if is_severe else "✅ No severe weather alerts in this region"
    import streamlit.components.v1 as comp
    comp.html(f"""
    <div style="border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.25);margin-bottom:8px;">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <div id="smap" style="height:300px;width:100%;"></div>
    <script>
      var map=L.map('smap',{{zoomControl:true,scrollWheelZoom:false}}).setView([{lat},{lon}],5);
      L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap',maxZoom:18}}).addTo(map);
      L.tileLayer('https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid=demo',{{opacity:0.4}}).addTo(map);
      var circle=L.circle([{lat},{lon}],{{color:'{alert_color}',fillColor:'{alert_color}',fillOpacity:0.15,radius:80000}}).addTo(map);
      var icon=L.divIcon({{html:'<div style="font-size:28px;">{"⚠️" if is_severe else "📍"}</div>',iconSize:[35,35],className:''}});
      L.marker([{lat},{lon}],{{icon:icon}}).addTo(map).bindPopup('<b>{city_name}</b><br>{WMO_CODES.get(code,"")}').openPopup();
    </script></div>""", height=310)
    st.markdown(f'<div class="{"warn-box" if is_severe else "info-box"}">{alert_msg}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 14 — PWA MANIFEST (installable app)
# ═══════════════════════════════════════════════════════════════
def inject_pwa():
    st.markdown("""
    <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiTmltYnVzQUkiLCJzaG9ydF9uYW1lIjoiTmltYnVzIiwic3RhcnRfdXJsIjoiLyIsImRpc3BsYXkiOiJzdGFuZGFsb25lIiwiYmFja2dyb3VuZF9jb2xvciI6IiMxYTZlZmYiLCJ0aGVtZV9jb2xvciI6IiMxYTZlZmYiLCJpY29ucyI6W3sic3JjIjoiaHR0cHM6Ly9lbW9qaXBlZGlhLm9yZy9pbWFnZXMvZW1vamlwZWRpYS9ub3JtYWwvc3VuLWJlaGluZC1zbWFsbC1jbG91ZF8yNmY0LWZlMGYucG5nIiwic2l6ZXMiOiIxOTJ4MTkyIiwidHlwZSI6ImltYWdlL3BuZyJ9XX0=">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="NimbusAI">
    <meta name="theme-color" content="#1a6eff">
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FEATURE 15 — WEATHER STATS SUMMARY CARD
# ═══════════════════════════════════════════════════════════════
def render_stats_summary(temp_f, humidity, wind_mph, uv, rain_pct, aqi_text, fgi, unit, temp_d, feels_d):
    st.markdown("---")
    st.markdown('<p style="color:white;font-weight:700;font-size:16px;margin-bottom:8px;">📊 Complete Weather Stats</p>', unsafe_allow_html=True)

    def rate(val, low_bad, low_ok, hi_ok, hi_bad):
        if val <= low_bad or val >= hi_bad: return "🔴"
        if val <= low_ok or val >= hi_ok:  return "🟡"
        return "🟢"

    stats = [
        ("🌡️ Temperature",  f"{round(temp_d)}{unit}", rate(temp_f,32,50,85,100)),
        ("🥵 Feels Like",   f"{round(feels_d)}{unit}", rate(temp_f,32,50,85,100)),
        ("💧 Humidity",     f"{humidity}%",             rate(humidity,20,30,60,80)),
        ("💨 Wind Speed",   f"{round(wind_mph)} mph",   rate(wind_mph,0,0,15,30)),
        ("🌧️ Rain Chance",  f"{rain_pct}%",             rate(rain_pct,0,0,30,70)),
        ("🌞 UV Index",     f"{round(uv)}/11",          rate(uv,0,0,5,8)),
        ("😊 Feel-Good",    f"{fgi}/100",               rate(100-fgi,0,0,30,60)),
        ("💨 Air Quality",  aqi_text.split()[0] if aqi_text != "N/A" else "N/A", "🟢" if "Good" in aqi_text else "🟡" if "Moderate" in aqi_text else "🔴"),
    ]
    html = '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px;">'
    for label, val, dot in stats:
        html += f'<div class="glass-card" style="padding:10px 12px;"><div style="display:flex;justify-content:space-between;align-items:center;"><span style="font-size:12px;color:rgba(255,255,255,0.7);">{label}</span><span>{dot}</span></div><div style="font-size:18px;font-weight:700;color:white;margin-top:4px;">{val}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
for k,v in [("history",[]),("city_input",""),("dark_mode",False),
             ("last_updated",None),("outfit_memory",{})]:
    if k not in st.session_state: st.session_state[k]=v

import streamlit.components.v1 as components

# ── Header ─────────────────────────────────────────────────────────────────────
c1,c2=st.columns([5,1])
with c1: st.markdown('<p style="font-size:28px;font-weight:900;color:white;margin:0 0 4px;letter-spacing:-1px;">🌤️ NimbusAI</p>',unsafe_allow_html=True)
with c2: st.session_state.dark_mode=st.toggle("🌙",value=st.session_state.dark_mode,help="Dark mode")
if st.session_state.dark_mode:
    st.markdown("<style>.stApp{filter:brightness(0.6) saturate(0.7) !important;}</style>",unsafe_allow_html=True)

unit=st.radio("",["°F","°C"],horizontal=True,label_visibility="collapsed")

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
</script>""",height=60)

if st.session_state.history:
    st.markdown(f'<div class="chip-row">'+''.join(f'<span class="chip">🕐 {c}</span>' for c in st.session_state.history)+'</div>',unsafe_allow_html=True)

city_typed=st.text_input("",placeholder="Search a city...",label_visibility="collapsed",value=st.session_state.city_input)
fetch_city=city_typed.strip()

# ── Main display ───────────────────────────────────────────────────────────────
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
        condition_str=WMO_CODES.get(code,"Unknown"); wind_dir_str=wind_dir_label(wind_deg)
        temp_d=cur_d["temperature_2m"]; feels_d=cur_d["apparent_temperature"]

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

        try:
            sr_raw=daily_f.get("sunrise",["",""])[1]; ss_raw=daily_f.get("sunset",["",""])[1]
            sr_fmt=datetime.strptime(sr_raw,"%Y-%m-%dT%H:%M").strftime("%I:%M %p")
            ss_fmt=datetime.strptime(ss_raw,"%Y-%m-%dT%H:%M").strftime("%I:%M %p")
        except: sr_fmt,ss_fmt="N/A","N/A"

        tz_str=wx_f.get("timezone","UTC"); local_now=datetime.now(ZoneInfo(tz_str)); now_h=local_now.hour
        h_slice=slice(24,48)
        hourly_temps_f=wx_f["hourly"]["temperature_2m"][h_slice]
        hourly_temps_d=wx_display["hourly"]["temperature_2m"][h_slice]
        hourly_feels_d=wx_display["hourly"].get("apparent_temperature",wx_display["hourly"]["temperature_2m"])[h_slice]
        hourly_rain_vals=wx_f["hourly"]["precipitation_probability"][h_slice]
        hourly_wind=wx_f["hourly"]["wind_speed_10m"][h_slice]
        hourly_times=wx_f["hourly"]["time"][h_slice]
        hour_labels=[datetime.strptime(t,"%Y-%m-%dT%H:%M").strftime("%-I%p").lower() for t in hourly_times]
        week_hi_f=daily_f["temperature_2m_max"][1:7]; week_hi_d=daily_d["temperature_2m_max"][1:7]

        best_i,best_window_str=best_outdoor_window(hourly_temps_f,hourly_rain_vals,hourly_wind,hour_labels)
        yesterday_change=what_changed_yesterday(hi_f_val,lo_f_val,t_rain_arr[1] if len(t_rain_arr)>1 else rain_pct,yest_hi_f,yest_lo_f,yest_rain,unit)
        fgi,fgi_lbl,fgi_col=feel_good_index(temp_f,humidity,wind_mph)
        moon_icon,moon_name=get_moon_phase(datetime.now())
        aqi_text,aqi_color=aqi_label(aqi)

        sky_bg=sky_class(code)
        st.session_state.last_updated=local_now.strftime("%I:%M %p")
        if city_name not in st.session_state.history: st.session_state.history.insert(0,city_name)
        st.session_state.history=st.session_state.history[:6]
        st.markdown(make_particles(sky_bg),unsafe_allow_html=True)

        alt_t=f"/ {to_c(temp_f)}°C" if unit=="°F" else f"/ {to_f(temp_d)}°F"
        alt_f2=f"/ {to_c(feels_f)}°C" if unit=="°F" else f"/ {to_f(feels_d)}°F"

        st.markdown(f"""<div class="hero-card">
          <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px;">
            <span style="font-size:32px;font-weight:800;color:white;letter-spacing:-1px;">{local_now.strftime("%I:%M %p")}</span>
            <span style="font-size:13px;color:rgba(255,255,255,0.6);">{local_now.strftime("%a, %b %d")}</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.4);margin-left:auto;">Updated {st.session_state.last_updated}</span>
          </div>
          <div class="hero-city">📍 {city_name}, {country}</div>
          <div class="hero-cond">{condition_str}</div>
          <div style="display:flex;align-items:flex-end;gap:16px;margin-top:8px;flex-wrap:wrap;">
            <div><div class="hero-temp">{round(temp_d)}{unit}</div><div class="dual-temp">{alt_t}</div></div>
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

        st.markdown(f'<div class="info-box"><div class="box-title">📅 What Changed Since Yesterday</div>{yesterday_change}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="ai-box"><div class="box-title">🌟 Best Time to Go Outside</div>{best_window_str}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="ai-box"><div class="box-title">✨ Weather Summary</div>{ai_comment(temp_f,condition_str,wind_mph)}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card"><div class="box-title">🌡️ Why Does It Feel Like That?</div><div style="font-size:14px;color:white;">{feels_like_reason(temp_f,humidity,wind_mph)}</div></div>',unsafe_allow_html=True)

        t_icon=WMO_CODES.get(t_code,"🌡️").split()[0]; t_cond_str=WMO_CODES.get(t_code,"Unknown")
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

        wear_items=what_to_wear(temp_f,condition_str,wind_mph); svg_fig=outfit_svg(temp_f,condition_str)
        wc1,wc2=st.columns([1,2])
        with wc1: st.markdown(f'<div class="glass-card" style="text-align:center;padding:12px;"><div class="box-title">👤 Outfit Preview</div>{svg_fig}</div>',unsafe_allow_html=True)
        with wc2: st.markdown(f'<div class="wear-box"><div class="box-title">👗 What to Wear</div>{"<br>".join(wear_items)}</div>',unsafe_allow_html=True)

        outfit_key=f"{round(temp_f//10)*10}"; saved=st.session_state.outfit_memory.get(outfit_key)
        with st.expander("💾 Save Your Own Outfit for This Temperature Range"):
            outfit_input=st.text_input("What are you wearing today?",value=saved or "",placeholder="e.g. jeans, hoodie, sneakers",key="outfit_inp")
            if st.button("Save Outfit"):
                st.session_state.outfit_memory[outfit_key]=outfit_input
                st.success(f"✅ Saved for {round(temp_f//10)*10}–{round(temp_f//10)*10+9}°F!")
        if saved:
            st.markdown(f'<div class="glass-card"><div class="box-title">💡 Your Saved Outfit</div><div style="color:white;font-size:14px;">👕 {saved}</div></div>',unsafe_allow_html=True)

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
        </div>""",unsafe_allow_html=True)

        hum_msg,hum_col=humidity_comfort(humidity)
        st.markdown(f'<div class="glass-card"><div class="box-title">💧 Humidity Comfort</div><div style="font-size:14px;color:{hum_col};">{hum_msg}</div><div class="glass-sub">{humidity}% relative humidity</div></div>',unsafe_allow_html=True)

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

        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px;">
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌾 Grass Pollen</div><div class="glass-value" style="font-size:15px;">{pollen_label(grass_pollen,"grass")}</div></div>
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌳 Tree Pollen</div><div class="glass-value" style="font-size:15px;">{pollen_label(tree_pollen,"tree")}</div></div>
        </div>""",unsafe_allow_html=True)

        st.markdown('<p style="color:white;font-weight:700;font-size:14px;margin:10px 0 8px;">📅 5-DAY FORECAST</p>',unsafe_allow_html=True)
        fc='<div class="forecast-row">'
        for i in range(5):
            idx=i+1; dn="Today" if i==0 else datetime.strptime(daily_f["time"][idx],"%Y-%m-%d").strftime("%a")
            di=WMO_CODES.get(daily_f["weather_code"][idx],"🌡️").split()[0]
            dh=round(daily_d["temperature_2m_max"][idx]); dl=round(daily_d["temperature_2m_min"][idx])
            dhf=round(daily_f["temperature_2m_max"][idx]); dlf=round(daily_f["temperature_2m_min"][idx])
            au="°C" if unit=="°F" else "°F"; dha=to_c(dhf) if unit=="°F" else to_f(dh); dla=to_c(dlf) if unit=="°F" else to_f(dl)
            fc+=f'<div class="forecast-day"><div class="day-name">{dn}</div><div class="day-icon">{di}</div><div class="day-hi">{dh}{unit}</div><div class="day-lo">{dl}{unit}</div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px;">{dha}/{dla}{au}</div></div>'
        st.markdown(fc+"</div>",unsafe_allow_html=True)

        trend_up=week_hi_f[-1]>week_hi_f[0]; trend_label=f"📈 Warming trend this week" if trend_up else f"📉 Cooling trend this week"
        spark_color="#f87171" if trend_up else "#60a5fa"
        st.markdown(f'<div class="glass-card"><div class="box-title">📊 Weekly High Temperature Trend</div>{make_sparkline(week_hi_d,spark_color)}<div class="glass-sub" style="margin-top:6px;">{trend_label}</div></div>',unsafe_allow_html=True)

        st.markdown(make_sun_arc(local_now,sr_fmt,ss_fmt),unsafe_allow_html=True)
        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px;">
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌅 Sunrise</div><div class="glass-value">{sr_fmt}</div></div>
          <div class="glass-card" style="flex:1;text-align:center;"><div class="glass-label">🌇 Sunset</div><div class="glass-value">{ss_fmt}</div></div>
        </div>""",unsafe_allow_html=True)

        chart_temp  = make_chart(hourly_temps_d,"white","ag","rgba(255,255,255,0.25)",unit,now_h,hour_labels,highlight_i=best_i)
        chart_feels = make_chart(hourly_feels_d,"rgba(255,200,100,0.9)","flg","rgba(255,180,60,0.3)",unit,now_h,hour_labels)
        chart_rain  = make_chart(hourly_rain_vals,"rgba(150,210,255,0.9)","rg","rgba(100,180,255,0.4)","%",now_h,hour_labels,fixed_min=0,fixed_max=100)
        chart_wind  = make_chart(hourly_wind,"rgba(200,240,200,0.9)","wg","rgba(150,220,150,0.3)"," mph",now_h,hour_labels)
        st.markdown(f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:6px;"><div class="box-title">🌡️ Hourly Temperature <span style="font-size:9px;color:rgba(255,255,255,0.4);">★ shaded = best outdoor window</span></div>{chart_temp}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:6px;"><div class="box-title">🥵 Hourly Feels Like</div>{chart_feels}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:6px;"><div class="box-title">🌧️ Hourly Rain Probability</div>{chart_rain}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card" style="padding:16px 12px 8px;margin-bottom:12px;"><div class="box-title">💨 Hourly Wind Speed</div>{chart_wind}</div>',unsafe_allow_html=True)

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

        st.markdown('<div class="box-title" style="color:rgba(255,255,255,0.6);margin-bottom:6px;">🗺️ WEATHER MAP</div>',unsafe_allow_html=True)
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
        </script></div>""",height=270)

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
                    h2=cur2_f["relative_humidity_2m"]
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

        st.markdown('<p class="footer">Open-Meteo API • Air Quality API • OpenStreetMap • No API keys needed 😄</p>',unsafe_allow_html=True)

        # ── All 15 extra features ──────────────────────────────────────────
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

# ── Favourites + PWA always visible ───────────────────────────────────────────
render_favourites()
inject_pwa()

