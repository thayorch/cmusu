import { reactive } from "vue";

const state = reactive({
  visible: false,
  type: "info",
  message: "",
  resolve: null,
});

export function useAlert() {
  const showAlert = (message, type = "info") =>
    new Promise((resolve) => {
      Object.assign(state, { visible: true, type, message, resolve });
    });

  const showConfirm = (message) =>
    new Promise((resolve) => {
      Object.assign(state, {
        visible: true,
        type: "confirm",
        message,
        resolve,
      });
    });

  const showWarningConfirm = (message) =>
    new Promise((resolve) => {
      Object.assign(state, {
        visible: true,
        type: "confirm",
        message,
        resolve,
      });
    });

  const close = (result = true) => {
    state.visible = false;
    if (state.resolve) state.resolve(result);
    state.resolve = null;
  };

  return { state, showAlert, showConfirm, close };
}
