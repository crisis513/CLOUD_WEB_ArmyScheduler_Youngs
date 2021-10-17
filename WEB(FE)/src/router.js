import Vue from "vue";
import Router from "vue-router";

import AdminIndex from "./views/admin/Index.vue";
import AdminMunit from "./views/admin/Munit.vue";
import AdminMwork from "./views/admin/Mwork.vue";

import UserIndex from "./views/user/Index.vue";
import UserStatistics from "./views/user/Statistics.vue";

import Index from "./views/Index.vue";
import Login from "./views/Login.vue";
import Signup from "./views/Signup.vue";

import CleanNavbar from "./layout/CleanNavbar.vue";
import NoUserNavbar from "./layout/NoUserNavbar.vue";
import AdminMainNavbar from "./layout/AdminMainNavbar.vue";
import MainNavbar from "./layout/MainNavbar.vue";
import MainFooter from "./layout/MainFooter.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/user/",
      name: "index",
      components: { default: UserIndex, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/user/statistics",
      name: "statistics",
      components: { default: UserStatistics, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/admin",
      name: "admin-index",
      components: { default: AdminIndex, header: AdminMainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/admin/munit",
      name: "admin-manage-unit",
      components: { default: AdminMunit, header: AdminMainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/admin/mwork",
      name: "admin-manage-work",
      components: { default: AdminMwork, header: AdminMainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/",
      name: "index",
      components: { default: Index, header: NoUserNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/login",
      name: "login",
      components: { default: Login, header: CleanNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 }
      }
    },
    {
      path: "/signup",
      name: "signup",
      components: { default: Signup, header: CleanNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 }
      }
    }
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});
