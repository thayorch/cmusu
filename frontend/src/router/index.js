import { createRouter, createWebHistory } from "vue-router";

const Home = () => import("../Pages/Home.vue");
const Admin = () => import("../Pages/Admin.vue");
const Activity = () => import("../Pages/Activity.vue");
const News = () => import("../Pages/News.vue");
const Borrow = () => import("../Pages/Borrow.vue");
const Report = () => import("../Pages/Report.vue");
const BorrowCentral = () => import("../Pages/BorrowCentral.vue");
const BorrowFaculty = () => import("../Pages/BorrowFaculty.vue");

const routes = [
  {
    path: "/",
    component: Home,
  },
  {
    path: "/news",
    component: News,
  },

  {
    path: "/activity",
    component: Activity,
  },
  {
    path: "/borrow",
    component: Borrow,
  },
  {
    path: "/report",
    component: Report,
  },
  {
    path: "/admin",
    component: Admin,
  },
  {
    path: "/borrow-central",
    component: BorrowCentral,
  },
  {
    path: "/borrow-faculty",
    component: BorrowFaculty,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return {
        top: 0,
        behavior: "smooth",
      };
    }
  },
});

export default router;
