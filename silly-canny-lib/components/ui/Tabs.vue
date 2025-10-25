<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  tabs: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const activeTab = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})
</script>

<template>
  <div class="inline-flex flex-col">
    <!-- Tab Headers -->
    <div
      class="flex p-[4px] rounded-[10px] bg-[var(--color-background-secondary)]"
    >
      <button
        v-for="tab in tabs"
        :key="tab.value"
        :class="[
          'px-[16px] py-[8px] rounded-[6px] text-button-adaptive transition-colors',
          activeTab === tab.value
            ? 'bg-[var(--color-text-primary)] text-white cursor-default'
            : 'text-[var(--color-text-primary)] cursor-pointer',
        ]"
        @click="activeTab = tab.value"
      >
        {{ tab.label }}
      </button>
    </div>
  </div>
</template>
