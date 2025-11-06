<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  index: {
    type: String,
    required: true,
  },
})

const categories = ['cold_water', 'hot_water', 'electricity']
const categoryLabels = {
  cold_water: 'ХВС',
  hot_water: 'ГВС',
  electricity: 'Электричество',
}
const categoryColors = {
  cold_water: 'var(--color-accent-blue-bg)',
  hot_water: 'var(--color-accent-orange-bg)',
  electricity: 'var(--color-accent-purple-bg)',
}
const categoryHoverColors = {
  cold_water: 'var(--color-accent-blue)',
  hot_water: 'var(--color-accent-orange)',
  electricity: 'var(--color-accent-purple)',
}

const chartHeight = 150
const marginTop = 16
const marginBottom = 0
const marginLeft = 0
const marginRight = 0
const barSpacing = 2

const containerRef = ref(null)
const svgWidth = ref(600)

const hoveredBarIndex = ref(null)

const maxValue = computed(() => {
  return Math.max(
    ...props.data.map((item) => categories.reduce((sum, cat) => sum + (item[cat] || 0), 0)),
    1,
  )
})

const chartWidth = computed(() => svgWidth.value - marginLeft - marginRight)
const barWidth = computed(() => {
  if (props.data.length === 0) return 0
  const available = chartWidth.value
  const totalSpacing = (props.data.length - 1) * barSpacing
  const totalBars = available - totalSpacing
  return Math.max(12, totalBars / props.data.length)
})

const bars = computed(() => {
  return props.data.map((item, i) => {
    const x = marginLeft + i * (barWidth.value + barSpacing)
    let yStack = 0
    const segments = categories.map((cat, j) => {
      const value = item[cat] || 0
      const height = (value / maxValue.value) * (chartHeight - marginTop - marginBottom)
      const y = chartHeight - marginBottom - yStack - height
      yStack += height
      return {
        value,
        height,
        y,
        cat,
        color: categoryColors[cat],
        hoverColor: categoryHoverColors[cat],
        label: categoryLabels[cat],
        isTop: j === categories.length - 1 || (value > 0 && item[categories[j + 1]] === 0),
      }
    })
    return {
      x,
      width: barWidth.value,
      label: item[props.index],
      segments,
      item,
    }
  })
})

// Tooltip
const tooltip = ref({ visible: false, x: 0, y: 0, content: {} })

const showTooltip = (evt, bar, index) => {
  hoveredBarIndex.value = index

  const rect = containerRef.value.getBoundingClientRect()
  const tooltipWidth = 160
  const tooltipHeight = 80

  let x = evt.clientX - rect.left + 10
  let y = evt.clientY - rect.top - 10

  if (x + tooltipWidth > rect.width) x = evt.clientX - rect.left - tooltipWidth - 10
  if (y < 0) y = 0
  if (y + tooltipHeight > rect.height) y = rect.height - tooltipHeight

  tooltip.value = {
    visible: true,
    x,
    y,
    content: {
      time: bar.label,
      cold: bar.item.cold_water || 0,
      hot: bar.item.hot_water || 0,
      electricity: bar.item.electricity || 0,
    },
  }
}

const hideTooltip = () => {
  tooltip.value.visible = false
  hoveredBarIndex.value = null
}

const updateWidth = () => {
  if (containerRef.value) {
    svgWidth.value = containerRef.value.clientWidth
  }
}

onMounted(() => {
  updateWidth()
  window.addEventListener('resize', updateWidth)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', updateWidth)
})
</script>

<template>
  <div ref="containerRef" class="relative w-full">
    <svg
      :width="svgWidth"
      :height="chartHeight"
      class="bg-[var(--color-background-primary)] rounded-lg border border-[var(--color-text-muted)]"
    >
      <!-- Сетка -->
      <line
        v-for="i in 4"
        :key="i"
        :x1="marginLeft"
        :y1="marginTop + ((chartHeight - marginTop - marginBottom) * i) / 4"
        :x2="svgWidth - marginRight"
        :y2="marginTop + ((chartHeight - marginTop - marginBottom) * i) / 4"
        stroke="#e5e7eb"
        stroke-dasharray="4"
      />

      <!-- Столбики -->
      <g
        v-for="(bar, i) in bars"
        :key="i"
        @mousemove="(e) => showTooltip(e, bar, i)"
        @mouseleave="hideTooltip"
        class="cursor-pointer"
      >
        <g v-for="(seg, j) in bar.segments" :key="j">
          <rect
            :x="bar.x"
            :y="seg.y"
            :width="bar.width"
            :height="Math.max(1, seg.height)"
            :fill="hoveredBarIndex === i ? seg.hoverColor : seg.color"
            class="transition-all"
            :style="seg.isTop ? 'clip-path: inset(0 0 0 round 2px 2px 0 0)' : ''"
          />
        </g>
      </g>
    </svg>

    <!-- Tooltip -->
    <div
      v-if="tooltip.visible"
      class="absolute bg-[var(--color-background-primary)] border border-[var(--color-text-muted)] rounded-[6px] text-micro-regular p-2 pointer-events-none"
      :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
    >
      <div class="text-small-medium">{{ tooltip.content.time }}</div>
      <div>Холодная вода: {{ tooltip.content.cold }}</div>
      <div>Горячая вода: {{ tooltip.content.hot }}</div>
      <div>Электричество: {{ tooltip.content.electricity }}</div>
    </div>
  </div>
</template>
