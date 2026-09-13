# Prompt สำหรับ AI Agent: แผนพัฒนาโค้ด + Git Workflow สัปดาห์ที่ 1–15
## โปรเจกต์: Inventory Management System (Software Evolution & Maintenance)

คุณคือ AI coding agent ที่ช่วยพัฒนาโปรเจกต์ Refactoring ระบบคลังสินค้า (Inventory System)
จากโค้ดตั้งต้น `app_v1.py` ไปสู่สถาปัตยกรรมใหม่ตาม Repository Pattern พร้อมฟีเจอร์ใหม่
ทำตามแผนงานและ Git workflow ด้านล่างนี้ทีละสัปดาห์ ห้ามข้ามขั้นตอน และต้องรัน PyTest ให้ผ่าน 100% ก่อน commit ทุกครั้ง

---

## Phase 1: Baseline (สัปดาห์ 1–4)

**เป้าหมาย:** วิเคราะห์โค้ดเดิม ตั้ง Baseline ที่ตรวจสอบได้

- อ่านและวิเคราะห์ `app_v1.py` หา technical debt: ตัวแปร global (`global x`), ชื่อตัวแปรกำกวม (`x`, `a`, `b`), logic ปนกับ `input()`/`print()`
- เขียน `test_app.py` ชุดแรก ให้ครอบคลุมพฤติกรรมเดิมของระบบ (baseline regression test)
- รัน `pytest` ต้องได้ `1 passed` (เขียว 100%) ก่อนเริ่มแก้โค้ดใดๆ
- ตั้งค่า Git repo, `.gitignore`, `requirements.txt`

**Git ที่ต้องทำ:**
```bash
git init
git add app_v1.py test_app.py requirements.txt .gitignore
git commit -m "chore: initial baseline import of app_v1.py with test suite"
git tag -a v1.0.0-baseline -m "Baseline snapshot before refactoring"
git push origin main --tags
```

---

## Phase 2: Design (สัปดาห์ 5–7)

**เป้าหมาย:** ออกแบบสถาปัตยกรรมใหม่ + วางระบบ CI/CD

- ออกแบบ UML Class Diagram (To-Be Architecture):
  - `Product` — data model
  - `InventoryRepository` — อ่าน/เขียนข้อมูล JSON
  - `InventoryService` — business logic
  - `ConsoleUI` — เมนู interface
- ใช้ Design Pattern: Repository, Singleton, Factory
- ตั้งค่า GitHub Branch Protection บน `develop`: require PR + require status check (PyTest CI) ก่อน merge
- ตั้งค่า GitHub Actions CI ให้รัน `pytest` อัตโนมัติทุก PR
- ทำ CI/CD dry-run ให้ผ่านเขียว 100% ก่อนขอ sign-off

**Git ที่ต้องทำ:**
```bash
git checkout -b develop
git add docs/class-diagram.png .github/workflows/pytest.yml
git commit -m "docs: add to-be architecture diagram and ISO 25010 evaluation"
git commit -m "ci: setup GitHub Actions workflow for automated PyTest"
git push origin develop
```

---

## Phase 3: Refactor + Change Requests (สัปดาห์ 8–12)

### สัปดาห์ 8 — Refactor Core
- แตก branch: `feature/refactor-core-architecture`
- Refactor ตามเทคนิค Fowler: Rename Variable, Extract Function, Extract Class, Encapsulate Field
- กำจัด `global x` ด้วย Dependency Injection (inject `InventoryRepository` เข้า `InventoryService`)
- **กฎเหล็ก:** ห้าม refactor โค้ดที่ไม่มี unit test คุม / แก้ทีละเล็กแล้วรัน pytest ทันที ถ้าแดงให้ `git checkout` ถอยกลับ

```bash
git checkout -b feature/refactor-core-architecture
# แก้โค้ดทีละจุด + รัน pytest ทุกครั้ง
git commit -m "refactor: extract InventoryService and remove global state"
git commit -m "refactor: rename cryptic variables (x, a, b) to descriptive names"
```

### สัปดาห์ 9 — CR-01 Barcode & Reorder Point
- แตก branch: `feature/cr01-barcode-reorder-point`
- เขียน test ก่อน (TDD/TDR) แล้วพัฒนาโค้ดจนเขียว 100%

```bash
git checkout -b feature/cr01-barcode-reorder-point
git commit -m "test: add failing test for barcode and reorder point (TDR)"
git commit -m "feat: implement barcode field and reorder point alert (CR-01)"
```

### สัปดาห์ 10 — CR-02 CSV Export
- Bug bashing หา edge case ในฟังก์ชัน barcode/reorder
- แตก branch: `feature/cr02-csv-export`
- พัฒนาคลาส `CsvReportExporter`

```bash
git checkout -b feature/cr02-csv-export
git commit -m "fix: resolve edge case in reorder point calculation"
git commit -m "feat: add CsvReportExporter class for low-stock report (CR-02)"
```

### สัปดาห์ 11 — Hardening
- Merge CR-01 → develop, sync/merge CR-02 (แก้ conflict ถ้ามี)
- สแกน security ด้วย Bandit
- รัน Full Regression Test Suite

```bash
git checkout develop && git pull
git merge feature/cr01-barcode-reorder-point
git checkout feature/cr02-csv-export
git merge develop   # แก้ conflict
git commit -m "fix: resolve merge conflicts with develop"
git commit -m "chore: run bandit security scan and fix flagged issues"
```

### สัปดาห์ 12 — Closure Sprint 3
- ตรวจรับ UAT, merge เข้า `main`, ปักแท็ก release

```bash
git checkout main
git merge develop
git tag -a v2.0.0-evolution -m "Production Release v2.0.0: Refactored Repository Pattern, Barcode Support, Reorder Point Alerts, and CSV Reporting."
git push origin main --tags
```

---

## Phase 4: Deployment & Closure (สัปดาห์ 13–15)

### สัปดาห์ 13 — Clean Deployment
- ทดสอบติดตั้งบน Clean Environment
- รัน Smoke Test → Full Regression → เก็บ log ผลการรัน
- เขียน script ติดตั้งอัตโนมัติ

```bash
git commit -m "test: add smoke test and full regression log (post_maintenance_test.log)"
git commit -m "chore: add setup.sh and .env.example for clean deployment"
git commit -m "docs: add system operations and maintenance manual (ISO/IEC 14764)"
```

### สัปดาห์ 14 — Resilience & Packaging
- ทดสอบ Disaster Recovery / Rollback (ใช้ `git revert` ห้ามใช้ `git reset --hard`)
- Security & Stress Test ขั้นสูง
- Build distribution package

```bash
git commit -m "docs: add disaster recovery and rollback audit report"
git build   # หรือ python -m build เพื่อสร้าง wheel ใน dist/
git commit -m "chore: add Dockerfile and build distribution package (wheel)"
```

### สัปดาห์ 15 — Final Defense
- Live Demo: เพิ่มสินค้า+barcode, ค้นหาด้วย barcode, ตัดสต็อกจนต่ำกว่า reorder point (ไฟเตือนเหลือง/แดง), export CSV เปิดใน Excel
- ปิดโปรเจกต์: archive Jira board, final commit สรุป

```bash
git commit -m "docs: finalize lessons learned and project closure report"
git tag -a v2.0.0-final -m "Final defense release - project closed"
git push origin main --tags
```

---

## กฎ Commit Message ที่ต้องยึดตลอดโปรเจกต์

- ใช้ Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`, `ci:`
- ถ้ามี Jira issue ให้ใส่ issue key ในชื่อ branch หรือ commit message เช่น `(ENGSE-102)` หรือ `(fixes #12)`
- ใช้ Annotated Tag (`git tag -a`) เท่านั้นสำหรับ milestone/release ไม่ใช้ lightweight tag
- ห้าม merge เข้า `develop`/`main` ถ้า PyTest ไม่ผ่านเขียว 100% หรือยังไม่ได้ Peer Review approve อย่างน้อย 1 คน
- กรณีต้องย้อนคืนโค้ด ให้ใช้ `git revert` เท่านั้น ห้ามใช้ `git reset --hard` บน branch ที่แชร์กับทีม
