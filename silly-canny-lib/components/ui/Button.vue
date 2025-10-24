<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'outline', 'link'].includes(value),
  },
  as: {
    type: String,
    default: 'button',
  },
})

defineEmits(['click'])

const buttonClasses = computed(() => {
  const baseClasses =
    'text-body-medium rounded-[6px] px-[16px] py-[8px] inline-flex justify-center items-center gap-[8px]'
  if (props.variant === 'default') {
    return `${baseClasses} bg-[var(--color-text-primary)] text-white hover:bg-[var(--color-text-secondary)]`
  }
  if (props.variant === 'outline') {
    return `${baseClasses} border-[1px] border-[var(--color-text-muted)] text-[var(--color-text-primary)] hover:bg-[color-mix(in srgb, var(--color-accent-orange), white 90%)]`
  }
  if (props.variant === 'link') {
    return `${baseClasses} underline underline-offset-2 text-[var(--color-accent-orange)] hover:text-[color-mix(in srgb, var(--color-accent-orange), black 20%)]`
  }

  return baseClasses
})
</script>

<template>
  <component :is="as" :class="buttonClasses" @click="$emit('click', $event)">
    <slot />
  </component>
</template>
