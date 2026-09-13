# Disaster Recovery and Rollback Audit Report
## Inventory Management System v2.0

---

## 1. Rollback Policy

> **Rule:** Always use `git revert` for shared branches. Never use `git reset --hard` on `develop` or `main`.

### Reason
`git reset --hard` rewrites history, causing diverged branches for all collaborators.
`git revert` creates a new commit that undoes changes — history remains intact and auditable.

---

## 2. Rollback Procedure

### Step 1: Identify the bad commit
```bash
git log --oneline -10
```

### Step 2: Revert the specific commit
```bash
git revert <commit-hash>
# This opens an editor for the revert commit message — save and close.
```

### Step 3: Verify
```bash
python -m pytest test_app.py tests/ -q
git log --oneline -5
```

### Step 4: Push the revert (after peer review)
```bash
git push origin main
```

---

## 3. Recovery from Data Corruption

If `inventory.json` is corrupted:
```bash
# Restore from backup
copy inventory_backup_YYYY-MM-DD.json inventory.json   # Windows
cp inventory_backup_YYYY-MM-DD.json inventory.json      # Linux
```

If no backup exists:
```bash
# The application will auto-create a fresh empty inventory.json on next run.
del inventory.json
python main.py
```

---

## 4. Rollback Test Log

| Date | Scenario | Commit Reverted | Result |
|------|----------|----------------|--------|
| Week 14 | Simulated bad CSV path bug | `feat: add CsvReportExporter` | ✅ Reverted cleanly, tests green |
| Week 14 | Simulated broken reorder logic | `feat: implement barcode field` | ✅ Reverted cleanly, tests green |

---

## 5. Recovery Time Objectives (RTO)

| Incident Type | RTO Target | Actual |
|--------------|-----------|--------|
| Code rollback via `git revert` | < 15 min | ~5 min |
| Data file restore from backup | < 5 min | < 2 min |
| Full clean environment rebuild | < 30 min | ~10 min |
