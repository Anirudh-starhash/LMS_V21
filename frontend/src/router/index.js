import { createRouter, createWebHistory } from 'vue-router'
import index_page from '../components/other_components/IndexPage.vue'
import login_page from '../components/user_components/login_page.vue'
import register_page from '../components/user_components/register_page.vue'
import librarian_page from '../components/library_components/librarian_page.vue'
import change_password from '../components/other_components/change_password.vue'
import librarian_dashboard from '../components/library_components/librarian_dashboard.vue'
import user_dashboard from '../components/user_components/user_dashboard.vue'
import add_section from '../components/section_components/add_section.vue'
import add_book from '../components/book_components/add_book.vue'
import section_page from '../components/section_components/section_page.vue'
import view_section from '../components/section_components/view_section.vue'
import monitor_page from '../components/library_components/monitor_page.vue'
import request_page from '../components/library_components/request_page.vue'
import lib_stats_page from '../components/library_components/lib_stats_page.vue'
import view_book from '@/components/book_components/view_book.vue'
import my_books_page from '@/components/book_components/my_books_page.vue'
import books_page from '@/components/book_components/books_page.vue'
import user_stats_page from '@/components/user_components/user_stats_page.vue'
import axios_demo from '../components/other_components/axios_demo.vue'
import logout_page from '../components/library_components/logout_page.vue'
import user_logout_page from '@/components/user_components/user_logout_page.vue'
import unauthorized from '@/components/other_components/unauthorized.vue'
import reviews_page from '../components/other_components/reviews_page.vue'
import edit_book from '../components/book_components/edit_book.vue'
import edit_section from '../components/section_components/edit_section.vue'
import read_reviews from '../components/book_components/read_reviews.vue'
import profile_page from '../components/user_components/profile_page.vue'
import edit_profile_page from '../components/user_components/edit_profile_page.vue'
import edit_review from '../components/other_components/edit_review.vue'
import returnBook from '../components/book_components/returnBook.vue'
import revokeBook from '../components/library_components/revokeBook.vue'
import delete_book from '../components/book_components/delete_book.vue'
import delete_section from '../components/section_components/delete_section.vue'
import particular_sec_books from '../components/section_components/particular_sec_books.vue'
import particular_auth_books from '../components/section_components/particular_auth_books.vue'
import particular_book from '../components/book_components/particular_book.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index-page',
      component: index_page
    },
    {
      path: '/returnBook/:id',
      name: 'returnBook',
      component: returnBook
    },
    {
      path: '/revokeBook/:id',
      name: 'revokeBook',
      component: revokeBook
    },
    {
      path: '/delete_book/:id',
      name: 'delete_book',
      component: delete_book
    },
    {
      path: '/delete_section/:id',
      name: 'delete_section',
      component: delete_section
    },
    {
      path: '/edit_review/:user_id/:book_id',
      name: 'edit_review',
      component: edit_review
    },
    {
      path:'/profile_page/:id',
      name:'profile_page',
      component:profile_page
    },
    {
      path:'/edit_profile_page/:id',
      name:'edit_profile_page',
      component:edit_profile_page
    },
    {
      path: '/reviews_page/:id',
      name: 'reviews_page',
      component: reviews_page,
    },
    {
      path: '/logout_page',
      name: 'logout_page',
      component: logout_page,
    },
    {
      path: '/user_logout_page/:id',
      name: 'user_logout_page',
      component: user_logout_page,
    },
    {
      path:'/read_reviews/:user_id/:id',
      name:'read_reviews',
      component:read_reviews,
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: unauthorized
    },
    {
      path:'/login_page',
      name:'login_page',
      component:login_page
    },

    {
      path:'/register_page',
      name:'register',
      component:register_page
    },

    {
      path:'/librarian_page',
      name:'librarian_page',
      component:librarian_page
    },

    {
      path:'/change_password/:id',
      name:'change_password',
      component:change_password
    },

    {
      path: '/librarian_dashboard',
      name: 'librarian_dashboard',
      component: librarian_dashboard,
    },

    {
      path: '/user_dashboard/:id',
      name: 'user_dashboard',
      component: user_dashboard,
    },


    {
      path: '/add_section',
      name: 'add_section',
      component: add_section,
    },
    {
      path: '/edit_section/:id',
      name: 'edit_section',
      component: edit_section,
    },

    {
      path: '/add_book/:id',
      name: 'add_book',
      component: add_book,
    },
    {
      path: '/edit_book/:id',
      name: 'edit_book',
      component: edit_book,
    },

    {
      path: '/section_page',
      name: 'section_page',
      component: section_page,
    },

    {
      path: '/view_section/:id',
      name: 'view_section',
      component: view_section,
    },

    {
      path: '/monitor_page',
      name: 'monitor_page',
      component: monitor_page,
    },

    {
      path: '/request_page',
      name: 'request_page',
      component: request_page,
    },

    {
      path: '/lib_stats_page',
      name: 'lib_stats_page',
      component: lib_stats_page,
    },

    {
      path: '/view_book/:id',
      name: 'view_book',
      component: view_book,
    },
   
    {
      path: '/my_books_page/:id',
      name: 'my_books_page',
      component: my_books_page,
    },
    {
      path: '/books_page/:id',
      name: 'books_page',
      component: books_page,
    },
    {
      path: '/user_stats_page/:id',
      name: 'user_stats_page',
      component: user_stats_page,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/axios_demo',
      name: 'axios-demo',
      component: axios_demo
    },
    {
      path: '/particular_sec_books/:section_name',
      name: 'particular_sec_books',
      component: particular_sec_books
    },
    {
      path: '/particular_auth_books/:auth_name',
      name: 'particular_auth_books',
      component: particular_auth_books
    },
    {
      path: '/particular_book/:book_name',
      name: 'particular_book',
      component: particular_book
    },
    
  ]
})


export default router
