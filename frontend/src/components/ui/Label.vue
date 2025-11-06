<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'outline',
    validator: (value) => ['outline', 'ghost', 'tip'].includes(value),
  },
})

const labelClasses = computed(() => {
  const baseClasses =
    'rounded-[6px] px-[8px] py-[2px] inline-flex justify-center items-center gap-[8px] transition'
  if (props.variant === 'outline') {
    return `${baseClasses} text-body-medium border-[1px] border-[var(--color-text-muted)] text-[var(--color-text-primary)] bg-[var(--color-backround-primary)]`
  } else if (props.variant === 'ghost') {
    return `${baseClasses} text-body-medium bg-[var(--color-background-secondary)] text-[var(--color-text-primary)]`
  } else if (props.variant === 'tip') {
    return `${baseClasses} text-small-medium bg-[var(--color-text-primary)] text-[var(--color-background-primary)]`
  }

  return baseClasses
})
</script>

<template>
  <div :class="labelClasses"><slot /></div>
</template>
