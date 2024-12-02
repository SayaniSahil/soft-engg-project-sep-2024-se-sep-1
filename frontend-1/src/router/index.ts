import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import InstructorDashboard from '../views/InstructorDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import AdminProjectStats from '../views/AdminProjectStats.vue'
import AdminProject from '../views/AdminProject.vue'
import MilestoneDetailView from '../views/MilestoneDetailView.vue'
import InstructorStudentView from '../views/InstructorStudentView.vue'
import InstructorMilestoneView from '../views/InstructorMilestoneView.vue'
import InstructorCommitHistory from '../views/InstructorCommitHistory.vue'

const routes = [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/register-instructor',
      name: 'register-instructor',
      component: Register
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
      component: InstructorCommitHistory
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
    },
    {
      path: '/:pathMatch(.*)*', // Catch-all route for undefined paths
      redirect: '/'
    }
]

const baseUrl = '/';
console.log('BASE_URL:', baseUrl);

const router = createRouter({
  history: createWebHistory(baseUrl),
  routes
})

router.beforeEach((to, from, next) => {
  const role = localStorage.getItem('role')
  const name = localStorage.getItem('username')
  const id = localStorage.getItem('id')

  console.log(to.name, role, name, id)
  if((!role || !name || !id) && (to.name !== 'login' && to.name !== 'register-instructor')){
    localStorage.clear()
    next({ name: 'login' })
  }else if(to.name === 'login' && role){
    console.log('Redirecting to', role)
    next({ name: role })
  }
  let path = to.name?.toString();
  path = path?.split('-')[0];

  if (path.includes("instructor") && role !== 'instructor') {
    // Wrong dashboard for role
    next({ name: role === 'student' ? 'student' : role === 'admin' ? 'admin' : 'login' })
  } else if (path.includes("student") && role !== 'student') {
    // Wrong dashboard for role
    next({ name: role === 'instructor' ? 'instructor' : role === 'admin' ? 'admin' : 'login' })
  } else if (path.includes("admin") && role !== 'admin') {
    // Wrong dashboard for role
    next({ name: role === 'student' ? 'student' : role === 'instructor' ? 'instructor' : 'login' })
  } else {
    // Continue to route
    next()
  }
})

export default router