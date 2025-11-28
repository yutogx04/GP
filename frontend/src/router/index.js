import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import VerifyEmail from '../views/VerifyEmail.vue'
import Dashboard from '../views/Dashboard.vue'
import OffersList from '../views/OffersList.vue'
import OfferDetail from '../views/OfferDetail.vue'
import CreateOffer from '../views/CreateOffer.vue'
import Profile from '../views/Profile.vue'
import { useAuthStore } from '../store/auth'


const routes = [
{ path: '/', name: 'home', component: Home },
{ path: '/login', name: 'login', component: Login },
{ path: '/register', name: 'register', component: Register },
{ path: '/verify-email', name: 'verify-email', component: VerifyEmail },
{ path: '/offers', name: 'offers', component: OffersList },
{ path: '/offers/:id', name: 'offer-detail', component: OfferDetail, props: true },
{ path: '/profile', name: 'profile', component: Profile, meta: { requiresAuth: true } },
{ path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
{ path: '/create-offer', name: 'create-offer', component: CreateOffer, meta: { requiresAuth: true, role: 'hospital_admin' } },
]


const router = createRouter({
history: createWebHistory(),
routes,
})


router.beforeEach((to, from, next) => {
const auth = useAuthStore()
const requiresAuth = to.meta.requiresAuth
if (requiresAuth && !auth.isLoggedIn) {
return next({ name: 'login', query: { next: to.fullPath } })
}
const requiredRole = to.meta.role
if (requiredRole) {
if (!auth.isLoggedIn) return next({ name: 'login' })
if (auth.user?.role !== requiredRole) return next({ name: 'home' })
}
next()
})


export default router