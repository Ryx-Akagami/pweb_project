<template>
  <div class="add-root">
    <div class="form-card">

      <!-- Card header -->
      <div class="form-header">
        <div class="header-badge">New Product</div>
        <p class="header-sub">Fill in the details below to add a shoe to the catalog.</p>
      </div>

      <!-- Form body -->
      <div class="form-body">
        <div class="row-2">
          <!-- Shoe Name -->
          <div class="field">
            <label>Shoe Name <span class="req">*</span></label>
            <input
              v-model="form.name"
              type="text"
              placeholder="e.g. Nike Air Max 97"
              :class="{ filled: form.name, error: errors.name }"
            />
            <span class="field-err" v-if="errors.name">{{ errors.name }}</span>
          </div>

          <!-- Price -->
          <div class="field">
            <label>Price <span class="req">*</span><span class="label-note">DZD</span></label>
            <div class="input-icon-wrap">
              <input
                v-model="form.price"
                type="number"
                placeholder="e.g. 12 000"
                :class="{ filled: form.price, error: errors.price }"
              />
              <span class="input-suffix">DZD</span>
            </div>
            <span class="field-err" v-if="errors.price">{{ errors.price }}</span>
          </div>
        </div>

        <!-- Description -->
        <div class="field">
          <label>Description <span class="req">*</span></label>
          <textarea
            v-model="form.description"
            placeholder="Describe the shoe — materials, fit, use case, sizing…"
            :class="{ filled: form.description, error: errors.description }"
          ></textarea>
          <span class="field-err" v-if="errors.description">{{ errors.description }}</span>
        </div>

        <!-- Image URL -->
        <div class="field">
          <label>Image URL <span class="req">*</span></label>
          <input
            v-model="form.image_url"
            type="text"
            placeholder="https://…"
            :class="{ filled: form.image_url, error: errors.image_url }"
          />
          <span class="field-err" v-if="errors.image_url">{{ errors.image_url }}</span>
        </div>

        <!-- Image preview -->
        <transition name="preview-fade">
          <div class="preview-wrap" v-if="form.image_url">
            <div class="preview-label">
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                <rect x="1" y="1" width="11" height="11" rx="2" stroke="currentColor" stroke-width="1.4"/>
                <circle cx="4.5" cy="4.5" r="1.5" stroke="currentColor" stroke-width="1.2"/>
                <path d="M1 9l3-3 2.5 2.5L9 6l3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Preview
            </div>
            <img
              :src="form.image_url"
              alt="preview"
              onerror="this.parentElement.style.display='none'"
            />
          </div>
        </transition>

        <!-- Submit -->
        <button
          class="btn-submit"
          @click="submit"
          :disabled="isLoading"
          :class="{ loading: isLoading }"
        >
          <svg v-if="!isLoading" width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M8 1v14M1 8h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          </svg>
          <span>{{ isLoading ? 'Adding to catalog…' : 'Add to Catalog' }}</span>
        </button>

        <!-- Feedback message -->
        <transition name="msg-fade">
          <div v-if="message" :class="['msg', msgType]">
            <span class="msg-icon">
              <svg v-if="msgType === 'success'" width="13" height="13" viewBox="0 0 13 13" fill="none">
                <path d="M2 7l3.5 3.5L11 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else width="13" height="13" viewBox="0 0 13 13" fill="none">
                <path d="M2 2l9 9M11 2L2 11" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              </svg>
            </span>
            {{ message }}
          </div>
        </transition>
      </div>
    </div>

    <!-- Sidebar tips -->
    <div class="tips-panel">
      <h3 class="tips-title">Quick Tips</h3>
      <ul class="tips-list">
        <li>
          <span class="tip-num">01</span>
          <div>
            <strong>Name clearly</strong>
            <p>Include brand and model (e.g. "Adidas Ultraboost 22")</p>
          </div>
        </li>
        <li>
          <span class="tip-num">02</span>
          <div>
            <strong>Describe thoroughly</strong>
            <p>Mention materials, fit, and intended use case</p>
          </div>
        </li>
        <li>
          <span class="tip-num">03</span>
          <div>
            <strong>Use a clean image</strong>
            <p>Direct URL to a high-res product photo works best</p>
          </div>
        </li>
        <li>
          <span class="tip-num">04</span>
          <div>
            <strong>Set the right price</strong>
            <p>Price in Algerian Dinar (DZD), no commas needed</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      form: { name: '', description: '', price: '', image_url: '' },
      errors: {},
      message: '',
      msgType: '',
      isLoading: false
    }
  },
  methods: {
    validate() {
      const e = {}
      if (!this.form.name.trim()) e.name = 'Shoe name is required'
      if (!this.form.description.trim()) e.description = 'Description is required'
      if (!this.form.price || Number(this.form.price) <= 0) e.price = 'Enter a valid price'
      if (!this.form.image_url.trim()) e.image_url = 'Image URL is required'
      this.errors = e
      return Object.keys(e).length === 0
    },
    async submit() {
      if (!this.validate()) return
      this.isLoading = true
      try {
        const res = await fetch(`${API}/products`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: this.form.name.trim(),
            description: this.form.description.trim(),
            price: parseFloat(this.form.price),
            image_url: this.form.image_url.trim()
          })
        })
        const data = await res.json()
        if (res.ok) {
          this.showMsg('Product added to catalog!', 'success')
          this.form = { name: '', description: '', price: '', image_url: '' }
          this.errors = {}
        } else {
          this.showMsg(data.error || 'Something went wrong', 'error')
        }
      } catch {
        this.showMsg('Cannot connect to server — is Flask running?', 'error')
      } finally {
        this.isLoading = false
      }
    },
    showMsg(msg, type) {
      this.message = msg
      this.msgType = type
      setTimeout(() => { this.message = '' }, 4000)
    }
  }
}
</script>

<style scoped>
.add-root {
  display: flex;
  gap: 28px;
  align-items: flex-start;
  max-width: 920px;
  animation: fadeUp 0.45s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: none; }
}

/* ── Form card ── */
.form-card {
  flex: 1;
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-m);
}

.form-header {
  padding: 28px 32px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--green-pale);
  position: relative;
  overflow: hidden;
}

.form-header::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  right: 0; height: 3px;
  background: linear-gradient(90deg, var(--green) 0%, var(--green-mid) 60%, transparent 100%);
}

.header-badge {
  display: inline-block;
  background: var(--green);
  color: #fff;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 10px;
}

.header-sub {
  font-size: 14px;
  color: var(--muted);
  line-height: 1.5;
}

.form-body {
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* ── Fields ── */
.field {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

label {
  font-family: var(--font-body);
  font-size: 13.5px;
  font-weight: 600;
  color: var(--ink);
  display: flex;
  align-items: center;
  gap: 6px;
}

.req { color: var(--green); font-size: 15px; line-height: 1; }

.label-note {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 400;
  color: var(--muted);
  letter-spacing: 0.5px;
}

input, textarea {
  background: var(--off-white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 14.5px;
  padding: 11px 14px;
  outline: none;
  transition: border-color 0.18s, box-shadow 0.18s, background 0.18s;
  width: 100%;
}

input::placeholder, textarea::placeholder { color: #B0ADA6; }

input:focus, textarea:focus {
  border-color: var(--green);
  background: var(--white);
  box-shadow: 0 0 0 3px rgba(26,107,60,0.1);
}

input.filled, textarea.filled {
  border-color: rgba(26,107,60,0.35);
  background: var(--white);
}

input.error, textarea.error { border-color: #D9534F !important; }

textarea { min-height: 110px; resize: vertical; }

.field-err {
  font-size: 12px;
  color: #D9534F;
  font-weight: 500;
}

/* Price suffix */
.input-icon-wrap { position: relative; }

.input-icon-wrap input { padding-right: 48px; }

.input-suffix {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--muted);
  pointer-events: none;
  letter-spacing: 0.5px;
}

/* ── Preview ── */
.preview-wrap {
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--off-white);
}

.preview-label {
  padding: 9px 14px;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 1px;
  color: var(--green);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 7px;
  text-transform: uppercase;
  background: var(--green-pale);
}

.preview-wrap img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}

.preview-fade-enter-active, .preview-fade-leave-active { transition: all 0.25s ease; }
.preview-fade-enter-from, .preview-fade-leave-to { opacity: 0; transform: translateY(-8px); }

/* ── Submit button ── */
.btn-submit {
  width: 100%;
  padding: 14px 24px;
  background: var(--green);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 15.5px;
  cursor: pointer;
  transition: all 0.18s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(26,107,60,0.25);
}

.btn-submit:hover:not(:disabled) {
  background: var(--green-mid);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(26,107,60,0.3);
}

.btn-submit:active:not(:disabled) { transform: scale(0.99); }
.btn-submit:disabled { opacity: 0.65; cursor: not-allowed; }

/* ── Message ── */
.msg {
  padding: 12px 16px;
  border-radius: var(--radius);
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
}

.msg.success {
  background: var(--green-light);
  border: 1.5px solid rgba(26,107,60,0.25);
  color: var(--green);
}

.msg.error {
  background: #FFF0F0;
  border: 1.5px solid rgba(217,83,79,0.25);
  color: #C0392B;
}

.msg-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.msg.success .msg-icon { background: rgba(26,107,60,0.15); }
.msg.error .msg-icon { background: rgba(217,83,79,0.15); }

.msg-fade-enter-active, .msg-fade-leave-active { transition: all 0.22s ease; }
.msg-fade-enter-from, .msg-fade-leave-to { opacity: 0; transform: translateY(-6px); }

/* ── Tips sidebar ── */
.tips-panel {
  width: 240px;
  flex-shrink: 0;
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-s);
  position: sticky;
  top: 88px;
}

.tips-title {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}

.tips-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.tips-list li {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.tip-num {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--green);
  background: var(--green-light);
  padding: 3px 7px;
  border-radius: 4px;
  flex-shrink: 0;
  margin-top: 2px;
  letter-spacing: 0.5px;
}

.tips-list li strong {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 3px;
}

.tips-list li p {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.55;
}
</style>