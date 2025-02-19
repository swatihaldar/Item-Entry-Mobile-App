<template>
  <div id="app" class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Hide Navbar on the Login page -->
    <Navbar v-if="$route.name !== 'Login'" :user="user.data" />
    
    <main class="flex-grow overflow-y-auto pb-16">
      <router-view></router-view>
    </main>
    
    <!-- Hide BottomNavbar on the Login page -->
    <BottomNavbar v-if="$route.name !== 'Login'" />
  </div>
</template>

<script setup>
import { createResource } from "frappe-ui";
import { useRoute } from "vue-router"; // Import useRoute
import Navbar from './components/Navbar.vue';
import BottomNavbar from './components/BottomNavbar.vue';

const route = useRoute(); // Get current route

const user = createResource({
  url: "erp_mobile.api.get_current_user_info",
  auto: true,
  // onError() {
  //   window.location.href = "/login?redirect-to=%2Fhr%2Froster";
  // },
});
</script>
