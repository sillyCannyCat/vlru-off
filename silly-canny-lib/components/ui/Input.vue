<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  prefixIcon: {
    type: String,
    default: '',
  },
  suffixIcon: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).slice(2, 11)}`,
  },
})

const emit = defineEmits(['update:modelValue'])

const onInput = (e) => {
  emit('update:modelValue', e.target.value)
}

const inputClasses = computed(() => {
  let baseClasses =
    'w-full text-body-regular px-[12px] py-[8px] rounded-[6px] border-[1px] border-[var(--color-text-muted)] placeholder-custom outline-none'
  const focus =
    'ring-inset focus:ring-[1.24px] focus:ring-offset-0 focus:ring-[var(--color-text-primary)]'

  if (props.prefixIcon) {
    baseClasses += ' pl-[40px]'
  }
  if (props.suffixIcon) {
    baseClasses += ' pr-[40px]'
  }
  return `${baseClasses} ${focus}`
})
</script>

<template>
  <div class="flex flex-col gap-[6px]">
    <!-- Label -->
    <label
      v-if="label"
      :for="id"
      class="text-small-medium text-[var(--color-text-primary)]"
    >
      {{ label }}
    </label>

    <!-- Input wrapper -->
    <div class="relative">
      <!-- Prefix icon -->
      <span
        v-if="prefixIcon"
        class="absolute left-[12px] top-1/2 -translate-y-1/2 text-[var(--color-text-muted)]"
      >
        <img :src="prefixIcon" class="w-[20px] h-[20px]" />
      </span>

      <!-- Input -->
      <input
        :id="id"
        :value="modelValue"
        :type="type"
        :placeholder="placeholder"
        :class="inputClasses"
        @input="onInput"
      />

      <!-- Suffix icon -->
      <span
        v-if="suffixIcon"
        class="absolute right-[12px] top-1/2 -translate-y-1/2 text-[var(--color-text-muted)]"
      >
        <img :src="suffixIcon" class="w-[20px] h-[20px]" />
      </span>
    </div>
  </div>
</template>

<style scoped>
.placeholder-custom::placeholder {
  color: #c0c0c0;
  opacity: 1;
}
</style>
