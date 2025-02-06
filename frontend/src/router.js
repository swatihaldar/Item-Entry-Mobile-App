import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    name: 'Login',
    path: '/account/login',
    component: () => import('@/pages/Login.vue'),
  },
  {
    path: '/items',
    name: 'Items',
    component: () => import('@/components/Items.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/components/Profile.vue')
  },
  {
    path: '/item/:id',
    name: 'ItemDetails',
    component: () => import('@/components/ItemDetails.vue')
  },
]

let router = createRouter({
  history: createWebHistory('/erp_mobile'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    isLoggedIn = false
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !isLoggedIn) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
