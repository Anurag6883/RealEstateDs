import streamlit as st

st.set_page_config(
    page_title="Gurgaon Real Estate • Studio",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======= STYLE =======
st.markdown("""
<style>
/* Background — soft animated gradient overlayed on a hero image */
.appview-container, .main {
  background: radial-gradient(1200px 700px at 10% 10%, #0ea5e915 0%, transparent 55%),
              radial-gradient(1000px 600px at 90% 20%, #22c55e15 0%, transparent 60%),
              radial-gradient(1000px 600px at 20% 90%, #8b5cf615 0%, transparent 60%),
              #0b0f14;
}
.hero {
  position: relative;
  padding: 64px 48px;
  border-radius: 28px;
  overflow: hidden;
  margin-bottom: 22px;
  background: linear-gradient(180deg, #0b0f14aa, #0b0f14dd),
              url('https://images.unsplash.com/photo-1505761671935-60b3a7427bad?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  border: 1px solid #ffffff18;
  box-shadow: 0 30px 80px rgba(0,0,0,.35);
}
.hero h1 {font-size: 44px; margin: 0 0 6px; background: linear-gradient(90deg,#22c55e,#06b6d4,#a78bfa);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.hero p {opacity:.8; max-width: 900px}

.card {
  border-radius: 20px; padding: 18px 18px 14px;
  border: 1px solid #ffffff20; background: linear-gradient(180deg,#0f141b,#0c1117);
  transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.card:hover { transform: translateY(-4px); border-color:#22c55e55; box-shadow: 0 16px 50px rgba(34,197,94,.08);}
.kicker {letter-spacing:.2em; text-transform:uppercase; font-size:12px; opacity:.65}
a:link, a:visited {text-decoration:none}
.stButton>button {
  border-radius: 999px; padding: 10px 18px; font-weight:600; border:0;
  background: linear-gradient(90deg,#22c55e,#06b6d4,#a78bfa);
  box-shadow: 0 10px 30px rgba(34,197,94,.18);
}
.stButton>button:hover { filter:brightness(1.05); transform: translateY(-1px);}
.sidebar .sidebar-content {background:transparent}
</style>
""", unsafe_allow_html=True)

# ======= SIDEBAR =======
with st.sidebar:
    st.markdown("Pages")
    st.info("Use the pages in the sidebar to explore.")
    st.markdown("---")
    st.caption("Crafted for curious home-hunters and data lovers.")

# ======= HERO =======
st.markdown("""
<div class="hero">
  <div class="kicker">GURGAON • REAL ESTATE STUDIO</div>
  <h1>Price. Places. Possibilities.</h1>
  <p>Predict prices with confidence, roam interactive sector maps, and discover apartments that feel like destiny — all in a crisp, art-directed interface.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1,1,1])
with c1:
    st.markdown("""<div class="card">
      <div class="kicker">Prediction</div>
      <h3>Price Predictor</h3>
      <p>Granular inputs, clean outputs. A calm estimator with a realistic band.</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="card">
      <div class="kicker">Exploration</div>
      <h3>Market Analytics</h3>
      <p>Geomaps, BHK breakdowns, and distributions that breathe.</p>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="card">
      <div class="kicker">Discovery</div>
      <h3>Recommendations</h3>
      <p>Near-me radius search and cosine-based kindred apartments.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("— pick a page on the left to begin.")
