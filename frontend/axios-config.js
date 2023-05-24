import axios from 'axios';

// Membuat instance Axios
const instance = axios.create({
  baseURL: 'https://example.com', // Ganti dengan URL server Anda
  timeout: 5000, // Waktu tunggu maksimum untuk permintaan
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*', // Atur domain yang diizinkan atau gunakan '*' untuk semua domain
  },
});

export default instance;