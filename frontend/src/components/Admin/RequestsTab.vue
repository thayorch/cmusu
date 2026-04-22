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
              <th class="p-4 font-bold text-sm text-gray-600 w-48 text-center">
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

              <td class="p-4 align-top pt-4 text-center">
                <select
                  :value="req.status"
                  @change="handleStatusChange($event, req)"
                  :disabled="req.status === 'returned'"
                  class="px-4 py-2.5 rounded-xl text-sm font-bold border outline-none cursor-pointer shadow-sm transition-colors w-full text-center appearance-none"
                  :class="{
                    'bg-yellow-50 text-yellow-700 border-yellow-200 hover:bg-yellow-100':
                      req.status === 'pending',
                    'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100':
                      req.status === 'approved',
                    'bg-green-50 text-green-700 border-green-200 cursor-not-allowed opacity-80':
                      req.status === 'returned',
                  }"
                >
                  <option value="pending" class="text-gray-800 bg-white">
                    ⏳ รออนุมัติ
                  </option>
                  <option value="approved" class="text-gray-800 bg-white">
                    🔄 กำลังยืม
                  </option>
                  <option value="returned" class="text-gray-800 bg-white">
                    ✅ คืนแล้ว
                  </option>
                </select>
                <p
                  v-if="req.status === 'returned'"
                  class="text-[10px] text-gray-400 mt-2 font-bold italic"
                >
                  เสร็จสิ้นรายการ
                </p>
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
import { ref, onMounted } from "vue";
import { ClipboardDocumentListIcon } from "@heroicons/vue/24/solid";

const borrowRequests = ref([]);

const fetchRequests = async () => {
  try {
    const res = await fetch("/api/admin/requests", { credentials: "include" });
    const json = await res.json();
    if (json.status === "success") borrowRequests.value = json.data;
  } catch (e) {
    console.error(e);
  }
};

onMounted(fetchRequests);

const handleStatusChange = async (event, req) => {
  const newStatus = event.target.value;
  const oldStatus = req.status;

  if (
    newStatus === "returned" &&
    !confirm("ยืนยันการรับคืนอุปกรณ์? สินค้าจะถูกบวกกลับเข้าคลังทันที")
  ) {
    event.target.value = oldStatus;
    return;
  }

  try {
    const csrfRes = await fetch("/api/csrf-token", {
      method: "GET",
      credentials: "include",
    });
    const csrfData = await csrfRes.json();

    const res = await fetch(`/api/admin/requests/status`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrfData.csrf_token,
      },
      credentials: "include",
      body: JSON.stringify({ id: req.id, status: newStatus }),
    });

    if (res.ok) {
      fetchRequests();
    } else {
      alert("เกิดข้อผิดพลาดในการอัปเดตสถานะ");
      event.target.value = oldStatus;
    }
  } catch (e) {
    console.error(e);
    event.target.value = oldStatus;
  }
};
</script>
