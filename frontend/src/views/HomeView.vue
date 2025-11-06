<script setup>
import DesktopHome from '@/components/DesktopHome.vue'
import MobileHome from '@/components/MobileHome.vue'
import { onMounted, ref } from 'vue'

const isMobile = ref(false)
const checkMobile = () => {
  isMobile.value = window.innerWidth < 640
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})
</script>

<template>
  <div class="w-full flex justify-center">
    <MobileHome v-if="isMobile" />
    <DesktopHome v-else />
  </div>
</template>

<style scoped></style>
