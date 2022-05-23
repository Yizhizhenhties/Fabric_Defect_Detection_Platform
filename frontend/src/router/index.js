import Vue from 'vue'
import Router from 'vue-router'

const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'login',
            component: () => import('../views/login.vue')
        },
        {
            path: '/index',
            name: 'index',
            component: () => import('../views/index.vue'),
            redirect: '/index/process',
            children: [
                {
                    path: 'process',
                    component: () => import('../views/process.vue')
                },
                {
                    path: 'history',
                    component: () => import('../views/history.vue')
                },
                {
                    path: 'aboutus',
                    component: () => import('../views/aboutus.vue')
                },
                {
                    path: 'contactus',
                    component: () => import('../views/contactus.vue')
                },
                {
                    path: 'helper',
                    component: () => import('../views/helper.vue')
                },
                {
                    path: 'output',
                    name: 'output',
                    component: () => import('../views/output.vue')
                }
            ]
        }
    ]
})
