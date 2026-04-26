<template>
  <div class="form-wrap">
    <div class="form-card">
      <div class="form-header">
        <div class="form-number">01</div>
        <div>
          <div class="form-subtitle">FILL IN THE DETAILS</div>
          <div class="form-title">NEW PRODUCT</div>
        </div>
      </div>

      <div class="form-body">
        <div class="form-row">
          <div class="form-group">
            <label>
              <span class="label-num">01</span>
              Shoe Name
            </label>
            <input
              v-model="form.name"
              type="text"
              placeholder="e.g. Nike Air Max"
              :class="{ filled: form.name }"
            />
          </div>
          <div class="form-group">
            <label>
              <span class="label-num">02</span>
              Price (DZD)
            </label>
            <input
              v-model="form.price"
              type="number"
              placeholder="e.g. 12000"
              :class="{ filled: form.price }"
            />
          </div>
        </div>

        <div class="form-group">
          <label>
            <span class="label-num">03</span>
            Description
          </label>
          <textarea
            v-model="form.description"
            placeholder="Describe the shoe — materials, fit, use case..."
            :class="{ filled: form.description }"
          ></textarea>
        </div>

        <div class="form-group">
          <label>
            <span class="label-num">04</span>
            Image URL
          </label>
          <input
            v-model="form.image_url"
            type="text"
            placeholder="https://..."
            :class="{ filled: form.image_url }"
          />
        </div>

        <!-- Preview -->
        <div class="preview" v-if="form.image_url">
          <div class="preview-label">PREVIEW</div>
          <img :src="form.image_url" alt="preview"
               onerror="this.style.display='none'" />
        </div>

        <button class="btn-submit" @click="submit" :class="{ loading: isLoading }">
          <span v-if="!isLoading">ADD TO CATALOG ⚡</span>
          <span v-else>ADDING...</span>
        </button>

        <div v-if="message" :class="['msg', type]">
          <span class="msg-icon">{{ type === 'success' ? '✓' : '✕' }}</span>
          {{ message }}
        </div>
      </div>
    </div>

    <!-- Side decoration -->
    <div class="side-deco">
      <div class="deco-text">SPORT SHOES CATALOG 2026</div>
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
      type: '',
      isLoading: false
    }
  },
  methods: {
    async submit() {
      if (!this.form.name.trim())
        return this.show('Shoe name is required', 'error')
      if (!this.form.description.trim())
        return this.show('Description is required', 'error')
      if (!this.form.price || this.form.price <= 0)
        return this.show('Enter a valid price', 'error')
      if (!this.form.image_url.trim())
        return this.show('Image URL is required', 'error')

      this.isLoading = true
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
          this.show('Product added to catalog!', 'success')
          this.form = { name: '', description: '', price: '', image_url: '' }
        } else {
          this.show(data.error || 'Something went wrong', 'error')
        }
      } catch {
        this.show('Cannot connect to server — is Flask running?', 'error')
      } finally {
        this.isLoading = false
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
.form-wrap {
  display: flex;
  gap: 32px;
  max-width: 780px;
}

.form-card {
  flex: 1;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  animation: slideIn 0.5s ease both;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: none; }
}

.form-header {
  padding: 28px 32px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 20px;
  background: linear-gradient(135deg, #111 0%, #0d0d0d 100%);
  position: relative;
  overflow: hidden;
}

.form-header::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--green), transparent);
}

.form-number {
  font-family: var(--font-display);
  font-size: 56px;
  color: rgba(0,255,135,0.1);
  line-height: 1;
  letter-spacing: 2px;
}

.form-subtitle {
  font-family: var(--font-cond);
  font-size: 11px;
  letter-spacing: 3px;
  color: var(--green);
  margin-bottom: 4px;
}

.form-title {
  font-family: var(--font-display);
  font-size: 28px;
  letter-spacing: 3px;
  color: var(--white);
}

.form-body {
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-family: var(--font-cond);
  font-size: 12px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-num {
  color: var(--green);
  font-size: 10px;
}

input, textarea {
  background: #0c0c0c;
  border: 1px solid var(--border);
  border-radius: 3px;
  color: var(--white);
  font-family: var(--font-body);
  font-size: 15px;
  padding: 12px 16px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  width: 100%;
}

input::placeholder, textarea::placeholder { color: #333; }

input:focus, textarea:focus {
  border-color: var(--green);
  box-shadow: 0 0 0 3px rgba(0,255,135,0.08);
}

input.filled, textarea.filled {
  border-color: rgba(0,255,135,0.3);
}

textarea { height: 110px; resize: vertical; }

/* Preview */
.preview {
  border: 1px solid var(--border);
  border-radius: 3px;
  overflow: hidden;
}

.preview-label {
  font-family: var(--font-cond);
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--green);
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
  background: #0c0c0c;
}

.preview img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

/* Button */
.btn-submit {
  width: 100%;
  padding: 16px;
  background: var(--green);
  color: #000;
  border: none;
  border-radius: 3px;
  font-family: var(--font-display);
  font-size: 20px;
  letter-spacing: 3px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.btn-submit::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
  opacity: 0;
  transition: opacity 0.2s;
}

.btn-submit:hover { background: var(--green2); transform: translateY(-1px); }
.btn-submit:hover::after { opacity: 1; }
.btn-submit:active { transform: scale(0.99); }
.btn-submit.loading { opacity: 0.7; cursor: wait; }

/* Message */
.msg {
  padding: 12px 16px;
  border-radius: 3px;
  font-family: var(--font-cond);
  font-size: 14px;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: none; }
}

.msg-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  flex-shrink: 0;
}

.msg.success {
  background: rgba(0,255,135,0.08);
  border: 1px solid rgba(0,255,135,0.25);
  color: var(--green);
}

.msg.success .msg-icon { background: rgba(0,255,135,0.2); }

.msg.error {
  background: rgba(255,60,60,0.08);
  border: 1px solid rgba(255,60,60,0.25);
  color: #ff6b6b;
}

.msg.error .msg-icon { background: rgba(255,60,60,0.2); }

/* Side decoration */
.side-deco {
  display: flex;
  align-items: center;
  justify-content: center;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

.deco-text {
  font-family: var(--font-cond);
  font-size: 11px;
  letter-spacing: 4px;
  color: rgba(0,255,135,0.15);
  text-transform: uppercase;
  transform: rotate(180deg);
}
</style>