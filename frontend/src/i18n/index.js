// i18n/index.js - Simple internationalization for French/English
import { ref, computed } from 'vue'

const currentLocale = ref(localStorage.getItem('locale') || 'en')

const translations = {
    en: {
        // Navigation
        'nav.home': 'Home',
        'nav.dashboard': 'Dashboard',
        'nav.internships': 'Internships',
        'nav.applications': 'My Applications',
        'nav.evaluations': 'Evaluations',
        'nav.messages': 'Messages',
        'nav.profile': 'Profile',
        'nav.settings': 'Settings',
        'nav.logout': 'Sign out',
        'nav.login': 'Log in',

        // Settings
        'settings.title': 'Settings',
        'settings.subtitle': 'Manage your account preferences',
        'settings.appearance': 'Appearance',
        'settings.theme': 'Theme',
        'settings.theme.light': 'Light',
        'settings.theme.dark': 'Dark',
        'settings.theme.system': 'System',
        'settings.language': 'Language',
        'settings.language.en': 'English',
        'settings.language.fr': 'Français',
        'settings.security': 'Security',
        'settings.password': 'Change Password',
        'settings.password.current': 'Current Password',
        'settings.password.new': 'New Password',
        'settings.password.confirm': 'Confirm Password',
        'settings.password.update': 'Update Password',
        'settings.notifications': 'Notifications',
        'settings.notifications.email': 'Email Notifications',
        'settings.notifications.push': 'Push Notifications',

        // Common
        'common.save': 'Save',
        'common.cancel': 'Cancel',
        'common.delete': 'Delete',
        'common.edit': 'Edit',
        'common.loading': 'Loading...',
        'common.error': 'An error occurred',
        'common.success': 'Success',

        // Dashboard
        'dashboard.welcome': 'Welcome back',
        'dashboard.overview': 'Overview',

        // Internships
        'internships.title': 'Browse Internships',
        'internships.search': 'Search internships...',
        'internships.apply': 'Apply Now',
        'internships.applied': 'Applied',
        'internships.slots': 'slots available',

        // Applications
        'applications.title': 'My Applications',
        'applications.status.pending': 'Pending',
        'applications.status.accepted': 'Accepted',
        'applications.status.rejected': 'Rejected',
        'applications.withdraw': 'Withdraw',
    },
    fr: {
        // Navigation
        'nav.home': 'Accueil',
        'nav.dashboard': 'Tableau de bord',
        'nav.internships': 'Stages',
        'nav.applications': 'Mes Candidatures',
        'nav.evaluations': 'Évaluations',
        'nav.messages': 'Messages',
        'nav.profile': 'Profil',
        'nav.settings': 'Paramètres',
        'nav.logout': 'Déconnexion',
        'nav.login': 'Connexion',

        // Settings
        'settings.title': 'Paramètres',
        'settings.subtitle': 'Gérer les préférences de votre compte',
        'settings.appearance': 'Apparence',
        'settings.theme': 'Thème',
        'settings.theme.light': 'Clair',
        'settings.theme.dark': 'Sombre',
        'settings.theme.system': 'Système',
        'settings.language': 'Langue',
        'settings.language.en': 'English',
        'settings.language.fr': 'Français',
        'settings.security': 'Sécurité',
        'settings.password': 'Changer le mot de passe',
        'settings.password.current': 'Mot de passe actuel',
        'settings.password.new': 'Nouveau mot de passe',
        'settings.password.confirm': 'Confirmer',
        'settings.password.update': 'Mettre à jour',
        'settings.notifications': 'Notifications',
        'settings.notifications.email': 'Notifications par email',
        'settings.notifications.push': 'Notifications push',

        // Common
        'common.save': 'Enregistrer',
        'common.cancel': 'Annuler',
        'common.delete': 'Supprimer',
        'common.edit': 'Modifier',
        'common.loading': 'Chargement...',
        'common.error': 'Une erreur est survenue',
        'common.success': 'Succès',

        // Dashboard
        'dashboard.welcome': 'Bienvenue',
        'dashboard.overview': 'Aperçu',

        // Internships
        'internships.title': 'Parcourir les stages',
        'internships.search': 'Rechercher des stages...',
        'internships.apply': 'Postuler',
        'internships.applied': 'Candidature envoyée',
        'internships.slots': 'places disponibles',

        // Applications
        'applications.title': 'Mes Candidatures',
        'applications.status.pending': 'En attente',
        'applications.status.accepted': 'Acceptée',
        'applications.status.rejected': 'Refusée',
        'applications.withdraw': 'Retirer',
    }
}

export function useI18n() {
    const locale = computed(() => currentLocale.value)

    const t = (key) => {
        return translations[currentLocale.value]?.[key] || translations['en'][key] || key
    }

    const setLocale = (newLocale) => {
        currentLocale.value = newLocale
        localStorage.setItem('locale', newLocale)
        document.documentElement.lang = newLocale
    }

    const availableLocales = ['en', 'fr']

    return {
        locale,
        t,
        setLocale,
        availableLocales
    }
}

export default { useI18n }
