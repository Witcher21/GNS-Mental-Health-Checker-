<template>
  <!-- Global Back Button (Hidden on Home Page) -->
  <div v-if="$route.path !== '/'" class="back-btn" @click="goBack" title="Go Back">
    <div class="hover-ring"></div>
    <q-icon name="arrow_back" style="color: #fff; z-index: 2; position: relative" size="22px" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goBack() {
  if (window.history.length > 2) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.back-btn {
  position: fixed;
  top: 84px; /* Move below header to prevent overlap */
  left: 18px;
  z-index: 1000;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: rgba(10, 15, 30, 0.5); /* Glass base */
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
}

.hover-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition:
    width 0.4s ease-out,
    height 0.4s ease-out;
  z-index: 1;
}

.back-btn:hover {
  transform: scale(1.1);
  border-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.1);
}

.back-btn:hover .hover-ring {
  width: 150%;
  height: 150%;
}

.back-btn:active {
  transform: scale(0.9);
}
</style>
