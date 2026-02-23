import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useWellnessStore = defineStore(
  'wellness',
  () => {
    const checkIns = ref([]) // [{ date, mood, score, note }]
    const streakDays = ref(0)
    const lastCheckInDate = ref(null)
    const companionLevel = ref(1)
    const companionXP = ref(0)
    const weeklyScores = ref([])
    const userName = ref('')
    const userAge = ref(null)
    const userAvatar = ref(null)
    const journalEntries = ref([])
    const appLanguage = ref('en-US')

    // Mood history for chart
    const moodHistory = computed(() => checkIns.value.slice(-7))

    const wellnessScore = computed(() => {
      if (!weeklyScores.value.length) return null
      const sum = weeklyScores.value.reduce((a, b) => a + b, 0)
      return Math.round(sum / weeklyScores.value.length)
    })

    const companionXpToNext = computed(() => companionLevel.value * 100)
    const companionProgress = computed(() =>
      Math.min((companionXP.value / companionXpToNext.value) * 100, 100),
    )

    function logCheckIn(mood, score, note = '') {
      const today = new Date().toISOString().split('T')[0]

      if (lastCheckInDate.value === today) return // already checked in today

      checkIns.value.push({
        id: Date.now(),
        date: today,
        mood,
        score,
        note,
      })

      weeklyScores.value.push(score)
      if (weeklyScores.value.length > 7) weeklyScores.value.shift()

      // Streak logic
      const yesterday = new Date()
      yesterday.setDate(yesterday.getDate() - 1)
      const yStr = yesterday.toISOString().split('T')[0]

      if (lastCheckInDate.value === yStr) {
        streakDays.value++
      } else if (lastCheckInDate.value !== today) {
        streakDays.value = 1
      }

      lastCheckInDate.value = today

      // Award XP
      gainXP(20 + Math.floor(score / 5))
    }

    function gainXP(amount) {
      companionXP.value += amount
      while (companionXP.value >= companionXpToNext.value) {
        companionXP.value -= companionXpToNext.value
        companionLevel.value++
      }
    }

    function clearAllData() {
      checkIns.value = []
      streakDays.value = 0
      lastCheckInDate.value = null
      companionLevel.value = 1
      companionXP.value = 0
      weeklyScores.value = []
      userName.value = ''
      userAge.value = null
      userAvatar.value = null
      journalEntries.value = []
      appLanguage.value = 'en-US'
    }

    function updateUser(name, age) {
      userName.value = name
      userAge.value = age
    }

    function setAvatar(url) {
      userAvatar.value = url
    }

    return {
      checkIns,
      streakDays,
      lastCheckInDate,
      companionLevel,
      companionXP,
      weeklyScores,
      userName,
      userAge,
      userAvatar,
      journalEntries,
      appLanguage,
      moodHistory,
      wellnessScore,
      companionXpToNext,
      companionProgress,
      logCheckIn,
      gainXP,
      clearAllData,
      updateUser,
      setAvatar,
    }
  },
  { persist: true },
)
