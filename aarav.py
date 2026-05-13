from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
import re

src = "/mnt/data/NimbusAI-main.zip"
work = Path("/mnt/data/nimbus_fix")
work.mkdir(exist_ok=True)

with ZipFile(src, "r") as z:
    z.extractall(work)

app = work / "NimbusAI-main" / "aarav.py"
code = app.read_text(encoding="utf-8", errors="ignore")

# safer import injection
if "streamlit_autorefresh" not in code:
    code = code.replace(
        "from concurrent.futures import ThreadPoolExecutor, as_completed",
        "from concurrent.futures import ThreadPoolExecutor, as_completed\n"
        "from streamlit_autorefresh import st_autorefresh\n"
        "import streamlit.components.v1 as components"
    )

# visible upgrades
if "weather_refresh" not in code:
    code = code.replace(
        'st.set_page_config(page_title="NimbusAI", page_icon="🌤️", layout="centered")',
        'st.set_page_config(page_title="NimbusAI", page_icon="🌤️", layout="centered")\n'
        'st_autorefresh(interval=1800000, key="weather_refresh")'
    )

# better CSS
code = code.replace(
    "hero-temp   { font-size:84px; font-weight:900; line-height:1; letter-spacing:-4px; text-shadow:0 4px 20px rgba(0,0,0,0.2); color:white; }",
    """hero-temp   {
        font-size:84px;
        font-weight:900;
        line-height:1;
        letter-spacing:-4px;
        background:linear-gradient(90deg,#60a5fa,#22c55e,#f97316);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        text-shadow:0 4px 20px rgba(0,0,0,0.2);
        animation: tempGlow 6s ease infinite;
    }"""
)

if "@keyframes tempGlow" not in code:
    code = code.replace(
        ".main .block-container { position:relative; z-index:10; }",
        """.main .block-container {
            position:relative;
            z-index:10;
            animation:fadeWeather 0.8s ease;
        }

        @keyframes fadeWeather {
            from {opacity:0; transform:translateY(12px);}
            to {opacity:1; transform:translateY(0px);}
        }

        @keyframes tempGlow {
            0% { filter:brightness(1); }
            50% { filter:brightness(1.25); }
            100% { filter:brightness(1); }
        }"""
    )

# stronger glassmorphism
code = code.replace(
    "backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px);",
    "backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px); box-shadow:0 10px 35px rgba(0,0,0,0.25);"
)

# keyboard shortcuts
if "keydown" not in code:
    code += """

components.html(\"\"\"
<script>
document.addEventListener('keydown', function(e){
    if(e.key === 'r'){
        window.location.reload();
    }
});
</script>
\"\"\", height=0)
"""

# Add visible upgraded header
if "NimbusAI ULTRA" not in code:
    code = code.replace(
        'st.markdown("""',
        '''st.markdown("""
<div style="
padding:12px 18px;
margin-bottom:12px;
border-radius:18px;
background:rgba(255,255,255,0.12);
backdrop-filter:blur(14px);
border:1px solid rgba(255,255,255,0.2);
color:white;
font-weight:700;
text-align:center;
font-size:18px;
">
⚡ NimbusAI ULTRA • Enhanced Visual Edition
</div>
'''
    )

app.write_text(code, encoding="utf-8")

# requirements
req = work / "NimbusAI-main" / "requirements.txt"
txt = req.read_text(errors="ignore")
for pkg in ["streamlit-autorefresh"]:
    if pkg not in txt:
        txt += f"\n{pkg}"
req.write_text(txt)

out = "/mnt/data/NimbusAI-visible-upgrade.zip"
with ZipFile(out, "w", ZIP_DEFLATED) as z:
    for f in work.rglob("*"):
        z.write(f, f.relative_to(work))

print(out)
