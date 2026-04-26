<template>
  <div>
    <!-- Search bar -->
    <div class="search-wrap">
      <div class="search-icon">⌕</div>
      <input
        id="search-input"
        type="text"
        placeholder="SEARCH BY NAME..."
        v-model="searchQuery"
      />
      <div class="search-count" v-if="searchQuery">
        {{ products.length }} RESULTS
      </div>
    </div>

    <!-- Stats bar -->
    <div class="stats-bar">
      <div class="stat">
        <span class="stat-num">{{ products.length }}</span>
        <span class="stat-label">PRODUCTS</span>
      </div>
      <div class="stat-divider">|</div>
      <div class="stat">
        <span class="stat-num">{{ searchQuery ? 'FILTERED' : 'ALL' }}</span>
        <span class="stat-label">VIEW</span>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="products.length === 0" class="empty">
      <div class="empty-icon">👟</div>
      <div class="empty-title">NO PRODUCTS FOUND</div>
      <div class="empty-sub">Try a different search or add a new product</div>
    </div>

    <!-- Grid -->
    <div class="grid">
      <div
        class="card"
        v-for="(product, i) in products"
        :key="product.id"
        :style="{ animationDelay: (i * 80) + 'ms' }"
      >
        <!-- Image -->
        <div class="card-img-wrap">
          <img
            class="card-img"
            :src="product.image_url"
            :alt="product.name"
            onerror="this.src='https://placehold.co/400x240/141414/333?text=NO+IMAGE'"
          />
          <div class="card-img-overlay"></div>
          <div class="card-badge">IN STOCK</div>
        </div>

        <!-- Body -->
        <div class="card-body">
          <div class="card-name">{{ product.name }}</div>
          <div class="card-desc">{{ product.description }}</div>
          <div class="card-footer">
            <div class="price-wrap">
              <div class="price-label">PRICE</div>
              <div class="price">{{ product.price.toFixed(2) }}</div>
              <div class="price-currency">DZD</div>
            </div>
            <div class="card-arrow">→</div>
          </div>
        </div>

        <!-- Hover line -->
        <div class="card-line"></div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      products: [],
      searchQuery: ''
    }
  },
  mounted() {
    this.fetchProducts('')
    $('#search-input').on('input', () => {
      this.searchQuery = $('#search-input').val()
      this.fetchProducts(this.searchQuery)
    })
  },
  methods: {
    fetchProducts(q) {
      const url = q
        ? `${API}/products?q=${encodeURIComponent(q)}`
        : `${API}/products`
      $.get(url, data => { this.products = data })
    }
  }
}
</script>

<style scoped>
/* ── Search ── */
.search-wrap {
  position: relative;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  animation: fadeUp 0.4s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: none; }
}

.search-icon {
  font-size: 22px;
  color: var(--green);
  flex-shrink: 0;
}

#search-input {
  flex: 1;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 3px;
  color: var(--white);
  font-family: var(--font-cond);
  font-size: 15px;
  letter-spacing: 2px;
  padding: 14px 20px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  text-transform: uppercase;
}

#search-input::placeholder {
  color: #2a2a2a;
  letter-spacing: 3px;
}

#search-input:focus {
  border-color: var(--green);
  box-shadow: 0 0 0 3px rgba(0,255,135,0.07);
}

.search-count {
  font-family: var(--font-cond);
  font-size: 12px;
  letter-spacing: 2px;
  color: var(--green);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Stats bar ── */
.stats-bar {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 36px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
  animation: fadeUp 0.4s 0.1s ease both;
}

.stat { display: flex; align-items: baseline; gap: 8px; }

.stat-num {
  font-family: var(--font-display);
  font-size: 22px;
  color: var(--green);
  letter-spacing: 2px;
}

.stat-label {
  font-family: var(--font-cond);
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--muted);
  text-transform: uppercase;
}

.stat-divider { color: var(--border); font-size: 18px; }

/* ── Empty ── */
.empty {
  text-align: center;
  padding: 100px 20px;
  animation: fadeUp 0.4s ease both;
}

.empty-icon { font-size: 52px; margin-bottom: 20px; opacity: 0.3; }

.empty-title {
  font-family: var(--font-display);
  font-size: 28px;
  letter-spacing: 4px;
  color: var(--muted);
  margin-bottom: 10px;
}

.empty-sub {
  font-family: var(--font-cond);
  font-size: 13px;
  letter-spacing: 1px;
  color: #333;
  text-transform: uppercase;
}

/* ── Grid ── */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

/* ── Card ── */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  transition: border-color 0.25s, transform 0.25s;
  animation: cardIn 0.5s ease both;
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to   { opacity: 1; transform: none; }
}

.card:hover {
  border-color: var(--green);
  transform: translateY(-5px);
}

.card:hover .card-line { width: 100%; }
.card:hover .card-arrow { transform: translateX(4px); color: var(--green); }
.card:hover .card-img { transform: scale(1.06); }

/* Image */
.card-img-wrap {
  position: relative;
  overflow: hidden;
  height: 220px;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.5s ease;
}

.card-img-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, var(--card) 0%, transparent 50%);
  pointer-events: none;
}

.card-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--green);
  color: #000;
  font-family: var(--font-cond);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  padding: 4px 10px;
  border-radius: 2px;
  text-transform: uppercase;
}

/* Body */
.card-body { padding: 20px 20px 16px; }

.card-name {
  font-family: var(--font-display);
  font-size: 24px;
  letter-spacing: 2px;
  color: var(--white);
  margin-bottom: 8px;
  line-height: 1;
}

.card-desc {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 18px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}

.price-wrap { display: flex; align-items: baseline; gap: 4px; }

.price-label {
  font-family: var(--font-cond);
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--muted);
  margin-right: 4px;
}

.price {
  font-family: var(--font-display);
  font-size: 26px;
  color: var(--green);
  letter-spacing: 1px;
  line-height: 1;
}

.price-currency {
  font-family: var(--font-cond);
  font-size: 12px;
  color: var(--muted);
  letter-spacing: 1px;
}

.card-arrow {
  font-size: 20px;
  color: var(--muted);
  transition: all 0.2s;
}

/* Hover line at bottom */
.card-line {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 0;
  background: linear-gradient(90deg, var(--green), var(--green2));
  transition: width 0.4s ease;
}
</style>