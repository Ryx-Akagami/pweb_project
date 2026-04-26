<template>
  <div id="root">
    <!-- Animated background grid -->
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>

    <!-- Header -->
    <header>
      <div class="logo">
        <span class="logo-icon">⚡</span>
        <span class="logo-text">KICK<em>VAULT</em></span>
      </div>
      <nav>
        <button
          :class="{ active: view === 'add' }"
          @click="view = 'add'"
        >
          <span class="nav-icon">+</span> Add Product
        </button>
        <button
          :class="{ active: view === 'list' }"
          @click="view = 'list'"
        >
          <span class="nav-icon">◈</span> Catalog
        </button>
      </nav>
    </header>

    <!-- Hero -->
    <div class="hero">
      <div class="hero-tag">{{ view === 'add' ? '— NEW DROP' : '— COLLECTION' }}</div>
      <h1 class="hero-title" v-if="view === 'add'">
        ADD A <span class="accent">FRESH</span><br/>PAIR
      </h1>
      <h1 class="hero-title" v-if="view === 'list'">
        THE<br/><span class="accent">CATALOG</span>
      </h1>
      <div class="hero-line"></div>
    </div>

    <!-- Content -->
    <main>
      <AddProduct v-if="view === 'add'" />
      <ProductList v-if="view === 'list'" />
    </main>

    <!-- Footer -->
    <footer>
      <span>KICKVAULT © 2026</span>
      <span class="footer-dot">⚡</span>
      <span>SPORT SHOES CATALOG</span>
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
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@600;700&display=swap');

:root {
  --black:   #080808;
  --dark:    #101010;
  --card:    #141414;
  --border:  #222;
  --green:   #00ff87;
  --green2:  #00cc6a;
  --white:   #f0ede6;
  --muted:   #555;
  --font-display: 'Bebas Neue', sans-serif;
  --font-cond:    'Barlow Condensed', sans-serif;
  --font-body:    'Barlow', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: var(--black);
  color: var(--white);
  font-family: var(--font-body);
  min-height: 100vh;
  overflow-x: hidden;
}

#root { position: relative; min-height: 100vh; }

/* ── Animated background ── */
.bg-grid {
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,255,135,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,135,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

.bg-glow {
  position: fixed;
  top: -200px;
  right: -200px;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(0,255,135,0.06) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  animation: glowPulse 4s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.1); }
}

/* ── Header ── */
header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(8,8,8,0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  padding: 0 48px;
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-display);
  font-size: 26px;
  letter-spacing: 3px;
}

.logo-icon {
  color: var(--green);
  animation: iconSpin 3s ease-in-out infinite;
  display: inline-block;
}

@keyframes iconSpin {
  0%, 100% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(15deg) scale(1.2); }
}

.logo-text em {
  font-style: normal;
  color: var(--green);
}

nav { display: flex; gap: 6px; }

nav button {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 8px 20px;
  border-radius: 2px;
  cursor: pointer;
  font-family: var(--font-cond);
  font-size: 14px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-icon { font-size: 16px; }

nav button:hover {
  color: var(--white);
  border-color: var(--green);
}

nav button.active {
  background: var(--green);
  color: #000;
  border-color: var(--green);
  font-weight: 700;
}

/* ── Hero ── */
.hero {
  position: relative;
  z-index: 1;
  padding: 52px 48px 36px;
  border-bottom: 1px solid var(--border);
  overflow: hidden;
}

.hero-tag {
  font-family: var(--font-cond);
  font-size: 12px;
  letter-spacing: 4px;
  color: var(--green);
  margin-bottom: 12px;
  animation: fadeUp 0.6s ease both;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(60px, 9vw, 110px);
  line-height: 0.9;
  letter-spacing: 4px;
  color: var(--white);
  animation: fadeUp 0.6s 0.1s ease both;
}

.hero-title .accent { color: var(--green); }

.hero-line {
  margin-top: 28px;
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, var(--green), transparent);
  animation: expandLine 0.8s 0.3s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: none; }
}

@keyframes expandLine {
  from { width: 0; }
  to   { width: 80px; }
}

/* ── Main ── */
main {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 52px 48px;
}

/* ── Footer ── */
footer {
  position: relative;
  z-index: 1;
  border-top: 1px solid var(--border);
  padding: 20px 48px;
  display: flex;
  align-items: center;
  gap: 16px;
  font-family: var(--font-cond);
  font-size: 12px;
  letter-spacing: 2px;
  color: var(--muted);
  text-transform: uppercase;
}

.footer-dot { color: var(--green); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--black); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--green); }
</style>