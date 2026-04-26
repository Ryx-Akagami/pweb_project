<template>
  <div id="root">
    <!-- Subtle noise texture overlay -->
    <div class="noise"></div>

    <!-- Header -->
    <header>
      <div class="logo">
        <div class="logo-mark">
          <span class="logo-bolt">⚡</span>
        </div>
        <div class="logo-text">
          Nebbak<span class="logo-accent"> for Choses</span>
        </div>
      </div>

      <nav>
        <button :class="{ active: view === 'add' }" @click="view = 'add'">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Add Product
        </button>
        <button :class="{ active: view === 'list' }" @click="view = 'list'">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <rect x="1" y="1" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="8" y="1" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="1" y="8" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="8" y="8" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/>
          </svg>
          Catalog
        </button>
      </nav>

      <div class="header-tag">EST. 2026</div>
    </header>

    <!-- Hero strip -->
    <div class="hero">
      <div class="hero-left">
        <span class="hero-eyebrow">{{ view === 'add' ? 'NEW DROP' : 'COLLECTION' }}</span>
        <h1 class="hero-title" v-if="view === 'add'">Add a <em>Fresh</em> Pair</h1>
        <h1 class="hero-title" v-if="view === 'list'">The <em>Catalog</em></h1>
      </div>
      <div class="hero-right">
        <div class="hero-stat">
          <span class="hero-stat-num">2026</span>
          <span class="hero-stat-label">Season</span>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-stat">
          <span class="hero-stat-num">DZD</span>
          <span class="hero-stat-label">Currency</span>
        </div>
      </div>
    </div>

    <!-- Content -->
    <main>
      <AddProduct v-if="view === 'add'" />
      <ProductList v-if="view === 'list'" />
    </main>

    <!-- Footer -->
    <footer>
      <span class="footer-logo">Nebbak for choses</span>
      <span class="footer-sep">—</span>
      <span class="footer-copy">Sport Shoes Catalog © 2026</span>
      <div class="footer-line"></div>
    </footer>
  </div>
</template>

<script>
import AddProduct from './components/AddProduct.vue'
import ProductList from './components/ProductList.vue'

export default {
  components: { AddProduct, ProductList },
  data() {
    return { view: 'add' }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --white:      #FAFAF8;
  --off-white:  #F2F0EB;
  --paper:      #ECEAE4;
  --green:      #1A6B3C;
  --green-mid:  #2D8A54;
  --green-light:#EBF5EF;
  --green-pale: #F3FAF5;
  --black:      #0D0D0D;
  --ink:        #1C1C1C;
  --muted:      #6B6B6B;
  --border:     #DDDBD5;
  --border-dark:#C8C5BC;

  --font-display: 'Playfair Display', Georgia, serif;
  --font-body:    'DM Sans', sans-serif;
  --font-mono:    'DM Mono', monospace;

  --radius:   6px;
  --shadow-s: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-m: 0 4px 16px rgba(0,0,0,0.08), 0 2px 6px rgba(0,0,0,0.05);
  --shadow-l: 0 12px 40px rgba(0,0,0,0.10), 0 4px 12px rgba(0,0,0,0.06);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; font-size: 16px; }

body {
  background: var(--white);
  color: var(--ink);
  font-family: var(--font-body);
  min-height: 100vh;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

#root { position: relative; min-height: 100vh; display: flex; flex-direction: column; }

/* ── Noise texture ── */
.noise {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1000;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 256px;
}

/* ── Header ── */
header {
  position: sticky;
  top: 0;
  z-index: 200;
  background: rgba(250,250,248,0.92);
  backdrop-filter: blur(24px);
  border-bottom: 1px solid var(--border);
  padding: 0 56px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.logo-mark {
  width: 36px;
  height: 36px;
  background: var(--green);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.logo-bolt {
  font-size: 18px;
  filter: brightness(10);
}

.logo-text {
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 17px;
  letter-spacing: 3px;
  color: var(--ink);
  text-transform: uppercase;
}

.logo-accent { color: var(--green); }

nav {
  display: flex;
  background: var(--off-white);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 3px;
  gap: 2px;
}

nav button {
  background: transparent;
  border: none;
  color: var(--muted);
  padding: 7px 18px;
  border-radius: 4px;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 13.5px;
  font-weight: 500;
  transition: all 0.18s;
  display: flex;
  align-items: center;
  gap: 7px;
  white-space: nowrap;
}

nav button:hover { color: var(--ink); background: rgba(0,0,0,0.04); }

nav button.active {
  background: var(--white);
  color: var(--green);
  box-shadow: var(--shadow-s);
  font-weight: 600;
}

nav button.active svg { color: var(--green); }

.header-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--border-dark);
  text-transform: uppercase;
}

/* ── Hero ── */
.hero {
  background: var(--green-pale);
  border-bottom: 1px solid var(--border);
  padding: 48px 56px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  overflow: hidden;
  position: relative;
}

.hero::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 240px; height: 240px;
  background: radial-gradient(circle, rgba(26,107,60,0.08) 0%, transparent 70%);
  border-radius: 50%;
}

.hero-eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 3px;
  color: var(--green);
  text-transform: uppercase;
  display: block;
  margin-bottom: 10px;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(38px, 5vw, 64px);
  font-weight: 700;
  color: var(--ink);
  line-height: 1.05;
}

.hero-title em {
  font-style: italic;
  color: var(--green);
}

.hero-right {
  display: flex;
  align-items: center;
  gap: 28px;
  flex-shrink: 0;
}

.hero-stat { text-align: right; }

.hero-stat-num {
  display: block;
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  line-height: 1;
  margin-bottom: 4px;
}

.hero-stat-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--muted);
  text-transform: uppercase;
}

.hero-divider {
  width: 1px;
  height: 40px;
  background: var(--border-dark);
}

/* ── Main ── */
main {
  flex: 1;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
  padding: 52px 56px;
}

/* ── Footer ── */
footer {
  border-top: 1px solid var(--border);
  padding: 24px 56px;
  display: flex;
  align-items: center;
  gap: 14px;
  position: relative;
  overflow: hidden;
}

.footer-logo {
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 3px;
  color: var(--green);
  text-transform: uppercase;
}

.footer-sep { color: var(--border-dark); }

.footer-copy {
  font-size: 13px;
  color: var(--muted);
}

.footer-line {
  position: absolute;
  top: 0; left: 0;
  width: 120px; height: 2px;
  background: linear-gradient(90deg, var(--green), transparent);
}

/* ── Shared form & card utilities ── */
.btn-primary {
  background: var(--green);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 15px;
  padding: 14px 28px;
  cursor: pointer;
  transition: all 0.18s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary:hover { background: var(--green-mid); transform: translateY(-1px); box-shadow: var(--shadow-m); }
.btn-primary:active { transform: scale(0.99); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--off-white); }
::-webkit-scrollbar-thumb { background: var(--border-dark); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--green); }
</style>