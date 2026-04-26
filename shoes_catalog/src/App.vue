<template>
  <div>
    <header>
      <h1>👟 Sport Shoes Catalog</h1>
      <nav>
        <button :class="{ active: view === 'add' }" @click="view = 'add'">Add a product</button>
        <button :class="{ active: view === 'list' }" @click="view = 'list'">View all products</button>
      </nav>
    </header>
    <main>
      <AddProduct v-if="view === 'add'" />
      <ProductList v-if="view === 'list'" />
    </main>
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
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: #f5f5f5; }
header {
  background: #1a1a2e;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
header h1 { color: white; font-size: 20px; }
nav button {
  background: transparent;
  border: 2px solid white;
  color: white;
  padding: 8px 18px;
  margin-left: 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
nav button:hover, nav button.active {
  background: white;
  color: #1a1a2e;
}
main { max-width: 1100px; margin: 40px auto; padding: 0 24px; }
</style>