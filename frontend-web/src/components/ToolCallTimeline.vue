<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTrace } from '@/api/agentApi'
import type { TraceStep } from '@/types'

const props = defineProps<{
  traceId: string
}>()

const steps = ref<TraceStep[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const trace = await getTrace(props.traceId)
    steps.value = trace.steps
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load trace'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="timeline">
    <h3>Tool Trace</h3>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="steps.length === 0" class="empty">No trace steps.</div>
    <div v-else class="steps">
      <div v-for="(step, i) in steps" :key="i" class="step">
        <div class="step-header">
          <span class="step-node">{{ step.node }}</span>
          <span class="step-action">{{ step.action }}</span>
        </div>
        <pre v-if="Object.keys(step.details).length > 0" class="step-details">{{ JSON.stringify(step.details, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.timeline {
  padding: 16px;
}
h3 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #a0a0c0;
}
.loading, .error, .empty {
  font-size: 13px;
  color: #606080;
}
.error {
  color: #ff6b6b;
}
.steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.step {
  padding: 10px;
  border-radius: 6px;
  background: #1e1e36;
  border: 1px solid #2a2a4e;
}
.step-header {
  display: flex;
  gap: 8px;
  align-items: center;
}
.step-node {
  font-weight: 600;
  font-size: 13px;
  color: #6c63ff;
}
.step-action {
  font-size: 12px;
  color: #a0a0c0;
}
.step-details {
  margin: 6px 0 0;
  padding: 8px;
  border-radius: 4px;
  background: #14142a;
  font-size: 11px;
  color: #808090;
  overflow-x: auto;
}
</style>
