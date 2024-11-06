import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import InstructorDashboard from '../views/InstructorDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard
    },
    {
      path: '/instructor',
      name: 'instructor',
      component: InstructorDashboard
    },
    {
      path: '/student',
      name: 'student',
      component: StudentDashboard
    }
  ]
})

export default router