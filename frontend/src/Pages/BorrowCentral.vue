<template>
  <Navbar />
  <section class="relative z-10 max-w-6xl mx-auto px-6 py-10 animate-fade-in">
    <div class="text-center mb-12">
      <div
        class="glass inline-flex items-center gap-2 px-5 py-2 rounded-full mb-5"
      >
        <ArchiveBoxIcon class="w-4 h-4 text-[#a259ff]" />
        <span
          class="font-mono text-xs font-bold tracking-widest uppercase"
          style="color: #a259ff"
        >
          CMUSU Borrow
        </span>
      </div>
      <h2 class="font-black text-dark text-4xl md:text-5xl mb-4">
        ครุภัณฑ์ส่วนกลาง
      </h2>
      <p class="text-lg text-[#8b7bae]">ระบบแคตตาล็อกและตะกร้ายืมครุภัณฑ์</p>
    </div>

    <div v-if="isCheckingAuth" class="text-center py-20 text-[#8b7bae]">
      กำลังตรวจสอบสิทธิ์...
    </div>
    <div
      v-else-if="!user"
      class="glass max-w-md mx-auto p-10 text-center rounded-3xl mt-10 shadow-xl"
    >
      <div
        class="w-20 h-20 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-6"
      >
        <LockClosedIcon class="w-10 h-10 text-blue-500" />
      </div>
      <h3 class="text-2xl font-bold mb-3">กรุณาเข้าสู่ระบบ</h3>
      <p class="text-sm text-gray-500">
        สงวนสิทธิ์การยืมเฉพาะนักศึกษามหาวิทยาลัยเชียงใหม่
      </p>
      <p class="text-sm text-gray-500 mb-8">(Login with CMU Account)</p>
      <a
        href="/api/auth/login"
        class="w-full py-4 bg-white hover:bg-gray-50 text-gray-800 font-bold rounded-2xl shadow-sm border flex items-center justify-center gap-3"
      >
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"
          alt="Microsoft Logo"
          class="w-5 h-5"
        />
        เข้าสู่ระบบด้วย Microsoft
      </a>
    </div>

    <div v-else>
      <div
        class="flex justify-between items-center mb-8 glass p-4 rounded-2xl shadow-sm"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-10 h-10 bg-gradient-to-br from-[#a259ff] to-[#5bc8ff] text-white rounded-full flex items-center justify-center font-bold text-lg"
          >
            {{ user.email[0].toUpperCase() }}
          </div>
          <div>
            <p class="text-sm font-bold text-gray-800">{{ user.email }}</p>
            <button
              @click="logout"
              class="text-xs text-red-500 hover:text-red-700 font-medium"
            >
              ออกจากระบบ
            </button>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="text-center py-20 text-gray-500">
        กำลังโหลดแคตตาล็อก...
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="item in equipments"
          :key="item.id"
          class="glass rounded-3xl overflow-hidden flex flex-col group hover:-translate-y-1 transition-transform shadow-md"
        >
          <div class="h-48 overflow-hidden bg-gray-100 relative">
            <img
              :src="item.image_url"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <div
              class="absolute top-3 right-3 px-3 py-1 bg-white/90 backdrop-blur rounded-xl text-xs font-bold shadow-sm"
              :class="
                item.available_quantity > 0 ? 'text-green-600' : 'text-red-500'
              "
            >
              เหลือ {{ item.available_quantity }} / {{ item.total_quantity }}
            </div>
          </div>
          <div class="p-6 flex-1 flex flex-col">
            <h3 class="font-bold text-xl mb-2">{{ item.name }}</h3>
            <p class="text-sm text-gray-500 mb-6 flex-1 line-clamp-2">
              {{ item.description }}
            </p>

            <button
              @click="addToCart(item)"
              :disabled="item.available_quantity <= 0"
              class="w-full py-3 rounded-xl font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              :class="
                item.available_quantity > 0
                  ? 'bg-gradient-to-r from-[#a259ff] to-[#5bc8ff] text-white hover:opacity-90 shadow-md'
                  : 'bg-gray-200 text-gray-500'
              "
            >
              {{
                item.available_quantity > 0
                  ? "+ เพิ่มลงตะกร้า"
                  : "ของหมดชั่วคราว"
              }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <button
      v-if="user && cart.length > 0"
      @click="isCartOpen = true"
      class="fixed bottom-8 right-8 z-40 bg-gray-900 text-white p-4 rounded-full shadow-2xl hover:scale-110 transition-transform flex items-center gap-3 animate-fade-in"
    >
      <div class="relative">
        <ShoppingCartIcon class="w-7 h-7" />
        <span
          class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full"
          >{{ cart.length }}</span
        >
      </div>
      <span class="font-bold pr-2 hidden md:block">ดูตะกร้ายืม</span>
    </button>

    <div
      v-if="isCartOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in"
    >
      <div
        class="bg-white w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-3xl p-8 relative shadow-2xl"
      >
        <button
          @click="isCartOpen = false"
          class="absolute top-6 right-6 text-gray-400 hover:text-gray-600"
        >
          <XMarkIcon class="w-6 h-6" />
        </button>

        <h3 class="text-2xl font-bold mb-6 flex items-center gap-2">
          <ShoppingCartIcon class="w-6 h-6 text-[#a259ff]" /> ตะกร้ายืมครุภัณฑ์
        </h3>

        <div class="space-y-4 mb-8">
          <div
            v-for="(cartItem, index) in cart"
            :key="cartItem.equipment.id"
            class="flex items-center gap-4 bg-gray-50 p-3 rounded-2xl border"
          >
            <img
              :src="cartItem.equipment.image_url"
              class="w-16 h-16 object-cover rounded-xl"
            />
            <div class="flex-1">
              <h4 class="font-bold text-sm">{{ cartItem.equipment.name }}</h4>
              <p class="text-xs text-gray-500">
                เหลือ {{ cartItem.equipment.available_quantity }} ชิ้น
              </p>
            </div>

            <div
              class="flex items-center gap-2 bg-white border rounded-lg px-2 py-1"
            >
              <button
                @click="updateCartQty(index, -1)"
                class="w-6 h-6 flex items-center justify-center bg-gray-100 hover:bg-gray-200 rounded text-gray-700 font-bold"
              >
                -
              </button>
              <input
                v-model.number="cartItem.quantity"
                @change="validateCartQty(index)"
                type="number"
                class="w-10 text-center text-sm font-bold outline-none"
              />
              <button
                @click="updateCartQty(index, 1)"
                class="w-6 h-6 flex items-center justify-center bg-gray-100 hover:bg-gray-200 rounded text-gray-700 font-bold"
              >
                +
              </button>
            </div>

            <button
              @click="removeFromCart(index)"
              class="p-2 text-red-400 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors"
            >
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>

          <div
            v-if="cart.length === 0"
            class="text-center py-6 text-gray-400 bg-gray-50 rounded-2xl border border-dashed"
          >
            ตะกร้าว่างเปล่า
          </div>
        </div>

        <hr class="mb-6" />

        <form
          v-if="cart.length > 0"
          @submit.prevent="submitBorrowCheckout"
          class="space-y-4"
        >
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-bold mb-1 text-gray-700"
                >ชื่อ-นามสกุล <span class="text-red-500">*</span></label
              >
              <input
                v-model="formData.full_name"
                type="text"
                required
                class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border focus:bg-white focus:ring-2 focus:ring-[#a259ff] outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-bold mb-1 text-gray-700"
                >รหัสนักศึกษา <span class="text-red-500">*</span></label
              >
              <input
                v-model="formData.student_id"
                type="text"
                required
                class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border focus:bg-white focus:ring-2 focus:ring-[#a259ff] outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-bold mb-1 text-gray-700"
              >ช่องทางติดต่อ <span class="text-red-500">*</span></label
            >
            <input
              v-model="formData.contact_info"
              type="text"
              required
              class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border focus:bg-white focus:ring-2 focus:ring-[#a259ff] outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-bold mb-1 text-gray-700"
                >วันที่ยืม <span class="text-red-500">*</span></label
              >
              <input
                v-model="formData.borrow_date"
                type="date"
                required
                class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border focus:bg-white focus:ring-2 focus:ring-[#a259ff] outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-bold mb-1 text-gray-700"
                >วันที่คืน <span class="text-red-500">*</span></label
              >
              <input
                v-model="formData.return_date"
                type="date"
                required
                class="w-full px-4 py-2.5 rounded-xl bg-gray-50 border focus:bg-white focus:ring-2 focus:ring-[#a259ff] outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full mt-6 py-4 bg-gray-900 hover:bg-black text-white font-bold rounded-xl transition-all shadow-md disabled:opacity-50 text-lg"
          >
            {{
              isSubmitting ? "กำลังดำเนินการ..." : "ยืนยันการยืมครุภัณฑ์ทั้งหมด"
            }}
          </button>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue";
import Navbar from "../components/Navbar.vue";
import {
  LockClosedIcon,
  XMarkIcon,
  ArchiveBoxIcon,
  ShoppingCartIcon,
  TrashIcon,
} from "@heroicons/vue/24/solid";

const user = ref(null);
const equipments = ref([]);
const isCheckingAuth = ref(true);
const isLoading = ref(false);

// --- ระบบ Cart ---
const cart = ref([]);
const isCartOpen = ref(false);
const isSubmitting = ref(false);

const formData = reactive({
  full_name: "",
  student_id: "",
  contact_info: "",
  borrow_date: "",
  return_date: "",
});

onMounted(async () => {
  try {
    const res = await fetch("/api/auth/me", { credentials: "include" });
    const json = await res.json();
    user.value = json.user;
    if (user.value) fetchEquipments();
  } catch (error) {
    console.error("Not logged in");
  } finally {
    isCheckingAuth.value = false;
  }
});

const logout = async () => {
  await fetch("/api/auth/logout", { method: "POST", credentials: "include" });
  window.location.reload();
};

const fetchEquipments = async () => {
  isLoading.value = true;
  try {
    const res = await fetch("/api/equipments/central");
    const json = await res.json();
    if (json.status === "success") equipments.value = json.data;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

// 🛒 เพิ่มลงตะกร้า (เช็ค Validate)
const addToCart = (equipment) => {
  const existing = cart.value.find(
    (item) => item.equipment.id === equipment.id,
  );
  if (existing) {
    if (existing.quantity < equipment.available_quantity) existing.quantity++;
    else alert("ไม่สามารถเพิ่มได้เกินจำนวนที่มีในคลัง");
  } else {
    cart.value.push({ equipment: equipment, quantity: 1 });
  }
};

// ปรับจำนวนด้วยปุ่ม + / -
const updateCartQty = (index, amount) => {
  const item = cart.value[index];
  const newQty = item.quantity + amount;
  if (newQty > 0 && newQty <= item.equipment.available_quantity) {
    item.quantity = newQty;
  }
};

// เช็ค Validate ตอนพิมพ์ตัวเลขตรงๆ ใน Input
const validateCartQty = (index) => {
  const item = cart.value[index];
  if (item.quantity > item.equipment.available_quantity) {
    item.quantity = item.equipment.available_quantity;
    alert(`ปรับจำนวนสูงสุดได้ที่ ${item.equipment.available_quantity} ชิ้น`);
  } else if (item.quantity < 1 || isNaN(item.quantity)) {
    item.quantity = 1;
  }
};

const removeFromCart = (index) => {
  cart.value.splice(index, 1);
};

const submitBorrowCheckout = async () => {
  isSubmitting.value = true;
  try {
    const csrfRes = await fetch("/api/csrf-token", {
      method: "GET",
      credentials: "include",
    });
    const csrfData = await csrfRes.json();

    const payloadItems = cart.value.map((item) => ({
      equipment_id: item.equipment.id,
      quantity: item.quantity,
    }));

    const res = await fetch("/api/borrow/request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrfData.csrf_token,
      },
      credentials: "include",
      body: JSON.stringify({
        ...formData,
        items: payloadItems,
      }),
    });

    if (res.ok) {
      alert("✅ ส่งคำร้องสำเร็จ! ระบบตัดยอดอุปกรณ์เรียบร้อยแล้ว");
      isCartOpen.value = false;
      cart.value = [];
      Object.keys(formData).forEach((key) => (formData[key] = ""));
      fetchEquipments();
    } else {
      const errorData = await res.json();
      alert(`❌ ผิดพลาด: ${errorData.detail}`);
    }
  } catch (error) {
    alert("เกิดข้อผิดพลาดในการเชื่อมต่อ");
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
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
</style>
