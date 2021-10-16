import Vue from "vue";
import Router from "vue-router";

import AdminIndex from "./views/admin/Index.vue";
import AdminSchedule from "./views/admin/Schedule.vue";
import AdminMunit from "./views/admin/Munit.vue";
import AdminMwork from "./views/admin/Mwork.vue";

import Index from "./views/user/Index.vue";
import Schedule from "./views/user/Schedule.vue";
import Statistics from "./views/user/Statistics.vue";

import Landing from "./views/Landing.vue";
import Login from "./views/Login.vue";
import Signup from "./views/Signup.vue";
import Profile from "./views/Profile.vue";

import NoUserNavbar from "./layout/NoUserNavbar.vue";
import AdminMainNavbar from "./layout/AdminMainNavbar.vue";
import MainNavbar from "./layout/MainNavbar.vue";
import MainFooter from "./layout/MainFooter.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "index",
      components: { default: Index, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/schedule",
      name: "schedule",
      components: { default: Schedule, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/statistics",
      name: "statistics",
      components: { default: Statistics, header: MainNavbar, footer: MainFooter },
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
      path: "/admin/schedule",
      name: "admin-schedule",
      components: { default: AdminSchedule, header: AdminMainNavbar, footer: MainFooter },
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
      path: "/landing",
      name: "landing",
      components: { default: Landing, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
      }
    },
    {
      path: "/login",
      name: "login",
      components: { default: Login, header: NoUserNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 }
      }
    },
    {
      path: "/signup",
      name: "signup",
      components: { default: Signup, header: NoUserNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 }
      }
    },
    {
      path: "/profile",
      name: "profile",
      components: { default: Profile, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: "black" }
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
