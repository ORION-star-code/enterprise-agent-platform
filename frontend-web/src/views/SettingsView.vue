<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { healthCheck } from '@/api/agentApi'

const status = ref('checking...')

onMounted(async () => {
  try {
    const resp = await healthCheck()
    status.value = resp.status
  } catch {
    status.value = 'unreachable'
  }
})
</script>

<template>
  <div class="settings-layout">
    <div class="settings-header">
      <h1>Settings</h1>
      <nav class="nav">
        <router-link to="/">Back to Chat</router-link>
      </nav>
    </div>
    <div class="settings-content">
      <div class="setting-item">
        <label>Agent Gateway</label>
        <span class="value">http://localhost:8001</span>
        <span class="status" :class="status === 'ok' ? 'ok' : 'error'">
          {{ status }}
        </span>
      </div>
      <div class="setting-item">
        <label>Business MCP Server</label>
        <span class="value">http://localhost:8002</span>
      </div>
      <div class="setting-item">
        <label>Knowledge MCP Server</label>
        <span class="value">http://localhost:8003</span>
      </div>
      <div class="setting-item">
        <label>RAG Service</label>
        <span class="value">http://localhost:8000</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-layout {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
  background: #0f0f1a;
  color: #e0e0e0;
  min-height: 100vh;
}
.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.settings-header h1 {
  font-size: 20px;
  margin: 0;
}
.nav a {
  color: #6c63ff;
  text-decoration: none;
  font-size: 14px;
}
.settings-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.setting-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid #2a2a3e;
  border-radius: 8px;
  background: #1a1a2e;
}
.setting-item label {
  font-weight: 600;
  font-size: 14px;
  min-width: 180px;
}
.setting-item .value {
  font-size: 13px;
  color: #a0a0c0;
  font-family: monospace;
}
.status {
  margin-left: auto;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}
.status.ok {
  background: #1b3a2a;
  color: #4caf50;
}
.status.error {
  background: #3a1b1b;
  color: #ff6b6b;
}
</style>
