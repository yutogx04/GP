<template>
  <div class="min-h-screen py-8 bg-slate-50 dark:bg-slate-900">
    <div class="container mx-auto px-4 max-w-5xl">
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-8">Messages</h1>

      <div v-if="error" class="card p-12 text-center mb-6 flex flex-col items-center">
        <ExclamationTriangleIcon class="w-16 h-16 text-slate-300 dark:text-slate-600 mb-4" />
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Failed to load messages</h3>
        <p class="text-slate-600 dark:text-slate-400 mb-4">{{ error }}</p>
        <button @click="loadConversations" class="btn btn-primary">Retry</button>
      </div>

      <div v-else class="grid lg:grid-cols-3 gap-6">
        <!-- Conversations List -->
        <div class="lg:col-span-1">
          <div class="card p-4">
            <div class="mb-4">
              <input v-model="search" type="search" placeholder="Search messages..." class="input-field">
            </div>
            
            <div v-if="loadingConversations" class="py-8 text-center text-slate-500">Loading...</div>
            
            <div v-else-if="conversations.length === 0" class="py-8 text-center text-slate-500">
              No conversations yet
            </div>
            
            <div v-else class="space-y-2">
              <button
                v-for="conv in filteredConversations"
                :key="conv.id"
                @click="selectConversation(conv)"
                :class="selectedConversation?.id === conv.id ? 'bg-sky-50 dark:bg-sky-900/20 border-sky-500' : 'hover:bg-slate-50 dark:hover:bg-slate-800'"
                class="w-full p-3 rounded-lg border border-transparent text-left transition-all"
              >
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-slate-200 dark:bg-slate-700 rounded-full flex items-center justify-center font-medium text-slate-600 dark:text-slate-300">
                    {{ getParticipantInitial(conv) }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="font-medium text-slate-900 dark:text-white truncate">
                      {{ getParticipantName(conv) }}
                    </div>
                    <div class="text-sm text-slate-500 truncate">{{ conv.last_message?.content || 'No messages yet' }}</div>
                  </div>
                  <div v-if="conv.unread_count" class="w-5 h-5 bg-sky-500 rounded-full text-white text-xs flex items-center justify-center">
                    {{ conv.unread_count }}
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Messages Panel -->
        <div class="lg:col-span-2">
          <div v-if="!selectedConversation" class="card p-12 text-center flex flex-col items-center justify-center h-full">
            <ChatBubbleLeftRightIcon class="w-24 h-24 text-slate-200 dark:text-slate-700 mb-6" />
            <h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Select a conversation</h3>
            <p class="text-slate-600 dark:text-slate-400">Choose a conversation from the list to start messaging</p>
          </div>

          <div v-else class="card flex flex-col h-[600px]">
            <!-- Header -->
            <div class="p-4 border-b border-slate-100 dark:border-slate-700 flex items-center gap-3">
              <div class="w-10 h-10 bg-slate-200 dark:bg-slate-700 rounded-full flex items-center justify-center font-medium">
                {{ getParticipantInitial(selectedConversation) }}
              </div>
              <div>
                <div class="font-medium text-slate-900 dark:text-white">
                  {{ getParticipantName(selectedConversation) }}
                </div>
                <div class="text-sm text-slate-500">{{ selectedConversation.subject || 'Conversation' }}</div>
              </div>
            </div>

            <!-- Messages -->
            <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
              <div v-if="loadingMessages" class="text-center py-8 text-slate-500">Loading messages...</div>
              <div v-else-if="messages.length === 0" class="text-center py-8 text-slate-500">No messages yet. Send one!</div>
              <div
                v-else
                v-for="msg in messages"
                :key="msg.id"
                :class="msg.sender === currentUserId ? 'flex-row-reverse' : ''"
                class="flex gap-3"
              >
                <div
                  :class="msg.sender === currentUserId ? 'bg-sky-500 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white'"
                  class="max-w-[70%] p-3 rounded-2xl"
                >
                  <p>{{ msg.content }}</p>
                  <div :class="msg.sender === currentUserId ? 'text-sky-200' : 'text-slate-500'" class="text-xs mt-1">
                    {{ formatTime(msg.created_at) }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Input -->
            <form @submit.prevent="sendMessage" class="p-4 border-t border-slate-100 dark:border-slate-700 flex gap-3">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Type a message..."
                class="input-field flex-1"
                :disabled="sending"
              >
              <button type="submit" class="btn btn-primary" :disabled="!newMessage.trim() || sending">
                {{ sending ? '...' : 'Send' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import { ExclamationTriangleIcon, ChatBubbleLeftRightIcon } from '@heroicons/vue/24/outline'

const auth = useAuthStore()
const currentUserId = computed(() => auth.user?.id)

const loadingConversations = ref(true)
const loadingMessages = ref(false)
const error = ref(null)
const conversations = ref([])
const selectedConversation = ref(null)
const messages = ref([])
const newMessage = ref('')
const sending = ref(false)
const search = ref('')
const messagesContainer = ref(null)

const filteredConversations = computed(() => {
  if (!Array.isArray(conversations.value)) return []
  if (!search.value) return conversations.value
  const s = search.value.toLowerCase()
  return conversations.value.filter(c => {
    const name = getParticipantName(c).toLowerCase()
    return name.includes(s)
  })
})

const getParticipantName = (conv) => {
  // Try to get participant info from participants_data
  if (conv.participants_data && conv.participants_data.length > 0) {
    const other = conv.participants_data.find(p => p.id !== currentUserId.value)
    return other ? other.name : conv.participants_data[0]?.name || 'Unknown'
  }
  // Fallback to subject
  return conv.subject || 'Conversation'
}

const getParticipantInitial = (conv) => {
  const name = getParticipantName(conv)
  return name ? name[0]?.toUpperCase() : '?'
}

const loadConversations = async () => {
  loadingConversations.value = true
  error.value = null
  try {
    const response = await api.get('/users/conversations/')
    conversations.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
  } catch (err) {
    console.error('Failed to load conversations:', err)
    error.value = err.response?.data?.detail || 'Could not load conversations. Please try again.'
    conversations.value = []
  } finally {
    loadingConversations.value = false
  }
}

onMounted(loadConversations)

const selectConversation = async (conv) => {
  selectedConversation.value = conv
  loadingMessages.value = true
  try {
    const response = await api.get(`/users/conversations/${conv.id}/messages/`)
    messages.value = response.data?.results || (Array.isArray(response.data) ? response.data : [])
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Failed to load messages:', err)
    messages.value = []
  } finally {
    loadingMessages.value = false
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  
  sending.value = true
  try {
    const response = await api.post(`/users/conversations/${selectedConversation.value.id}/messages/`, {
      content: newMessage.value
    })
    messages.value.push(response.data)
    newMessage.value = ''
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Failed to send message:', err)
  } finally {
    sending.value = false
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
</script>
