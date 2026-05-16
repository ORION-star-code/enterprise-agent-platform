<script setup lang="ts">
import type { ChatMessage } from '@/types'

defineProps<{
  message: ChatMessage
}>()
</script>

<template>
  <div class="chat-message" :class="message.role">
    <div class="avatar">{{ message.role === 'user' ? 'U' : 'A' }}</div>
    <div class="bubble">
      <div v-if="message.intent" class="intent-tag">{{ message.intent }}</div>
      <div class="content">{{ message.content }}</div>
      <div v-if="message.sources && message.sources.length > 0" class="sources-hint">
        {{ message.sources.length }} source(s) referenced
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-message {
  display: flex;
  gap: 10px;
  padding: 8px 0;
}
.chat-message.user {
  flex-direction: row-reverse;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}
.user .avatar {
  background: #6c63ff;
  color: #fff;
}
.assistant .avatar {
  background: #2a2a4e;
  color: #a0a0c0;
}
.bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 10px;
  line-height: 1.5;
  font-size: 14px;
}
.user .bubble {
  background: #6c63ff;
  color: #fff;
  border-bottom-right-radius: 2px;
}
.assistant .bubble {
  background: #2a2a3e;
  color: #e0e0e0;
  border-bottom-left-radius: 2px;
}
.intent-tag {
  display: inline-block;
  padding: 2px 8px;
  margin-bottom: 6px;
  border-radius: 4px;
  background: #3a3a5e;
  color: #a0a0c0;
  font-size: 11px;
}
.sources-hint {
  margin-top: 6px;
  font-size: 12px;
  color: #808090;
}
</style>
