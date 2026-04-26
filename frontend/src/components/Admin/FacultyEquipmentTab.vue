<template>
  <div class="animate-fade-in">
    <div
      class="flex flex-col md:flex-row justify-between items-start md:items-end mb-6 gap-4"
    >
      <div>
        <h3
          class="text-2xl md:text-3xl font-black text-dark mb-1 flex items-center gap-2"
        >
          <BuildingLibraryIcon class="w-7 h-7 md:w-8 md:h-8 text-[#43b89c]" />
          จัดการครุภัณฑ์ประจำคณะ
        </h3>
        <p class="text-gray-500 text-sm">
          ดูรายการ เพิ่ม แก้ไข หรือลบครุภัณฑ์ของแต่ละคณะ
        </p>
      </div>
      <button
        @click="openModal('add')"
        class="w-full md:w-auto px-6 py-3 bg-gray-900 hover:bg-black text-white font-bold rounded-xl transition-all shadow-md flex items-center justify-center gap-2"
      >
        <PlusIcon class="w-5 h-5" />
        เพิ่มครุภัณฑ์ใหม่
      </button>
    </div>

    <!-- Faculty filter: mobile select -->
    <div class="sm:hidden mb-5">
      <select
        v-model="selectedFacultyFilter"
        class="w-full px-4 py-2.5 rounded-xl bg-white border border-gray-200 text-sm font-bold text-gray-700 outline-none focus:ring-2 focus:ring-[#43b89c]/40 focus:border-[#43b89c] transition-all"
      >
        <option value="">ทั้งหมด ({{ items.length }})</option>
        <option v-for="f in FACULTIES" :key="f.id" :value="f.id">
          {{ f.id }} · {{ f.shortName }}{{ countByFaculty[f.id] ? ` (${countByFaculty[f.id]})` : '' }}
        </option>
      </select>
    </div>

    <!-- Faculty filter: desktop buttons -->
    <div class="hidden sm:flex flex-wrap gap-2 mb-5">
      <button
        @click="selectedFacultyFilter = ''"
        :class="
          selectedFacultyFilter === ''
            ? 'bg-gray-900 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
        "
        class="px-3 py-1.5 rounded-xl text-xs font-bold transition-all"
      >
        ทั้งหมด ({{ items.length }})
      </button>
      <button
        v-for="f in FACULTIES"
        :key="f.id"
        @click="selectedFacultyFilter = f.id"
        :class="
          selectedFacultyFilter === f.id
            ? 'text-white'
            : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
        "
        class="px-3 py-1.5 rounded-xl text-xs font-bold transition-all"
        :style="
          selectedFacultyFilter === f.id
            ? `background-color: ${f.color}; color: ${f.textColor}`
            : ''
        "
      >
        {{ f.id }} · {{ f.shortName }}
        <span v-if="countByFaculty[f.id]" class="ml-1 opacity-70"
          >({{ countByFaculty[f.id] }})</span
        >
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-20 text-gray-400">
      <div class="inline-flex flex-col items-center gap-3">
        <div
          class="w-8 h-8 border-4 border-[#43b89c]/30 border-t-[#43b89c] rounded-full animate-spin"
        />
        <span class="text-sm font-medium">กำลังโหลดข้อมูล...</span>
      </div>
    </div>

    <div
      v-else-if="filteredItems.length === 0"
      class="text-center py-20 text-gray-400"
    >
      <BuildingLibraryIcon class="w-12 h-12 mx-auto mb-3 opacity-30" />
      <p class="font-medium">ยังไม่มีครุภัณฑ์ในหมวดนี้</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <div
        v-for="item in filteredItems"
        :key="item.id"
        class="glass rounded-3xl overflow-hidden flex flex-col group hover:-translate-y-0.5 transition-all duration-200 shadow-sm hover:shadow-md"
      >
        <div class="relative h-40 bg-gray-100 overflow-hidden">
          <img
            v-if="item.image_url"
            :src="item.image_url"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            alt=""
          />
          <div v-else class="w-full h-full flex items-center justify-center">
            <BuildingLibraryIcon class="w-10 h-10 text-gray-300" />
          </div>

          <div
            class="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-black shadow-sm backdrop-blur-sm"
            :class="
              item.available_quantity > 0
                ? 'bg-green-500/90 text-white'
                : 'bg-red-500/90 text-white'
            "
          >
            {{
              item.available_quantity > 0
                ? `เหลือ ${item.available_quantity}`
                : "หมด"
            }}
          </div>

          <div
            class="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-bold shadow-sm backdrop-blur-sm text-white"
            :style="`background-color: ${facultyColor(item.faculty_id)}`"
          >
            {{ item.faculty_id }} · {{ facultyShortName(item.faculty_id) }}
          </div>
        </div>

        <div class="p-4 flex-1 flex flex-col gap-3">
          <div class="flex-1">
            <h4
              class="font-black text-gray-900 text-base leading-tight line-clamp-1"
            >
              {{ item.name }}
            </h4>
            <p class="text-xs text-gray-400 mt-1 line-clamp-2 leading-relaxed">
              {{ item.description || "ไม่มีรายละเอียด" }}
            </p>
          </div>

          <div>
            <div
              class="flex justify-between text-xs font-bold text-gray-500 mb-1"
            >
              <span>สต็อก</span>
              <span>
                <span
                  :class="
                    item.available_quantity > 0
                      ? 'text-green-600'
                      : 'text-red-500'
                  "
                >
                  {{ item.available_quantity }}
                </span>
                <span class="text-gray-400"> / {{ item.total_quantity }}</span>
              </span>
            </div>
            <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-500"
                :class="
                  item.available_quantity > 0 ? 'bg-green-400' : 'bg-red-400'
                "
                :style="`width: ${(item.available_quantity / item.total_quantity) * 100}%`"
              />
            </div>
          </div>

          <div class="flex gap-2">
            <button
              @click="openModal('edit', item)"
              class="flex-1 flex items-center justify-center gap-1.5 py-2 text-xs font-bold rounded-xl bg-yellow-50 text-yellow-600 hover:bg-yellow-500 hover:text-white transition-colors border border-yellow-100 hover:border-yellow-500"
            >
              <PencilIcon class="w-3.5 h-3.5" /> แก้ไข
            </button>
            <button
              @click="deleteItem(item.id)"
              class="flex-1 flex items-center justify-center gap-1.5 py-2 text-xs font-bold rounded-xl bg-red-50 text-red-500 hover:bg-red-500 hover:text-white transition-colors border border-red-100 hover:border-red-500"
            >
              <TrashIcon class="w-3.5 h-3.5" /> ลบ
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
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
                {{
                  isEditing ? "แก้ไขครุภัณฑ์ประจำคณะ" : "เพิ่มครุภัณฑ์ประจำคณะ"
                }}
              </h3>
              <p class="text-gray-400 text-sm mb-6">กรอกรายละเอียดอุปกรณ์</p>

              <form @submit.prevent="submitItem" class="space-y-4">
                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700">
                    คณะ <span class="text-red-500">*</span>
                  </label>
                  <select
                    v-model="form.faculty_id"
                    required
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#43b89c]/40 focus:border-[#43b89c] transition-all"
                  >
                    <option value="" disabled>เลือกคณะ</option>
                    <option v-for="f in FACULTIES" :key="f.id" :value="f.id">
                      {{ f.id }} · {{ f.nameTh }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700">
                    ชื่ออุปกรณ์ <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.name"
                    type="text"
                    required
                    placeholder="เช่น โปรเจกเตอร์, ไมโครโฟน"
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#43b89c]/40 focus:border-[#43b89c] transition-all"
                  />
                </div>

                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700"
                    >จำนวนทั้งหมด <span class="text-red-500">*</span></label
                  >
                  <input
                    v-model="form.total_quantity"
                    type="number"
                    min="1"
                    required
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#43b89c]/40 focus:border-[#43b89c] transition-all"
                  />
                </div>

                <div>
                  <label class="block text-sm font-bold mb-1.5 text-gray-700"
                    >รายละเอียด</label
                  >
                  <textarea
                    v-model="form.description"
                    rows="2"
                    placeholder="อธิบายอุปกรณ์โดยย่อ..."
                    class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border border-gray-200 outline-none focus:ring-2 focus:ring-[#43b89c]/40 focus:border-[#43b89c] transition-all resize-none"
                  />
                </div>

                <div class="p-4 bg-gray-50 border border-gray-200 rounded-2xl">
                  <label class="block text-sm font-bold mb-2 text-gray-700"
                    >รูปภาพอุปกรณ์</label
                  >
                  <div
                    class="flex flex-col sm:flex-row items-start sm:items-center gap-3"
                  >
                    <label
                      class="cursor-pointer px-4 py-2 bg-[#43b89c] hover:bg-[#2e9e84] text-white text-sm font-bold rounded-xl transition-colors flex items-center gap-2"
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
                    <span
                      v-if="isUploading"
                      class="text-xs text-blue-500 animate-pulse font-bold"
                      >กำลังอัปโหลด...</span
                    >
                    <span
                      v-else-if="form.image_url"
                      class="text-xs text-green-600 font-bold"
                      >✓ อัปโหลดสำเร็จ</span
                    >
                  </div>
                  <img
                    v-if="form.image_url"
                    :src="form.image_url"
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
                    {{
                      isSubmitting
                        ? "กำลังบันทึก..."
                        : isEditing
                          ? "บันทึกการแก้ไข"
                          : "เพิ่มครุภัณฑ์"
                    }}
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
import { ref, reactive, computed, onMounted } from "vue";
import {
  BuildingLibraryIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  XMarkIcon,
  PhotoIcon,
} from "@heroicons/vue/24/solid";
import { useAlert } from "../../composables/useAlert";
import { useCsrf } from "../../composables/useCsrf";

const { showAlert, showConfirm } = useAlert();
const { getCsrfToken } = useCsrf();

const FACULTIES = [
  {
    id: "01",
    nameTh: "คณะมนุษยศาสตร์",
    shortName: "มนุษยศาสตร์",
    color: "#d1d5db",
    textColor: "#374151",
  },
  {
    id: "02",
    nameTh: "คณะศึกษาศาสตร์",
    shortName: "ศึกษาศาสตร์",
    color: "#43C7F4",
    textColor: "#ffffff",
  },
  {
    id: "03",
    nameTh: "คณะวิจิตรศิลป์",
    shortName: "วิจิตรศิลป์",
    color: "#E41E26",
    textColor: "#ffffff",
  },
  {
    id: "04",
    nameTh: "คณะสังคมศาสตร์",
    shortName: "สังคมศาสตร์",
    color: "#4BA2DB",
    textColor: "#ffffff",
  },
  {
    id: "05",
    nameTh: "คณะวิทยาศาสตร์",
    shortName: "วิทยาศาสตร์",
    color: "#FACB21",
    textColor: "#374151",
  },
  {
    id: "06",
    nameTh: "คณะวิศวกรรมศาสตร์",
    shortName: "วิศวกรรมศาสตร์",
    color: "#5B171E",
    textColor: "#ffffff",
  },
  {
    id: "07",
    nameTh: "คณะแพทยศาสตร์",
    shortName: "แพทยศาสตร์",
    color: "#007832",
    textColor: "#ffffff",
  },
  {
    id: "08",
    nameTh: "คณะเกษตรศาสตร์",
    shortName: "เกษตรศาสตร์",
    color: "#FAA61A",
    textColor: "#374151",
  },
  {
    id: "09",
    nameTh: "คณะทันตแพทยศาสตร์",
    shortName: "ทันตแพทยศาสตร์",
    color: "#6D2C90",
    textColor: "#ffffff",
  },
  {
    id: "10",
    nameTh: "คณะเภสัชศาสตร์",
    shortName: "เภสัชศาสตร์",
    color: "#5C990E",
    textColor: "#ffffff",
  },
  {
    id: "11",
    nameTh: "คณะเทคนิคการแพทย์",
    shortName: "เทคนิคการแพทย์",
    color: "#28487F",
    textColor: "#ffffff",
  },
  {
    id: "12",
    nameTh: "คณะพยาบาลศาสตร์",
    shortName: "พยาบาลศาสตร์",
    color: "#F16422",
    textColor: "#ffffff",
  },
  {
    id: "13",
    nameTh: "คณะอุตสาหกรรมเกษตร",
    shortName: "อุตสาหกรรมเกษตร",
    color: "#CC9933",
    textColor: "#ffffff",
  },
  {
    id: "14",
    nameTh: "คณะสัตวแพทยศาสตร์",
    shortName: "สัตวแพทยศาสตร์",
    color: "#5EAFD2",
    textColor: "#ffffff",
  },
  {
    id: "15",
    nameTh: "คณะบริหารธุรกิจ",
    shortName: "บริหารธุรกิจ",
    color: "#008EAA",
    textColor: "#ffffff",
  },
  {
    id: "16",
    nameTh: "คณะเศรษฐศาสตร์",
    shortName: "เศรษฐศาสตร์",
    color: "#ED4081",
    textColor: "#ffffff",
  },
  {
    id: "17",
    nameTh: "คณะสถาปัตยกรรมศาสตร์",
    shortName: "สถาปัตยกรรมศาสตร์",
    color: "#FFEE4C",
    textColor: "#374151",
  },
  {
    id: "18",
    nameTh: "คณะการสื่อสารมวลชน",
    shortName: "สื่อสารมวลชน",
    color: "#838383",
    textColor: "#ffffff",
  },
  {
    id: "19",
    nameTh: "คณะรัฐศาสตร์และรัฐประศาสนศาสตร์",
    shortName: "รัฐศาสตร์ฯ",
    color: "#173C6E",
    textColor: "#ffffff",
  },
  {
    id: "20",
    nameTh: "คณะนิติศาสตร์",
    shortName: "นิติศาสตร์",
    color: "#B2A4D4",
    textColor: "#ffffff",
  },
  {
    id: "21",
    nameTh: "วิทยาลัยศิลปะ สื่อ และเทคโนโลยี",
    shortName: "CAMT",
    color: "#AC6B4D",
    textColor: "#ffffff",
  },
  {
    id: "22",
    nameTh: "วิทยาลัยนานาชาตินวัตกรรมดิจิทัล",
    shortName: "ICIT",
    color: "#012169",
    textColor: "#ffffff",
  },
];

const facultyMap = Object.fromEntries(FACULTIES.map((f) => [f.id, f]));
const facultyColor = (id) => facultyMap[id]?.color ?? "#a259ff";
const facultyShortName = (id) => facultyMap[id]?.shortName ?? id;

const items = ref([]);
const isLoading = ref(false);
const isSubmitting = ref(false);
const isUploading = ref(false);
const isModalOpen = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const selectedFacultyFilter = ref("");

const countByFaculty = computed(() => {
  const map = {};
  for (const item of items.value) {
    map[item.faculty_id] = (map[item.faculty_id] || 0) + 1;
  }
  return map;
});

const filteredItems = computed(() =>
  selectedFacultyFilter.value
    ? items.value.filter((i) => i.faculty_id === selectedFacultyFilter.value)
    : items.value,
);

const form = reactive({
  faculty_id: "",
  name: "",
  description: "",
  image_url: "",
  total_quantity: 1,
});

const fetchItems = async () => {
  isLoading.value = true;
  try {
    const res = await fetch("/api/admin/faculty-equipment", {
      credentials: "include",
    });
    const json = await res.json();
    if (json.status === "success") items.value = json.data;
  } catch (e) {
    console.error(e);
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchItems);

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
      form.image_url = data.url;
    } else {
      await showAlert("อัปโหลดรูปภาพไม่สำเร็จ", "error");
    }
  } catch (e) {
    await showAlert("เกิดข้อผิดพลาดในการเชื่อมต่อ", "error");
  } finally {
    isUploading.value = false;
  }
};

const openModal = (mode, item = null) => {
  if (mode === "edit" && item) {
    isEditing.value = true;
    editingId.value = item.id;
    Object.assign(form, {
      faculty_id: item.faculty_id,
      name: item.name,
      description: item.description || "",
      image_url: item.image_url || "",
      total_quantity: item.total_quantity,
    });
  } else {
    isEditing.value = false;
    editingId.value = null;
    resetForm();
  }
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const resetForm = () => {
  form.faculty_id = selectedFacultyFilter.value || "";
  form.name = "";
  form.description = "";
  form.image_url = "";
  form.total_quantity = 1;
};

const submitItem = async () => {
  isSubmitting.value = true;
  try {
    const token = await getCsrfToken();
    const url = isEditing.value
      ? `/api/admin/faculty-equipment/${editingId.value}`
      : "/api/admin/faculty-equipment";
    const res = await fetch(url, {
      method: isEditing.value ? "PUT" : "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": token },
      credentials: "include",
      body: JSON.stringify(form),
    });
    const data = await res.json();
    if (res.ok) {
      await showAlert(data.message || "บันทึกเรียบร้อย", "success");
      closeModal();
      fetchItems();
    } else {
      await showAlert(data.detail || "เกิดข้อผิดพลาด", "error");
    }
  } catch (e) {
    await showAlert("เกิดข้อผิดพลาดในการเชื่อมต่อ", "error");
  } finally {
    isSubmitting.value = false;
  }
};

const deleteItem = async (id) => {
  if (!(await showConfirm("ลบครุภัณฑ์ชิ้นนี้?"))) return;
  try {
    const token = await getCsrfToken();
    const res = await fetch(`/api/admin/faculty-equipment/${id}`, {
      method: "DELETE",
      headers: { "X-CSRF-Token": token },
      credentials: "include",
    });
    const data = await res.json();
    if (res.ok) {
      await showAlert(data.message || "ลบเรียบร้อย", "success");
      fetchItems();
    } else {
      await showAlert(data.detail || "เกิดข้อผิดพลาด", "error");
    }
  } catch (e) {
    console.error(e);
  }
};
</script>
