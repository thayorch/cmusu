<template>
  <Navbar />

  <section class="relative z-10 max-w-5xl mx-auto px-6 py-6 flex items-center">
    <div
      class="glass w-full rounded-[2rem] p-8 md:p-12 shadow-2xl border border-white/20 relative overflow-hidden"
    >
      <div
        class="absolute top-0 right-0 -mr-32 -mt-32 w-96 h-96 rounded-full bg-gradient-to-br from-[#5bc8ff] to-[#a259ff] opacity-20 blur-3xl pointer-events-none"
      ></div>
      <div
        class="absolute bottom-0 left-0 -ml-32 -mb-32 w-96 h-96 rounded-full bg-gradient-to-tr from-[#ff6ec7] to-[#ffd166] opacity-10 blur-3xl pointer-events-none"
      ></div>

      <div class="relative z-10 flex flex-col lg:flex-row gap-12 items-center">
        <div class="flex-1 text-center lg:text-left">
          <div
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#5bc8ff]/10 border border-[#5bc8ff]/30 mb-6"
          >
            <ChatBubbleBottomCenterTextIcon class="w-4 h-4 text-[#5bc8ff]" />
            <span
              class="font-mono text-xs font-bold tracking-wider text-[#5bc8ff]"
            >
              CMU VOICE OF CUSTOMER
            </span>
          </div>

          <h1
            class="font-black text-dark leading-tight tracking-tight mb-6 text-4xl md:text-5xl"
          >
            ระบบรับฟังเสียง <br />
            <span
              class="text-transparent bg-clip-text bg-gradient-to-r from-[#a259ff] to-[#5bc8ff]"
            >
              เพื่อพัฒนาการบริการ
            </span>
          </h1>

          <p
            class="text-base md:text-lg font-light leading-relaxed mb-8"
            style="color: #8b7bae"
          >
            ระบบ VOC หรือ Voice of Customer
            นี้เป็นช่องทางหนึ่งที่จัดทำขึ้นเพื่อรับฟังเสียงจากนักศึกษา บุคลากร
            นักศึกษาเก่า และบุคคลทั่วไป โดยจะรวบรวมข้อคิดเห็น ข้อเสนอแนะ
            และข้อร้องเรียนต่าง ๆ จากผู้รับบริการของมหาวิทยาลัยเชียงใหม่
            เพื่อนำมาใช้ในการพัฒนาบริการของสโมสรนักศึกษาให้มีคุณภาพมาตรฐานที่ดี
            และตรงตามความต้องการของผู้รับบริการให้มากยิ่งขึ้น
          </p>

          <div class="flex flex-wrap gap-4 justify-center lg:justify-start">
            <button
              @click="isFormOpen = true"
              class="px-6 py-3.5 rounded-xl bg-gradient-to-r from-[#a259ff] to-[#5bc8ff] text-white font-bold shadow-lg shadow-[#a259ff]/30 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex items-center gap-2"
            >
              <PencilSquareIcon class="w-5 h-5" />
              ส่งข้อเสนอแนะ / ร้องเรียน
            </button>
          </div>
        </div>

        <div class="w-full lg:w-5/12 grid grid-cols-2 gap-4">
          <div
            @click="openFormWithRole('student')"
            class="hover:cursor-pointer glass flex flex-col items-center justify-center p-6 rounded-2xl text-center hover:-translate-y-1 transition-transform duration-300"
          >
            <div
              class="w-12 h-12 rounded-full bg-[#A259FF]/15 flex items-center justify-center mb-3"
            >
              <AcademicCapIcon class="w-6 h-6 text-[#A259FF]" />
            </div>
            <h3 class="font-bold text-dark text-sm">นักศึกษา</h3>
          </div>

          <div
            @click="openFormWithRole('staff')"
            class="hover:cursor-pointer glass flex flex-col items-center justify-center p-6 rounded-2xl text-center hover:-translate-y-1 transition-transform duration-300"
          >
            <div
              class="w-12 h-12 rounded-full bg-[#5BC8FF]/15 flex items-center justify-center mb-3"
            >
              <BriefcaseIcon class="w-6 h-6 text-[#5BC8FF]" />
            </div>
            <h3 class="font-bold text-dark text-sm">บุคลากร</h3>
          </div>

          <div
            @click="openFormWithRole('alumni')"
            class="hover:cursor-pointer glass flex flex-col items-center justify-center p-6 rounded-2xl text-center hover:-translate-y-1 transition-transform duration-300"
          >
            <div
              class="w-12 h-12 rounded-full bg-[#FF6EC7]/15 flex items-center justify-center mb-3"
            >
              <UsersIcon class="w-6 h-6 text-[#FF6EC7]" />
            </div>
            <h3 class="font-bold text-dark text-sm">นักศึกษาเก่า</h3>
          </div>

          <div
            @click="openFormWithRole('general')"
            class="hover:cursor-pointer glass flex flex-col items-center justify-center p-6 rounded-2xl text-center hover:-translate-y-1 transition-transform duration-300"
          >
            <div
              class="w-12 h-12 rounded-full bg-[#06D6A0]/15 flex items-center justify-center mb-3"
            >
              <GlobeAltIcon class="w-6 h-6 text-[#06D6A0]" />
            </div>
            <h3 class="font-bold text-dark text-sm">บุคคลทั่วไป</h3>
          </div>
        </div>
      </div>
    </div>
  </section>

  <transition name="fade">
    <div
      v-if="isFormOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm overflow-y-auto"
      @click.self="isFormOpen = false"
    >
      <div
        class="glass w-full max-w-2xl rounded-2xl p-6 md:p-8 shadow-2xl relative my-auto animate-scale-up"
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-black text-dark flex items-center gap-2">
            <PencilSquareIcon class="w-6 h-6 text-[#a259ff]" />
            แบบฟอร์มส่งข้อเสนอแนะ / ร้องเรียน
          </h2>
          <button
            @click="isFormOpen = false"
            class="p-2 rounded-full bg-white/50 hover:bg-red-100 hover:text-red-500 transition-colors text-gray-500"
          >
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="submitForm" class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-bold text-dark mb-1"
                >ประเภทผู้ให้ข้อมูล <span class="text-red-500">*</span></label
              >
              <select
                v-model="formData.userType"
                required
                class="w-full px-4 py-3 rounded-xl bg-white/60 border border-white/50 focus:outline-none focus:ring-2 focus:ring-[#a259ff] text-dark"
              >
                <option value="" disabled>เลือกประเภท...</option>
                <option value="student">นักศึกษา</option>
                <option value="staff">บุคลากร</option>
                <option value="alumni">นักศึกษาเก่า</option>
                <option value="general">บุคคลทั่วไป</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-bold text-dark mb-1"
                >ประเภทเรื่อง <span class="text-red-500">*</span></label
              >
              <select
                v-model="formData.topicType"
                required
                class="w-full px-4 py-3 rounded-xl bg-white/60 border border-white/50 focus:outline-none focus:ring-2 focus:ring-[#5bc8ff] text-dark"
              >
                <option value="" disabled>เลือกประเภทเรื่อง...</option>
                <option value="feedback">ข้อเสนอแนะเพื่อการพัฒนา</option>
                <option value="complaint">ร้องเรียนปัญหา</option>
                <option value="inquiry">สอบถามข้อมูล</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-bold text-dark mb-1"
              >หัวข้อเรื่อง <span class="text-red-500">*</span></label
            >
            <input
              v-model="formData.title"
              type="text"
              required
              placeholder="ระบุหัวข้อที่ต้องการแจ้ง..."
              class="w-full px-4 py-3 rounded-xl bg-white/60 border border-white/50 focus:outline-none focus:ring-2 focus:ring-[#a259ff] text-dark placeholder-gray-400"
            />
          </div>

          <div>
            <label class="block text-sm font-bold text-dark mb-1"
              >รายละเอียด <span class="text-red-500">*</span></label
            >
            <textarea
              v-model="formData.description"
              required
              rows="4"
              placeholder="อธิบายรายละเอียดปัญหาหรือข้อเสนอแนะของคุณ..."
              class="w-full px-4 py-3 rounded-xl bg-white/60 border border-white/50 focus:outline-none focus:ring-2 focus:ring-[#a259ff] text-dark placeholder-gray-400 resize-none"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-bold text-dark mb-1"
              >อีเมลหรือเบอร์โทรศัพท์ (หากต้องการให้ติดต่อกลับ)</label
            >
            <input
              v-model="formData.contactInfo"
              type="text"
              placeholder="example@cmu.ac.th หรือ 08X-XXX-XXXX"
              class="w-full px-4 py-3 rounded-xl bg-white/60 border border-white/50 focus:outline-none focus:ring-2 focus:ring-[#5bc8ff] text-dark placeholder-gray-400"
            />
          </div>

          <div
            v-if="errorMessage"
            class="text-red-500 text-sm font-bold text-center"
          >
            {{ errorMessage }}
          </div>

          <div class="pt-4 border-t border-gray-200/50 flex justify-end gap-3">
            <button
              type="button"
              @click="isFormOpen = false"
              class="px-6 py-3 rounded-xl font-bold text-gray-500 hover:bg-white/50 transition-colors"
              :disabled="isLoading"
            >
              ยกเลิก
            </button>
            <button
              type="submit"
              class="px-6 py-3 rounded-xl bg-gradient-to-r from-[#a259ff] to-[#5bc8ff] text-white font-bold shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="isLoading"
            >
              <span v-if="isLoading">กำลังส่ง...</span>
              <span v-else>ส่งข้อมูล</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>
<script setup>
import { ref, reactive } from "vue";
import Navbar from "../components/Navbar.vue";

import {
  ChatBubbleBottomCenterTextIcon,
  PencilSquareIcon,
  AcademicCapIcon,
  BriefcaseIcon,
  UsersIcon,
  GlobeAltIcon,
  XMarkIcon,
} from "@heroicons/vue/24/solid";

const isFormOpen = ref(false);
const isLoading = ref(false);
const errorMessage = ref("");

// สร้าง Object เก็บข้อมูลของฟอร์ม
const formData = reactive({
  userType: "",
  topicType: "",
  title: "",
  description: "",
  contactInfo: "",
});

// ฟังก์ชันเปิดฟอร์มพร้อมเลือกกลุ่มผู้ใช้ให้อัตโนมัติ (เมื่อคลิกที่การ์ด 4 ใบ)
const openFormWithRole = (role) => {
  formData.userType = role;
  isFormOpen.value = true;
};

// ฟังก์ชันรีเซ็ตฟอร์มให้ว่างเปล่า
const resetForm = () => {
  formData.userType = "";
  formData.topicType = "";
  formData.title = "";
  formData.description = "";
  formData.contactInfo = "";
  errorMessage.value = "";
};

const submitForm = async () => {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const csrfRes = await fetch("/api/csrf-token", {
      method: "GET",
      credentials: "include",
    });

    if (!csrfRes.ok) throw new Error("ไม่สามารถเชื่อมต่อระบบความปลอดภัยได้");

    const csrfData = await csrfRes.json();
    const csrfToken = csrfData.csrf_token;

    const response = await fetch("/api/report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrfToken,
      },
      credentials: "include",
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      throw new Error(`เกิดข้อผิดพลาด: ${response.status}`);
    }

    const result = await response.json();

    alert("ส่งข้อมูลเรียบร้อยแล้ว ขอบคุณสำหรับข้อเสนอแนะครับ/ค่ะ");

    resetForm();
    isFormOpen.value = false;
  } catch (error) {
    console.error("Error submitting form:", error);
    errorMessage.value = "ไม่สามารถส่งข้อมูลได้ กรุณาลองใหม่อีกครั้ง";
  } finally {
    isLoading.value = false;
  }
};
</script>
