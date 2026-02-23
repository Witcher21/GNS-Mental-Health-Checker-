<template>
  <teleport to="body">
    <transition name="crisis-fade">
      <div v-if="chatStore.crisisDetected" class="crisis-overlay">
        <div class="crisis-card q-pa-xl">
          <!-- Icon -->
          <div class="text-center q-mb-md">
            <div style="font-size: 3rem; margin-bottom: 8px">🆘</div>
            <div
              class="font-display"
              style="font-size: 2.8rem; color: var(--danger); line-height: 1"
            >
              {{ $t('crisis_header') }}
            </div>
            <div class="scanline-h" style="border-color: var(--danger); margin-top: 12px" />
          </div>

          <p
            class="q-mt-md"
            style="
              color: var(--text-secondary);
              font-family: 'Space Mono', monospace;
              font-size: 0.8rem;
              line-height: 1.8;
              text-align: center;
              margin-bottom: 20px;
            "
          >
            {{ $t('crisis_main_desc') }}
          </p>

          <!-- Hotlines -->
          <div class="q-gutter-xs q-mb-lg">
            <a
              v-for="line in hotlines"
              :key="line.number"
              :href="`tel:${line.number}`"
              class="hotline-row"
            >
              <div class="row items-center" style="gap: 12px">
                <span style="font-size: 1.4rem">{{ line.emoji }}</span>
                <div>
                  <div class="text-label" style="color: var(--text-secondary); font-size: 8px">
                    {{ $t(line.labelKey) }}
                  </div>
                  <div
                    class="font-display"
                    style="
                      color: var(--danger);
                      font-size: 1.4rem;
                      line-height: 1;
                      letter-spacing: 0.1em;
                    "
                  >
                    {{ line.number }}
                  </div>
                </div>
              </div>
            </a>
          </div>

          <!-- Grounding Tip -->
          <div
            class="q-pa-md q-mb-lg"
            style="
              border-left: 2px solid var(--neon);
              background: var(--neon-muted);
              border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
            "
          >
            <div class="text-label" style="color: var(--neon); margin-bottom: 4px">
              ◆ {{ $t('quick_grounding') }}
            </div>
            <div
              style="
                color: var(--text-secondary);
                font-size: 0.82rem;
                line-height: 1.7;
                font-family: 'Space Mono', monospace;
              "
            >
              {{ $t('grounding_breath_tip') }}
            </div>
          </div>

          <!-- Actions -->
          <div class="column" style="gap: 10px">
            <a
              href="tel:1333"
              class="btn-danger-neon"
              style="
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 14px;
                text-decoration: none;
                font-family: 'Space Mono', monospace;
                letter-spacing: 0.12em;
                border-radius: var(--radius-sm);
              "
              >📞 {{ $t('call_1333_now') }}</a
            >
            <button class="btn-ghost-neon" style="padding: 12px; width: 100%" @click="dismiss">
              {{ $t('i_am_safe') }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { useChatStore } from 'src/stores/chatStore'

const chatStore = useChatStore()

const hotlines = [
  { emoji: '🇱🇰', labelKey: 'sl_helpline', number: '1333' },
  { emoji: '🌍', labelKey: 'int_crisis', number: '116123' },
  { emoji: '🚨', labelKey: 'emergency_services', number: '119' },
]

function dismiss() {
  chatStore.dismissCrisis()
}
</script>

<style scoped>
.hotline-row {
  display: block;
  padding: 12px 16px;
  border: 1px solid rgba(255, 45, 85, 0.25);
  border-radius: var(--radius-sm);
  background: rgba(255, 45, 85, 0.06);
  text-decoration: none;
  transition:
    background 0.2s ease,
    box-shadow 0.2s ease;
  margin-bottom: 8px;
}
.hotline-row:hover {
  background: rgba(255, 45, 85, 0.12);
  box-shadow: 0 0 16px rgba(255, 45, 85, 0.2);
}
.crisis-fade-enter-active,
.crisis-fade-leave-active {
  transition: opacity 0.3s ease;
}
.crisis-fade-enter-from,
.crisis-fade-leave-to {
  opacity: 0;
}
</style>
