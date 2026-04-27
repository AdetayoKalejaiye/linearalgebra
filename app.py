from flask import Flask, render_template_string, request, jsonify
import numpy as np
import json

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Least Squares Lab</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --card: #16161f;
    --border: #2a2a3a;
    --accent: #6c63ff;
    --accent2: #ff6584;
    --accent3: #43e97b;
    --text: #e8e8f0;
    --muted: #7a7a9a;
    --mono: 'Space Mono', monospace;
    --sans: 'Syne', sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: var(--sans); min-height: 100vh; }

  /* GRID BG */
  body::before {
    content: '';
    position: fixed; inset: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
                      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.3;
    pointer-events: none;
    z-index: 0;
  }

  .wrapper { position: relative; z-index: 1; max-width: 1100px; margin: 0 auto; padding: 0 24px 80px; }

  /* HEADER */
  header {
    padding: 48px 0 32px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
  }
  .header-tag {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--accent);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 12px;
  }
  header h1 {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #fff 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  header p { color: var(--muted); margin-top: 10px; font-size: 15px; max-width: 560px; }

  /* TABS */
  .tabs { display: flex; gap: 4px; margin-bottom: 32px; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 4px; width: fit-content; }
  .tab {
    font-family: var(--mono); font-size: 12px; font-weight: 700;
    padding: 8px 20px; border-radius: 7px; cursor: pointer; border: none;
    background: transparent; color: var(--muted); transition: all .2s; letter-spacing: 1px; text-transform: uppercase;
  }
  .tab.active { background: var(--accent); color: #fff; }

  /* PANELS */
  .panel { display: none; }
  .panel.active { display: block; }

  /* CARDS */
  .card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; padding: 28px; margin-bottom: 20px;
  }
  .card-title {
    font-family: var(--mono); font-size: 11px; color: var(--accent2);
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px;
  }
  .card h3 { font-size: 1.15rem; font-weight: 700; margin-bottom: 10px; }

  /* THEORY */
  .concept-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  @media(max-width: 640px){ .concept-grid { grid-template-columns: 1fr; } }

  .concept-box {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 20px;
  }
  .concept-box .label {
    font-family: var(--mono); font-size: 10px; color: var(--accent3);
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;
  }
  .concept-box p { font-size: 14px; color: var(--muted); line-height: 1.6; }

  .formula-box {
    background: #0d0d1a; border: 1px solid var(--accent);
    border-radius: 10px; padding: 20px; margin: 16px 0;
    font-family: var(--mono); font-size: 14px; color: var(--accent3);
    text-align: center; letter-spacing: 1px;
  }
  .formula-box .formula-label {
    font-size: 10px; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 2px;
  }
  .formula-main { font-size: 1.2rem; color: #fff; margin: 8px 0; }

  .step-list { counter-reset: steps; list-style: none; }
  .step-list li {
    counter-increment: steps;
    padding: 12px 16px 12px 52px;
    position: relative;
    border-left: 2px solid var(--border);
    margin-left: 16px;
    margin-bottom: 8px;
    font-size: 14px;
    color: var(--muted);
    line-height: 1.6;
  }
  .step-list li::before {
    content: counter(steps);
    position: absolute; left: -16px; top: 10px;
    width: 28px; height: 28px;
    background: var(--accent); border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--mono); font-size: 11px; font-weight: 700; color: #fff;
    line-height: 28px; text-align: center;
  }
  .step-list li strong { color: var(--text); }

  /* CALCULATOR */
  .input-section { margin-bottom: 24px; }
  .input-section label {
    display: block; font-family: var(--mono); font-size: 11px;
    color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;
  }
  textarea, input[type=text], select {
    width: 100%; background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 12px 14px; color: var(--text);
    font-family: var(--mono); font-size: 13px; resize: vertical;
    transition: border-color .2s;
  }
  textarea:focus, input[type=text]:focus, select:focus {
    outline: none; border-color: var(--accent);
  }
  .hint { font-family: var(--mono); font-size: 11px; color: var(--muted); margin-top: 6px; }

  .row-inputs { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  @media(max-width:640px){ .row-inputs { grid-template-columns: 1fr; } }

  .btn {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--accent); color: #fff; border: none;
    padding: 13px 28px; border-radius: 8px; cursor: pointer;
    font-family: var(--mono); font-size: 13px; font-weight: 700;
    letter-spacing: 1px; text-transform: uppercase; transition: all .2s;
  }
  .btn:hover { background: #574ecc; transform: translateY(-1px); }
  .btn-outline {
    background: transparent; border: 1px solid var(--border); color: var(--muted);
  }
  .btn-outline:hover { border-color: var(--accent); color: var(--accent); background: transparent; transform: none; }

  /* RESULTS */
  #results { display: none; }

  .result-header {
    display: flex; align-items: center; gap: 12px; margin-bottom: 24px;
  }
  .result-badge {
    background: var(--accent3); color: #000; font-family: var(--mono);
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    padding: 4px 10px; border-radius: 4px; text-transform: uppercase;
  }

  .answer-box {
    background: #050510; border: 2px solid var(--accent3);
    border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;
  }
  .answer-box .answer-label {
    font-family: var(--mono); font-size: 10px; color: var(--accent3);
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;
  }
  .answer-box .answer-val {
    font-family: var(--mono); font-size: 1.3rem; color: #fff; line-height: 1.8;
  }

  .steps-container { display: flex; flex-direction: column; gap: 16px; }
  .step-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden;
    animation: slideIn .4s ease forwards;
    opacity: 0;
  }
  @keyframes slideIn { to { opacity: 1; transform: translateY(0); } from { transform: translateY(16px); } }

  .step-card:nth-child(1) { animation-delay: .05s; }
  .step-card:nth-child(2) { animation-delay: .1s; }
  .step-card:nth-child(3) { animation-delay: .15s; }
  .step-card:nth-child(4) { animation-delay: .2s; }
  .step-card:nth-child(5) { animation-delay: .25s; }
  .step-card:nth-child(6) { animation-delay: .3s; }
  .step-card:nth-child(7) { animation-delay: .35s; }

  .step-card-header {
    display: flex; align-items: center; gap: 14px;
    padding: 16px 20px; border-bottom: 1px solid var(--border);
  }
  .step-num {
    width: 32px; height: 32px; border-radius: 50%; background: var(--accent);
    font-family: var(--mono); font-size: 12px; font-weight: 700; color: #fff;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }
  .step-card-header h4 { font-size: 14px; font-weight: 700; }
  .step-card-header .step-tag {
    margin-left: auto; font-family: var(--mono); font-size: 9px;
    color: var(--accent2); letter-spacing: 2px; text-transform: uppercase;
  }
  .step-card-body { padding: 20px; }
  .step-card-body p { font-size: 13px; color: var(--muted); margin-bottom: 12px; line-height: 1.7; }
  .step-card-body p strong { color: var(--text); }

  .matrix-display {
    font-family: var(--mono); font-size: 12px;
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 8px; padding: 14px; overflow-x: auto;
    white-space: pre; color: var(--accent3); line-height: 1.8;
  }

  .vector-display {
    font-family: var(--mono); font-size: 13px;
    background: var(--bg); border: 1px solid var(--accent);
    border-radius: 8px; padding: 14px;
    color: #fff; line-height: 1.8;
  }

  .error-box {
    background: #1a0510; border: 1px solid var(--accent2);
    border-radius: 10px; padding: 16px 20px;
    font-family: var(--mono); font-size: 13px; color: var(--accent2);
  }

  /* EXAMPLES */
  .example-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
  .example-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px; cursor: pointer; transition: all .2s;
  }
  .example-card:hover { border-color: var(--accent); transform: translateY(-2px); }
  .example-card .ex-tag {
    font-family: var(--mono); font-size: 10px; color: var(--accent);
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;
  }
  .example-card h4 { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
  .example-card p { font-size: 12px; color: var(--muted); line-height: 1.5; }

  .pill {
    display: inline-block; background: var(--surface); border: 1px solid var(--border);
    border-radius: 20px; padding: 3px 10px;
    font-family: var(--mono); font-size: 11px; color: var(--muted); margin: 3px;
  }

  #loading { display: none; align-items: center; gap: 10px; padding: 20px 0; color: var(--muted); font-family: var(--mono); font-size: 13px; }
  .spinner { width: 18px; height: 18px; border: 2px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin .7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>
<div class="wrapper">
  <header>
    <div class="header-tag">Linear Algebra // MATH TOOL</div>
    <h1>Least Squares<br>Approximation</h1>
    <p>Understand the theory, compute solutions, and see every step — built to help you pass.</p>
  </header>

  <div class="tabs">
    <button class="tab active" onclick="switchTab('theory')">📖 Theory</button>
    <button class="tab" onclick="switchTab('calc')">🧮 Calculator</button>
    <button class="tab" onclick="switchTab('examples')">⚡ Examples</button>
  </div>

  <!-- THEORY PANEL -->
  <div class="panel active" id="panel-theory">
    <div class="card">
      <div class="card-title">01 — The Core Idea</div>
      <h3>What is Least Squares?</h3>
      <p style="color:var(--muted);font-size:14px;line-height:1.7;margin-bottom:16px;">
        When a system <strong>Ax = b</strong> has <strong>no exact solution</strong> (overdetermined — more equations than unknowns), we find the <strong>best approximate solution</strong> x̂ that minimizes the residual error ‖b − Ax‖².
        This is the foundation of linear regression and data fitting.
      </p>
      <div class="concept-grid">
        <div class="concept-box">
          <div class="label">When it's exact</div>
          <p><strong>Ax = b</strong> — Square system, consistent. The solution x satisfies every equation perfectly.</p>
        </div>
        <div class="concept-box">
          <div class="label">When least squares kicks in</div>
          <p><strong>Ax ≈ b</strong> — More equations than unknowns. No perfect solution exists, so we minimize the error.</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">02 — The Normal Equations</div>
      <h3>The Key Formula You MUST Know</h3>
      <div class="formula-box">
        <div class="formula-label">Normal Equations</div>
        <div class="formula-main">Aᵀ A x̂ = Aᵀ b</div>
        <div style="color:var(--muted);font-size:12px;margin-top:8px;">solving this gives the least squares solution x̂</div>
      </div>
      <div class="formula-box">
        <div class="formula-label">Closed Form Solution</div>
        <div class="formula-main">x̂ = (AᵀA)⁻¹ Aᵀ b</div>
        <div style="color:var(--muted);font-size:12px;margin-top:8px;">only when AᵀA is invertible (columns of A are linearly independent)</div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">03 — Step by Step Process</div>
      <h3>How to Solve Least Squares</h3>
      <ul class="step-list" style="margin-top:16px;">
        <li><strong>Set up the system:</strong> Write Ax = b where A is your coefficient matrix, b is the right-hand side. Confirm it's overdetermined (more rows than columns).</li>
        <li><strong>Compute Aᵀ (A transpose):</strong> Flip rows and columns of A. If A is m×n, then Aᵀ is n×m.</li>
        <li><strong>Multiply Aᵀ · A:</strong> This gives an n×n square matrix. This is ALWAYS square and symmetric.</li>
        <li><strong>Multiply Aᵀ · b:</strong> This gives an n×1 vector on the right-hand side of the normal equations.</li>
        <li><strong>Solve the normal system (AᵀA)x̂ = Aᵀb:</strong> This is now a square system. Use row reduction, inverse, or numpy.</li>
        <li><strong>Compute residual (optional but important):</strong> r = b − Ax̂. The norm ‖r‖ tells you the error of your approximation.</li>
        <li><strong>Verify:</strong> Aᵀr = 0 means the residual is orthogonal to the column space of A — the geometric meaning of least squares!</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-title">04 — Geometric Intuition</div>
      <h3>Why Does This Work?</h3>
      <p style="color:var(--muted);font-size:14px;line-height:1.7;margin-bottom:16px;">
        The vector <strong>b</strong> lives outside the column space of A. The least squares solution finds the <strong>projection</strong> of b onto Col(A), which is the closest point in the column space to b.
        The residual <strong>r = b − Ax̂</strong> is perpendicular (orthogonal) to Col(A).
      </p>
      <div class="concept-grid">
        <div class="concept-box">
          <div class="label">Projection Formula</div>
          <p>The projection of b onto Col(A) is <strong>p = Ax̂ = A(AᵀA)⁻¹Aᵀb</strong>. The matrix P = A(AᵀA)⁻¹Aᵀ is called the <strong>projection matrix</strong>.</p>
        </div>
        <div class="concept-box">
          <div class="label">Orthogonality Condition</div>
          <p>The key insight: <strong>Aᵀ(b − Ax̂) = 0</strong>. The error vector must be orthogonal to every column of A. This IS the normal equation.</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">05 — Quick Reference</div>
      <h3>Terms to Know for the Exam</h3>
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;">
        <span class="pill">Overdetermined system</span>
        <span class="pill">Normal equations</span>
        <span class="pill">Least squares solution x̂</span>
        <span class="pill">Residual r = b − Ax̂</span>
        <span class="pill">Projection p = Ax̂</span>
        <span class="pill">Projection matrix P</span>
        <span class="pill">‖r‖ = minimum error</span>
        <span class="pill">AᵀA invertible ↔ A has ind. cols</span>
        <span class="pill">r ⊥ Col(A)</span>
      </div>
    </div>
  </div>

  <!-- CALCULATOR PANEL -->
  <div class="panel" id="panel-calc">
    <div class="card">
      <div class="card-title">Input — Matrix A</div>
      <div class="input-section">
        <label>Matrix A — Enter rows, one per line. Separate values with spaces or commas.</label>
        <textarea id="matA" rows="5" placeholder="1 1&#10;1 2&#10;1 3&#10;1 4"></textarea>
        <div class="hint">// Example: 4 rows × 2 cols = overdetermined system</div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Input — Vector b</div>
      <div class="input-section">
        <label>Vector b — One value per line (or space-separated)</label>
        <textarea id="vecB" rows="4" placeholder="1&#10;3&#10;4&#10;6"></textarea>
      </div>
    </div>

    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:32px;">
      <button class="btn" onclick="calculate()">▶ Solve &amp; Explain</button>
      <button class="btn btn-outline" onclick="clearAll()">✕ Clear</button>
    </div>

    <div id="loading"><div class="spinner"></div> Computing...</div>
    <div id="error-display"></div>
    <div id="results"></div>
  </div>

  <!-- EXAMPLES PANEL -->
  <div class="panel" id="panel-examples">
    <div class="card">
      <div class="card-title">Quick Start Examples</div>
      <p style="color:var(--muted);font-size:14px;margin-bottom:20px;">Click any example to load it into the calculator.</p>
      <div class="example-grid">
        <div class="example-card" onclick="loadExample('fitline')">
          <div class="ex-tag">Classic</div>
          <h4>Linear Fit (4 points)</h4>
          <p>Fit a line y = c₁ + c₂x through 4 data points. The textbook least squares example.</p>
        </div>
        <div class="example-card" onclick="loadExample('overdetermined3')">
          <div class="ex-tag">3 unknowns</div>
          <h4>5×3 Overdetermined</h4>
          <p>5 equations, 3 unknowns. Find the best approximate solution via normal equations.</p>
        </div>
        <div class="example-card" onclick="loadExample('quadfit')">
          <div class="ex-tag">Quadratic</div>
          <h4>Quadratic Curve Fit</h4>
          <p>Fit y = c₁ + c₂x + c₃x² through 5 data points.</p>
        </div>
        <div class="example-card" onclick="loadExample('simple3x2')">
          <div class="ex-tag">Starter</div>
          <h4>Simple 3×2 System</h4>
          <p>The simplest non-trivial overdetermined case. Great for checking hand calculations.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const EXAMPLES = {
  fitline: {
    A: "1 1\n1 2\n1 3\n1 4",
    b: "1\n3\n4\n6"
  },
  overdetermined3: {
    A: "2 1 3\n1 0 2\n3 2 1\n0 1 4\n1 3 2",
    b: "5\n3\n7\n6\n8"
  },
  quadfit: {
    A: "1 -2 4\n1 -1 1\n1 0 0\n1 1 1\n1 2 4",
    b: "3\n1\n0\n1\n4"
  },
  simple3x2: {
    A: "1 1\n1 2\n2 1",
    b: "2\n3\n3"
  }
};

function switchTab(name) {
  document.querySelectorAll('.tab').forEach((t,i) => {
    const panels = ['theory','calc','examples'];
    t.classList.toggle('active', panels[i] === name);
  });
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
}

function loadExample(key) {
  const ex = EXAMPLES[key];
  document.getElementById('matA').value = ex.A;
  document.getElementById('vecB').value = ex.b;
  switchTab('calc');
}

function clearAll() {
  document.getElementById('matA').value = '';
  document.getElementById('vecB').value = '';
  document.getElementById('results').style.display = 'none';
  document.getElementById('error-display').innerHTML = '';
}

function parseMatrix(text) {
  return text.trim().split('\n').map(row =>
    row.trim().split(/[\s,]+/).map(Number)
  );
}

function parseVector(text) {
  return text.trim().split(/[\s\n,]+/).map(Number);
}

async function calculate() {
  const aText = document.getElementById('matA').value.trim();
  const bText = document.getElementById('vecB').value.trim();
  const errDiv = document.getElementById('error-display');
  const resultsDiv = document.getElementById('results');
  const loading = document.getElementById('loading');

  errDiv.innerHTML = '';
  resultsDiv.style.display = 'none';

  if (!aText || !bText) {
    errDiv.innerHTML = '<div class="error-box">⚠ Please enter both Matrix A and Vector b.</div>';
    return;
  }

  loading.style.display = 'flex';

  try {
    const res = await fetch('/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ A: aText, b: bText })
    });
    const data = await res.json();
    loading.style.display = 'none';

    if (data.error) {
      errDiv.innerHTML = '<div class="error-box">⚠ ' + data.error + '</div>';
      return;
    }
    renderResults(data);
  } catch(e) {
    loading.style.display = 'none';
    errDiv.innerHTML = '<div class="error-box">⚠ Request failed: ' + e.message + '</div>';
  }
}

function fmtMat(arr2d) {
  return arr2d.map(row => '  [ ' + row.map(v => String(parseFloat(v.toFixed(6))).padStart(12)).join('  ') + ' ]').join('\n');
}

function fmtVec(arr, label) {
  return arr.map((v,i) => '  ' + (label||'x') + '₍' + (i+1) + '₎ = ' + parseFloat(v.toFixed(8))).join('\n');
}

function renderResults(d) {
  const div = document.getElementById('results');
  const xSol = d.x_hat.map(v => (label,i) => `x̂₍${i+1}₎ = ${parseFloat(v.toFixed(6))} `);

  const xLines = d.x_hat.map((v,i) => `x̂<sub>${i+1}</sub> = <b>${parseFloat(v.toFixed(6))}</b>`).join('&nbsp;&nbsp;&nbsp;');
  const rNorm = parseFloat(d.residual_norm.toFixed(8));

  div.innerHTML = `
    <div class="result-header">
      <span class="result-badge">✓ Solved</span>
      <span style="font-family:var(--mono);font-size:12px;color:var(--muted);">
        A is ${d.shape[0]}×${d.shape[1]} — overdetermined
      </span>
    </div>

    <div class="answer-box">
      <div class="answer-label">Least Squares Solution x̂</div>
      <div class="answer-val">${xLines}</div>
      <div style="margin-top:12px;font-family:var(--mono);font-size:12px;color:var(--muted);">
        ‖b − Ax̂‖ = ${rNorm} &nbsp;|&nbsp; Residual norm (lower = better fit)
      </div>
    </div>

    <div class="steps-container">

      <div class="step-card">
        <div class="step-card-header">
          <div class="step-num">1</div>
          <h4>Confirm the system is overdetermined</h4>
          <span class="step-tag">Setup</span>
        </div>
        <div class="step-card-body">
          <p>Matrix A has <strong>${d.shape[0]} rows and ${d.shape[1]} columns</strong>, and vector b has <strong>${d.shape[0]} entries</strong>.</p>
          <p>Since there are <strong>more equations (${d.shape[0]}) than unknowns (${d.shape[1]})</strong>, the system Ax=b likely has no exact solution. We need least squares.</p>
          <div class="matrix-display">A =\n${fmtMat(d.A)}\n\nb =\n${d.b.map((v,i)=>'  [ '+parseFloat(v.toFixed(6))+' ]').join('\n')}</div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-card-header">
          <div class="step-num">2</div>
          <h4>Compute Aᵀ (Transpose of A)</h4>
          <span class="step-tag">Transpose</span>
        </div>
        <div class="step-card-body">
          <p>Flip rows and columns: if A is <strong>${d.shape[0]}×${d.shape[1]}</strong>, then Aᵀ is <strong>${d.shape[1]}×${d.shape[0]}</strong>.</p>
          <div class="matrix-display">Aᵀ =\n${fmtMat(d.At)}</div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-card-header">
          <div class="step-num">3</div>
          <h4>Compute AᵀA</h4>
          <span class="step-tag">Normal Matrix</span>
        </div>
        <div class="step-card-body">
          <p>Multiply Aᵀ (${d.shape[1]}×${d.shape[0]}) by A (${d.shape[0]}×${d.shape[1]}) → result is <strong>${d.shape[1]}×${d.shape[1]} square &amp; symmetric</strong>.</p>
          <p>This is always invertible if the columns of A are <strong>linearly independent</strong>.</p>
          <div class="matrix-display">AᵀA =\n${fmtMat(d.AtA)}</div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-card-header">
          <div class="step-num">4</div>
          <h4>Compute Aᵀb</h4>
          <span class="step-tag">Right-Hand Side</span>
        </div>
        <div class="step-card-body">
          <p>Multiply Aᵀ (${d.shape[1]}×${d.shape[0]}) by b (${d.shape[0]}×1) → <strong>${d.shape[1]}×1 vector</strong>. This is the RHS of the normal equations.</p>
          <div class="vector-display">${fmtVec(d.Atb, 'Aᵀb')}</div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-card-header">
          <div class="step-num">5</div>
          <h4>Solve the Normal Equations: (AᵀA)x̂ = Aᵀb</h4>
          <span class="step-tag">Core Step</span>
        </div>
        <div class="step-card-body">
          <p>Now we solve a <strong>square ${d.shape[1]}×${d.shape[1]} system</strong>. numpy uses <code>np.linalg.lstsq</code> which applies QR factorization internally — more numerically stable than computing (AᵀA)⁻¹ directly.</p>
          <p>The formula is: <strong>x̂ = (AᵀA)⁻¹Aᵀb</strong></p>
          <div class="vector-display">${fmtVec(d.x_hat, 'x̂')}</div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-card-header">
          <div class="step-num">6</div>
          <h4>Compute Residual r = b − Ax̂</h4>
          <span class="step-tag">Error Check</span>
        </div>
        <div class="step-card-body">
          <p>Plug x̂ back in. The difference <strong>r = b − Ax̂</strong> is the residual vector — the "leftover" error we couldn't eliminate.</p>
          <p>Residual norm <strong>‖r‖ = ${rNorm}</strong> — this is the minimum possible error for any x.</p>
          <div class="vector-display">${fmtVec(d.residual, 'r')}</div>
        </div>
      </div>

      <div class="step-card">
        <div class="step-card-header">
          <div class="step-num">7</div>
          <h4>Verify: r ⊥ Col(A) → Aᵀr ≈ 0</h4>
          <span class="step-tag">Geometric Check</span>
        </div>
        <div class="step-card-body">
          <p>The geometric heart of least squares: the residual <strong>r must be orthogonal to the column space of A</strong>. This means Aᵀr = 0.</p>
          <p>If these values are ≈ 0 (up to floating point), your solution is correct. ✓</p>
          <div class="vector-display">${fmtVec(d.Atr, 'Aᵀr')}</div>
          <p style="margin-top:12px;"><strong>Interpretation:</strong> ${rNorm < 1e-8 ? 'Residual norm ≈ 0 → the system had an exact solution.' : 'The residual is non-zero, confirming the system was truly overdetermined and x̂ is the best possible approximation.'}</p>
        </div>
      </div>

    </div>
  `;
  div.style.display = 'block';
}
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        A_raw = data['A']
        b_raw = data['b']

        # Parse A
        A_rows = []
        for line in A_raw.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            parts = [float(x) for x in line.replace(',', ' ').split()]
            A_rows.append(parts)

        # Validate consistent cols
        col_counts = set(len(r) for r in A_rows)
        if len(col_counts) > 1:
            return jsonify({'error': 'All rows of A must have the same number of columns.'})

        A = np.array(A_rows, dtype=float)

        # Parse b
        b_vals = [float(x) for x in b_raw.strip().replace(',', ' ').replace('\n', ' ').split()]
        b = np.array(b_vals, dtype=float)

        m, n = A.shape
        if m != len(b):
            return jsonify({'error': f'A has {m} rows but b has {len(b)} entries. They must match.'})
        if m <= n:
            return jsonify({'error': f'System is {m}×{n} — needs more rows than columns to be overdetermined. Add more rows to A (and entries to b).'})

        At = A.T
        AtA = At @ A
        Atb = At @ b

        # Solve via lstsq (numerically stable)
        x_hat, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        residual = b - A @ x_hat
        residual_norm = float(np.linalg.norm(residual))
        Atr = At @ residual  # Should be ~0

        return jsonify({
            'A': A.tolist(),
            'b': b.tolist(),
            'At': At.tolist(),
            'AtA': AtA.tolist(),
            'Atb': Atb.tolist(),
            'x_hat': x_hat.tolist(),
            'residual': residual.tolist(),
            'residual_norm': residual_norm,
            'Atr': Atr.tolist(),
            'shape': [m, n]
        })

    except ValueError as e:
        return jsonify({'error': f'Parse error: {str(e)}. Make sure all values are numbers.'})
    except np.linalg.LinAlgError as e:
        return jsonify({'error': f'Linear algebra error: {str(e)}'})
    except Exception as e:
        return jsonify({'error': str(e)})

app.run(debug=True, port=5000)