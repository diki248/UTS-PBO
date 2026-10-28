# UTS Pemrograman Berorientasi Objek

## Identitas
- NIM: ISI_NIM_ANDA
- Nama: ISI_NAMA_ANDA

## Deskripsi
Program Python untuk membaca dan mengolah data karyawan dan sensor dari dua file JSON.

## File
- `main.py`: kode program utama.
- `employee.json`: 30 data karyawan dari soal.
- `sensor_logs.json`: 30 data sensor dari soal.

## Konsep OOP
- **Rule:** aturan bonus dan klasifikasi suhu.
- **Inheritance:** `PermanentEmployee` dan `ContractEmployee` mewarisi `Employee`; `TemperatureSensor` mewarisi `Sensor`.
- **Polymorphism:** metode yang sama dapat menghasilkan perilaku berbeda sesuai jenis objek.
- **Override:** kelas turunan mengimplementasikan `calculate_salary()` dan `determine_status()`.

## Cara menjalankan
Pastikan Python 3 terpasang dan semua file berada dalam folder yang sama. Jalankan:

```bash
python main.py
```

## Catatan aturan
Soal tidak mencantumkan persentase bonus atau ambang suhu. Persentase bonus dan ambang suhu dalam program merupakan asumsi contoh dan perlu disesuaikan jika dosen memberikan aturan khusus.
