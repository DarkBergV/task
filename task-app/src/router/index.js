import { createRouter, createWebHistory } from "vue-router";
import MainPage from "@/views/MainPage.vue"; // Import your MainPage component
import UserPage from "@/views/UserPage.vue"; // Import your UserPage component

const routes = [
  {
    path: "/",
    component: MainPage,
  },
  {
    path: "/user/:id",
    component: UserPage,
    props: true, // Pass route params as props
  },
];

const router = createRouter({
  history: createWebHistory(), // Use history mode for cleaner URLs
  routes,
});

export default router;