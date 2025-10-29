<script setup>
import { ref } from 'vue'
import BarChart from './ui/BarChart.vue'
import Button from './ui/Button.vue'
import Tabs from './ui/Tabs.vue'

const { complaintsData24h, complaintsData60m } = defineProps({
  complaintsData24h: { type: Array, required: true },
  complaintsData60m: { type: Array, required: true },
})

const graphTabs = [
  { value: '24h', label: '24 часа' },
  { value: '60m', label: '60 минут' },
]
const selectedGraphTabs = ref(graphTabs[0].value)
</script>

<template>
  <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
    <div class="self-stretch inline-flex justify-between items-center">
      <Tabs v-model="selectedGraphTabs" :tabs="graphTabs"></Tabs>
      <Button variant="outline">Подробнее</Button>
    </div>

    <BarChart
      :data="selectedGraphTabs === '24h' ? complaintsData24h : complaintsData60m"
      index="time"
    />
    <div
      v-if="selectedGraphTabs === '24h'"
      class="self-stretch inline-flex justify-between items-center text-micro-regular w-full"
    >
      <span>00:00</span>
      <span>08:00</span>
      <span>16:00</span>
      <span>23:00</span>
    </div>
    <div
      v-else
      class="self-stretch inline-flex justify-between items-center text-micro-regular w-full"
    >
      <span>{{ complaintsData60m[0].time }}</span>
      <span>{{ complaintsData60m[complaintsData60m.length - 1].time }}</span>
    </div>

    <div
      class="self-stretch inline-flex justify-center items-start gap-[8px] flex-wrap content-start"
    >
      <!-- Cold water -->
      <div class="inline-flex justify-start items-center gap-[4px]">
        <div class="w-4 h-4 bg-[var(--color-accent-blue)] rounded-[6px]"></div>
        <span class="text-micro-regular">Холодная вода</span>
      </div>
      <!-- Hot water -->
      <div class="inline-flex justify-start items-center gap-[4px]">
        <div class="w-4 h-4 bg-[var(--color-accent-orange)] rounded-[6px]"></div>
        <span class="text-micro-regular">Горячая вода</span>
      </div>
      <!-- Electricity -->
      <div class="inline-flex justify-start items-center gap-[4px]">
        <div class="w-4 h-4 bg-[var(--color-accent-purple)] rounded-[6px]"></div>
        <span class="text-micro-regular">Электроэнергия</span>
      </div>
    </div>
  </div>
</template>
