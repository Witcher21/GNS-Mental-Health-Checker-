<template>
  <q-page class="page-root" style="padding-bottom: 0">
    <!-- ── PORTAL ENTRY ── -->
    <transition name="portal-out">
      <div v-if="phase === 'entry'" key="entry" class="portal-scene">
        <!-- Aurora Canvas -->
        <canvas ref="auroraCanvas" class="aurora-canvas" />

        <!-- Floating orbs -->
        <div class="portal-orb p-orb-1" />
        <div class="portal-orb p-orb-2" />
        <div class="portal-orb p-orb-3" />

        <!-- Gentle vignette -->
        <div class="vignette" />

        <div class="portal-scroll-area">
          <div class="portal-content-wrapper">
            <div class="fluid-spacer"></div>

            <!-- Entry Content -->
            <div class="entry-center" :class="{ dimming: doorOpening }">
              <!-- Animated logo mark -->
              <div class="logo-mark animate-in" style="animation-delay: 0.1s">
                <div class="logo-ring" />
                <div class="logo-ring r2" />
                <div class="logo-inner">💜</div>
              </div>

              <div class="animate-in" style="animation-delay: 0.2s; margin-top: 28px">
                <div class="entry-eyebrow">AURA · VIBESYNC</div>
                <h1 class="entry-headline">
                  {{ $t('home') }}<br />
                  <span class="text-gradient">{{ $t('wellness') }}</span>
                </h1>
                <p class="entry-sub">
                  {{ $t('aura_slogan') }}
                </p>
              </div>

              <div class="animate-in" style="animation-delay: 0.4s; margin-top: 36px">
                <button class="enter-btn" :class="{ loading: doorOpening }" @click="enterPortal">
                  <span v-if="!doorOpening" class="enter-btn-content">
                    <span>{{ $t('start_journey') }}</span>
                    <span class="enter-arrow">→</span>
                  </span>
                  <span v-else class="enter-loading">
                    <span class="loading-dot" /><span class="loading-dot" /><span
                      class="loading-dot"
                    />
                  </span>
                </button>
                <p class="entry-disclaimer">{{ $t('entry_disclaimer') }}</p>
              </div>
            </div>

            <div class="fluid-spacer"></div>

            <!-- Bottom stats row -->
            <div class="entry-stats animate-in" style="animation-delay: 0.6s">
              <div class="entry-stat" v-for="s in stats" :key="s.labelKey">
                <span class="stat-val">{{ $t(s.valKey) }}</span>
                <span class="stat-lbl">{{ $t(s.labelKey) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- ── PROFILE SELECT ── -->
    <transition name="portal-out">
      <div
        v-if="phase === 'profile-select'"
        key="profile-select"
        class="portal-scene flex-center"
        style="
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          padding: 40px 20px;
        "
      >
        <div
          class="glass-card q-pa-xl text-center animate-in"
          style="width: 100%; max-width: 450px; margin: auto; position: relative; z-index: 10"
        >
          <h2 class="font-display q-mb-md" style="font-size: 2rem; color: var(--text-primary)">
            {{ $t('who_is_using') }}
          </h2>
          <p style="color: var(--text-secondary); margin-bottom: 30px">
            {{ $t('select_profile') }}
          </p>

          <div class="row q-col-gutter-md q-mb-lg justify-center">
            <div class="col-6" v-for="p in profiles" :key="p.id">
              <div class="profile-card" @click="selectProfile(p)">
                <div class="profile-avatar">{{ p.name.substring(0, 2).toUpperCase() }}</div>
                <div class="profile-name">{{ p.name }}</div>
              </div>
            </div>
          </div>
          <button
            v-if="profiles.length < 3"
            class="btn-ghost full-width"
            @click="phase = 'onboarding'"
          >
            {{ $t('add_user') }}
          </button>
        </div>
        <div class="bg-atmosphere"><div class="particle-field" /></div>
      </div>
    </transition>

    <!-- ── ONBOARDING ── -->
    <transition name="portal-out">
      <div
        v-if="phase === 'onboarding'"
        key="onboarding"
        class="portal-scene flex-center"
        style="
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          padding: 40px 20px;
        "
      >
        <div
          class="glass-card q-pa-xl text-center animate-in"
          style="width: 100%; max-width: 400px; margin: auto; position: relative; z-index: 10"
        >
          <h2 class="font-display q-mb-md" style="font-size: 2rem; color: var(--text-primary)">
            {{ $t('welcome') }}
          </h2>
          <p style="color: var(--text-secondary); margin-bottom: 30px">
            {{ $t('personalize') }}
          </p>

          <input
            v-model="onboardName"
            :placeholder="$t('your_name')"
            class="journal-input q-mb-md"
            style="
              padding: 16px;
              background: rgba(0, 0, 0, 0.3);
              border: 1px solid var(--border-subtle);
              border-radius: 8px;
              width: 100%;
              color: white;
              margin-bottom: 20px;
            "
          />
          <input
            v-model="onboardAge"
            type="number"
            :placeholder="$t('your_age')"
            class="journal-input q-mb-lg"
            style="
              padding: 16px;
              background: rgba(0, 0, 0, 0.3);
              border: 1px solid var(--border-subtle);
              border-radius: 8px;
              width: 100%;
              color: white;
              margin-bottom: 30px;
            "
          />

          <button class="btn-primary full-width" style="padding: 14px" @click="finishOnboarding">
            {{ $t('start_journey') }}
          </button>
          <button
            v-if="profiles.length > 0"
            class="btn-ghost full-width"
            @click="phase = 'profile-select'"
          >
            {{ $t('back_to_profiles') }}
          </button>
        </div>
        <div class="bg-atmosphere"><div class="particle-field" /></div>
      </div>
    </transition>

    <!-- ── DASHBOARD ── -->
    <transition name="dash-in">
      <div
        v-if="phase === 'dashboard'"
        key="dash"
        class="dash-scroll q-px-md q-pt-xl"
        style="padding-bottom: 110px"
      >
        <!-- Header -->
        <div class="row items-center justify-between q-mb-xl animate-in">
          <div>
            <p class="section-label" style="margin-bottom: 6px">{{ greeting }}</p>
            <h2
              class="font-display"
              style="font-size: 1.9rem; color: var(--text-primary); margin: 0"
            >
              {{ $t('how_feeling') }}
            </h2>
          </div>
          <button class="icon-btn" @click="$router.push('/settings')">
            <q-icon name="person" size="22px" />
          </button>
        </div>

        <!-- Wellness Score Card -->
        <div class="gradient-card q-pa-lg q-mb-md animate-in delay-1">
          <div class="row items-center justify-between q-mb-lg">
            <div>
              <div class="section-label q-mb-sm">{{ $t('wellness_score') }}</div>
              <div class="row items-end" style="gap: 8px">
                <span
                  class="font-display"
                  style="font-size: 3.8rem; line-height: 1"
                  :style="{ color: scoreColor }"
                >
                  {{ wellnessStore.wellnessScore ?? '—' }}
                </span>
                <span
                  class="font-heading"
                  style="font-size: 1.2rem; color: var(--text-muted); padding-bottom: 8px"
                  >/100</span
                >
              </div>
              <div :class="scoreBadgeClass" style="margin-top: 6px">{{ scoreLabel }}</div>
            </div>
            <!-- Companion -->
            <div class="companion-wrap" style="margin-right: 8px">
              <div class="companion-ring" />
              <div class="companion-ring-2" />
              <div class="companion-body" style="font-size: 3.6rem; position: relative; z-index: 1">
                {{ companionEmoji }}
              </div>
            </div>
          </div>

          <!-- Mood strip -->
          <div class="section-label q-mb-sm">{{ $t('wellness_trace') }}</div>
          <div class="row q-gutter-xs">
            <div v-for="(entry, i) in weekStrip" :key="i" class="col">
              <div
                :style="{
                  height: '36px',
                  borderRadius: '6px',
                  background: entry ? moodFill(entry.score) : 'rgba(255,255,255,0.04)',
                  border: entry
                    ? '1px solid rgba(99,102,241,0.3)'
                    : '1px solid rgba(255,255,255,0.05)',
                  transition: 'all 0.4s var(--ease-spring)',
                  animationDelay: i * 0.06 + 's',
                }"
              />
              <div
                style="
                  text-align: center;
                  font-size: 9px;
                  color: var(--text-muted);
                  margin-top: 4px;
                  font-family: 'JetBrains Mono', monospace;
                "
              >
                {{ entry ? dayLabel(entry.date) : '·' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Quick actions -->
        <div class="row q-gutter-sm q-mb-md animate-in delay-2">
          <button
            class="btn-primary col"
            style="padding: 15px 0; border-radius: var(--r-md)"
            @click="$router.push('/chat')"
          >
            💬 &nbsp;{{ $t('talk_to_aura') }}
          </button>
          <button
            class="btn-secondary col"
            style="padding: 15px 0; border-radius: var(--r-md)"
            @click="checkInDialog = true"
          >
            ✦ &nbsp;{{ $t('check_in_now') }}
          </button>
        </div>

        <!-- Streak + Companion row -->
        <div class="row q-gutter-sm q-mb-md">
          <!-- Streak -->
          <div class="glass-card col q-pa-md animate-in delay-3" style="cursor: default">
            <div class="row items-center q-gutter-sm q-mb-xs">
              <span style="font-size: 1.5rem">🔥</span>
              <span class="font-heading" style="font-size: 1.6rem; color: var(--text-primary)">{{
                wellnessStore.streakDays
              }}</span>
            </div>
            <div style="font-size: 0.78rem; font-weight: 600; color: var(--text-secondary)">
              {{ $t('streak') }}
            </div>
            <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 2px">
              {{ $t(streakMsgKey) }}
            </div>
          </div>
          <!-- Companion level -->
          <div
            class="glass-card col q-pa-md animate-in delay-3"
            style="cursor: pointer"
            @click="$router.push('/wellness')"
          >
            <div class="row items-center justify-between q-mb-sm">
              <div class="badge-violet">Lv {{ wellnessStore.companionLevel }}</div>
              <span>{{ companionEmoji }}</span>
            </div>
            <div class="progress-bar q-mb-xs">
              <div class="fill" :style="{ width: wellnessStore.companionProgress + '%' }" />
            </div>
            <div style="font-size: 0.7rem; color: var(--text-muted)">
              {{ wellnessStore.companionXP }}/{{ wellnessStore.companionXpToNext }} XP
            </div>
          </div>
        </div>

        <!-- Module Grid -->
        <div class="section-label q-mb-sm animate-in delay-4">{{ $t('quick_access') }}</div>
        <div class="row q-gutter-sm q-mb-xl">
          <div
            v-for="(m, i) in modules"
            :key="m.label"
            class="glass-card col q-pa-md animate-in"
            :class="`delay-${i + 5}`"
            style="cursor: pointer; min-width: calc(50% - 8px)"
            @click="$router.push(m.route)"
          >
            <div
              :style="{
                width: '48px',
                height: '48px',
                borderRadius: 'var(--r-md)',
                background: `linear-gradient(135deg, ${m.c1}, ${m.c2})`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.4rem',
                marginBottom: '10px',
                boxShadow: `0 4px 16px ${m.c1}40`,
              }"
            >
              {{ m.emoji }}
            </div>
            <div
              style="
                font-weight: 700;
                font-size: 0.9rem;
                color: var(--text-primary);
                margin-bottom: 2px;
              "
            >
              {{ $t(m.label) }}
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted)">{{ $t(m.desc) }}</div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Check-in dialog -->
    <q-dialog v-model="checkInDialog">
      <q-card class="q-pa-xl" style="width: 100%; max-width: 420px">
        <h3 class="font-heading" style="font-size: 1.5rem; margin: 0 0 4px">
          {{ $t('check_in_now') }}
        </h3>
        <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0 0 24px">
          {{ $t('how_feeling') }}
        </p>

        <div class="row justify-between q-mb-lg">
          <div
            v-for="m in moods"
            :key="m.emoji"
            style="
              cursor: pointer;
              text-align: center;
              transition: transform 0.2s var(--ease-spring);
            "
            :style="{ transform: selectedMood?.emoji === m.emoji ? 'scale(1.18)' : 'scale(1)' }"
            @click="selectedMood = m"
          >
            <div
              style="
                font-size: 2rem;
                width: 50px;
                height: 50px;
                border-radius: var(--r-md);
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
              "
              :style="{
                background:
                  selectedMood?.emoji === m.emoji ? 'var(--indigo-muted)' : 'var(--bg-elevated)',
                border:
                  selectedMood?.emoji === m.emoji
                    ? '2px solid var(--indigo)'
                    : '1px solid var(--border-subtle)',
                boxShadow: selectedMood?.emoji === m.emoji ? 'var(--indigo-glow)' : 'none',
              }"
            >
              {{ m.emoji }}
            </div>
            <div
              style="
                font-size: 9px;
                color: var(--text-muted);
                margin-top: 4px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.06em;
              "
            >
              {{ $t(m.label) }}
            </div>
          </div>
        </div>

        <div
          style="
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 8px;
          "
        >
          {{ $t('intensity') }} —
          <span :style="{ color: 'var(--indigo-light)' }">{{ moodScore }}</span>
        </div>
        <q-slider
          v-model="moodScore"
          :min="0"
          :max="100"
          :step="5"
          color="primary"
          class="q-mb-xl"
        />

        <div class="row q-gutter-sm">
          <button class="btn-ghost col" style="padding: 12px" @click="checkInDialog = false">
            {{ $t('cancel') }}
          </button>
          <button
            class="btn-primary col"
            style="padding: 12px"
            :style="{
              opacity: !selectedMood ? 0.45 : 1,
              cursor: !selectedMood ? 'not-allowed' : 'pointer',
            }"
            :disabled="!selectedMood"
            @click="saveCheckIn"
          >
            {{ $t('save_check_in') }}
          </button>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useQuasar } from 'quasar'
import { useI18n } from 'vue-i18n'
import { useWellnessStore } from 'src/stores/wellnessStore'

const { t } = useI18n()
const $q = useQuasar()
const wellnessStore = useWellnessStore()
const phase = ref('entry')
const doorOpening = ref(false)
const auroraCanvas = ref(null)
const checkInDialog = ref(false)
const selectedMood = ref(null)
const moodScore = ref(60)

const onboardName = ref('')
const onboardAge = ref('')
const profiles = ref(JSON.parse(localStorage.getItem('aura-profiles') || '[]'))

const greeting = computed(() => {
  const hour = new Date().getHours()
  const timeKey = hour < 12 ? 'morning' : hour < 17 ? 'afternoon' : 'evening'
  const timeStr = t(timeKey)
  return wellnessStore.userName ? `${timeStr}, ${wellnessStore.userName}` : timeStr
})

const stats = [
  { valKey: 'users_supported_val', labelKey: 'users_supported' },
  { valKey: 'private_encrypted_val', labelKey: 'private_encrypted' },
  { valKey: 'crisis_support_val', labelKey: 'crisis_support' },
]

const moods = [
  { emoji: '😔', label: 'low', score: 20 },
  { emoji: '😐', label: 'meh', score: 45 },
  { emoji: '🙂', label: 'okay', score: 65 },
  { emoji: '😊', label: 'good', score: 80 },
  { emoji: '🤩', label: 'great', score: 95 },
]

const modules = [
  {
    emoji: '🧠',
    label: 'ai_triage',
    desc: 'talk_to_aura',
    route: '/chat',
    c1: '#6366F1',
    c2: '#8B5CF6',
  },
  {
    emoji: '🏋️',
    label: 'wellness',
    desc: 'daily_exercises',
    route: '/wellness',
    c1: '#34D399',
    c2: '#059669',
  },
  {
    emoji: '📅',
    label: 'therapy',
    desc: 'book_session',
    route: '/booking',
    c1: '#F472B6',
    c2: '#DB2777',
  },
  {
    emoji: '📓',
    label: 'journal',
    desc: 'private_log',
    route: '/journal',
    c1: '#FBBF24',
    c2: '#F97316',
  },
]

function enterPortal() {
  doorOpening.value = true
  setTimeout(() => {
    if (wellnessStore.userName) {
      phase.value = 'dashboard'
    } else {
      const savedProfiles = JSON.parse(localStorage.getItem('aura-profiles') || '[]')
      if (savedProfiles.length > 0) {
        profiles.value = savedProfiles
        phase.value = 'profile-select'
      } else {
        phase.value = 'onboarding'
      }
    }
    doorOpening.value = false
  }, 900)
}

function selectProfile(p) {
  localStorage.setItem('aura-active-profile-id', p.id)
  sessionStorage.setItem('aura-skip-intro', 'true')
  window.location.reload()
}

function finishOnboarding() {
  if (!onboardName.value.trim() || !onboardAge.value) {
    $q.notify({
      message: t('enter_name_age'),
      color: 'warning',
      position: 'top',
    })
    return
  }

  const newId = 'p_' + Date.now()
  const savedProfiles = JSON.parse(localStorage.getItem('aura-profiles') || '[]')

  // Max 3 Check
  if (savedProfiles.length >= 3) {
    $q.notify({
      message: t('max_profiles'),
      color: 'negative',
      position: 'top',
    })
    return
  }

  savedProfiles.push({ id: newId, name: onboardName.value.trim(), age: onboardAge.value })
  localStorage.setItem('aura-profiles', JSON.stringify(savedProfiles))
  localStorage.setItem('aura-active-profile-id', newId)

  // Initialize the new profile's wellness store directly in localStorage
  // so it exists perfectly formatted when the page reloads.
  const initialWellnessData = {
    userName: onboardName.value.trim(),
    userAge: onboardAge.value,
    checkIns: [],
    journalEntries: [],
    streakDays: 0,
    companionLevel: 1,
    companionXP: 0,
    weeklyScores: [],
  }
  localStorage.setItem(`aura-store-wellness-${newId}`, JSON.stringify(initialWellnessData))

  // Reload to instantiate fully isolated environment
  sessionStorage.setItem('aura-skip-intro', 'true')
  window.location.reload()
}

const scoreColor = computed(() => {
  const s = wellnessStore.wellnessScore
  if (!s) return 'var(--text-muted)'
  return s < 40 ? 'var(--danger)' : s < 65 ? 'var(--amber)' : 'var(--mint)'
})
const scoreBadgeClass = computed(() => {
  const s = wellnessStore.wellnessScore
  if (!s) return 'badge-indigo'
  return s < 40 ? 'badge-danger' : s < 65 ? 'badge-amber' : 'badge-mint'
})
const scoreLabel = computed(() => {
  const s = wellnessStore.wellnessScore
  if (!s) return t('no_data')
  return s < 40 ? t('needs_attention') : s < 65 ? t('moderate') : t('optimal')
})
const companionEmoji = computed(() => {
  const lv = wellnessStore.companionLevel
  return lv >= 10 ? '🌟' : lv >= 7 ? '🦋' : lv >= 5 ? '🌸' : lv >= 3 ? '🌱' : '🥚'
})
const streakMsgKey = computed(() => {
  const s = wellnessStore.streakDays
  return s === 0 ? 'streak_start' : s < 7 ? 'streak_keep' : 'streak_amazing'
})
const weekStrip = computed(() => {
  const slots = []
  for (let i = 6; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    slots.push(wellnessStore.checkIns.find((c) => c.date === d.toISOString().split('T')[0]) || null)
  }
  return slots
})
function dayLabel(date) {
  return new Date(date).toLocaleDateString(t('language_code'), { weekday: 'short' }).slice(0, 1)
}
function moodFill(score) {
  if (score < 40) return 'linear-gradient(135deg, rgba(239,68,68,0.5), rgba(239,68,68,0.25))'
  if (score < 65) return 'linear-gradient(135deg, rgba(251,191,36,0.5), rgba(251,191,36,0.25))'
  return 'linear-gradient(135deg, rgba(99,102,241,0.6), rgba(139,92,246,0.3))'
}
function saveCheckIn() {
  wellnessStore.logCheckIn(selectedMood.value.emoji, moodScore.value)
  checkInDialog.value = false
  selectedMood.value = null
  moodScore.value = 60
}

// Aurora canvas
let animId = null
function initAurora() {
  const canvas = auroraCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  const W = canvas.width,
    H = canvas.height
  function draw(t) {
    ctx.clearRect(0, 0, W, H)
    // Removed solid background fill to allow persistent 3D background to show through.
    // bg.addColorStop(0, '#080B14')
    // bg.addColorStop(1, '#0A0F1E')
    // ctx.fillStyle = bg
    // ctx.fillRect(0, 0, W, H)

    // Aurora waves
    const waves = [
      { y: H * 0.4, amp: 70, freq: 0.003, speed: 0.5, c: 'rgba(99,102,241,', alpha: 0.07 },
      { y: H * 0.55, amp: 50, freq: 0.004, speed: 0.3, c: 'rgba(139,92,246,', alpha: 0.06 },
      { y: H * 0.65, amp: 40, freq: 0.0025, speed: 0.4, c: 'rgba(52,211,153,', alpha: 0.04 },
    ]
    waves.forEach((w) => {
      ctx.beginPath()
      for (let x = 0; x <= W; x += 2) {
        const y = w.y + Math.sin(x * w.freq + t * w.speed) * w.amp
        x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)
      }
      ctx.lineTo(W, H)
      ctx.lineTo(0, H)
      ctx.closePath()
      const grad = ctx.createLinearGradient(0, w.y - w.amp, 0, w.y + w.amp)
      grad.addColorStop(0, w.c + w.alpha + ')')
      grad.addColorStop(1, w.c + '0)')
      ctx.fillStyle = grad
      ctx.fill()
    })

    // Stars
    for (let i = 0; i < 60; i++) {
      const sx = (i * 173.47) % W,
        sy = (i * 97.23) % (H * 0.6)
      const twinkle = 0.3 + 0.5 * Math.sin(t * 0.5 + i)
      ctx.beginPath()
      ctx.arc(sx, sy, 0.8, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(255,255,255,${twinkle * 0.5})`
      ctx.fill()
    }

    animId = requestAnimationFrame((ts) => draw(ts / 1000))
  }
  draw(0)
}

onMounted(() => {
  if (sessionStorage.getItem('aura-skip-intro') === 'true') {
    sessionStorage.removeItem('aura-skip-intro')
    phase.value = 'dashboard'
  }
  nextTick(initAurora)
})
onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
})
</script>

<style scoped>
/* Portal Scene */
.portal-scene {
  position: fixed;
  inset: 0;
  z-index: 10;
  overflow: hidden;
  background: transparent;
}
.portal-scroll-area {
  position: absolute;
  inset: 0;
  z-index: 3;
  overflow-y: auto;
  overflow-x: hidden;
}
.portal-content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100%;
  width: 100%;
  padding-bottom: 120px; /* Crucial: clears the bottom fixed navigation bar on mobile */
}
.fluid-spacer {
  flex: 1;
  min-height: 35px;
  width: 100%;
}
.aurora-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
.vignette {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  background: radial-gradient(ellipse at center, transparent 40%, rgba(7, 11, 20, 0.8) 100%);
}

/* Floating background orbs for portal */
.portal-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  pointer-events: none;
  z-index: 1;
}
.p-orb-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.18), transparent 70%);
  top: -100px;
  left: -100px;
  animation: orb-float 14s ease-in-out infinite;
}
.p-orb-2 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.14), transparent 70%);
  bottom: 60px;
  right: -80px;
  animation: orb-float 18s ease-in-out infinite reverse;
}
.p-orb-3 {
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(52, 211, 153, 0.1), transparent 70%);
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: orb-float 22s ease-in-out infinite;
  animation-delay: -8s;
}

/* Logo Mark */
.logo-mark {
  width: 88px;
  height: 88px;
  position: relative;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
}
.logo-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 1.5px solid rgba(99, 102, 241, 0.5);
  animation: ring-expand 3s ease-in-out infinite;
}
.logo-ring.r2 {
  inset: -14px;
  border-color: rgba(139, 92, 246, 0.25);
  animation-delay: 0.5s;
}
.logo-inner {
  font-size: 2.6rem;
  animation: float-gentle 4s ease-in-out infinite;
  position: relative;
  z-index: 1;
}

/* Entry Text */
.entry-center {
  position: relative;
  z-index: 3;
  text-align: center;
  padding: 20px 24px;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  transition: opacity 0.5s ease;
}
.entry-center.dimming {
  opacity: 0;
  transform: scale(0.98);
}

.entry-eyebrow {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--indigo-light);
  margin-bottom: 12px;
  opacity: 0.85;
}
.entry-headline {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  font-size: clamp(2.4rem, 6vw, 3.6rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin: 0;
}
.entry-sub {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 16px 0 0;
  line-height: 1.6;
  font-weight: 400;
}

/* ENTER button */
.enter-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 16px 40px;
  border-radius: 100px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  color: #fff;
  cursor: pointer;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  box-shadow:
    0 8px 32px rgba(99, 102, 241, 0.45),
    0 2px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.3s var(--ease-spring);
  min-width: 220px;
  min-height: 56px;

  &:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.55);
  }
  &:active {
    transform: scale(0.97);
  }
  &.loading {
    pointer-events: none;
    opacity: 0.8;
  }
}
.enter-btn-content {
  display: flex;
  align-items: center;
  gap: 10px;
}
.enter-arrow {
  font-size: 1.2rem;
  transition: transform 0.2s;
}
.enter-btn:hover .enter-arrow {
  transform: translateX(4px);
}
.enter-loading {
  display: flex;
  gap: 6px;
  align-items: center;
}
.loading-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  animation: typing-pulse 1.2s ease-in-out infinite;
  &:nth-child(2) {
    animation-delay: 0.15s;
  }
  &:nth-child(3) {
    animation-delay: 0.3s;
  }
}
.entry-disclaimer {
  font-size: 0.72rem;
  color: var(--text-dim);
  margin-top: 14px;
  font-weight: 500;
}

/* Stats bar */
.entry-stats {
  position: relative;
  margin-top: 10px;
  margin-bottom: 40px;
  z-index: 3;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-around;
  width: 92%;
  max-width: 500px;
  background: rgba(14, 21, 40, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 16px 12px;
}
.entry-stat {
  text-align: center;
  flex: 1;
}
.stat-val {
  display: block;
  font-weight: 800;
  font-size: 0.95rem;
  color: var(--indigo-light);
  margin-bottom: 2px;
}
.stat-lbl {
  font-size: 0.6rem;
  color: var(--text-muted);
  font-weight: 600;
  line-height: 1.2;
}

/* Dashboard */
.dash-scroll {
  width: 100%;
}

/* Profile Selection */
.profile-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--r-md);
  padding: 24px 16px;
  cursor: pointer;
  transition: all 0.2s var(--ease-spring);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
.profile-card:hover {
  transform: translateY(-4px) scale(1.02);
  border-color: var(--indigo);
  box-shadow: var(--indigo-glow);
}
.profile-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--indigo-light), var(--indigo));
  color: #fff;
  font-weight: 800;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.profile-name {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  text-align: center;
  word-break: break-all;
}

/* Transitions */
.portal-out-leave-active {
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}
.portal-out-leave-to {
  opacity: 0;
  transform: scale(1.04);
}
.dash-in-enter-active {
  transition:
    opacity 0.5s ease 0.2s,
    transform 0.5s var(--ease-out) 0.2s;
}
.dash-in-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
</style>
