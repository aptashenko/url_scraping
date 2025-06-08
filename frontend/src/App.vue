<template>
  <div class="container">
    <h1>🔍 Web Scraper</h1>

    <form @submit.prevent="runScraping">
      <input v-model="url" type="url" placeholder="Введите URL" required />
      <input v-model="depth" type="number" min="1" placeholder="Глубина" />
      <button :disabled="loading" type="submit">
          {{loading ? 'Завантаження...' : 'Скрейпити'}}
      </button>
    </form>

    <div v-if="links.length > 0" class="results">
      <h3>Выберите страницы для скрейпинга:</h3>
      <div class="labels-list">
        <label v-for="link in links" :key="link">
          <input type="checkbox" :value="link" v-model="selectedLinks" />
          {{ link }}
        </label>
      </div>
      <button :disabled="loading" @click="submitLinks">
        {{loading ? 'Завантаження...' : 'Скрейпити вибрані'}}
      </button>
    </div>

    <p v-if="done" class="success">✅ Готово! Проверь файл <code>knowledge_base.json</code></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const url = ref('')
const depth = ref(1)
const links = ref([])
const selectedLinks = ref([])
const done = ref(false)
const loading = ref(false);

async function runScraping() {
  done.value = false
  links.value = []
  selectedLinks.value = []

  loading.value = true;
  try {
    await fetch(`http://localhost:8000/start?url=${encodeURIComponent(url.value)}&depth=${depth.value}`)
    const res = await fetch("http://localhost:8000/links")
    links.value = await res.json()
  } catch (e) {
    alert("Ошибка при скрейпинге")
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitLinks() {
  loading.value = true;
  try {
    await fetch("http://localhost:8000/continue", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ links: selectedLinks.value })
    })
    done.value = true
  } catch (e) {
    alert("Ошибка при отправке ссылок")
    console.error(e)
  } finally {
    loading.value = false;
  }
}
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
  padding: 2rem;
  font-family: sans-serif;
}
input[type="url"], input[type="number"] {
  width: 100%;
  margin-bottom: 1rem;
  padding: 8px;
  font-size: 16px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  margin-top: 1rem;
  cursor: pointer;
}
.results {
  margin-top: 2rem;
}
.success {
  margin-top: 1rem;
  color: green;
  font-weight: bold;
}
.labels-list {
  display: flex;
  flex-direction: column;
}
</style>