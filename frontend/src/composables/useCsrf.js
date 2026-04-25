export function useCsrf() {
  const getCsrfToken = async () => {
    const res = await fetch("/api/csrf-token", { method: "GET", credentials: "include" });
    const data = await res.json();
    return data.csrf_token;
  };

  return { getCsrfToken };
}
