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
    <!-- Mobile top bar -->
    <div class="md:hidden glass p-4 rounded-3xl shadow-sm">
      <div class="flex items-center justify-between gap-3 mb-3">
        <div class="flex items-center gap-3">
          <div
            class="w-10 h-10 shrink-0 bg-gradient-to-br from-[#ff6ec7] to-[#a259ff] rounded-full flex items-center justify-center shadow-lg"
          >
            <ShieldCheckIcon class="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 class="font-black text-base text-dark leading-tight">Admin Panel</h2>
            <p class="text-[11px] text-gray-500">CMUSU Control Center</p>
          </div>
        </div>
        <button
          @click="logout"
          class="shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold text-red-500 bg-red-50 border border-red-100 hover:bg-red-100 transition-colors"
        >
          <PowerIcon class="w-4 h-4" />
          ออกจากระบบ
        </button>
      </div>

      <nav class="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="
            activeTab === tab.id
              ? [tab.activeClass, 'shadow-md']
              : 'text-gray-600 bg-white/60 border border-gray-100'
          "
          class="shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all"
        >
          <component :is="tab.icon" class="w-3.5 h-3.5" />
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <!-- Desktop sidebar -->
    <div class="hidden md:block w-64 shrink-0">
      <div class="glass p-6 rounded-3xl sticky top-24 shadow-sm">
        <div class="flex flex-col items-center mb-6">
          <div
            class="w-16 h-16 bg-gradient-to-br from-[#ff6ec7] to-[#a259ff] rounded-full flex items-center justify-center mb-3 shadow-lg"
          >
            <ShieldCheckIcon class="w-8 h-8 text-white" />
          </div>
          <h2 class="font-black text-xl text-dark">Admin Panel</h2>
          <p class="text-xs text-gray-500">CMUSU Control Center</p>
        </div>

        <nav class="flex flex-col gap-2">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="
              activeTab === tab.id
                ? [tab.activeClass, 'shadow-md']
                : 'hover:bg-gray-100 text-gray-600'
            "
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-all"
          >
            <component :is="tab.icon" class="w-5 h-5" />
            {{ tab.label }}
          </button>

          <button
            @click="logout"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-red-600 hover:bg-gray-100 transition-all"
          >
            <PowerIcon class="w-5 h-5" />
            ออกจากระบบ
          </button>
        </nav>
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <EquipmentTab v-if="activeTab === 'equipment'" />
      <RequestsTab v-if="activeTab === 'requests'" />
      <NewsTab v-if="activeTab === 'news'" />
      <ActivityTab v-if="activeTab === 'activity'" />
      <FacultyEquipmentTab v-if="activeTab === 'faculty-equipment'" />
      <ReportsTab v-if="activeTab === 'reports'" />
      <AdminRoleTab v-if="activeTab === 'admin-role'" />
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
  NewspaperIcon,
  CalendarDaysIcon,
  PowerIcon,
  BuildingLibraryIcon,
  UserPlusIcon,
} from "@heroicons/vue/24/solid";

import EquipmentTab from "./Admin/EquipmentTab.vue";
import RequestsTab from "./Admin/RequestsTab.vue";
import ReportsTab from "./Admin/ReportsTab.vue";
import NewsTab from "./Admin/NewsTab.vue";
import ActivityTab from "./Admin/ActivityTab.vue";
import FacultyEquipmentTab from "./Admin/FacultyEquipmentTab.vue";
import AdminRoleTab from "./Admin/AdminRoleTab.vue";
import { useAlert } from "../composables/useAlert";

const { showAlert } = useAlert();
const router = useRouter();
const activeTab = ref("equipment");
const isAdmin = ref(false);
const isChecking = ref(true);

const tabs = [
  { id: "equipment",         label: "จัดการครุภัณฑ์", icon: ArchiveBoxIcon,             activeClass: "bg-[#a259ff] text-white" },
  { id: "requests",          label: "รายการขอยืม",     icon: ClipboardDocumentListIcon,  activeClass: "bg-[#ffd166] text-gray-900" },
  { id: "news",              label: "ข่าวสาร",          icon: NewspaperIcon,              activeClass: "bg-[#ff6ec7] text-white" },
  { id: "activity",          label: "กิจกรรม",          icon: CalendarDaysIcon,           activeClass: "bg-[#ffd166] text-gray-900" },
  { id: "faculty-equipment", label: "ครุภัณฑ์คณะ",     icon: BuildingLibraryIcon,        activeClass: "bg-[#43b89c] text-white" },
  { id: "reports",           label: "VOC",              icon: MegaphoneIcon,              activeClass: "bg-gray-700 text-white" },
  { id: "admin-role",        label: "สิทธิ์แอดมิน",     icon: UserPlusIcon,               activeClass: "bg-[#a259ff] text-white" },
];

const logout = async () => {
  await fetch("/api/auth/logout", { method: "POST", credentials: "include" });
  window.location.reload();
};

onMounted(async () => {
  try {
    const res = await fetch("/api/auth/me", { credentials: "include" });
    const data = await res.json();

    if (data.user && data.user.app_metadata?.role === "admin") {
      isAdmin.value = true;
    } else {
      router.replace("/admin/login?error=unauthorized");
    }
  } catch (error) {
    router.replace("/admin/login");
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
