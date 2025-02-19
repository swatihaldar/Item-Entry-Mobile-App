<template>
  <div class="bg-gray-50 min-h-screen">
    <!-- Hero Section with Image -->
    <div class="relative h-48 md:h-72 lg:h-96 mb-6">
      <img 
        src="/Working.jpg"
        alt="Hero image"
        class="w-full h-full object-cover object-center"
      />
      <div class="absolute inset-0 bg-gradient-to-b from-transparent to-[#6C63FF]/90">
        <div class="absolute bottom-6 left-6 text-white max-w-xl">
          <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-2">
            Hello, {{ userInfo?.full_name || 'User' }}!
          </h1>
          <p class="text-lg md:text-xl opacity-90">Welcome to ERP Mobile</p>
        </div>
      </div>
    </div>

    <!-- Main Content Container -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Quick Actions Cards -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h2>
        <div class="grid grid-cols-3 gap-4 md:gap-6">
          <div
            v-for="action in quickActions"
            :key="action.label"
            @click="handleActionClick(action)"
            class="bg-white rounded-2xl p-4 md:p-6 shadow-sm hover:shadow-md transition-all transform hover:-translate-y-1 cursor-pointer"
          >
            <div class="flex flex-col items-center">
              <div 
                class="w-12 h-12 md:w-16 md:h-16 rounded-full mb-3 flex items-center justify-center"
                :class="action.bgColor"
              >
                <component :is="action.icon" class="w-6 h-6 md:w-8 md:h-8 text-white" />
              </div>
              <span class="text-sm md:text-base font-medium text-gray-700 text-center">
                {{ action.label }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity Section -->
      <div class="mb-20">
        <div class="bg-white rounded-2xl p-6 shadow-sm">
          <h2 class="text-xl font-semibold mb-6 text-gray-800">Recent Activities</h2>
          <div v-if="recentActivities.loading" class="flex justify-center py-4">
            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#6C63FF]"></div>
          </div>
          <div v-else-if="!recentActivities.data?.length" class="text-center py-4 text-gray-500">
            No recent activities
          </div>
          <div v-else class="grid gap-4 md:grid-cols-3">
            <div 
              v-for="activity in limitedActivities" 
              :key="activity.name" 
              class="bg-gray-50 p-4 rounded-xl hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center mb-3">
                <div 
                  class="w-10 h-10 rounded-full flex items-center justify-center mr-3"
                  :class="getActivityColor(activity.action)"
                >
                  <component :is="getActivityIcon(activity.action)" class="w-5 h-5 text-white" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-800">{{ getActivityLabel(activity.action) }}</h3>
                  <p class="text-xs text-gray-500">{{ formatTimeAgo(activity.creation) }}</p>
                </div>
              </div>
              <p class="text-sm text-gray-600">{{ formatActivityTitle(activity) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Item Statistics Section -->
      <div class="mb-20">
        <div class="bg-white rounded-2xl p-6 shadow-sm">
          <h2 class="text-xl font-semibold mb-6 text-gray-800">Item Statistics</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-50 p-4 rounded-xl">
              <h3 class="text-lg font-medium mb-2 text-gray-700">Total Items</h3>
              <p class="text-3xl font-bold text-[#6C63FF]">{{ itemStats.totalItems }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-xl">
              <h3 class="text-lg font-medium mb-2 text-gray-700">Categories</h3>
              <p class="text-3xl font-bold text-[#6C63FF]">{{ itemStats.categories }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analytics Modal -->
    <div 
      v-if="showAnalytics" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
      @click.self="showAnalytics = false"
    >
      <div class="bg-white rounded-2xl w-full max-w-3xl p-6 animate-slide-up">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-800">Analytics Overview</h2>
          <button 
            @click="showAnalytics = false"
            class="p-2 hover:bg-gray-100 rounded-full"
          >
            <XIcon class="w-5 h-5 text-gray-500" />
          </button>
        </div>
        <Barchart />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  PackageIcon, 
  UserIcon,
  BarChart3Icon,
  PlusIcon,
  TrashIcon,
  PencilIcon,
  XIcon
} from 'lucide-vue-next'
import { createResource } from 'frappe-ui'
import Barchart from '../components/Barchart.vue'

const router = useRouter()
const userInfo = ref(null)
const showAnalytics = ref(false)

// Quick Actions with different colors
const quickActions = [
  { 
    label: 'Items',
    icon: PackageIcon,
    action: 'items',
    bgColor: 'bg-violet-500',
    to: '/items'
  },
  { 
    label: 'Analytics',
    icon: BarChart3Icon,
    action: 'analytics',
    bgColor: 'bg-violet-500'
  },
  { 
    label: 'Profile',
    icon: UserIcon,
    action: 'profile',
    bgColor: 'bg-violet-500',
    to: '/profile'
  }
]

// Show only the latest 3 activities
const limitedActivities = computed(() => {
  return recentActivities.data?.slice(0, 3) || []
})

function getActivityColor(action) {
  switch (action) {
    case 'create':
      return 'bg-green-500'
    case 'delete':
      return 'bg-red-500'
    case 'update':
      return 'bg-blue-500'
    default:
      return 'bg-gray-500'
  }
}

function getActivityLabel(action) {
  switch (action) {
    case 'create':
      return 'Item Added'
    case 'delete':
      return 'Item Deleted'
    case 'update':
      return 'Item Updated'
    default:
      return 'Action Performed'
  }
}

function handleActionClick(action) {
  if (action.action === 'analytics') {
    showAnalytics.value = true
  } else if (action.to) {
    router.push(action.to)
  }
}

// Fetch recent activities
const recentActivities = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Version',
    filters: {
      ref_doctype: 'Item',
    },
    fields: ['name', 'owner', 'creation', 'data', 'docname'],
    order_by: 'creation desc',
    limit: 3,
  },
  auto: true,
  transform(data) {
    return data.map(activity => {
      try {
        activity.data = JSON.parse(activity.data)
        return {
          ...activity,
          action: activity.data.changed && activity.data.changed.length > 0 ? 'update' :
                 activity.data.added && activity.data.added.length > 0 ? 'create' :
                 activity.data.removed && activity.data.removed.length > 0 ? 'delete' : 'other'
        }
      } catch (e) {
        console.error('Error parsing activity data:', e)
        return activity
      }
    })
  }
})

function getActivityIcon(action) {
  switch (action) {
    case 'create':
      return PlusIcon
    case 'delete':
      return TrashIcon
    case 'update':
      return PencilIcon
    default:
      return PackageIcon
  }
}

function formatActivityTitle(activity) {
  const itemName = activity.docname || 'Unknown Item'
  
  switch (activity.action) {
    case 'create':
      return `${itemName} has been added to inventory`
    case 'delete':
      return `${itemName} has been removed from inventory`
    case 'update':
      return `${itemName} details have been updated`
    default:
      return 'Action performed on item'
  }
}

function formatTimeAgo(timestamp) {
  const now = new Date()
  const activityDate = new Date(timestamp)
  const diffInSeconds = Math.floor((now - activityDate) / 1000)

  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`
  return `${Math.floor(diffInSeconds / 86400)} days ago`
}

const fetchUserInfo = createResource({
  url: 'erp_mobile.api.get_current_user_info',
  auto: true,
  onSuccess(data) {
    userInfo.value = data
  },
  onError(error) {
    console.error('Error fetching user info:', error)
  }
})

// Fetch item statistics
const itemStats = ref({ totalItems: 0, categories: 0 })
const fetchItemStats = createResource({
  url: 'frappe.client.get_count',
  params: {
    doctype: 'Item',
  },
  auto: true,
  onSuccess(data) {
    itemStats.value.totalItems = data
  },
})

const fetchItemCategories = createResource({
  url: 'frappe.client.get_count',
  params: {
    doctype: 'Item Group',
  },
  auto: true,
  onSuccess(data) {
    itemStats.value.categories = data
  },
})

// Auto-refresh recent activities and stats
let refreshInterval
onMounted(() => {
  fetchUserInfo.submit()
  refreshInterval = setInterval(() => {
    recentActivities.reload()
    fetchItemStats.reload()
    fetchItemCategories.reload()
  }, 60000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.router-link-active {
  color: #6C63FF;
}

.router-link-exact-active {
  color: #6C63FF;
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}

@keyframes slide-up {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>