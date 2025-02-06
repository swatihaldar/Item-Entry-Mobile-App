<template>
    <div class="p-4 sm:p-6">

      <div v-if="items.loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
  
      
      <div v-else-if="items.error" class="text-center text-red-500 p-4">
        Error: {{ items.error }}
      </div>
  
      
      <div v-else class="h-64 sm:h-80">
        <Bar :data="barChartData" :options="barChartOptions" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { createListResource } from 'frappe-ui'
  import { computed } from 'vue'
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  
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
  
  // Bar chart data
  const barChartData = computed(() => ({
    labels: groupedData.value.map(item => item.category),
    datasets: [
      {
        label: 'Number of Items by Category',
        data: groupedData.value.map(item => item.count),
        backgroundColor: [
          '#2231ff'
        ],
        borderColor: '#FFFFFF',
        borderWidth: 1,
      },
    ],
  }))
  

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          boxWidth: 12,
          padding: 15,
          font: {
            size: 14, 
            weight: 'bold',  
          },
        },
      },
      title: {
        display: true,
        text: 'Items by Category',
        font: {
          size: 18, 
          weight: 'bold',
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Categories',
          font: {
            size: 14,
            weight: 'bold',
          },
        },
        grid: {
          display: false,  
        },
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Number of Items',
          font: {
            size: 14,
            weight: 'bold',
          },
        },
        grid: {
          display: false, 
        },
      },
    },
  }
  </script>
  
  <style scoped>

  .chart-container {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  </style>
  