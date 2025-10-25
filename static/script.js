const pwInput = document.getElementById("password");
const strengthText = document.getElementById("strength-text");
const entropyText = document.getElementById("entropy-text");
const suggestionsList = document.getElementById("suggestions");
const iconWrap = document.getElementById("icon");
const toggleEye = document.getElementById("toggle-eye");
const generateBtn = document.getElementById("generate-pass");
const segments = document.querySelectorAll(".strength-segment");

async function analyzePassword() {
    const password = pwInput.value;
    const res = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
    });
    const data = await res.json();

    strengthText.textContent = `Strength: ${data.label} (${data.score}%)`;
    entropyText.textContent = `Entropy: ${data.entropy} bits`;

    suggestionsList.innerHTML = "";
    data.suggestions.forEach(s => {
        const li = document.createElement("li");
        li.textContent = s;
        suggestionsList.appendChild(li);
    });

    updateStrengthSegments(data.score);
    updateIcon(data.score);
}

function updateStrengthSegments(score) {
    segments.forEach(seg => seg.style.opacity = 0.3);
    if(score <= 20){
        segments[0].style.opacity = 1;
    } else if(score <= 50){
        segments[0].style.opacity = 1;
        segments[1].style.opacity = 1;
    } else if(score <= 80){
        segments[0].style.opacity = 1;
        segments[1].style.opacity = 1;
        segments[2].style.opacity = 1;
    } else {
        segments.forEach(seg => seg.style.opacity = 1);
    }
}

function updateIcon(score){
    if(score < 40){
        iconWrap.innerHTML = lockSVG("red");
    } else if(score < 70){
        iconWrap.innerHTML = shieldSVG("orange");
    } else {
        iconWrap.innerHTML = lockSVG("green");
    }
}

function lockSVG(color){
    return `<svg viewBox="0 0 24 24" width="24" height="24">
        <path d="M17 8V7a5 5 0 0 0-10 0v1H5v12h14V8h-2zM9 8V7a3 3 0 0 1 6 0v1H9z" fill="${color}"/>
    </svg>`;
}

function shieldSVG(color){
    return `<svg viewBox="0 0 24 24" width="24" height="24">
        <path d="M12 2L4 5v6c0 5 3.7 9.7 8 11 4.3-1.3 8-6 8-11V5l-8-3z" fill="${color}"/>
    </svg>`;
}

toggleEye.addEventListener("click", () => {
    pwInput.type = pwInput.type === "password" ? "text" : "password";
});

generateBtn.addEventListener("click", () => {
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
    let pass = "";
    for(let i=0;i<14;i++) pass += chars[Math.floor(Math.random()*chars.length)];
    pwInput.value = pass;
    analyzePassword();
});

pwInput.addEventListener("input", analyzePassword);
analyzePassword();
