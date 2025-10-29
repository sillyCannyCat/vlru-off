<script setup>
import declOfNum from '@/lib/declOfNum'
import Button from './ui/Button.vue'

const { byTypeOutages } = defineProps({
  byTypeOutages: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="self-stretch w-full inline-flex flex-col justify-start items-start">
    <div
      v-for="typeOutages in byTypeOutages"
      :key="typeOutages.id"
      :class="!(typeOutages.id % 2 === 0) ? 'bg-[var(--color-background-secondary)]' : ''"
      class="self-stretch h-[32px] inline-flex justify-between items-center"
    >
      <div class="inline-flex justify-start items-center gap-[8px]">
        <img :src="typeOutages.icon" class="w-[20px] h-[20px]" />
        <span class="text-small-regular">{{ typeOutages.title }}</span>
      </div>

      <Button variant="link">{{
        typeOutages.value > 0
          ? `${typeOutages.value} ${declOfNum(typeOutages.value, ['дом', 'дома', 'домов'])}`
          : 'нет отключений'
      }}</Button>
    </div>
    <!-- Heat -->
    <div class="self-stretch h-[8px]"></div>
    <div
      class="bg-[var(--color-background-secondary)] self-stretch h-[32px] inline-flex justify-between items-center"
    >
      <div class="inline-flex justify-start items-center gap-[8px]">
        <img src="/icons/heat.svg" class="w-[20px] h-[20px]" />
        <span class="text-small-regular">Отопление</span>
      </div>

      <Button variant="link">Узнать больше</Button>
    </div>
  </div>
</template>
