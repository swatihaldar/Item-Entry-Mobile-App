<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Simple Header Section -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold">Hello, {{ userInfo?.full_name || 'User' }}!</h1>
      <p class="text-xl">Welcome to ERP Mobile</p>
    </div>

    <!-- Quick Links Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-2xl font-semibold mb-4">Quick Links</h2>
      <div class="grid grid-cols-2 gap-4">
        <router-link
          v-for="link in filteredLinks"
          :key="link.to"
          :to="link.to"
          class="flex items-center justify-center p-4 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <component :is="link.icon" class="w-6 h-6 mr-2" />
          <span class="text-gray-800">{{ link.label }}</span>
        </router-link>
      </div>
    </div>

    <!-- Item Statistics Bar Chart -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-semibold mb-4">Item Statistics</h2>
      <Barchart />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { UserIcon, PackageIcon } from 'lucide-vue-next'
import { createResource } from 'frappe-ui'
import Barchart from '../components/Barchart.vue'


const userInfo = ref(null)


const quickLinks = [
  { to: '/items', icon: PackageIcon, label: 'Items' },
  { to: '/profile', icon: UserIcon, label: 'Profile' },
]


const filteredLinks = computed(() => {
  return quickLinks
})


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


onMounted(() => {
  fetchUserInfo.submit()
})
</script>

<style>

.router-link-active {
  color: #4CAF50; 
}

.router-link-exact-active {
  color: #2231ff; 
}

.router-link {
  text-decoration: none;
}

router-link {
  color: #4A5568; 
}

router-link:hover {
  color: #2D3748; 
}
</style>