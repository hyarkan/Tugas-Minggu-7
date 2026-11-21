## Ringkasan perubahan
Jelaskan perubahan yang dibuat dan kaitannya dengan tugas Minggu 6.

## Checklist implementasi
- [ ] KRSStatus dan `transition()` menolak transisi ilegal
- [ ] Submit menolak KRS kosong dan menjalankan `validate_krs()` ulang
- [ ] Approve/revise memeriksa dosen PA dan kepemilikan
- [ ] Endpoint submit/approve/revise mengembalikan 403/409 sesuai kondisi
- [ ] Approval menyimpan status, timestamp, audit log, dan notifikasi dalam satu transaksi
- [ ] Pessimistic lock dan optimistic version diterapkan
- [ ] Property test total SKS: 1.000 contoh
- [ ] Property test bentrok jadwal: 1.000 contoh
- [ ] Pengujian state machine: 4 transisi legal dan 28 transisi ilegal (total 32 kombinasi state dan aktor)
- [ ] AI Log, OPAR, ADR, dan risiko/limitasi diperbarui

## Bantuan AI dan revisi manual
Jelaskan bagian yang dibantu AI, pemeriksaan yang dilakukan, serta revisi manual yang diterapkan.

## Tiga prompt terbaik
1. Prompt analisis state machine dan aktor.
2. Prompt transaction management dan concurrency.
3. Prompt property-based testing dan edge cases.

## Risiko dan limitasi
- Header `X-Actor-*` hanya simulasi identitas untuk demo, bukan autentikasi produksi.
- `dosen_pa_id` harus ditetapkan oleh proses akademik sebelum approval.
- SQLite tidak membuktikan row-level locking MySQL/InnoDB atau race condition multi-worker.
- Notifikasi masih dicatat ke database; pengiriman email/push ditangani pada tahap observer berikutnya.

## Cara pengujian
```bash
pip install -r requirements.txt
alembic upgrade head
alembic current
python -m pytest -v --cov=app --cov-report=term-missing
```

## Bukti pengujian
Hasil verifikasi lokal terakhir:
- 64 passed, 0 failed, 0 errors.
- Total coverage: 85%.
- Alembic current: `0004_krs_state_machine (head)`.
- Terdapat satu deprecation warning dari Starlette/httpx yang tidak menyebabkan kegagalan.

Lampirkan log migration, hasil Pytest, contoh respons endpoint, dan screenshot Swagger UI.

Pengujian MySQL/InnoDB, race condition multi-worker, dan forced rollback belum dilakukan dan tetap menjadi keterbatasan pengujian.
