<template>
  <nav class="bg-white shadow-lg fixed bottom-0 left-0 right-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-around">
        <router-link
          to="/"
          class="py-2 px-2 transition duration-300 flex flex-col items-center"
          :class="isActive('/')"
        >
          <HomeIcon class="w-5 h-5 mx-auto" />
          <span class="text-xs">Home</span>
        </router-link>

        <router-link
          to="/items"
          class="py-2 px-2 transition duration-300 flex flex-col items-center"
          :class="isActive('/items')"
        >
          <BoxIcon class="w-5 h-5 mx-auto" />
          <span class="text-xs">Items</span>
        </router-link>

        <router-link
          to="/profile"
          class="py-2 px-2 transition duration-300 flex flex-col items-center"
          :class="isActive('/profile')"
        >
          <UserIcon class="w-5 h-5 mx-auto" />
          <span class="text-xs">Profile</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { HomeIcon, BoxIcon, UserIcon } from "lucide-vue-next";
import { useRoute } from "vue-router";

const route = useRoute();

const isActive = (path) => {
  return route.path === path
    ? "text-purple-700"
    : "text-gray-500 hover:text-indigo-500";
};
</script>
