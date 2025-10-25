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
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('tab1')
const tabList = [
  { label: 'Tab1', value: 'tab1' },
  { label: 'Tab2', value: 'tab2' },
  { label: 'Tab3', value: 'tab3' },
]

import Button from '../components/ui/Button.vue'
import Input from '../components/ui/Input.vue'
import Label from '../components/ui/Label.vue'
import StatsLabel from '../components/ui/StatsLabel.vue'
import Tabs from '../components/ui/Tabs.vue'
</script>
