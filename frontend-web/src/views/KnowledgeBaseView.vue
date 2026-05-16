<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCollectionStatus } from '@/api/documentApi'
import DocumentUploader from '@/components/DocumentUploader.vue'

const collection = ref('')
const chunkCount = ref(0)
const loading = ref(true)

onMounted(async () => {
  try {
    const status = await getCollectionStatus()
    collection.value = status.collection
    chunkCount.value = status.chunk_count
  } catch {
    collection.value = 'unavailable'
  } finally {
    loading.value = false
  }
})

function handleUploaded() {
  getCollectionStatus().then((status) => {
    collection.value = status.collection
    chunkCount.value = status.chunk_count
  })
}
</script>

<template>
  <div class="kb-layout">
    <div class="kb-header">
      <h1>Knowledge Base</h1>
      <nav class="nav">
        <router-link to="/">Back to Chat</router-link>
      </nav>
    </div>
    <div class="kb-content">
      <div class="status-card">
        <h3>Collection Status</h3>
        <div v-if="loading">Loading...</div>
        <div v-else>
          <p>Collection: <strong>{{ collection }}</strong></p>
          <p>Chunks: <strong>{{ chunkCount }}</strong></p>
        </div>
      </div>
      <DocumentUploader @uploaded="handleUploaded" />
    </div>
  </div>
</template>

<style scoped>
.kb-layout {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
  background: #0f0f1a;
  color: #e0e0e0;
  min-height: 100vh;
}
.kb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.kb-header h1 {
  font-size: 20px;
  margin: 0;
}
.nav a {
  color: #6c63ff;
  text-decoration: none;
  font-size: 14px;
}
.kb-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.status-card {
  padding: 16px;
  border: 1px solid #2a2a3e;
  border-radius: 8px;
  background: #1a1a2e;
}
.status-card h3 {
  margin: 0 0 10px;
  font-size: 14px;
  color: #a0a0c0;
}
.status-card p {
  margin: 4px 0;
  font-size: 14px;
}
</style>
