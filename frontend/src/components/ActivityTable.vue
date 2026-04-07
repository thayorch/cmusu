<template>
  <section class="relative z-10 max-w-4xl mx-auto px-6 py-6">
    <div class="text-center mb-16">
      <div
        class="glass inline-flex items-center gap-2 px-5 py-2 rounded-full mb-5"
      >
        <MegaphoneIcon class="w-4 h-4 text-[#5bc8ff]" />
        <span
          class="font-mono text-xs font-bold tracking-widest"
          style="color: #5bc8ff"
        >
          CMUSU ACTIVITIES
        </span>
      </div>
      <h2
        class="font-black text-dark leading-tight tracking-tight mb-3"
        style="font-size: clamp(2rem, 5vw, 3.5rem)"
      >
        ตารางกิจกรรมสโมสรนักศึกษา
      </h2>
      <p
        class="font-light text-lg max-w-sm mx-auto mb-6"
        style="color: #8b7bae"
      >
        มหาวิทยาลัยเชียงใหม่ ปีการศึกษา 2569
      </p>

      <div class="flex flex-wrap gap-3 justify-center">
        <span
          v-for="m in meta"
          :key="m.text"
          class="glass flex items-center gap-2 px-4 py-2 rounded-2xl text-sm font-medium"
          :style="{ color: m.color }"
        >
          <component :is="m.icon" class="w-5 h-5" />
          {{ m.text }}
        </span>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-20 text-[#8b7bae]">
      กำลังโหลดข้อมูลกิจกรรม...
    </div>

    <div v-else-if="errorMessage" class="text-center py-20 text-red-500">
      {{ errorMessage }}
    </div>

    <div v-else class="relative">
      <div
        class="absolute top-0 bottom-0 w-0.5 rounded-full pointer-events-none"
        style="
          left: 88px;
          background: linear-gradient(
            to bottom,
            transparent,
            #a259ff 10%,
            #5bc8ff 50%,
            #ff6ec7 90%,
            transparent
          );
        "
      ></div>

      <template v-for="(group, groupIdx) in scheduleGroups" :key="group.month">
        <div class="flex gap-6 mb-8 mt-12 first:mt-0 relative z-10">
          <div class="shrink-0 w-[88px]"></div>
          <div class="flex-1">
            <h3
              class="inline-flex items-center gap-2 px-5 py-2.5 rounded-2xl text-base font-bold backdrop-blur-md"
              :style="{
                background: group.color + '15',
                color: group.color,
                border: '1px solid ' + group.color + '30',
              }"
            >
              <CalendarDaysIcon class="w-5 h-5" />
              {{ group.month }}
            </h3>
          </div>
        </div>

        <div
          v-for="(item, i) in group.events"
          :key="item.time"
          class="flex gap-6 mb-5 relative z-10"
          :style="{ animationDelay: groupIdx * 0.1 + i * 0.05 + 's' }"
        >
          <div class="relative shrink-0 w-[88px] text-right pr-5 pt-4">
            <span
              class="font-mono text-xl font-bold"
              :style="{ color: item.color || '#8B7BAE' }"
              >{{ item.time }}</span
            >
            <div
              class="absolute right-[-7px] top-[18px] w-3.5 h-3.5 rounded-full border-[2.5px] border-white"
              :style="{
                background: item.color || '#A259FF',
                boxShadow: `0 0 10px ${item.color || '#A259FF'}80`,
              }"
            ></div>
          </div>

          <div
            class="flex-1 quest-card group cursor-default"
            :class="item.highlight ? 'ring-2 ring-offset-1' : ''"
            :style="item.highlight ? { ringColor: item.color } : {}"
          >
            <div class="flex items-start justify-between gap-3 mb-2">
              <div class="flex items-center gap-3">
                <component
                  :is="iconMap[item.icon]"
                  class="w-7 h-7 select-none shrink-0"
                  :style="{ color: item.color }"
                  style="filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))"
                />

                <div>
                  <span
                    class="tag-pill text-xs flex items-center gap-1"
                    :style="{
                      color: item.color || '#A259FF',
                      borderColor: (item.color || '#A259FF') + '50',
                      background: (item.color || '#A259FF') + '14',
                    }"
                  >
                    <ClockIcon class="w-3 h-3" /> {{ item.phase }}
                  </span>
                </div>
              </div>
            </div>

            <h3
              class="font-black text-dark text-base leading-tight mb-1.5 mt-2"
            >
              {{ item.title }}
            </h3>
            <p
              class="text-sm font-light leading-relaxed flex items-start gap-1.5 mb-3"
              style="color: #8b7bae"
            >
              <MapPinIcon class="w-4 h-4 shrink-0 mt-0.5" /> {{ item.desc }}
            </p>

            <div
              v-if="item.badge"
              class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold mt-2"
              :style="{
                background: (item.color || '#A259FF') + '18',
                color: item.color || '#A259FF',
              }"
            >
              <StarIcon class="w-3.5 h-3.5" /> {{ item.badge }}
            </div>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import {
  MegaphoneIcon,
  AcademicCapIcon,
  MapPinIcon,
  SparklesIcon,
  TicketIcon,
  TruckIcon,
  UserGroupIcon,
  HeartIcon,
  BriefcaseIcon,
  GiftIcon,
  BookOpenIcon,
  GlobeAltIcon,
  MoonIcon,
  StarIcon,
  FireIcon,
  ChatBubbleLeftRightIcon,
  FlagIcon,
  ComputerDesktopIcon,
  ShoppingBagIcon,
  PaintBrushIcon,
  ShieldCheckIcon,
  CalendarDaysIcon,
  ClockIcon,
} from "@heroicons/vue/24/solid";

// สร้าง Map เพื่อแปลงชื่อ Icon (String) จาก Database ให้เป็น Component จริง
const iconMap = {
  TicketIcon,
  TruckIcon,
  UserGroupIcon,
  HeartIcon,
  BriefcaseIcon,
  BookOpenIcon,
  MoonIcon,
  StarIcon,
  FireIcon,
  FlagIcon,
  ComputerDesktopIcon,
  ShoppingBagIcon,
  PaintBrushIcon,
  ShieldCheckIcon,
  GiftIcon,
  GlobeAltIcon,
  ChatBubbleLeftRightIcon,
};

const meta = [
  { icon: AcademicCapIcon, text: "ปีการศึกษา 2569", color: "#A259FF" },
  { icon: MapPinIcon, text: "มหาวิทยาลัยเชียงใหม่", color: "#5BC8FF" },
  { icon: SparklesIcon, text: "รวม 18 กิจกรรมหลัก", color: "#FF6EC7" },
];

// ตัวแปร State
const scheduleGroups = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");

// ดึงข้อมูลจาก Backend เมื่อโหลดหน้าเว็บเสร็จ
onMounted(async () => {
  try {
    isLoading.value = true;
    errorMessage.value = "";

    const response = await fetch("/api/activity");

    if (!response.ok) {
      throw new Error(`เกิดข้อผิดพลาดในการโหลดข้อมูล: ${response.status}`);
    }

    const result = await response.json();

    if (result.status === "success") {
      scheduleGroups.value = result.data;
    } else {
      throw new Error(result.message || "โหลดข้อมูลไม่สำเร็จ");
    }
  } catch (error) {
    console.error("Fetch Activity Error:", error);
    errorMessage.value =
      "ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์เพื่อโหลดตารางกิจกรรมได้";
  } finally {
    isLoading.value = false;
  }
});
</script>
