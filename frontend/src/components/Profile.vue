<template>
  <div class="container mx-auto px-4 py-8 mt-15">
    <h1 class="text-3xl font-bold text-center mb-8">User Profile</h1>

    <div v-if="userInfo" class="bg-white shadow-md rounded-lg p-6 text-center">
  
      <!-- User Avatar -->
      <div class="flex justify-center mb-6">
        <img
          :src="userInfo.user_image || defaultImage"
          alt="User Avatar"
          class="w-24 h-24 rounded-full border-2 border-gray-300"
          @error="onImageError"
        />
      </div>

      <!-- Welcome Message -->
      <h2 class="text-2xl font-semibold mb-2">
        Welcome to your profile, {{ userInfo.full_name || 'User' }}!
      </h2>

      <p class="text-gray-600 mb-4">Username: {{ userInfo.first_name || 'N/A' }}</p>
      <p class="text-gray-600 mb-4">Email: {{ userInfo.name || 'N/A' }}</p>

      <!-- Logout Button -->
      <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-center">
        <button
          @click="logout"
          class="w-full md:w-auto flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          <LogOutIcon class="w-5 h-5 mr-2" />
          Logout
        </button>
      </div>
    </div>

    <!-- Loading Spinner -->
    <div v-else class="text-center">
      <p>Loading user information...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { session } from "../data/session"; 
import { LogOutIcon } from 'lucide-vue-next'

const defaultImage = "https://cdn-icons-png.flaticon.com/512/1053/1053244.png";
const userInfo = ref(null);

// Image error handler
function onImageError(event) {
  event.target.src = defaultImage;
}

// Fetch user info from API
async function fetchUserInfo() {
  try {
    const response = await axios.get("/api/method/erp_mobile.api.get_current_user_info");
    userInfo.value = response.data.message;
  } catch (error) {
    console.error("Error fetching user info:", error);
  }
}

// Handle logout
function logout() {
  session.logout.submit(); 
  console.log("User logged out");
}

onMounted(() => {
  fetchUserInfo();
});
</script>
