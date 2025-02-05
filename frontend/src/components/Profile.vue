<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-center mb-8">User Profile</h1>

    <div v-if="session.isLoggedIn" class="bg-white shadow-md rounded-lg p-6 text-center">
      <h2 class="text-2xl font-semibold mb-4">
        Welcome to your profile, {{ session.user }}!
      </h2>
      
      <!-- <p class="text-gray-600 mb-8">Username: {{ session.user }}</p> -->

      <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <button
            @click="logout"
            class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            <LogOutIcon class="w-5 h-5 mr-2" />
            Logout
          </button>
        </div>
    </div>

    <div v-else class="text-center text-gray-600">
      Please log in to view your profile.
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { session } from '../data/session'
import { Button } from 'frappe-ui'
import { LogOutIcon } from 'lucide-vue-next'

function logout() {
  session.logout.submit()
}

onMounted(() => {
  if (!session.isLoggedIn) {
    session.fetch()
  }
})
</script>