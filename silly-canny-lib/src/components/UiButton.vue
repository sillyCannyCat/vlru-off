<template>
  <button class="my-button" @click="$emit('click')">
    <slot />
  </button>
</template>

<style>
.my-button {
  background: #42b883;
  border: none;
  color: white;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.my-button:hover {
  background: #2a7d63;
}
</style>
