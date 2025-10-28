<script setup>
import { ref } from 'vue'
import Button from './components/ui/Button.vue'
import Input from './components/ui/Input.vue'
import Label from './components/ui/Label.vue'
import StatsLabel from './components/ui/StatsLabel.vue'
import Tabs from './components/ui/Tabs.vue'
import declOfNum from './lib/declOfNum'

let isTypeOutages = ref(true)
const toggleOutages = () => {
  isTypeOutages.value = !isTypeOutages.value
}

const byTypeOutages = {
  coldWater: {
    id: 1,
    icon: '/icons/cold-water.svg',
    title: 'Холодная вода',
    value: 3,
  },
  hotWater: {
    id: 2,
    icon: '/icons/hot-water.svg',
    title: 'Горячая вода',
    value: 15,
  },
  electricity: {
    id: 3,
    icon: '/icons/electricity.svg',
    title: 'Электоэнергия',
    value: 100,
  },
}

const byOrgOutages = [
  { id: 1, name: 'МУПВ ВПЭС', value: 52 },
  { id: 2, name: 'КГУП «Приморский водоканал»', value: 22 },
  { id: 3, name: 'Управляющие компании', value: 11 },
]

const graphTabs = [
  { value: '24h', label: '24 часа' },
  { value: '60m', label: '60 минут' },
]
let selectedGraphTabs = ref(graphTabs[0].value)

const loginUser = () => {}
const plannedOutages = () => {}
const mapOutages = () => {}
</script>

<template>
  <div class="w-full px-[16px] py-[16px] inline-flex flex-col justify-start items-start gap-[24px]">
    <!-- Header -->
    <div class="self-stretch inline-flex justify-between items-center">
      <!-- Logo and title -->
      <div class="inline-flex justify-start items-center">
        <img src="/icons/vlru-logo.svg" class="w-[81px] h-[36px]" />
        <div class="inline-flex flex-col justify-center items-start">
          <p class="text-body-medium">Отключения</p>
          <span class="text-micro-regular">Владивосток</span>
        </div>
      </div>

      <Button @click="loginUser" suffixIcon="/icons/log-in.svg">Войти</Button>
    </div>

    <!-- Search bar -->
    <div class="self-stretch inline-flex flex-col justify-start items-start gap-[6px]">
      <Input prefixIcon="/icons/search.svg" placeholder="Информация по вашему адресу"></Input>
      <span class="text-micro-regular">Введите свой адрес, чтобы узнать об отключениях</span>
    </div>

    <!-- Overall -->
    <div class="self-stretch inline-flex flex-col justify-start items-start gap-[16px]">
      <!-- Stats -->
      <div class="self-stretch inline-flex flex-col justify-start items-start gap-[2px]">
        <div class="inline-flex justify-start items-center gap-1.5">
          <Label variant="outline">21.10</Label>
          <p class="text-h3-medium">Сегодня 1300 отключений</p>
        </div>
        <div class="inline-flex justify-start items-center gap-[8px]">
          <span class="text-small-regular">На 300 случаев больше, чем вчера</span>
          <StatsLabel :value="10" />
        </div>
      </div>

      <!-- Buttons -->
      <div class="self-stretch inline-flex justify-start items-start gap-[8px]">
        <Button @click="plannedOutages" class="w-full">Плановые (9)</Button>
        <Button @click="mapOutages" class="w-full">Карта отключений</Button>
      </div>
    </div>

    <!-- Outages today -->
    <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
      <!-- Title -->
      <div class="self-stretch inline-flex justify-between items-center">
        <p class="text-body-medium">Отключения сейчас</p>
        <Button @click="toggleOutages" variant="outline">{{
          isTypeOutages ? 'К организациям' : 'К типам'
        }}</Button>
      </div>

      <!-- By type -->
      <div v-if="isTypeOutages" class="self-stretch inline-flex flex-col justify-start items-start">
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
      <!-- By org -->
      <div v-else class="self-stretch inline-flex flex-col justify-start items-start">
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
    </div>

    <!-- By complaints -->
    <div class="self-stretch inline-flex flex-col justify-start items-start gap-[16px]">
      <!-- Title and summorized info -->
      <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
        <p class="text-body-medium">Отключения по жалобам</p>
        <span class="text-small-regular"
          ><span class="text-small-medium">Сводка по жалобам:</span> Жители сообщают о множественных
          отключениях горячей воды и света</span
        >
      </div>

      <!-- Graphs -->
      <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
        <div class="self-stretch inline-flex justify-between items-center">
          <Tabs v-model="selectedGraphTabs" :tabs="graphTabs"></Tabs>
          <Button variant="outline">Подробнее</Button>
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
            <span class="text-micro-regular">Электоэнергия</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
