import axios from 'axios'
import qs from 'qs'

axios.interceptors.request.use(
    config => {
        if (config.method === 'post') {
            if (config.url.indexOf('api') === -1){
                config.data = qs.stringify(config.data)
            }
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)
export default axios