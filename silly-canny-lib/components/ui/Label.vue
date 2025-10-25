<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'outline',
    validator: (value) => ['outline', 'ghost'].includes(value),
  },
})

const labelClasses = computed(() => {
  const baseClasses =
    'text-body-medium rounded-[6px] px-[8px] py-[2px] inline-flex justify-center items-center gap-[8px] transition'
  if (props.variant === 'outline') {
    return `${baseClasses} border-[1px] border-[var(--color-text-muted)] text-[var(--color-text-primary)] bg-[var(--color-backround-primary)]`
  } else if (props.variant === 'ghost') {
    return `${baseClasses} bg-[var(--color-background-secondary)] text-[var(--color-text-primary)]`
  }

  return baseClasses
})
</script>

<template>
  <component :class="labelClasses"><slot /></component>
</template>
