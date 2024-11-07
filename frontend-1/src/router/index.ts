import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import InstructorDashboard from '../views/InstructorDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import AdminProjectStats from '../views/AdminProjectStats.vue'
import AdminProject from '../views/AdminProject.vue'
import MilestoneDetailView from '../views/MilestoneDetailView.vue'
import InstructorStudentView from '../views/InstructorStudentView.vue'
import InstructorMilestoneView from '../views/InstructorMilestoneView.vue'

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
      path: '/admin/stats',
      name: 'admin-project-stats',
      component: AdminProjectStats
    },
    {
      path: '/admin/projects',
      name: 'admin-project',
      component: AdminProject
    },
    {
      path: '/instructor',
      name: 'instructor',
      component: InstructorDashboard
    },
    {
      path: '/instructor/milestones',
      name: 'instructor-milestones',
      component: InstructorMilestoneView
    },
    {
      path: '/instructor/students',
      name: 'instructor-students',
      component: InstructorStudentView
    },
    {
      path: '/instructor/github',
      name: 'instructor-github',
      component: InstructorDashboard
    },
    {
      path: '/student',
      name: 'student',
      component: StudentDashboard
    },
    {
      path: '/student/milestones/:id',
      name: 'milestone-detail',
      component: MilestoneDetailView,
      props: true
    }
  ]
})

export default router