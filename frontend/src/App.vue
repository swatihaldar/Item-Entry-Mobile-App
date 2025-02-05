<template>
  <div id="app" class="min-h-screen bg-gray-100 flex flex-col">
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
import { HomeIcon, BoxIcon, UserIcon } from 'lucide-vue-next'
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
  height: calc(100vh - 64px); 
  overflow-y: auto;
}
</style>

