<template>
  <q-page class="page-root q-px-md q-pt-xl q-pb-xl">
    <div class="content-layer">
      <!-- Header -->
      <div class="q-mb-xl animate-in">
        <div class="section-label q-mb-sm">{{ $t('privacy_profile') }}</div>
        <h1 class="font-display" style="font-size: 2.8rem; color: var(--text-primary); margin: 0">
          {{ $t('settings_title') }} <span class="text-gradient">{{ $t('security_title') }}</span>
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
          <q-icon name="shield" size="12px" /> {{ $t('device_only_desc') }}
        </p>
      </div>

      <!-- User Info Card -->
      <div class="gradient-card q-pa-lg q-mb-xl animate-in delay-1 row items-center q-gutter-lg">
        <div class="avatar-wrap">
          <div class="avatar-ring" style="border-width: 2px; animation-duration: 8s" />
          <div
            class="avatar-core"
            style="font-size: 2rem; width: 64px; height: 64px; overflow: hidden"
          >
            <template v-if="wellnessStore.userAvatar">
              <img
                :src="wellnessStore.userAvatar"
                style="width: 100%; height: 100%; object-fit: cover"
              />
            </template>
            <template v-else>
              {{ userInitials }}
            </template>
          </div>
        </div>
        <div class="col">
          <q-input
            v-model="userName"
            :placeholder="$t('your_name')"
            borderless
            dense
            input-style="color:var(--text-primary);font-size:1.5rem;font-weight:700;font-family:'Plus Jakarta Sans',sans-serif;padding:0;"
            style="width: 100%; margin-bottom: 4px"
            hide-underline
          />
          <div style="font-size: 0.85rem; color: var(--text-secondary)">
            {{ $t('companion') }} {{ wellnessStore.companionLevel }}
          </div>
        </div>
        <button
          class="icon-btn"
          style="border-radius: 50%"
          :title="$t('edit_avatar')"
          @click="$refs.fileInput.click()"
        >
          <q-icon name="photo_camera" size="18px" />
        </button>
        <input
          type="file"
          ref="fileInput"
          style="display: none"
          accept="image/*"
          @change="handleFileUpload"
        />
      </div>

      <!-- Preferences -->
      <div class="section-label q-mb-sm animate-in delay-2">{{ $t('app_preferences') }}</div>
      <div class="glass-card q-mb-xl animate-in delay-3" style="overflow: hidden">
        <q-item clickable v-ripple class="q-pa-md">
          <q-item-section avatar>
            <div class="pf-icon"><q-icon name="dark_mode" size="20px" /></div>
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('theme') }}</q-item-label>
            <q-item-label caption>{{ $t('theme_desc') }}</q-item-label>
          </q-item-section>
          <q-item-section side><q-badge color="indigo" :label="$t('dark')" /></q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-ripple class="q-pa-md">
          <q-item-section avatar>
            <div class="pf-icon"><q-icon name="notifications_active" size="20px" /></div>
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('daily_reminder') }}</q-item-label>
            <q-item-label caption>{{ $t('notif_desc') }}</q-item-label>
          </q-item-section>
          <q-item-section side><q-toggle v-model="notifs" color="primary" /></q-item-section>
        </q-item>
      </div>

      <!-- Security & Data -->
      <div class="section-label q-mb-sm animate-in delay-4">{{ $t('data_autonomy') }}</div>
      <div class="glass-card q-mb-xl animate-in delay-5" style="overflow: hidden">
        <q-item clickable v-ripple class="q-pa-md" @click="toggleLanguage">
          <q-item-section avatar>
            <div class="pf-icon" style="background: var(--mint-muted); color: var(--mint)">
              <q-icon name="translate" size="20px" />
            </div>
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('language') }}</q-item-label>
            <q-item-label caption>{{ $t('language_desc') }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-ripple class="q-pa-md" @click="logoutProfile">
          <q-item-section avatar>
            <div
              class="pf-icon"
              style="background: rgba(255, 255, 255, 0.05); color: var(--text-secondary)"
            >
              <q-icon name="logout" size="20px" />
            </div>
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('log_out') }}</q-item-label>
            <q-item-label caption>{{ $t('log_out_desc') }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-ripple class="q-pa-md" @click="exportData">
          <q-item-section avatar>
            <div
              class="pf-icon"
              style="background: var(--indigo-muted); color: var(--indigo-light)"
            >
              <q-icon name="download" size="20px" />
            </div>
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('export_data') }}</q-item-label>
            <q-item-label caption>{{ $t('export_desc') }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-ripple class="q-pa-md" @click="confirmDeleteDialog = true">
          <q-item-section avatar>
            <div class="pf-icon" style="background: var(--danger-muted); color: var(--danger)">
              <q-icon name="delete_forever" size="20px" />
            </div>
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-danger" style="font-weight: 700">{{
              $t('erase_account')
            }}</q-item-label>
            <q-item-label caption>{{ $t('erase_desc') }}</q-item-label>
          </q-item-section>
        </q-item>
      </div>

      <!-- Zero-Knowledge Guarantee -->
      <div
        class="q-pa-lg text-center animate-in delay-6"
        style="border: 1px dashed var(--border-mid); border-radius: var(--r-lg)"
      >
        <q-icon
          name="verified_user"
          size="32px"
          color="primary"
          class="q-mb-sm"
          style="filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.5))"
        />
        <div
          class="font-heading"
          style="color: var(--indigo-light); font-size: 1.1rem; margin-bottom: 8px"
        >
          {{ $t('zero_knowledge') }}
        </div>
        <p style="color: var(--text-muted); font-size: 0.8rem; line-height: 1.6; margin: 0">
          {{ $t('zero_knowledge_desc') }}
        </p>
      </div>

      <!-- Footer gap -->
      <div style="height: 40px" />
    </div>

    <!-- Erase Dialog -->
    <q-dialog v-model="confirmDeleteDialog">
      <q-card class="q-pa-xl" style="width: 100%; max-width: 440px">
        <div class="row items-center q-gutter-sm q-mb-md">
          <q-icon name="warning" color="negative" size="32px" />
          <div class="font-display" style="font-size: 1.5rem; color: var(--danger)">
            {{ $t('nuclear_option') }}
          </div>
        </div>
        <p style="color: var(--text-primary); font-weight: 600; margin-bottom: 8px">
          {{ $t('are_you_sure') }}
        </p>
        <p
          style="
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 24px;
          "
        >
          {{ $t('wipe_desc') }}
          <strong style="color: var(--danger)">{{ $t('cannot_undone') }}</strong>
        </p>
        <div class="row q-gutter-md">
          <button class="btn-ghost col" @click="confirmDeleteDialog = false">
            {{ $t('cancel') }}
          </button>
          <button
            class="btn-danger col"
            style="background: var(--danger); color: #fff"
            @click="executeDataWipe"
          >
            {{ $t('erase_account') }}
          </button>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useI18n } from 'vue-i18n'
import { useWellnessStore } from 'src/stores/wellnessStore'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const $q = useQuasar()
const router = useRouter()
const wellnessStore = useWellnessStore()

const userName = computed({
  get: () => wellnessStore.userName || t('no_name'),
  set: (val) => wellnessStore.updateUser(val, wellnessStore.userAge),
})

const userInitials = computed(() => {
  return (userName.value || 'JD').substring(0, 2).toUpperCase()
})

const fileInput = ref(null)

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      wellnessStore.setAvatar(e.target.result)
      $q.notify({
        message: t('avatar_updated'),
        color: 'positive',
        position: 'top',
      })
    }
    reader.readAsDataURL(file)
  }
}

const notifs = ref(true)
const confirmDeleteDialog = ref(false)

function toggleLanguage() {
  wellnessStore.appLanguage = wellnessStore.appLanguage === 'en-US' ? 'si-LK' : 'en-US'
  $q.notify({
    message: wellnessStore.appLanguage === 'en-US' ? t('lang_changed_en') : t('lang_changed_si'),
    color: 'positive',
    position: 'top',
  })
}

function exportData() {
  const data = {
    wellness: JSON.parse(localStorage.getItem('aura-store-wellness') || '{}'),
    chat: JSON.parse(localStorage.getItem('aura-store-chat') || '{}'),
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `Aura_Therapy_Export_${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)

  $q.notify({
    message: t('export_success'),
    color: 'positive',
    position: 'top',
  })
}

function logoutProfile() {
  localStorage.removeItem('aura-active-profile-id')
  sessionStorage.removeItem('aura-skip-intro')
  $q.notify({ message: t('logout_success'), color: 'positive', position: 'top' })
  router.push('/')
  setTimeout(() => window.location.reload(), 300)
}

function executeDataWipe() {
  const currentId = localStorage.getItem('aura-active-profile-id')

  if (currentId && currentId !== 'GUEST-VOLATILE') {
    let profiles = JSON.parse(localStorage.getItem('aura-profiles') || '[]')
    profiles = profiles.filter((p) => p.id !== currentId)
    localStorage.setItem('aura-profiles', JSON.stringify(profiles))

    localStorage.removeItem(`aura-store-wellness-${currentId}`)
    localStorage.removeItem(`aura-store-chat-${currentId}`)
  }

  // NUKE EVERY CONCEIVABLE GHOST KEY
  // (Fixes old versions getting stuck in cache)
  const ghostKeys = [
    'aura-store-wellness-default',
    'aura-store-chat-default',
    'aura-store-wellness-GUEST-VOLATILE',
    'aura-store-chat-GUEST-VOLATILE',
    'wellness-store',
    'chat-store',
    'wellness',
    'chat',
  ]
  ghostKeys.forEach((k) => localStorage.removeItem(k))

  localStorage.removeItem('aura-active-profile-id')

  confirmDeleteDialog.value = false
  $q.notify({
    message: t('erase_acc_confirm'),
    color: 'negative',
    position: 'top',
    icon: 'delete',
  })

  sessionStorage.removeItem('aura-skip-intro')
  router.push('/')
  setTimeout(() => window.location.reload(), 300)
}
</script>

<style scoped>
.pf-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--r-sm);
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.avatar-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.avatar-ring {
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  border: 1px solid var(--border-strong);
  animation: spin-slow 10s linear infinite;
}
.avatar-core {
  border-radius: 50%;
  background: var(--grad-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 24px rgba(99, 102, 241, 0.5);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
}
</style>
