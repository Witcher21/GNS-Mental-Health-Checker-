<template>
  <q-page class="page-root q-px-md q-pt-xl q-pb-xl">
    <div class="content-layer">
      <!-- Header -->
      <div class="q-mb-xl animate-in">
        <div class="section-label q-mb-sm">{{ $t('private_space') }}</div>
        <h1 class="font-display" style="font-size: 2.8rem; color: var(--text-primary); margin: 0">
          Field <span class="text-gradient-warm">{{ $t('journal') }}</span>
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
          <q-icon name="lock" size="12px" /> {{ $t('eyes_only') }}
        </p>
      </div>

      <!-- New Entry Card -->
      <div class="gradient-card q-pa-lg q-mb-xl animate-in delay-1">
        <div class="row justify-between items-center q-mb-md">
          <div class="font-heading" style="font-size: 1.1rem; color: var(--indigo-light)">
            {{ $t('new_entry') }}
          </div>
          <div class="badge-indigo">{{ todayStr }}</div>
        </div>

        <!-- Mood Selector -->
        <div class="text-caption q-mb-sm">{{ $t('feeling_msg') }}</div>
        <div class="row q-gutter-xs justify-between q-mb-lg">
          <button
            v-for="m in moods"
            :key="m.emoji"
            class="mood-btn"
            :class="{ active: newEntry.mood?.emoji === m.emoji }"
            @click="newEntry.mood = m"
            :title="m.label"
          >
            <span style="font-size: 1.6rem">{{ m.emoji }}</span>
          </button>
        </div>

        <!-- Tag Selector -->
        <div class="text-caption q-mb-sm">{{ $t('occupying_mind') }}</div>
        <div class="row q-gutter-sm q-mb-lg" style="flex-wrap: wrap">
          <button
            v-for="tag in availableTags"
            :key="tag"
            class="chip"
            :class="{ active: newEntry.tags.includes(tag) }"
            @click="toggleTag(tag)"
          >
            {{ $t('tags.' + tag.toLowerCase()) }}
          </button>
        </div>

        <!-- Text Area -->
        <textarea
          v-model="newEntry.content"
          :placeholder="$t('write_freely')"
          rows="4"
          class="journal-input q-mb-md"
        />

        <button
          class="btn-primary"
          style="width: 100%"
          :style="{ opacity: !newEntry.content.trim() ? 0.5 : 1 }"
          :disabled="!newEntry.content.trim()"
          @click="saveEntry"
        >
          {{ $t('save_log') }}
        </button>
      </div>

      <!-- NLP Insight (Simulated) -->
      <transition name="fade">
        <div v-if="lastInsight" class="insight-card q-pa-md q-mb-xl animate-in-scale">
          <div class="row items-center q-gutter-sm q-mb-xs">
            <q-icon name="auto_awesome" color="primary" size="20px" />
            <span class="font-heading" style="color: var(--indigo-light)">{{
              $t('aura_insight')
            }}</span>
          </div>
          <div
            style="
              font-size: 0.9rem;
              line-height: 1.6;
              color: var(--text-secondary);
              margin-top: 8px;
            "
          >
            {{ lastInsight }}
          </div>
        </div>
      </transition>

      <!-- Past Entries -->
      <div class="section-label q-mb-md animate-in delay-2">
        {{ $t('past_entries') }} ({{ entries.length }})
      </div>

      <div v-if="!entries.length" class="text-center q-py-xl animate-in delay-3">
        <div style="font-size: 3rem; opacity: 0.6; margin-bottom: 16px">📓</div>
        <div class="font-heading" style="color: var(--text-secondary)">{{ $t('no_entries') }}</div>
      </div>

      <div class="entry-list">
        <transition-group name="list">
          <div
            v-for="(entry, index) in reversedEntries"
            :key="entry.id"
            class="glass-card q-pa-md q-mb-sm list-item"
            :style="{ animationDelay: `${index * 0.05 + 0.3}s` }"
            @click="openDetail(entry)"
          >
            <div class="row justify-between items-start">
              <div class="row q-gutter-md">
                <div class="entry-emoji">{{ entry.mood?.emoji || '◈' }}</div>
                <div>
                  <div class="font-heading" style="color: var(--text-primary); font-size: 1rem">
                    {{ entry.dateLabel }}
                  </div>
                  <div class="row q-gutter-xs q-mt-xs">
                    <span
                      v-for="tag in entry.tags"
                      :key="tag"
                      class="badge-indigo"
                      style="font-size: 0.6rem; padding: 2px 6px"
                      >{{ tag }}</span
                    >
                  </div>
                </div>
              </div>
              <button
                class="icon-btn"
                style="width: 32px; height: 32px; border-color: transparent"
                @click.stop="deleteEntry(entry.id)"
              >
                <q-icon name="close" style="color: var(--danger)" size="16px" />
              </button>
            </div>
            <p class="entry-preview q-mt-md q-mb-0">{{ entry.content }}</p>
          </div>
        </transition-group>
      </div>
    </div>

    <!-- Detail Dialog -->
    <q-dialog
      v-model="detailOpen"
      maximized
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <div
        class="bg-base"
        style="min-height: 100vh; padding: 24px; position: relative; background: var(--bg-base)"
      >
        <!-- bg orbs -->
        <div
          class="orb orb-2"
          style="top: -100px; left: -100px; opacity: 0.3; pointer-events: none; position: absolute"
        />

        <div class="content-layer">
          <div class="row justify-between items-center q-mb-xl">
            <button class="icon-btn" @click="detailOpen = false">
              <q-icon name="arrow_back" size="20px" />
            </button>
            <div class="text-caption">E2E Encrypted</div>
          </div>

          <div style="font-size: 3.5rem; margin-bottom: 8px">
            {{ selectedEntry?.mood?.emoji || '◈' }}
          </div>
          <h2 class="font-display" style="font-size: 2rem; margin: 0 0 16px">
            {{ selectedEntry?.dateLabel }}
          </h2>

          <div class="row q-gutter-sm q-mb-xl">
            <span v-for="tag in selectedEntry?.tags" :key="tag" class="badge-indigo">{{
              $t('tags.' + tag.toLowerCase())
            }}</span>
          </div>

          <div class="detail-content">
            {{ selectedEntry?.content }}
          </div>
        </div>
      </div>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWellnessStore } from 'src/stores/wellnessStore'

const { t } = useI18n()
const wellnessStore = useWellnessStore()
const entries = computed(() => wellnessStore.journalEntries)
const detailOpen = ref(false)
const selectedEntry = ref(null)
const lastInsight = ref(null)

const todayStr = new Date().toLocaleDateString('en', {
  weekday: 'short',
  month: 'short',
  day: 'numeric',
})
const moods = [
  { emoji: '😔', label: 'Sad' },
  { emoji: '😰', label: 'Anxious' },
  { emoji: '😐', label: 'Neutral' },
  { emoji: '🙂', label: 'Good' },
  { emoji: '😊', label: 'Happy' },
]
const availableTags = ['work', 'family', 'health', 'social', 'finance', 'other']
const newEntry = reactive({ content: '', mood: null, tags: [] })

const reversedEntries = computed(() => [...entries.value].reverse())

function toggleTag(t) {
  const i = newEntry.tags.indexOf(t)
  if (i === -1) newEntry.tags.push(t)
  else newEntry.tags.splice(i, 1)
}

function saveEntry() {
  const id = Date.now()
  wellnessStore.journalEntries.push({
    id,
    content: newEntry.content,
    mood: newEntry.mood ? { ...newEntry.mood } : null,
    tags: [...newEntry.tags],
    dateLabel: todayStr,
    timestamp: new Date().toISOString(),
    language: t('language_code') === 'si-LK' ? 'si' : 'en',
  })

  // Basic NLP simulation insight
  const lower = newEntry.content.toLowerCase()

  // Keywords for stress/anxiety
  const stressKeys = [
    'stress',
    'overwhelm',
    'tired',
    'anxious',
    'sad',
    'bad',
    'panic',
    'පීඩනය',
    'කලබල',
    'බය',
    'දුක',
    'එපා',
  ]
  // Keywords for positive
  const joyKeys = [
    'happy',
    'grateful',
    'great',
    'good',
    'joy',
    'wonderful',
    'සතුටු',
    'යහපත්',
    'හොඳ',
    'ගොඩක්',
  ]

  if (stressKeys.some((k) => lower.includes(k))) {
    lastInsight.value = t('insight_stressed')
  } else if (joyKeys.some((k) => lower.includes(k))) {
    lastInsight.value = t('insight_positive')
  } else {
    lastInsight.value = null
  }

  // reset form
  newEntry.content = ''
  newEntry.mood = null
  newEntry.tags = []
}

function deleteEntry(id) {
  wellnessStore.journalEntries = wellnessStore.journalEntries.filter((e) => e.id !== id)
}
function openDetail(e) {
  selectedEntry.value = e
  detailOpen.value = true
}
</script>

<style scoped>
.mood-btn {
  width: 54px;
  height: 54px;
  border-radius: var(--r-md);
  border: 1px solid var(--border-subtle);
  background: var(--bg-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s var(--ease-spring);
  &:hover {
    background: rgba(255, 255, 255, 0.05);
    transform: translateY(-2px);
  }
  &.active {
    background: var(--indigo-muted);
    border-color: var(--indigo);
    transform: scale(1.1);
    box-shadow: var(--indigo-glow);
  }
}

.journal-input {
  width: 100%;
  padding: 16px;
  background: rgba(7, 11, 20, 0.4);
  border: 1px solid var(--border-subtle);
  border-radius: var(--r-md);
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  transition: all 0.2s;
  &:focus {
    border-color: var(--indigo);
    box-shadow: 0 0 0 3px var(--indigo-muted);
    background: rgba(7, 11, 20, 0.7);
  }
}

.insight-card {
  background: linear-gradient(145deg, rgba(99, 102, 241, 0.08), rgba(139, 92, 246, 0.03));
  border: 1px solid var(--border-mid);
  border-left: 3px solid var(--indigo);
  border-radius: var(--r-md);
}

.entry-emoji {
  width: 44px;
  height: 44px;
  border-radius: var(--r-md);
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
}

.entry-preview {
  color: var(--text-secondary);
  font-size: 0.88rem;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.detail-content {
  color: var(--text-primary);
  font-size: 1rem;
  line-height: 1.8;
  font-family: 'Inter', sans-serif;
  white-space: pre-wrap;
}

/* List Transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s var(--ease-spring);
}
.list-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
.list-item {
  cursor: pointer;
  animation: fade-in-up 0.4s var(--ease-out) both;
}
</style>
