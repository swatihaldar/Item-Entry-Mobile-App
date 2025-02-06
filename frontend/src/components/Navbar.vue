<template>
  <div class="bg-white border-b px-6 py-3 flex items-center justify-between shadow-md">

    <div class="flex items-center space-x-4">
      <router-link to="/" class="text-gray-800 hover:text-blue-600 font-semibold text-lg flex items-center">
        ERP Mobile
      </router-link>
    </div>

  
    <div class="flex items-center space-x-4">
      <!-- Optional: Add more navigation items if needed -->
      <!-- <router-link to="/items" class="text-gray-600 hover:text-gray-700">
        <BoxIcon class="h-6 w-6" />
      </router-link> -->
      
      <Dropdown
        :options="[
          {
            label: 'My Profile',
            onClick: () => $router.push('/profile'),
          },
        ]"
      >
        <Avatar
          :label="user?.full_name"
          :image="user?.user_image"
          size="lg"
          class="cursor-pointer border-2 border-gray-200 p-1"
        />
      </Dropdown>
    </div>
  </div>
</template>

<script setup>
import { Dropdown, Avatar } from "frappe-ui";
import { BoxIcon } from "lucide-vue-next";
import { useRouter } from "vue-router";


const props = defineProps({
  user: {
    type: Object,
    required: false,
  },
});


const router = useRouter();

</script>

<style scoped>
.bg-white {
  background-color: #ffffff;
}

.shadow-md {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.text-gray-800 {
  color: #2d3748;
}

.text-blue-600 {
  color: #3182ce;
}

.font-semibold {
  font-weight: 600;
}

.text-lg {
  font-size: 1.125rem;
}

.cursor-pointer {
  cursor: pointer;
}

.border-2 {
  border-width: 2px;
}

.border-gray-200 {
  border-color: #edf2f7;
}

.p-1 {
  padding: 0.25rem;
}

</style>
