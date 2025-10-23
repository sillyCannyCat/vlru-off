<!-- App.vue -->
<template>
  <div style="padding: 20px">
    <h1>Test your components 🚀</h1>
    <Button @click="onClick">Click me</Button>
  </div>
</template>

<script setup>
const onClick = () => {
  console.log('clicked once ✅')
}
</script>
