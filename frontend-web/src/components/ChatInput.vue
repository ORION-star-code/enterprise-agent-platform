<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  send: [message: string]
}>()

defineProps<{
  disabled?: boolean
}>()

const text = ref('')

function handleSend() {
  const trimmed = text.value.trim()
  if (!trimmed) return
  emit('send', trimmed)
  text.value = ''
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="chat-input">
    <textarea
      v-model="text"
      :disabled="disabled"
      placeholder="Type a message... (Shift+Enter for new line)"
      rows="2"
      @keydown="handleKeydown"
    />
    <button :disabled="disabled || !text.trim()" @click="handleSend">
      Send
    </button>
  </div>
</template>

<style scoped>
.chat-input {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid #2a2a3e;
  background: #1a1a2e;
}
textarea {
  flex: 1;
  resize: none;
  padding: 10px;
  border: 1px solid #3a3a5e;
  border-radius: 6px;
  background: #16162a;
  color: #e0e0e0;
  font-size: 14px;
  font-family: inherit;
}
textarea:focus {
  outline: none;
  border-color: #6c63ff;
}
button {
  padding: 0 20px;
  border: none;
  border-radius: 6px;
  background: #6c63ff;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
button:hover:not(:disabled) {
  background: #5a52e0;
}
</style>
