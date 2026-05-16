<script setup lang="ts">
import { useRoute } from 'vue-router'
import ToolCallTimeline from '@/components/ToolCallTimeline.vue'

const route = useRoute()
const traceId = route.params.id as string
</script>

<template>
  <div class="trace-layout">
    <div class="trace-header">
      <h1>Tool Trace</h1>
      <nav class="nav">
        <router-link to="/">Back to Chat</router-link>
      </nav>
    </div>
    <ToolCallTimeline :trace-id="traceId" />
  </div>
</template>

<style scoped>
.trace-layout {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
  background: #0f0f1a;
  color: #e0e0e0;
  min-height: 100vh;
}
.trace-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.trace-header h1 {
  font-size: 20px;
  margin: 0;
}
.nav a {
  color: #6c63ff;
  text-decoration: none;
  font-size: 14px;
}
</style>
