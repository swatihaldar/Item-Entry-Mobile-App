<template>
  <div class="p-4">
    <div v-if="items.loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#6C63FF]"></div>
    </div>

    <div v-else-if="items.error" class="text-center text-red-500 p-4">
      Error: {{ items.error }}
    </div>

    <div v-else class="h-64">
      <Bar :data="barChartData" :options="barChartOptions" />
    </div>
  </div>
</template>

<script setup>
import { createListResource } from 'frappe-ui'
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  Title, 
  Tooltip, 
  Legend, 
  BarElement, 
  CategoryScale, 
  LinearScale 
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const items = createListResource({
  doctype: 'Item',
  fields: ['item_group', 'name'],
  auto: true,
})

const groupedData = computed(() => {
  if (!items.data?.length) return []

  const categories = items.data.reduce((acc, item) => {
    const category = item.item_group || 'Uncategorized'
    acc[category] = (acc[category] || 0) + 1
    return acc
  }, {})

  return Object.entries(categories).map(([category, count]) => ({ category, count }))
})

const barChartData = computed(() => ({
  labels: groupedData.value.map(item => item.category),
  datasets: [
    {
      label: 'Items per Category',
      data: groupedData.value.map(item => item.count),
      backgroundColor: '#6C63FF',
      borderColor: '#8A84FF',
      borderWidth: 1,
      borderRadius: 8,
      maxBarThickness: 40,
    },
  ],
}))

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: '#6C63FF',
      titleFont: {
        size: 14,
        weight: 'bold',
      },
      bodyFont: {
        size: 12,
      },
      padding: 12,
      cornerRadius: 8,
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
        drawBorder: false 
      },
      ticks: {
        font: {
          size: 11,
        },
        color: '#64748B',
      },
    },
    y: {
      beginAtZero: true,
      grid: {
        color: '#E2E8F0',
        drawBorder: false, 
        display: false 
      },
      ticks: {
        font: {
          size: 11,
        },
        color: '#64748B',
        padding: 8,
      },
    },
  },
}
</script>

<style scoped>
.chart-container {
  border-radius: 16px;
  background-color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>
