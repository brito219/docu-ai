<script setup lang="ts">
import { computed, ref } from 'vue'

import { api } from './services/api'

type UploadState = 'idle' | 'loading' | 'success' | 'error'

interface UploadedDocument {
  id: string
  original_filename: string
  stored_filename: string
  content_type: string
  size_bytes: number
  storage_type: string
  status: string
  created_at: string
}

const file = ref<File | null>(null)
const uploadState = ref<UploadState>('idle')
const errorMessage = ref('')
const successDocument = ref<UploadedDocument | null>(null)

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const maxUploadSizeMb = 10

const selectedFileSummary = computed(() => {
  if (!file.value) {
    return ''
  }

  const sizeInMb = (file.value.size / (1024 * 1024)).toFixed(2)
  return `${file.value.name} (${sizeInMb} MB)`
})

async function submitUpload() {
  if (!file.value) {
    uploadState.value = 'error'
    errorMessage.value = 'Selecione um arquivo PDF antes de enviar.'
    return
  }

  uploadState.value = 'loading'
  errorMessage.value = ''
  successDocument.value = null

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const response = await api.post<UploadedDocument>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    successDocument.value = response.data
    uploadState.value = 'success'
  } catch (error: unknown) {
    uploadState.value = 'error'
    errorMessage.value = 'Falha ao enviar o arquivo.'

    if (typeof error === 'object' && error && 'response' in error) {
      const response = error.response as { data?: { detail?: string } }
      errorMessage.value = response.data?.detail || errorMessage.value
    }
  }
}

function handleFileSelection(files: File | File[] | null) {
  if (Array.isArray(files)) {
    file.value = files[0] ?? null
    return
  }

  file.value = files
}
</script>

<template>
  <v-app>
    <v-main>
      <section class="page-shell">
        <div class="upload-card">
          <div class="headline-block">
            <p class="eyebrow">DocuAI Viewer</p>
            <h1>Upload e persistencia local de PDFs</h1>
            <p class="lead">
              Envie um PDF de ate {{ maxUploadSizeMb }} MB. O backend valida o
              arquivo, salva localmente e registra os metadados no PostgreSQL.
            </p>
          </div>

          <v-alert
            v-if="uploadState === 'error'"
            type="error"
            variant="tonal"
            class="message"
          >
            {{ errorMessage }}
          </v-alert>

          <v-alert
            v-if="uploadState === 'success' && successDocument"
            type="success"
            variant="tonal"
            class="message"
          >
            Upload concluido com sucesso para {{ successDocument.original_filename }}.
          </v-alert>

          <v-file-input
            label="Selecionar PDF"
            accept=".pdf,application/pdf"
            prepend-icon="mdi-file-pdf-box"
            variant="outlined"
            show-size
            :disabled="uploadState === 'loading'"
            @update:model-value="handleFileSelection"
          />

          <div class="meta-row">
            <span class="hint">API: {{ apiUrl }}/documents/upload</span>
            <span v-if="selectedFileSummary" class="hint">{{ selectedFileSummary }}</span>
          </div>

          <v-btn
            color="primary"
            size="large"
            block
            :loading="uploadState === 'loading'"
            :disabled="uploadState === 'loading'"
            @click="submitUpload"
          >
            Enviar PDF
          </v-btn>

          <div v-if="successDocument" class="result-panel">
            <p class="result-title">Metadados registrados</p>
            <dl class="result-grid">
              <div>
                <dt>ID</dt>
                <dd>{{ successDocument.id }}</dd>
              </div>
              <div>
                <dt>Nome original</dt>
                <dd>{{ successDocument.original_filename }}</dd>
              </div>
              <div>
                <dt>Tamanho</dt>
                <dd>{{ successDocument.size_bytes }} bytes</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>{{ successDocument.status }}</dd>
              </div>
              <div>
                <dt>Storage</dt>
                <dd>{{ successDocument.storage_type }}</dd>
              </div>
              <div>
                <dt>Criado em</dt>
                <dd>{{ new Date(successDocument.created_at).toLocaleString('pt-BR') }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </section>
    </v-main>
  </v-app>
</template>

<style scoped>
.page-shell {
  display: grid;
  min-height: 100vh;
  padding: 32px;
  place-items: center;
}

.upload-card {
  width: min(760px, 100%);
  padding: 36px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 28px 90px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(16px);
}

.headline-block {
  margin-bottom: 20px;
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
  font-size: clamp(2rem, 5vw, 3.6rem);
  line-height: 1;
}

.lead {
  max-width: 60ch;
  margin: 16px 0 0;
  color: #334155;
  font-size: 1rem;
  line-height: 1.7;
}

.message {
  margin-bottom: 16px;
}

.meta-row {
  display: flex;
  gap: 12px;
  justify-content: space-between;
  margin: 8px 0 20px;
  color: #475569;
  font-size: 0.92rem;
  flex-wrap: wrap;
}

.hint {
  word-break: break-word;
}

.result-panel {
  margin-top: 24px;
  padding: 20px;
  border-radius: 22px;
  background: linear-gradient(180deg, #f8fafc 0%, #e0f2fe 100%);
  border: 1px solid rgba(14, 165, 233, 0.14);
}

.result-title {
  margin: 0 0 16px;
  color: #0f172a;
  font-size: 1rem;
  font-weight: 700;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin: 0;
}

dt {
  margin-bottom: 6px;
  color: #475569;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

dd {
  margin: 0;
  color: #0f172a;
  font-size: 0.95rem;
  word-break: break-word;
}

@media (max-width: 640px) {
  .page-shell {
    padding: 16px;
  }

  .upload-card {
    padding: 24px;
  }
}
</style>
