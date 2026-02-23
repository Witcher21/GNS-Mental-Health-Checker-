import { defineStore } from '#q-app/wrappers'
import { createPinia } from 'pinia'

export default defineStore((/* { ssrContext } */) => {
  const pinia = createPinia()

  // Custom LocalStorage Persistence Plugin
  pinia.use(({ store, options }) => {
    if (options.persist) {
      const activeProfileId = localStorage.getItem('aura-active-profile-id') || 'GUEST-VOLATILE'
      const key = `aura-store-${store.$id}-${activeProfileId}`
      const saved = localStorage.getItem(key)
      if (saved) {
        // Restore state perfectly
        store.$patch(JSON.parse(saved))
      }

      // Auto-save on every state change
      store.$subscribe(
        (mutation, state) => {
          if (localStorage.getItem('aura-active-profile-id')) {
            localStorage.setItem(key, JSON.stringify(state))
          }
        },
        { detached: true },
      )
    }
  })

  return pinia
})
