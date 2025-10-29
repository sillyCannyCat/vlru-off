<template>
  <div ref="mapContainer" class="map-container" style="width: 100%; height: 100%"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const mapContainer = ref(null)
let map = null

// стартовая точка
const center = [43.115542, 131.885494]

// массив меток
const markers = [
  {
    coords: [43.14199293270051, 131.90807239774105],
    title: 'Метка 1',
    desc: 'Описание 1',
  },
  {
    coords: [43.171246518452826, 131.91704320382007],
    title: 'Метка 2',
    desc: 'Описание 2',
  },
  {
    coords: [43.17160112621735, 131.91786531590515],
    title: 'Метка 3',
    desc: 'Описание 3',
  },
]

onMounted(() => {
  // загружаем скрипт Яндекс.Карт динамически
  if (!window.ymaps) {
    const script = document.createElement('script')
    script.src = 'https://api-maps.yandex.ru/2.1/?lang=ru_RU'
    script.onload = initMap
    document.head.appendChild(script)
  } else {
    initMap()
  }
})

function initMap() {
  window.ymaps.ready(() => {
    map = new window.ymaps.Map(mapContainer.value, {
      center: center,
      zoom: 14,
      controls: ['zoomControl', 'fullscreenControl'],
    })

    markers.forEach((m) => {
      const placemark = new window.ymaps.GeoObject({
        geometry: {
          type: 'Point', // тип геометрии - точка
          coordinates: m.coords, // координаты точки
        },
      })
      map.geoObjects.add(placemark)
    })
  })
}
</script>
