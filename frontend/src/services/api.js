import axios from 'axios'
let refreshSubscribers = []
let isRefreshing = false


function onRrefreshed(token) {
for (const cb of refreshSubscribers) {
	cb(token)
}
refreshSubscribers = []
}


function addRefreshSubscriber(cb) {
refreshSubscribers.push(cb)
}


api.interceptors.response.use(
res => res,
async err => {
const auth = useAuthStore()
const original = err.config
if (err.response?.status === 401 && !original._retry) {
original._retry = true
if (isRefreshing) {
return new Promise((resolve) => {
addRefreshSubscriber((token) => {
original.headers.Authorization = `Bearer ${token}`
resolve(api(original))
})
})
}
isRefreshing = true
try {
const resp = await axios.post(`${api.defaults.baseURL.replace('/api', '')}/api/auth/token/refresh/`, { refresh: auth.refreshToken })
const newAccess = resp.data.access
auth.setAccessToken(newAccess)
onRrefreshed(newAccess)
isRefreshing = false
original.headers.Authorization = `Bearer ${newAccess}`
return api(original)
} catch (e) {
isRefreshing = false
auth.logout()
throw e
}
}
throw err
}
)


const api = axios.create({
	baseURL: 'http://localhost:8000/api/',
	headers: {
		'Content-Type': 'application/json',
	},
})

export default api