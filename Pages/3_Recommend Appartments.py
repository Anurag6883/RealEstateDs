import streamlit as st, pickle, pandas as pd, numpy as np

st.set_page_config(page_title="Recommendations", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

# ======= GLOSSY / MINIMAL / PREMIUM CSS (matching other pages) =======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

.appview-container, .main {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  background:
    radial-gradient(900px 500px at 10% 10%, rgba(6,182,212,0.04) 0%, transparent 40%),
    radial-gradient(800px 450px at 90% 20%, rgba(34,197,94,0.03) 0%, transparent 45%),
    linear-gradient(180deg,#06070a 0%, #07090d 100%),
    url('https://images.unsplash.com/photo-1549074862-6171f5d4d1d4?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  color:#e7fef5;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
}

/* subtle overlay for legibility */
.appview-container::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(3,7,10,0.56), rgba(3,7,10,0.66));
  pointer-events: none;
  z-index: 0;
}
.main, .panel, .banner, .sb-hero, .result { position: relative; z-index: 1; }

/* Sidebar glass */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(11,15,20,0.55), rgba(13,18,25,0.58));
  backdrop-filter: blur(8px) saturate(110%);
  border-right: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 8px 30px rgba(2,6,12,0.6);
}

/* sidebar wrapper */
.sb-wrap{ padding:14px 12px 22px; }

/* hero card inside sidebar */
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
.sb-hero-in{ padding:18px; }
.sb-title{ font-weight:700; font-size:18px; margin:0;
  background: linear-gradient(90deg,#a7f3d0,#60a5fa,#c4b5fd);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.sb-chip{ display:inline-block; border-radius:999px; padding:6px 10px; margin-right:8px;
  font-size:12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.04); color:#e6fbf7; }
.sb-caption{ opacity:0.78; font-size:12px; margin-top:6px; }

/* Banner - premium glass */
.banner{
  border-radius:18px; overflow:hidden; margin-bottom:18px; border:1px solid rgba(255,255,255,0.06);
  background:
    linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)),
    url('https://images.unsplash.com/photo-1531874822436-5f484932dbd2?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  backdrop-filter: blur(4px);
  box-shadow: 0 10px 35px rgba(2,6,12,0.6);
}
.banner-in{ padding:36px 28px; }
.banner-in h2{ margin:0; font-weight:700; font-size:22px; color:#fff; letter-spacing:0.2px }
.banner-in p{ opacity:0.78; margin-top:6px; font-size:13px }

/* Panel / result styles */
.panel{ border: 1px solid rgba(255,255,255,0.04); border-radius:14px; padding:16px; 
  background: linear-gradient(180deg, rgba(10,12,15,0.55), rgba(8,10,12,0.45));
  backdrop-filter: blur(6px); box-shadow: 0 8px 28px rgba(2,6,12,0.5); }

.badge{ display:inline-block; border-radius:999px; padding:6px 10px; margin-right:8px; font-size:12px; 
  background: rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.04); color:#e6fbf7; }

/* Results list */
.result{
  border:1px solid rgba(126,245,196,0.12);
  border-radius:12px;
  padding:12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
  box-shadow: 0 8px 22px rgba(2,6,12,0.45);
  margin-bottom:10px;
}

/* small legend under banner */
.reco-legend{
  border-radius:12px; padding:12px; background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
  border:1px solid rgba(255,255,255,0.03); box-shadow: 0 6px 18px rgba(2,6,12,0.45); margin-bottom:16px;
}
.legend-grid{ display:flex; gap:18px; flex-wrap:wrap; }
.legend-item{ min-width:200px; font-size:13px; opacity:0.9; }

/* responsive */
@media (max-width:900px){
  .banner-in{ padding:22px 16px; }
}

/* focus */
:focus { outline: 2px solid rgba(96,165,250,0.18); outline-offset:2px; box-shadow:0 0 0 4px rgba(96,165,250,0.04); }
</style>
""", unsafe_allow_html=True)

# ======= SIDEBAR =======
with st.sidebar:
    st.markdown('<div class="sb-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-hero"><div class="sb-hero-in">
      <p class="sb-title">Gurgaon Studio</p>
      <div class="sb-caption">Discovery tools:</div>
      <div style="margin-top:8px">
        <span class="sb-chip">Nearby</span>
        <span class="sb-chip">Similar</span>
      </div>
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sb-caption">Tip: try 1–3 km for dense areas.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======= BANNER =======
st.markdown("""<div class="banner"><div class="banner-in">
  <h2 style="margin:0">Recommendations</h2>
  <p class="hint">Find nearby properties or get similar apartment suggestions — powered by precomputed matrices.</p>
</div></div>""", unsafe_allow_html=True)

# ======= SMALL LEGEND / CONTEXT =======
st.markdown("""
<div class="reco-legend">
  <div class="legend-grid">
    <div class="legend-item"><strong>Nearby Search</strong><div style="opacity:0.85;font-size:13px">Returns properties within chosen radius (meters in dataset).</div></div>
    <div class="legend-item"><strong>Similar Apartments</strong><div style="opacity:0.85;font-size:13px">Combines multiple similarity matrices to recommend similar listings by score.</div></div>
    <div class="legend-item"><strong>Scores</strong><div style="opacity:0.85;font-size:13px">Higher score = more similar. You can change weightings inside the recommend function.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ======= LOADERS (unchanged logic) =======
@st.cache_data
def load_location_df():
    try:
        return pd.read_pickle('datasets/location_distance.pkl')
    except Exception as e:
        st.error(f"Failed to load location_distance.pkl: {e}")
        return pd.DataFrame()

@st.cache_resource
def load_cosines():
    try:
        return (pickle.load(open('datasets/cosine_sim1.pkl','rb')),
                pickle.load(open('datasets/cosine_sim2.pkl','rb')),
                pickle.load(open('datasets/cosine_sim3.pkl','rb')))
    except Exception as e:
        st.error(f"Failed to load similarity matrices: {e}")
        return None, None, None

location_df = load_location_df()
c1, c2, c3 = load_cosines()

def recommend_properties_with_scores(name, top_n=5):
    # keep original weightings; easy to tweak here
    M = 0.5*c1 + 0.8*c2 + 1*c3
    if name not in location_df.index:
        return pd.DataFrame({'PropertyName':['Property Not Found'],'SimilarityScore':[0.0]})
    sim = list(enumerate(M[location_df.index.get_loc(name)]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)[1:top_n+1]
    idx = [i for i,_ in sim]; scores = [s for _,s in sim]
    return pd.DataFrame({'PropertyName': location_df.index[idx].tolist(),
                         'SimilarityScore': np.round(scores,3)})

if location_df.empty:
    st.info("Location index is empty or failed to load — upload datasets/location_distance.pkl to enable recommendations.")
    st.stop()

# ======= TABS =======
tab1, tab2 = st.tabs(["Nearby Search","Similar Apartments"])

with tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    colA, colB = st.columns([2,1])
    with colA:
        # populate with column names (locations)
        selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()))
    with colB:
        radius = st.number_input('Radius (km)', min_value=0.0, step=0.5, value=2.0)
    if st.button("Search"):
        # distances stored in meters — filter by radius*1000
        result = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()
        st.subheader(f"Within {radius:.1f} km of **{selected_location}**")
        if result.empty:
            st.info("No properties within this radius.")
        else:
            for name, meters in result.items():
                km = round(meters/1000,2)
                st.markdown(
                    f'<div class="result"><span class="badge">{name}</span>'
                    f'<span class="badge">📏 {km} km</span></div>',
                    unsafe_allow_html=True
                )
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if any(x is None for x in [c1,c2,c3]):
        st.info("Similarity matrices failed to load — check datasets/cosine_sim*.pkl")
        st.stop()

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    ca, cb = st.columns([2,1])
    with ca:
        selected_appt = st.selectbox('Apartment', sorted(location_df.index.to_list()))
    with cb:
        topn = st.slider("How many?", 3, 15, 5)
    if st.button("Recommend"):
        df = recommend_properties_with_scores(selected_appt, topn)
        st.subheader(f"Top {len(df)} for **{selected_appt}**")
        for _, row in df.iterrows():
            st.markdown(
                f'<div class="result"><span class="badge">{row.PropertyName}</span>'
                f'<span class="badge">🧮 score {row.SimilarityScore}</span></div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)
