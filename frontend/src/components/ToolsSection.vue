<template>
  <Navbar />

  <section class="relative z-10 max-w-6xl mx-auto px-6 py-6 min-h-screen">
    <div
      class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10"
    >
      <div>
        <div
          class="glass inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-4"
        >
          <TagIcon class="w-4 h-4 text-[#5BC8FF]" />
          <span
            class="font-mono text-xs font-bold tracking-widest"
            style="color: #5bc8ff"
          >
            BORROW EQUIPMENT
          </span>
        </div>
        <h2
          class="font-black text-dark leading-tight tracking-tight mb-2"
          style="font-size: clamp(2rem, 4vw, 3rem)"
        >
          ยืมอุปกรณ์/ครุภัณฑ์
        </h2>
        <p class="font-light" style="color: #8b7bae">
          ระบบตรวจสอบสถานะและขอยืมครุภัณฑ์ สโมสรนักศึกษามหาวิทยาลัยเชียงใหม่
        </p>
      </div>

      <div
        class="glass rounded-3xl px-6 py-4 text-center shrink-0 hidden md:block"
      >
        <div class="font-black text-4xl leading-none" style="color: #5bc8ff">
          {{ equipments.length }}
        </div>
        <div class="font-mono text-xs mt-1" style="color: #8b7bae">
          Items Available
        </div>
      </div>
    </div>

    <div
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
    >
      <div
        v-for="item in equipments"
        :key="item.id"
        class="quest-card !p-5 flex flex-col group relative"
        style="transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)"
      >
        <div class="absolute top-4 left-4 z-10">
          <span
            v-if="item.available > 0"
            class="px-2 py-1 bg-[#06D6A0]/10 text-[#06D6A0] text-[10px] font-bold rounded-md border border-[#06D6A0]/20"
          >
            {{ item.status }}
          </span>
          <span
            v-else
            class="px-2 py-1 bg-red-500/10 text-red-500 text-[10px] font-bold rounded-md border border-red-500/20"
          >
            ชำรุด/ไม่พร้อมใช้งาน
          </span>
        </div>

        <div
          class="text-6xl mb-4 text-center py-6 bg-white/40 rounded-2xl select-none"
          style="
            filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.05));
            transition: transform 0.3s;
          "
          :class="['group-hover:scale-110']"
        >
          {{ item.emoji }}
        </div>

        <div class="flex-1">
          <div class="text-[10px] font-mono text-gray-400 mb-1">
            {{ item.code }}
          </div>
          <div class="font-bold text-dark text-lg leading-tight mb-1">
            {{ item.name }}
          </div>
          <div
            class="text-sm font-light mb-3 line-clamp-2"
            style="color: #8b7bae"
          >
            {{ item.desc }}
          </div>
        </div>

        <div
          class="flex items-center justify-between mt-4 pt-4 border-t border-[#8b7bae]/20"
        >
          <div class="flex flex-col">
            <span class="text-xs text-gray-500">คงเหลือให้ยืม</span>
            <div class="font-black text-xl" :style="{ color: item.color }">
              {{ item.available }} <span class="text-sm font-normal">ชิ้น</span>
            </div>
          </div>
          <button
            @click="addToCart(item)"
            :disabled="item.available === 0"
            class="px-4 py-2 rounded-xl text-white font-bold text-sm hover:-translate-y-1 transition-transform flex items-center gap-1.5 disabled:opacity-50 disabled:hover:translate-y-0 disabled:cursor-not-allowed"
            :style="{
              background: item.color,
              boxShadow:
                item.available > 0 ? `0 4px 12px ${item.color}40` : 'none',
            }"
          >
            <PlusIcon class="w-4 h-4" /> ยืม
          </button>
        </div>
      </div>
    </div>

    <button
      @click="isCartOpen = true"
      class="fixed bottom-8 right-8 z-40 w-16 h-16 rounded-full flex items-center justify-center shadow-2xl hover:scale-110 transition-transform duration-300"
      style="background: linear-gradient(135deg, #a259ff, #5bc8ff)"
    >
      <ShoppingCartIcon class="w-7 h-7 text-white" />
      <span
        v-if="cartTotalItems > 0"
        class="absolute -top-2 -right-2 bg-[#FF6EC7] text-white text-xs font-black w-7 h-7 flex items-center justify-center rounded-full border-2 border-white shadow-md animate-bounce"
      >
        {{ cartTotalItems }}
      </span>
    </button>

    <div
      v-if="isCartOpen"
      class="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-sm transition-opacity"
      @click.self="isCartOpen = false"
    >
      <div
        class="w-full max-w-md bg-[#f8f9fc] h-full shadow-2xl flex flex-col animate-slide-left"
      >
        <div
          class="px-6 py-14 flex items-center justify-between bg-white border-b border-gray-100"
        >
          <h3 class="font-black text-xl text-dark flex items-center gap-2">
            <ShoppingCartIcon class="w-6 h-6 text-[#A259FF]" />
            รายการที่ต้องการยืม
          </h3>
          <button
            @click="isCartOpen = false"
            class="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <XMarkIcon class="w-6 h-6 text-gray-500" />
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6 space-y-4">
          <div
            v-if="cart.length === 0"
            class="text-center py-10 text-gray-400 font-medium"
          >
            <div class="text-6xl mb-4">🛒</div>
            ยังไม่มีรายการอุปกรณ์ที่ต้องการยืม
          </div>

          <div
            v-for="item in cart"
            :key="item.id"
            class="flex items-center gap-4 bg-white p-4 rounded-2xl shadow-sm border border-gray-100"
          >
            <div
              class="text-3xl bg-gray-50 w-14 h-14 rounded-xl flex items-center justify-center"
            >
              {{ item.emoji }}
            </div>
            <div class="flex-1">
              <div class="font-bold text-dark text-sm line-clamp-1">
                {{ item.name }}
              </div>
              <div class="text-xs text-gray-500">
                พร้อมให้ยืมทั้งหมด: {{ item.available }} ชิ้น
              </div>
            </div>

            <div class="flex items-center gap-2 bg-gray-50 rounded-lg p-1">
              <button
                @click="decreaseQty(item)"
                class="w-6 h-6 flex items-center justify-center rounded bg-white shadow-sm hover:text-red-500"
              >
                -
              </button>
              <span class="text-sm font-bold w-4 text-center">{{
                item.quantity
              }}</span>
              <button
                @click="increaseQty(item)"
                :disabled="item.quantity >= item.available"
                class="w-6 h-6 flex items-center justify-center rounded bg-white shadow-sm text-[#06D6A0] disabled:opacity-30 disabled:cursor-not-allowed"
              >
                +
              </button>
            </div>
          </div>
        </div>

        <div class="p-6 bg-white border-t border-gray-100">
          <button
            class="w-full py-4 rounded-2xl text-white font-bold text-lg shadow-lg hover:-translate-y-1 transition-transform"
            style="background: linear-gradient(135deg, #a259ff, #5bc8ff)"
            :disabled="cart.length === 0"
            :class="{
              'opacity-50 cursor-not-allowed hover:translate-y-0':
                cart.length === 0,
            }"
          >
            ยืนยันการขอยืม
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from "vue";
import {
  TagIcon,
  ShoppingCartIcon,
  PlusIcon,
  XMarkIcon,
} from "@heroicons/vue/24/solid";

// ข้อมูลจำลองจากไฟล์ CSV
const equipments = [
  {
    id: 1,
    code: "ค.ส.มช. 005 - 024/2568",
    emoji: "📻",
    name: "วิทยุสื่อสารสีแดง HAMheart FB-7K",
    desc: "พร้อม เสาอากาศหางหนู แท่นชาร์จและหูฟัง (ย่านความถี่ประชาชน 245-246.9875)",
    available: 18,
    status: "ดี/พร้อมใช้งาน",
    location: "ห้องสำนักงาน ส.มช.",
    color: "#A259FF",
  },
  {
    id: 2,
    code: "ไม่มีระบุ",
    emoji: "🐘",
    name: "ช้างทอง",
    desc: "ของตกแต่ง/สัญลักษณ์สำหรับจัดงาน",
    available: 1,
    status: "ดี/พร้อมใช้งาน",
    location: "ห้องสำนักงาน ส.มช.",
    color: "#F59E0B",
  },
  {
    id: 3,
    code: "ไม่มีระบุ",
    emoji: "🏷️",
    name: "ป้ายมหาวิทยาลัย",
    desc: "ป้ายชื่อมหาวิทยาลัยเชียงใหม่",
    available: 1,
    status: "ดี/พร้อมใช้งาน",
    location: "ห้องสำนักงาน ส.มช.",
    color: "#5BC8FF",
  },
  {
    id: 4,
    code: "อุปกรณ์ทั่วไป",
    emoji: "🔌",
    name: "ปลั๊กพ่วง 5 เมตร",
    desc: "ปลั๊กพ่วง 4 ช่องเสียบ พร้อมสวิตช์แยก",
    available: 5,
    status: "ดี/พร้อมใช้งาน",
    location: "ห้องเก็บของ ส.มช.",
    color: "#06D6A0",
  },
  {
    id: 5,
    code: "อุปกรณ์เครื่องเสียง",
    emoji: "🎤",
    name: "ไมโครโฟนไร้สาย (คู่)",
    desc: "ไมค์ลอยพร้อมตัวรับสัญญาณ",
    available: 2,
    status: "ดี/พร้อมใช้งาน",
    location: "ห้องสำนักงาน ส.มช.",
    color: "#FF6EC7",
  },
  {
    id: 6,
    code: "ค.ส.มช. 025/2568",
    emoji: "📻",
    name: "วิทยุสื่อสาร WK09",
    desc: "วิทยุสื่อสารส่วนบุคคล",
    available: 0,
    status: "ชำรุด",
    location: "ส่งซ่อม",
    color: "#EF4444",
  },
];

// ระบบตระกร้ายืมของ
const cart = ref([]);
const isCartOpen = ref(false);

// กดปุ่มยืมจากการ์ดด้านนอก
const addToCart = (product) => {
  if (product.available <= 0) return;

  const existingItem = cart.value.find((item) => item.id === product.id);
  if (existingItem) {
    if (existingItem.quantity < product.available) {
      existingItem.quantity++;
    }
  } else {
    cart.value.push({ ...product, quantity: 1 });
  }
};

// กดปุ่ม + ในตะกร้า
const increaseQty = (item) => {
  const existingItem = cart.value.find((i) => i.id === item.id);
  if (existingItem && existingItem.quantity < existingItem.available) {
    existingItem.quantity++;
  }
};

// ลดจำนวนสินค้า (ถ้าน้อยกว่า 1 จะลบออกจากตะกร้า)
const decreaseQty = (item) => {
  const existingItem = cart.value.find((i) => i.id === item.id);
  if (existingItem) {
    if (existingItem.quantity > 1) {
      existingItem.quantity--;
    } else {
      cart.value = cart.value.filter((i) => i.id !== item.id);
    }
  }
};

// คำนวณจำนวนชิ้นรวมในตะกร้า
const cartTotalItems = computed(() => {
  return cart.value.reduce((total, item) => total + item.quantity, 0);
});
</script>

<style scoped>
@keyframes slideLeft {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
.animate-slide-left {
  animation: slideLeft 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
