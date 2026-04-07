<template>
  <Navbar />
  <section class="relative z-10 max-w-4xl mx-auto px-6 py-6">
    <div class="text-center mb-16">
      <div
        class="glass inline-flex items-center gap-2 px-5 py-2 rounded-full mb-5"
      >
        <ArchiveBoxIcon class="w-4 h-4 text-[#a259ff]" />
        <span
          class="font-mono text-xs font-bold tracking-widest uppercase"
          style="color: #a259ff"
        >
          CMUSU Borrow
        </span>
      </div>
      <h2
        class="font-black text-dark leading-tight tracking-tight mb-3"
        style="font-size: clamp(2rem, 5vw, 3.5rem)"
      >
        ยืมอุปกรณ์/ครุภัณฑ์
      </h2>
      <p class="font-light text-lg mx-auto mb-6" style="color: #8b7bae">
        ระบบตรวจสอบสถานะและขอยืมครุภัณฑ์ สโมสรนักศึกษามหาวิทยาลัยเชียงใหม่
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

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-10 animate-fade-in">
      <Router-Link to="/borrow-central">
        <div
          class="glass group cursor-pointer flex flex-col items-center justify-center py-16 px-6 text-center rounded-[2rem] hover:-translate-y-2 hover:shadow-xl transition-all duration-300 relative overflow-hidden"
        >
          <div
            class="absolute top-0 right-0 -mr-16 -mt-16 w-48 h-48 rounded-full bg-gradient-to-br from-[#5bc8ff] to-[#a259ff] opacity-10 blur-2xl pointer-events-none group-hover:opacity-20 transition-opacity"
          ></div>

          <div
            class="w-20 h-20 rounded-full bg-[#5BC8FF]/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
          >
            <BuildingLibraryIcon class="w-10 h-10 text-[#5BC8FF]" />
          </div>
          <h3 class="text-2xl font-black text-dark mb-3">ครุภัณฑ์ส่วนกลาง</h3>
          <p
            class="text-sm font-light max-w-xs mx-auto mb-8"
            style="color: #8b7bae"
          >
            อุปกรณ์สนับสนุนกิจกรรมส่วนกลาง
          </p>
          <span
            class="inline-flex items-center gap-2 text-sm font-bold text-[#5BC8FF]"
          >
            ดูรายการครุภัณฑ์
            <ArrowRightIcon
              class="w-4 h-4 group-hover:translate-x-1 transition-transform"
            />
          </span>
        </div>
      </Router-Link>
      <div
        class="glass group cursor-pointer flex flex-col items-center justify-center py-16 px-6 text-center rounded-[2rem] hover:-translate-y-2 hover:shadow-xl transition-all duration-300 relative overflow-hidden"
      >
        <div
          class="absolute bottom-0 left-0 -ml-16 -mb-16 w-48 h-48 rounded-full bg-gradient-to-tr from-[#ff6ec7] to-[#ffd166] opacity-10 blur-2xl pointer-events-none group-hover:opacity-20 transition-opacity"
        ></div>

        <div
          class="w-20 h-20 rounded-full bg-[#FF6EC7]/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300"
        >
          <BuildingOfficeIcon class="w-10 h-10 text-[#FF6EC7]" />
        </div>
        <h3 class="text-2xl font-black text-dark mb-3">ครุภัณฑ์ส่วนคณะ</h3>
        <p
          class="text-sm font-light max-w-xs mx-auto mb-8"
          style="color: #8b7bae"
        >
          อุปกรณ์สนับสนุนกิจกรรมสโมสรนักศึกษาคณะ
        </p>
        <span
          class="inline-flex items-center gap-2 text-sm font-bold text-[#FF6EC7]"
        >
          ดูรายการครุภัณฑ์
          <ArrowRightIcon
            class="w-4 h-4 group-hover:translate-x-1 transition-transform"
          />
        </span>
      </div>
    </div>
  </section>
</template>

<script setup>
import {
  ArchiveBoxIcon,
  CheckBadgeIcon,
  ClockIcon,
  BuildingLibraryIcon,
  BuildingOfficeIcon,
  ArrowRightIcon,
} from "@heroicons/vue/24/solid";
import Navbar from "../components/Navbar.vue";
const meta = [
  {
    icon: ClockIcon,
    text: "ยืม/คืนอุปกรณ์และครุภัณฑ์",
    color: "#5BC8FF",
  },
  {
    icon: CheckBadgeIcon,
    text: "ส่วนกลางและส่วนคณะ",
    color: "#FF6EC7",
  },
];
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
</style>
