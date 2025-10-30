import { useOutagesStore } from '@/stores/outages'

export async function initStoreActions() {
  const outagesStore = useOutagesStore()

  await Promise.all([
    outagesStore.todayOutagesUpdater(),
    outagesStore.statsOutagesUpdater(),
    outagesStore.todayComplaintsUpdater(),
    outagesStore.complaintsDataUpdater(),
  ])
}
