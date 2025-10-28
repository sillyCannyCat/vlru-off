<script setup>
import '@/styles/typography.css'

defineProps({
  address: {
    type: String,
    default: 'Прикольная ул. 52'
  },
  issue: {
    type: String,
    default: 'Нет горячей воды'
  },
  until: {
    type: String,
    default: '12:00'
  }
})
</script>

<template>
  <div class="w-80 p-2 bg-white rounded-md outline outline-1 outline-offset-[-1px] outline-zinc-200 inline-flex flex-col justify-start items-center gap-2 overflow-hidden">
    <div class="self-stretch inline-flex justify-between items-center">
      <div class="flex justify-start items-center gap-1">
        <div class="w-5 h-5 flex items-center justify-center">
          <img
            src="/icons/location-icon.svg"
            class="w-4 h-4 object-contain"
          />
        </div>
        <div class="text-body-regular text-black">
          <slot name="address">{{ address }}</slot>
        </div>
      </div>

      <div class="px-2 py-1 bg-white rounded-md outline outline-1 outline-offset-[-1px] outline-zinc-200 flex justify-center items-center gap-2.5 cursor-pointer hover:bg-zinc-50 transition">
        <div class="text-small-regular text-black">
          <slot name="edit">Изменить</slot>
        </div>
      </div>
    </div>

    <div class="inline-flex justify-start items-center gap-1">
      <div class="text-body-regular text-black font-normal">
        <slot name="issue">{{ issue }}</slot>
      </div>
      <div class="px-2 py-0.5 bg-zinc-100 rounded-md flex justify-center items-center gap-2.5">
        <div class="text-small-regular text-black">
          до <slot name="until">{{ until }}</slot>
        </div>
      </div>
    </div>

    <div class="self-stretch inline-flex justify-start items-start gap-2">
      <button class="flex-1 px-4 py-2 bg-black rounded-md flex justify-center items-center gap-2.5 hover:bg-zinc-800 transition">
        <div class="text-small-medium text-white">
          <slot name="action">Подробнее</slot>
        </div>
      </button>
    </div>
  </div>
</template>