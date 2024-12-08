import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminProjectStats from '../views/AdminProjectStats.vue'
import AdminProject from '../views/AdminProject.vue'
import Instructor from '../views/Instructor.vue'
import Student from '../views/Student.vue'

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
      path: '/instructor/:type',
      name: 'instructor',
      component: Instructor
    },
    {
      path: '/student/:type/:id',
      name: 'student',
      component: Student
    },
    {
      path: '/:pathMatch(.*)*', // Catch-all route for undefined paths
      redirect: '/'
    }
]

const baseUrl = '/';
//console.log('BASE_URL:', baseUrl);

const router = createRouter({
  history: createWebHistory(baseUrl),
  routes
})

router.beforeEach((to, from, next) => {
  const role = localStorage.getItem('role')
  const name = localStorage.getItem('username')
  const id = localStorage.getItem('id')

  //console.log(to.name, role, name, id)
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
    if(role === 'student'){
      next({ name: 'student', params: { type: 'dashboard', id: 0 } })
    }else{
      next({ name: role === 'admin' ? 'admin' : 'login' })
    }
    next({ name: role === 'student' ? 'student' : role === 'admin' ? 'admin' : 'login' })
  } else if (path.includes("student") && role !== 'student') {
    // Wrong dashboard for role
    if(role === 'instructor'){
      next({ name: 'instructor', params: { type: 'dashboard' } })
    }else{
      next({ name: role === 'admin' ? 'admin' : 'login' })
    }
  } else if (path.includes("admin") && role !== 'admin') {
    // Wrong dashboard for role
    if(role === 'instructor'){
      next({ name: 'instructor', params: { type: 'dashboard' } })
    }
    else{
      next({ name: 'student', params: { type: 'dashboard', id: 0 } })
    }
  } else {
    // Continue to route
    next()
  }
})

export default router