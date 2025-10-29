<script setup>
import declOfNum from '@/lib/declOfNum'
import Button from './ui/Button.vue'

const { byOrgOutages, byOrgOutagesLen } = defineProps({
  byOrgOutages: {
    type: Array,
    required: true,
  },
  byOrgOutagesLen: {
    type: Number,
    required: true,
  },
})
</script>

<template>
  <div class="self-stretch w-full inline-flex flex-col justify-start items-start">
    <div
      v-if="byOrgOutages.length <= 4"
      class="self-stretch inline-flex flex-col justify-start items-start"
    >
      <div
        v-for="orgOutages in byOrgOutages"
        :key="orgOutages.id"
        :class="!(orgOutages.id % 2 === 0) ? 'bg-[var(--color-background-secondary)]' : ''"
        class="self-stretch h-[32px] inline-flex justify-between items-center"
      >
        <span class="text-small-regular">{{ orgOutages.name }}</span>
        <Button variant="link">{{
          `${orgOutages.value} ${declOfNum(orgOutages.value, ['дом', 'дома', 'домов'])}`
        }}</Button>
      </div>
    </div>
    <div v-else class="self-stretch inline-flex flex-col justify-start items-start">
      <div
        v-for="orgOutages in byOrgOutages.slice(0, 3)"
        :key="orgOutages.id"
        :class="!(orgOutages.id % 2 === 0) ? 'bg-[var(--color-background-secondary)]' : ''"
        class="self-stretch h-[32px] inline-flex justify-between items-center"
      >
        <span class="text-small-regular">{{ orgOutages.name }}</span>
        <Button variant="link">{{
          `${orgOutages.value} ${declOfNum(orgOutages.value, ['дом', 'дома', 'домов'])}`
        }}</Button>
      </div>
      <div class="self-stretch h-[8px]"></div>
      <div
        class="bg-[var(--color-background-secondary)] self-stretch h-[32px] inline-flex justify-between items-center"
      >
        <span class="text-small-regular">Ещё {{ byOrgOutagesLen }} организации</span>

        <Button variant="link">Узнать больше</Button>
      </div>
    </div>
  </div>
</template>
