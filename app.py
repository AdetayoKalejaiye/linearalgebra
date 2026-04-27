from flask import Flask, render_template_string, request, jsonify
import numpy as np
import os

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Least Squares Lab</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:       #f9f9f7;
  --surface:  #ffffff;
  --border:   #e2e2de;
  --accent:   #2563eb;
  --danger:   #dc2626;
  --success:  #16a34a;
  --text:     #1a1a1a;
  --muted:    #6b7280;
  --code-bg:  #f3f3f0;
}

body {
  background: var(--bg);
  color: var(--text);
  font-size: 15px;
  line-height: 1.6;
}

.wrap {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 24px 80px;
}

/* ── HEADER ── */
header {
  padding: 48px 0 32px;
  border-bottom: 2px solid var(--text);
  margin-bottom: 40px;
}
.header-label {
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 10px;
}
header h1 {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.1;
}
header p {
  color: var(--muted);
  margin-top: 10px;
  font-size: 14px;
  max-width: 480px;
}

/* ── TABS ── */
.tabs {
  display: flex;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  width: fit-content;
  margin-bottom: 32px;
}
.tab {
  font-size: 13px;
  font-weight: 600;
  padding: 9px 22px;
  cursor: pointer;
  border: none;
  background: var(--surface);
  color: var(--muted);
  border-right: 1px solid var(--border);
  transition: background .15s, color .15s;
  letter-spacing: .3px;
}
.tab:last-child { border-right: none; }
.tab:hover { background: var(--bg); color: var(--text); }
.tab.active { background: var(--text); color: #fff; }

/* ── PANELS ── */
.panel { display: none; }
.panel.active { display: block; }

/* ── SECTION BLOCKS ── */
.block {
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--surface);
  padding: 28px;
  margin-bottom: 16px;
}
.block-label {
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 12px;
}
.block h3 {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 10px;
}

/* ── THEORY ELEMENTS ── */
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 14px;
}
@media(max-width:580px){ .two-col { grid-template-columns: 1fr; } }

.info-box {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
}
.info-box .ib-label {
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}
.info-box p { font-size: 13px; color: var(--muted); line-height: 1.6; }
.info-box p strong { color: var(--text); }

.formula-block {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 6px;
  padding: 16px 20px;
  margin: 14px 0;
  text-align: center;
}
.formula-block .f-label {
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 8px;
}
.formula-block .f-main {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin: 4px 0;
}
.formula-block small { font-size: 12px; color: var(--muted); }

.step-list {
  counter-reset: s;
  list-style: none;
  margin-top: 14px;
}
.step-list li {
  counter-increment: s;
  position: relative;
  padding: 10px 14px 10px 46px;
  margin-bottom: 6px;
  font-size: 14px;
  color: var(--muted);
  line-height: 1.6;
  border-radius: 6px;
  background: var(--bg);
}
.step-list li::before {
  content: counter(s);
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  height: 22px;
  background: var(--text);
  color: #fff;
  border-radius: 50%;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}
.step-list li strong { color: var(--text); }

.pill {
  display: inline-block;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 3px 11px;
  font-size: 12px;
  color: var(--muted);
  margin: 3px;
}

/* ── CALCULATOR ── */
.field { margin-bottom: 20px; }
.field label {
  display: block;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 7px;
  font-weight: 600;
}
textarea {
  width: 100%;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 7px;
  padding: 11px 14px;
  color: var(--text);
  font-size: 13px;
  resize: vertical;
  transition: border-color .2s;
  line-height: 1.7;
}
textarea:focus { outline: none; border-color: var(--accent); }
.hint { font-size: 12px; color: var(--muted); margin-top: 5px; }

.btn-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 28px; }
.btn {
  padding: 10px 24px;
  border-radius: 7px;
  border: none;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: opacity .15s, transform .1s;
}
.btn:hover { opacity: .85; transform: translateY(-1px); }
.btn-primary { background: var(--text); color: #fff; }
.btn-ghost { background: transparent; border: 1px solid var(--border); color: var(--muted); }
.btn-ghost:hover { color: var(--text); border-color: var(--text); opacity: 1; }

#loading { display: none; align-items: center; gap: 10px; padding: 16px 0; color: var(--muted); font-size: 13px; }
.spin {
  width: 18px; height: 18px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── RESULTS ── */
#results { display: none; }

.answer-block {
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 3px solid var(--success);
  border-radius: 10px;
  padding: 24px;
  margin-bottom: 20px;
  text-align: center;
}
.answer-block .a-label {
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--success);
  margin-bottom: 12px;
}
.answer-block .a-val {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 2;
}
.answer-block small { font-size: 12px; color: var(--muted); display: block; margin-top: 6px; }

.step-cards { display: flex; flex-direction: column; gap: 12px; }
.sc {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  opacity: 0;
  animation: fadeUp .35s ease forwards;
}
.sc:nth-child(1){animation-delay:.04s}.sc:nth-child(2){animation-delay:.08s}
.sc:nth-child(3){animation-delay:.12s}.sc:nth-child(4){animation-delay:.16s}
.sc:nth-child(5){animation-delay:.20s}.sc:nth-child(6){animation-delay:.24s}
.sc:nth-child(7){animation-delay:.28s}
@keyframes fadeUp { to{opacity:1;transform:none} from{transform:translateY(10px)} }

.sc-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 18px;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}
.sc-num {
  width: 26px; height: 26px;
  background: var(--text); color: #fff;
  border-radius: 50%;
  font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.sc-head h4 { font-size: 14px; font-weight: 700; }
.sc-tag {
  margin-left: auto;
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--muted);
}

.sc-body { padding: 18px; }
.sc-body p { font-size: 13px; color: var(--muted); margin-bottom: 10px; line-height: 1.7; }
.sc-body p strong { color: var(--text); }

.mat-out {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 12px 14px;
  overflow-x: auto;
  white-space: pre;
  font-size: 12px;
  line-height: 1.9;
  color: var(--text);
}
.vec-out {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 6px;
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.9;
  white-space: pre;
  color: var(--text);
}

.err-box {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 13px 16px;
  font-size: 13px;
  color: var(--danger);
  margin-bottom: 16px;
}

/* ── EXAMPLES ── */
.ex-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}
.ex-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px;
  cursor: pointer;
  transition: border-color .15s, transform .15s;
}
.ex-card:hover { border-color: var(--text); transform: translateY(-2px); }
.ex-card .et {
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}
.ex-card h4 { font-size: 14px; font-weight: 700; margin-bottom: 5px; }
.ex-card p { font-size: 12px; color: var(--muted); line-height: 1.5; }
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="header-label">Linear Algebra &mdash; Study Tool</div>
    <h1>Least Squares<br>Approximation</h1>
    <p>Theory, step-by-step calculations, and instant examples. Built to help you pass.</p>
  </header>

  <div class="tabs">
    <button class="tab active" onclick="switchTab('theory')">Theory</button>
    <button class="tab" onclick="switchTab('calc')">Calculator</button>
    <button class="tab" onclick="switchTab('examples')">Examples</button>
  </div>

  <!-- ══ THEORY ══ -->
  <div class="panel active" id="panel-theory">

    <div class="block">
      <div class="block-label">01 &mdash; The Core Idea</div>
      <h3>What is Least Squares?</h3>
      <p style="font-size:14px;color:var(--muted);line-height:1.7;margin-bottom:14px">
        When <strong style="color:var(--text)">Ax&nbsp;=&nbsp;b</strong> has <strong style="color:var(--text)">no exact solution</strong>
        (overdetermined &mdash; more equations than unknowns), we find the
        <strong style="color:var(--text)">best approximate solution x&#x0302;</strong> that minimises
        the total squared error &lVert;b&nbsp;&minus;&nbsp;Ax&rVert;&sup2;. This is the backbone of linear regression.
      </p>
      <div class="two-col">
        <div class="info-box">
          <div class="ib-label">Exact system</div>
          <p><strong>Ax = b</strong> &mdash; square &amp; consistent. x satisfies every equation perfectly.</p>
        </div>
        <div class="info-box">
          <div class="ib-label">Overdetermined (use least squares)</div>
          <p><strong>Ax &asymp; b</strong> &mdash; more rows than columns. No perfect x exists, so we minimise the error.</p>
        </div>
      </div>
    </div>

    <div class="block">
      <div class="block-label">02 &mdash; The Normal Equations</div>
      <h3>The Formula You Must Know</h3>
      <div class="formula-block">
        <div class="f-label">Normal Equations</div>
        <div class="f-main">A&sup1; A x&#x0302; = A&sup1; b</div>
        <small>solving this gives the least squares solution x&#x0302;</small>
      </div>
      <div class="formula-block">
        <div class="f-label">Closed-Form Solution</div>
        <div class="f-main">x&#x0302; = (A&sup1;A)&minus;&sup1; A&sup1; b</div>
        <small>valid when A&sup1;A is invertible &mdash; i.e. columns of A are linearly independent</small>
      </div>
    </div>

    <div class="block">
      <div class="block-label">03 &mdash; Step-by-Step Process</div>
      <h3>How to Solve Least Squares</h3>
      <ul class="step-list">
        <li><strong>Write Ax = b.</strong> Confirm overdetermined: more rows than columns.</li>
        <li><strong>Compute A&sup1; (transpose).</strong> If A is m&times;n, then A&sup1; is n&times;m &mdash; flip rows and columns.</li>
        <li><strong>Multiply A&sup1;&middot;A.</strong> Always gives an n&times;n square, symmetric matrix.</li>
        <li><strong>Multiply A&sup1;&middot;b.</strong> Gives an n&times;1 vector &mdash; the right-hand side of the normal equations.</li>
        <li><strong>Solve (A&sup1;A)x&#x0302; = A&sup1;b.</strong> Now it&apos;s a square system. Row reduce or invert.</li>
        <li><strong>Compute residual r = b &minus; Ax&#x0302;.</strong> &lVert;r&rVert; is the minimum achievable error.</li>
        <li><strong>Verify: A&sup1;r &asymp; 0.</strong> Residual must be orthogonal to Col(A). Confirms correctness.</li>
      </ul>
    </div>

    <div class="block">
      <div class="block-label">04 &mdash; Geometric Intuition</div>
      <h3>Why Does This Work?</h3>
      <p style="font-size:14px;color:var(--muted);line-height:1.7;margin-bottom:14px">
        Vector <strong style="color:var(--text)">b</strong> lives outside the column space of A.
        Least squares finds the <strong style="color:var(--text)">projection of b onto Col(A)</strong> &mdash;
        the closest point inside Col(A) to b.
        The residual <strong style="color:var(--text)">r = b &minus; Ax&#x0302;</strong> is perpendicular to every column of A.
      </p>
      <div class="two-col">
        <div class="info-box">
          <div class="ib-label">Projection Formula</div>
          <p>Projection: <strong>p = A(A&sup1;A)&minus;&sup1;A&sup1;b</strong><br>
          Projection matrix: <strong>P = A(A&sup1;A)&minus;&sup1;A&sup1;</strong></p>
        </div>
        <div class="info-box">
          <div class="ib-label">Orthogonality Condition</div>
          <p><strong>A&sup1;(b &minus; Ax&#x0302;) = 0</strong><br>
          The error is orthogonal to every column of A. This is the normal equation rearranged.</p>
        </div>
      </div>
    </div>

    <div class="block">
      <div class="block-label">05 &mdash; Exam Vocabulary</div>
      <h3>Terms to Know</h3>
      <div style="margin-top:10px">
        <span class="pill">Overdetermined system</span>
        <span class="pill">Normal equations</span>
        <span class="pill">Least squares solution x&#x0302;</span>
        <span class="pill">Residual r = b &minus; Ax&#x0302;</span>
        <span class="pill">Projection p = Ax&#x0302;</span>
        <span class="pill">Projection matrix P</span>
        <span class="pill">&lVert;r&rVert; = minimum error</span>
        <span class="pill">r &perp; Col(A)</span>
        <span class="pill">A&sup1;A invertible &hArr; ind. columns</span>
      </div>
    </div>

  </div>

  <!-- ══ CALCULATOR ══ -->
  <div class="panel" id="panel-calc">

    <div class="block">
      <div class="block-label">Matrix A</div>
      <div class="field">
        <label>Enter rows &mdash; one per line, values separated by spaces</label>
        <textarea id="matA" rows="5" placeholder="1 1&#10;1 2&#10;1 3&#10;1 4"></textarea>
        <div class="hint">Example above: 4&times;2 matrix &mdash; 4 equations, 2 unknowns</div>
      </div>
    </div>

    <div class="block">
      <div class="block-label">Vector b</div>
      <div class="field">
        <label>Enter values &mdash; one per line (must match the number of rows in A)</label>
        <textarea id="vecB" rows="4" placeholder="1&#10;3&#10;4&#10;6"></textarea>
      </div>
    </div>

    <div class="btn-row">
      <button class="btn btn-primary" onclick="calculate()">Solve &amp; Explain</button>
      <button class="btn btn-ghost" onclick="clearAll()">Clear</button>
    </div>

    <div id="loading"><div class="spin"></div>Computing&hellip;</div>
    <div id="err-display"></div>
    <div id="results"></div>

  </div>

  <!-- ══ EXAMPLES ══ -->
  <div class="panel" id="panel-examples">

    <div class="block">
      <div class="block-label">Quick-Load Examples</div>
      <p style="font-size:14px;color:var(--muted);margin-bottom:18px">Click any card to load it straight into the Calculator.</p>
      <div class="ex-grid">

        <div class="ex-card" onclick="loadEx('fitline')">
          <div class="et">Classic</div>
          <h4>Linear Fit &mdash; 4 points</h4>
          <p>Fit y = c&#x2081; + c&#x2082;x through 4 data points. The textbook example.</p>
        </div>

        <div class="ex-card" onclick="loadEx('simple3x2')">
          <div class="et">Starter</div>
          <h4>Simple 3&times;2 System</h4>
          <p>The simplest overdetermined case. Great for checking hand calculations.</p>
        </div>

        <div class="ex-card" onclick="loadEx('overdetermined3')">
          <div class="et">3 Unknowns</div>
          <h4>5&times;3 System</h4>
          <p>5 equations, 3 unknowns. Shows how normal equations scale up.</p>
        </div>

        <div class="ex-card" onclick="loadEx('quadfit')">
          <div class="et">Quadratic</div>
          <h4>Quadratic Curve Fit</h4>
          <p>Fit y = c&#x2081; + c&#x2082;x + c&#x2083;x&sup2; through 5 data points.</p>
        </div>

      </div>
    </div>

    <div class="block">
      <div class="block-label">How to Read the Results</div>
      <ul class="step-list" style="margin-top:4px">
        <li><strong>x&#x0302; values</strong> &mdash; your least squares solution. Plug back in to check.</li>
        <li><strong>Residual r</strong> &mdash; how far off each equation is. Smaller = better fit.</li>
        <li><strong>&lVert;r&rVert; (residual norm)</strong> &mdash; total error as one number. Zero means an exact solution existed.</li>
        <li><strong>A&sup1;r &asymp; 0</strong> &mdash; orthogonality check. Near zero confirms your solution is correct.</li>
      </ul>
    </div>

  </div>

</div><!-- /wrap -->

<script>
var EXAMPLES = {
  fitline:        { A:"1 1\n1 2\n1 3\n1 4",                  b:"1\n3\n4\n6" },
  simple3x2:      { A:"1 1\n1 2\n2 1",                        b:"2\n3\n3" },
  overdetermined3:{ A:"2 1 3\n1 0 2\n3 2 1\n0 1 4\n1 3 2",   b:"5\n3\n7\n6\n8" },
  quadfit:        { A:"1 -2 4\n1 -1 1\n1 0 0\n1 1 1\n1 2 4",  b:"3\n1\n0\n1\n4" }
};

function switchTab(name) {
  var names = ['theory','calc','examples'];
  document.querySelectorAll('.tab').forEach(function(t,i){
    t.classList.toggle('active', names[i] === name);
  });
  document.querySelectorAll('.panel').forEach(function(p){
    p.classList.remove('active');
  });
  document.getElementById('panel-'+name).classList.add('active');
}

function loadEx(key) {
  var ex = EXAMPLES[key];
  document.getElementById('matA').value = ex.A;
  document.getElementById('vecB').value = ex.b;
  switchTab('calc');
}

function clearAll() {
  document.getElementById('matA').value = '';
  document.getElementById('vecB').value = '';
  document.getElementById('results').style.display = 'none';
  document.getElementById('err-display').innerHTML = '';
}

function fmt(v){ return parseFloat(v.toFixed(8)).toString(); }

function fmtMat(arr){
  return arr.map(function(row){
    return '  [ ' + row.map(function(v){ return fmt(v).padStart(12); }).join('  ') + ' ]';
  }).join('\n');
}

function fmtVec(arr, sym){
  return arr.map(function(v,i){
    return '  ' + sym + '[' + (i+1) + '] = ' + fmt(v);
  }).join('\n');
}

async function calculate() {
  var aText   = document.getElementById('matA').value.trim();
  var bText   = document.getElementById('vecB').value.trim();
  var errDiv  = document.getElementById('err-display');
  var resDiv  = document.getElementById('results');
  var loading = document.getElementById('loading');

  errDiv.innerHTML = '';
  resDiv.style.display = 'none';

  if (!aText || !bText) {
    errDiv.innerHTML = '<div class="err-box">Please fill in both Matrix A and Vector b.</div>';
    return;
  }

  loading.style.display = 'flex';

  try {
    var resp = await fetch('/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ A: aText, b: bText })
    });
    var data = await resp.json();
    loading.style.display = 'none';
    if (data.error) {
      errDiv.innerHTML = '<div class="err-box">' + data.error + '</div>';
      return;
    }
    renderResults(data);
  } catch(e) {
    loading.style.display = 'none';
    errDiv.innerHTML = '<div class="err-box">Request failed: ' + e.message + '</div>';
  }
}

function sc(num, title, tag, body) {
  return '<div class="sc">' +
    '<div class="sc-head"><div class="sc-num">'+num+'</div><h4>'+title+'</h4><span class="sc-tag">'+tag+'</span></div>' +
    '<div class="sc-body">'+body+'</div>' +
  '</div>';
}

function renderResults(d) {
  var div = document.getElementById('results');
  var m = d.shape[0], n = d.shape[1];
  var rn = parseFloat(d.residual_norm.toFixed(8));

  var xHTML = d.x_hat.map(function(v,i){
    return 'x&#x0302;<sub>'+(i+1)+'</sub>&nbsp;=&nbsp;<strong>'+fmt(v)+'</strong>';
  }).join('&emsp;');

  var verdict = rn < 1e-8
    ? 'Residual &asymp; 0 &rarr; the system had an exact solution.'
    : 'Non-zero residual confirms the system was overdetermined. x&#x0302; is the best possible approximation.';

  div.innerHTML =
    '<div class="answer-block">' +
      '<div class="a-label">Least Squares Solution x&#x0302;</div>' +
      '<div class="a-val">'+xHTML+'</div>' +
      '<small>&lVert;b &minus; Ax&#x0302;&rVert; = '+rn+'&emsp;Residual norm (lower = better fit)</small>' +
    '</div>' +

    '<div class="step-cards">' +

    sc(1,'Confirm overdetermined system','Setup',
      '<p>A has <strong>'+m+' rows</strong> and <strong>'+n+' columns</strong>. ' +
      'Since '+m+' &gt; '+n+', there are more equations than unknowns &mdash; least squares is required.</p>' +
      '<pre class="mat-out">A =\n'+fmtMat(d.A)+'\n\nb =\n'+d.b.map(function(v){return '  [ '+fmt(v)+' ]';}).join('\n')+'</pre>') +

    sc(2,'Compute A&sup1; (transpose)','Transpose',
      '<p>Flip rows &amp; columns. A is <strong>'+m+'&times;'+n+'</strong>, so A&sup1; is <strong>'+n+'&times;'+m+'</strong>.</p>' +
      '<pre class="mat-out">A&sup1; =\n'+fmtMat(d.At)+'</pre>') +

    sc(3,'Compute A&sup1;A','Normal Matrix',
      '<p>Multiply A&sup1; ('+n+'&times;'+m+') by A ('+m+'&times;'+n+') &rarr; a <strong>'+n+'&times;'+n+' square, symmetric</strong> matrix. ' +
      'Invertible when columns of A are linearly independent.</p>' +
      '<pre class="mat-out">A&sup1;A =\n'+fmtMat(d.AtA)+'</pre>') +

    sc(4,'Compute A&sup1;b','RHS Vector',
      '<p>Multiply A&sup1; ('+n+'&times;'+m+') by b ('+m+'&times;1) &rarr; a <strong>'+n+'&times;1 vector</strong>. ' +
      'This is the right-hand side of the normal equations.</p>' +
      '<pre class="vec-out">'+fmtVec(d.Atb,'A\u00B9b')+'</pre>') +

    sc(5,'Solve (A&sup1;A)x&#x0302; = A&sup1;b','Core Step',
      '<p>Now a <strong>square '+n+'&times;'+n+' system</strong>. ' +
      'NumPy uses <code>np.linalg.lstsq</code> (QR factorisation &mdash; more stable than inverting A&sup1;A directly).</p>' +
      '<p>Formula: <strong>x&#x0302; = (A&sup1;A)&minus;&sup1; A&sup1;b</strong></p>' +
      '<pre class="vec-out">'+fmtVec(d.x_hat,'x\u0302')+'</pre>') +

    sc(6,'Compute residual r = b &minus; Ax&#x0302;','Error Check',
      '<p>Plug x&#x0302; back in. The difference <strong>r = b &minus; Ax&#x0302;</strong> is the remaining error we cannot eliminate.</p>' +
      '<p>Residual norm <strong>&lVert;r&rVert; = '+rn+'</strong> &mdash; the minimum possible error for any x.</p>' +
      '<pre class="vec-out">'+fmtVec(d.residual,'r')+'</pre>') +

    sc(7,'Verify A&sup1;r &asymp; 0 (orthogonality check)','Geometric Check',
      '<p>Key theorem: <strong>r must be orthogonal to Col(A)</strong>, meaning A&sup1;r = 0. ' +
      'Values near zero confirm the solution is correct.</p>' +
      '<pre class="vec-out">'+fmtVec(d.Atr,'A\u00B9r')+'</pre>' +
      '<p style="margin-top:12px"><strong>'+verdict+'</strong></p>') +

    '</div>';

  div.style.display = 'block';
}
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        A_raw = data['A']
        b_raw = data['b']

        A_rows = []
        for line in A_raw.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            parts = [float(x) for x in line.replace(',', ' ').split()]
            A_rows.append(parts)

        col_counts = set(len(r) for r in A_rows)
        if len(col_counts) > 1:
            return jsonify({'error': 'All rows of A must have the same number of columns.'})

        A = np.array(A_rows, dtype=float)
        b_vals = [float(x) for x in b_raw.strip().replace(',', ' ').replace('\n', ' ').split()]
        b = np.array(b_vals, dtype=float)

        m, n = A.shape

        if m != len(b):
            return jsonify({'error': f'A has {m} rows but b has {len(b)} entries — they must match.'})
        if m <= n:
            return jsonify({'error': f'System is {m}x{n}. Need more rows than columns (overdetermined). Add more equations.'})

        At  = A.T
        AtA = At @ A
        Atb = At @ b

        x_hat, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        residual      = b - A @ x_hat
        residual_norm = float(np.linalg.norm(residual))
        Atr           = At @ residual

        return jsonify({
            'A': A.tolist(), 'b': b.tolist(),
            'At': At.tolist(), 'AtA': AtA.tolist(), 'Atb': Atb.tolist(),
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
