<template>
  <div class="animate-fade-in">
    <div
      class="flex flex-col md:flex-row justify-between items-start md:items-end mb-6 gap-4"
    >
      <div>
        <h3
          class="text-2xl md:text-3xl font-black text-dark mb-1 flex items-center gap-2"
        >
          <ArchiveBoxIcon class="w-7 h-7 md:w-8 md:h-8 text-[#a259ff]" />
          จัดการครุภัณฑ์
        </h3>
        <p class="text-gray-500 text-sm">ดูรายการ ลบ หรือแก้ไขอุปกรณ์ในระบบ</p>
      </div>
      <button
        @click="openModal('add')"
        class="w-full md:w-auto px-6 py-3 bg-gray-900 hover:bg-black text-white font-bold rounded-xl transition-all shadow-md flex items-center justify-center gap-2"
      >
        <span>+</span> เพิ่มครุภัณฑ์ใหม่
      </button>
    </div>

    <div v-if="isLoadingEq" class="text-center py-10 text-gray-500">
      กำลังโหลดข้อมูล...
    </div>

    <div v-else class="glass rounded-3xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-[600px]">
          <thead>
            <tr class="bg-white/40 border-b border-gray-200">
              <th class="p-4 font-bold text-sm text-gray-600">รูปภาพ</th>
              <th class="p-4 font-bold text-sm text-gray-600">ชื่ออุปกรณ์</th>
              <th class="p-4 font-bold text-sm text-gray-600 text-center">
                คงเหลือ / ทั้งหมด
              </th>
              <th class="p-4 font-bold text-sm text-gray-600 text-center">
                จัดการ
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="eq in equipments"
              :key="eq.id"
              class="border-b border-gray-100 last:border-0 hover:bg-white/60"
            >
              <td class="p-4">
                <img
                  :src="eq.image_url"
                  class="w-14 h-14 object-cover rounded-xl shadow-sm"
                />
              </td>
              <td class="p-4 font-bold text-gray-800">{{ eq.name }}</td>
              <td class="p-4 text-center font-bold">
                <span
                  :class="
                    eq.available_quantity > 0
                      ? 'text-green-600'
                      : 'text-red-500'
                  "
                  >{{ eq.available_quantity }}</span
                >
                <span class="text-gray-400"> / {{ eq.total_quantity }}</span>
              </td>
              <td class="p-4 text-center">
                <div class="flex items-center justify-center gap-2">
                  <button
                    @click="openModal('edit', eq)"
                    class="p-2 bg-yellow-50 text-yellow-500 hover:bg-yellow-500 hover:text-white rounded-lg transition-colors"
                  >
                    <PencilIcon class="w-5 h-5" />
                  </button>
                  <button
                    @click="deleteEquipment(eq.id)"
                    class="p-2 bg-red-50 text-red-500 hover:bg-red-500 hover:text-white rounded-lg transition-colors"
                  >
                    <TrashIcon class="w-5 h-5" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="isModalOpen"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      >
        <div
          class="bg-white w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-3xl p-6 md:p-8 relative shadow-2xl"
        >
          <button
            @click="closeModal"
            class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 bg-gray-100 p-2 rounded-full"
          >
            <XMarkIcon class="w-5 h-5" />
          </button>

          <h3 class="text-2xl font-black mb-1">
            {{ isEditingEq ? "✏️ แก้ไขข้อมูล" : "📦 เพิ่มครุภัณฑ์ใหม่" }}
          </h3>
          <p class="text-gray-500 text-sm mb-6">
            กรอกรายละเอียดอุปกรณ์เพื่อนำเข้าสู่ระบบ
          </p>

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
                  class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border outline-none focus:ring-2 focus:ring-[#a259ff]"
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
                  class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border outline-none focus:ring-2 focus:ring-[#a259ff]"
                />
              </div>
            </div>

            <div class="p-4 bg-gray-50 border rounded-2xl">
              <label class="block text-sm font-bold mb-2"
                >อัปโหลดรูปภาพอุปกรณ์</label
              >
              <div
                class="flex flex-col md:flex-row items-start md:items-center gap-4"
              >
                <input
                  type="file"
                  @change="uploadImage"
                  accept="image/*"
                  class="text-sm file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-[#a259ff] file:text-white"
                />
                <span
                  v-if="isUploading"
                  class="text-xs text-blue-500 animate-pulse font-bold"
                  >กำลังอัปโหลด...</span
                >
              </div>
              <img
                v-if="formEq.image_url"
                :src="formEq.image_url"
                class="mt-4 max-h-32 rounded-lg object-contain shadow-sm mx-auto"
              />
            </div>

            <div class="pt-4 flex gap-3">
              <button
                type="button"
                @click="closeModal"
                class="flex-1 py-3 bg-gray-100 font-bold rounded-xl"
              >
                ยกเลิก
              </button>
              <button
                type="submit"
                :disabled="isSubmitting || isUploading"
                class="flex-1 py-3 text-white font-bold rounded-xl bg-gray-900"
              >
                {{ isSubmitting ? "กำลังบันทึก..." : "ยืนยันข้อมูล" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import {
  ArchiveBoxIcon,
  TrashIcon,
  PencilIcon,
  XMarkIcon,
} from "@heroicons/vue/24/solid";

const equipments = ref([]);
const isLoadingEq = ref(false);
const isSubmitting = ref(false);
const isUploading = ref(false);
const isModalOpen = ref(false);
const isEditingEq = ref(false);
const editingEqId = ref(null);

const formEq = reactive({
  name: "",
  category: "ส่วนกลาง",
  description: "",
  image_url: "",
  total_quantity: 1,
});

const getCsrfToken = async () => {
  const res = await fetch("/api/csrf-token", {
    method: "GET",
    credentials: "include",
  });
  const data = await res.json();
  return data.csrf_token;
};

const fetchEquipments = async () => {
  isLoadingEq.value = true;
  try {
    const res = await fetch("/api/admin/equipment", { credentials: "include" });
    const json = await res.json();
    if (json.status === "success") equipments.value = json.data;
  } catch (e) {
    console.error(e);
  } finally {
    isLoadingEq.value = false;
  }
};

onMounted(fetchEquipments);

const uploadImage = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  isUploading.value = true;
  const formData = new FormData();
  formData.append("file", file);
  try {
    const token = await getCsrfToken();
    const res = await fetch("/api/admin/upload", {
      method: "POST",
      headers: { "X-CSR-Token": token },
      credentials: "include",
      body: formData,
    });
    const data = await res.json();
    if (res.ok && data.url) formEq.image_url = data.url;
  } catch (e) {
    console.error(e);
  } finally {
    isUploading.value = false;
  }
};

const openModal = (mode, eq = null) => {
  isModalOpen.value = true;
  if (mode === "edit") {
    isEditingEq.value = true;
    editingEqId.value = eq.id;
    Object.assign(formEq, eq);
  } else {
    isEditingEq.value = false;
    resetForm();
  }
};

const closeModal = () => {
  isModalOpen.value = false;
};
const resetForm = () => {
  Object.keys(formEq).forEach(
    (k) => (formEq[k] = k === "total_quantity" ? 1 : ""),
  );
  formEq.category = "ส่วนกลาง";
};

const submitEquipment = async () => {
  isSubmitting.value = true;
  try {
    const token = await getCsrfToken();
    const url = isEditingEq.value
      ? `/api/admin/equipment/${editingEqId.value}`
      : "/api/admin/equipment";
    const method = isEditingEq.value ? "PUT" : "POST";
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", "X-CSRF-Token": token },
      credentials: "include",
      body: JSON.stringify(formEq),
    });
    if (res.ok) {
      closeModal();
      fetchEquipments();
    }
  } catch (e) {
    console.error(e);
  } finally {
    isSubmitting.value = false;
  }
};

const deleteEquipment = async (id) => {
  if (!confirm("ลบอุปกรณ์ชิ้นนี้?")) return;
  try {
    const token = await getCsrfToken();
    await fetch(`/api/admin/equipment/${id}`, {
      method: "DELETE",
      headers: { "X-CSRF-Token": token },
      credentials: "include",
    });
    fetchEquipments();
  } catch (e) {
    console.error(e);
  }
};
</script>
