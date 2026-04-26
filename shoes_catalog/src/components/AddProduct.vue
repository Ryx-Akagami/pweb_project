<template>
  <div class="form-wrap">
    <div class="form-card">
      <h2>Add a new product</h2>
      <div class="form-group">
        <label>Name *</label>
        <input v-model="form.name" type="text" placeholder="e.g. Nike Air Max" />
      </div>
      <div class="form-group">
        <label>Description *</label>
        <textarea v-model="form.description" placeholder="Describe the shoe..."></textarea>
      </div>
      <div class="form-group">
        <label>Price (DZD) *</label>
        <input v-model="form.price" type="number" placeholder="e.g. 12000" />
      </div>
      <div class="form-group">
        <label>Image URL *</label>
        <input v-model="form.image_url" type="text" placeholder="https://..." />
      </div>
      <button class="btn" @click="submit">Add Product</button>
      <div v-if="message" :class="['msg', type]">{{ message }}</div>
    </div>
  </div>
</template>

<script>
const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      form: { name: '', description: '', price: '', image_url: '' },
      message: '',
      type: ''
    }
  },
  methods: {
    async submit() {
      if (!this.form.name.trim())
        return this.show('Name is required', 'error')
      if (!this.form.description.trim())
        return this.show('Description is required', 'error')
      if (!this.form.price || this.form.price <= 0)
        return this.show('Enter a valid price', 'error')
      if (!this.form.image_url.trim())
        return this.show('Image URL is required', 'error')

      try {
        const res = await fetch(`${API}/products`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: this.form.name,
            description: this.form.description,
            price: parseFloat(this.form.price),
            image_url: this.form.image_url
          })
        })
        const data = await res.json()
        if (res.ok) {
          this.show('Product added successfully!', 'success')
          this.form = { name: '', description: '', price: '', image_url: '' }
        } else {
          this.show(data.error || 'Something went wrong', 'error')
        }
      } catch {
        this.show('Cannot connect to server', 'error')
      }
    },

    show(msg, type) {
      this.message = msg
      this.type = type
      setTimeout(() => { this.message = '' }, 4000)
    }
  }
}
</script>

<style scoped>
.form-wrap { max-width: 540px; margin: 0 auto; }
.form-card {
  background: white;
  border-radius: 12px;
  padding: 36px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
h2 { margin-bottom: 24px; font-size: 20px; }
.form-group { margin-bottom: 18px; }
label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: bold;
  color: #555;
}
input, textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
}
input:focus, textarea:focus { border-color: #1a1a2e; }
textarea { height: 100px; resize: vertical; }
.btn {
  width: 100%;
  padding: 12px;
  background: #1a1a2e;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
}
.btn:hover { background: #2d2d5e; }
.msg {
  margin-top: 14px;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 14px;
}
.msg.success { background: #d4edda; color: #155724; }
.msg.error   { background: #f8d7da; color: #721c24; }
</style>