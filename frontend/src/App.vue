<script setup lang="ts">
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
</script>

<template>
  <v-app>
    <v-main>
      <section class="hero">
        <div class="panel">
          <p class="eyebrow">DocuAI Viewer</p>
          <h1>Day 1 setup concluido</h1>
          <p class="lead">
            Frontend Vue 3 com Vuetify, backend FastAPI e PostgreSQL via Docker
            Compose prontos para evoluir para upload e visualizacao de PDFs.
          </p>

          <div class="status-grid">
            <div class="status-card">
              <span class="label">Frontend</span>
              <strong>Online em :5173</strong>
            </div>
            <div class="status-card">
              <span class="label">Backend</span>
              <strong>{{ apiUrl }}/health</strong>
            </div>
            <div class="status-card">
              <span class="label">Banco</span>
              <strong>PostgreSQL em :5432</strong>
            </div>
          </div>
        </div>
      </section>
    </v-main>
  </v-app>
</template>

<style scoped>
.hero {
  display: grid;
  min-height: 100vh;
  padding: 32px;
  place-items: center;
}

.panel {
  width: min(880px, 100%);
  padding: 40px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 24px 80px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(18px);
}

.eyebrow {
  margin: 0 0 8px;
  color: #0369a1;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  color: #0f172a;
  font-size: clamp(2.4rem, 5vw, 4.5rem);
  line-height: 0.95;
}

.lead {
  max-width: 58ch;
  margin: 20px 0 0;
  color: #334155;
  font-size: 1.05rem;
  line-height: 1.7;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-top: 28px;
}

.status-card {
  padding: 18px;
  border-radius: 20px;
  background: linear-gradient(180deg, #ffffff 0%, #e0f2fe 100%);
  border: 1px solid rgba(14, 165, 233, 0.14);
}

.label {
  display: block;
  margin-bottom: 8px;
  color: #475569;
  font-size: 0.85rem;
}

strong {
  color: #0f172a;
  font-size: 1rem;
}

@media (max-width: 640px) {
  .hero {
    padding: 16px;
  }

  .panel {
    padding: 24px;
  }
}
</style>
