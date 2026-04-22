<template>
  <section
    class="relative min-h-screen flex flex-col items-center justify-center text-center px-6 overflow-hidden z-10"
  >
    <div
      class="absolute w-72 h-72 rounded-full opacity-30 pointer-events-none"
      style="
        background: radial-gradient(circle, #a259ff, transparent);
        top: -80px;
        left: -60px;
        filter: blur(70px);
        animation: floatBlob 10s ease-in-out infinite;
      "
    ></div>
    <div
      class="absolute w-64 h-64 rounded-full opacity-25 pointer-events-none"
      style="
        background: radial-gradient(circle, #5bc8ff, transparent);
        top: -40px;
        right: -40px;
        filter: blur(70px);
        animation: floatBlob 12s ease-in-out infinite;
        animation-delay: -4s;
      "
    ></div>
    <div
      class="absolute w-56 h-56 rounded-full opacity-20 pointer-events-none"
      style="
        background: radial-gradient(circle, #ff6ec7, transparent);
        bottom: 60px;
        left: 5%;
        filter: blur(60px);
        animation: floatBlob 9s ease-in-out infinite;
        animation-delay: -7s;
      "
    ></div>

    <div
      class="absolute w-[600px] h-[600px] rounded-full pointer-events-none opacity-10"
      style="
        border: 2px dashed #a259ff;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: spinSlow 30s linear infinite;
      "
    ></div>

    <div
      class="absolute w-[500px] h-[500px] rounded-full pointer-events-none opacity-20"
      style="
        background: radial-gradient(circle, #a259ff, transparent);
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        filter: blur(100px);
      "
    ></div>

    <div
      class="text-8xl mb-4 relative z-10 select-none"
      style="
        animation: wiggle 3s ease-in-out infinite;
        filter: drop-shadow(0 12px 32px rgba(162, 89, 255, 0.3));
      "
    >
      <img src="/logo-circle.png" alt="cmusu-logo" class="w-32 mx-auto" />
    </div>

    <h1
      class="z-10 font-black leading-[0.95] tracking-tight mb-4"
      style="
        font-size: clamp(3rem, 8vw, 6.5rem);
        animation: bounceIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s both;
      "
    >
      <span class="block text-dark">สโมสรนักศึกษา</span>
      <span
        class="block dung pt-2"
        style="
          background: linear-gradient(
            180deg,
            #541e96 0%,
            #903ffb 50%,
            #541e96 100%
          );
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        "
      >
        มหาวิทยาลัยเชียงใหม่
      </span>
    </h1>
    <h2
      class="text-2xl z-10 font-black leading-[0.95] tracking-tight mb-4"
      style="
        font-size: clamp(1rem, 2vw, 1.5rem);
        animation: bounceIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s both;
      "
    >
      Chiang Mai University Student Union
    </h2>

    <div
      class="flex gap-4 flex-wrap justify-center z-10 my-12"
      style="animation: slideUp 0.6s 0.45s ease both"
    >
      <button
        @click="router.push('/news')"
        class="sticker-btn text-white flex items-center justify-center gap-2 hover:cursor-pointer"
        style="background: linear-gradient(#903ffb, #541e96)"
      >
        <SparklesIcon class="w-6 h-6" /> เข้าสู่เว็บไซต์
      </button>
    </div>

    <div
      class="flex flex-wrap gap-3 justify-center z-10 mb-4"
      style="animation: slideUp 0.6s 0.55s ease both"
    >
      <div
        v-for="s in stats"
        :key="s.label"
        @click="router.push(s.link)"
        class="quest-card !p-4 !rounded-2xl text-center min-w-[100px] cursor-pointer hover:-translate-y-1"
        style="transition: transform 0.2s"
      >
        <div class="flex justify-center mb-2">
          <component :is="s.icon" class="w-8 h-8" :style="{ color: s.color }" />
        </div>
        <div class="text-xs mt-1 font-medium" style="color: #8b7bae">
          {{ s.label }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";
import {
  CalendarDaysIcon,
  WrenchScrewdriverIcon,
  ExclamationTriangleIcon,
  SparklesIcon,
  MegaphoneIcon,
} from "@heroicons/vue/24/solid";

const router = useRouter();

const stats = [
  {
    icon: MegaphoneIcon,
    label: "ข่าวสารและประกาศ",
    color: "#FF6EC7",
    link: "/news",
  },
  {
    icon: CalendarDaysIcon,
    label: "ตารางกิจกรรม",
    color: "#A259FF",
    link: "/activity",
  },

  {
    icon: WrenchScrewdriverIcon,
    label: "ยืมอุปกรณ์/ครุภัณฑ์",
    color: "#5BC8FF",
    link: "/borrow",
  },
  {
    icon: ExclamationTriangleIcon,
    label: "แจ้งปัญหา/ร้องเรียน",
    color: "#FFD166",
    link: "/report",
  },
];
</script>
