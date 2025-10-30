<script setup>
import { useOutagesStore } from '@/stores/outages'
import { ref } from 'vue'
import ComplaintsGraphBlock from './ComplaintsGraphBlock.vue'
import OrgOutagesBlock from './OrgOutagesBlock.vue'
import TypeOutagesBlock from './TypeOutagesBlock.vue'
import Button from './ui/Button.vue'
import Input from './ui/Input.vue'
import Label from './ui/Label.vue'
import NotificationBanner from './ui/NotificationBanner.vue'
import StatsLabel from './ui/StatsLabel.vue'

const outagesStore = useOutagesStore()

const isTypeOutages = ref(true)
const toggleOutages = () => {
  isTypeOutages.value = !isTypeOutages.value
}
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

    <NotificationBanner
      gradient="purple"
      title="Подключите уведомления об отключениях в Telegram"
      desc="Нажми на баннер"
      suffixIcon="/icons/telegram.svg"
    />

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
          <Label variant="outline">{{ outagesStore.todayOutages.date }}</Label>
          <p class="text-h3-medium">
            Сегодня {{ outagesStore.todayOutages.todayCount }} отключений
          </p>
        </div>
        <div class="inline-flex justify-start items-center gap-[8px]">
          <span class="text-small-regular">{{ outagesStore.todayOutages.differenceSentence }}</span>
          <StatsLabel :value="outagesStore.todayOutages.differencePercentage" />
        </div>
      </div>

      <!-- Buttons -->
      <div class="self-stretch inline-flex justify-start items-start gap-[8px]">
        <Button @click="plannedOutages" class="w-full"
          >Плановые ({{ outagesStore.todayOutages.plannedCount }})</Button
        >
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
        <TypeOutagesBlock :byTypeOutages="outagesStore.typeOutages" />
      </div>
      <!-- By org -->
      <div v-else class="self-stretch inline-flex flex-col justify-start items-start">
        <OrgOutagesBlock
          :byOrgOutages="outagesStore.orgOutages"
          :byOrgOutagesLen="outagesStore.orgOutagesLen"
        />
      </div>
    </div>

    <!-- Complaints -->
    <div class="self-stretch inline-flex flex-col justify-start items-start gap-[16px]">
      <!-- Title and summorized info -->
      <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
        <p class="text-h3-medium">Отключения по жалобам</p>
        <span class="text-micro-regular"
          ><span class="text-micro-medium">Сводка: </span
          >{{ outagesStore.todayComplaints.summarySentence }}</span
        >
      </div>

      <ComplaintsGraphBlock
        :complaintsData24h="outagesStore.complaintsData24h"
        :complaintsData60m="outagesStore.complaintsData60m"
      />
    </div>
  </div>
</template>
