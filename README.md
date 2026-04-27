# 📐 Least Squares Lab

A web-based **Linear Algebra study tool** focused on Least Squares Approximation. Enter any overdetermined system (matrix **A** and vector **b**), and get the solution **x̂** along with a full, numbered step-by-step breakdown — from computing the transpose through verifying orthogonality.

---

## ✨ Features

| Tab | What it does |
|-----|-------------|
| **📖 Theory** | Explains the core concept, the normal equations, the 7-step solution process, geometric intuition (projection), and key exam vocabulary |
| **✏️ Calculator** | Enter any matrix A (rows × columns) and vector b, then solve — displays x̂, residual, residual norm, and an orthogonality check |
| **⚡ Examples** | One-click presets: Linear Fit (4-pt), Simple 3×2, 5×3 Overdetermined, Quadratic Curve Fit |

**Calculation pipeline (shown step by step):**

1. Confirm the system is overdetermined (rows > columns)
2. Compute **Aᵀ** (transpose)
3. Form **AᵀA** (normal matrix)
4. Compute **Aᵀb** (RHS vector)
5. Solve **(AᵀA)x̂ = Aᵀb** via `numpy.linalg.lstsq`
6. Compute residual **r = b − Ax̂** and its norm ‖r‖
7. Verify **Aᵀr ≈ 0** (orthogonality / correctness check)

---

## 🛠️ Tech Stack

- **[Flask](https://flask.palletsprojects.com/)** — lightweight Python web framework
- **[NumPy](https://numpy.org/)** — matrix operations and least-squares solver
- **[Gunicorn](https://gunicorn.org/)** — WSGI server for production deployment

---

## 🚀 Running Locally

**1. Clone the repo**

```bash
git clone https://github.com/AdetayoKalejaiye/linearalgebra.git
cd linearalgebra
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Start the server**

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

**Production start (gunicorn)**

```bash
gunicorn app:app
```

---

## 📖 How to Use the Calculator

1. Navigate to the **✏️ Calculator** tab.
2. Enter matrix **A** — one row per line, values separated by spaces.  
   _Example 4×2 matrix:_
   ```
   1 1
   1 2
   1 3
   1 4
   ```
3. Enter vector **b** — one value per line (must match the number of rows in A).  
   _Example:_
   ```
   1
   3
   4
   6
   ```
4. Click **▶ Solve & Explain**.

The results panel shows:
- **x̂** — the least squares solution
- **Residual r** — per-equation error
- **‖r‖** — total error (0 means an exact solution existed)
- **Aᵀr ≈ 0** — orthogonality confirmation

> **Tip:** Use the **⚡ Examples** tab to load a preset and explore the output before entering your own data.

---

## 📁 Project Structure

```
linearalgebra/
├── app.py            # Flask app — HTML, CSS, JS, and /solve API all in one file
├── requirements.txt  # Python dependencies (flask, numpy, gunicorn)
└── README.md
```

---

## 📐 The Math (Quick Reference)

Given an overdetermined system **Ax ≈ b** (more equations than unknowns), the **least squares solution** minimises ‖b − Ax‖²:

```
x̂ = (AᵀA)⁻¹ Aᵀb        ← closed-form (Normal Equations)
```

The residual **r = b − Ax̂** is orthogonal to every column of A:

```
Aᵀr = 0
```

This is guaranteed by the Normal Equations and is verified after every calculation.
