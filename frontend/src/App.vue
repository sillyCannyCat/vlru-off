<script setup>
import Button from './components/ui/Button.vue'
import Input from './components/ui/Input.vue'
import Label from './components/ui/Label.vue'
import StatsLabel from './components/ui/StatsLabel.vue'

const loginUser = () => {}
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
          <span class="text-micro-regular">На 300 случаев больше, чем вчера</span>
          <StatsLabel :value="10" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
