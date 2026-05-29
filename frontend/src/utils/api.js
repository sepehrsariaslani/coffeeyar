const csrfToken = () => window.csrf_token || ''

async function call(method, args = {}, { post = false } = {}) {
  const endpoint = `/api/method/${method}`

  if (!post) {
    const query = new URLSearchParams()
    Object.entries(args || {}).forEach(([key, value]) => {
      if (value === undefined || value === null) return
      if (typeof value === 'object') {
        query.set(key, JSON.stringify(value))
      } else {
        query.set(key, String(value))
      }
    })

    const res = await fetch(query.toString() ? `${endpoint}?${query}` : endpoint, {
      credentials: 'same-origin',
    })
    const json = await res.json()
    if (!res.ok) throw new Error(json?.message || 'Request failed')
    return json.message
  }

  const payload = new URLSearchParams()
  Object.entries(args || {}).forEach(([key, value]) => {
    if (value === undefined || value === null) return
    payload.set(key, typeof value === 'object' ? JSON.stringify(value) : String(value))
  })

  const res = await fetch(endpoint, {
    method: 'POST',
    body: payload,
    credentials: 'same-origin',
    headers: {
      'X-Frappe-CSRF-Token': csrfToken(),
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    },
  })
  const json = await res.json()
  if (!res.ok || json.exc) {
    throw new Error(json?._server_messages || json?.message || 'Request failed')
  }
  return json.message
}

export const api = {
  listProducts(filters = {}, sort = 'default', page = 1) {
    return call('coffeeyar.api.list_products', { filters, sort, page })
  },
  listCategories() {
    return call('coffeeyar.api.list_categories')
  },
  listAttributes() {
    return call('coffeeyar.api.list_attributes')
  },
  listProductVariants(slug) {
    return call('coffeeyar.api.list_product_variants', { slug })
  },
  getProduct(slug) {
    return call('coffeeyar.api.get_product', { slug })
  },
  getSitePage(slug = 'home') {
    return call('coffeeyar.api.get_site_page', { slug })
  },
  listBlogPosts(page = 1, pageSize = 12) {
    return call('coffeeyar.api.list_blog_posts', { page, page_size: pageSize })
  },
  getBlogPost(slug) {
    return call('coffeeyar.api.get_blog_post', { slug })
  },
  getNavigation() {
    return call('coffeeyar.api.get_navigation')
  },
  createOrder(payload) {
    return call('coffeeyar.api.create_order', { payload }, { post: true })
  },
  startPayment(order_id, order_token) {
    return call('coffeeyar.api.start_payment', { order_id, order_token }, { post: true })
  },
  verifyPayment(order_id, authority, status) {
    return call('coffeeyar.api.verify_payment', { order_id, authority, status }, { post: true })
  },
}
