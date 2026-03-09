import streamlit as st

# ── Page config is set in the main entry point, not here ─────────────────────

# ═════════════════════════════════════════════════════════════════════════════
# HERO SECTION  — animated dark banner with geometric H₂ molecule motif
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

  /* ── Reset Streamlit default padding for this page ── */
  .block-container { padding-top: 1rem !important; }

  /* ── Hero banner ── */
  .hero-wrap {
    background: linear-gradient(135deg, #060d1a 0%, #0b1f38 45%, #0d2f3f 100%);
    border-radius: 16px;
    padding: 56px 48px 48px 48px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  /* Subtle hex-grid watermark */
  .hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
      repeating-linear-gradient(60deg,  transparent,  transparent  28px, rgba(32,160,160,.06) 28px, rgba(32,160,160,.06) 29px),
      repeating-linear-gradient(120deg, transparent,  transparent  28px, rgba(32,160,160,.06) 28px, rgba(32,160,160,.06) 29px),
      repeating-linear-gradient(0deg,   transparent,  transparent  28px, rgba(32,160,160,.06) 28px, rgba(32,160,160,.06) 29px);
    pointer-events: none;
  }
  /* Glowing orb accent */
  .hero-wrap::after {
    content: "";
    position: absolute;
    width: 380px; height: 380px;
    right: -80px; top: -120px;
    background: radial-gradient(circle, rgba(20,200,180,.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
  }

  .hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #14c8b4;
    margin: 0 0 14px 0;
  }
  .hero-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: clamp(1.9rem, 4vw, 2.9rem) !important;
    color: #ffffff !important;
    margin: 0 0 6px 0 !important;
    line-height: 1.15 !important;
    position: relative; z-index: 1 !important;
  }
  .hero-title em {
    font-style: italic !important;
    color: #14c8b4 !important;
  }
  .hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 1.05rem;
    color: #8bafc8;
    margin: 14px 0 32px 0;
    max-width: 620px;
    line-height: 1.65;
    position: relative; z-index: 1;
  }

  /* ── Stat pills ── */
  .stat-row {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 4px;
    position: relative; z-index: 1;
  }
  .stat-pill {
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(20,200,180,.25);
    border-radius: 100px;
    padding: 8px 18px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #14c8b4;
    line-height: 1;
  }
  .stat-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    color: #8bafc8;
    line-height: 1.2;
    font-weight: 400;
  }

  /* ── Section headers ── */
  .section-head {
    font-family: 'DM Serif Display', serif;
    font-size: 1.45rem;
    color: #1a2e40;
    margin: 0 0 4px 0;
    border-left: 3px solid #14c8b4;
    padding-left: 12px;
  }
  .section-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #4a6a80;
    margin: 0 0 20px 12px;
    font-weight: 400;
  }

  /* ── Page cards ── */
  .page-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 16px;
    margin-top: 8px;
  }
  .page-card {
    background: linear-gradient(145deg, #0d1e30 0%, #0a1928 100%);
    border: 1px solid rgba(20,200,180,.18);
    border-radius: 12px;
    padding: 22px 22px 18px 22px;
    transition: border-color .2s, transform .2s;
    cursor: default;
  }
  .page-card:hover {
    border-color: rgba(20,200,180,.55);
    transform: translateY(-2px);
  }
  .page-card-icon {
    font-size: 1.7rem;
    margin-bottom: 10px;
    display: block;
  }
  .page-card-num {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #14c8b4;
    margin-bottom: 4px;
  }
  .page-card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.08rem;
    color: #dce8f5;
    margin: 0 0 8px 0;
  }
  .page-card-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.83rem;
    color: #6a90ab;
    line-height: 1.55;
    font-weight: 300;
    margin: 0;
  }
  .page-card-tags {
    margin-top: 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .tag {
    background: rgba(20,200,180,.1);
    border: 1px solid rgba(20,200,180,.2);
    color: #14c8b4;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    padding: 3px 9px;
    border-radius: 100px;
    letter-spacing: 0.04em;
  }

  /* ── How-to steps ── */
  .steps-wrap {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 14px;
    margin-top: 8px;
  }
  .step-box {
    background: #f4f9fb;
    border: 1px solid rgba(20,200,180,.25);
    border-radius: 10px;
    padding: 18px 18px 14px 18px;
  }
  .step-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #14c8b4;
    line-height: 1;
    margin-bottom: 6px;
  }
  .step-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #1a2e40;
    margin-bottom: 4px;
  }
  .step-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    color: #3a5a70;
    line-height: 1.5;
    font-weight: 400;
  }

  /* ── About callout ── */
  .about-box {
    background: linear-gradient(135deg, #081320 0%, #0c1e30 100%);
    border: 1px solid rgba(245,180,50,.18);
    border-left: 4px solid #f5b432;
    border-radius: 10px;
    padding: 22px 24px;
    margin-top: 8px;
  }
  .about-box p {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #8aabbf;
    line-height: 1.7;
    margin: 0;
    font-weight: 300;
  }
  .about-box strong {
    color: #f5b432;
    font-weight: 500;
  }
</style>

<!-- ═══ HERO ═══ -->
<div class="hero-wrap">
  <p class="hero-eyebrow">Research Intelligence Dashboard &nbsp;·&nbsp; 2024 – 2026</p>
  <h1 class="hero-title">Waste<em>2</em>Hydrogen<br>ML Dashboard</h1>
  <p class="hero-subtitle">
    A structured analytical portal synthesising <strong style="color:#c8daea;">29 peer-reviewed papers</strong>
    on machine learning applications for hydrogen production from waste feedstocks —
    covering thermochemical, biological, and electrochemical conversion routes.
  </p>
  <div class="stat-row">
    <div class="stat-pill">
      <span class="stat-num">29</span>
      <span class="stat-label">Papers<br>reviewed</span>
    </div>
    <div class="stat-pill">
      <span class="stat-num">29</span>
      <span class="stat-label">ML algorithms<br>catalogued</span>
    </div>
    <div class="stat-pill">
      <span class="stat-num">17</span>
      <span class="stat-label">H₂ production<br>routes</span>
    </div>
    <div class="stat-pill">
      <span class="stat-num">14</span>
      <span class="stat-label">Feedstock<br>types</span>
    </div>
    <div class="stat-pill">
      <span class="stat-num">22</span>
      <span class="stat-label">Countries &amp;<br>regions</span>
    </div>
    <div class="stat-pill">
      <span class="stat-num">14</span>
      <span class="stat-label">Journals<br>covered</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# ABOUT CALLOUT
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="about-box">
  <p>
    This dashboard was built to support structured literature synthesis on the intersection of
    <strong>machine learning</strong> and <strong>green hydrogen production from waste</strong>.
    It compiles papers published between 2024 and 2026, extracting process data, ML methodologies,
    interpretability approaches, and identified research gaps into a single queryable interface.
    Each paper is accompanied by a full technical summary with standardised fields for direct comparison.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<p class="section-head">Dashboard Pages</p>
<p class="section-sub">Four analytical modules — navigate from the sidebar</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-grid">

  <div class="page-card">
    <span class="page-card-icon">📊</span>
    <p class="page-card-num">Page 1</p>
    <p class="page-card-title">Overview</p>
    <p class="page-card-body">
      High-level landscape of the dataset: study types, ML family frequencies,
      dataset sizes, and publication trends across the 29 reviewed papers.
    </p>
    <div class="page-card-tags">
      <span class="tag">Dataset stats</span>
      <span class="tag">ML families</span>
      <span class="tag">Year trends</span>
    </div>
  </div>

  <div class="page-card">
    <span class="page-card-icon">⚗️</span>
    <p class="page-card-num">Page 2</p>
    <p class="page-card-title">Process Analysis</p>
    <p class="page-card-body">
      Explore hydrogen production routes and feedstock types. Interactive charts
      show route frequency, country distribution, and system flags. Filter papers
      by route, feedstock, study type, and more, with full technical explainers
      for every process and feedstock in the dataset.
    </p>
    <div class="page-card-tags">
      <span class="tag">H₂ routes</span>
      <span class="tag">Feedstocks</span>
      <span class="tag">Process explainers</span>
      <span class="tag">Query form</span>
    </div>
  </div>

  <div class="page-card">
    <span class="page-card-icon">🤖</span>
    <p class="page-card-num">Page 3</p>
    <p class="page-card-title">ML Analysis</p>
    <p class="page-card-body">
      Deep-dive into the ML methods applied across papers: algorithm frequency,
      optimisation methods, and interpretability techniques. Filter the paper set
      and read detailed technical explanations for every algorithm, optimiser,
      and XAI method found in the literature.
    </p>
    <div class="page-card-tags">
      <span class="tag">Algorithms</span>
      <span class="tag">Optimisation</span>
      <span class="tag">XAI / SHAP</span>
      <span class="tag">Method explainers</span>
    </div>
  </div>

  <div class="page-card">
    <span class="page-card-icon">📚</span>
    <p class="page-card-num">Page 4</p>
    <p class="page-card-title">Paper Explorer</p>
    <p class="page-card-body">
      Search and filter all 29 papers by title, author, journal, route, ML family,
      and more. Select any paper to read its complete structured technical summary —
      objective, system description, modelling approach, key results, strengths,
      limitations, and research gaps — with a direct link to the full paper.
    </p>
    <div class="page-card-tags">
      <span class="tag">Full-text search</span>
      <span class="tag">Technical summaries</span>
      <span class="tag">Drive links</span>
      <span class="tag">Research gaps</span>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# HOW TO USE
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<p class="section-head">How to Use This Dashboard</p>
<p class="section-sub">A suggested navigation path for first-time users</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="steps-wrap">

  <div class="step-box">
    <div class="step-num">01</div>
    <div class="step-title">Start with Overview</div>
    <div class="step-body">
      Get a feel for the dataset composition — how many papers use experimental
      vs. simulation data, which ML families dominate, and how the literature
      is distributed by year.
    </div>
  </div>

  <div class="step-box">
    <div class="step-num">02</div>
    <div class="step-title">Explore Processes</div>
    <div class="step-body">
      Use the Process Analysis page to understand which hydrogen production
      routes and feedstocks are most studied, and read the process explainers
      to build domain context before diving into ML.
    </div>
  </div>

  <div class="step-box">
    <div class="step-num">03</div>
    <div class="step-title">Analyse ML Methods</div>
    <div class="step-body">
      In the ML Analysis page, filter papers by algorithm or interpretability
      method, then expand the technical explainers to understand how each
      method is applied in the hydrogen production context.
    </div>
  </div>

  <div class="step-box">
    <div class="step-num">04</div>
    <div class="step-title">Read the Papers</div>
    <div class="step-body">
      Use the Paper Explorer to search by keyword, narrow down by route or
      ML family, and read full structured technical summaries side-by-side.
      Open the Drive link to access the original paper directly.
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SCOPE NOTE
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<p class="section-head">Scope & Coverage</p>
<p class="section-sub">What is and is not included in this review</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **✅ Included**
    - Papers published 2024 – 2026
    - Studies applying ML to hydrogen production from waste feedstocks
    - Thermochemical routes: gasification, SCWG, pyrolysis, HTL
    - Biological routes: dark fermentation, photofermentation, biophotolysis
    - Electrochemical routes: electrolysis
    - Reforming routes: biogas SR + DR
    - Integrated and hybrid system studies
    - Review, simulation, and original research paper types
    """)

with col2:
    st.markdown("""
    **❌ Not included**
    - Papers without a direct ML modelling or application component
    - Grey literature, theses, conference abstracts without full text
    - Studies on fossil-fuel-based hydrogen production without waste co-feed
    - Papers pre-dating 2024
    - Studies focused purely on catalyst or materials development with no process ML
    - Techno-economic analyses without an ML predictive or optimisation model
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  border-top: 1px solid rgba(20,200,180,.15);
  padding-top: 18px;
  margin-top: 8px;
  text-align: center;
">
  <p style="
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    color: #3a5a70;
    margin: 0;
    letter-spacing: 0.04em;
  ">
    Waste2Hydrogen ML Dashboard &nbsp;·&nbsp; 29 papers &nbsp;·&nbsp; 2024 – 2026 literature &nbsp;·&nbsp;
    Navigate using the <strong style="color:#14c8b4;">sidebar</strong> ←
  </p>
</div>
""", unsafe_allow_html=True)
