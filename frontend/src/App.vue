<script setup>
import { onMounted } from 'vue'
import { initStoreActions } from './lib/initStoreActions'

onMounted(() => {
  initStoreActions()
})
</script>

<template>
  <router-view></router-view>
</template>
