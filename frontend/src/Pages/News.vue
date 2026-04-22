<template>
  <Navbar />
  <section class="relative z-10 max-w-4xl mx-auto px-6 py-6">
    <div class="text-center mb-16">
      <div
        class="glass inline-flex items-center gap-2 px-5 py-2 rounded-full mb-5"
      >
        <NewspaperIcon class="w-4 h-4 text-[#ff6ec7]" />
        <span
          class="font-mono text-xs font-bold tracking-widest"
          style="color: #ff6ec7"
        >
          CMUSU NEWS & UPDATES
        </span>
      </div>
      <h2
        class="font-black text-dark leading-tight tracking-tight mb-3"
        style="font-size: clamp(2rem, 5vw, 3.5rem)"
      >
        ข่าวสารและประกาศ
      </h2>
      <p
        class="font-light text-lg max-w-sm mx-auto mb-6"
        style="color: #8b7bae"
      >
        อัปเดตความเคลื่อนไหวจากสโมสรนักศึกษา มหาวิทยาลัยเชียงใหม่
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

    <div
      v-if="newsGroups.length === 0"
      class="glass flex flex-col items-center justify-center py-20 px-6 text-center rounded-[2rem] mt-10 animate-fade-in"
    >
      <div
        class="text-6xl mb-6 select-none opacity-80"
        style="filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.05))"
      >
        📭
      </div>
      <h3 class="text-2xl font-black text-dark mb-3">
        ยังไม่มีข่าวสารหรือประกาศในขณะนี้
      </h3>
      <p class="text-base font-light max-w-md" style="color: #8b7bae">
        ทีมงานกำลังเตรียมข้อมูลและกิจกรรมดีๆ ไว้รอทุกคนอยู่
        โปรดติดตามการอัปเดตจากสโมสรนักศึกษาเร็วๆ นี้นะครับ/ค่ะ!
      </p>
    </div>

    <div v-else class="relative">
      <div
        class="absolute top-0 bottom-0 w-0.5 rounded-full pointer-events-none hidden sm:block"
        style="
          left: 88px;
          background: linear-gradient(
            to bottom,
            transparent,
            #ff6ec7 10%,
            #a259ff 50%,
            #5bc8ff 90%,
            transparent
          );
        "
      ></div>

      <template v-for="(group, groupIdx) in newsGroups" :key="group.month">
        <div class="flex gap-6 mb-8 mt-12 first:mt-0 relative z-10">
          <div class="hidden sm:block shrink-0 w-[88px]"></div>
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
          :key="item.id"
          class="flex gap-6 mb-5 relative z-10"
          :style="{ animationDelay: groupIdx * 0.1 + i * 0.05 + 's' }"
        >
          <a :href="item.href" target="_blank" class="flex flex-1 gap-6">
            <div class="hidden sm:block relative shrink-0 w-[88px] text-right pr-5 pt-4">
              <span
                class="font-black text-2xl"
                :style="{ color: item.color || '#8B7BAE' }"
                >{{ item.day }}</span
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
              class="flex-1 quest-card group cursor-pointer hover:-translate-y-1 transition-transform duration-300"
              :class="item.highlight ? 'ring-2 ring-offset-1' : ''"
              :style="item.highlight ? { ringColor: item.color } : {}"
            >
              <div class="flex items-start justify-between gap-3 mb-2">
                <div class="flex items-center gap-3">
                  <span
                    class="sm:hidden font-black text-xl mr-1"
                    :style="{ color: item.color || '#8B7BAE' }"
                    >{{ item.day }}</span
                  >
                  <component
                    :is="iconMap[item.icon]"
                    class="w-7 h-7 select-none shrink-0"
                    :style="{ color: item.color }"
                    style="filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))"
                  />

                  <div>
                    <span
                      class="tag-pill text-xs flex items-center gap-1 font-semibold"
                      :style="{
                        color: item.color || '#A259FF',
                        borderColor: (item.color || '#A259FF') + '50',
                        background: (item.color || '#A259FF') + '14',
                      }"
                    >
                      {{ item.category }}
                    </span>
                  </div>
                </div>
              </div>

              <h3
                class="font-black text-dark text-lg leading-tight mb-2 mt-3 group-hover:text-opacity-80 transition-colors"
              >
                {{ item.title }}
              </h3>
              <p
                class="text-sm font-light leading-relaxed mb-4 line-clamp-2"
                style="color: #8b7bae"
              >
                {{ item.desc }}
              </p>

              <div class="flex items-center justify-between mt-2">
                <div
                  v-if="item.badge"
                  class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-bold"
                  :style="{
                    background: '#ef444415',
                    color: '#ef4444',
                  }"
                >
                  <FireIcon class="w-3.5 h-3.5" /> {{ item.badge }}
                </div>
                <div v-else></div>

                <span
                  class="text-xs font-bold flex items-center gap-1"
                  :style="{ color: item.color }"
                >
                  อ่านเพิ่มเติม <ArrowRightIcon class="w-3 h-3" />
                </span>
              </div>
            </div>
          </a>
        </div>
      </template>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import {
  NewspaperIcon,
  BellAlertIcon,
  FireIcon,
  CalendarDaysIcon,
  ArrowRightIcon,
  SparklesIcon,
} from "@heroicons/vue/24/solid";

// เตรียม Map สำหรับแปลงชื่อ Icon
const iconMap = {
  SparklesIcon,
  NewspaperIcon,
  BellAlertIcon,
  FireIcon,
};

const meta = [
  { icon: NewspaperIcon, text: "ข่าวสารทั้งหมด", color: "#FF6EC7" },
  { icon: BellAlertIcon, text: "อัปเดตล่าสุด", color: "#5BC8FF" },
];

const newsGroups = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    const response = await fetch("/api/news");
    if (!response.ok) throw new Error("โหลดข้อมูลไม่สำเร็จ");

    const result = await response.json();
    if (result.status === "success") {
      newsGroups.value = result.data;
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = "ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้";
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* เพิ่มแอนิเมชันสำหรับตอนโหลด Empty State */
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
