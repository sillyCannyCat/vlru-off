<script setup>
import '@/styles/typography.css'
import Button from '@/components/ui/Button.vue'
import Label from '@/components/ui/Label.vue'


const props = defineProps({
  address: {
    type: String,
    default: 'Прикольная ул. 52',
    required: false
  },
  issue: {
    type: String,
    default: 'Нет горячей воды',
    required: false
  },
  until: {
    type: String,
    default: '12:00',
    required: false
  },

  editText: {
    type: String,
    default: 'Изменить'
  },
  actionText: {
    type: String,
    default: 'Подробнее'
  }
})

const emit = defineEmits({
  'detail-click': (event) => true,

  'edit-click': (event) => true
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
          <slot name="address">{{ props.address }}</slot>
        </div>
      </div>

      <button
        @click="emit('edit-click', $event)"
        class="text-small-regular text-[var(--color-text-primary)] underline cursor-pointer hover:opacity-70 transition"
      >
        <slot name="edit">{{ props.editText }}</slot>
      </button>
    </div>

    <div class="inline-flex justify-start items-center gap-1">
      <div class="text-body-regular text-black font-normal">
        <slot name="issue">{{ props.issue }}</slot>
      </div>

      <Label variant="ghost">
        до <slot name="until">{{ props.until }}</slot>
      </Label>
    </div>

    <div class="self-stretch">
      <Button
        @click="emit('detail-click', $event)"
        class="w-full"
      >
        <slot name="action">{{ props.actionText }}</slot>
      </Button>
    </div>
  </div>
</template>