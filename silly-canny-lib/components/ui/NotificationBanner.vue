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
  const baseClasses =
    'w-full h-[70px] px-[16px] py-[12px] rounded-[6px] inline-flex justify-between items-center transition'

  if (props.variant === 'counters') {
    return `${baseClasses} bg-gradient-to-r from-[var(--color-accent-orange)] to-[var(--color-accent-orange)]/70`
  } else if (props.variant === 'notifications') {
    return `${baseClasses} bg-gradient-to-r from-[#8441F9] to-[#DE53F7]`
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
      <!-- Text -->
      <div class="inline-flex flex-col justify-start items-start gap-[4px]">
        <div class="text-body-medium text-white">
          <slot name="title">
            {{
              variant === 'counters'
                ? 'Не забудьте про счётчики!'
                : 'Не пропустите отключения!'
            }}
          </slot>
        </div>
        <div class="text-small-regular text-white opacity-90">
          <slot name="description">
            {{
              variant === 'counters'
                ? 'Отправьте показания сейчас'
                : 'Подключите уведомления в Telegram'
            }}
          </slot>
        </div>
      </div>
    </div>
    <!-- Icons -->
    <div class="flex items-center">
      <!-- Иконка счётчиков -->
      <div v-if="variant === 'counters'" class="w-12 h-12 relative">
        <img
          src="/icons/counter-icon.svg"
          alt="Счётчики"
          class="w-full h-full object-contain"
        />
      </div>

      <!-- Иконка Telegram -->
      <div v-else-if="variant === 'notifications'" class="w-10 h-10 relative">
        <img
          src="/icons/telegram-icon.svg"
          alt="Telegram"
          class="w-full h-full object-contain"
        />
      </div>
    </div>
  </div>
</template>
