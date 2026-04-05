<template>
  <div>
    <input
      id="search-input"
      type="text"
      class="search"
      placeholder="Search by name..."
    />

    <p class="count">{{ products.length }} product(s) found</p>

    <div v-if="products.length === 0" class="empty">No products found.</div>

    <div class="grid">
      <div class="card" v-for="product in products" :key="product.id">
        <img :src="product.image_url" :alt="product.name"
             onerror="this.src='https://placehold.co/300x200?text=No+Image'" />
        <div class="body">
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <span class="price">{{ product.price.toFixed(2) }} DZD</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return { products: [] }
  },
  mounted() {
    this.fetch('')
    // jQuery live search — sends request on every keypress
    $('#search-input').on('input', () => {
      this.fetch($('#search-input').val())
    })
  },
  methods: {
    fetch(q) {
      const url = q ? `${API}/products?q=${encodeURIComponent(q)}` : `${API}/products`
      $.get(url, data => { this.products = data })
    }
  }
}
</script>

<style scoped>
.search {
  width: 100%; padding: 12px 16px;
  border: 1px solid #ddd; border-radius: 8px;
  font-size: 15px; outline: none;
  margin-bottom: 20px;
}
.search:focus { border-color: #1a1a2e; }
.count { font-size: 13px; color: #999; margin-bottom: 20px; }
.empty { text-align: center; color: #999; margin-top: 60px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 24px; }
.card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); transition: transform 0.2s; }
.card:hover { transform: translateY(-4px); }
.card img { width: 100%; height: 200px; object-fit: cover; }
.body { padding: 16px; }
h3 { font-size: 17px; margin-bottom: 8px; }
p { font-size: 14px; color: #666; margin-bottom: 12px; line-height: 1.5; }
.price { font-size: 18px; font-weight: bold; color: #1a1a2e; }
</style>