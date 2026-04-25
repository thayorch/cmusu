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
        <PlusIcon class="w-5 h-5" />
        เพิ่มครุภัณฑ์ใหม่
      </button>
    </div>

    <div v-if="isLoadingEq" class="text-center py-20 text-gray-400">
      <div class="inline-flex flex-col items-center gap-3">
        <div class="w-8 h-8 border-4 border-[#a259ff]/30 border-t-[#a259ff] rounded-full animate-spin" />
        <span class="text-sm font-medium">กำลังโหลดข้อมูล...</span>
      </div>
    </div>

    <div v-else-if="equipments.length === 0" class="text-center py-20 text-gray-400">
      <ArchiveBoxIcon class="w-12 h-12 mx-auto mb-3 opacity-30" />
      <p class="font-medium">ยังไม่มีครุภัณฑ์ในระบบ</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <div
        v-for="eq in equipments"
        :key="eq.id"
        class="glass rounded-3xl overflow-hidden flex flex-col group hover:-translate-y-0.5 transition-all duration-200 shadow-sm hover:shadow-md"
      >
        <!-- Image -->
        <div class="relative h-44 bg-gray-100 overflow-hidden">
          <img
            v-if="eq.image_url"
            :src="eq.image_url"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            alt=""
          />
          <div v-else class="w-full h-full flex items-center justify-center">
            <ArchiveBoxIcon class="w-10 h-10 text-gray-300" />
          </div>

          <!-- Stock Badge -->
          <div
            class="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-black shadow-sm backdrop-blur-sm"
            :class="
              eq.available_quantity > 0
                ? 'bg-green-500/90 text-white'
                : 'bg-red-500/90 text-white'
            "
          >
            {{ eq.available_quantity > 0 ? `เหลือ ${eq.available_quantity}` : "หมด" }}
          </div>

          <!-- Category Badge -->
          <div
            class="absolute top-3 left-3 px-3 py-1 bg-white/85 backdrop-blur-sm rounded-full text-xs font-bold text-gray-600 shadow-sm"
          >
            {{ eq.category }}
          </div>
        </div>

        <!-- Content -->
        <div class="p-4 flex-1 flex flex-col gap-3">
          <div class="flex-1">
            <h4 class="font-black text-gray-900 text-base leading-tight line-clamp-1">
              {{ eq.name }}
            </h4>
            <p class="text-xs text-gray-400 mt-1 line-clamp-2 leading-relaxed">
              {{ eq.description || "ไม่มีรายละเอียด" }}
            </p>
          </div>

          <!-- Stock Bar -->
          <div>
            <div class="flex justify-between text-xs font-bold text-gray-500 mb-1">
              <span>สต็อก</span>
              <span>
                <span :class="eq.available_quantity > 0 ? 'text-green-600' : 'text-red-500'">
                  {{ eq.available_quantity }}
                </span>
                <span class="text-gray-400"> / {{ eq.total_quantity }}</span>
              </span>
            </div>
            <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-500"
                :class="eq.available_quantity > 0 ? 'bg-green-400' : 'bg-red-400'"
                :style="`width: ${(eq.available_quantity / eq.total_quantity) * 100}%`"
              />
            </div>
          </div>

          <!-- Actions -->
          <div class="flex gap-2">
            <button
              @click="openModal('edit', eq)"
              class="flex-1 flex items-center justify-center gap-1.5 py-2 text-xs font-bold rounded-xl bg-yellow-50 text-yellow-600 hover:bg-yellow-500 hover:text-white transition-colors border border-yellow-100 hover:border-yellow-500"
            >
              <PencilIcon class="w-3.5 h-3.5" />
              แก้ไข
            </button>
            <button
              @click="deleteEquipment(eq.id)"
              class="flex-1 flex items-center justify-center gap-1.5 py-2 text-xs font-bold rounded-xl bg-red-50 text-red-500 hover:bg-red-500 hover:text-white transition-colors border border-red-100 hover:border-red-500"
            >
              <TrashIcon class="w-3.5 h-3.5" />
              ลบ
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add / Edit Modal -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isModalOpen"
          class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
          @mousedown.self="closeModal"
        >
          <Transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0 scale-95 translate-y-2"
            enter-to-class="opacity-100 scale-100 translate-y-0"
            appear
          >
            <div
              v-if="isModalOpen"
              class="bg-white w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-3xl p-6 md:p-8 relative shadow-2xl"
            >
              <button
                @click="closeModal"
                class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 bg-gray-100 hover:bg-gray-200 p-2 rounded-full transition-colors"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>

              <h3 class="text-xl font-black mb-0.5">
                {{ isEditingEq ? "แก้ไขข้อมูลครุภัณฑ์" : "เพิ่มครุภัณฑ์ใหม่" }}
              </h3>
              <p class="text-gray-400 text-sm mb-6">
                กรอกรายละเอียดอุปกรณ์เพื่อนำเข้าสู่ระบบ
              </p>

              <form @submit.prevent="submitEquipment" class="space-y-4">
                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700">
                    ชื่ออุปกรณ์ <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="formEq.name"
                    type="text"
                    required
                    placeholder="เช่น ไมโครโฟน, โปรเจกเตอร์"
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#a259ff]/40 focus:border-[#a259ff] transition-all"
                  />
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">
                      จำนวนทั้งหมด <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="formEq.total_quantity"
                      type="number"
                      min="1"
                      required
                      class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#a259ff]/40 focus:border-[#a259ff] transition-all"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-bold mb-1.5 text-gray-700">
                      หมวดหมู่
                    </label>
                    <input
                      v-model="formEq.category"
                      type="text"
                      class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#a259ff]/40 focus:border-[#a259ff] transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700">
                    รายละเอียด
                  </label>
                  <textarea
                    v-model="formEq.description"
                    rows="2"
                    placeholder="อธิบายอุปกรณ์โดยย่อ..."
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#a259ff]/40 focus:border-[#a259ff] transition-all resize-none"
                  />
                </div>

                <div class="p-4 bg-gray-50 border border-gray-200 rounded-2xl">
                  <label class="block text-sm font-bold mb-2 text-gray-700">
                    รูปภาพอุปกรณ์
                  </label>
                  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3">
                    <label
                      class="cursor-pointer px-4 py-2 bg-[#a259ff] hover:bg-[#8b3dff] text-white text-sm font-bold rounded-xl transition-colors flex items-center gap-2"
                    >
                      <PhotoIcon class="w-4 h-4" />
                      เลือกไฟล์
                      <input
                        type="file"
                        @change="uploadImage"
                        accept="image/*"
                        class="hidden"
                      />
                    </label>
                    
                    <span v-if="isUploading" class="text-xs text-blue-500 animate-pulse font-bold">
                      กำลังอัปโหลด...
                    </span>
                    <span v-else-if="formEq.image_url" class="text-xs text-green-600 font-bold">
                      ✓ อัปโหลดสำเร็จ
                    </span>
                  </div>
                  <img
                    v-if="formEq.image_url"
                    :src="formEq.image_url"
                    class="mt-3 h-28 w-full object-cover rounded-xl shadow-sm"
                  />
                </div>

                <div class="flex gap-3 pt-2">
                  <button
                    type="button"
                    @click="closeModal"
                    class="flex-1 py-3 bg-gray-100 hover:bg-gray-200 font-bold rounded-xl transition-colors text-gray-700"
                  >
                    ยกเลิก
                  </button>
                  <button
                    type="submit"
                    :disabled="isSubmitting || isUploading"
                    class="flex-1 py-3 text-white font-bold rounded-xl bg-gray-900 hover:bg-black transition-colors disabled:opacity-50"
                  >
                    {{ isSubmitting ? "กำลังบันทึก..." : isEditingEq ? "บันทึกการแก้ไข" : "เพิ่มครุภัณฑ์" }}
                  </button>
                </div>
              </form>
            </div>
          </Transition>
        </div>
      </Transition>
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
  PlusIcon,
  PhotoIcon,
} from "@heroicons/vue/24/solid";
import { useAlert } from "../../composables/useAlert";
import { useCsrf } from "../../composables/useCsrf";

const { showAlert, showConfirm } = useAlert();
const { getCsrfToken } = useCsrf();

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
      headers: { "X-CSRF-Token": token },
      credentials: "include",
      body: formData,
    });
    const data = await res.json();
    if (res.ok && data.url) {
      formEq.image_url = data.url;
    } else {
      await showAlert("อัปโหลดรูปภาพไม่สำเร็จ: " + (data.detail || "โปรดลองอีกครั้ง"), "error");
    }
  } catch (e) {
    console.error(e);
    await showAlert("เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์", "error");
  } finally {
    isUploading.value = false;
  }
};

const openModal = (mode, eq = null) => {
  if (mode === "edit") {
    isEditingEq.value = true;
    editingEqId.value = eq.id;
    Object.assign(formEq, eq);
  } else {
    isEditingEq.value = false;
    resetForm();
  }
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const resetForm = () => {
  Object.keys(formEq).forEach((k) => (formEq[k] = k === "total_quantity" ? 1 : ""));
  formEq.category = "ส่วนกลาง";
};

const submitEquipment = async () => {
  isSubmitting.value = true;
  try {
    const token = await getCsrfToken();
    const url = isEditingEq.value
      ? `/api/admin/equipment/${editingEqId.value}`
      : "/api/admin/equipment";
    const res = await fetch(url, {
      method: isEditingEq.value ? "PUT" : "POST",
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
  if (!(await showConfirm("ลบอุปกรณ์ชิ้นนี้?"))) return;
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
