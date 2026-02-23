<template>
  <q-layout view="lHh lpr lFf">
    <!-- Persistent 3D Background -->
    <VantaBackground />

    <!-- Tab Bar -->
    <q-footer class="aura-nav" style="padding-bottom: env(safe-area-inset-bottom)">
      <div class="row justify-around items-center q-py-xs">
        <div
          v-for="tab in tabs"
          :key="tab.name"
          class="nav-tab col-auto"
          :class="{ active: $route.name === tab.name }"
          @click="$router.push({ name: tab.name })"
        >
          <q-icon :name="$route.name === tab.name ? tab.iconFill : tab.icon" class="nav-icon" />
          <span>{{ $t(tab.label) }}</span>
        </div>
      </div>
      <!-- Project Credits -->
      <div
        style="
          text-align: center;
          color: rgba(255, 255, 255, 0.3);
          font-size: 0.6rem;
          padding: 4px 0 8px;
          font-family: 'JetBrains Mono', monospace;
          letter-spacing: 0.05em;
        "
      >
        {{ $t('created_by') }}
      </div>
    </q-footer>

    <q-page-container>
      <router-view v-slot="{ Component, route }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" :key="route.name" />
        </transition>
      </router-view>
    </q-page-container>

    <BackButton />
    <PanicButton />
    <CrisisModal />
  </q-layout>
</template>

<script setup>
import VantaBackground from 'src/components/VantaBackground.vue'
import BackButton from 'src/components/BackButton.vue'
import PanicButton from 'src/components/PanicButton.vue'
import CrisisModal from 'src/components/CrisisModal.vue'

const tabs = [
  { name: 'home', label: 'home', icon: 'home', iconFill: 'home' },
  { name: 'chat', label: 'aura', icon: 'chat_bubble_outline', iconFill: 'chat_bubble' },
  { name: 'journal', label: 'journal', icon: 'edit_note', iconFill: 'edit_note' },
  { name: 'wellness', label: 'wellness', icon: 'self_improvement', iconFill: 'self_improvement' },
  { name: 'settings', label: 'profile', icon: 'person_outline', iconFill: 'person' },
]
</script>

<style>
/* Modern Page Route Transitions */
.page-fade-enter-active {
  transition:
    opacity 0.4s ease,
    transform 0.5s cubic-bezier(0, 0, 0.2, 1);
}
.page-fade-leave-active {
  transition: opacity 0.25s ease;
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.page-fade-leave-to {
  opacity: 0;
}
</style>
