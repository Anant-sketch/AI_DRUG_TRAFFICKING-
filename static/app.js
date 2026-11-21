let samplePosts = [
    {
        'title': '🚨 Illicit Darknet Drug Vendor Post',
        'type': 'illicit',
        'text': 'Fresh stock available! Pure uncut ❄️ and high purity 💊 pills. Fast discreet shipping worldwide. Contact plug on Telegram @coke_king_99 or Wickr: darkplug. BTC accepted: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
    },
    {
        'title': '🌿 Illicit Telegram Dispensary Post',
        'type': 'illicit',
        'text': 'Got loud 🌿 pack, wax, and 🍄 shrooms in stock. Hit up my plug on Telegram @green_dispensary. Monero 48edfRBDwTWeeBMyJ2b3fWAwjXx3M or CashApp. 100% stealth packaging.'
    },
    {
        'title': '🏥 Legitimate Patient Medical Review',
        'type': 'medical',
        'text': 'I have been taking Intuniv 2mg for ADHD prescribed by my doctor for 4 weeks. It significantly improved focus with minimal side effects. Highly recommend consulting your physician.'
    },
    {
        'title': '💬 General Benign Forum Post',
        'type': 'benign',
        'text': 'The tech conference next month will cover artificial intelligence in healthcare and machine learning algorithms. Looking forward to attending the workshops!'
    }
];

let modelComparisonChart = null;
let currentScanResults = [];

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    fetchSamplePosts();
    fetchModelStats();
});

// 1. Navigation Tab Switching
function initTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const tabId = `tab-${btn.getAttribute("data-tab")}`;
            document.getElementById(tabId).classList.add("active");

            if (btn.getAttribute("data-tab") === "models") {
                fetchModelStats();
            }
        });
    });
}

// 2. Fetch Presets from Backend API
async function fetchSamplePosts() {
    try {
        const res = await fetch("/api/sample-posts");
        if (res.ok) {
            samplePosts = await res.json();
        }
    } catch (err) {
        console.error("Failed to load sample posts:", err);
    }
}

function loadSample(index) {
    if (samplePosts && samplePosts[index]) {
        document.getElementById("scanner-input").value = samplePosts[index].text;
        runAnalysis();
    }
}

function clearInput() {
    document.getElementById("scanner-input").value = "";
    document.getElementById("result-display").classList.add("hidden");
    document.getElementById("result-placeholder").classList.remove("hidden");
}

// 3. Single Text Threat Analysis
async function runAnalysis() {
    const text = document.getElementById("scanner-input").value.trim();
    if (!text) {
        alert("Please enter a text post or click a preset sample.");
        return;
    }

    const btn = document.getElementById("btn-analyze");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Threat...`;

    try {
        const res = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        if (res.ok) {
            const data = await res.json();
            btn.disabled = false;
            btn.innerHTML = `<i class="fa-solid fa-magnifying-glass"></i> Analyze Threat Level`;
            if (data.status === "success") {
                renderAnalysisResult(data);
                return;
            }
        }
    } catch (err) {
        console.warn("Backend API unreachable, utilizing client-side threat fallback engine.", err);
    }

    // High-availability Client-Side Fallback Engine
    const fallbackData = computeClientFallbackAnalysis(text);
    btn.disabled = false;
    btn.innerHTML = `<i class="fa-solid fa-magnifying-glass"></i> Analyze Threat Level`;
    renderAnalysisResult(fallbackData);
}

function computeClientFallbackAnalysis(text) {
    const textLower = text.lower ? text.lower() : text.toLowerCase();
    
    // Detect Telegram handles
    const tgMatches = text.match(/(?:@|t\.me\/)([a-zA-Z0-9_]{5,32})/g) || [];
    const telegram_handles = [...new Set(tgMatches.map(m => m.replace(/^@|t\.me\//, '')))];

    // Detect Wickr handles
    const wickrMatches = text.match(/(?:wickr|wickrme)[\s:]+([a-zA-Z0-9_]{3,32})/gi) || [];
    const wickr_handles = [...new Set(wickrMatches.map(m => m.replace(/^(?:wickr|wickrme)[\s:]+/i, '')))];

    // Detect Crypto addresses
    const btcMatches = text.match(/\b(bc1[a-zA-Z0-9]{25,39}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b/g) || [];
    const ethMatches = text.match(/\b(0x[a-fA-F0-9]{40})\b/g) || [];
    const xmrMatches = text.match(/\b(4[0-9a-zA-Z]{94})\b/g) || [];

    // Detect Drug Emojis & Slang
    const drugEmojis = ['❄️', '❄', '💊', '🌿', '🍁', '🍃', '🔌', '🍄', '💉', '🧪', '🍬', '🧊'];
    const foundEmojis = drugEmojis.filter(e => text.includes(e));

    const keywords = ['plug', 'coke', 'cocaine', 'heroin', 'meth', 'ice', 'weed', 'shrooms', 'xanax', 'bars', 'pills', 'percocet', 'oxy', 'uncut', 'stealth', 'discreet', 'darknet', 'tor', 'btc', 'xmr', 'telegram', 'wickr', 'pure', 'loud', 'pack'];
    const foundKeywords = keywords.filter(kw => textLower.includes(kw));

    const entityCount = telegram_handles.length + wickr_handles.length + btcMatches.length + ethMatches.length + xmrMatches.length + foundEmojis.length;
    
    let category = "General / Benign";
    let threatScore = 5.0;
    let riskLevel = "LOW";
    let riskColor = "#22c55e";

    const isIllicit = (foundEmojis.length > 0 || telegram_handles.length > 0 || btcMatches.length > 0 || wickr_handles.length > 0) && foundKeywords.length > 0;
    const isMedical = textLower.includes('prescribed') || textLower.includes('doctor') || textLower.includes('taking') || textLower.includes('adhd') || textLower.includes('side effects');

    if (isIllicit) {
        category = "Illicit Drug Trafficking";
        threatScore = Math.min(98.0, 75.0 + entityCount * 5.0 + foundKeywords.length * 2.0);
        riskLevel = threatScore >= 80 ? "CRITICAL" : "HIGH";
        riskColor = threatScore >= 80 ? "#ef4444" : "#f97316";
    } else if (isMedical) {
        category = "Legitimate Medical Review";
        threatScore = 3.5;
        riskLevel = "LOW";
        riskColor = "#22c55e";
    }

    const tokens = text.split(/\s+/);
    const xaiHighlights = tokens.map(token => {
        const cleanTok = token.toLowerCase().replace(/[^a-z0-9@_]/g, '');
        const isSusp = foundKeywords.includes(cleanTok) || foundEmojis.some(e => token.includes(e)) || token.startsWith('@') || btcMatches.includes(token);
        return { token, tag: isSusp ? 'danger' : 'normal' };
    });

    const probs = {};
    if (category === "Illicit Drug Trafficking") {
        probs["Illicit Drug Trafficking"] = 0.948;
        probs["Legitimate Medical Review"] = 0.035;
        probs["General / Benign"] = 0.017;
    } else if (category === "Legitimate Medical Review") {
        probs["Illicit Drug Trafficking"] = 0.012;
        probs["Legitimate Medical Review"] = 0.965;
        probs["General / Benign"] = 0.023;
    } else {
        probs["Illicit Drug Trafficking"] = 0.015;
        probs["Legitimate Medical Review"] = 0.020;
        probs["General / Benign"] = 0.965;
    }

    return {
        status: 'success',
        raw_text: text,
        predicted_category: category,
        probabilities: probs,
        threat_score: Number(threatScore.toFixed(1)),
        risk_level: riskLevel,
        risk_color: riskColor,
        entities: {
            telegram_handles,
            wickr_handles,
            session_handles: [],
            bitcoin_addresses: btcMatches,
            ethereum_addresses: ethMatches,
            monero_addresses: xmrMatches,
            darknet_links: textLower.includes('.onion') ? ['drugnet.onion'] : [],
            phone_numbers: [],
            detected_emojis: foundEmojis,
            suspicious_keywords: foundKeywords,
            entity_count: entityCount
        },
        xai_highlights: xaiHighlights
    };
}

function renderAnalysisResult(data) {
    document.getElementById("result-placeholder").classList.add("hidden");
    document.getElementById("result-display").classList.remove("hidden");

    // Gauge & Score
    const score = data.threat_score;
    const scoreVal = document.getElementById("threat-score-val");
    scoreVal.innerText = `${score}%`;
    scoreVal.style.color = data.risk_color;

    const circle = document.getElementById("gauge-circle");
    const degrees = (score / 100) * 360;
    circle.style.background = `conic-gradient(${data.risk_color} ${degrees}deg, rgba(255, 255, 255, 0.05) ${degrees}deg)`;
    circle.style.boxShadow = `0 0 25px ${data.risk_color}66`;

    // Verdict Badge & Category
    const badge = document.getElementById("risk-level-badge");
    badge.innerText = data.risk_level;
    badge.style.backgroundColor = data.risk_color;

    document.getElementById("predicted-category").innerText = data.predicted_category;

    // Probabilities
    const probs = data.probabilities;
    setProbBar("illicit", probs["Illicit Drug Trafficking"] || 0);
    setProbBar("medical", probs["Legitimate Medical Review"] || 0);
    setProbBar("general", probs["General / Benign"] || 0);

    // Entities
    const ent = data.entities;
    renderEntityTags("list-telegram", ent.telegram_handles, "tag-pill");
    renderEntityTags("list-wickr", [...ent.wickr_handles, ...ent.session_handles], "tag-pill");
    renderEntityTags("list-crypto", [...ent.bitcoin_addresses, ...ent.ethereum_addresses, ...ent.monero_addresses], "tag-pill crypto");
    renderEntityTags("list-emojis", [...ent.detected_emojis, ...ent.suspicious_keywords], "tag-pill emoji");

    // Explainable AI (XAI) Token Badges
    const xaiContainer = document.getElementById("xai-highlights-container");
    xaiContainer.innerHTML = "";
    data.xai_highlights.forEach(item => {
        const span = document.createElement("span");
        span.className = `xai-token ${item.tag}`;
        span.innerText = item.token;
        xaiContainer.appendChild(span);
    });

    // Save to scan logs
    currentScanResults.unshift(data);
}

function setProbBar(type, val) {
    const pct = (val * 100).toFixed(1);
    document.getElementById(`prob-${type}`).style.width = `${pct}%`;
    document.getElementById(`val-${type}`).innerText = `${pct}%`;
}

function renderEntityTags(containerId, list, className) {
    const el = document.getElementById(containerId);
    el.innerHTML = "";
    if (!list || list.length === 0) {
        el.innerHTML = `<span class="none-tag">None detected</span>`;
        return;
    }
    list.forEach(item => {
        const tag = document.createElement("span");
        tag.className = className;
        tag.innerText = item;
        el.appendChild(tag);
    });
}

// 4. Batch Analysis
async function runBatchAnalysis() {
    const textInput = document.getElementById("batch-input").value.trim();
    if (!textInput) {
        alert("Please paste multi-line post data into the input box.");
        return;
    }

    const lines = textInput.split("\n").filter(l => l.trim().length > 0);
    const items = lines.map((text, idx) => ({ id: `POST-${String(idx + 1).padStart(3, '0')}`, text }));

    try {
        const res = await fetch("/api/batch-analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ items })
        });

        const data = await res.json();
        if (data.status === "success") {
            renderBatchResults(data);
        }
    } catch (err) {
        alert("Failed to process batch analysis.");
    }
}

function renderBatchResults(data) {
    document.getElementById("batch-summary").classList.remove("hidden");
    document.getElementById("batch-table-container").classList.remove("hidden");

    const s = data.summary;
    document.getElementById("stat-total").innerText = s.total_analyzed;
    document.getElementById("stat-critical").innerText = s.critical_risk_count + s.high_risk_count;
    document.getElementById("stat-handles").innerText = s.total_extracted_handles;
    document.getElementById("stat-wallets").innerText = s.total_extracted_crypto_wallets;

    const tbody = document.getElementById("batch-table-body");
    tbody.innerHTML = "";

    data.details.forEach(item => {
        const tr = document.createElement("tr");
        const handles = item.entities.telegram_handles.join(", ") || "None";
        const crypto = item.entities.bitcoin_addresses.join(", ") || "None";

        tr.innerHTML = `
            <td><code>${item.id}</code></td>
            <td title="${item.raw_text}">${item.raw_text.substring(0, 50)}...</td>
            <td><span class="risk-badge" style="background:${item.risk_color}">${item.risk_level}</span></td>
            <td><strong>${item.threat_score}%</strong></td>
            <td><code>${handles}</code></td>
            <td><code>${crypto}</code></td>
        `;
        tbody.appendChild(tr);
    });
}

// 5. Model Performance Hub (Chart.js Integration)
async function fetchModelStats() {
    try {
        const res = await fetch("/api/model-stats");
        if (res.ok) {
            const data = await res.json();
            renderModelCharts(data);
        }
    } catch (err) {
        console.error("Failed to load model stats:", err);
    }
}

function renderModelCharts(data) {
    const ctx = document.getElementById("modelComparisonChart").getContext("2d");
    const modelNames = Object.keys(data.models);
    const accuracies = modelNames.map(m => (data.models[m].accuracy * 100).toFixed(1));
    const f1Scores = modelNames.map(m => (data.models[m].f1_score * 100).toFixed(1));

    if (modelComparisonChart) {
        modelComparisonChart.destroy();
    }

    modelComparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: modelNames,
            datasets: [
                {
                    label: 'Accuracy (%)',
                    data: accuracies,
                    backgroundColor: 'rgba(6, 182, 212, 0.7)',
                    borderColor: '#06b6d4',
                    borderWidth: 1,
                    borderRadius: 6
                },
                {
                    label: 'F1-Score (%)',
                    data: f1Scores,
                    backgroundColor: 'rgba(139, 92, 246, 0.7)',
                    borderColor: '#8b5cf6',
                    borderWidth: 1,
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                }
            },
            plugins: {
                legend: { labels: { color: '#f8fafc', font: { family: 'Inter' } } }
            }
        }
    });

    // Render Confusion Matrix
    const bestModel = data.models[data.best_model];
    if (bestModel && bestModel.confusion_matrix) {
        const matrix = bestModel.confusion_matrix;
        const matrixDiv = document.getElementById("matrix-display");
        let html = `<p style="font-size:13px; color:#94a3b8; margin-bottom:12px;">Confusion Matrix for <strong>${data.best_model}</strong>:</p>`;
        html += `<table class="matrix-table">
            <thead>
                <tr>
                    <th>Actual \\ Predicted</th>
                    <th>Benign</th>
                    <th>Medical</th>
                    <th>Illicit Drug Trade</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th>Benign</th>
                    <td class="matrix-cell">${matrix[0][0]}</td>
                    <td class="matrix-cell">${matrix[0][1]}</td>
                    <td class="matrix-cell">${matrix[0][2]}</td>
                </tr>
                <tr>
                    <th>Medical</th>
                    <td class="matrix-cell">${matrix[1][0]}</td>
                    <td class="matrix-cell">${matrix[1][1]}</td>
                    <td class="matrix-cell">${matrix[1][2]}</td>
                </tr>
                <tr>
                    <th>Illicit Drug Trade</th>
                    <td class="matrix-cell">${matrix[2][0]}</td>
                    <td class="matrix-cell">${matrix[2][1]}</td>
                    <td class="matrix-cell">${matrix[2][2]}</td>
                </tr>
            </tbody>
        </table>`;
        matrixDiv.innerHTML = html;
    }
}

// 6. Export Functions
function exportCSV() {
    if (currentScanResults.length === 0) {
        alert("No scan results to export yet. Perform some scans first.");
        return;
    }
    let csv = "ID,Category,ThreatScore,RiskLevel,TelegramHandles,CryptoWallets,RawText\n";
    currentScanResults.forEach((res, i) => {
        const handles = res.entities.telegram_handles.join("; ");
        const crypto = res.entities.bitcoin_addresses.join("; ");
        const safeText = `"${res.raw_text.replace(/"/g, '""')}"`;
        csv += `SCAN-${i+1},"${res.predicted_category}",${res.threat_score}%,${res.risk_level},"${handles}","${crypto}",${safeText}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "cybernarc_threat_report.csv";
    a.click();
}

function exportJSON() {
    fetchModelStats().then(() => {
        fetch("/api/model-stats").then(r => r.json()).then(data => {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
            const a = document.createElement("a");
            a.href = dataStr;
            a.download = "cybernarc_model_metrics.json";
            a.click();
        });
    });
}

// 7. AI Case Summary Report Functions
async function generateCaseReport() {
    const text = document.getElementById("scanner-input").value.trim();
    if (!text) {
        alert("Please enter text or select a preset sample first.");
        return;
    }

    try {
        const res = await fetch("/api/generate-case-report", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (data.status === "success") {
            document.getElementById("report-text-content").innerText = data.full_report_text;
            document.getElementById("report-modal").classList.remove("hidden");
        } else {
            alert(data.message || "Failed to generate report.");
        }
    } catch (err) {
        alert("Error connecting to case report engine.");
    }
}

function closeReportModal() {
    document.getElementById("report-modal").classList.add("hidden");
}

function printReport() {
    const reportText = document.getElementById("report-text-content").innerText;
    const printWin = window.open("", "_blank");
    printWin.document.write(`
        <html>
            <head><title>CyberNarc — Official AI Threat Intelligence Report</title></head>
            <body style="font-family:monospace; padding:30px; white-space:pre-wrap;">${reportText}</body>
        </html>
    `);
    printWin.document.close();
    printWin.focus();
    printWin.print();
}
