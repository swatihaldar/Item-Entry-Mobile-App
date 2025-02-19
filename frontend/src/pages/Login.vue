<template>
  <div class="flex items-center justify-center min-h-screen px-4 bg-gradient-to-r from-[#6C63FF] to-[#8A84FF]">
    <Card title="Login to Your ERP Mobile App!" class="w-full max-w-md p-6 rounded-lg shadow-lg bg-white">
      <form class="flex flex-col space-y-4 w-full" @submit.prevent="submit">
        <Input
          required
          name="email"
          type="text"
          placeholder="johndoe@email.com"
          label="User ID"
          class="border border-gray-300 rounded-md p-3 text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
        />
        <Input
          required
          name="password"
          type="password"
          placeholder="••••••"
          label="Password"
          class="border border-gray-300 rounded-md p-3 text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-[#6C63FF]"
        />
        <Button 
          :loading="session.login.loading" 
          variant="solid"
          class="bg-[#6C63FF] text-white rounded-md hover:bg-[#8A84FF] transition duration-200 py-2 md:py-3 text-sm md:text-base"
        >
          Login
        </Button>
      </form>

      <!-- <p class="mt-4 text-center text-gray-600 text-sm md:text-base">
        Don't have an account? 
        <router-link to="/register" class="text-[#6C63FF] font-semibold">Sign Up</router-link>
      </p> -->
    </Card>
  </div>
</template>

<style scoped>

.card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

input:focus {
  border-color: #6C63FF;
}
</style>

<script lang="ts" setup>
import { session } from '../data/session'

function submit(e) {
  let formData = new FormData(e.target)
  session.login.submit({
    email: formData.get('email'),
    password: formData.get('password'),
  })
}
</script>
