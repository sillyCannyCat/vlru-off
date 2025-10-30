<script setup>
import { useOutagesStore } from '@/stores/outages'
import MapView from '@/views/MapView.vue'
import ComplaintsGraphBlock from './ComplaintsGraphBlock.vue'
import OrgOutagesBlock from './OrgOutagesBlock.vue'
import TypeOutagesBlock from './TypeOutagesBlock.vue'
import Button from './ui/Button.vue'
import Input from './ui/Input.vue'
import Label from './ui/Label.vue'
import NotificationBanner from './ui/NotificationBanner.vue'
import StatsLabel from './ui/StatsLabel.vue'

const outagesStore = useOutagesStore()
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
      <div class="w-full min-w-[700px] inline-flex flex-col gap-[32px]">
        <!-- Search bar -->
        <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
          <Input prefixIcon="/icons/search.svg" placeholder="Информация по вашему адресу"></Input>
          <span class="text-body-regular flex gap-[8px]"
            ><Label variant="tip">Совет</Label> Введите свой адрес, чтобы узнать об отключениях и
            восстановлениях</span
          >
        </div>

        <!-- Overall -->
        <div class="self-stretch inline-flex flex-col justify-start items-start gap-[16px]">
          <div class="self-stretch inline-flex justify-between items-center">
            <!-- Stats -->
            <div class="inline-flex justify-start items-center gap-[8px]">
              <Label variant="outline">{{ outagesStore.todayOutages.date }}</Label>
              <p class="text-h3-medium">
                Сегодня {{ outagesStore.todayOutages.todayCount }} отключений
              </p>
            </div>

            <div class="inline-flex justify-start items-center gap-[8px]">
              <span class="text-body-regular">{{
                outagesStore.todayOutages.differenceSentence
              }}</span>
              <StatsLabel :value="outagesStore.todayOutages.differencePercentage" />
            </div>
          </div>

          <Button class="w-full"
            >Плановые отключени ({{ outagesStore.todayOutages.plannedCount }})</Button
          >
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

            <TypeOutagesBlock :byTypeOutages="outagesStore.typeOutages" />
          </div>

          <!-- By orgs -->
          <div class="self-stretch w-full inline-flex flex-col gap-[8px]">
            <!-- Title -->
            <div class="self-stretch w-full inline-flex justify-between items-center">
              <Label><span class="text-body-regular">по организациям</span></Label>
            </div>

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
            <span class="text-body-regular flex gap-[8px]"
              ><Label variant="tip">Сводка</Label
              >{{ outagesStore.todayComplaints.summarySentence }}</span
            >
          </div>

          <!-- Graph -->
          <ComplaintsGraphBlock
            :complaintsData24h="outagesStore.complaintsData24h"
            :complaintsData60m="outagesStore.complaintsData60m"
          />
        </div>
      </div>

      <div class="self-stretch inline-flex flex-col justify-start items-start gap-[24px]">
        <div
          class="min-w-[400px] h-[400px] rounded-[6px] border-[1px] border-[var(--color-text-muted)] overflow-hidden"
        >
          <MapView />
        </div>

        <!-- Useful resources -->
        <div class="self-stretch inline-flex flex-col justify-start items-start gap-[8px]">
          <p class="text-h3-medium">Полезные ресурсы</p>

          <NotificationBanner
            gradient="purple"
            title="Подключите уведомления в Telegram"
            desc="о плановых и не только отключениях"
            suffixIcon="/icons/telegram.svg"
          />

          <NotificationBanner
            gradient="orange"
            title="Передайте показания счётчиков до 26.10"
            desc="холодной, горячей воды и электроэнергии"
            suffixIcon="/icons/meter.svg"
          />
        </div>
      </div>
    </div>
  </div>
</template>
