<template>
  <div v-if="isChecking" class="min-h-screen flex items-center justify-center">
    <div class="text-center animate-pulse">
      <ShieldCheckIcon class="w-16 h-16 text-[#a259ff] mx-auto mb-4" />
      <p class="font-bold text-gray-600">กำลังตรวจสอบสิทธิ์...</p>
    </div>
  </div>

  <section
    v-else-if="isAdmin"
    class="relative z-10 max-w-7xl mx-auto px-4 md:px-6 py-6 md:py-10 flex flex-col md:flex-row gap-6 md:gap-8"
  >
    <div class="w-full md:w-64 shrink-0">
      <div
        class="glass p-4 md:p-6 rounded-3xl md:sticky md:top-24 shadow-sm z-20"
      >
        <div class="flex items-center md:flex-col gap-4 md:gap-0 mb-4 md:mb-6">
          <div
            class="w-12 h-12 md:w-16 md:h-16 shrink-0 bg-gradient-to-br from-[#ff6ec7] to-[#a259ff] rounded-full flex items-center justify-center md:mx-auto md:mb-3 shadow-lg"
          >
            <ShieldCheckIcon class="w-6 h-6 md:w-8 md:h-8 text-white" />
          </div>
          <div class="text-left md:text-center">
            <h2 class="font-black text-lg md:text-xl text-dark">Admin Panel</h2>
            <p class="text-xs text-gray-500">CMUSU Control Center</p>
          </div>
        </div>

        <nav
          class="flex flex-row md:flex-col gap-2 overflow-x-auto pb-2 md:pb-0 scrollbar-hide"
        >
          <button
            @click="activeTab = 'equipment'"
            :class="
              activeTab === 'equipment'
                ? 'bg-[#a259ff] text-white shadow-md'
                : 'hover:bg-gray-100 text-gray-600 bg-white/50 md:bg-transparent'
            "
            class="shrink-0 whitespace-nowrap w-auto md:w-full flex items-center gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl text-sm font-bold transition-all border md:border-none border-gray-100"
          >
            <ArchiveBoxIcon class="w-4 h-4 md:w-5 md:h-5" /> จัดการครุภัณฑ์
          </button>

          <button
            @click="activeTab = 'requests'"
            :class="
              activeTab === 'requests'
                ? 'bg-[#ffd166] text-gray-900 shadow-md'
                : 'hover:bg-gray-100 text-gray-600 bg-white/50 md:bg-transparent'
            "
            class="shrink-0 whitespace-nowrap w-auto md:w-full flex items-center gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl text-sm font-bold transition-all border md:border-none border-gray-100"
          >
            <ClipboardDocumentListIcon class="w-4 h-4 md:w-5 md:h-5" />
            รายการขอยืม
          </button>

          <button
            @click="activeTab = 'reports'"
            :class="
              activeTab === 'reports'
                ? 'bg-[#ff6ec7] text-white shadow-md'
                : 'hover:bg-gray-100 text-gray-600 bg-white/50 md:bg-transparent'
            "
            class="shrink-0 whitespace-nowrap w-auto md:w-full flex items-center gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl text-sm font-bold transition-all border md:border-none border-gray-100"
          >
            <MegaphoneIcon class="w-4 h-4 md:w-5 md:h-5" />
            VOC
          </button>
        </nav>
      </div>
    </div>

    <div class="flex-1 w-full max-w-full overflow-hidden">
      <EquipmentTab v-if="activeTab === 'equipment'" />
      <RequestsTab v-if="activeTab === 'requests'" />
      <ReportsTab v-if="activeTab === 'reports'" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import {
  ShieldCheckIcon,
  ArchiveBoxIcon,
  ClipboardDocumentListIcon,
  MegaphoneIcon,
} from "@heroicons/vue/24/solid";

import EquipmentTab from "./admin/EquipmentTab.vue";
import RequestsTab from "./admin/RequestsTab.vue";
import ReportsTab from "./admin/ReportsTab.vue";
import { useAlert } from "../composables/useAlert";

const { showAlert } = useAlert();

const router = useRouter();
const activeTab = ref("equipment");
const isAdmin = ref(false);
const isChecking = ref(true);

onMounted(async () => {
  try {
    const res = await fetch("/api/auth/me", { credentials: "include" });
    const data = await res.json();

    if (data.user && data.user.app_metadata.role === "admin") {
      isAdmin.value = true;
    } else {
      await showAlert("คุณไม่มีสิทธิ์เข้าถึงหน้านี้", "error");
      router.push("/");
    }
  } catch (error) {
    router.push("/borrow-central");
  } finally {
    isChecking.value = false;
  }
});
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
