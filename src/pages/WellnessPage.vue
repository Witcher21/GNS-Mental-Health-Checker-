<template>
  <q-page class="page-root q-px-md q-pt-xl q-pb-xl">
    <div class="content-layer">
      <!-- Header -->
      <div class="q-mb-xl animate-in">
        <div class="section-label q-mb-sm">{{ $t('growth_journey') }}</div>
        <h1 class="font-display" style="font-size: 2.8rem; color: var(--text-primary); margin: 0">
          Your <span class="text-gradient-mint">{{ $t('wellness') }}</span>
        </h1>
        <p
          class="text-caption"
          style="
            margin-top: 10px;
            text-transform: none;
            letter-spacing: 0;
            font-family: 'JetBrains Mono', monospace;
          "
        >
          {{ $t('companion_evolution') }}
        </p>
      </div>

      <!-- Companion Stage -->
      <div class="gradient-card q-pa-lg q-mb-xl animate-in delay-1" style="text-align: center">
        <div class="companion-wrap q-py-lg">
          <div
            class="companion-ring"
            style="border-style: dashed; border-width: 2px; animation-duration: 8s"
          />
          <div class="companion-ring-2" style="animation-direction: reverse" />
          <div class="companion-body" style="font-size: 5.5rem">{{ companionEmoji }}</div>
        </div>
        <div
          class="font-heading"
          style="font-size: 1.6rem; color: var(--text-primary); margin-top: 12px"
        >
          {{ $t('level') }} {{ wellnessStore.companionLevel }}
        </div>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin: 4px 0 20px">
          {{
            wellnessStore.companionLevel >= 10
              ? $t('companion_msg_full')
              : $t('companion_msg_daily')
          }}
        </p>

        <div class="row items-center q-gutter-md q-mb-md">
          <div
            class="col"
            style="
              text-align: right;
              font-size: 0.8rem;
              color: var(--text-secondary);
              font-weight: 600;
            "
          >
            {{ wellnessStore.companionXP }} XP
          </div>
          <div class="col-6">
            <div class="progress-bar progress-bar-mint">
              <div class="fill" :style="{ width: wellnessStore.companionProgress + '%' }" />
            </div>
          </div>
          <div class="col" style="text-align: left; font-size: 0.8rem; color: var(--text-muted)">
            {{ wellnessStore.companionXpToNext }} XP
          </div>
        </div>

        <div
          class="inline-block q-pa-sm"
          style="
            background: var(--bg-elevated);
            border-radius: var(--r-lg);
            border: 1px solid var(--border-subtle);
          "
        >
          <div class="row q-gutter-md items-center justify-center q-px-md">
            <div class="row items-center q-gutter-xs">
              <span style="font-size: 1.2rem">🔥</span>
              <span class="font-heading" style="color: var(--text-primary)"
                >{{ wellnessStore.streakDays }}
                <span style="font-size: 0.7rem; color: var(--text-muted)">{{
                  $t('days_caps')
                }}</span></span
              >
            </div>
            <div style="width: 1px; height: 24px; background: var(--border-subtle)" />
            <div class="row items-center q-gutter-xs">
              <span style="font-size: 1.2rem">📝</span>
              <span class="font-heading" style="color: var(--text-primary)"
                >{{ wellnessStore.checkIns.length }}
                <span style="font-size: 0.7rem; color: var(--text-muted)">{{
                  $t('logs_caps')
                }}</span></span
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Module Grid -->
      <div class="section-label q-mb-md animate-in delay-2">{{ $t('daily_practices') }}</div>

      <div class="row q-gutter-md q-mb-xl">
        <div
          v-for="(mod, i) in modules"
          :key="mod.title"
          class="glass-card col-12 col-md-6 q-pa-md row items-center q-gutter-md list-item"
          :style="{ animationDelay: `${i * 0.1 + 0.3}s` }"
        >
          <div
            class="mod-icon"
            :style="{
              background: `linear-gradient(135deg, ${mod.c1}, ${mod.c2})`,
              boxShadow: `0 4px 16px ${mod.c1}40`,
            }"
          >
            {{ mod.icon }}
          </div>
          <div class="col">
            <div class="font-heading" style="font-size: 1rem; color: var(--text-primary)">
              {{ $t(mod.titleKey) }}
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 2px">
              {{ $t(mod.descKey) }}
            </div>
          </div>
          <button
            class="icon-btn"
            style="border-radius: 50%; width: 36px; height: 36px"
            @click="startModule(mod.id)"
          >
            <q-icon name="play_arrow" size="20px" />
          </button>
        </div>
      </div>

      <!-- Trend Chart (Simulated visually) -->
      <div class="section-label q-mb-md animate-in delay-4">{{ $t('wellness_trend') }}</div>
      <div class="glass-card q-pa-xl q-mb-xl text-center animate-in delay-5">
        <div
          class="row justify-between items-end"
          style="
            height: 120px;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 10px;
            margin-bottom: 10px;
          "
        >
          <!-- Empty state if no data -->
          <div
            v-if="!wellnessStore.checkIns.length"
            class="absolute-center text-muted col-12"
            style="font-size: 0.85rem"
          >
            {{ $t('log_first') }}
          </div>

          <!-- Dynamic Bar Chart -->
          <div
            v-for="(entry, i) in weekStrip"
            v-else
            :key="i"
            class="col flex items-end justify-center"
            style="height: 100%"
          >
            <div
              v-if="entry"
              class="chart-bar"
              :style="{
                height: Math.max(10, entry.score) + '%',
                background:
                  entry.score < 40
                    ? 'var(--grad-warm)'
                    : entry.score < 65
                      ? 'var(--grad-amber)'
                      : 'var(--grad-mint)',
              }"
            />
            <div v-else class="chart-bar-empty" />
          </div>
        </div>
        <div class="row justify-between">
          <span
            v-for="(entry, i) in weekStrip"
            :key="'label-' + i"
            class="col text-caption"
            style="font-family: 'JetBrains Mono', monospace"
            >{{ dayLabel(i) }}</span
          >
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Box Breathing Modal -->
    <q-dialog
      v-model="breathDialog"
      maximized
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <div class="bg-base column flex-center" style="min-height: 100vh; position: relative">
        <div
          class="hex-btn q-ma-md"
          style="position: absolute; top: 0; right: 0"
          @click="breathDialog = false"
        >
          <q-icon name="close" />
        </div>
        <div class="text-center q-mb-xl">
          <div class="font-display" style="font-size: 2rem; color: var(--text-primary)">
            {{ $t('box_breathing') }}
          </div>
          <p style="color: var(--text-secondary)">
            {{ $t('breath_guide') }}
          </p>
        </div>

        <div class="breath-container">
          <div class="breath-circle" :class="breathPhase"></div>
          <div class="breath-text">{{ breathText }}</div>
        </div>

        <button class="btn-primary q-mt-xl" @click="toggleBreathing">
          {{ isBreathing ? $t('stop') : $t('start') }}
        </button>
      </div>
    </q-dialog>

    <!-- Body Scan Modal -->
    <q-dialog
      v-model="scanDialog"
      maximized
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <div
        class="bg-base column items-center"
        style="min-height: 100vh; position: relative; padding: 60px 20px"
      >
        <div
          class="hex-btn q-ma-md"
          style="position: absolute; top: 0; right: 0"
          @click="scanDialog = false"
        >
          <q-icon name="close" />
        </div>
        <div class="text-center q-mb-xl">
          <div class="font-display" style="font-size: 2rem; color: var(--text-primary)">
            {{ $t('body_scan') }}
          </div>
          <p style="color: var(--text-secondary)">{{ $t('scan_guide') }}</p>
        </div>

        <div class="glass-card q-pa-lg text-center" style="width: 100%; max-width: 400px">
          <div style="font-size: 4rem; margin-bottom: 20px">🧘</div>
          <div class="font-heading q-mb-md" style="font-size: 1.5rem; color: var(--indigo-light)">
            {{ scanText }}
          </div>
          <q-linear-progress :value="scanProgress" color="primary" class="q-mt-none" />

          <button class="btn-secondary full-width q-mt-lg" @click="startScan" v-if="!isScanning">
            {{ $t('begin_scan') }}
          </button>
        </div>
      </div>
    </q-dialog>

    <!-- Gratitude Box Modal -->
    <q-dialog
      v-model="gratitudeDialog"
      maximized
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <div
        class="bg-base column items-center"
        style="min-height: 100vh; position: relative; padding: 60px 20px"
      >
        <div
          class="hex-btn q-ma-md"
          style="position: absolute; top: 0; right: 0"
          @click="gratitudeDialog = false"
        >
          <q-icon name="close" />
        </div>
        <div class="text-center q-mb-xl">
          <div class="font-display" style="font-size: 2rem; color: var(--text-primary)">
            {{ $t('gratitude_box') }}
          </div>
          <p style="color: var(--text-secondary)">{{ $t('grat_guide') }}</p>
        </div>

        <div class="glass-card q-pa-lg" style="width: 100%; max-width: 400px">
          <div class="q-mb-md">
            <div class="text-caption q-mb-xs">{{ $t('grat_1') }}</div>
            <textarea v-model="gratitudeInputs[0]" class="journal-input" rows="2"></textarea>
          </div>
          <div class="q-mb-md">
            <div class="text-caption q-mb-xs">{{ $t('grat_2') }}</div>
            <textarea v-model="gratitudeInputs[1]" class="journal-input" rows="2"></textarea>
          </div>
          <div class="q-mb-lg">
            <div class="text-caption q-mb-xs">{{ $t('grat_3') }}</div>
            <textarea v-model="gratitudeInputs[2]" class="journal-input" rows="2"></textarea>
          </div>
          <button class="btn-primary full-width" @click="saveGratitude">{{ $t('save_xp') }}</button>
        </div>
      </div>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWellnessStore } from 'src/stores/wellnessStore'
import { useQuasar } from 'quasar'

const { t } = useI18n()
const wellnessStore = useWellnessStore()
const $q = useQuasar()

const companionEmoji = computed(() => {
  const lv = wellnessStore.companionLevel
  return lv >= 10 ? '🌟' : lv >= 7 ? '🦋' : lv >= 5 ? '🌸' : lv >= 3 ? '🌱' : '🥚'
})

const modules = [
  {
    id: 'breath',
    icon: '🌬️',
    titleKey: 'box_breathing',
    descKey: 'meditation_desc',
    c1: '#34D399',
    c2: '#059669',
  },
  {
    id: 'scan',
    icon: '🧘',
    titleKey: 'body_scan',
    descKey: 'breathing_desc',
    c1: '#8B5CF6',
    c2: '#6D28D9',
  },
  {
    id: 'gratitude',
    icon: '✍️',
    titleKey: 'gratitude_box',
    descKey: 'gratitude_desc',
    c1: '#FBBF24',
    c2: '#D97706',
  },
]

const weekStrip = computed(() => {
  const slots = []
  for (let i = 6; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    slots.push(wellnessStore.checkIns.find((c) => c.date === d.toISOString().split('T')[0]) || null)
  }
  return slots
})

function dayLabel(index) {
  const d = new Date()
  d.setDate(d.getDate() - (6 - index))
  return d.toLocaleDateString(t('language_code'), { weekday: 'short' }).slice(0, 1)
}

// Modal Ref State
const breathDialog = ref(false)
const scanDialog = ref(false)
const gratitudeDialog = ref(false)

function startModule(id) {
  if (id === 'breath') breathDialog.value = true
  if (id === 'scan') scanDialog.value = true
  if (id === 'gratitude') gratitudeDialog.value = true
}

// ── Box Breathing Logic ──
const isBreathing = ref(false)
const breathPhase = ref('inhale')
const breathText = ref(t('ready'))
let breathInterval = null

function toggleBreathing() {
  if (isBreathing.value) {
    clearInterval(breathInterval)
    isBreathing.value = false
    breathPhase.value = ''
    breathText.value = t('ready')
    return
  }
  isBreathing.value = true
  runBreathCycle()
  breathInterval = setInterval(runBreathCycle, 16000)
}

function runBreathCycle() {
  breathPhase.value = 'inhale'
  breathText.value = t('inhale')
  setTimeout(() => {
    breathPhase.value = 'hold1'
    breathText.value = t('hold')
    setTimeout(() => {
      breathPhase.value = 'exhale'
      breathText.value = t('exhale')
      setTimeout(() => {
        breathPhase.value = 'hold2'
        breathText.value = t('hold')
      }, 4000)
    }, 4000)
  }, 4000)
}

// ── Body Scan Logic ──
const isScanning = ref(false)
const scanProgress = ref(0)
const scanText = ref(t('comfort_pos'))
const scanStages = ['feet', 'legs', 'stomach', 'chest', 'arms', 'face', 'mind']
let scanTimer = null

function startScan() {
  isScanning.value = true
  let step = 0
  scanText.value = `${t('focus_on')} ${t(scanStages[step])}... ${t('relax_deeply')}`
  scanProgress.value = 0

  scanTimer = setInterval(() => {
    step++
    scanProgress.value = step / scanStages.length
    if (step >= scanStages.length) {
      clearInterval(scanTimer)
      scanText.value = t('scan_complete')
      isScanning.value = false
      setTimeout(() => {
        scanDialog.value = false
      }, 3000)
    } else {
      scanText.value = `${t('focus_on')} ${t(scanStages[step])}... ${t('relax_deeply')}`
    }
  }, 5000)
}

// ── Gratitude Box Logic ──
const gratitudeInputs = ref(['', '', ''])

function saveGratitude() {
  if (gratitudeInputs.value.every((v) => v.trim() === '')) {
    $q.notify({
      message: t('fill_one'),
      color: 'warning',
      position: 'top',
    })
    return
  }
  wellnessStore.gainXP(50)
  gratitudeInputs.value = ['', '', '']
  gratitudeDialog.value = false
  $q.notify({
    message: `${t('grat_saved')} ${t('xp_gained')}`,
    color: 'positive',
    position: 'top',
    icon: 'favorite',
  })
}
</script>

<style scoped>
.mod-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--r-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  color: #fff;
}

.chart-bar {
  width: 24px;
  border-radius: 4px 4px 0 0;
  box-shadow: 0 -4px 12px rgba(52, 211, 153, 0.3);
  animation: bar-grow 1s var(--ease-spring) both;
}
.chart-bar-empty {
  width: 24px;
  height: 4px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  margin-bottom: 2px;
}

@keyframes bar-grow {
  from {
    height: 0;
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.list-item {
  animation: fade-in-up 0.5s var(--ease-out) both;
  cursor: default;
}
.list-item:hover {
  transform: translateY(-3px);
}

/* Breathing UI */
.breath-container {
  width: 250px;
  height: 250px;
  border-radius: 50%;
  border: 4px solid var(--border-subtle);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 40px auto;
}
.breath-circle {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, var(--mint) 0%, transparent 70%);
  opacity: 0.3;
  transition: all 4s linear;
  transform: scale(0.3);
}
.breath-circle.inhale {
  transform: scale(1);
  opacity: 0.8;
}
.breath-circle.hold1 {
  transform: scale(1);
  opacity: 0.8;
}
.breath-circle.exhale {
  transform: scale(0.3);
  opacity: 0.2;
}
.breath-circle.hold2 {
  transform: scale(0.3);
  opacity: 0.2;
}

.breath-text {
  position: absolute;
  font-size: 1.5rem;
  color: #fff;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.journal-input {
  width: 100%;
  padding: 12px;
  background: rgba(7, 11, 20, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--r-md);
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
  resize: none;
  outline: none;
  transition: 0.2s;
}
.journal-input:focus {
  border-color: var(--indigo);
  box-shadow: 0 0 0 3px var(--indigo-muted);
}
</style>
