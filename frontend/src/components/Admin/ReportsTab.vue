<template>
  <div class="animate-fade-in relative">
    <div
      v-if="openFilterDropdown"
      @click="openFilterDropdown = null"
      class="fixed inset-0 z-30"
    ></div>

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

    <div class="flex flex-wrap gap-3 mb-5 relative z-40">
      <div class="relative">
        <button
          @click="openFilterDropdown = openFilterDropdown === 'topic' ? null : 'topic'"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold border shadow-sm transition-all bg-white hover:bg-gray-50"
          :class="filterTopic ? 'border-[#ff6ec7] text-[#ff6ec7]' : 'border-gray-200 text-gray-600'"
        >
          <FunnelIcon class="w-4 h-4" />
          {{ filterTopic ? getTopicStyle(filterTopic).label : 'ทุกประเภท' }}
          <ChevronDownIcon
            class="w-4 h-4 transition-transform duration-200"
            :class="{ 'rotate-180': openFilterDropdown === 'topic' }"
          />
        </button>
        <transition
          enter-active-class="transition ease-out duration-150"
          enter-from-class="transform opacity-0 scale-95 translate-y-[-10px]"
          enter-to-class="transform opacity-100 scale-100 translate-y-0"
          leave-active-class="transition ease-in duration-100"
          leave-from-class="transform opacity-100 scale-100 translate-y-0"
          leave-to-class="transform opacity-0 scale-95 translate-y-[-10px]"
        >
          <div
            v-if="openFilterDropdown === 'topic'"
            class="absolute z-50 mt-2 w-44 origin-top bg-white border border-gray-100 rounded-2xl shadow-xl overflow-hidden"
          >
            <div class="p-2 flex flex-col gap-1">
              <button
                @click="filterTopic = null; openFilterDropdown = null; currentPage = 1"
                class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold text-gray-600 hover:bg-gray-50 transition-colors"
                :class="{ 'bg-gray-100': !filterTopic }"
              >
                ทุกประเภท
              </button>
              <button
                v-for="(style, key) in topicStyles"
                :key="key"
                @click="filterTopic = key; openFilterDropdown = null; currentPage = 1"
                class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-colors"
                :class="[style.hoverClass, filterTopic === key ? style.activeClass : 'text-gray-700']"
              >
                {{ style.label }}
              </button>
            </div>
          </div>
        </transition>
      </div>

      <div class="relative">
        <button
          @click="openFilterDropdown = openFilterDropdown === 'role' ? null : 'role'"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold border shadow-sm transition-all bg-white hover:bg-gray-50"
          :class="filterRole ? 'border-[#ff6ec7] text-[#ff6ec7]' : 'border-gray-200 text-gray-600'"
        >
          <UserIcon class="w-4 h-4" />
          {{ filterRole ? getUserRoleLabel(filterRole) : 'ทุกกลุ่มผู้ใช้' }}
          <ChevronDownIcon
            class="w-4 h-4 transition-transform duration-200"
            :class="{ 'rotate-180': openFilterDropdown === 'role' }"
          />
        </button>
        <transition
          enter-active-class="transition ease-out duration-150"
          enter-from-class="transform opacity-0 scale-95 translate-y-[-10px]"
          enter-to-class="transform opacity-100 scale-100 translate-y-0"
          leave-active-class="transition ease-in duration-100"
          leave-from-class="transform opacity-100 scale-100 translate-y-0"
          leave-to-class="transform opacity-0 scale-95 translate-y-[-10px]"
        >
          <div
            v-if="openFilterDropdown === 'role'"
            class="absolute z-50 mt-2 w-44 origin-top bg-white border border-gray-100 rounded-2xl shadow-xl overflow-hidden"
          >
            <div class="p-2 flex flex-col gap-1">
              <button
                @click="filterRole = null; openFilterDropdown = null; currentPage = 1"
                class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold text-gray-600 hover:bg-gray-50 transition-colors"
                :class="{ 'bg-gray-100': !filterRole }"
              >
                ทุกกลุ่มผู้ใช้
              </button>
              <button
                v-for="(label, key) in userRoles"
                :key="key"
                @click="filterRole = key; openFilterDropdown = null; currentPage = 1"
                class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold text-gray-700 hover:bg-pink-50 hover:text-[#ff6ec7] transition-colors"
                :class="{ 'bg-pink-50 text-[#ff6ec7]': filterRole === key }"
              >
                {{ label }}
              </button>
            </div>
          </div>
        </transition>
      </div>

      <button
        v-if="filterTopic || filterRole"
        @click="filterTopic = null; filterRole = null; currentPage = 1"
        class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold text-gray-400 hover:text-red-500 hover:bg-red-50 border border-transparent hover:border-red-100 transition-colors"
      >
        <XMarkIcon class="w-3.5 h-3.5" /> ล้างตัวกรอง
      </button>
    </div>

    <div
      v-if="isLoading"
      class="text-center py-20 text-[#ff6ec7] animate-pulse font-bold"
    >
      กำลังโหลดข้อมูลเสียงสะท้อน...
    </div>

    <div v-else class="glass rounded-3xl overflow-hidden shadow-sm">
      <div class="md:hidden flex flex-col gap-4 p-4 bg-gray-50/50">
        <div
          v-for="report in paginatedReports"
          :key="'mobile-' + report.id"
          class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-3"
        >
          <div
            class="flex items-start justify-between gap-2 border-b pb-3 border-gray-100"
          >
            <span
              class="shrink-0 px-2.5 py-1 rounded-lg text-[10px] font-bold whitespace-nowrap"
              :class="getTopicStyle(report.topic_type).class"
            >
              {{ getTopicStyle(report.topic_type).label }}
            </span>
            <div class="flex flex-col items-end">
              <span class="text-[10px] font-bold text-gray-800">
                {{
                  new Date(report.created_at).toLocaleDateString("th-TH", {
                    day: "numeric",
                    month: "short",
                  })
                }}
              </span>
              <span class="text-[9px] text-gray-400">
                {{
                  new Date(report.created_at).toLocaleTimeString("th-TH", {
                    hour: "2-digit",
                    minute: "2-digit",
                  })
                }}
                น.
              </span>
            </div>
          </div>

          <h4 class="font-bold text-gray-800 text-base leading-tight mt-1">
            {{ report.title }}
          </h4>

          <div
            class="bg-gray-50 p-3 rounded-xl border border-gray-100 mt-1 max-h-32 overflow-y-auto custom-scrollbar"
          >
            <p
              class="text-xs text-gray-600 whitespace-pre-wrap leading-relaxed"
            >
              {{ report.description }}
            </p>
          </div>

          <div
            class="flex flex-wrap items-center justify-between gap-2 mt-2 pt-3 border-t border-gray-100"
          >
            <div class="flex items-center gap-1.5">
              <div
                class="w-5 h-5 rounded-full bg-[#ff6ec7]/10 flex items-center justify-center"
              >
                <span class="text-[#ff6ec7] font-bold text-[10px]">{{
                  getUserRoleLabel(report.user_type)[0]
                }}</span>
              </div>
              <span class="font-bold text-gray-800 text-xs">
                {{ getUserRoleLabel(report.user_type) }}
              </span>
            </div>
            <span
              class="text-[10px] text-gray-500 font-mono bg-white px-2 py-1 rounded-lg border w-fit truncate max-w-[150px]"
            >
              {{ report.contact_info || "ไม่ประสงค์ออกนาม" }}
            </span>
          </div>
        </div>

        <div
          v-if="filteredReports.length === 0"
          class="p-8 text-center text-gray-500 bg-white rounded-2xl border border-dashed"
        >
          <MegaphoneIcon class="w-10 h-10 text-gray-300 mx-auto mb-2" />
          <p class="text-sm font-bold">{{ filterTopic || filterRole ? 'ไม่พบรายการที่ตรงกับตัวกรอง' : 'ยังไม่มีข้อมูลเสียงสะท้อน' }}</p>
        </div>
      </div>

      <div class="hidden md:block overflow-x-auto">
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
              :key="'desktop-' + report.id"
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

            <tr v-if="filteredReports.length === 0">
              <td colspan="3" class="p-16 text-center text-gray-500">
                <MegaphoneIcon class="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p class="font-bold text-lg">{{ filterTopic || filterRole ? 'ไม่พบรายการที่ตรงกับตัวกรอง' : 'ยังไม่มีข้อมูลเสียงสะท้อนในระบบ' }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="totalPages > 1"
        class="flex flex-col sm:flex-row justify-between items-center p-4 border-t border-gray-100 bg-white/40 gap-4"
      >
        <span class="text-xs text-gray-500 font-bold text-center sm:text-left">
          แสดง {{ (currentPage - 1) * itemsPerPage + 1 }} ถึง
          {{ Math.min(currentPage * itemsPerPage, filteredReports.length) }} จากทั้งหมด
          {{ filteredReports.length }} รายการ
        </span>

        <div class="flex items-center gap-2 w-full sm:w-auto justify-center">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="shrink-0 px-3 py-1.5 rounded-lg text-sm font-bold border border-gray-200 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white transition-colors"
          >
            ก่อนหน้า
          </button>

          <div
            class="flex items-center gap-1 overflow-x-auto max-w-[150px] sm:max-w-none scrollbar-hide px-1"
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
            class="shrink-0 px-3 py-1.5 rounded-lg text-sm font-bold border border-gray-200 text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-white transition-colors"
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
import {
  MegaphoneIcon,
  FunnelIcon,
  ChevronDownIcon,
  XMarkIcon,
  UserIcon,
} from "@heroicons/vue/24/solid";

const reports = ref([]);
const isLoading = ref(true);

const openFilterDropdown = ref(null);
const filterTopic = ref(null);
const filterRole = ref(null);

const topicStyles = {
  feedback: {
    label: "💡 เสนอแนะ",
    class: "bg-blue-100 text-blue-700 border border-blue-200",
    hoverClass: "hover:bg-blue-50 hover:text-blue-700",
    activeClass: "bg-blue-50 text-blue-700",
  },
  complaint: {
    label: "🚨 ร้องเรียน",
    class: "bg-red-100 text-red-700 border border-red-200",
    hoverClass: "hover:bg-red-50 hover:text-red-700",
    activeClass: "bg-red-50 text-red-700",
  },
  inquiry: {
    label: "❓ สอบถาม",
    class: "bg-green-100 text-green-700 border border-green-200",
    hoverClass: "hover:bg-green-50 hover:text-green-700",
    activeClass: "bg-green-50 text-green-700",
  },
};

const userRoles = {
  student: "นักศึกษา",
  staff: "บุคลากร",
  alumni: "ศิษย์เก่า",
  general: "บุคคลทั่วไป",
};

const currentPage = ref(1);
const itemsPerPage = 10;

const filteredReports = computed(() => {
  return reports.value.filter((r) => {
    if (filterTopic.value && r.topic_type !== filterTopic.value) return false;
    if (filterRole.value && r.user_type !== filterRole.value) return false;
    return true;
  });
});

const totalPages = computed(() => {
  return Math.ceil(filteredReports.value.length / itemsPerPage) || 1;
});

const paginatedReports = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredReports.value.slice(start, end);
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
      currentPage.value = 1;
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
  animation: fadeIn 0.4s ease-out forwards;
}

/* ซ่อน Scrollbar ของตารางและปุ่มเปลี่ยนหน้า แต่ยังเอานิ้วไถได้ */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* แต่ง Scrollbar เล็กๆ สำหรับกล่องข้อความรายละเอียดให้ดูสะอาดตา */
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
