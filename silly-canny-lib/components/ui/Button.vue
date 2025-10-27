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
  suffixIcon: {
    type: String,
    default: '',
  },
})

defineEmits(['click'])

const buttonClasses = computed(() => {
  const baseClasses =
    'text-[14px] leading-[20px] md:text-[16px] md:leading-[24px] rounded-[6px] py-[10px] md:py-[8px] inline-flex justify-center items-center gap-[6px] md:gap-[8px] cursor-pointer transition w-full md:w-auto min-h-[44px] md:min-h-0'

  if (props.variant === 'default') {
    return `${baseClasses} px-[12px] md:px-[16px] bg-[var(--color-text-primary)] text-white hover:bg-[var(--color-text-secondary)]`
  } else if (props.variant === 'outline') {
    return `${baseClasses} px-[12px] md:px-[16px] border-[1px] border-[var(--color-text-muted)] text-[var(--color-text-primary)] hover:bg-[var(--color-background-secondary)]`
  } else if (props.variant === 'link') {
    return `${baseClasses} underline text-[var(--color-text-primary)] px-0 min-h-0`
  }

  return baseClasses
})
</script>

<template>
  <component :is="as" :class="buttonClasses" @click="$emit('click', $event)">
    <slot />
    <img v-if="suffixIcon" :src="props.suffixIcon" class="w-[16px] h-[16px]" />
  </component>
</template>