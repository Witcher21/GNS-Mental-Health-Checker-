<template>
  <router-view />
</template>

<script setup>
import { watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWellnessStore } from 'src/stores/wellnessStore'

const { locale } = useI18n()
const store = useWellnessStore()

watchEffect(() => {
  locale.value = store.appLanguage || 'en-US'
})
</script>
