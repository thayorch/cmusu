<template>
  <section
    class="relative z-10 max-w-7xl mx-auto px-6 py-10 animate-fade-in flex flex-col md:flex-row gap-8"
  >
    <div class="w-full md:w-64 shrink-0">
      <div class="glass p-6 rounded-3xl sticky top-24 shadow-sm">
        <div class="text-center mb-6">
          <div
            class="w-16 h-16 bg-gradient-to-br from-[#ff6ec7] to-[#a259ff] rounded-full flex items-center justify-center mx-auto mb-3 shadow-lg"
          >
            <ShieldCheckIcon class="w-8 h-8 text-white" />
          </div>
          <h2 class="font-black text-xl text-dark">Admin Panel</h2>
          <p class="text-xs text-gray-500">CMUSU Control Center</p>
        </div>

        <nav class="space-y-2">
          <button
            @click="activeTab = 'equipment'"
            :class="
              activeTab === 'equipment'
                ? 'bg-[#a259ff] text-white shadow-md'
                : 'hover:bg-gray-100 text-gray-600'
            "
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-all"
          >
            <ArchiveBoxIcon class="w-5 h-5" /> จัดการครุภัณฑ์
          </button>
          <button
            @click="activeTab = 'news'"
            :class="
              activeTab === 'news'
                ? 'bg-[#5bc8ff] text-white shadow-md'
                : 'hover:bg-gray-100 text-gray-600'
            "
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-all"
          >
            <NewspaperIcon class="w-5 h-5" /> เพิ่มข่าวสาร
          </button>
          <button
            @click="activeTab = 'activities'"
            :class="
              activeTab === 'activities'
                ? 'bg-[#ff6ec7] text-white shadow-md'
                : 'hover:bg-gray-100 text-gray-600'
            "
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-all"
          >
            <CalendarDaysIcon class="w-5 h-5" /> เพิ่มกิจกรรม
          </button>
        </nav>
      </div>
    </div>

    <div class="flex-1">
      <div v-if="activeTab === 'equipment'" class="animate-fade-in">
        <div class="flex justify-between items-end mb-6">
          <div>
            <h3 class="text-3xl font-black text-dark mb-1">
              เพิ่มครุภัณฑ์ใหม่
            </h3>
            <p class="text-gray-500 text-sm">
              เพิ่มรายการอุปกรณ์เข้าสู่แคตตาล็อกส่วนกลาง
            </p>
          </div>
        </div>

        <div class="glass p-8 rounded-3xl shadow-sm">
          <form @submit.prevent="submitEquipment" class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-bold mb-1"
                  >ชื่ออุปกรณ์ <span class="text-red-500">*</span></label
                >
                <input
                  v-model="formEq.name"
                  type="text"
                  required
                  class="w-full px-4 py-2.5 rounded-xl bg-white border outline-none focus:ring-2 focus:ring-[#a259ff]"
                  placeholder="เช่น ลำโพงบลูทูธ"
                />
              </div>
              <div>
                <label class="block text-sm font-bold mb-1">หมวดหมู่</label>
                <select
                  v-model="formEq.category"
                  class="w-full px-4 py-2.5 rounded-xl bg-white border outline-none focus:ring-2 focus:ring-[#a259ff]"
                >
                  <option value="ส่วนกลาง">ส่วนกลาง</option>
                  <option value="ส่วนคณะ">ส่วนคณะ</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-bold mb-1"
                >รายละเอียด <span class="text-red-500">*</span></label
              >
              <textarea
                v-model="formEq.description"
                required
                rows="2"
                class="w-full px-4 py-2.5 rounded-xl bg-white border outline-none focus:ring-2 focus:ring-[#a259ff]"
              ></textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-bold mb-1"
                  >ลิงก์รูปภาพ (URL) <span class="text-red-500">*</span></label
                >
                <input
                  v-model="formEq.image_url"
                  type="url"
                  required
                  class="w-full px-4 py-2.5 rounded-xl bg-white border outline-none focus:ring-2 focus:ring-[#a259ff]"
                  placeholder="https://..."
                />
              </div>
              <div>
                <label class="block text-sm font-bold mb-1"
                  >จำนวนทั้งหมด (ชิ้น)
                  <span class="text-red-500">*</span></label
                >
                <input
                  v-model="formEq.total_quantity"
                  type="number"
                  min="1"
                  required
                  class="w-full px-4 py-2.5 rounded-xl bg-white border outline-none focus:ring-2 focus:ring-[#a259ff]"
                />
              </div>
            </div>

            <button
              type="submit"
              :disabled="isSubmitting"
              class="w-full py-3.5 bg-gray-900 hover:bg-black text-white font-bold rounded-xl transition-all disabled:opacity-50"
            >
              {{ isSubmitting ? "กำลังบันทึก..." : "+ บันทึกอุปกรณ์ใหม่" }}
            </button>
          </form>
        </div>
      </div>

      <div v-if="activeTab === 'news'" class="animate-fade-in">
        <h3 class="text-3xl font-black text-dark mb-1">เพิ่มประกาศ/ข่าวสาร</h3>
        <p class="text-gray-500 text-sm mb-6">
          กระจายข่าวสารให้หน้าแรกของเว็บอัปเดตอัตโนมัติ
        </p>

        <div class="glass p-8 rounded-3xl shadow-sm">
          <form @submit.prevent="submitNews" class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div>
                <label class="block text-sm font-bold mb-1"
                  >เดือน <span class="text-red-500">*</span></label
                >
                <input
                  v-model="formNews.month_group"
                  type="text"
                  required
                  class="w-full px-4 py-2.5 rounded-xl border"
                  placeholder="เช่น มิถุนายน"
                />
              </div>
              <div>
                <label class="block text-sm font-bold mb-1"
                  >วันที่ <span class="text-red-500">*</span></label
                >
                <input
                  v-model="formNews.day_string"
                  type="text"
                  required
                  class="w-full px-4 py-2.5 rounded-xl border"
                  placeholder="เช่น 01 หรือ 15-20"
                />
              </div>
              <div>
                <label class="block text-sm font-bold mb-1">ประเภท</label>
                <input
                  v-model="formNews.category"
                  type="text"
                  class="w-full px-4 py-2.5 rounded-xl border"
                  placeholder="เช่น ✨ กิจกรรม"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-bold mb-1"
                >หัวข้อข่าว <span class="text-red-500">*</span></label
              >
              <input
                v-model="formNews.title"
                type="text"
                required
                class="w-full px-4 py-2.5 rounded-xl border"
              />
            </div>

            <div>
              <label class="block text-sm font-bold mb-1"
                >เนื้อหาแบบย่อ <span class="text-red-500">*</span></label
              >
              <textarea
                v-model="formNews.description"
                required
                rows="3"
                class="w-full px-4 py-2.5 rounded-xl border"
              ></textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-bold mb-1"
                  >ลิงก์อ่านเพิ่มเติม (URL)</label
                >
                <input
                  v-model="formNews.href"
                  type="url"
                  class="w-full px-4 py-2.5 rounded-xl border"
                  placeholder="https://..."
                />
              </div>
              <div>
                <label class="block text-sm font-bold mb-1"
                  >สีหลักของข่าว (Hex Code)</label
                >
                <input
                  v-model="formNews.item_color"
                  type="text"
                  class="w-full px-4 py-2.5 rounded-xl border"
                  placeholder="#A259FF"
                />
              </div>
            </div>

            <button
              type="submit"
              :disabled="isSubmitting"
              class="w-full py-3.5 bg-[#5bc8ff] hover:opacity-90 text-white font-bold rounded-xl transition-all"
            >
              ประกาศข่าวสาร
            </button>
          </form>
        </div>
      </div>

      <div v-if="activeTab === 'activities'" class="animate-fade-in">
        <h3 class="text-3xl font-black text-dark mb-1">เพิ่มกิจกรรมใหม่</h3>
        <p class="text-gray-500 text-sm mb-6">
          ลงปฏิทินกิจกรรมของสโมสรนักศึกษาตลอดปี
        </p>

        <div class="glass p-8 rounded-3xl shadow-sm text-center">
          <CalendarDaysIcon class="w-16 h-16 text-[#ff6ec7] mx-auto mb-4" />
          <h4 class="text-xl font-bold">กำลังพัฒนาระบบฟอร์มกิจกรรม</h4>
          <p class="text-gray-500">
            สามารถใช้หลักการเดียวกับฟอร์มข่าวสารในการสร้างต่อได้เลยครับ
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import {
  ShieldCheckIcon,
  ArchiveBoxIcon,
  NewspaperIcon,
  CalendarDaysIcon,
} from "@heroicons/vue/24/solid";

const activeTab = ref("equipment");
const isSubmitting = ref(false);

// 📝 ข้อมูลฟอร์มอุปกรณ์
const formEq = reactive({
  name: "",
  category: "ส่วนกลาง",
  description: "",
  image_url: "",
  total_quantity: 1,
});

// 📝 ข้อมูลฟอร์มข่าวสาร
const formNews = reactive({
  month_group: "",
  day_string: "",
  category: "📢 ข่าวสาร",
  title: "",
  description: "",
  href: "",
  item_color: "#A259FF",
  icon_name: "NewspaperIcon",
});

// ฟังก์ชันดึง CSRF Token (จำเป็นสำหรับความปลอดภัย)
const getCsrfToken = async () => {
  const res = await fetch("/api/csrf-token", {
    method: "GET",
    credentials: "include",
  });
  if (!res.ok) throw new Error("CSRF Error");
  const data = await res.json();
  return data.csrf_token;
};

// 🚀 ยิง API บันทึกอุปกรณ์ใหม่
const submitEquipment = async () => {
  isSubmitting.value = true;
  try {
    const token = await getCsrfToken();
    const res = await fetch("/api/admin/equipment", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": token },
      credentials: "include",
      body: JSON.stringify(formEq),
    });

    if (res.ok) {
      alert("✅ เพิ่มครุภัณฑ์สำเร็จ!");
      Object.keys(formEq).forEach(
        (k) => (formEq[k] = k === "total_quantity" ? 1 : ""),
      ); // ล้างฟอร์ม
    } else {
      alert("❌ เกิดข้อผิดพลาดจากเซิร์ฟเวอร์");
    }
  } catch (error) {
    alert("เกิดข้อผิดพลาดในการส่งข้อมูล");
  } finally {
    isSubmitting.value = false;
  }
};

// 🚀 ยิง API บันทึกข่าวสารใหม่
const submitNews = async () => {
  isSubmitting.value = true;
  try {
    const token = await getCsrfToken();
    const res = await fetch("/api/admin/news", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": token },
      credentials: "include",
      body: JSON.stringify(formNews),
    });

    if (res.ok) {
      alert("✅ ประกาศข่าวสารสำเร็จ!");
      Object.keys(formNews).forEach((k) => (formNews[k] = "")); // ล้างฟอร์ม
    } else {
      alert("❌ เกิดข้อผิดพลาดจากเซิร์ฟเวอร์");
    }
  } catch (error) {
    alert("เกิดข้อผิดพลาดในการส่งข้อมูล");
  } finally {
    isSubmitting.value = false;
  }
};
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
  animation: fadeIn 0.4s ease-out forwards;
}
</style>
