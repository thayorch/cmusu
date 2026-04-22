<template>
  <div class="animate-fade-in">
    <div class="mb-6">
      <h3
        class="text-2xl md:text-3xl font-black text-dark mb-1 flex items-center gap-2"
      >
        <ClipboardDocumentListIcon
          class="w-7 h-7 md:w-8 md:h-8 text-[#ffd166]"
        />
        รายการขอยืม
      </h3>
      <p class="text-gray-500 text-sm">จัดการสถานะการยืม และเช็คคืนอุปกรณ์</p>
    </div>

    <div class="glass rounded-3xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr class="bg-white/40 border-b border-gray-200">
              <th class="p-4 font-bold text-sm text-gray-600">
                ผู้ยืม และ รายการอุปกรณ์
              </th>
              <th class="p-4 font-bold text-sm text-gray-600 w-48">
                วันที่ยืม-คืน
              </th>
              <th class="p-4 font-bold text-sm text-gray-600 w-56 text-center">
                จัดการสถานะ
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="req in borrowRequests"
              :key="req.id"
              class="border-b border-gray-100 hover:bg-white/60 transition-colors"
            >
              <td class="p-4 align-top">
                <div class="flex flex-col gap-1">
                  <p class="font-bold text-gray-800 text-base">
                    {{ req.full_name }}
                  </p>
                  <p class="text-xs text-gray-500 font-mono">
                    {{ req.student_id }} | {{ req.contact_info }}
                  </p>

                  <div
                    v-if="
                      req.borrow_request_items &&
                      req.borrow_request_items.length > 0
                    "
                    class="mt-4 flex flex-col gap-2.5"
                  >
                    <p
                      class="text-[10px] font-black uppercase tracking-wider text-gray-400 border-b pb-1 inline-block w-fit"
                    >
                      รายการอุปกรณ์ที่ยืม:
                    </p>

                    <div
                      v-for="(item, index) in req.borrow_request_items"
                      :key="index"
                      class="flex items-center gap-3 bg-[#a259ff]/5 border border-[#a259ff]/10 p-2 rounded-2xl w-fit hover:bg-white transition-colors shadow-sm"
                    >
                      <div
                        class="w-12 h-12 shrink-0 bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 flex items-center justify-center"
                      >
                        <img
                          v-if="item.equipments?.image_url"
                          :src="item.equipments.image_url"
                          class="w-full h-full object-cover"
                          alt="equipment"
                        />
                        <span v-else class="text-[10px] text-gray-400"
                          >ไม่มีรูป</span
                        >
                      </div>

                      <div class="flex flex-col pr-3">
                        <span
                          class="text-sm font-bold text-gray-800 line-clamp-1"
                        >
                          {{ item.equipments?.name || "ไม่ทราบชื่ออุปกรณ์" }}
                        </span>
                        <span class="text-xs font-bold text-[#a259ff]">
                          จำนวน: {{ item.quantity }} ชิ้น
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </td>

              <td class="p-4 text-sm text-gray-700 align-top pt-5">
                <div class="flex flex-col gap-1">
                  <span class="text-xs text-gray-500"
                    >ยืม:
                    <span class="font-bold text-gray-800">{{
                      req.borrow_date
                    }}</span>
                  </span>
                  <span class="text-xs text-gray-500"
                    >คืน:
                    <span class="font-bold text-[#a259ff]">{{
                      req.return_date
                    }}</span>
                  </span>
                </div>
              </td>

              <td class="p-4 align-top pt-4">
                <div class="flex flex-col items-center gap-2">
                  <!-- Custom Dropdown -->
                  <div class="relative w-full" ref="dropdownRefs">
                    <button
                      @click="toggleDropdown(req.id)"
                      :disabled="req.status === 'returned'"
                      class="w-full flex items-center justify-between gap-2 px-4 py-2.5 rounded-xl text-sm font-bold border outline-none transition-all shadow-sm"
                      :class="[
                        statusStyle(req.status).btn,
                        req.status === 'returned'
                          ? 'cursor-not-allowed opacity-80'
                          : 'cursor-pointer',
                      ]"
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
                        class="absolute z-50 mt-1 w-full bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden"
                      >
                        <button
                          v-for="opt in statusOptions"
                          :key="opt.value"
                          @click="selectStatus(opt.value, req)"
                          class="w-full flex items-center gap-2 px-4 py-2.5 text-sm font-bold text-left transition-colors"
                          :class="[
                            opt.hover,
                            req.status === opt.value
                              ? opt.active
                              : 'text-gray-700',
                          ]"
                        >
                          <span>{{ opt.label }}</span>
                          <CheckIcon
                            v-if="req.status === opt.value"
                            class="w-4 h-4 ml-auto"
                          />
                        </button>
                      </div>
                    </Transition>
                  </div>

                  <p
                    v-if="req.status === 'returned'"
                    class="text-[10px] text-gray-400 font-bold italic"
                  >
                    เสร็จสิ้นรายการ
                  </p>

                  <!-- Delete Button -->
                  <button
                    @click="handleDelete(req)"
                    class="w-full flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold text-red-500 border border-red-100 bg-red-50 hover:bg-red-100 hover:border-red-200 transition-colors cursor-pointer"
                  >
                    <TrashIcon class="w-3.5 h-3.5" />
                    ลบรายการ
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="borrowRequests.length === 0">
              <td colspan="3" class="p-10 text-center text-gray-500">
                ยังไม่มีรายการขอยืมอุปกรณ์ในขณะนี้
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import {
  ClipboardDocumentListIcon,
  ChevronDownIcon,
  CheckIcon,
  TrashIcon,
} from "@heroicons/vue/24/solid";
import { useAlert } from "../../composables/useAlert";

const { showAlert, showConfirm } = useAlert();

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
    const csrfRes = await fetch("/api/csrf-token", {
      method: "GET",
      credentials: "include",
    });
    const { csrf_token } = await csrfRes.json();

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
    const csrfRes = await fetch("/api/csrf-token", {
      method: "GET",
      credentials: "include",
    });
    const { csrf_token } = await csrfRes.json();

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
