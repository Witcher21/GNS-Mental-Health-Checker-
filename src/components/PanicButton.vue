<template>
  <!-- Floating Panic Button (Hidden on Home Page) -->
  <div v-if="$route.path !== '/'" class="panic-btn" @click="trigger" :title="$t('panic_protocol')">
    <q-icon name="favorite" class="panic-icon" size="22px" />
  </div>

  <!-- Grounding Dialog -->
  <q-dialog
    v-model="open"
    persistent
    maximized
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <div
      style="background: var(--bg-void); overflow-y: auto; min-height: 100vh; position: relative"
    >
      <!-- Particles -->
      <div class="bg-atmosphere"><div class="particle-field" /></div>

      <!-- Close -->
      <div
        class="hex-btn content-layer q-ma-md"
        style="
          position: absolute;
          top: 0;
          right: 0;
          width: 40px;
          height: 40px;
          z-index: 9999;
          cursor: pointer;
        "
        @click="close"
      >
        <q-icon name="close" size="14px" />
      </div>

      <div
        class="content-layer column items-center justify-center"
        style="min-height: 100vh; padding: 32px 24px"
      >
        <!-- Title -->
        <div class="text-center q-mb-xl animate-fade-up">
          <div style="font-size: 2.5rem; margin-bottom: 8px">🌬️</div>
          <div class="font-display" style="font-size: 3.5rem; color: var(--text-primary)">
            {{ $t('you_are_safe_part1', 'YOU ARE') }}
            <span style="color: var(--neon)">{{ $t('you_are_safe_part2', 'SAFE') }}</span>
          </div>
          <div class="scanline-h q-mt-sm q-mb-md" />
          <p class="text-label" style="color: var(--text-secondary); letter-spacing: 0.15em">
            {{ $t('grounding_desc') }}
          </p>
        </div>

        <!-- Step Card -->
        <div
          class="glass-card animate-fade-up"
          style="
            width: 100%;
            max-width: 400px;
            padding: 32px;
            text-align: center;
            margin-bottom: 32px;
          "
        >
          <div style="font-size: 3.5rem; margin-bottom: 16px">{{ steps[currentStep].emoji }}</div>
          <div
            class="font-display"
            style="
              font-size: 5rem;
              color: var(--neon);
              line-height: 1;
              margin-bottom: 8px;
              text-shadow: 0 0 30px rgba(45, 248, 114, 0.5);
            "
          >
            {{ steps[currentStep].count }}
          </div>
          <div
            style="
              font-weight: 700;
              color: var(--text-primary);
              font-size: 1rem;
              text-transform: uppercase;
              letter-spacing: 0.1em;
              margin-bottom: 10px;
            "
          >
            {{ $t(steps[currentStep].senseKey) }}
          </div>
          <p style="color: var(--text-secondary); font-size: 0.88rem; line-height: 1.7">
            {{ $t(steps[currentStep].instructionKey) }}
          </p>
        </div>

        <!-- Step Dots -->
        <div class="row q-gutter-sm q-mb-xl">
          <div
            v-for="(step, i) in steps"
            :key="i"
            :style="{
              width: i === currentStep ? '24px' : '8px',
              height: '8px',
              borderRadius: '4px',
              background: i <= currentStep ? 'var(--neon)' : 'var(--border-card)',
              boxShadow: i <= currentStep ? '0 0 8px var(--neon)' : 'none',
              transition: 'all 0.3s ease',
            }"
          />
        </div>

        <!-- Controls -->
        <div class="row q-gutter-md">
          <button
            v-if="currentStep > 0"
            class="btn-ghost-neon"
            style="min-width: 100px; padding: 12px"
            @click="currentStep--"
          >
            ← {{ $t('back_caps') }}
          </button>
          <button
            v-if="currentStep < steps.length - 1"
            class="btn-neon-solid"
            style="min-width: 180px; padding: 12px; font-size: 0.7rem"
            @click="currentStep++"
          >
            {{ $t('next_caps') }} — {{ $t(steps[currentStep + 1].senseKey) }} →
          </button>
          <button
            v-else
            class="btn-neon-solid"
            style="min-width: 180px; padding: 12px; font-size: 0.7rem"
            @click="close"
          >
            {{ $t('protocol_complete') }}
          </button>
        </div>

        <!-- Helpline -->
        <div class="q-mt-xl text-center">
          <div class="text-label q-mb-sm" style="color: var(--text-muted)">
            {{ $t('still_overwhelmed') }}
          </div>
          <a
            href="tel:1333"
            style="
              color: var(--danger);
              font-family: 'Space Mono', monospace;
              font-weight: 700;
              letter-spacing: 0.1em;
              text-decoration: none;
              font-size: 1rem;
            "
          >
            📞 1333 · {{ $t('crisis_helpline_label') }}
          </a>
        </div>
      </div>
    </div>
  </q-dialog>
</template>

<script setup>
import { ref } from 'vue'

const open = ref(false)
const currentStep = ref(0)

const steps = [
  {
    count: '5',
    senseKey: 'sense_see',
    emoji: '👁️',
    instructionKey: 'see_desc',
  },
  {
    count: '4',
    senseKey: 'sense_touch',
    emoji: '🤲',
    instructionKey: 'touch_desc',
  },
  {
    count: '3',
    senseKey: 'sense_hear',
    emoji: '👂',
    instructionKey: 'hear_desc',
  },
  {
    count: '2',
    senseKey: 'sense_smell',
    emoji: '👃',
    instructionKey: 'smell_desc',
  },
  {
    count: '1',
    senseKey: 'sense_taste',
    emoji: '👅',
    instructionKey: 'taste_desc',
  },
]

function trigger() {
  currentStep.value = 0
  open.value = true
}
function close() {
  open.value = false
}
</script>
