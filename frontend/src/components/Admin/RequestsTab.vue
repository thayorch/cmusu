<template>
  <div class="animate-fade-in">
    <div class="mb-6">
      <h3 class="text-2xl md:text-3xl font-black text-dark mb-1 flex items-center gap-2">
        <ClipboardDocumentListIcon class="w-7 h-7 md:w-8 md:h-8 text-[#ffd166]" />
        รายการขอยืม
      </h3>
      <p class="text-gray-500 text-sm">จัดการสถานะการยืม และเช็คคืนอุปกรณ์</p>
    </div>

    <!-- Empty state -->
    <div v-if="borrowRequests.length === 0" class="text-center py-20 text-gray-400">
      <ClipboardDocumentListIcon class="w-12 h-12 mx-auto mb-3 opacity-30" />
      <p class="font-medium">ยังไม่มีรายการขอยืมอุปกรณ์ในขณะนี้</p>
    </div>

    <!-- Card list (ทุกขนาดหน้าจอ) -->
    <div class="flex flex-col gap-4">
      <div
        v-for="req in borrowRequests"
        :key="req.id"
        class="glass rounded-3xl p-4 sm:p-5 shadow-sm flex flex-col gap-4"
      >
        <!-- Row 1: ข้อมูลผู้ยืม + วันที่ -->
        <div class="flex flex-col sm:flex-row sm:items-start gap-3">
          <div class="flex-1 min-w-0">
            <p class="font-black text-gray-800 text-base leading-tight">{{ req.full_name }}</p>
            <p class="text-xs text-gray-400 font-mono mt-0.5">{{ req.student_id }} · {{ req.contact_info }}</p>
          </div>
          <div class="flex gap-4 text-xs shrink-0">
            <span class="text-gray-500">ยืม: <span class="font-bold text-gray-800">{{ req.borrow_date }}</span></span>
            <span class="text-gray-500">คืน: <span class="font-bold text-[#a259ff]">{{ req.return_date }}</span></span>
          </div>
        </div>

        <!-- Row 2: รายการอุปกรณ์ -->
        <div v-if="req.borrow_request_items?.length" class="flex flex-col gap-2">
          <p class="text-[10px] font-black uppercase tracking-wider text-gray-400">รายการอุปกรณ์ที่ยืม:</p>
          <div class="flex flex-wrap gap-2">
            <div
              v-for="(item, index) in req.borrow_request_items"
              :key="index"
              class="flex items-center gap-2.5 bg-[#a259ff]/5 border border-[#a259ff]/10 px-3 py-2 rounded-2xl"
            >
              <div class="w-10 h-10 shrink-0 bg-white rounded-xl overflow-hidden border border-gray-100 flex items-center justify-center">
                <img v-if="item.equipments?.image_url" :src="item.equipments.image_url" class="w-full h-full object-cover" alt="" />
                <span v-else class="text-[9px] text-gray-400">ไม่มีรูป</span>
              </div>
              <div>
                <p class="text-sm font-bold text-gray-800 leading-tight">{{ item.equipments?.name || "ไม่ทราบชื่ออุปกรณ์" }}</p>
                <p class="text-xs font-bold text-[#a259ff]">{{ item.quantity }} ชิ้น</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Row 3: Actions -->
        <div class="flex flex-wrap items-center gap-2 pt-1 border-t border-gray-100">
          <!-- Status dropdown -->
          <div class="relative">
            <button
              @click="toggleDropdown(req.id)"
              :disabled="req.status === 'returned'"
              class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold border transition-all"
              :class="[statusStyle(req.status).btn, req.status === 'returned' ? 'cursor-not-allowed opacity-70' : 'cursor-pointer']"
            >
              <span>{{ statusLabel(req.status) }}</span>
              <ChevronDownIcon
                v-if="req.status !== 'returned'"
                class="w-4 h-4 shrink-0 transition-transform"
                :class="openDropdownId === req.id ? 'rotate-180' : ''"
              />
            </button>
            <Transition
              enter-active-class="transition ease-out duration-150"
              enter-from-class="opacity-0 translate-y-1 scale-95"
              enter-to-class="opacity-100 translate-y-0 scale-100"
              leave-active-class="transition ease-in duration-100"
              leave-from-class="opacity-100 translate-y-0 scale-100"
              leave-to-class="opacity-0 translate-y-1 scale-95"
            >
              <div
                v-if="openDropdownId === req.id"
                class="absolute z-50 bottom-full mb-1 min-w-[160px] bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden"
              >
                <button
                  v-for="opt in statusOptions"
                  :key="opt.value"
                  @click="selectStatus(opt.value, req)"
                  class="w-full flex items-center gap-2 px-4 py-2.5 text-sm font-bold text-left transition-colors"
                  :class="[opt.hover, req.status === opt.value ? opt.active : 'text-gray-700']"
                >
                  <span>{{ opt.label }}</span>
                  <CheckIcon v-if="req.status === opt.value" class="w-4 h-4 ml-auto" />
                </button>
              </div>
            </Transition>
          </div>

          <p v-if="req.status === 'returned'" class="text-[10px] text-gray-400 font-bold italic">เสร็จสิ้นรายการ</p>

          <button
            @click="handleDelete(req)"
            class="ml-auto flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold text-red-500 border border-red-100 bg-red-50 hover:bg-red-100 transition-colors"
          >
            <TrashIcon class="w-3.5 h-3.5" />
            ลบรายการ
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  ClipboardDocumentListIcon,
  ChevronDownIcon,
  CheckIcon,
  TrashIcon,
} from "@heroicons/vue/24/solid";
import { useAlert } from "../../composables/useAlert";
import { useCsrf } from "../../composables/useCsrf";

const { showAlert, showConfirm } = useAlert();
const { getCsrfToken } = useCsrf();

const borrowRequests = ref([]);
const openDropdownId = ref(null);

const statusOptions = [
  {
    value: "pending",
    label: "⏳ รออนุมัติ",
    btn: "bg-yellow-50 text-yellow-700 border-yellow-200 hover:bg-yellow-100",
    hover: "hover:bg-yellow-50",
    active: "text-yellow-700 bg-yellow-50",
  },
  {
    value: "approved",
    label: "🔄 กำลังยืม",
    btn: "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100",
    hover: "hover:bg-blue-50",
    active: "text-blue-700 bg-blue-50",
  },
  {
    value: "returned",
    label: "✅ คืนแล้ว",
    btn: "bg-green-50 text-green-700 border-green-200",
    hover: "hover:bg-green-50",
    active: "text-green-700 bg-green-50",
  },
];

const statusLabel = (status) =>
  statusOptions.find((o) => o.value === status)?.label ?? status;

const statusStyle = (status) =>
  statusOptions.find((o) => o.value === status) ?? statusOptions[0];

const toggleDropdown = (id) => {
  openDropdownId.value = openDropdownId.value === id ? null : id;
};

onMounted(() => {
  fetchRequests();
});

const fetchRequests = async () => {
  try {
    const res = await fetch("/api/admin/requests", { credentials: "include" });
    const json = await res.json();
    if (json.status === "success") borrowRequests.value = json.data;
  } catch (e) {
    console.error(e);
  }
};

const selectStatus = async (newStatus, req) => {
  openDropdownId.value = null;
  if (newStatus === req.status) return;

  if (newStatus === "returned") {
    const ok = await showConfirm(
      "ยืนยันการรับคืนอุปกรณ์? สินค้าจะถูกบวกกลับเข้าคลังทันที",
    );
    if (!ok) return;
  }

  try {
    const csrf_token = await getCsrfToken();

    const res = await fetch("/api/admin/requests/status", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf_token,
      },
      credentials: "include",
      body: JSON.stringify({ id: req.id, status: newStatus }),
    });

    if (res.ok) {
      fetchRequests();
    } else {
      await showAlert("เกิดข้อผิดพลาดในการอัปเดตสถานะ", "error");
    }
  } catch (e) {
    console.error(e);
  }
};

const handleDelete = async (req) => {
  const ok = await showConfirm(
    `ลบรายการขอยืมของ "${req.full_name}" ใช่หรือไม่?`,
  );
  if (!ok) return;

  try {
    const csrf_token = await getCsrfToken();

    const res = await fetch(`/api/admin/requests/${req.id}`, {
      method: "DELETE",
      headers: { "X-CSRF-Token": csrf_token },
      credentials: "include",
    });

    if (res.ok) {
      fetchRequests();
    } else {
      await showAlert("เกิดข้อผิดพลาดในการลบรายการ", "error");
    }
  } catch (e) {
    console.error(e);
  }
};
</script>
