<template>
    <div class="container mx-auto px-4 py-8">
      <div v-if="item" class="bg-white rounded-lg shadow-lg overflow-hidden max-w-6xl mx-auto">
        <!-- Header with back button -->
        <div class="relative">
          <div class="md:flex">
            <!-- Image Section -->
            <div class="md:w-1/2 relative">
              <button 
                @click="$router.back()" 
                class="absolute top-4 left-4 bg-white rounded-full p-2 shadow-lg z-10"
              >
                <ChevronLeftIcon class="h-6 w-6 text-gray-600" />
              </button>
              <img 
                :src="item.image || '/placeholder.svg?height=400&width=400'" 
                :alt="item.item_name"
                class="w-full h-64 md:h-[500px] object-cover"
              />
            </div>
  
            <!-- Details Section -->
            <div class="md:w-1/2 p-6">
              <div class="flex justify-between items-start">
                <div>
                  <h1 class="text-2xl md:text-3xl font-bold text-gray-900">{{ item.item_name }}</h1>
                  <p class="text-gray-500">Code: {{ item.item_code }}</p>
                </div>
                <div class="flex space-x-2">
                  <button 
                    @click="isEditMode = true" 
                    class="p-2 text-blue-600 hover:bg-blue-50 rounded-full"
                  >
                    <EditIcon class="h-5 w-5" />
                  </button>
                  <button 
                    @click="confirmDelete" 
                    class="p-2 text-red-600 hover:bg-red-50 rounded-full"
                  >
                    <TrashIcon class="h-5 w-5" />
                  </button>
                </div>
              </div>
  
              <!-- Item Details -->
              <div v-if="!isEditMode" class="mt-6 space-y-6">
                <div>
                  <h2 class="text-lg font-semibold mb-2">Description</h2>
                  <p class="text-gray-600">{{ item.description || 'No description available.' }}</p>
                </div>
  
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">Item Group</p>
                    <p class="font-medium">{{ item.item_group }}</p>
                  </div>
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">UOM</p>
                    <p class="font-medium">{{ item.stock_uom }}</p>
                  </div>
                </div>
  
                <div class="space-y-2">
                  <p class="text-gray-600">Created: {{ formatDate(item.creation) }}</p>
                  <p class="text-gray-600">Last Modified: {{ formatDate(item.modified) }}</p>
                  <p class="text-gray-600">Created By: {{ item.owner }}</p>
                </div>
              </div>
  
              <!-- Edit Form -->
              <div v-else class="mt-6">
                <form @submit.prevent="saveChanges" class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Item Name</label>
                    <input 
                      v-model="editedItem.item_name" 
                      type="text" 
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                  </div>
  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Description</label>
                    <textarea 
                      v-model="editedItem.description" 
                      rows="3"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    ></textarea>
                  </div>
  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Item Group</label>
                    <select 
                      v-model="editedItem.item_group"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      <option v-for="group in itemGroups" :key="group.name" :value="group.name">
                        {{ group.item_group_name }}
                      </option>
                    </select>
                  </div>
  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">UOM</label>
                    <select 
                      v-model="editedItem.stock_uom"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      <option value="Nos">Nos</option>
                      <option v-for="uom in uoms" :key="uom.name" :value="uom.name">
                        {{ uom.uom_name }}
                      </option>
                    </select>
                  </div>
  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Image URL</label>
                    <input 
                      v-model="editedItem.image" 
                      type="text"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />
                  </div>
  
                  <div class="flex justify-end space-x-2">
                    <button 
                      type="button"
                      @click="cancelEdit"
                      class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                    >
                      Cancel
                    </button>
                    <button 
                      type="submit"
                      class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-indigo-700"
                      :disabled="updateItem.loading"
                    > 
                      {{ updateItem.loading ? 'Saving...' : 'Save Changes' }} 
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Loading State -->
      <div v-else class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { createResource } from 'frappe-ui'
  import { useRoute, useRouter } from 'vue-router'
  import { ChevronLeftIcon, EditIcon, TrashIcon } from 'lucide-vue-next'
  
  const route = useRoute()
  const router = useRouter()
  const item = ref(null)
  const isEditMode = ref(false)
  const editedItem = ref({})
  const itemGroups = ref([])
  const uoms = ref([])
  
  const fetchItem = createResource({
    url: 'frappe.client.get',
    params: {
      doctype: 'Item',
      name: route.params.id
    },
    onSuccess(data) {
      item.value = data
      editedItem.value = { ...data }
    }
  })
  
  const fetchItemGroups = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Item Group',
      fields: ['name', 'item_group_name']
    },
    auto: true,
    onSuccess(data) {
      itemGroups.value = data
    }
  })
  
  const fetchUOMs = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'UOM',
      fields: ['name', 'uom_name']
    },
    auto: true,
    onSuccess(data) {
      uoms.value = data
    }
  })
  
  const updateItem = createResource({
    url: 'frappe.client.set_value',
    onSuccess() {
      isEditMode.value = false
      fetchItem.submit()
    }
  })
  
  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  function saveChanges() {
    updateItem.submit({
      doctype: 'Item',
      name: item.value.name,
      fieldname: {
        item_name: editedItem.value.item_name,
        description: editedItem.value.description,
        item_group: editedItem.value.item_group,
        stock_uom: editedItem.value.stock_uom,
        image: editedItem.value.image
      }
    })
  }
  
  function cancelEdit() {
    isEditMode.value = false
    editedItem.value = { ...item.value }
  }
  
  function confirmDelete() {
    if (confirm('Are you sure you want to delete this item?')) {
      deleteItem.submit({
        doctype: 'Item',
        name: item.value.name
      })
    }
  }
  
  const deleteItem = createResource({
    url: 'frappe.client.delete',
    onSuccess() {
      router.push('/items')
    }
  })
  
  onMounted(() => {
    fetchItem.submit()
  })
  </script>
  
  