import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('../views/HomeView.vue'),
        meta: { title: 'Home - MedIntern' }
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/LoginView.vue'),
        meta: { title: 'Login - MedIntern', requiresGuest: true }
    },
    {
        path: '/forgot-password',
        name: 'forgot-password',
        component: () => import('../views/ForgotPasswordView.vue'),
        meta: { title: 'Reset Password - MedIntern', requiresGuest: true }
    },
    {
        path: '/verify-email',
        name: 'verify-email',
        component: () => import('../views/VerifyEmail.vue'),
        meta: { title: 'Verify Email - MedIntern' }
    },
    {
        path: '/reset-password',
        name: 'reset-password',
        component: () => import('../views/ResetPasswordView.vue'),
        meta: { title: 'Reset Password - MedIntern', requiresGuest: true }
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import('../views/DashboardView.vue'),
        meta: { title: 'Dashboard - MedIntern', requiresAuth: true }
    },
    {
        path: '/profile',
        name: 'profile',
        component: () => import('../views/ProfileView.vue'),
        meta: { title: 'Profile - MedIntern', requiresAuth: true }
    },
    {
        path: '/settings',
        name: 'settings',
        component: () => import('../views/SettingsView.vue'),
        meta: { title: 'Settings - MedIntern', requiresAuth: true }
    },
    {
        path: '/calendar',
        name: 'calendar',
        component: () => import('../views/CalendarView.vue'),
        meta: { title: 'Calendar - MedIntern', requiresAuth: true }
    },
    {
        path: '/assignments',
        name: 'assignments',
        component: () => import('../views/AssignmentBoard.vue'),
        meta: { title: 'Assignment Board - MedIntern', requiresAuth: true, roles: ['hospital_admin', 'faculty_admin'] }
    },
    {
        path: '/reports',
        name: 'reports',
        component: () => import('../views/OptimizationReports.vue'),
        meta: { title: 'Optimization Reports - MedIntern', requiresAuth: true, roles: ['faculty_admin', 'hospital_admin'] }
    },
    // Student Routes
    {
        path: '/internships',
        name: 'internships',
        component: () => import('../views/InternshipsView.vue'),
        meta: { title: 'Browse Internships - MedIntern' }
    },
    {
        path: '/internships/:id',
        name: 'internship-detail',
        component: () => import('../views/InternshipDetailView.vue'),
        meta: { title: 'Internship Details - MedIntern' }
    },
    {
        path: '/applications',
        name: 'applications',
        component: () => import('../views/ApplicationsView.vue'),
        meta: { title: 'My Applications - MedIntern', requiresAuth: true, roles: ['student'] }
    },
    {
        path: '/evaluations',
        name: 'evaluations',
        component: () => import('../views/EvaluationsView.vue'),
        meta: { title: 'My Evaluations - MedIntern', requiresAuth: true, roles: ['student'] }
    },
    {
        path: '/journal',
        name: 'journal',
        component: () => import('../views/InternshipJournalView.vue'),
        meta: { title: 'Internship Journal - MedIntern', requiresAuth: true, roles: ['student'] }
    },
    // Hospital Admin Routes
    {
        path: '/offers/create',
        name: 'create-offer',
        component: () => import('../views/CreateOffer.vue'),
        meta: { title: 'Create Offer - MedIntern', requiresAuth: true, roles: ['hospital_admin'] }
    },
    {
        path: '/offers/manage',
        name: 'manage-offers',
        component: () => import('../views/ManageOffers.vue'),
        meta: { title: 'Manage Offers - MedIntern', requiresAuth: true, roles: ['hospital_admin'] }
    },
    {
        path: '/hospital/applications',
        name: 'hospital-applications',
        component: () => import('../views/HospitalApplicationsView.vue'),
        meta: { title: 'Applications - MedIntern', requiresAuth: true, roles: ['hospital_admin'] }
    },
    {
        path: '/hospital/staff',
        name: 'hospital-staff',
        component: () => import('../views/HospitalStaffView.vue'),
        meta: { title: 'Staff Management - MedIntern', requiresAuth: true, roles: ['hospital_admin'] }
    },
    {
        path: '/hospital/internships',
        name: 'active-internships',
        component: () => import('../views/ActiveInternshipsView.vue'),
        meta: { title: 'Active Internships - MedIntern', requiresAuth: true, roles: ['hospital_admin', 'encadrant'] }
    },
    // Supervisor Routes
    {
        path: '/supervisor/students',
        name: 'supervisor-students',
        component: () => import('../views/SupervisorStudentsView.vue'),
        meta: { title: 'My Students - MedIntern', requiresAuth: true, roles: ['encadrant'] }
    },
    {
        path: '/supervisor/evaluations',
        name: 'supervisor-evaluations',
        component: () => import('../views/SupervisorEvaluationsView.vue'),
        meta: { title: 'Evaluations - MedIntern', requiresAuth: true, roles: ['encadrant'] }
    },
    // Faculty Admin Routes
    {
        path: '/faculty/students',
        name: 'faculty-students',
        component: () => import('../views/FacultyStudentsView.vue'),
        meta: { title: 'Students - MedIntern', requiresAuth: true, roles: ['faculty_admin'] }
    },
    {
        path: '/faculty/offers',
        name: 'faculty-offers',
        component: () => import('../views/FacultyOffersView.vue'),
        meta: { title: 'Validate Offers - MedIntern', requiresAuth: true, roles: ['faculty_admin'] }
    },
    {
        path: '/faculty/reports',
        name: 'faculty-reports',
        component: () => import('../views/FacultyReportsView.vue'),
        meta: { title: 'Reports - MedIntern', requiresAuth: true, roles: ['faculty_admin'] }
    },
    // Messaging
    {
        path: '/messages',
        name: 'messages',
        component: () => import('../views/MessagesView.vue'),
        meta: { title: 'Messages - MedIntern', requiresAuth: true }
    },
    // 404
    {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: () => import('../views/NotFoundView.vue'),
        meta: { title: 'Page Not Found - MedIntern' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) return savedPosition
        return { top: 0 }
    }
})

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    // Set page title
    document.title = to.meta.title || 'MedIntern - Hospital Internship Platform'

    // Wait for auth to initialize before making any decisions
    if (!authStore.isInitialized) {
        await authStore.waitForInit()
        // Also wait a tick for the state to propagate
        await new Promise(resolve => setTimeout(resolve, 50))
    }

    // Check if route requires authentication
    if (to.meta.requiresAuth && !authStore.isLoggedIn) {
        next({ name: 'login', query: { redirect: to.fullPath } })
        return
    }

    // Check if route requires guest (non-authenticated)
    if (to.meta.requiresGuest && authStore.isLoggedIn) {
        next({ name: 'dashboard' })
        return
    }

    // Check role requirements
    if (to.meta.roles && to.meta.roles.length > 0 && authStore.isLoggedIn) {
        // Ensure user data is loaded
        if (!authStore.user) {
            try {
                await authStore.loadUser()
            } catch (error) {
                console.error('Failed to load user for role check:', error)
            }
        }

        const userRole = authStore.userRole
        if (userRole && !to.meta.roles.includes(userRole)) {
            console.warn(`Role ${userRole} not allowed for ${to.path}, redirecting to dashboard`)
            next({ name: 'dashboard' })
            return
        }
    }

    next()
})

export default router
