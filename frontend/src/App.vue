<template>
  <div id="app" class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Pass user data as a prop to Navbar -->
    <Navbar :user="user.data" />
    <main class="flex-grow overflow-y-auto pb-16">
      <router-view></router-view>
    </main>
    <nav class="bg-white shadow-lg fixed bottom-0 left-0 right-0">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-around">
          <router-link to="/" class="py-3 px-2 text-gray-500 hover:text-indigo-500 transition duration-300">
            <HomeIcon class="w-6 h-6 mx-auto" />
            <span class="text-xs">Home</span>
          </router-link>
          <router-link to="/items" class="py-3 px-2 text-gray-500 hover:text-indigo-500 transition duration-300">
            <BoxIcon class="w-6 h-6 mx-auto" />
            <span class="text-xs">Items</span>
          </router-link>
          <router-link to="/profile" class="py-3 px-2 text-gray-500 hover:text-indigo-500 transition duration-300">
            <UserIcon class="w-6 h-6 mx-auto" />
            <span class="text-xs">Profile</span>
          </router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { HomeIcon, BoxIcon, UserIcon } from 'lucide-vue-next';
import Navbar from './components/Navbar.vue';
import { createResource } from "frappe-ui";

const user = createResource({
  url: "erp_mobile.api.get_current_user_info",
  auto: true,
  onError() {
    window.location.href = "/login?redirect-to=%2Fhr%2Froster";
  },
});
</script>

<style>
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#app {
  height: 100vh;
  overflow: hidden;
}

main {
  height: calc(100vh - 112px);
  overflow-y: auto;
}
</style>
