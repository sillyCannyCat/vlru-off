import { defineStore } from 'pinia'

export const useOutagesStore = defineStore('outages', {
  state: () => ({
    // Overall
    todayOutages: {
      date: '01.01',
      todayCount: 0,
      yesterdayCount: 0,
      plannedCount: 0,
      difference: 0,
      differenceSentence: '',
      differencePercentage: 0,
      trend: 'same',
    },
    // Outages
    typeOutages: {
      coldWater: { id: 1, icon: '/icons/cold-water.svg', title: 'Холодная вода', value: 0 },
      hotWater: { id: 2, icon: '/icons/hot-water.svg', title: 'Горячая вода', value: 0 },
      electricity: {
        id: 3,
        icon: '/icons/electricity.svg',
        title: 'Электоэнергия',
        value: 0,
      },
    },
    orgOutages: [],
    orgOutagesLen: 0,

    // Complaints
    todayComplaints: {
      date: '',
      summarySentence: 'Жители сообщают о множественных отключениях ',
      summaryTypes: [],
      count: 0,
    },
    complaintsData24h: [],
    complaintsData60m: [],
  }),
  actions: {},
})
