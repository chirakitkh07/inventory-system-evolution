# Lessons Learned and Project Closure Report
## Inventory Management System — Software Evolution & Maintenance
## Project Duration: 15 Weeks

---

## 1. Project Summary

| Item | Detail |
|------|--------|
| **Project** | Inventory Management System Refactoring |
| **Duration** | Weeks 1–15 (15 weeks) |
| **Final Version** | v2.0.0-final |
| **Architecture** | Repository Pattern + Dependency Injection |
| **Test Coverage** | 79 tests, 100% passing |
| **Security** | Bandit scan: 0 Medium/High issues |

---

## 2. What Went Well ✅

- **TDD discipline enforced by the Iron Rule**: Writing tests before refactoring prevented regressions. Every refactoring step was covered by tests, making it safe to change code incrementally.
- **Repository Pattern eliminated global state**: The `global x` variable that caused tight coupling and untestability was completely removed. The DI-based architecture enabled pure unit tests with no file I/O.
- **Conventional Commits + annotated tags** provided a clean, auditable history that will be easy to review months later.
- **CI with GitHub Actions** automated quality gating — no manual "did someone run tests?" guesswork.
- **Bandit** caught potential security issues early in the development cycle rather than post-deployment.

---

## 3. Challenges Faced ⚠️

- **Mixed I/O in v1**: The original `input()` calls inside business functions made the baseline tests require `monkeypatch` — a technique that added complexity to the test fixture setup.
- **Windows PATH issue with pytest/bandit**: Tools installed by `pip` were not on PATH; `python -m pytest` workaround was required.
- **Line-ending (CRLF/LF) warnings**: Git on Windows auto-converts line endings — added a `.gitattributes` recommendation for future work.

---

## 4. Technical Debt Resolved

| Debt Item | v1 | v2 |
|-----------|----|----|
| `global x` state | ❌ present | ✅ eliminated via DI |
| Cryptic names (`x`, `a`, `b`) | ❌ present | ✅ renamed descriptively |
| Logic mixed with `input()`/`print()` | ❌ present | ✅ separated into UI layer |
| No data persistence | ❌ in-memory only | ✅ JSON file via Repository |
| No error handling | ❌ crashes on bad input | ✅ validated with ValueError |
| No barcode support | ❌ | ✅ CR-01 complete |
| No CSV export | ❌ | ✅ CR-02 complete |

---

## 5. Recommendations for Future Teams

1. **Never skip baseline tests** before refactoring. The v1 test suite was the safety net that made every refactoring step reversible.
2. **Use `git revert` not `git reset --hard`** on shared branches — always.
3. **Add `.gitattributes`** to normalise line endings on cross-platform teams.
4. **Consider SQLite** as next persistence upgrade — `InventoryRepository` can be swapped with a new implementation without touching service or UI layers.
5. **Add pytest-cov** for coverage reporting in the CI pipeline.

---

## 6. Final Git Log Summary

```
git log --oneline main
```
Key milestones:
- `v1.0.0-baseline` — Baseline snapshot before refactoring
- `v2.0.0-evolution` — Production Release: Repository Pattern + Barcode + Reorder + CSV
- `v2.0.0-final` — Final defense release, project closed

---

*Project formally closed. Archive Jira board: ENGSE project.*
