import streamlit as st
import pickle
import pickletools
import io
import numpy as np
import os
import sys

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Genre Predictor",
    page_icon="🎵",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e4dc;
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #1a0a2e 0%, #0a0a0f 55%),
                radial-gradient(ellipse at 80% 100%, #0d1a2e 0%, transparent 60%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 680px; }

/* ── Header ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.4rem, 6vw, 3.6rem);
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: linear-gradient(135deg, #e8e4dc 30%, #9b6dff 70%, #4fc3f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.hero-sub {
    font-size: 0.95rem;
    color: #6b6880;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Slider section label ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #9b6dff;
    margin-bottom: 1.2rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1b2e;
}

/* ── Slider labels ── */
.slider-label {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: -0.6rem;
}
.slider-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #c9c4bc;
    letter-spacing: 0.04em;
}
.slider-desc {
    font-size: 0.72rem;
    color: #4a4760;
}

/* ── Streamlit slider overrides ── */
[data-testid="stSlider"] > div > div > div > div {
    background: #9b6dff !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background-color: #fff !important;
    box-shadow: 0 0 0 3px #9b6dff55 !important;
}

/* ── Predict button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border: none;
    border-radius: 8px;
    padding: 0.85rem 2rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 24px #7c3aed44;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8b47f5, #5a52f0);
    box-shadow: 0 6px 32px #7c3aed66;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, #13102a 0%, #0f1525 100%);
    border: 1px solid #2a2550;
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-top: 2rem;
    box-shadow: 0 8px 40px #00000055;
}
.result-genre {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2rem, 8vw, 3rem);
    background: linear-gradient(135deg, #e8e4dc, #9b6dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}
.result-conf {
    font-size: 0.82rem;
    color: #6b6880;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.6rem;
}

/* ── Probability bars ── */
.prob-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.6rem;
}
.prob-genre-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    color: #c9c4bc;
    width: 90px;
    flex-shrink: 0;
    text-transform: capitalize;
}
.prob-track {
    flex: 1;
    height: 6px;
    background: #1e1b2e;
    border-radius: 99px;
    overflow: hidden;
}
.prob-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s cubic-bezier(.23,1,.32,1);
}
.prob-pct {
    font-size: 0.78rem;
    color: #6b6880;
    width: 38px;
    text-align: right;
    flex-shrink: 0;
}

/* ── Error / warning box ── */
.warn-box {
    background: #1a0e0e;
    border: 1px solid #5c2323;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #e07070;
    font-size: 0.88rem;
    margin-top: 1.5rem;
}

/* ── Divider ── */
.my-divider {
    border: none;
    border-top: 1px solid #1e1b2e;
    margin: 2rem 0 1.8rem;
}
</style>
""", unsafe_allow_html=True)


# ── Robust model loader ────────────────────────────────────────────────────────
class CompatUnpickler(pickle.Unpickler):
    """
    Fixes 'STACK_GLOBAL requires str' — caused when a pickle was saved with
    Python 2 or an old scikit-learn that stored class references as bytes
    instead of str.  We decode bytes keys on the fly.
    """
    def find_class(self, module, name):
        # Both may arrive as bytes when the pickle protocol is old
        if isinstance(module, bytes):
            module = module.decode("utf-8")
        if isinstance(name, bytes):
            name = name.decode("utf-8")
        # Remap removed sklearn locations (0.x → 1.x)
        module = module.replace("sklearn.neighbors.classification",
                                "sklearn.neighbors._classification")
        module = module.replace("sklearn.neighbors.base",
                                "sklearn.neighbors._base")
        module = module.replace("sklearn.utils.deprecation",
                                "sklearn.utils._deprecation")
        return super().find_class(module, name)


@st.cache_resource
def load_model(path="genre_knn.pkl"):
    if not os.path.exists(path):
        return None, (
            f"Model file `{path}` not found. "
            "Place it in the same directory as this script."
        )

    raw = open(path, "rb").read()

    # Strategy 1 — standard pickle
    try:
        model = pickle.loads(raw)
        return model, None
    except Exception as e1:
        pass

    # Strategy 2 — compat unpickler (fixes STACK_GLOBAL bytes issue)
    try:
        model = CompatUnpickler(io.BytesIO(raw)).load()
        return model, None
    except Exception as e2:
        pass

    # Strategy 3 — joblib (common alternative save format)
    try:
        import joblib
        model = joblib.load(path)
        return model, None
    except Exception as e3:
        pass

    # All strategies failed — build a helpful diagnostic
    import sklearn
    diag = (
        f"**Could not load `{path}`** after trying pickle, compat-unpickler, and joblib.\n\n"
        f"**Root cause:** `STACK_GLOBAL requires str` usually means the file was pickled "
        f"with **Python 2** or a very old scikit-learn, but you're running "
        f"Python {sys.version.split()[0]} / scikit-learn {sklearn.__version__}.\n\n"
        f"**Fix options:**\n"
        f"1. Re-save the model in the original environment: "
        f"`joblib.dump(model, 'genre_knn.pkl')`\n"
        f"2. Or use `pickle.dump(model, f, protocol=2)` for maximum compatibility."
    )
    return None, diag

model, load_error = load_model()


# ── Genre emoji map ────────────────────────────────────────────────────────────
GENRE_EMOJI = {
    "pop": "🎤", "rock": "🎸", "jazz": "🎷", "classical": "🎻",
    "hip-hop": "🎧", "hiphop": "🎧", "hip hop": "🎧",
    "electronic": "🎛️", "edm": "🎛️", "dance": "💃",
    "country": "🤠", "r&b": "🎶", "rnb": "🎶",
    "metal": "🤘", "folk": "🪕", "blues": "🎺",
    "reggae": "🌴", "latin": "💃", "indie": "🎵",
}

def genre_emoji(g):
    return GENRE_EMOJI.get(g.lower().strip(), "🎵")

# colour ramp for bars (top genres get warm purple→teal)
BAR_COLORS = [
    "#9b6dff", "#7c5cd6", "#5e4daa", "#4a3e80",
    "#3a3060", "#2e2550", "#221c3c", "#1a1530",
]


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Genre Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">ML-powered music analysis</div>', unsafe_allow_html=True)

st.markdown('<div class="section-label">Audio Features</div>', unsafe_allow_html=True)

# Sliders
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="slider-label"><span class="slider-name">Tempo</span><span class="slider-desc">BPM</span></div>', unsafe_allow_html=True)
    tempo = st.slider("Tempo", 40, 220, 120, label_visibility="collapsed")

    st.markdown('<div class="slider-label"><span class="slider-name">Energy</span><span class="slider-desc">0 → 1</span></div>', unsafe_allow_html=True)
    energy = st.slider("Energy", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")

with col2:
    st.markdown('<div class="slider-label"><span class="slider-name">Danceability</span><span class="slider-desc">0 → 1</span></div>', unsafe_allow_html=True)
    danceability = st.slider("Danceability", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")

    st.markdown('<div class="slider-label"><span class="slider-name">Acousticness</span><span class="slider-desc">0 → 1</span></div>', unsafe_allow_html=True)
    acousticness = st.slider("Acousticness", 0.0, 1.0, 0.5, 0.01, label_visibility="collapsed")

st.markdown('<hr class="my-divider">', unsafe_allow_html=True)

predict_btn = st.button("Predict Genre")

# ── Prediction ─────────────────────────────────────────────────────────────────
if predict_btn:
    if load_error:
        st.markdown('<div class="warn-box">⚠️ <strong>Model load failed</strong></div>',
                    unsafe_allow_html=True)
        st.markdown(load_error)
    else:
        import streamlit.components.v1 as components

        features = np.array([[tempo, energy, danceability, acousticness]])
        prediction = model.predict(features)[0]
        emoji = genre_emoji(str(prediction))

        has_proba = hasattr(model, "predict_proba")
        probabilities = model.predict_proba(features)[0] if has_proba else None
        classes = model.classes_ if has_proba else []

        if has_proba:
            max_prob = float(np.max(probabilities))
            conf_str = f"Confidence · {max_prob:.0%}"
        else:
            conf_str = "Top prediction"

        bars_html = ""
        if has_proba:
            pairs = sorted(zip(classes, probabilities), key=lambda x: -x[1])
            for i, (g, p) in enumerate(pairs):
                color = BAR_COLORS[min(i, len(BAR_COLORS) - 1)]
                bars_html += f"""
                <div class="prob-row">
                  <div class="prob-genre-name">{g}</div>
                  <div class="prob-track">
                    <div class="prob-fill" style="width:{p*100:.1f}%;background:{color};"></div>
                  </div>
                  <div class="prob-pct">{p:.0%}</div>
                </div>"""

        card_height = 160 + (len(classes) if has_proba else 0) * 36
        components.html(f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: linear-gradient(135deg, #13102a 0%, #0f1525 100%);
    border: 1px solid #2a2550;
    border-radius: 16px;
    padding: 2rem 2.2rem;
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
  }}
  .result-genre {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    background: linear-gradient(135deg, #e8e4dc, #9b6dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 0.25rem;
  }}
  .result-conf {{
    font-size: 0.78rem;
    color: #6b6880;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.4rem;
  }}
  .prob-row {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.55rem;
  }}
  .prob-genre-name {{
    font-size: 0.8rem;
    font-weight: 500;
    color: #c9c4bc;
    width: 90px;
    flex-shrink: 0;
    text-transform: capitalize;
  }}
  .prob-track {{
    flex: 1;
    height: 6px;
    background: #1e1b2e;
    border-radius: 99px;
    overflow: hidden;
  }}
  .prob-fill {{
    height: 100%;
    border-radius: 99px;
  }}
  .prob-pct {{
    font-size: 0.76rem;
    color: #6b6880;
    width: 38px;
    text-align: right;
    flex-shrink: 0;
  }}
</style>
</head>
<body>
  <div class="result-genre">{emoji} {prediction}</div>
  <div class="result-conf">{conf_str}</div>
  {bars_html}
</body></html>""", height=card_height, scrolling=False)