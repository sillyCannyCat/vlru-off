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
</template>

<script setup>
import Button from '../components/ui/Button.vue'
import Input from '../components/ui/Input.vue'
import Label from '../components/ui/Label.vue'
import StatsLabel from '../components/ui/StatsLabel.vue'
</script>
