<script setup lang="ts">
import { ref } from 'vue'
import { uploadDocument } from '@/api/documentApi'

const emit = defineEmits<{
  uploaded: [docId: string]
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)
const result = ref('')
const error = ref('')

async function handleUpload() {
  const input = fileInput.value
  if (!input?.files?.length) return

  const file = input.files[0]
  uploading.value = true
  result.value = ''
  error.value = ''

  try {
    const resp = await uploadDocument(file)
    result.value = `Uploaded "${resp.filename}" — ${resp.chunk_count} chunks`
    emit('uploaded', resp.doc_id)
    input.value = ''
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Upload failed'
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="uploader">
    <h3>Upload Document</h3>
    <div class="controls">
      <input ref="fileInput" type="file" accept=".md,.txt,.pdf,.docx" />
      <button :disabled="uploading" @click="handleUpload">
        {{ uploading ? 'Uploading...' : 'Upload' }}
      </button>
    </div>
    <div v-if="result" class="result">{{ result }}</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<style scoped>
.uploader {
  padding: 16px;
  border: 1px dashed #3a3a5e;
  border-radius: 8px;
  background: #1a1a2e;
}
h3 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #a0a0c0;
}
.controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
input[type="file"] {
  font-size: 13px;
  color: #a0a0c0;
}
button {
  padding: 6px 16px;
  border: none;
  border-radius: 4px;
  background: #6c63ff;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.result {
  margin-top: 8px;
  font-size: 13px;
  color: #4caf50;
}
.error {
  margin-top: 8px;
  font-size: 13px;
  color: #ff6b6b;
}
</style>
