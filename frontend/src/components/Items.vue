<template>
  <div class="container mx-auto px-4 py-8 pb-20">
    <!-- Header with filters -->
    <div class="flex flex-col space-y-4 mb-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-900">Items</h1>
        <button
          v-if="!selectedItem"
          @click="openAddItemDialog"
          class="bg-blue-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg inline-flex items-center"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Add Item
        </button>
        <button
          v-else
          @click="selectedItem = null"
          class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-lg inline-flex items-center"
        >
          <ChevronLeftIcon class="w-4 h-4 mr-2" />
          Back to List
        </button>
      </div>
    </div>

    <!-- Items List -->
    <div v-if="!selectedItem" class="space-y-4">
      <div
        v-for="item in items"
        :key="item.name"
        @click="selectItem(item)"
        class="block bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
      >
        <div class="flex items-center p-4">
          <div class="w-16 h-16 flex-shrink-0">
            <img
              :src="item.image || '/placeholder.svg?height=100&width=100'"
              :alt="item.item_name"
              class="w-full h-full object-cover rounded-lg"
            />
          </div>
          <div class="ml-4 flex-grow">
            <h2 class="text-lg font-semibold text-gray-900">{{ item.item_name }}</h2>
            <p class="text-sm text-gray-500">Code: {{ item.item_code || 'N/A' }}</p>
            <p class="text-sm text-gray-500">Group: {{ item.item_group }}</p>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click.stop="deleteItem(item.name)"
              class="p-2 text-gray-400 hover:text-red-600 rounded-full hover:bg-red-50"
            >
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Item Details -->
    <div v-else>
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="md:flex">
          <!-- Image Section -->
          <div class="md:w-1/2 relative aspect-w-16 aspect-h-9 md:aspect-none md:h-[400px]">
            <img 
              :src="selectedItem.image || '/placeholder.svg?height=400&width=400'" 
              :alt="selectedItem.item_name"
              class="w-full h-full object-cover"
            />
          </div>

          <!-- Item Details -->
          <div class="md:w-1/2 p-6 space-y-6">
            <div v-if="!isEditMode">
              <div>
                <h2 class="text-2xl font-semibold mb-2">{{ selectedItem.item_name }}</h2>
                <p class="text-gray-600">Code: {{ selectedItem.item_code }}</p>
              </div>

              <div class="mt-4">
                <h3 class="text-lg font-semibold mb-2">Description</h3>
                <p class="text-gray-600">{{ selectedItem.description || 'No description available.' }}</p>
              </div>

              <div class="grid grid-cols-2 gap-4 mt-6">
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-500">Item Group</p>
                  <p class="font-medium">{{ selectedItem.item_group }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-500">UOM</p>
                  <p class="font-medium">{{ selectedItem.stock_uom }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-500">Created By</p>
                  <p class="font-medium">{{ selectedItem.owner }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <p class="text-sm text-gray-500">Last Modified</p>
                  <p class="font-medium">{{ formatDate(selectedItem.modified) }}</p>
                </div>
              </div>

              <div class="mt-6 text-sm text-gray-500">
                <p>Created: {{ formatDate(selectedItem.creation) }}</p>
              </div>

              <div class="mt-6 flex justify-end space-x-2">
                <button 
                  @click="isEditMode = true" 
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Edit
                </button>
                <button 
                  @click="confirmDelete(selectedItem.name)" 
                  class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
                >
                  Delete
                </button>
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
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
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

    <!-- Add Item Dialog -->
    <div v-if="isAddItemDialogOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg shadow-xl max-w-md w-full m-4">
        <h2 class="text-2xl font-bold mb-4">Add New Item</h2>
        <form @submit.prevent="submitItem">
          <div class="mb-4">
            <label for="item_code" class="block text-sm font-medium text-gray-700">Item Code</label>
            <input type="text" id="item_code" v-model="newItem.item_code" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
          </div>
          <div class="mb-4">
            <label for="item_name" class="block text-sm font-medium text-gray-700">Item Name</label>
            <input type="text" id="item_name" v-model="newItem.item_name" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
          </div>
          <div class="mb-4">
            <label for="item_group" class="block text-sm font-medium text-gray-700">Item Group</label>
            <select id="item_group" v-model="newItem.item_group" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
              <option value="">Select an Item Group</option>
              <option v-for="group in itemGroups" :key="group.name" :value="group.name">
                {{ group.item_group_name }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label for="stock_uom" class="block text-sm font-medium text-gray-700">UOM</label>
            <select id="stock_uom" v-model="newItem.stock_uom" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
              <option value="Nos">Nos</option>
              <option v-for="uom in uoms" :key="uom.name" :value="uom.name">
                {{ uom.uom_name }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
            <textarea id="description" v-model="newItem.description" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"></textarea>
          </div>
          <div class="mb-4">
            <label for="image" class="block text-sm font-medium text-gray-700">Image</label>
            <input type="file" id="image" @change="handleImageUpload" accept="image/*" class="mt-1 block w-full">
            <input type="text" v-model="newItem.image_url" placeholder="Or enter image URL" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
          </div>
          <div class="flex justify-end space-x-2 mt-6">
            <button 
              type="button" 
              @click="closeAddItemDialog"
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button 
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Add Item
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import { PlusIcon, TrashIcon, ChevronLeftIcon } from 'lucide-vue-next'

const items = ref([])
const selectedItem = ref(null)
const itemGroups = ref([])
const uoms = ref([])
const newItem = ref({ item_code: '', item_name: '', item_group: '', stock_uom: 'Nos', description: '', image: null, image_url: '' })
const isAddItemDialogOpen = ref(false)
const isEditMode = ref(false)
const editedItem = ref({})
const imageFile = ref(null)

const fetchItems = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Item',
    fields: ['name', 'item_code', 'item_name', 'item_group', 'stock_uom', 'description', 'image', 'owner', 'creation', 'modified'],
  },
  auto: true,
  onSuccess(data) {
    items.value = data
  },
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

const addItem = createResource({
  url: 'frappe.client.insert',
  onSuccess() {
    newItem.value = { item_code: '', item_name: '', item_group: '', stock_uom: 'Nos', description: '', image: null, image_url: '' }
    isAddItemDialogOpen.value = false
    fetchItems.reload()
  }
})

const updateItem = createResource({
  url: 'frappe.client.set_value',
  onSuccess() {
    isEditMode.value = false
    fetchItems.reload()
    selectedItem.value = { ...editedItem.value }
  }
})

const deleteItemResource = createResource({
  url: 'frappe.client.delete',
  onSuccess() {
    fetchItems.reload()
    selectedItem.value = null
  }
})

function openAddItemDialog() {
  isAddItemDialogOpen.value = true
}

function closeAddItemDialog() {
  isAddItemDialogOpen.value = false
}

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      if (isEditMode.value) {
        editedItem.value.image = e.target.result
      } else {
        newItem.value.image = e.target.result
      }
    }
    reader.readAsDataURL(file)
  }
}

function submitItem() {
  const itemData = { ...newItem.value }
  if (itemData.image_url) {
    itemData.image = itemData.image_url
  }
  delete itemData.image_url

  addItem.submit({
    doc: {
      doctype: 'Item',
      ...itemData
    }
  })
}

function selectItem(item) {
  selectedItem.value = item
}

function saveChanges() {
  let imageUrl = editedItem.value.image

  if (imageFile.value) {
    // Upload the image file and get the URL
    const formData = new FormData()
    formData.append('file', imageFile.value)
    formData.append('doctype', 'Item')
    formData.append('docname', selectedItem.value.name)
    formData.append('fieldname', 'image')

    fetch('/api/method/upload_file', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(result => {
        if (result.message && result.message.file_url) {
          imageUrl = result.message.file_url
        }
        updateItemWithImage(imageUrl)
      })
      .catch(error => {
        console.error('Error uploading image:', error)
        updateItemWithImage(imageUrl)
      })
  } else {
    updateItemWithImage(imageUrl)
  }
}

function updateItemWithImage(imageUrl) {
  updateItem.submit({
    doctype: 'Item',
    name: selectedItem.value.name,
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
  editedItem.value = { ...selectedItem.value }
  imageFile.value = null
}

function confirmDelete(itemName) {
  if (confirm('Are you sure you want to delete this item?')) {
    deleteItemResource.submit({
      doctype: 'Item',
      name: itemName
    })
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchItems.reload()
  fetchItemGroups.reload()
  fetchUOMs.reload()
})
</script>

