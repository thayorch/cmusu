<template>
  <div class="animate-fade-in p-4 md:p-0">
    <div class="max-w-2xl">
      <div
        v-if="feedback.message"
        :class="
          feedback.isError
            ? 'bg-red-50 text-red-600 border-red-100'
            : 'bg-green-50 text-green-600 border-green-100'
        "
        class="mb-6 p-4 rounded-2xl border flex items-center gap-3 animate-fade-in"
      >
        <CheckCircleIcon v-if="!feedback.isError" class="w-5 h-5" />
        <ExclamationTriangleIcon v-else class="w-5 h-5" />
        <span class="font-bold text-sm">{{ feedback.message }}</span>
      </div>

      <div class="glass rounded-3xl p-6 md:p-8 shadow-sm border border-white">
        <div class="flex items-center gap-3 mb-6">
          <div class="p-3 bg-[#a259ff]/10 rounded-2xl">
            <ShieldCheckIcon class="w-6 h-6 text-[#a259ff]" />
          </div>
          <div>
            <h4 class="text-xl font-black text-gray-800">เพิ่มสิทธิ์ Admin</h4>
            <p class="text-xs text-gray-500">
              จัดการสิทธิ์โดยตรงผ่านระบบ Supabase Auth
            </p>
          </div>
        </div>

        <form @submit.prevent="submitPromotion" class="space-y-5">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-2 pl-1"
              >อีเมล CMU IT Account</label
            >
            <input
              v-model="email"
              type="email"
              required
              placeholder="name.surname@cmu.ac.th"
              class="w-full px-5 py-3.5 rounded-2xl bg-gray-50/50 border border-gray-200 outline-none focus:ring-4 focus:ring-[#a259ff]/10 focus:border-[#a259ff] transition-all"
              :disabled="loading"
            />
          </div>

          <button
            type="submit"
            :disabled="loading || !email"
            class="w-full py-4 bg-gray-900 hover:bg-black text-white font-black rounded-2xl shadow-lg shadow-gray-200 transition-all active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <span
              v-if="loading"
              class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"
            ></span>
            ยืนยันการแต่งตั้งแอดมิน
          </button>
        </form>

        <div class="mt-8 pt-6 border-t border-gray-100">
          <h5
            class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3"
          >
            คำแนะนำ
          </h5>
          <ul class="text-xs text-gray-500 space-y-2">
            <li class="flex gap-2">
              <span>•</span> สิทธิ์จะถูกบันทึกใน <b>app_metadata</b> ของระบบ
              Auth โดยตรง
            </li>
            <li class="flex gap-2">
              <span>•</span> ผู้ใช้ที่ได้รับสิทธิ์ต้อง
              <b>Logout และ Login ใหม่</b> เพื่ออัปเดต Token
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import {
  ShieldCheckIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from "@heroicons/vue/24/solid";

const email = ref("");
const loading = ref(false);
const feedback = reactive({ message: "", isError: false });

const submitPromotion = async () => {
  loading.value = true;
  feedback.message = "";

  try {
    const csrfRes = await fetch("/api/csrf-token", { credentials: "include" });
    const { csrf_token } = await csrfRes.json();

    const res = await fetch("/api/admin/promote", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf_token,
      },
      credentials: "include",
      body: JSON.stringify({ email: email.value }),
    });

    const result = await res.json();

    if (res.ok && result.status === "success") {
      feedback.message = result.message;
      feedback.isError = false;
      email.value = "";
    } else {
      feedback.message = result.message || "ไม่สามารถดำเนินการได้";
      feedback.isError = true;
    }
  } catch (e) {
    feedback.message = "เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์";
    feedback.isError = true;
  } finally {
    loading.value = false;
  }
};
</script>
