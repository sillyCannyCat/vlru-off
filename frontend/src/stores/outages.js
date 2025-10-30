import { getComplaintsData } from '@/lib/getComplaintsData'
import { getTodayComplaints } from '@/lib/getTodayComplaints'
import { getTodayOutages } from '@/lib/getTodayOutages.js'
import { getTodayStats } from '@/lib/getTodayStats'
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
  actions: {
    async todayOutagesUpdater() {
      const response = await getTodayOutages()

      this.todayOutages.date = response.date
      this.todayOutages.todayCount = response.today_count
      this.todayOutages.yesterdayCount = response.yesterday_count
      this.todayOutages.plannedCount = response.planned_count

      const difference = response.difference
      if (difference > 0) {
        this.todayOutages.differenceSentence = `На ${difference} больше, чем вчера`
      } else if (difference < 0) {
        this.todayOutages.differenceSentence = `На ${Math.abs(difference)} меньше, чем вчера`
      } else {
        this.todayOutages.differenceSentence = 'Статистика не изменилась'
      }

      this.todayOutages.difference = difference
      this.todayOutages.differencePercentage = response.difference_percentage
      this.todayOutages.trend = response.trend
    },
    async statsOutagesUpdater() {
      const response = await getTodayStats()

      this.typeOutages.coldWater.value = response.types.cold_water
      this.typeOutages.hotWater.value = response.types.hot_water
      this.typeOutages.electricity.value = response.types.electricity

      const orgOutagesArr = response.orgs
      this.orgOutages = orgOutagesArr
      this.orgOutagesLen =
        orgOutagesArr.length - 4 <= 0 ? orgOutagesArr.length : orgOutagesArr.length - 4
    },
    async todayComplaintsUpdater() {
      const response = await getTodayComplaints()

      this.todayComplaints.date = response.report_date
      this.todayComplaints.summaryTypes = response.summary_types
      this.todayComplaints.count = response.count
    },
    async complaintsDataUpdater() {
      const response24h = await getComplaintsData('24h')
      this.complaintsData24h = response24h.data
      const response60m = await getComplaintsData('60m')
      this.complaintsData60m = response60m.data
    },
  },
})
