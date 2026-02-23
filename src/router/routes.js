const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/HomePage.vue') },
      { path: 'chat', name: 'chat', component: () => import('pages/ChatPage.vue') },
      { path: 'journal', name: 'journal', component: () => import('pages/JournalPage.vue') },
      { path: 'wellness', name: 'wellness', component: () => import('pages/WellnessPage.vue') },
      { path: 'booking', name: 'booking', component: () => import('pages/BookingPage.vue') },
      { path: 'settings', name: 'settings', component: () => import('pages/SettingsPage.vue') },
    ],
  },
]

export default routes
