<script setup>
import { computed } from 'vue'

const props = defineProps({
  gradient: {
    type: String,
    default: 'orange',
    validator: (value) => ['orange', 'purple', 'blue'].includes(value),
  },
  title: {
    type: String,
    default: 'Title',
  },
  desc: {
    type: String,
    default: 'Description',
  },
  suffixIcon: {
    type: String,
    default: '',
  },
})

const bannerClasses = computed(() => {
  const baseClasses =
    'w-full h-[70px] px-[16px] py-[12px] rounded-[6px] inline-flex justify-between items-center transition'

  if (props.gradient === 'orange') {
    return `${baseClasses} bg-[var(--color-accent-orange)]`
  } else if (props.gradient === 'purple') {
    return `${baseClasses} bg-gradient-to-r from-[#8441F9] to-[#DE53F7]`
  }

  return baseClasses
})
</script>

<template>
  <div :class="bannerClasses">
    <div class="inline-flex flex-col justify-start items-start text-white">
      <div class="text-small-medium">
        {{ props.title }}
      </div>
      <div class="text-micro-regular">
        {{ props.desc }}
      </div>
    </div>
    <img v-if="props.suffixIcon" :src="suffixIcon" class="object-contain w-[40px] h-[40px]" />
  </div>
</template>
