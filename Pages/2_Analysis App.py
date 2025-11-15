import streamlit as st, pandas as pd, plotly.express as px, pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt, seaborn as sns

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# ======= GLOSSY / MINIMAL / PREMIUM STYLE (matches Price Predictor) =======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

.appview-container, .main {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  background:
    radial-gradient(900px 500px at 10% 10%, rgba(6,182,212,0.03) 0%, transparent 40%),
    radial-gradient(800px 450px at 90% 20%, rgba(34,197,94,0.03) 0%, transparent 45%),
    linear-gradient(180deg,#06070a 0%, #07090d 100%),
    url('https://images.unsplash.com/photo-1606144042614-b2417e99c4f6?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  color:#e7fef5;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
}

/* subtle overlay for legibility */
.appview-container::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(3,7,10,0.55), rgba(3,7,10,0.65));
  pointer-events: none;
  z-index: 0;
}
.main, .panel, .banner, .sb-hero { position: relative; z-index: 1; }

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
    linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)),
    url('https://images.unsplash.com/photo-1508057198894-247b23fe5ade?q=80&w=800&auto=format&fit=crop') center/cover no-repeat;
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
    url('https://images.unsplash.com/photo-1464013778555-8e723c2f01f8?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  backdrop-filter: blur(4px);
  box-shadow: 0 10px 35px rgba(2,6,12,0.6);
}
.banner-in{ padding:36px 28px; }
.banner-in h2{ margin:0; font-weight:700; font-size:22px; color:#fff; letter-spacing:0.2px }
.banner-in p{ opacity:0.78; margin-top:6px; font-size:13px }

/* Panel */
.panel{ border: 1px solid rgba(255,255,255,0.04); border-radius:14px; padding:16px; 
  background: linear-gradient(180deg, rgba(10,12,15,0.55), rgba(8,10,12,0.45));
  backdrop-filter: blur(6px); box-shadow: 0 8px 28px rgba(2,6,12,0.5); }

/* small legend */
.analytics-legend{
  border-radius:12px; padding:12px; background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
  border:1px solid rgba(255,255,255,0.03); box-shadow: 0 6px 18px rgba(2,6,12,0.45); margin-bottom:16px;
}
.legend-grid{ display:flex; gap:18px; flex-wrap:wrap; }
.legend-item{ min-width:200px; font-size:13px; opacity:0.9; }

/* Plot backgrounds */
.relayout .plotly, .js-plotly-plot { background: transparent !important; }

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
      <div class="sb-caption">Explore visuals:</div>
      <div style="margin-top:8px">
        <span class="sb-chip">🗺️ Geomap</span>
        <span class="sb-chip">📈 Scatter</span>
        <span class="sb-chip">🥧 Pie</span>
        <span class="sb-chip">📦 Box</span>
      </div>
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sb-caption">All charts are interactive — hover & zoom.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======= BANNER =======
st.markdown("""<div class="banner"><div class="banner-in">
  <h2 style="margin:0">Analytics</h2>
  <p>Explore Gurgaon market visuals — hover charts to inspect values.</p>
</div></div>""", unsafe_allow_html=True)

# ======= LEGEND / CONTEXT CARD (beneath banner) =======
st.markdown("""
<div class="analytics-legend">
  <div class="legend-grid">
    <div class="legend-item"><strong>Map</strong><div style="opacity:0.85;font-size:13px">Sector centroids show average price_per_sqft. Size = avg built_up_area.</div></div>
    <div class="legend-item"><strong>WordCloud</strong><div style="opacity:0.85;font-size:13px">Text features from listings highlighting frequent terms.</div></div>
    <div class="legend-item"><strong>Scatter</strong><div style="opacity:0.85;font-size:13px">Built-up area vs price; color = BHK.</div></div>
    <div class="legend-item"><strong>Distribution</strong><div style="opacity:0.85;font-size:13px">KDEs show price distribution split by property type.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ======= LOAD DATA =======
@st.cache_data
def load():
    return (pd.read_csv('datasets/data_viz1.csv'),
            pickle.load(open('datasets/feature_text.pkl','rb')))
new_df, feature_text = load()
group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]

# ======= TABS & CHARTS =======
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["🗺️ Geomap","☁️ WordCloud","📈 Area vs Price","🥧 BHK Pie","📦 BHK Box","📉 Distributions"]
)

with tab1:
    st.caption("Sector-wise average price per sqft (hover).")
    fig = px.scatter_mapbox(
        group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
        color_continuous_scale=["#0ea5e9","#22c55e","#a78bfa","#f59e0b"],
        zoom=10, mapbox_style="carto-positron", height=650, hover_name=group_df.index
    )
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.caption("Textured feature cloud.")
    wc = WordCloud(width=1300, height=480, background_color=None, mode="RGBA",
                   colormap="viridis", stopwords={'s'}).generate(feature_text)
    plt.figure(figsize=(12,4)); plt.imshow(wc, interpolation='bilinear'); plt.axis("off")
    st.pyplot(plt.gcf(), clear_figure=True)

with tab3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    ptype = st.selectbox('Property Type', ['flat','house'], key="ptype_scatter")
    data = new_df[new_df['property_type']==ptype]
    fig1 = px.scatter(data, x="built_up_area", y="price", color="bedRoom",
                      opacity=.9, labels={"bedRoom":"BHK"})
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=600)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    options = ['overall'] + new_df['sector'].unique().tolist()
    sect = st.selectbox('Sector', options, key="sector_pie")
    data = new_df if sect=='overall' else new_df[new_df['sector']==sect]
    fig2 = px.pie(data, names='bedRoom', hole=.35)
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

with tab5:
    fig3 = px.box(new_df[new_df['bedRoom']<=4], x='bedRoom', y='price', points='suspectedoutliers')
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

with tab6:
    fig4 = plt.figure(figsize=(10,4))
    sns.kdeplot(new_df[new_df['property_type']=='house']['price'], label='house', linewidth=2)
    sns.kdeplot(new_df[new_df['property_type']=='flat']['price'], label='flat', linewidth=2)
    plt.legend(); st.pyplot(fig4)
