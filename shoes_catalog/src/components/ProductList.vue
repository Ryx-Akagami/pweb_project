<template>
  <div class="list-root">

    <!-- Toolbar: search + filters -->
    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
          <circle cx="6.5" cy="6.5" r="5" stroke="#6B6B6B" stroke-width="1.5"/>
          <path d="M10.5 10.5L14 14" stroke="#6B6B6B" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name…"
          @input="onSearch"
        />
        <button v-if="searchQuery" class="search-clear" @click="searchQuery = ''; fetchProducts()">✕</button>
      </div>

      <div class="filters">
        <!-- Sort -->
        <div class="filter-group">
          <label class="filter-label">Sort by</label>
          <div class="select-wrap">
            <select v-model="sortBy" @change="applyFilters">
              <option value="">Default</option>
              <option value="price_asc">Price ↑</option>
              <option value="price_desc">Price ↓</option>
              <option value="name_asc">Name A–Z</option>
            </select>
            <svg width="10" height="6" viewBox="0 0 10 6" fill="none" class="select-arrow">
              <path d="M1 1l4 4 4-4" stroke="#6B6B6B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>

        <!-- Min price -->
        <div class="filter-group">
          <label class="filter-label">Min (DZD)</label>
          <input class="price-input" v-model.number="minPrice" type="number" placeholder="0" @input="applyFilters" />
        </div>

        <!-- Max price -->
        <div class="filter-group">
          <label class="filter-label">Max (DZD)</label>
          <input class="price-input" v-model.number="maxPrice" type="number" placeholder="∞" @input="applyFilters" />
        </div>

        <button class="btn-reset" @click="resetFilters" title="Reset all filters">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
            <path d="M1 6.5A5.5 5.5 0 1 0 6.5 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M1 1v5.5h5.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Reset
        </button>
      </div>
    </div>

    <!-- Stats row -->
    <div class="stats-row">
      <span class="stats-count">
        <strong>{{ displayed.length }}</strong> product{{ displayed.length !== 1 ? 's' : '' }}
        <span v-if="searchQuery || minPrice || maxPrice || sortBy" class="stats-filtered"> — filtered</span>
      </span>
    </div>

    <!-- Empty state -->
    <div v-if="displayed.length === 0" class="empty">
      <div class="empty-icon">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <circle cx="24" cy="24" r="23" stroke="#DDDBD5" stroke-width="2"/>
          <path d="M14 20c0-5.523 4.477-10 10-10s10 4.477 10 10v8H14v-8z" stroke="#DDDBD5" stroke-width="2"/>
          <rect x="12" y="28" width="24" height="12" rx="3" stroke="#DDDBD5" stroke-width="2"/>
        </svg>
      </div>
      <p class="empty-title">No products found</p>
      <p class="empty-sub">Try adjusting your search or filters</p>
    </div>

    <!-- Product grid -->
    <div class="grid" v-else>
      <div
        class="card"
        v-for="(product, i) in displayed"
        :key="product.id"
        :style="{ animationDelay: (i * 60) + 'ms' }"
      >
        <!-- Delete button -->
        <button class="card-delete" @click.stop="deleteProduct(product)" title="Remove product">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M1 1l10 10M11 1L1 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>

        <!-- Image -->
        <div class="card-img-wrap">
          <img
            class="card-img"
            :src="product.image_url"
            :alt="product.name"
            onerror="this.src='https://placehold.co/400x260/F2F0EB/C8C5BC?text=No+Image'"
          />
          <div class="card-img-fade"></div>
        </div>

        <!-- Body -->
        <div class="card-body">
          <p class="card-name">{{ product.name }}</p>
          <p class="card-desc">{{ product.description }}</p>

          <div class="card-footer">
            <div class="price-block">
              <span class="price-amount">{{ product.price.toLocaleString() }}</span>
              <span class="price-unit">DZD</span>
            </div>
            <div class="card-chip">In stock</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <transition name="modal">
      <div class="modal-backdrop" v-if="confirmTarget" @click.self="confirmTarget = null">
        <div class="modal">
          <div class="modal-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6" stroke="#1A6B3C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3 class="modal-title">Remove product?</h3>
          <p class="modal-sub">
            <strong>{{ confirmTarget && confirmTarget.name }}</strong> will be permanently deleted.
          </p>
          <div class="modal-actions">
            <button class="btn-cancel" @click="confirmTarget = null">Cancel</button>
            <button class="btn-confirm" @click="confirmDelete">Remove</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Toast -->
    <transition name="toast">
      <div class="toast" v-if="toast" :class="toast.type">
        <span class="toast-dot"></span>
        {{ toast.msg }}
      </div>
    </transition>
  </div>
</template>

<script>
const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      allProducts: [],
      displayed: [],
      searchQuery: '',
      sortBy: '',
      minPrice: '',
      maxPrice: '',
      confirmTarget: null,
      toast: null,
      toastTimer: null
    }
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      try {
        const q = this.searchQuery
        const url = q
          ? `${API}/products?q=${encodeURIComponent(q)}`
          : `${API}/products`
        const res = await fetch(url)
        this.allProducts = await res.json()
        this.applyFilters()
      } catch {
        this.showToast('Cannot connect to server', 'error')
      }
    },
    onSearch() {
      this.fetchProducts()
    },
    applyFilters() {
      let list = [...this.allProducts]

      if (this.minPrice !== '' && !isNaN(this.minPrice))
        list = list.filter(p => p.price >= Number(this.minPrice))

      if (this.maxPrice !== '' && !isNaN(this.maxPrice))
        list = list.filter(p => p.price <= Number(this.maxPrice))

      if (this.sortBy === 'price_asc') list.sort((a, b) => a.price - b.price)
      else if (this.sortBy === 'price_desc') list.sort((a, b) => b.price - a.price)
      else if (this.sortBy === 'name_asc') list.sort((a, b) => a.name.localeCompare(b.name))

      this.displayed = list
    },
    resetFilters() {
      this.searchQuery = ''
      this.sortBy = ''
      this.minPrice = ''
      this.maxPrice = ''
      this.fetchProducts()
    },
    deleteProduct(p) {
      this.confirmTarget = p
    },
    async confirmDelete() {
      if (!this.confirmTarget) return
      const id = this.confirmTarget.id
      this.confirmTarget = null
      try {
        const res = await fetch(`${API}/products/${id}`, { method: 'DELETE' })
        if (res.ok) {
          this.showToast('Product removed successfully', 'success')
          this.fetchProducts()
        } else {
          this.showToast('Failed to delete product', 'error')
        }
      } catch {
        this.showToast('Cannot connect to server', 'error')
      }
    },
    showToast(msg, type) {
      if (this.toastTimer) clearTimeout(this.toastTimer)
      this.toast = { msg, type }
      this.toastTimer = setTimeout(() => { this.toast = null }, 3200)
    }
  }
}
</script>

<style scoped>
.list-root { position: relative; }

/* ── Toolbar ── */
.toolbar {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  animation: fadeUp 0.4s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: none; }
}

/* Search */
.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 200px;
}

.search-icon {
  position: absolute;
  left: 14px;
  pointer-events: none;
  flex-shrink: 0;
}

.search-wrap input {
  width: 100%;
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 14.5px;
  padding: 10px 38px 10px 42px;
  outline: none;
  transition: border-color 0.18s, box-shadow 0.18s;
  box-shadow: var(--shadow-s);
}

.search-wrap input::placeholder { color: #B0ADA6; }
.search-wrap input:focus {
  border-color: var(--green);
  box-shadow: 0 0 0 3px rgba(26,107,60,0.1);
}

.search-clear {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: var(--muted);
  cursor: pointer;
  font-size: 12px;
  padding: 2px;
  line-height: 1;
  transition: color 0.15s;
}
.search-clear:hover { color: var(--ink); }

/* Filters */
.filters {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 1.5px;
  color: var(--muted);
  text-transform: uppercase;
}

.select-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.select-wrap select {
  appearance: none;
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 13.5px;
  padding: 9px 32px 9px 12px;
  cursor: pointer;
  outline: none;
  box-shadow: var(--shadow-s);
  transition: border-color 0.18s;
  min-width: 130px;
}

.select-wrap select:focus { border-color: var(--green); }

.select-arrow {
  position: absolute;
  right: 10px;
  pointer-events: none;
}

.price-input {
  width: 100px;
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 13.5px;
  padding: 9px 12px;
  outline: none;
  box-shadow: var(--shadow-s);
  transition: border-color 0.18s;
}

.price-input:focus { border-color: var(--green); }

.price-input::-webkit-inner-spin-button { opacity: 0.4; }

.btn-reset {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--off-white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  color: var(--muted);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  padding: 9px 14px;
  cursor: pointer;
  transition: all 0.18s;
  white-space: nowrap;
  box-shadow: var(--shadow-s);
}
.btn-reset:hover { color: var(--green); border-color: var(--green); background: var(--green-pale); }

/* ── Stats row ── */
.stats-row {
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
  animation: fadeUp 0.4s 0.08s ease both;
}

.stats-count {
  font-size: 13.5px;
  color: var(--muted);
}

.stats-count strong { color: var(--ink); font-weight: 600; }

.stats-filtered {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--green);
  letter-spacing: 0.5px;
}

/* ── Empty ── */
.empty {
  text-align: center;
  padding: 80px 20px;
  animation: fadeUp 0.4s ease both;
}

.empty-icon { margin-bottom: 20px; opacity: 0.5; }
.empty-title {
  font-family: var(--font-display);
  font-size: 22px;
  color: var(--ink);
  margin-bottom: 8px;
}
.empty-sub {
  font-size: 14px;
  color: var(--muted);
}

/* ── Grid ── */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

/* ── Card ── */
.card {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  transition: border-color 0.22s, box-shadow 0.22s, transform 0.22s;
  animation: cardIn 0.5s ease both;
  box-shadow: var(--shadow-s);
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: none; }
}

.card:hover {
  border-color: var(--green);
  box-shadow: var(--shadow-l);
  transform: translateY(-4px);
}

/* Delete btn */
.card-delete {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(255,255,255,0.9);
  border: 1px solid var(--border);
  color: var(--muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.18s;
  backdrop-filter: blur(4px);
  box-shadow: var(--shadow-s);
}

.card:hover .card-delete { opacity: 1; }
.card-delete:hover { background: #FFF0F0; border-color: #FFB3B3; color: #D9534F; }

/* Image */
.card-img-wrap {
  position: relative;
  height: 210px;
  overflow: hidden;
  background: var(--off-white);
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.45s ease;
}

.card:hover .card-img { transform: scale(1.05); }

.card-img-fade {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(250,250,248,0.6) 0%, transparent 50%);
  pointer-events: none;
}

/* Body */
.card-body { padding: 18px 20px 16px; }

.card-name {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 7px;
  line-height: 1.15;
}

.card-desc {
  font-size: 13.5px;
  color: var(--muted);
  line-height: 1.65;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}

.price-block { display: flex; align-items: baseline; gap: 5px; }

.price-amount {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--green);
  line-height: 1;
}

.price-unit {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--muted);
  letter-spacing: 1px;
}

.card-chip {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 1px;
  color: var(--green);
  background: var(--green-light);
  border: 1px solid rgba(26,107,60,0.2);
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
}

/* ── Modal ── */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.28);
  backdrop-filter: blur(4px);
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: 14px;
  padding: 36px 40px;
  width: 360px;
  max-width: 92vw;
  text-align: center;
  box-shadow: var(--shadow-l);
}

.modal-icon {
  width: 52px;
  height: 52px;
  background: var(--green-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.modal-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 10px;
}

.modal-sub {
  font-size: 14px;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 28px;
}

.modal-actions { display: flex; gap: 10px; }

.btn-cancel {
  flex: 1;
  padding: 12px;
  background: var(--off-white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  color: var(--muted);
  font-family: var(--font-body);
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.18s;
}
.btn-cancel:hover { border-color: var(--border-dark); color: var(--ink); }

.btn-confirm {
  flex: 1;
  padding: 12px;
  background: #D9534F;
  border: none;
  border-radius: var(--radius);
  color: #fff;
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.18s;
}
.btn-confirm:hover { background: #C9302C; }

/* Modal transition */
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: transform 0.22s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal { transform: scale(0.94) translateY(12px); }
.modal-leave-to .modal { transform: scale(0.94) translateY(12px); }

/* ── Toast ── */
.toast {
  position: fixed;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 600;
  background: var(--ink);
  color: #fff;
  padding: 12px 22px;
  border-radius: 40px;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  white-space: nowrap;
}

.toast.success .toast-dot { background: var(--green); }
.toast.error .toast-dot { background: #D9534F; }

.toast-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.toast-enter-active, .toast-leave-active { transition: all 0.25s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(-50%) translateY(12px); }
</style>