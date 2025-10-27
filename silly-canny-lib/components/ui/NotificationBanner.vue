<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'counters',
    validator: (value) => ['counters', 'notifications'].includes(value),
  },
})

const bannerClasses = computed(() => {
  const baseClasses = 'self-stretch h-16 px-4 py-2 rounded-[6px] inline-flex justify-between items-center overflow-hidden transition'
  
  if (props.variant === 'counters') {
    return `${baseClasses} bg-gradient-to-r from-[var(--color-accent-orange)] to-[var(--color-accent-orange)]/70`
  } else if (props.variant === 'notifications') {
    return `${baseClasses} bg-gradient-to-r from-[var(--color-accent-purple)] to-[var(--color-accent-blue)]`
  }

  return baseClasses
})

const bannerContentClasses = computed(() => {
  return props.variant === 'notifications' 
    ? 'inline-flex justify-start items-center gap-[8px] flex-1'
    : 'inline-flex justify-between items-center flex-1'
})
</script>

<template>
  <div :class="bannerClasses">
    <div :class="bannerContentClasses">
      <div class="inline-flex flex-col justify-start items-start gap-[4px]">
        <div class="text-white text-base font-medium leading-5 font-[var(--font-family-sans)]">
          <slot name="title">
            {{ variant === 'counters' ? 'Не забудьте про счётчики!' : 'Не пропустите отключения!' }}
          </slot>
        </div>
        <div class="text-white text-xs font-normal leading-4 opacity-90 font-[var(--font-family-sans)]">
          <slot name="description">
            {{ variant === 'counters' ? 'Отправьте показания сейчас' : 'Подключите уведомления в Telegram' }}
          </slot>
        </div>
      </div>

      <div class="flex items-center">
        <div v-if="variant === 'counters'" class="w-12 h-12 relative overflow-hidden">
          <div class="w-8 h-8 left-[8px] top-[14.40px] absolute bg-white rounded-[2px]"></div>
          <div class="w-8 h-3.5 left-[8.88px] top-[24.80px] absolute bg-white rounded-[2px]"></div>
          <div class="w-10 h-10 left-[4.80px] top-[4.80px] absolute bg-white rounded-full"></div>
          <div class="w-8 h-2.5 left-[8px] top-[1.60px] absolute bg-white rounded-[2px]"></div>
        </div>

        <div v-if="variant === 'notifications'" class="w-10 h-10 relative overflow-hidden">
          <div class="w-10 h-8 left-0 top-[3.33px] absolute bg-white rounded-[2px]"></div>
        </div>
      </div>
    </div>
  </div>
</template>