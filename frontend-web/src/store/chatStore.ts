import { defineStore } from 'pinia'
import { ref } from 'vue'
import { sendMessage } from '@/api/agentApi'
import { listSessions, deleteSession as apiDeleteSession } from '@/api/sessionApi'
import type { ChatMessage } from '@/types'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const sessions = ref<string[]>([])
  const currentSessionId = ref('default')
  const loading = ref(false)

  async function send(text: string) {
    loading.value = true
    messages.value.push({ role: 'user', content: text })
    try {
      const resp = await sendMessage({
        message: text,
        session_id: currentSessionId.value,
      })
      messages.value.push({
        role: 'assistant',
        content: resp.response,
        sources: resp.sources,
        intent: resp.intent,
      })
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Request failed'
      messages.value.push({
        role: 'assistant',
        content: `[Error] ${errorMsg}`,
      })
    } finally {
      loading.value = false
    }
  }

  async function loadSessions() {
    try {
      sessions.value = await listSessions()
    } catch {
      sessions.value = []
    }
  }

  function switchSession(id: string) {
    currentSessionId.value = id
    messages.value = []
  }

  function newSession() {
    const id = `session-${Date.now()}`
    currentSessionId.value = id
    messages.value = []
    if (!sessions.value.includes(id)) {
      sessions.value.push(id)
    }
  }

  async function removeSession(id: string) {
    try {
      await apiDeleteSession(id)
    } catch {
      // ignore
    }
    sessions.value = sessions.value.filter((s) => s !== id)
    if (currentSessionId.value === id) {
      newSession()
    }
  }

  return {
    messages,
    sessions,
    currentSessionId,
    loading,
    send,
    loadSessions,
    switchSession,
    newSession,
    removeSession,
  }
})
