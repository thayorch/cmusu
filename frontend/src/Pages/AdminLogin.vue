<template>
  <Navbar />
  <div
    v-if="!isLogin"
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100"
  >
    <div v-if="isChecking" class="text-center animate-pulse">
      <ShieldCheckIcon class="w-16 h-16 text-[#a259ff] mx-auto mb-4" />
      <p class="font-bold text-gray-500">กำลังตรวจสอบสิทธิ์...</p>
    </div>

    <div
      v-else
      class="glass p-10 rounded-3xl shadow-xl max-w-sm w-full mx-4 text-center"
    >
      <div
        class="w-20 h-20 bg-gradient-to-br from-[#ff6ec7] to-[#a259ff] rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg"
      >
        <ShieldCheckIcon class="w-10 h-10 text-white" />
      </div>

      <h1 class="font-black text-2xl text-dark mb-1">Admin Panel</h1>
      <p class="text-sm text-gray-500 mb-8">CMUSU Control Center</p>

      <a
        href="/api/auth/login"
        class="flex items-center justify-center gap-3 w-full bg-[#a259ff] hover:bg-[#8b3dff] text-white font-bold py-3 px-6 rounded-xl transition-all shadow-md hover:shadow-lg"
      >
        <img src="/cmu_logo.png" alt="" class="w-9 h-9" />
        เข้าสู่ระบบด้วย CMU Account
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { ShieldCheckIcon } from "@heroicons/vue/24/solid";
import { useAlert } from "../composables/useAlert";
import Navbar from "../components/Navbar.vue";

const router = useRouter();
const route = useRoute();
const { showAlert } = useAlert();
const isChecking = ref(true);
const isLogin = ref(false);

onMounted(async () => {
  try {
    const res = await fetch("/api/auth/me", { credentials: "include" });
    const data = await res.json();

    if (data.user) {
      isLogin.value = true;
    }

    if (data.user && data.user.app_metadata?.role === "admin") {
      router.replace("/admin");
      return;
    }
  } catch {}
  if (route.query.error === "unauthorized") {
    if (isLogin.value) {
      await showAlert("คุณไม่มีสิทธิ์เข้าถึงหน้านี้", "error");
      router.push("/borrow-central");
    }
  }
  isChecking.value = false;
});
</script>
