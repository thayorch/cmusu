<template>
  <footer class="relative z-10" aria-label="ส่วนท้ายเว็บไซต์">
    <div
      style="
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(12px);
        border-top: 1.5px solid rgba(255, 255, 255, 0.9);
      "
    >
      <div
        class="max-w-5xl mx-auto px-6 py-10 grid grid-cols-2 gap-8 sm:grid-cols-4"
      >
        <RouterLink to="/" class="col-span-2 sm:col-span-1">
          <div>
            <img
              src="/logo-circle.png"
              alt="cmusu-logo"
              class="rounded-full w-20 mb-3"
            />
            <p class="font-black text-sm leading-snug" style="color: #3d2b6b">
              สโมสรนักศึกษา<br />มหาวิทยาลัยเชียงใหม่
            </p>
            <p class="text-xs mt-2 font-mono" style="color: #8b7bae">
              Chiang Mai University<br />
              Student Union
            </p>
          </div>
        </RouterLink>

        <nav aria-label="บริการหลัก">
          <p
            class="text-xs font-black uppercase tracking-widest mb-3"
            style="color: #a259ff"
          >
            บริการ
          </p>
          <ul class="space-y-2">
            <li v-for="link in services" :key="link.label">
              <RouterLink
                :to="link.to"
                class="text-xs hover:opacity-100 transition-opacity flex items-center gap-1.5 hover:font-bold"
                style="color: #5a4a7a; opacity: 0.75"
              >
                <component :is="link.icon" class="w-4 h-4" aria-hidden="true" />
                {{ link.label }}
              </RouterLink>
            </li>
          </ul>
        </nav>

        <nav aria-label="ข้อมูลเพิ่มเติม">
          <p
            class="text-xs font-black uppercase tracking-widest mb-3"
            style="color: #5bc8ff"
          >
            ข้อมูล
          </p>
          <ul class="space-y-2">
            <li v-for="link in info" :key="link.label">
              <a
                :href="link.href"
                target="_blank"
                rel="noopener noreferrer"
                class="text-xs hover:opacity-100 transition-opacity flex items-center gap-1.5 hover:font-bold"
                style="color: #5a4a7a; opacity: 0.75"
              >
                <component :is="link.icon" class="w-4 h-4" aria-hidden="true" />
                {{ link.label }}
              </a>
            </li>
          </ul>
        </nav>

        <div>
          <p
            class="text-xs font-black uppercase tracking-widest mb-3"
            style="color: #ff6ec7"
          >
            ติดต่อเรา
          </p>
          <ul class="space-y-2">
            <li v-for="c in contacts" :key="c.label">
              <a
                :href="c.href"
                target="_blank"
                rel="noopener noreferrer"
                class="text-xs hover:opacity-100 transition-opacity flex items-center gap-1.5 hover:font-bold"
                style="color: #5a4a7a; opacity: 0.75"
                :aria-label="c.label"
              >
                <component :is="c.icon" class="w-4 h-4" aria-hidden="true" />
                {{ c.label }}
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div
        class="flex flex-wrap gap-3 justify-between items-center py-4 px-6 text-xs font-mono"
        style="border-top: 1px solid rgba(162, 89, 255, 0.12); color: #8b7bae"
      >
        <span>© 2026 Chiang Mai Student Union, All rights reserved.</span>

        <a
          href="https://github.com/thayorch"
          target="_blank"
          rel="noopener noreferrer"
          class="font-bold hover:opacity-100 transition-opacity"
          style="opacity: 0.8"
          aria-label="GitHub ของ thayorch"
        >
          @thayorch
        </a>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from "vue-router";
import {
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
} from "@heroicons/vue/24/solid";

const services = [
  { icon: MegaphoneIcon, label: "ข่าวสารและประกาศ", to: "/news" },
  { icon: CalendarDaysIcon, label: "ตารางกิจกรรม", to: "/activity" },

  { icon: WrenchScrewdriverIcon, label: "ยืมอุปกรณ์/ครุภัณฑ์", to: "/borrow" },
  {
    icon: ExclamationTriangleIcon,
    label: "แจ้งปัญหา/ร้องเรียน",
    to: "/report",
  },
  {
    icon: KeyIcon,
    label: "สำหรับคณะกรรมการบริหารสโมสรนักศึกษา",
    to: "/admin",
  },
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
