import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useWellnessStore } from './wellnessStore'
import enUS from 'src/i18n/en-US'
import siLK from 'src/i18n/si-LK'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useChatStore = defineStore(
  'chat',
  () => {
    const wellnessStore = useWellnessStore()
    const getIcebreaker = () => {
      return wellnessStore.appLanguage === 'si-LK' ? siLK.icebreaker_msg : enUS.icebreaker_msg
    }

    const messages = ref([
      {
        id: 1,
        role: 'ai',
        content: getIcebreaker(),
        timestamp: new Date().toISOString(),
      },
    ])
    const isTyping = ref(false)
    const sessionId = ref(null)
    const extractedData = ref({})
    const crisisDetected = ref(false)
    const conversationPhase = ref('icebreaker') // icebreaker | intake | assessment | completed

    const messageCount = computed(() => messages.value.length)

    function addUserMessage(content) {
      messages.value.push({
        id: Date.now(),
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      })
    }

    function addAiMessage(content) {
      messages.value.push({
        id: Date.now() + 1,
        role: 'ai',
        content,
        timestamp: new Date().toISOString(),
      })
      speakText(content)
    }

    // --- Voice Synthesis Engine ---
    const getBestVoice = (langCode) => {
      const voices = window.speechSynthesis.getVoices()
      if (langCode === 'si-LK') {
        return (
          voices.find((v) => v.lang.startsWith('si')) ||
          voices.find((v) => v.lang === 'en-IN') ||
          voices[0]
        )
      }
      const enUSVoices = voices.filter((v) => v.lang === 'en-US')
      return enUSVoices.find((v) => v.name.includes('Female')) || enUSVoices[0] || voices[0]
    }

    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.onvoiceschanged = () => {
        window.speechSynthesis.getVoices()
      }
    }

    function speakText(text) {
      if (typeof window === 'undefined' || !('speechSynthesis' in window)) return

      // Stop any ongoing speech
      window.speechSynthesis.cancel()

      // Clean text before speech (remove emojis, markdown)
      const cleanText = text
        .replace(
          /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu,
          '',
        )
        .replace(/\*\*(.*?)\*\*/g, '$1')
        .replace(/__/g, '')
        .replace(/\s+/g, ' ')
        .replace(/<br\/>/g, ' ')
        .trim()

      if (!cleanText) return

      const utterance = new SpeechSynthesisUtterance(cleanText)

      const isSinhala = wellnessStore.appLanguage === 'si-LK'
      utterance.lang = isSinhala ? 'si-LK' : 'en-US'
      utterance.voice = getBestVoice(utterance.lang)

      utterance.rate = isSinhala ? 0.85 : 0.95 // slower paced
      utterance.pitch = 1.05
      utterance.volume = 1.0

      window.speechSynthesis.speak(utterance)
    }
    // --------------------------------

    async function sendMessage(userText) {
      addUserMessage(userText)
      isTyping.value = true

      try {
        const response = await axios.post(`${API_BASE}/api/chat/message`, {
          message: userText,
          session_id: sessionId.value,
          conversation_phase: conversationPhase.value,
          language: wellnessStore.appLanguage,
        })

        const data = response.data

        if (data.session_id) sessionId.value = data.session_id
        if (data.extracted_data) {
          extractedData.value = { ...extractedData.value, ...data.extracted_data }
        }
        if (data.crisis_detected) {
          crisisDetected.value = true
        }
        if (data.phase) conversationPhase.value = data.phase

        // Simulate human-like delay
        await new Promise((r) => setTimeout(r, 600 + Math.random() * 600))
        addAiMessage(data.reply)
      } catch (err) {
        console.error('Chat error:', err)
        // Offline fallback
        addAiMessage(
          "I'm having a little trouble connecting right now. If you're in crisis, please call **1333** immediately. I'll be right back. 💜",
        )
        runOfflineCrisisScan(userText)
      } finally {
        isTyping.value = false
      }
    }

    // Offline rule-based crisis detection
    const CRISIS_KEYWORDS = [
      'kill myself',
      'end my life',
      'suicide',
      'suicidal',
      'self harm',
      'hurt myself',
      'want to die',
      'no reason to live',
      'better off dead',
      'no point living',
      'overdose',
      'cut myself',
    ]

    function runOfflineCrisisScan(text) {
      const lower = text.toLowerCase()
      if (CRISIS_KEYWORDS.some((kw) => lower.includes(kw))) {
        crisisDetected.value = true
      }
    }

    function dismissCrisis() {
      crisisDetected.value = false
    }

    function clearChat() {
      messages.value = [
        {
          id: 1,
          role: 'ai',
          content:
            "Hi, I'm Aura. I'm here to listen without judgment and help evaluate your mental well-being. Could you start by telling me your name and how you're feeling today?",
          timestamp: new Date().toISOString(),
        },
      ]
      sessionId.value = null
      extractedData.value = {}
      crisisDetected.value = false
      conversationPhase.value = 'icebreaker'
    }

    return {
      messages,
      isTyping,
      sessionId,
      extractedData,
      crisisDetected,
      conversationPhase,
      messageCount,
      sendMessage,
      addAiMessage,
      addUserMessage,
      runOfflineCrisisScan,
      dismissCrisis,
      clearChat,
      speakText,
    }
  },
  { persist: true },
)
