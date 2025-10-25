<!-- StatsLabel.vue -->
<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    required: true,
  },
})

const displayValue = computed(() => {
  if (props.value > 0) {
    return `+${props.value}%`
  } else if (props.value < 0) {
    return `${props.value}%`
  } else {
    return '0%'
  }
})

const labelClasses = computed(() => {
  let base =
    'text-body-medium rounded-[6px] px-[8px] py-[2px] inline-flex justify-center items-center gap-[8px]'

  if (props.value > 0) {
    return `${base} bg-[var(--сolor-status-success-bg)] text-[var(--color-status-success)]`
  } else if (props.value < 0) {
    return `${base} bg-[var(--color-status-destructive-bg)] text-[var(--color-status-destructive)]`
  } else {
    return `${base} bg-[var(--color-background-secondary)] text-[var(--color-text-primary)]`
  }
})
</script>

<template>
  <div :class="labelClasses">
    {{ displayValue }}
  </div>
</template>
