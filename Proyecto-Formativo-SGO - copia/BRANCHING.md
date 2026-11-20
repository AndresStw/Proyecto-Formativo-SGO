# Branching Strategy — Sabor Caleño Backend

This project already has multiple branches (`main`, `frontend`, `backend`, etc.).
**All backend work happens on the `backend` branch.**

---

## 🗺️ Branch overview

```
main (protected, production-ready)
  ▲
  │ (merged only when a release is ready)
  │
backend (protected, backend integration)
  ▲ ▲ ▲
  │ │ │
  │ │ └── feature/ep04-reservas
  │ └──── feature/ep03-pedidos
  └────── feature/ep01-auth
```

| Branch                       | Who commits directly      | Who can open PRs                           |
| ---------------------------- | ------------------------- | ------------------------------------------ |
| `main`                       | ❌ Nobody                 | Only the project lead (`backend` → `main`) |
| `backend`                    | ❌ Nobody                 | Any backend dev (feature → `backend`)      |
| `feature/*`, `fix/*`, `db/*` | ✅ The dev who created it | Same dev                                   |

> **In short:** Nobody pushes directly to `main` or `backend`. Everything goes through Pull Requests. Feature branches are private to each developer.

---

## 🚀 Starting a new task

### 1. Make sure your `backend` is up to date

```powershell
git checkout backend
git pull origin backend
```

### 2. Create your feature branch from `backend`

Branch names must include the epic ID from `TASKS.md`:

```powershell
# Example: EP-01 (Authentication)
git checkout -b feature/ep01-auth

# Example: EP-03 (Orders)
git checkout -b feature/ep03-orders

# Example: fix on a specific epic
git checkout -b fix/ep02-product-category

# Example: database migration
git checkout -b db/add-reservas-table
```

### 3. Work and commit

Use the commit convention from `CONTRIBUTING.md`:

```powershell
git add app/api/auth.py app/services/auth_service.py
git commit -m "feat(ep01): add POST /login endpoint"
```

### 4. Push your branch to GitHub

```powershell
git push -u origin feature/ep01-auth
```

### 5. Open a Pull Request to `backend`

On GitHub:

1. Go to your branch → **Compare & pull request**
2. **Base branch: `backend`** (⚠️ not `main`)
3. Fill the PR template (see below)
4. Request a review from a teammate
5. Once approved → **Squash and merge**
6. **Delete the branch** after merge

---

## 🔄 Keeping your branch up to date

If `backend` gets new commits while you're still working on your feature:

```powershell
# Make sure you're on your feature branch
git checkout feature/ep01-auth

# Fetch and rebase onto latest backend
git fetch origin
git rebase origin/backend
```

**Why rebase and not merge?** Rebasing keeps history linear and avoids "merge commit" noise. If you get conflicts, resolve them and continue:

```powershell
# After resolving conflicts in the editor
git add <resolved-files>
git rebase --continue
```

> ⚠️ **Never rebase a branch that someone else is also working on.** For solo feature branches, rebase is safe.

---

## 📋 Pull Request template

When you open a PR, use this format:

```markdown
## What does this PR do?

Brief description of the change.

## Epic reference

EP-01 (Authentication)

## Checklist

- [ ] `pytest -q` passes
- [ ] Endpoints tested manually in PowerShell
- [ ] No `.env` or `venv/` in the diff
- [ ] README updated if new endpoints added
- [ ] No `console.log` / `print()` debug statements left

## Screenshots (if UI-related)

(optional)
```

---

## 🎯 When does `backend` go to `main`?

`backend` merges into `main` **only when a milestone is complete**. Typical triggers:

- ✅ All of EP-01 to EP-07 are merged into `backend`
- ✅ The demo/final presentation is ready
- ✅ Tests pass on `backend` (`pytest -q`)
- ✅ The deployed Vercel backend (from `backend`) responds correctly

Who does it: **only the project lead**.

```powershell
# Lead only — never do this yourself
git checkout main
git pull origin main
git merge --no-ff backend -m "release: backend v1.0 (EP-01 to EP-07)"
git push origin main
```

---

## ⚠️ Things you should NEVER do

| ❌ Don't                                  | Why                                           |
| ----------------------------------------- | --------------------------------------------- |
| `git push origin main`                    | Protected branch — will be rejected anyway    |
| `git push origin backend` (direct)        | Same — always go via PR                       |
| `git commit` on `backend`                 | Branch off it first                           |
| `git push --force` on `backend` or `main` | Destroys teammates' work                      |
| `git add .` without checking              | You might add `.env`, `venv/`, `__pycache__/` |
| `git add -f .env`                         | Forces the add despite `.gitignore`           |
| `git commit -m "fix"`                     | Use the convention from `CONTRIBUTING.md`     |

---

## 🆘 Common scenarios

### "I started on the wrong branch"

```powershell
# Move your uncommitted changes to a new branch
git stash
git checkout backend
git pull origin backend
git checkout -b feature/correct-name
git stash pop
```

### "I committed directly to `backend` by mistake"

```powershell
# Save your commit to a new branch
git branch feature/recover-my-work
git reset --hard origin/backend
git checkout feature/recover-my-work
```

### "My branch has conflicts with `backend`"

```powershell
git fetch origin
git rebase origin/backend
# Resolve conflicts in VS Code, then:
git add <resolved-files>
git rebase --continue
git push --force-with-lease origin feature/your-branch
```

> `--force-with-lease` is safer than `--force` because it refuses to overwrite if someone else pushed to the branch since you last pulled.

### "I forgot to pull before creating my branch"

If your feature branch is based on stale `backend`:

```powershell
git fetch origin
git rebase origin/backend
```

If rebase gets messy, an alternative is:

```powershell
git merge origin/backend
```

But **only do this if you're stuck** — merge commits pollute history.

---

## ✅ TL;DR

1. **Always branch off `backend`**
2. **Name branches `feature/epXX-task`**
3. **PR to `backend`** (never to `main`)
4. **Get one approval** before merging
5. **Squash and merge** on GitHub
6. **Delete your branch** after merging
7. **Only the lead** merges `backend` → `main`

That's it. Keep it simple, keep it clean.

# Branching Strategy — Sabor Caleño Backend

> ⚠️ **IMPORTANT RULE:** We work **ONLY** on the `Backend` branch for Python development.
> `main` is for final releases. Do not push directly to `Backend` or `main`.

---

## 🧹 Current Branch Cleanup (Read this first)

Looking at our current repository, we have a mix of branches. Going forward, we are standardizing the workflow:

- **`main`**: Production. Protected. Only the Lead merges here.
- **`Backend`**: Integration. All Python work merges here.
- **`Frontend`**: Integration. All React work merges here.
- **`Documentation`**: For our PDFs and markdown files.

**What about `Brandon`, `feature/Daniela`, `feature/samuel`, etc.?**
We are **abandoning personal branches**. From now on, you do not create a branch with your name. You create a branch based on the **Task/Epic** you are working on (see `TASKS.md`).

- ❌ Don't do: `feature/samuel`
- ✅ Do this: `feature/ep01-auth` (If Samuel is working on EP-01)

---

## ⚡ Quick Start: How to start a new task

Every new task starts with these **3 commands**:

```powershell
git checkout Backend               # 1. Switch to Backend
git pull origin Backend            # 2. Get latest changes
git checkout -b feature/epXX-name  # 3. Create your task branch
```
