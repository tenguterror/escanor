# Pull Request Checklist

How Tengu and Baus work together. One rule above all: **nobody merges their own code without the other person looking at it.**

---

## 🎩 Author: you wrote the code

1. **Start fresh**
   - Terminal: `git switch main`, `git pull`, then `git switch -c feature/<name>`
   - VS Code: branch name (bottom-left) → `main` → **Pull** → branch name → **Create new branch...**
2. **Code and commit** as you go
   - Terminal: `git add <file>`, then `git commit -m "type: what changed"`
   - VS Code: `+` to stage → message → ✓ **Commit**
   - New files need `git add`; `git commit -am` only grabs files git already tracks.
3. **Push**
   - Terminal: `git push -u origin feature/<name>` (first time), `git push` after that
   - VS Code: **Publish Branch** / **Sync Changes**
4. **Open the PR** on GitHub (`feature/<name>` → `main`)
   - **Title:** what it does
   - **Description:** 2–3 lines: *what changed* and *how you tested it*
5. **Tell Baus "PR is up"**
6. ⏸️ **Wait for the review. Don't merge yet.**
7. **Fix anything flagged** on the same branch → commit → push. The PR updates by itself.
8. **Merge** on GitHub when you're both happy
9. **Clean up**
   - Terminal: `git switch main`, `git pull`, `git branch -d feature/<name>`, `git push origin --delete feature/<name>`
   - VS Code: switch to `main` → **Pull** → `...` → **Branch → Delete Branch...**; **Delete branch** button on the merged PR

Finished when your prompt shows `main ≡`.

---

## 🔍 Reviewer: Baus wrote the docs

1. Open the PR → **Files changed** tab
2. Read the diff: **green** = added, **red** = removed
3. Ask: *Is it accurate? Anything wrong or missing?*
4. **Leave one specific comment.** Even "checked the step 3 wording, it's clear" counts.
5. **Merge**
6. `git pull` on `main` (VS Code: **Pull**)

---

## The one-line version

> **Author:** push → describe → **wait** → fix → merge → clean up.
> **Reviewer:** read → comment → merge.

---

## When git complains

| You see | It means | Do this |
|---|---|---|
| `divergent branches` | Both sides have new commits | `git pull --no-rebase origin main` |
| An editor opens after a pull | Git wants a merge commit message | Save and close (micro: `Ctrl+S`, `Ctrl+Q`) |
| `↑3` in the prompt | 3 local commits not on GitHub | `git push` |
| `?1` in the prompt | 1 untracked file | `git add` it, or delete it if it's junk |
| `≡` in the prompt | Local and GitHub match | Nothing, you're in sync ✅ |
