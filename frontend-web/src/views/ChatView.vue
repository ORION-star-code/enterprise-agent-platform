<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useChatStore } from '@/store/chatStore'
import ChatInput from '@/components/ChatInput.vue'
import ChatMessage from '@/components/ChatMessage.vue'
import CitationPanel from '@/components/CitationPanel.vue'
import type { SourceItem } from '@/types'

const store = useChatStore()
const messagesEl = ref<HTMLElement | null>(null)
const showSidebar = ref(true)
const selectedSources = ref<SourceItem[]>([])

onMounted(() => {
  store.loadSessions()
})

watch(
  () => store.messages.length,
  async () => {
    await nextTick()
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight
    }
  },
)

function handleSend(text: string) {
  store.send(text)
}

function handleSelectSources(sources: SourceItem[]) {
  selectedSources.value = sources
}
</script>

<template>
  <div class="chat-layout">
    <!-- Session sidebar -->
    <aside class="session-sidebar">
      <div class="sidebar-header">
        <span>Sessions</span>
        <button class="new-btn" @click="store.newSession()">+</button>
      </div>
      <div class="session-list">
        <div
          v-for="sid in store.sessions"
          :key="sid"
          class="session-item"
          :class="{ active: sid === store.currentSessionId }"
          @click="store.switchSession(sid)"
        >
          <span class="session-name">{{ sid }}</span>
          <button class="delete-btn" @click.stop="store.removeSession(sid)">x</button>
        </div>
        <div v-if="store.sessions.length === 0" class="empty-hint">No sessions yet</div>
      </div>
      <nav class="nav-links">
        <router-link to="/">Chat</router-link>
        <router-link to="/knowledge">Knowledge</router-link>
        <router-link to="/settings">Settings</router-link>
      </nav>
    </aside>

    <!-- Main chat area -->
    <main class="chat-main">
      <div ref="messagesEl" class="messages">
        <ChatMessage
          v-for="(msg, i) in store.messages"
          :key="i"
          :message="msg"
          @click="msg.sources && handleSelectSources(msg.sources)"
        />
        <div v-if="store.loading" class="typing">Thinking...</div>
      </div>
      <ChatInput :disabled="store.loading" @send="handleSend" />
    </main>

    <!-- Citation sidebar -->
    <aside v-if="showSidebar" class="citation-sidebar">
      <div class="sidebar-header">
        <span>Details</span>
        <button class="close-btn" @click="showSidebar = false">x</button>
      </div>
      <CitationPanel :sources="selectedSources" />
    </aside>
    <button v-else class="show-sidebar-btn" @click="showSidebar = true">Show Details</button>
  </div>
</template>

<style scoped>
.chat-layout {
  display: grid;
  grid-template-columns: 240px 1fr 300px;
  height: 100vh;
  background: #0f0f1a;
  color: #e0e0e0;
}

/* Session sidebar */
.session-sidebar {
  border-right: 1px solid #2a2a3e;
  display: flex;
  flex-direction: column;
  background: #12122a;
}
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #2a2a3e;
  font-size: 13px;
  font-weight: 600;
  color: #a0a0c0;
}
.new-btn {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 4px;
  background: #6c63ff;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.session-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}
.session-item:hover {
  background: #1e1e36;
}
.session-item.active {
  background: #2a2a4e;
}
.session-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.delete-btn {
  border: none;
  background: none;
  color: #606080;
  cursor: pointer;
  font-size: 12px;
  padding: 2px 4px;
}
.delete-btn:hover {
  color: #ff6b6b;
}
.empty-hint {
  padding: 16px;
  text-align: center;
  color: #404060;
  font-size: 13px;
}
.nav-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px 8px;
  border-top: 1px solid #2a2a3e;
}
.nav-links a {
  padding: 8px 12px;
  border-radius: 6px;
  color: #a0a0c0;
  text-decoration: none;
  font-size: 13px;
}
.nav-links a:hover {
  background: #1e1e36;
}
.nav-links a.router-link-active {
  background: #2a2a4e;
  color: #fff;
}

/* Chat main */
.chat-main {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.typing {
  padding: 8px 0;
  font-size: 13px;
  color: #606080;
  font-style: italic;
}

/* Citation sidebar */
.citation-sidebar {
  border-left: 1px solid #2a2a3e;
  background: #12122a;
  display: flex;
  flex-direction: column;
}
.close-btn {
  border: none;
  background: none;
  color: #606080;
  cursor: pointer;
  font-size: 14px;
}
.show-sidebar-btn {
  position: fixed;
  right: 12px;
  top: 12px;
  padding: 6px 12px;
  border: 1px solid #3a3a5e;
  border-radius: 4px;
  background: #1a1a2e;
  color: #a0a0c0;
  font-size: 12px;
  cursor: pointer;
}
</style>
