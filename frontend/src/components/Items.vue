<template>
  <div class="container mx-auto px-4 py-8 pb-20">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Items</h1>
      <button @click="openAddItemDialog" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-flex items-center">
        <PlusIcon class="w-4 h-4 mr-2" />
        Add Item
      </button>
    </div>

    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="item in items" :key="item.name" class="bg-white shadow-md rounded-lg overflow-hidden">
        <div class="p-4">
          <h2 class="text-xl font-semibold text-gray-800">{{ item.item_name }}</h2>
          <!-- <p class="text-sm text-gray-600">Code: {{ item.item_code }}</p> -->
        </div>
        <div class="relative">
          <img
            :src="item.image || '/placeholder.svg?height=200&width=200'"
            :alt="item.item_name"
            class="w-full h-48 object-contain"
          />
          <button @click="deleteItem(item.name)" class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1">
            <TrashIcon class="w-4 h-4" />
          </button>
        </div>
        <div class="p-4">
          <p class="text-sm text-gray-600">{{ item.description || 'No description available.' }}</p>
          <div class="mt-4 flex justify-between text-sm text-gray-500">
            <span>Group: {{ item.item_group }}</span>
            <span>UOM: {{ item.stock_uom }}</span>
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
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeAddItemDialog" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded">
              Cancel
            </button>
            <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
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
import { PlusIcon, TrashIcon } from 'lucide-vue-next'

const items = ref([])
const itemGroups = ref([])
const uoms = ref([])
const newItem = ref({ item_code: '', item_name: '', item_group: '', stock_uom: 'Nos', description: '', image: null, image_url: '' })
const isAddItemDialogOpen = ref(false)

const fetchItems = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Item',
    fields: ['name', 'item_code', 'item_name', 'item_group', 'stock_uom', 'description', 'image']
  },
  auto: true,
  onSuccess(data) {
    items.value = data
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

const addItem = createResource({
  url: 'frappe.client.insert',
  onSuccess() {
    newItem.value = { item_code: '', item_name: '', item_group: '', stock_uom: 'Nos', description: '', image: null, image_url: '' }
    isAddItemDialogOpen.value = false
    fetchItems.reload()
  }
})

const deleteItemResource = createResource({
  url: 'frappe.client.delete',
  onSuccess() {
    fetchItems.reload()
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
    const reader = new FileReader()
    reader.onload = (e) => {
      newItem.value.image = e.target.result
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

function deleteItem(itemName) {
  if (confirm('Are you sure you want to delete this item?')) {
    deleteItemResource.submit({
      doctype: 'Item',
      name: itemName
    })
  }
}

onMounted(() => {
  fetchItems.reload()
  fetchItemGroups.reload()
  fetchUOMs.reload()
})
</script>

