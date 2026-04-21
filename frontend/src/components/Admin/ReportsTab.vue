<template>
  <div class="animate-fade-in">
    <div class="mb-6">
      <h3
        class="text-2xl md:text-3xl font-black text-dark mb-1 flex items-center gap-2"
      >
        <MegaphoneIcon class="w-7 h-7 md:w-8 md:h-8 text-[#ff6ec7]" />
        เสียงสะท้อน (VOC)
      </h3>
      <p class="text-gray-500 text-sm">
        รายการข้อเสนอแนะและข้อร้องเรียนจากผู้ใช้งาน
      </p>
    </div>

    <div
      v-if="isLoading"
      class="text-center py-20 text-[#ff6ec7] animate-pulse font-bold"
    >
      กำลังโหลดข้อมูลเสียงสะท้อน...
    </div>

    <div v-else class="glass rounded-3xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr class="bg-white/40 border-b border-gray-200">
              <th class="p-4 font-bold text-sm text-gray-600">
                หัวข้อและรายละเอียด
              </th>
              <th class="p-4 font-bold text-sm text-gray-600 w-56">
                ผู้ให้ข้อมูล
              </th>
              <th class="p-4 font-bold text-sm text-gray-600 w-48 text-center">
                วันที่แจ้ง
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="report in paginatedReports"
              :key="report.id"
              class="border-b border-gray-100 hover:bg-white/60 transition-colors"
            >
              <td class="p-4 align-top">
                <div class="flex flex-col gap-2">
                  <div class="flex items-center gap-2">
                    <span
                      class="px-2 py-1 rounded-lg text-[10px] font-bold whitespace-nowrap"
                      :class="getTopicStyle(report.topic_type).class"
                    >
                      {{ getTopicStyle(report.topic_type).label }}
                    </span>
                    <h4 class="font-bold text-gray-800 text-base">
                      {{ report.title }}
                    </h4>
                  </div>
                  <div
                    class="bg-gray-50 p-3 rounded-xl border border-gray-100 max-h-24 overflow-y-auto custom-scrollbar"
                  >
                    <p
                      class="text-sm text-gray-600 whitespace-pre-wrap leading-relaxed"
                    >
                      {{ report.description }}
                    </p>
                  </div>
                </div>
              </td>

              <td class="p-4 align-top pt-5">
                <div class="flex flex-col gap-1">
                  <div class="flex items-center gap-1.5 mb-1">
                    <div
                      class="w-5 h-5 rounded-full bg-[#ff6ec7]/10 flex items-center justify-center"
                    >
                      <span class="text-[#ff6ec7] font-bold text-[10px]">{{
                        getUserRoleLabel(report.user_type)[0]
                      }}</span>
                    </div>
                    <span class="font-bold text-gray-800 text-sm">
                      {{ getUserRoleLabel(report.user_type) }}
                    </span>
                  </div>
                  <span
                    class="text-xs text-gray-500 font-mono bg-white px-2 py-1 rounded-lg border w-fit"
                  >
                    {{ report.contact_info || "ไม่ประสงค์ออกนาม" }}
                  </span>
                </div>
              </td>

              <td class="p-4 align-top pt-5 text-center">
                <div class="flex flex-col items-center justify-center gap-1">
                  <span class="text-sm font-bold text-gray-700">
                    {{
                      new Date(report.created_at).toLocaleDateString("th-TH", {
                        day: "numeric",
                        month: "short",
                        year: "numeric",
                      })
                    }}
                  </span>
                  <span
                    class="text-xs text-gray-400 font-bold bg-gray-50 px-2 py-0.5 rounded-md border"
                  >
                    {{
                      new Date(report.created_at).toLocaleTimeString("th-TH", {
                        hour: "2-digit",
                        minute: "2-digit",
                      })
                    }}
                    น.
                  </span>
                </div>
              </td>
            </tr>

            <tr v-if="reports.length === 0">
              <td colspan="3" class="p-16 text-center text-gray-500">
                <MegaphoneIcon class="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p class="font-bold text-lg">ยังไม่มีข้อมูลเสียงสะท้อนในระบบ</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="totalPages > 1"
        class="flex flex-col sm:flex-row justify-between items-center p-4 border-t border-gray-100 bg-white/40 gap-4"
      >
        <span class="text-xs text-gray-500 font-bold">
          แสดง {{ (currentPage - 1) * itemsPerPage + 1 }} ถึง
          {{ Math.min(currentPage * itemsPerPage, reports.length) }} จากทั้งหมด
          {{ reports.length }} รายการ
        </span>

        <div class="flex items-center gap-2">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="px-3 py-1.5 rounded-lg text-sm font-bold border border-gray-200 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white transition-colors"
          >
            ก่อนหน้า
          </button>

          <div
            class="flex items-center gap-1 overflow-x-auto max-w-[150px] sm:max-w-none scrollbar-hide"
          >
            <button
              v-for="page in totalPages"
              :key="page"
              @click="currentPage = page"
              class="shrink-0 w-8 h-8 flex items-center justify-center rounded-lg text-sm font-bold transition-all"
              :class="
                currentPage === page
                  ? 'bg-[#ff6ec7] text-white shadow-md'
                  : 'text-gray-600 hover:bg-white border border-transparent hover:border-gray-200'
              "
            >
              {{ page }}
            </button>
          </div>

          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="px-3 py-1.5 rounded-lg text-sm font-bold border border-gray-200 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white transition-colors"
          >
            ถัดไป
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { MegaphoneIcon } from "@heroicons/vue/24/solid";

const reports = ref([]);
const isLoading = ref(true);

// 💡 เปลี่ยนกลับมาเป็น 10 รายการต่อหน้า เพื่อให้เท่ากับหน้าขอยืม
const currentPage = ref(1);
const itemsPerPage = 10;

const totalPages = computed(() => {
  return Math.ceil(reports.value.length / itemsPerPage) || 1;
});

const paginatedReports = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return reports.value.slice(start, end);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const getTopicStyle = (type) => {
  const styles = {
    feedback: {
      label: "💡 เสนอแนะ",
      class: "bg-blue-100 text-blue-700 border border-blue-200",
    },
    complaint: {
      label: "🚨 ร้องเรียน",
      class: "bg-red-100 text-red-700 border border-red-200",
    },
    inquiry: {
      label: "❓ สอบถาม",
      class: "bg-green-100 text-green-700 border border-green-200",
    },
  };
  return (
    styles[type] || {
      label: type,
      class: "bg-gray-100 text-gray-700 border border-gray-200",
    }
  );
};

const getUserRoleLabel = (role) => {
  const roles = {
    student: "นักศึกษา",
    staff: "บุคลากร",
    alumni: "ศิษย์เก่า",
    general: "บุคคลทั่วไป",
  };
  return roles[role] || role;
};

const fetchReports = async () => {
  isLoading.value = true;
  try {
    const res = await fetch("/api/admin/reports", { credentials: "include" });
    const json = await res.json();
    if (json.status === "success") {
      reports.value = json.data;
      if (currentPage.value > totalPages.value && totalPages.value > 0) {
        currentPage.value = totalPages.value;
      }
    }
  } catch (e) {
    console.error("Error fetching reports:", e);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchReports();
});
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
  animation: fadeIn 0.3s ease-out forwards;
}

/* ซ่อน Scrollbar ของตารางแต่ยังไถลได้ */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* แต่ง Scrollbar เล็กๆ สำหรับกล่องข้อความรายละเอียด */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
