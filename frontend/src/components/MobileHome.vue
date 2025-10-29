<script setup>
import declOfNum from '@/lib/declOfNum'
import { ref } from 'vue'
import ComplaintsBlock from './ComplaintsGraphBlock.vue'
import Button from './ui/Button.vue'
import Input from './ui/Input.vue'
import Label from './ui/Label.vue'
import StatsLabel from './ui/StatsLabel.vue'

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
  { id: 4, name: 'Управляющие компании', value: 11 },
  { id: 5, name: 'Управляющие компании', value: 11 },
]
const byOrgOutagesLen = byOrgOutages.length - 3

const complaintData24h = [
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

const complaintData60m = [
  { time: '12:00', cold_water: 14, hot_water: 10, electricity: 4 },
  { time: '12:05', cold_water: 13, hot_water: 9, electricity: 4 },
  { time: '12:10', cold_water: 15, hot_water: 11, electricity: 5 },
  { time: '12:15', cold_water: 12, hot_water: 8, electricity: 3 },
  { time: '12:20', cold_water: 14, hot_water: 10, electricity: 4 },
  { time: '12:25', cold_water: 16, hot_water: 12, electricity: 5 },
  { time: '12:30', cold_water: 13, hot_water: 9, electricity: 4 },
  { time: '12:35', cold_water: 11, hot_water: 7, electricity: 3 },
  { time: '12:40', cold_water: 15, hot_water: 11, electricity: 4 },
  { time: '12:45', cold_water: 14, hot_water: 10, electricity: 5 },
  { time: '12:50', cold_water: 12, hot_water: 8, electricity: 3 },
  { time: '12:55', cold_water: 13, hot_water: 9, electricity: 4 },
]

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
        <div class="inline-flex justify-start items-center gap-[6px]">
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
    </div>

    <!-- Complaints -->
    <ComplaintsBlock :complaintsData24h="complaintData24h" :complaintsData60m="complaintData60m" />
  </div>
</template>
