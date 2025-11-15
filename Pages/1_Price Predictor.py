import streamlit as st, pickle, pandas as pd, numpy as np

st.set_page_config(page_title="Price Predictor", page_icon="🏷️", layout="wide", initial_sidebar_state="expanded")

with open('df.pkl','rb') as f: df = pickle.load(f)
with open('pipeline.pkl','rb') as f: pipeline = pickle.load(f)

# ======= GLOBAL STYLE =======
st.markdown("""
<style>
/* Import a clean modern font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

/* App background - subtle star/gradient + dimmed image (use your Gurgaon image URLs) */
.appview-container, .main {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  background:
    radial-gradient(900px 500px at 10% 10%, rgba(6,182,212,0.04) 0%, transparent 40%),
    radial-gradient(800px 450px at 90% 20%, rgba(34,197,94,0.03) 0%, transparent 45%),
    linear-gradient(180deg,#06070a 0%, #07090d 100%),
    url('https://images.unsplash.com/photo-1606144042614-b2417e99c4f6?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  color: #e7fef5;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
}

/* Overlay to gently dim background images for legibility */
.appview-container::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(3,7,10,0.55), rgba(3,7,10,0.65));
  pointer-events: none;
  z-index: 0;
}

/* Make main area and blocks sit above the overlay */
.main, .block, .callout, .banner, .sb-hero {
  position: relative;
  z-index: 1;
}

/* Sidebar - translucent glass */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(11,15,20,0.55), rgba(13,18,25,0.58));
  backdrop-filter: blur(8px) saturate(110%);
  border-right: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 8px 30px rgba(2,6,12,0.6);
}

/* Sidebar inner wrapper */
.sb-wrap{ padding:14px 12px 22px; }

/* Hero inside sidebar - glossy card */
.sb-hero{
  border-radius:16px;
  overflow:hidden;
  margin:8px 6px 14px;
  border: 1px solid rgba(255,255,255,0.06);
  background:
    linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  backdrop-filter: blur(6px);
  box-shadow: 0 6px 20px rgba(2,6,12,0.55);
}

/* Titles - modern gradient text */
.sb-title {
  font-weight:700;
  font-size:18px;
  margin:0;
  background: linear-gradient(90deg,#a7f3d0,#60a5fa,#c4b5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing:0.2px;
}

/* Chips - minimal */
.sb-chip{
  display:inline-block;
  border-radius:999px;
  padding:6px 10px;
  margin-right:8px;
  font-size:12px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.04);
  box-shadow: 0 2px 6px rgba(2,6,12,0.45);
  color: #e6fbf7;
}

/* Banner - premium glass card with background image */
.banner{
  border-radius:18px;
  overflow:hidden;
  margin-bottom:18px;
  border:1px solid rgba(255,255,255,0.06);
  background:
    linear-gradient(180deg, #0b0f14e0, #0b0f14f0),
    url('https://images.unsplash.com/photo-1568605114967-8130f3a36994?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  box-shadow: 0 10px 35px rgba(2,6,12,0.6);
}

/* Banner inner spacing */
.banner-in{ padding:36px 28px; }

/* Headline and hint */
.banner-in h2{ margin:0; font-weight:700; font-size:22px; color:#fff; letter-spacing:0.2px }
.hint{ opacity:0.78; margin-top:6px; font-size:13px; }

/* Blocks & cards - glass, softer corners */
.block{
  border: 1px solid rgba(255,255,255,0.04);
  border-radius:14px;
  padding:16px;
  background: linear-gradient(180deg, rgba(10,12,15,0.55), rgba(8,10,12,0.45));
  backdrop-filter: blur(6px);
  box-shadow: 0 8px 28px rgba(2,6,12,0.5);
}

/* Callout card - subtle gradient border */
.callout{
  border-radius:14px;
  padding:16px;
  border: 1px solid transparent;
  background-clip: padding-box, border-box;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)) padding-box,
    linear-gradient(90deg, rgba(167,243,208,0.06), rgba(96,165,250,0.06)) border-box;
  box-shadow: 0 6px 24px rgba(2,6,12,0.45);
}

/* Metric styles - premium typography */
.metric{
  border-radius:12px;
  padding:14px 16px;
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
  border: 1px solid rgba(255,255,255,0.03);
  box-shadow: 0 8px 20px rgba(2,6,12,0.45);
}

/* Big number - gradient text, heavier weight */
.big{
  font-size:30px;
  font-weight:800;
  margin-top:6px;
  display:block;
  line-height:1;
  background: linear-gradient(90deg,#7ef5c4,#60a5fa,#c4b5fd);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}

/* Subtext */
.sub{ opacity:0.78; font-size:13px }

/* Form inputs - slightly rounded and elevated */
.stTextInput>div>div>input, .stSelectbox>div>div>div, .stSlider>div>div {
  border-radius:10px !important;
  padding:10px 12px !important;
  background: rgba(255,255,255,0.02) !important;
  border: 1px solid rgba(255,255,255,0.04) !important;
  box-shadow: inset 0 -1px 0 rgba(255,255,255,0.01);
  color: #e7fef5 !important;
}

/* Buttons - glossy primary */
.stButton>button {
  border-radius:12px;
  padding:10px 14px;
  font-weight:700;
  letter-spacing:0.2px;
  background: linear-gradient(90deg, #22c55e, #06b6d4);
  border: none;
  color: #041018;
  box-shadow: 0 8px 26px rgba(6,182,212,0.09), 0 4px 10px rgba(34,197,94,0.06);
  transition: transform .12s ease, box-shadow .12s ease, opacity .12s ease;
}
.stButton>button:hover{ transform: translateY(-2px); box-shadow: 0 12px 36px rgba(6,182,212,0.12); opacity:0.98; }

/* Expander content readability */
.stExpander > div[role="button"] + div {
  background: rgba(255,255,255,0.01);
  border-radius:10px;
  padding:10px;
  border:1px solid rgba(255,255,255,0.03);
}

/* Small screens / responsive */
@media (max-width: 900px) {
  .banner-in{ padding:22px 16px }
  .big{ font-size:24px }
  .sb-title{ font-size:16px }
}

/* Accessibility: increased contrast for focus */
:focus { outline: 2px solid rgba(96,165,250,0.22); outline-offset: 2px; box-shadow: 0 0 0 4px rgba(96,165,250,0.06); }

/* Minor polish */
hr{ border-color: rgba(255,255,255,0.06) }
</style>
""", unsafe_allow_html=True)


# ======= SIDEBAR =======
with st.sidebar:
    st.markdown('<div class="sb-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-hero"><div class="sb-hero-in">
      <p class="sb-title">Gurgaon Studio</p>
      <div class="sb-caption">Navigate the suite:</div>
      <div style="margin-top:8px">
        <span class="sb-chip">🏷️ Predictor</span>
        <span class="sb-chip">📊 Analytics</span>
        <span class="sb-chip">🏢 Recos</span>
      </div>
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sb-caption">Tip: switch pages from the sidebar menu.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======= HEADER =======
st.markdown("""<div class="banner"><div class="banner-in">
  <h2 style="margin:0">Price Predictor</h2>
  <p class="hint">Fill the details • Get an elegant estimate (₹ crore)</p>
</div></div>""", unsafe_allow_html=True)

# ----------- NEW: dynamic area bounds for better range UX -----------
areas = pd.to_numeric(df["built_up_area"], errors="coerce").dropna()
area_min = float(areas.quantile(0.05))
area_max = float(areas.quantile(0.95))

# ======= FORM =======
with st.form("price_form"):
    l, m, r = st.columns(3)

    # -------- LEFT column --------
    with l:
        property_type = st.selectbox('Property Type', ['flat','house'])
        sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

        # 🔥 REPLACED: single input → RANGE input
        built_min, built_max = st.slider(
            "Built Up Area (sqft) — range",
            min_value=area_min,
            max_value=area_max,
            value=(float(areas.quantile(0.25)), float(areas.quantile(0.75))),
            step=10.0
        )

    # -------- MIDDLE column --------
    with m:
        bedrooms = float(st.selectbox('Bedrooms', sorted(df['bedRoom'].unique().tolist())))
        bathroom = float(st.selectbox('Bathrooms', sorted(df['bathroom'].unique().tolist())))
        balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

    # -------- RIGHT column --------
    with r:
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
        servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
        store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

    # BLOCK bottom section
    st.markdown('<div class="block">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
    with c2:
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
    with c3:
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    go = st.form_submit_button("Predict")

# ======= PREDICTION =======
if go:

    # build rows for min/mid/max areas
    mid_area = round((built_min + built_max)/2, 1)

    def predict_for(area):
        X = pd.DataFrame([[
            property_type, sector, bedrooms, bathroom, balcony, property_age,
            area, servant_room, store_room, furnishing_type,
            luxury_category, floor_category
        ]], columns=['property_type','sector','bedRoom','bathroom','balcony',
                     'agePossession','built_up_area','servant room','store room',
                     'furnishing_type','luxury_category','floor_category'])
        return float(np.expm1(pipeline.predict(X))[0])

    p1 = predict_for(built_min)
    p2 = predict_for(mid_area)
    p3 = predict_for(built_max)

    # Bands
    def band(p): return p-0.22, p+0.22
    l1, h1 = band(p1)
    l2, h2 = band(p2)
    l3, h3 = band(p3)

    # ===== RESULT CARDS (unchanged styling) =====
    st.markdown('<div class="callout">', unsafe_allow_html=True)
    a,b,c = st.columns(3)

    a.markdown(
        f'<div class="metric">'
        f'<div class="sub">At {built_min:.0f} sqft</div>'
        f'<div class="big">₹ {p1:.2f} Cr</div>'
        f'<div class="sub">Range: ₹ {l1:.2f} - {h1:.2f}</div></div>',
        unsafe_allow_html=True
    )

    b.markdown(
        f'<div class="metric">'
        f'<div class="sub">At {mid_area:.0f} sqft</div>'
        f'<div class="big">₹ {p2:.2f} Cr</div>'
        f'<div class="sub">Range: ₹ {l2:.2f} - {h2:.2f}</div></div>',
        unsafe_allow_html=True
    )

    c.markdown(
        f'<div class="metric">'
        f'<div class="sub">At {built_max:.0f} sqft</div>'
        f'<div class="big">₹ {p3:.2f} Cr</div>'
        f'<div class="sub">Range: ₹ {l3:.2f} - {h3:.2f}</div></div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("What influences this estimate?"):
        st.write(
            "- Historical Gurgaon market patterns\n"
            "- Relationship learned between area, BHK, sector, and amenities\n"
            "- Price naturally grows with area — we show predictions at 3 points in your selected range"
        )
