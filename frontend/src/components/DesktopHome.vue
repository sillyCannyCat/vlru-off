<script setup>
import MapView from '@/views/MapView.vue'
import ComplaintsGraphBlock from './ComplaintsGraphBlock.vue'
import OrgOutagesBlock from './OrgOutagesBlock.vue'
import TypeOutagesBlock from './TypeOutagesBlock.vue'
import Button from './ui/Button.vue'
import Input from './ui/Input.vue'
import Label from './ui/Label.vue'
import StatsLabel from './ui/StatsLabel.vue'

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
</script>

<template>
  <div
    class="w-full max-w-[1248px] px-[16px] py-[24px] inline-flex flex-col justify-start items-start gap-[32px]"
  >
    <!-- Header -->
    <div class="self-stretch inline-flex justify-between items-center">
      <!-- Logo and title -->
      <div class="inline-flex justify-start items-center">
        <img src="/icons/vlru-logo.svg" class="w-[95px] h-[42px]" />
        <div class="inline-flex flex-col justify-center items-start">
          <p class="text-h3-medium">Отключения</p>
          <span class="text-body-regular">Владивосток</span>
        </div>
      </div>

      <Button @click="loginUser" suffixIcon="/icons/log-in.svg">Войти</Button>
    </div>

    <!-- Container -->
    <div class="flex flex-row w-full items-start justify-start gap-x-[16px] gap-y-[32px]">
      <!-- Left side -->
      <div class="w-full min-w-[392px] inline-flex flex-col gap-[32px]">
        <!-- Search bar -->
        <div class="self-stretch inline-flex flex-col justify-start items-start gap-[6px]">
          <Input prefixIcon="/icons/search.svg" placeholder="Информация по вашему адресу"></Input>
          <span class="text-body-regular"
            ><span class="text-body-medium">Совет:</span> Введите свой адрес, чтобы узнать об
            отключениях и восстановлениях</span
          >
        </div>

        <!-- Overall -->
        <div class="self-stretch inline-flex flex-col justify-start items-start gap-[16px]">
          <div class="self-stretch inline-flex justify-between items-center">
            <!-- Stats -->
            <div class="inline-flex justify-start items-center gap-[8px]">
              <Label variant="outline">21.10</Label>
              <p class="text-h3-medium">Сегодня 1300 отключений</p>
            </div>

            <div class="inline-flex justify-start items-center gap-[8px]">
              <span class="text-body-regular">Это на 300 случаев больше, чем вчера</span>
              <StatsLabel :value="10" />
            </div>
          </div>

          <Button class="w-full">Плановые отключени (9)</Button>
        </div>

        <!-- Outages today -->
        <div class="flex flex-row w-full items-start justify-start gap-x-[24px] gap-y-[24px]">
          <!-- By types -->
          <div class="self-stretch w-full inline-flex flex-col gap-[8px]">
            <!-- Title -->
            <div class="self-stretch w-full inline-flex justify-between items-center">
              <p class="text-h3-medium">Отключения сейчас</p>
              <Label><span class="text-body-regular">по типам</span></Label>
            </div>

            <TypeOutagesBlock :byTypeOutages="byTypeOutages" />
          </div>

          <!-- By orgs -->
          <div class="self-stretch w-full inline-flex flex-col gap-[8px]">
            <!-- Title -->
            <div class="self-stretch w-full inline-flex justify-between items-center">
              <Label><span class="text-body-regular">по организациям</span></Label>
            </div>

            <OrgOutagesBlock :byOrgOutages="byOrgOutages" :byOrgOutagesLen="byOrgOutagesLen" />
          </div>
        </div>

        <!-- Complaints -->
        <div class="self-stretch inline-flex flex-col justify-start items-start gap-[16px]">
          <!-- Title and summorized info -->
          <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
            <p class="text-h3-medium">Отключения по жалобам</p>
            <span class="text-body-regular"
              ><span class="text-body-medium">Сводка:</span> Жители сообщают о множественных
              отключениях горячей воды и света</span
            >
          </div>

          <!-- Graph -->
          <ComplaintsGraphBlock
            :complaintsData24h="complaintData24h"
            :complaintsData60m="complaintData60m"
          />
        </div>
      </div>

      <div class="min-w-[400px] h-[400px] rounded-[6px] overflow-hidden">
        <MapView />
      </div>
    </div>
  </div>
</template>
