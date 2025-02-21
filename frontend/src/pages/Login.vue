<template>
  <div class="flex items-center justify-center min-h-screen bg-gradient-to-r from-[#6C63FF] to-[#8A84FF] px-4 py-8">
    <Card title="Login to Your ERP Mobile App!" class="w-full max-w-md p-8 rounded-2xl shadow-xl bg-white">
      <form class="flex flex-col space-y-6 w-full" @submit.prevent="submit">
        <div class="space-y-2">
          <Input
            required
            name="email"
            type="text"
            placeholder="johndoe@email.com"
            label="User ID"
            class="border border-gray-300 rounded-lg p-3 text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-[#6C63FF] transition duration-200"
          />
        </div>
        <div class="space-y-2">
          <Input
            required
            name="password"
            type="password"
            placeholder="••••••"
            label="Password"
            class="border border-gray-300 rounded-lg p-3 text-sm md:text-base focus:outline-none focus:ring-2 focus:ring-[#6C63FF] transition duration-200"
          />
        </div>

        <p v-if="errorMessage" class="text-red-500 text-sm font-medium">{{ errorMessage }}</p>
        
        <Button 
          :loading="session.login.loading" 
          variant="solid"
          class="bg-[#6C63FF] text-white rounded-lg hover:bg-[#8A84FF] transition duration-200 py-3 text-base font-semibold shadow-md hover:shadow-lg"
        >
          Login
        </Button>
      </form>

      <!-- <div class="mt-6 text-center">
        <a href="#" class="text-sm text-[#6C63FF] hover:underline">Forgot password?</a>
      </div> -->

      <div class="mt-8 pt-6 border-t border-gray-200">
        <p class="text-center text-gray-600 text-sm">
          Don't have an account? Contact your administrator.
        </p>
      </div>
    </Card>
  </div>
</template>

<style scoped>
.card {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

input:focus {
  border-color: #6C63FF;
}

body {
  overflow: hidden;
}
</style>

<script lang="ts" setup>
import { session } from '../data/session'
import { ref, onMounted } from 'vue'

const errorMessage = ref('')

function submit(e) {
  let formData = new FormData(e.target)
  session.login.submit({
    email: formData.get('email'),
    password: formData.get('password'),
  }).then((response) => {
    if (response.success) {
      errorMessage.value = ''  
    } else {
      errorMessage.value = 'Invalid credentials. Please try again.' 
    }
  }).catch(() => {
    errorMessage.value = 'An error occurred. Please try again.'
  })
}

onMounted(() => {
  document.body.style.overflow = 'hidden'
})
</script>