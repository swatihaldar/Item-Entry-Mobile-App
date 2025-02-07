<template>
    <div class="bg-gray-100 min-h-screen">
      <div class="max-w-7xl mx-auto p-4">
        <div v-if="item" class="bg-white rounded-lg shadow-lg overflow-hidden">
          <!-- Header with back button and edit/delete options -->
          <div class="relative bg-indigo-600 text-white p-4">
            <button 
              @click="$router.back()" 
              class="absolute top-4 left-4 bg-white rounded-full p-2 shadow-lg z-10"
            >
              <ChevronLeftIcon class="h-6 w-6 text-gray-600" />
            </button>
            <h1 class="text-2xl font-bold text-center">{{ item.item_name }}</h1>
            <div class="absolute top-4 right-4 flex space-x-2">
              <button 
                @click="isEditMode = true" 
                class="bg-green-500 text-white rounded-full p-2 hover:bg-green-600 transition-colors"
              >
                <EditIcon class="h-5 w-5" />
              </button>
              <button 
                @click="confirmDelete" 
                class="bg-red-500 text-white rounded-full p-2 hover:bg-red-600 transition-colors"
              >
                <TrashIcon class="h-5 w-5" />
              </button>
            </div>
          </div>
  
          <div class="md:flex">
            <!-- Image Section -->
            <div class="md:w-1/2 relative aspect-w-16 aspect-h-9 md:aspect-none md:h-[600px]">
              <img 
                :src="item.image || '/placeholder.svg?height=600&width=600'" 
                :alt="item.item_name"
                class="w-full h-full object-cover"
              />
            </div>
  
            <!-- Item Details -->
            <div class="md:w-1/2 p-6 space-y-6">
              <div v-if="!isEditMode">
                <div>
                  <h2 class="text-2xl font-semibold mb-2">{{ item.item_name }}</h2>
                  <p class="text-gray-600">Code: {{ item.item_code }}</p>
                </div>
  
                <div class="mt-4">
                  <h3 class="text-lg font-semibold mb-2">Description</h3>
                  <p class="text-gray-600">{{ item.description || 'No description available.' }}</p>
                </div>
  
                <div class="grid grid-cols-2 gap-4 mt-6">
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">Item Group</p>
                    <p class="font-medium">{{ item.item_group }}</p>
                  </div>
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">UOM</p>
                    <p class="font-medium">{{ item.stock_uom }}</p>
                  </div>
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">Created By</p>
                    <p class="font-medium">{{ item.owner }}</p>
                  </div>
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">Last Modified</p>
                    <p class="font-medium">{{ formatDate(item.modified) }}</p>
                  </div>
                </div>
  
                <div class="mt-6 text-sm text-gray-500">
                  <p>Created: {{ formatDate(item.creation) }}</p>
                </div>
              </div>
  
              <!-- Edit Form -->
              <form v-else @submit.prevent="saveChanges" class="space-y-6">
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
                  <label class="block text-sm font-medium text-gray-700">Image</label>
                  <div class="mt-1 flex items-center space-x-4">
                    <input 
                      type="file" 
                      accept="image/*" 
                      @change="handleImageUpload" 
                      class="hidden" 
                      ref="fileInput"
                    />
                    <button 
                      type="button" 
                      @click="$refs.fileInput.click()" 
                      class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                    >
                      Choose File
                    </button>
                    <span v-if="imageFile">{{ imageFile.name }}</span>
                  </div>
                  <p class="mt-2 text-sm text-gray-500">Or enter image URL:</p>
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
  
        <!-- Loading State -->
        <div v-else class="flex justify-center items-center h-64">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
        </div>
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
  const imageFile = ref(null)
  
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
  
  function handleImageUpload(event) {
    const file = event.target.files[0]
    if (file) {
      imageFile.value = file
      const reader = new FileReader()
      reader.onload = (e) => {
        editedItem.value.image = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
  
  async function saveChanges() {
    let imageUrl = editedItem.value.image
  
    if (imageFile.value) {
      // Upload the image file and get the URL
      const formData = new FormData()
      formData.append('file', imageFile.value)
      formData.append('doctype', 'Item')
      formData.append('docname', item.value.name)
      formData.append('fieldname', 'image')
  
      try {
        const response = await fetch('/api/method/upload_file', {
          method: 'POST',
          body: formData,
        })
        const result = await response.json()
        if (result.message && result.message.file_url) {
          imageUrl = result.message.file_url
        }
      } catch (error) {
        console.error('Error uploading image:', error)
      }
    }
  
    updateItem.submit({
      doctype: 'Item',
      name: item.value.name,
      fieldname: {
        item_name: editedItem.value.item_name,
        description: editedItem.value.description,
        item_group: editedItem.value.item_group,
        stock_uom: editedItem.value.stock_uom,
        image: imageUrl
      }
    })
  }
  
  function cancelEdit() {
    isEditMode.value = false
    editedItem.value = { ...item.value }
    imageFile.value = null
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
  
  