<template>
  <div class="container mx-auto px-4 py-8 pb-20 mt-15">
    <!-- Header with filters -->
    <div class="flex flex-col space-y-4 mb-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-900">Items</h1>
        <button
          @click="openAddItemDialog"
          class="bg-blue-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg inline-flex items-center"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Add Item
        </button>
      </div>
      <!-- Search Bar -->
      <div class="flex items-center">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by item name"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
        />
      </div>
    </div>

    <!-- Items List -->
    <div class="space-y-4">
      <router-link
        v-for="item in displayedItems"
        :key="item.name"
        :to="`/item/${item.name}`"
        class="block bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow"
      >
        <div class="flex items-center p-4">
          <div v-if="item.image" class="w-16 h-16 flex-shrink-0">
            <img
              :src="item.image"
              :alt="item.item_name"
              class="w-full h-full object-cover rounded-lg"
            />
          </div>
          <div class="ml-4 flex-grow">
            <h2 class="text-lg font-semibold text-gray-900">
              {{ item.item_name }}
            </h2>
            <p class="text-sm text-gray-500">Code: {{ item.item_code }}</p>
            <p class="text-sm text-gray-500">Group: {{ item.item_group }}</p>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click.prevent="deleteItem(item.name)"
              class="p-2 text-gray-400 hover:text-red-600 rounded-full hover:bg-red-50"
            >
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-6">
      <button
        @click="previousPage"
        :disabled="currentPage === 1"
        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
      >
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button
        @click="nextPage"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
      >
        Next
      </button>
    </div>

    <!-- Add Item Dialog -->
    <div
      v-if="isAddItemDialogOpen"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50"
    >
      <div class="bg-white p-8 rounded-lg shadow-xl max-w-md w-full m-4">
        <h2 class="text-2xl font-bold mb-4">Add New Item</h2>
        <form @submit.prevent="submitItem">
          <div class="mb-4">
            <label
              for="item_code"
              class="block text-sm font-medium text-gray-700"
              >Item Code <span class="text-red-500">*</span></label
            >
            <input
              type="text"
              id="item_code"
              v-model="newItem.item_code"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            />
          </div>

          <div class="mb-4">
            <label
              for="gst_hsn_code"
              class="block text-sm font-medium text-gray-700"
            >
              HSN/SAC Code <span class="text-red-500">*</span>
            </label>
            <select
              id="gst_hsn_code"
              v-model="newItem.gst_hsn_code"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            >
              <option value="">Select HSN/SAC Code</option>
              <option
                v-for="hsnCode in searchHSNCode.data"
                :key="hsnCode.name"
                :value="hsnCode.name"
              >
                {{ hsnCode.hns_code }}
              </option>
            </select>
          </div>

          <div class="mb-4">
            <label
              for="item_name"
              class="block text-sm font-medium text-gray-700"
              >Item Name <span class="text-red-500">*</span></label
            >
            <input
              type="text"
              id="item_name"
              v-model="newItem.item_name"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            />
          </div>
          <div class="mb-4">
            <label
              for="item_group"
              class="block text-sm font-medium text-gray-700"
              >Item Group <span class="text-red-500">*</span></label
            >
            <select
              id="item_group"
              v-model="newItem.item_group"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            >
              <option value="All Item Groups">All Item Groups</option>
              <option
                v-for="group in itemGroups"
                :key="group.name"
                :value="group.name"
              >
                {{ group.item_group_name }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label
              for="stock_uom"
              class="block text-sm font-medium text-gray-700"
              >UOM <span class="text-red-500">*</span></label
            >
            <select
              id="stock_uom"
              v-model="newItem.stock_uom"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            >
              <option value="">Select UOM</option>
              <option value="Nos">Nos</option>
              <option v-for="uom in uoms" :key="uom.name" :value="uom.name">
                {{ uom.uom_name }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label
              for="description"
              class="block text-sm font-medium text-gray-700"
              >Description</label
            >
            <textarea
              id="description"
              v-model="newItem.description"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            ></textarea>
          </div>

          <div class="mb-4">
            <label for="image" class="block text-sm font-medium text-gray-700">
              Image
            </label>
            <input
              type="file"
              id="image"
              @change="handleImageUpload"
              accept="image/*"
              class="mt-1 block w-full"
            />
            <input
              type="text"
              v-model="newItem.image_url"
              placeholder="Or enter image URL"
              class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            />

            <!-- Preview Uploaded Image -->
            <!-- <img
      v-if="newItem.image_preview"
      :src="newItem.image_preview"
      alt="Uploaded Image"
      class="mt-2 w-32 h-32 object-cover rounded-md border"
    /> -->
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
              class="px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-indigo-700"
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
import { ref, onMounted, computed } from 'vue'
import { createResource } from 'frappe-ui'
import { PlusIcon, TrashIcon } from 'lucide-vue-next'

const items = ref([])
const itemGroups = ref([])
const uoms = ref([])
const newItem = ref({
  item_code: '',
  item_name: '',
  item_group: 'All Item Groups',
  stock_uom: '',
  description: '',
  image: null,
  image_url: '',
  image_preview: null,
  gst_hsn_code: '',
})
const isAddItemDialogOpen = ref(false)
const hsnCodeSuggestions = ref([])

// Pagination
const itemsPerPage = 20
const currentPage = ref(1)
const searchQuery = ref('')

const fetchItems = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'Item',
    fields: ['name', 'item_code', 'item_name', 'item_group', 'image'],
    limit_page_length: 0,
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
    fields: ['name', 'item_group_name'],
  },
  auto: true,
  onSuccess(data) {
    itemGroups.value = data
  },
})

const fetchUOMs = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'UOM',
    fields: ['name', 'uom_name'],
  },
  auto: true,
  onSuccess(data) {
    uoms.value = data
  },
})

// const searchHSNCode = createResource({
//   url: 'frappe.client.get_list',
//   params: {
//     doctype: 'GST HSN Code',
//     fields: ['name', 'hsn_code'],
//   },
//   auto: true,
//   onSuccess(data) {
//     hsnCodeSuggestions.value = data
//   },
// })

const searchHSNCode = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'GST HSN Code',
    fields: ['name', 'hns_code'],
  },
  auto: true,
  onSuccess(data) {
    uoms.value = data
  },
})

const addItem = createResource({
  url: 'frappe.client.insert',
  onSuccess() {
    newItem.value = {
      item_code: '',
      item_name: '',
      item_group: 'All Item Groups',
      stock_uom: '',
      description: '',
      image: null,
      image_url: '',
      gst_hsn_code: '',
    }
    isAddItemDialogOpen.value = false
    fetchItems.reload()
  },
})

const deleteItemResource = createResource({
  url: 'frappe.client.delete',
  onSuccess() {
    fetchItems.reload()
  },
})

// Computed Properties
const filteredItems = computed(() => {
  if (!searchQuery.value) {
    return items.value
  }
  const lowerSearchQuery = searchQuery.value.toLowerCase()
  return items.value.filter((item) =>
    item.item_name.toLowerCase().includes(lowerSearchQuery)
  )
})

const totalPages = computed(() => {
  return Math.ceil(filteredItems.value.length / itemsPerPage)
})

const displayedItems = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  return filteredItems.value.slice(startIndex, endIndex)
})

// Pagination Methods
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function openAddItemDialog() {
  isAddItemDialogOpen.value = true
}

function closeAddItemDialog() {
  isAddItemDialogOpen.value = false
}


function onsearchHSNCode() {
  if (newItem.value.gst_hsn_code.length > 2) {
    searchHSNCode.submit({
      filters: { hsn_code: ['like', `%${newItem.value.gst_hsn_code}%`] },
    })
  } else {
    hsnCodeSuggestions.value = []
  }
}

function selectHSNCode(suggestion) {
  newItem.value.gst_hsn_code = suggestion.hsn_code
  hsnCodeSuggestions.value = []
}


function handleImageUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // Create a preview of the image
  newItem.value.image_preview = URL.createObjectURL(file)

  const formData = new FormData()
  formData.append('file', file)
  formData.append('doctype', 'Item')
  formData.append('docname', 'new-item') 
  formData.append('fieldname', 'image')
  formData.append('is_private', 0)

  fetch('/api/method/upload_file', {
    method: 'POST',
    body: formData,
    credentials: 'include',
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message && data.message.file_url) {
        newItem.value.image_url = data.message.file_url
      }
    })
    .catch((error) => console.error('File upload error:', error))
}

function submitItem() {
  const itemData = { ...newItem.value }

  if (itemData.image_url && itemData.image_url.trim() !== '') {
    itemData.image = itemData.image_url
  }

  delete itemData.image_url
  delete itemData.image_preview 

  addItem.submit({
    doc: {
      doctype: 'Item',
      ...itemData,
    },
  })
}

function deleteItem(itemName) {
  if (confirm('Are you sure you want to delete this item?')) {
    deleteItemResource.submit({
      doctype: 'Item',
      name: itemName,
    })
  }
}

onMounted(() => {
  fetchItems.reload()
  fetchItemGroups.reload()
  fetchUOMs.reload()
})
</script>
