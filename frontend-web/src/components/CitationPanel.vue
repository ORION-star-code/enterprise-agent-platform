<script setup lang="ts">
import type { SourceItem } from '@/types'

defineProps<{
  sources: SourceItem[]
}>()
</script>

<template>
  <div class="citation-panel">
    <h3>Sources</h3>
    <div v-if="sources.length === 0" class="empty">No sources for this message.</div>
    <div v-for="(src, i) in sources" :key="i" class="source-item">
      <div class="source-name">{{ src.doc_name }}</div>
      <div class="source-section">{{ src.section }}</div>
      <div class="source-score">Score: {{ src.score.toFixed(3) }}</div>
    </div>
  </div>
</template>

<style scoped>
.citation-panel {
  padding: 16px;
}
h3 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #a0a0c0;
}
.empty {
  color: #606080;
  font-size: 13px;
}
.source-item {
  padding: 10px;
  margin-bottom: 8px;
  border-radius: 6px;
  background: #1e1e36;
  border: 1px solid #2a2a4e;
}
.source-name {
  font-weight: 600;
  font-size: 13px;
  color: #d0d0e0;
}
.source-section {
  font-size: 12px;
  color: #808090;
  margin-top: 2px;
}
.source-score {
  font-size: 11px;
  color: #6c63ff;
  margin-top: 4px;
}
</style>
