<template>
  <q-page
    class="page-root"
    style="display: flex; flex-direction: column; height: 100vh; padding-bottom: 0"
  >
    <!-- ── Header ── -->
    <div class="chat-header q-px-md q-pt-xl q-pb-sm">
      <div class="row items-center q-gutter-md">
        <!-- AI Avatar Orb -->
        <div class="avatar-wrap">
          <div class="avatar-ring" />
          <div class="avatar-core">◈</div>
        </div>

        <div class="col">
          <div
            class="font-display"
            style="font-size: 1.4rem; color: var(--text-primary); line-height: 1"
          >
            Aura
          </div>
          <div class="row items-center q-gutter-xs">
            <div class="status-dot" />
            <span
              class="text-caption"
              style="color: var(--indigo-light); letter-spacing: 0.04em; text-transform: none"
              >{{ $t('online_listening') }}</span
            >
          </div>
        </div>

        <div class="row q-gutter-xs">
          <button class="icon-btn" @click="confirmClear = true" :title="$t('clear_chat')">
            <q-icon name="refresh" size="18px" />
          </button>
          <button class="icon-btn" @click="infoDialog = true" :title="$t('about_aura')">
            <q-icon name="info_outline" size="18px" />
          </button>
        </div>
      </div>
    </div>

    <!-- ── Messages Area ── -->
    <div ref="chatScroll" class="col q-px-md q-py-md chat-scroll-area">
      <!-- Welcome / Encryption Notice -->
      <div class="q-mb-xl q-mt-md text-center animate-in">
        <div
          class="inline-block q-pa-sm"
          style="
            background: var(--indigo-muted);
            border-radius: var(--r-pill);
            border: 1px solid var(--border-subtle);
          "
        >
          <span
            class="text-caption"
            style="color: var(--indigo-light); font-family: 'JetBrains Mono', monospace"
          >
            <q-icon name="lock" size="12px" class="q-mr-xs" /> {{ $t('encrypted') }}
          </span>
        </div>
      </div>

      <!-- Messages -->
      <div v-for="msg in chatStore.messages" :key="msg.id" class="q-mb-lg animate-in-scale">
        <!-- AI Message -->
        <div v-if="msg.role === 'ai'" class="row items-end q-gutter-sm">
          <div class="avatar-small">◈</div>
          <div class="chat-bubble-ai q-pa-md">
            <div class="message-text" v-html="formatMsg(msg.content)" />
            <div class="timestamp right">{{ formatTime(msg.timestamp) }}</div>
          </div>
        </div>

        <!-- User Message -->
        <div v-else class="row items-end justify-end q-gutter-sm">
          <div class="chat-bubble-user q-pa-md">
            <div class="message-text">{{ msg.content }}</div>
            <div class="timestamp left" style="color: rgba(255, 255, 255, 0.6)">
              {{ formatTime(msg.timestamp) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="chatStore.isTyping" class="row items-end q-gutter-sm q-mb-md animate-in-scale">
        <div class="avatar-small">◈</div>
        <div class="chat-bubble-ai q-pa-md" style="padding: 14px 18px">
          <div class="row q-gutter-xs items-center" style="height: 12px">
            <div class="typing-dot" />
            <div class="typing-dot" />
            <div class="typing-dot" />
          </div>
        </div>
      </div>
    </div>

    <!-- ── Quick Chips ── -->
    <transition name="slide-up">
      <div
        v-if="chatStore.messages.length <= 2 && !chatStore.isTyping"
        class="chips-area q-px-md q-py-sm"
      >
        <div class="row q-gutter-sm no-wrap" style="overflow-x: auto; padding-bottom: 4px">
          <button
            v-for="chip in quickReplies"
            :key="chip"
            class="chip animate-in-scale"
            @click="sendQuick(chip)"
          >
            {{ chip }}
          </button>
        </div>
      </div>
    </transition>

    <!-- ── Input Bar ── -->
    <div class="chat-input-bar q-px-md q-pb-xl q-pt-sm">
      <div
        v-if="voiceTranscript"
        class="text-caption q-mb-xs q-px-sm"
        style="color: var(--indigo-light)"
      >
        🎙️ "{{ voiceTranscript }}"
      </div>
      <div class="row items-center q-gutter-sm">
        <!-- Voice Button -->
        <button class="mic-btn" :class="{ recording: isRecording }" @click="toggleVoice">
          <q-icon :name="isRecording ? 'stop' : 'mic'" size="20px" />
        </button>

        <!-- Text Input -->
        <div
          class="col aura-input row items-center q-px-md"
          style="height: 52px; border-radius: 100px"
        >
          <input
            v-model="inputText"
            :placeholder="$t('type_message')"
            @keyup.enter.exact.prevent="send"
            style="
              background: transparent;
              border: none;
              outline: none;
              color: var(--text-primary);
              font-family: 'Plus Jakarta Sans', sans-serif;
              width: 100%;
              font-size: 0.95rem;
            "
          />
        </div>

        <!-- Send Button -->
        <button
          class="send-btn"
          :class="{ active: inputText.trim() && !chatStore.isTyping }"
          :disabled="!inputText.trim() || chatStore.isTyping"
          @click="send"
        >
          <q-icon name="send" size="18px" />
        </button>
      </div>
      <div class="text-center q-mt-md">
        <span class="text-caption" style="font-size: 0.65rem">{{ $t('aura_mistakes') }}</span>
      </div>
    </div>

    <!-- ── Dialogs ── -->
    <q-dialog v-model="infoDialog">
      <q-card class="q-pa-lg">
        <div
          class="font-display"
          style="font-size: 1.6rem; color: var(--text-primary); margin-bottom: 8px"
        >
          {{ $t('about_aura') }}
        </div>
        <p style="color: var(--text-secondary); font-size: 0.9rem; line-height: 1.7">
          {{ $t('about_aura_desc') }}
          <br /><br />
          <strong style="color: var(--danger)">{{ $t('therapy_note') }}</strong>
        </p>
        <button class="btn-secondary full-width q-mt-md" @click="infoDialog = false">
          {{ $t('close') }}
        </button>
      </q-card>
    </q-dialog>

    <q-dialog v-model="confirmClear">
      <q-card class="q-pa-lg">
        <div
          class="font-display"
          style="font-size: 1.5rem; color: var(--text-primary); margin-bottom: 8px"
        >
          {{ $t('clear_session_q') }}
        </div>
        <p style="color: var(--text-muted); font-size: 0.9rem">
          {{ $t('clear_session_desc') }}
        </p>
        <div class="row q-gutter-sm q-mt-md">
          <button class="btn-ghost col" @click="confirmClear = false">{{ $t('cancel') }}</button>
          <button class="btn-danger col" @click="clearChat">{{ $t('clear_chat') }}</button>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useChatStore } from 'src/stores/chatStore'

const { t } = useI18n()
const chatStore = useChatStore()
const inputText = ref('')
const chatScroll = ref(null)
const infoDialog = ref(false)
const confirmClear = ref(false)
const isRecording = ref(false)
const voiceTranscript = ref('')

const quickReplies = computed(() => [
  t('quick_anxious'),
  t('quick_overwhelmed'),
  t('quick_sleep'),
  t('quick_low'),
])

async function send() {
  const text = inputText.value.trim()
  if (!text || chatStore.isTyping) return
  inputText.value = ''
  voiceTranscript.value = ''
  await chatStore.sendMessage(text)
  scrollToBottom()
}
function sendQuick(text) {
  inputText.value = text
  send()
}

function scrollToBottom() {
  nextTick(() => {
    if (chatScroll.value) {
      chatScroll.value.scrollTo({ top: chatScroll.value.scrollHeight, behavior: 'smooth' })
    }
  })
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString(t('language_code'), {
    hour: 'numeric',
    minute: '2-digit',
  })
}
function formatMsg(text) {
  return text
    .replace(
      /\*\*(.*?)\*\*/g,
      '<strong style="color:var(--indigo-light);font-weight:700;">$1</strong>',
    )
    .replace(/\n/g, '<br/>')
}

// Minimal Voice API for demo
let recognition = null
function toggleVoice() {
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert('Voice input not supported in this browser.')
    return
  }
  if (isRecording.value) {
    recognition?.stop()
    isRecording.value = false
    return
  }

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition
  recognition = new SR()
  recognition.lang = t('language_code')
  recognition.continuous = false
  recognition.interimResults = true
  recognition.onresult = (e) => {
    const t = Array.from(e.results)
      .map((r) => r[0].transcript)
      .join('')
    voiceTranscript.value = t
    if (e.results[0].isFinal) {
      inputText.value = t
      voiceTranscript.value = ''
      isRecording.value = false
      send() // Auto-submit voice input
    }
  }
  recognition.onerror = () => {
    isRecording.value = false
  }
  recognition.onend = () => {
    isRecording.value = false
  }
  recognition.start()
  isRecording.value = true
}

function clearChat() {
  chatStore.clearChat()
  confirmClear.value = false
  setTimeout(() => {
    chatStore.speakText(chatStore.messages[0].content)
  }, 200)
  scrollToBottom()
}
watch(() => chatStore.messages.length, scrollToBottom)
watch(() => chatStore.isTyping, scrollToBottom)

onMounted(() => {
  if (chatStore.messages.length === 1 && !sessionStorage.getItem('aura_intro_spoken')) {
    // Speak initial greeting if it's a new session
    sessionStorage.setItem('aura_intro_spoken', 'true')
    setTimeout(() => {
      chatStore.speakText(chatStore.messages[0].content)
    }, 500)
  }
})
</script>

<style scoped>
/* Header */
.chat-header {
  background: rgba(7, 11, 20, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
  z-index: 10;
}

.avatar-wrap {
  position: relative;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.avatar-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 1px solid var(--border-strong);
  animation: spin-slow 10s linear infinite;
}
.avatar-core {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--grad-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  box-shadow: var(--indigo-glow);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--mint);
  box-shadow: 0 0 8px var(--mint);
  animation: pulse 2s ease-in-out infinite;
}

/* Chat Area */
.chat-scroll-area {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.avatar-small {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--bg-elevated);
  border: 1px solid var(--border-mid);
  color: var(--indigo-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.message-text {
  font-size: 0.95rem;
  line-height: 1.6;
  font-family: 'Inter', sans-serif;
  letter-spacing: 0.01em;
}

.timestamp {
  font-size: 0.65rem;
  color: var(--text-muted);
  margin-top: 6px;
  font-family: 'JetBrains Mono', monospace;
  &.right {
    text-align: right;
  }
  &.left {
    text-align: left;
  }
}

/* Input Bar */
.chat-input-bar {
  background: rgba(7, 11, 20, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid var(--border-subtle);
  flex-shrink: 0;
  z-index: 10;
}

.mic-btn {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: none;
  background: var(--bg-elevated);
  color: var(--text-secondary);
  box-shadow: inset 0 0 0 1px var(--border-subtle);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  &:hover {
    background: var(--indigo-muted);
    color: var(--indigo-light);
  }
  &.recording {
    background: var(--danger-muted);
    color: var(--danger);
    box-shadow:
      inset 0 0 0 1px var(--danger),
      var(--danger-glow);
    animation: danger-pulse 1.5s infinite;
  }
}

.send-btn {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: none;
  background: var(--bg-elevated);
  color: var(--text-muted);
  cursor: not-allowed;
  transition: all 0.25s var(--ease-spring);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  &.active {
    background: var(--grad-primary);
    color: #fff;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
    &:hover {
      transform: scale(1.08);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
    }
    &:active {
      transform: scale(0.95);
    }
  }
}

/* Scrollbar hide for chips */
.chips-area ::-webkit-scrollbar {
  display: none;
}
</style>
