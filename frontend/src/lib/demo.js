/**
 * The sandbox runs the storefront without the Frappe process. Vite's dev
 * server therefore uses the local catalogue unless an API target is
 * explicitly enabled with VITE_DEMO_MODE=false.
 */
export const isDemoMode = import.meta.env.DEV && import.meta.env.VITE_DEMO_MODE !== "false";
