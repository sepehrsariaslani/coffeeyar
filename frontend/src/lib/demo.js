/**
 * The sandbox runs the storefront without the Frappe process. Vite's dev
 * server therefore uses the local catalogue unless an API target is
 * explicitly enabled with VITE_DEMO_MODE=false.
 */
export const isDemoMode = import.meta.env.DEV && import.meta.env.VITE_DEMO_MODE !== "false";

// This is intentionally a preview-only credential. It is a SHA-256 digest,
// not a production authentication mechanism; real Frappe deployments always
// use the backend login endpoint.
const DEMO_ADMIN_USERNAME = "administrator";
const DEMO_ADMIN_PASSWORD_SHA256 = "cc03c2376095ecf9660fac9ee751216e4119f293a9f821b8c79e80d13862e933";

async function sha256(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export async function authenticateDemoAdmin(identifier, password) {
  if (!isDemoMode || String(identifier || "").trim().toLowerCase() !== DEMO_ADMIN_USERNAME) return null;
  if (await sha256(String(password || "")) !== DEMO_ADMIN_PASSWORD_SHA256) return null;

  return {
    name: "Administrator",
    email: "administrator@demo.local",
    username: DEMO_ADMIN_USERNAME,
    phone: "",
    is_admin: true,
    demo: true,
  };
}
