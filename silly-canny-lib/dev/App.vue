<template>
  <div class="p-8 inline-flex flex-col gap-[16px]">
    <div class="inline-flex flex-col">
      <Button variant="link">Узнать больше</Button>
      <Button variant="outline">Узнать больше</Button>
      <Button>Узнать больше</Button>
    </div>
  </div>
  <Label>12.12</Label>
  <Label variant="ghost">12.12</Label>
  <StatsLabel :value="-12"></StatsLabel>
  <StatsLabel :value="12"></StatsLabel>
  <Input
    label="Заголовок"
    placeholder="Пример текста"
    prefixIcon="/icons/hot-water.svg"
  ></Input>
  <Input
    label="Заголовок"
    placeholder="Пример текста"
    suffixIcon="/icons/hot-water.svg"
  ></Input>

  <Tabs v-model="activeTab" :tabs="tabList" />
  <div v-if="activeTab == 'tab1'">SOSAL</div>
  <NotificationBanner variant="notifications" />

  <div class="px-[16px] py-[32px] max-w-4xl mx-auto">
    <BarChart :data="complaintData" index="time" class="w-full" />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('tab1')
const tabList = [
  { label: 'Tab1', value: 'tab1' },
  { label: 'Tab2', value: 'tab2' },
  { label: 'Tab3', value: 'tab3' },
]

const complaintData = [
  { time: '00:00', cold_water: 2, hot_water: 1, electricity: 1 },
  { time: '01:00', cold_water: 1, hot_water: 1, electricity: 1 },
  { time: '02:00', cold_water: 1, hot_water: 0, electricity: 1 },
  { time: '03:00', cold_water: 1, hot_water: 1, electricity: 0 },
  { time: '04:00', cold_water: 1, hot_water: 1, electricity: 1 },
  { time: '05:00', cold_water: 2, hot_water: 2, electricity: 1 },
  { time: '06:00', cold_water: 5, hot_water: 4, electricity: 2 },
  { time: '07:00', cold_water: 9, hot_water: 7, electricity: 3 },
  { time: '08:00', cold_water: 12, hot_water: 8, electricity: 3 },
  { time: '09:00', cold_water: 10, hot_water: 6, electricity: 3 },
  { time: '10:00', cold_water: 9, hot_water: 5, electricity: 2 },
  { time: '11:00', cold_water: 11, hot_water: 7, electricity: 3 },
  { time: '12:00', cold_water: 14, hot_water: 10, electricity: 4 },
  { time: '13:00', cold_water: 13, hot_water: 9, electricity: 3 },
  { time: '14:00', cold_water: 10, hot_water: 7, electricity: 2 },
  { time: '15:00', cold_water: 9, hot_water: 6, electricity: 2 },
  { time: '16:00', cold_water: 10, hot_water: 7, electricity: 3 },
  { time: '17:00', cold_water: 12, hot_water: 8, electricity: 4 },
  { time: '18:00', cold_water: 15, hot_water: 11, electricity: 6 },
  { time: '19:00', cold_water: 16, hot_water: 12, electricity: 7 },
  { time: '20:00', cold_water: 14, hot_water: 10, electricity: 6 },
  { time: '21:00', cold_water: 12, hot_water: 8, electricity: 5 },
  { time: '22:00', cold_water: 8, hot_water: 6, electricity: 3 },
  { time: '23:00', cold_water: 4, hot_water: 3, electricity: 2 },
]

import BarChart from '../components/ui/BarChart.vue'
import Button from '../components/ui/Button.vue'
import Input from '../components/ui/Input.vue'
import Label from '../components/ui/Label.vue'
import NotificationBanner from '../components/ui/NotificationBanner.vue'
import StatsLabel from '../components/ui/StatsLabel.vue'
import Tabs from '../components/ui/Tabs.vue'
</script>
