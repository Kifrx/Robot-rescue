# Robot Rescue Pathfinding

Proyek ini ialah simulasi visualisasi *pathfinding* (pencarian jalur) berbasis *Weighted Graph* menggunakan Python dan Pygame. Program ini mensimulasikan sebuah robot penyelamat yang harus mengevakuasi 3 orang korban yang tersebar di dalam area berukuran 6x6 *node*.

##  Algoritma yang Digunakan

Robot rescue ini memakai dua algoritma utama yang bisa dibandingkan secara langsung kinerjanya, yaitu:

1. **Breadth-First Search (BFS):** Algoritma yang mencari rute berdasarkan **jumlah langkah (edge) paling sedikit**, tanpa mempedulikan bobot atau jarak sebenarnya antar *node*.
2. **Dijkstra's Algorithm:** Algoritma pencarian rute terpendek yang memperhitungkan **total bobot (cost/jarak) paling kecil**, sehingga robot mungkin memilih jalur memutar jika bobotnya lebih ringan.

**Logika Penyelamatan (Greedy Nearest Neighbor):**
Karena ada 3 target korban, robot dilengkapi dengan kecerdasan *Greedy*. Dari posisinya berada, robot akan menghitung jarak ke semua korban yang tersisa, lalu secara otomatis memprioritaskan penyelamatan korban dengan rute paling "murah" (berdasarkan langkah untuk BFS, atau berdasarkan bobot untuk Dijkstra) terlebih dahulu.

---

##  Cara Menjalankan Program

### Prasyarat
Pastikan kamu sudah menginstal Python 3.x di komputermu. Program ini juga membutuhkan *library* eksternal `pygame`.

### Langkah-langkah Instalasi
1. *Clone repository* ini ke dalam mesin lokalmu:
   ```bash
   git clone [https://github.com/Kifrx/Robot-rescue.git](https://github.com/Kifrx/Robot-rescue.git)
2. Masuk ke dalam direktori proyek:
   ```
   cd Robot-rescue
   ```
3. Instal dependencies Pygame:
   ```
   pip install -r requirements.txt
   ```
4. Jalankan program utamanya:
   ```
   python main.py
   ```

## How to play??
1. Saat program terbuka, klik salah satu lingkaran (*node*) untuk meletakkan **Robot**.
2. Klik pada 3 *node* lainnya yang berbeda untuk meletakkan **Korban**.
3. Perhatikan panel teks berwarna kuning di atas untuk panduan status saat ini.
4. Setelah data lengkap, klik tombol **Jalankan BFS** atau **Jalankan Dijkstra**.
5. Lihat animasi pergerakan robot dan perhatikan perbandingan statistik "Total Langkah" dan "Total Bobot" di bagian bawah layar.
6. Klik tombol **Reset** untuk menghapus dan memulai ulang simulasi dari awal.
