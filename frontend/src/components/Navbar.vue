<template>
  <nav class="sticky top-0 z-40 w-full glass-nav transition-all duration-300">
    <div class="mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between h-14 md:h-16">
        <router-link
          to="/"
          class="flex-shrink-0 flex items-center cursor-pointer no-underline"
        >
          <img
            src="/banner-sulogo-removebg-preview.png"
            alt="CMUSU Banner"
            class="h-10 md:h-12 w-auto"
          />
        </router-link>

        <button
          @click="isMenuOpen = true"
          class="p-2 rounded-xl text-[#8b7bae] hover:text-[#a259ff] hover:bg-[#a259ff]/10 focus:outline-none transition-colors"
        >
          <Bars3Icon class="w-7 h-7" />
        </button>
      </div>
    </div>

    <div
      v-if="isMenuOpen"
      class="fixed inset-0 z-50 flex justify-end bg-black/20 backdrop-blur-sm transition-opacity"
      @click.self="isMenuOpen = false"
    >
      <div
        class="w-72 sm:w-80 h-screen sidebar-glass shadow-2xl animate-slide-in-right flex flex-col"
      >
        <div class="flex justify-end px-4 h-14 md:h-16 items-center">
          <button
            @click="isMenuOpen = false"
            class="p-2 rounded-xl text-gray-500 hover:text-red-500 hover:bg-red-50 transition-colors"
          >
            <XMarkIcon class="w-7 h-7" />
          </button>
        </div>

        <div class="px-6 pb-10 space-y-8 overflow-y-auto hide-scrollbar">
          <div class="flex justify-center">
            <router-link
              @click="isMenuOpen = false"
              to="/"
              class="flex-shrink-0 flex items-center cursor-pointer no-underline w-full justify-center"
            >
              <img
                src="/banner-sulogo-removebg-preview.png"
                alt="CMUSU Banner"
                class="h-20 md:h-24 w-auto"
              />
            </router-link>
          </div>

          <nav aria-label="บริการหลัก">
            <p
              class="text-xs font-black uppercase tracking-widest mb-3"
              style="color: #a259ff"
            >
              บริการ
            </p>
            <div class="space-y-2">
              <RouterLink
                v-for="link in services"
                :key="link.label"
                :to="link.to"
                class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-black/5 transition-colors"
                style="color: #5a4a7a"
              >
                <component :is="link.icon" class="w-5 h-5 opacity-75" />
                <span class="text-sm font-medium">{{ link.label }}</span>
              </RouterLink>
            </div>
          </nav>

          <nav aria-label="ข้อมูลเพิ่มเติม">
            <p
              class="text-xs font-black uppercase tracking-widest mb-3"
              style="color: #5bc8ff"
            >
              ข้อมูล
            </p>
            <div class="space-y-2">
              <a
                v-for="link in info"
                :key="link.label"
                :href="link.href"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-black/5 transition-colors"
                style="color: #5a4a7a"
              >
                <component :is="link.icon" class="w-5 h-5 opacity-75" />
                <span class="text-sm font-medium">{{ link.label }}</span>
              </a>
            </div>
          </nav>

          <nav aria-label="ติดต่อเรา">
            <p
              class="text-xs font-black uppercase tracking-widest mb-3"
              style="color: #ff6ec7"
            >
              ติดต่อเรา
            </p>
            <div class="space-y-1">
              <a
                v-for="c in contacts"
                :key="c.label"
                :href="c.href"
                target="_blank"
                rel="noopener noreferrer"
                class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-black/5 transition-colors"
                style="color: #5a4a7a"
              >
                <component :is="c.icon" class="w-5 h-5 opacity-75" />
                <span class="text-sm font-medium">{{ c.label }}</span>
              </a>
            </div>
          </nav>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from "vue";
import RouterLinkBtn from "./utils/RouterLink-btn.vue";

// นำเข้าไอคอนทั้งหมดให้ตรงกับ Footer
import {
  HomeIcon,
  CalendarDaysIcon,
  WrenchScrewdriverIcon,
  ExclamationTriangleIcon,
  BuildingLibraryIcon,
  MegaphoneIcon,
  CalendarIcon,
  DocumentTextIcon,
  UsersIcon,
  CameraIcon,
  EnvelopeIcon,
  MapPinIcon,
  KeyIcon,
  Bars3Icon,
  XMarkIcon,
} from "@heroicons/vue/24/solid";

const isMenuOpen = ref(false);

// ข้อมูลเมนูแบบเดียวกับ Footer
const services = [
  { icon: MegaphoneIcon, label: "ข่าวสารและประกาศ", to: "/news" },
  { icon: CalendarDaysIcon, label: "ตารางกิจกรรม", to: "/activity" },
  { icon: WrenchScrewdriverIcon, label: "ยืมอุปกรณ์/ครุภัณฑ์", to: "/borrow" },
  {
    icon: ExclamationTriangleIcon,
    label: "แจ้งปัญหา/ร้องเรียน",
    to: "/report",
  },
  { icon: KeyIcon, label: "สำหรับคณะกรรมการฯ", to: "/admin" },
];

const info = [
  {
    icon: BuildingLibraryIcon,
    label: "เกี่ยวกับสโมสร",
    href: "https://sdd.oop.cmu.ac.th/studentOrg",
  },
  {
    icon: CalendarIcon,
    label: "ปฏิทินกิจกรรม",
    href: "https://www.reg.cmu.ac.th/webreg/th/eventics/",
  },
  {
    icon: DocumentTextIcon,
    label: "ระเบียบข้อบังคับ",
    href: "https://sdd.oop.cmu.ac.th/stdRoleLaw",
  },
];

const contacts = [
  {
    icon: UsersIcon,
    label: "Facebook",
    href: "https://www.facebook.com/ChiangmaiUniversityStudentUnion",
  },
  {
    icon: CameraIcon,
    label: "Instagram",
    href: "https://www.instagram.com/cmusu.official/",
  },
  {
    icon: EnvelopeIcon,
    label: "Email",
    href: "mailto:cmusu69@gmail.com",
  },
  {
    icon: MapPinIcon,
    label: "สำนักงานสโมสรนักศึกษา",
    href: "https://maps.app.goo.gl/63NjK7oH6DWdHwTS7",
  },
];
</script>

<style scoped>
/* Sidebar ด้านขวา (มีขอบซ้าย) */
.sidebar-glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-left: 1.5px solid rgba(255, 255, 255, 0.9);
}

@keyframes slideRightIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
.animate-slide-in-right {
  animation: slideRightIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ซ่อน Scrollbar ของ Sidebar เพื่อความสวยงาม */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
