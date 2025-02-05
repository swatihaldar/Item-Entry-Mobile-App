<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-center mb-8">Welcome to ERPNext Mobile</h1>
    
    <div class="grid grid-cols-2 gap-4">
      <router-link to="/items" class="bg-blue-500 hover:bg-blue-600 text-white rounded-lg p-6 flex flex-col items-center justify-center">
        <BoxIcon class="w-12 h-12 mb-2" />
        <span class="text-lg font-semibold">Items</span>
      </router-link>
      
      <router-link to="/profile" class="bg-green-500 hover:bg-green-600 text-white rounded-lg p-6 flex flex-col items-center justify-center">
        <UserIcon class="w-12 h-12 mb-2" />
        <span class="text-lg font-semibold">Profile</span>
      </router-link>
    </div>

    <div class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Recent Activities</h2>
      <ul class="bg-white rounded-lg shadow divide-y">
        <li v-for="(activity, index) in recentActivities" :key="index" class="p-4">
          <div class="flex items-center">
            <component :is="activity.icon" class="w-6 h-6 mr-3 text-gray-500" />
            <div>
              <p class="font-medium">{{ activity.text }}</p>
              <p class="text-sm text-gray-500">{{ activity.timestamp }}</p>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { BoxIcon, UserIcon, PlusIcon, EditIcon, TrashIcon } from 'lucide-vue-next'

const recentActivities = ref([
  { icon: PlusIcon, text: 'New item added: Iphone', timestamp: '2 hours ago' },
  { icon: EditIcon, text: 'Updated item: Realme', timestamp: '5 hours ago' },
  { icon: TrashIcon, text: 'Deleted item: ', timestamp: '1 day ago' },
  { icon: UserIcon, text: 'Profile updated', timestamp: '2 days ago' },
])
</script>

