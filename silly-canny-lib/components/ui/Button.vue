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
    'text-button-adaptive rounded-[6px] py-[8px] inline-flex justify-center items-center gap-[8px] cursor-pointer transition'
  if (props.variant === 'default') {
    return `${baseClasses} px-[16px] bg-[var(--color-text-primary)] text-white hover:bg-[var(--color-text-secondary)]`
  } else if (props.variant === 'outline') {
    return `${baseClasses} px-[16px] border-[1px] border-[var(--color-text-muted)] text-[var(--color-text-primary)] hover:bg-[var(--color-background-secondary)]`
  } else if (props.variant === 'link') {
    return `${baseClasses} underline text-[var(--color-text-primary)]`
  }

  return baseClasses
})
</script>

<template>
  <component :is="as" :class="buttonClasses" @click="$emit('click', $event)">
    <slot />
  </component>
</template>
