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
  :root {
    --bg: #ffffff;
    --surface: #111118;
    --card: #16161f;
    --border: #2a2a3a;
    --accent: #6c63ff;
    --accent2: #ff6584;
    --accent3: #43e97b;
    --text: #e8e8f0;
    --muted: #000000;

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


.tabs{display:flex;gap:4px;background:var(--surface);border:1px solid var(--border);
  border-radius:10px;padding:4px;width:fit-content;margin-bottom:28px}
.tab{font-family:monospace;font-size:12px;font-weight:700;padding:9px 22px;border-radius:7px;
  cursor:pointer;border:none;background:transparent;color:var(--muted);
  transition:all .2s;letter-spacing:1px;text-transform:uppercase}
.tab.active{background:var(--accent);color:#fff}

.panel{display:none}.panel.active{display:block}

.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:26px;margin-bottom:18px}
.card-title{font-family:monospace;font-size:10px;color:var(--accent2);
  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px}
.card h3{font-size:1.1rem;font-weight:700;margin-bottom:10px}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:600px){.grid2{grid-template-columns:1fr}}
.box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px}
.box .lbl{font-family:monospace;font-size:10px;color:var(--accent3);
  letter-spacing:2px;text-transform:uppercase;margin-bottom:7px}
.box p{font-size:13px;color:var(--muted);line-height:1.6}

.formula{background:#0d0d1a;border:1px solid var(--accent);border-radius:10px;
  padding:18px;margin:14px 0;font-family:monospace;text-align:center}
.formula .fl{font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px}
.formula .fm{font-size:1.15rem;color:#fff;margin:6px 0}
.formula small{font-size:11px;color:var(--muted)}

.steps{counter-reset:s;list-style:none}
.steps li{counter-increment:s;padding:11px 14px 11px 50px;position:relative;
  border-left:2px solid var(--border);margin-left:14px;margin-bottom:7px;
  font-size:13px;color:var(--muted);line-height:1.6}
.steps li::before{content:counter(s);position:absolute;left:-14px;top:9px;
  width:26px;height:26px;background:var(--accent);border-radius:50%;
  font-family:monospace;font-size:11px;font-weight:700;color:#fff;
  display:flex;align-items:center;justify-content:center;line-height:26px;text-align:center}
.steps li strong{color:var(--text)}

.pill{display:inline-block;background:var(--surface);border:1px solid var(--border);
  border-radius:20px;padding:3px 10px;font-family:monospace;font-size:11px;color:var(--muted);margin:3px}

label.lbl2{display:block;font-family:monospace;font-size:10px;color:var(--muted);
  letter-spacing:2px;text-transform:uppercase;margin-bottom:7px}
textarea{width:100%;background:var(--surface);border:1px solid var(--border);
  border-radius:8px;padding:11px 13px;color:var(--text);font-family:monospace;
  font-size:13px;resize:vertical;transition:border-color .2s}
textarea:focus{outline:none;border-color:var(--accent)}
.hint{font-family:monospace;font-size:11px;color:var(--muted);margin-top:5px}
.isec{margin-bottom:22px}

.btn{display:inline-flex;align-items:center;gap:7px;background:var(--accent);color:#fff;
  border:none;padding:12px 26px;border-radius:8px;cursor:pointer;
  font-family:monospace;font-size:12px;font-weight:700;letter-spacing:1px;
  text-transform:uppercase;transition:all .2s}
.btn:hover{background:#574ecc;transform:translateY(-1px)}
.btn.out{background:transparent;border:1px solid var(--border);color:var(--muted)}
.btn.out:hover{border-color:var(--accent);color:var(--accent);transform:none}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:28px}

#loading{display:none;align-items:center;gap:10px;padding:18px 0;
  color:var(--muted);font-family:monospace;font-size:13px}
.spin{width:18px;height:18px;border:2px solid var(--border);
  border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

#results{display:none}
.rbadge{background:var(--accent3);color:#000;font-family:monospace;
  font-size:10px;font-weight:700;letter-spacing:2px;padding:4px 10px;
  border-radius:4px;text-transform:uppercase}
.rhead{display:flex;align-items:center;gap:12px;margin-bottom:22px}

.abox{background:#050510;border:2px solid var(--accent3);border-radius:12px;
  padding:22px;margin-bottom:22px;text-align:center}
.abox .al{font-family:monospace;font-size:10px;color:var(--accent3);
  letter-spacing:3px;text-transform:uppercase;margin-bottom:10px}
.abox .av{font-family:monospace;font-size:1.2rem;color:#fff;line-height:1.9}
.abox small{font-family:monospace;font-size:11px;color:var(--muted);margin-top:10px;display:block}

.scon{display:flex;flex-direction:column;gap:14px}
.sc{background:var(--surface);border:1px solid var(--border);border-radius:12px;
  overflow:hidden;opacity:0;animation:si .4s ease forwards}
@keyframes si{to{opacity:1;transform:translateY(0)}from{transform:translateY(14px)}}
.sc:nth-child(1){animation-delay:.05s}.sc:nth-child(2){animation-delay:.1s}
.sc:nth-child(3){animation-delay:.15s}.sc:nth-child(4){animation-delay:.2s}
.sc:nth-child(5){animation-delay:.25s}.sc:nth-child(6){animation-delay:.3s}
.sc:nth-child(7){animation-delay:.35s}

.sch{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--border)}
.sn{width:30px;height:30px;border-radius:50%;background:var(--accent);
  font-family:monospace;font-size:11px;font-weight:700;color:#fff;
  display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sch h4{font-size:14px;font-weight:700}
.stag{margin-left:auto;font-family:monospace;font-size:9px;color:var(--accent2);letter-spacing:2px;text-transform:uppercase}

.scb{padding:18px}
.scb p{font-size:13px;color:var(--muted);margin-bottom:10px;line-height:1.7}
.scb p strong{color:var(--text)}
.mat{font-family:monospace;font-size:12px;background:var(--bg);
  border:1px solid var(--border);border-radius:8px;padding:12px;
  overflow-x:auto;white-space:pre;color:var(--accent3);line-height:1.8}
.vec{font-family:monospace;font-size:13px;background:var(--bg);
  border:1px solid var(--accent);border-radius:8px;padding:12px;color:#fff;line-height:1.8}

.err{background:#1a0510;border:1px solid var(--accent2);border-radius:10px;
  padding:14px 18px;font-family:monospace;font-size:13px;color:var(--accent2);margin-bottom:16px}

.egrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.ec{background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:18px;cursor:pointer;transition:all .2s}
.ec:hover{border-color:var(--accent);transform:translateY(-2px)}
.ec .et{font-family:monospace;font-size:10px;color:var(--accent);
  letter-spacing:2px;text-transform:uppercase;margin-bottom:7px}
.ec h4{font-size:14px;font-weight:700;margin-bottom:5px}
.ec p{font-size:12px;color:var(--muted);line-height:1.5}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="tag">Linear Algebra // Study Tool</div>
    <h1>Least Squares<br>Approximation</h1>
    <p>Theory, calculations, and full step-by-step breakdowns &mdash; built to help you pass.</p>
  </header>

  <div class="tabs">
    <button class="tab active" onclick="switchTab('theory')">&#128214; Theory</button>
    <button class="tab" onclick="switchTab('calc')">&#9998; Calculator</button>
    <button class="tab" onclick="switchTab('examples')">&#9889; Examples</button>
  </div>

  <!-- THEORY -->
  <div class="panel active" id="panel-theory">

    <div class="card">
      <div class="card-title">01 &mdash; The Core Idea</div>
      <h3>What is Least Squares?</h3>
      <p style="color:var(--muted);font-size:14px;line-height:1.7;margin-bottom:14px">
        When <strong>Ax = b</strong> has <strong>no exact solution</strong> (overdetermined &mdash; more equations than unknowns),
        we find the <strong>best approximate solution x&#x0302;</strong> that minimizes the total squared error &#x2016;b &#x2212; Ax&#x2016;&sup2;.
        This is the foundation of linear regression and data fitting.
      </p>
      <div class="grid2">
        <div class="box">
          <div class="lbl">Exact system</div>
          <p><strong>Ax = b</strong> &mdash; square &amp; consistent. x satisfies every equation perfectly.</p>
        </div>
        <div class="box">
          <div class="lbl">Overdetermined (use least squares)</div>
          <p><strong>Ax &asymp; b</strong> &mdash; more rows than columns. No perfect solution, so we minimize error.</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">02 &mdash; The Normal Equations</div>
      <h3>The Formula You MUST Know</h3>
      <div class="formula">
        <div class="fl">Normal Equations</div>
        <div class="fm">A&sup1; A x&#x0302; = A&sup1; b</div>
        <small>solving this gives the least squares solution x&#x0302;</small>
      </div>
      <div class="formula">
        <div class="fl">Closed-Form Solution</div>
        <div class="fm">x&#x0302; = (A&sup1;A)&#x207B;&#xB9; A&sup1; b</div>
        <small>valid when A&sup1;A is invertible (columns of A are linearly independent)</small>
      </div>
    </div>

    <div class="card">
      <div class="card-title">03 &mdash; Step-by-Step Process</div>
      <h3>How to Solve Least Squares</h3>
      <ul class="steps" style="margin-top:14px">
        <li><strong>Write Ax = b.</strong> Confirm overdetermined: more rows than columns.</li>
        <li><strong>Compute A&sup1; (transpose).</strong> If A is m&times;n, then A&sup1; is n&times;m. Flip rows and columns.</li>
        <li><strong>Multiply A&sup1; &middot; A.</strong> Always gives an n&times;n square, symmetric matrix.</li>
        <li><strong>Multiply A&sup1; &middot; b.</strong> Gives an n&times;1 vector (RHS of normal equations).</li>
        <li><strong>Solve (A&sup1;A)x&#x0302; = A&sup1;b.</strong> Now it&apos;s a square system. Row reduce or invert.</li>
        <li><strong>Compute residual r = b &minus; Ax&#x0302;.</strong> &#x2016;r&#x2016; is the minimum achievable error.</li>
        <li><strong>Verify: A&sup1;r &asymp; 0.</strong> Residual must be orthogonal to Col(A). This confirms correctness.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-title">04 &mdash; Geometric Intuition</div>
      <h3>Why Does This Work?</h3>
      <p style="color:var(--muted);font-size:14px;line-height:1.7;margin-bottom:14px">
        Vector <strong>b</strong> lives outside the column space of A. Least squares finds the
        <strong>projection of b onto Col(A)</strong> &mdash; the closest point in the column space to b.
        The residual <strong>r = b &minus; Ax&#x0302;</strong> is perpendicular (orthogonal) to every column of A.
      </p>
      <div class="grid2">
        <div class="box">
          <div class="lbl">Projection Formula</div>
          <p>Projection: <strong>p = Ax&#x0302; = A(A&sup1;A)&#x207B;&#xB9;A&sup1;b</strong><br>
          Projection matrix: <strong>P = A(A&sup1;A)&#x207B;&#xB9;A&sup1;</strong></p>
        </div>
        <div class="box">
          <div class="lbl">Orthogonality Condition</div>
          <p><strong>A&sup1;(b &minus; Ax&#x0302;) = 0</strong><br>
          The error is orthogonal to every column of A. This IS the normal equation rearranged.</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">05 &mdash; Exam Vocab</div>
      <h3>Terms to Know</h3>
      <div style="margin-top:10px">
        <span class="pill">Overdetermined system</span>
        <span class="pill">Normal equations</span>
        <span class="pill">Least squares solution x&#x0302;</span>
        <span class="pill">Residual r = b &minus; Ax&#x0302;</span>
        <span class="pill">Projection p = Ax&#x0302;</span>
        <span class="pill">Projection matrix P</span>
        <span class="pill">&#x2016;r&#x2016; = minimum error</span>
        <span class="pill">r &perp; Col(A)</span>
        <span class="pill">A&sup1;A invertible &hArr; ind. columns</span>
      </div>
    </div>

  </div>

  <!-- CALCULATOR -->
  <div class="panel" id="panel-calc">

    <div class="card">
      <div class="card-title">Matrix A</div>
      <div class="isec">
        <label class="lbl2">Enter rows of A &mdash; one per line, values separated by spaces</label>
        <textarea id="matA" rows="5" placeholder="1 1&#10;1 2&#10;1 3&#10;1 4"></textarea>
        <div class="hint">// Example: 4&times;2 matrix &mdash; 4 equations, 2 unknowns</div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Vector b</div>
      <div class="isec">
        <label class="lbl2">Enter values of b &mdash; one per line (must match rows in A)</label>
        <textarea id="vecB" rows="4" placeholder="1&#10;3&#10;4&#10;6"></textarea>
      </div>
    </div>

    <div class="btns">
      <button class="btn" onclick="calculate()">&#9654; Solve &amp; Explain</button>
      <button class="btn out" onclick="clearAll()">&#x2715; Clear</button>
    </div>

    <div id="loading"><div class="spin"></div>Computing&hellip;</div>
    <div id="err-display"></div>
    <div id="results"></div>

  </div>

  <!-- EXAMPLES -->
  <div class="panel" id="panel-examples">

    <div class="card">
      <div class="card-title">Quick-Load Examples</div>
      <p style="color:var(--muted);font-size:14px;margin-bottom:18px">Click any card to load it into the Calculator.</p>
      <div class="egrid">

        <div class="ec" onclick="loadEx('fitline')">
          <div class="et">Classic</div>
          <h4>Linear Fit &mdash; 4 points</h4>
          <p>Fit y = c&sub1; + c&sub2;x through 4 data points. The textbook example.</p>
        </div>

        <div class="ec" onclick="loadEx('simple3x2')">
          <div class="et">Starter</div>
          <h4>Simple 3&times;2 System</h4>
          <p>The simplest overdetermined case. Great for checking hand calculations.</p>
        </div>

        <div class="ec" onclick="loadEx('overdetermined3')">
          <div class="et">3 Unknowns</div>
          <h4>5&times;3 Overdetermined</h4>
          <p>5 equations, 3 unknowns. Shows how normal equations scale up.</p>
        </div>

        <div class="ec" onclick="loadEx('quadfit')">
          <div class="et">Quadratic</div>
          <h4>Quadratic Curve Fit</h4>
          <p>Fit y = c&sub1; + c&sub2;x + c&sub3;x&sup2; through 5 data points.</p>
        </div>

      </div>
    </div>

    <div class="card">
      <div class="card-title">How to Read the Results</div>
      <ul class="steps" style="margin-top:12px">
        <li><strong>x&#x0302; values</strong> &mdash; your least squares solution. Plug back in to check.</li>
        <li><strong>Residual r</strong> &mdash; how far off each equation is. Smaller = better fit.</li>
        <li><strong>&#x2016;r&#x2016; (residual norm)</strong> &mdash; total error as one number. Zero = exact solution existed.</li>
        <li><strong>A&sup1;r &asymp; 0</strong> &mdash; orthogonality check. Near zero means your solution is correct.</li>
      </ul>
    </div>

  </div>

</div>

<script>
var EXAMPLES = {
  fitline:        { A:"1 1\n1 2\n1 3\n1 4",                 b:"1\n3\n4\n6" },
  simple3x2:      { A:"1 1\n1 2\n2 1",                       b:"2\n3\n3" },
  overdetermined3:{ A:"2 1 3\n1 0 2\n3 2 1\n0 1 4\n1 3 2",  b:"5\n3\n7\n6\n8" },
  quadfit:        { A:"1 -2 4\n1 -1 1\n1 0 0\n1 1 1\n1 2 4", b:"3\n1\n0\n1\n4" }
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
    errDiv.innerHTML = '<div class="err">&#9888; Please fill in both Matrix A and Vector b.</div>';
    return;
  }

  loading.style.display = 'flex';

  try {
    var resp = await fetch('/solve', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({A:aText, b:bText})
    });
    var data = await resp.json();
    loading.style.display = 'none';
    if (data.error) {
      errDiv.innerHTML = '<div class="err">&#9888; ' + data.error + '</div>';
      return;
    }
    renderResults(data);
  } catch(e) {
    loading.style.display = 'none';
    errDiv.innerHTML = '<div class="err">&#9888; Request failed: ' + e.message + '</div>';
  }
}

function step(num, title, tag, body){
  return '<div class="sc">' +
    '<div class="sch"><div class="sn">'+num+'</div><h4>'+title+'</h4><span class="stag">'+tag+'</span></div>' +
    '<div class="scb">'+body+'</div>' +
  '</div>';
}

function renderResults(d){
  var div = document.getElementById('results');
  var m = d.shape[0], n = d.shape[1];
  var rn = parseFloat(d.residual_norm.toFixed(8));

  var xHTML = d.x_hat.map(function(v,i){
    return 'x&#x0302;<sub>'+(i+1)+'</sub> = <strong>'+fmt(v)+'</strong>';
  }).join('&nbsp;&nbsp;&nbsp;');

  var exact = rn < 1e-8
    ? 'Residual &asymp; 0 &rarr; the system had an exact solution!'
    : 'Non-zero residual confirms this was overdetermined. x&#x0302; is the best possible approximation.';

  div.innerHTML =
    '<div class="rhead"><span class="rbadge">&#10003; Solved</span>' +
    '<span style="font-family:monospace;font-size:12px;color:var(--muted)">A is '+m+'&times;'+n+' &mdash; overdetermined</span></div>' +

    '<div class="abox"><div class="al">Least Squares Solution x&#x0302;</div>' +
    '<div class="av">'+xHTML+'</div>' +
    '<small>&#x2016;b &minus; Ax&#x0302;&#x2016; = '+rn+' &nbsp;|&nbsp; Residual norm (lower = better fit)</small></div>' +

    '<div class="scon">' +

    step(1,'Confirm overdetermined system','Setup',
      '<p>A has <strong>'+m+' rows</strong> and <strong>'+n+' columns</strong>. ' +
      'Since '+m+' &gt; '+n+', there are more equations than unknowns &mdash; least squares is required.</p>' +
      '<div class="mat">A =\n'+fmtMat(d.A)+'\n\nb =\n'+d.b.map(function(v){return '  [ '+fmt(v)+' ]';}).join('\n')+'</div>') +

    step(2,'Compute A&sup1; (transpose)','Transpose',
      '<p>Flip rows &amp; columns. A is <strong>'+m+'&times;'+n+'</strong>, so A&sup1; is <strong>'+n+'&times;'+m+'</strong>.</p>' +
      '<div class="mat">A&sup1; =\n'+fmtMat(d.At)+'</div>') +

    step(3,'Compute A&sup1;A','Normal Matrix',
      '<p>Multiply A&sup1; ('+n+'&times;'+m+') by A ('+m+'&times;'+n+') &rarr; a <strong>'+n+'&times;'+n+' square, symmetric</strong> matrix. ' +
      'Always invertible when columns of A are linearly independent.</p>' +
      '<div class="mat">A&sup1;A =\n'+fmtMat(d.AtA)+'</div>') +

    step(4,'Compute A&sup1;b','RHS Vector',
      '<p>Multiply A&sup1; ('+n+'&times;'+m+') by b ('+m+'&times;1) &rarr; a <strong>'+n+'&times;1 vector</strong>. ' +
      'This is the right-hand side of the normal equations.</p>' +
      '<div class="vec">'+fmtVec(d.Atb,'A&sup1;b')+'</div>') +

    step(5,'Solve (A&sup1;A)x&#x0302; = A&sup1;b','Core Step',
      '<p>Now it&apos;s a <strong>square '+n+'&times;'+n+' system</strong>. ' +
      'NumPy uses <code>np.linalg.lstsq</code> (QR factorization &mdash; more stable than inverting A&sup1;A directly).</p>' +
      '<p>Formula: <strong>x&#x0302; = (A&sup1;A)&#x207B;&#xB9; A&sup1;b</strong></p>' +
      '<div class="vec">'+fmtVec(d.x_hat,'x&#x0302;')+'</div>') +

    step(6,'Compute residual r = b &minus; Ax&#x0302;','Error Check',
      '<p>Plug x&#x0302; back in. The difference <strong>r = b &minus; Ax&#x0302;</strong> is the leftover error we cannot eliminate.</p>' +
      '<p>Residual norm <strong>&#x2016;r&#x2016; = '+rn+'</strong> &mdash; the minimum possible error for any x.</p>' +
      '<div class="vec">'+fmtVec(d.residual,'r')+'</div>') +

    step(7,'Verify: A&sup1;r &asymp; 0 (orthogonality)','Geometric Check',
      '<p>Key theorem: <strong>r must be orthogonal to Col(A)</strong>, meaning A&sup1;r = 0. ' +
      'If these values are near zero, your solution is confirmed correct. &#10003;</p>' +
      '<div class="vec">'+fmtVec(d.Atr,'A&sup1;r')+'</div>' +
      '<p style="margin-top:12px"><strong>'+exact+'</strong></p>') +

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
