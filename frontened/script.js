// --- SIDEBAR LOGIC ---
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

// Prevent toggle button click from triggering document listener
document.addEventListener('click', function (event) {

    const sidebar = document.getElementById('sidebar');
    const toggle = document.querySelector('.menu-toggle');

    if (!sidebar || !toggle) return;

    // Ignore clicks on toggle button itself
    if (toggle.contains(event.target)) {
        return;
    }

    if (sidebar.classList.contains('open') &&
        !sidebar.contains(event.target)) {
        sidebar.classList.remove('open');
    }
});

// --- GOOGLE AUTH & API LOGIC ---
// const CLIENT_ID = '150745998816-ndet54lnu9qo15mugethd1k6874knkun.apps.googleusercontent.com';
const CLIENT_ID = '579743530310-9nffblt4a64hh9h7rh4rq169468aetv7.apps.googleusercontent.com';
const SCOPES =   "https://www.googleapis.com/auth/calendar " +
"https://www.googleapis.com/auth/userinfo.profile " +
"https://www.googleapis.com/auth/gmail.send";

let tokenClient;
let accessToken = null;

// Wait for GIS library to be ready
function initGIS() {

    if (!google || !google.accounts) {
        console.log("Google GIS library not loaded yet");
        return;
    }

    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: SCOPES,
        callback: (tokenResponse) => {
            accessToken = tokenResponse.access_token;
            console.log("Generated OAuth token:", accessToken);
            onLoginSuccess();
        },
    });
}

function handleAuth() {
    if (!tokenClient) {
        console.log("Reinitializing Google OAuth");
        initGIS();
    }
    tokenClient?.requestAccessToken();
}

function safeSetText(id, text) {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
}

function safeSetImage(id, src) {
    const img = document.getElementById(id);
    if (img) img.src = src;
}

function onLoginSuccess() {

    const authBtn = document.getElementById('authorize_button');
    const content = document.getElementById('content_section');

    if (authBtn) authBtn.style.display = 'none';
    if (content) content.style.display = 'flex';

    fetch('https://www.googleapis.com/oauth2/v1/userinfo?alt=json', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    })
    .then(res => res.json())
    .then(data => {
        safeSetText('user_name', data.given_name);
        safeSetImage('user_image', data.picture);
        safeSetText('greeting_text', `Welcome back, Agent ${data.given_name}.`);
    })
    .catch(err => {
        console.log("Error fetching user info", err);
    });
}

async function processCommand() {

    const inputBox = document.getElementById("user_input");
    const messageText = inputBox ? inputBox.value.trim() : "";

    if (!messageText) {
        console.log("Empty input");
        return;
    }

    const payload = { text: messageText };

    try {

        const response = await fetch("http://127.0.0.1:3000/message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("Saved:", data);

        if (inputBox) inputBox.value = "";

    } catch (err) {
        console.log("Error sending message", err);
    }
}

async function createGoogleMeet() {

    const resultContent = document.getElementById('result-content');
    const resultCard = document.getElementById('result-card');

    if (!accessToken) {
        if (resultContent) {
            resultContent.innerHTML = `<p class="error-msg">Please sign in first.</p>`;
        }
        return;
    }

    const now = new Date();

    const event = {
        summary: 'Hackathon Sync',
        description: 'Created by PPA',
        start: { dateTime: now.toISOString() },
        end: { dateTime: new Date(now.getTime() + 30 * 60000).toISOString() },
        conferenceData: {
            createRequest: {
                requestId: "req" + Date.now(),
                conferenceSolutionKey: { type: 'hangoutsMeet' }
            }
        }
    };

    try {

        const response = await fetch(
            'https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1&conferenceDataVersion=1',
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(event)
            }
        );

        const data = await response.json();

        if (resultCard) resultCard.style.display = "block";

        if (data.conferenceData && data.conferenceData.entryPoints) {

            const meetLink = data.conferenceData.entryPoints[0].uri;

            if (resultContent) {
                resultContent.innerHTML = `
                    <p style="font-size: 0.9rem;">Meeting Securely Created</p>
                    <a href="${meetLink}" target="_blank" class="meet-link">
                        Click to Join Google Meet
                    </a>
                `;
            }

        } else {
            if (resultContent) {
                resultContent.innerHTML = `<p class="error-msg">NO Meet link found.</p>`;
            }
        }

    } catch (error) {
        if (resultContent) {
            resultContent.innerHTML = `<p class="error-msg">API Error: ${error.message}</p>`;
        }
    }
}

// Ensure GIS initialization even if window.onload already used
window.addEventListener('load', () => {
    initGIS();
    loadNotifications();          // main panel
    loadSidebarNotifications();   // sidebar
});



// document.addEventListener('click', ...)


async function loadNotifications() {
    try {
        const res = await fetch("http://127.0.0.1:8000/notifications");
        const data = await res.json();

        if (!data.items || data.items.length === 0) {
            return;
        }

        // latest notification (already sorted DESC by backend)
        const [goal_id, message, created_at] = data.items[0];

        const resultCard = document.getElementById("result-card");
        const resultContent = document.getElementById("result-content");

        if (!resultCard || !resultContent) return;

        resultCard.style.display = "block";

        resultContent.innerHTML = `
            <p style="font-size: 0.8rem; color: #94a3b8;">
                Latest Meeting Summary
            </p>

            <div style="margin-top: 10px;">
                ${message.replace(/\n/g, "<br>")}
            </div>

            <p style="margin-top: 15px; font-size: 0.75rem; color: #64748b;">
                ${new Date(created_at).toLocaleString()}
            </p>
        `;
    } catch (err) {
        console.log("Failed to load notifications", err);
    }
}


async function loadSidebarNotifications() {
    try {
        const res = await fetch("http://127.0.0.1:8000/notifications");
        const data = await res.json();

        const list = document.getElementById("notification-list");
        if (!list) return;

        list.innerHTML = "";

        if (!data.items || data.items.length === 0) {
            list.innerHTML = `<li class="muted">No notifications yet</li>`;
            return;
        }

        data.items.slice(0, 5).forEach(([goal_id, message, created_at]) => {
            const li = document.createElement("li");
            li.innerText = message.split("\n")[0].replace("**", "");
            li.onclick = () => {
                document.getElementById("result-card").style.display = "block";
                document.getElementById("result-content").innerHTML =
                    message.replace(/\n/g, "<br>");
            };
            list.appendChild(li);
        });

    } catch (err) {
        console.log("Sidebar notification error", err);
    }
}


// document.getElementById("notif-bell")?.addEventListener("click", loadNotifications);
document.querySelector(".notif-bell")?.addEventListener("click", () => {
    loadNotifications();
    loadSidebarNotifications();
});


async function loadNotifications() {
    try {
        const res = await fetch("http://127.0.0.1:8000/notifications");
        const data = await res.json();

        const unread = data.items.filter(n => n[4] === 0).length;

        const countEl = document.getElementById("notif-count");
        if (unread > 0) {
            countEl.innerText = unread;
            countEl.classList.remove("hidden");
        } else {
            countEl.classList.add("hidden");
        }

    } catch (err) {
        console.error("Failed to load notifications", err);
    }
}

document.getElementById("notif-bell")?.addEventListener("click", loadNotifications);

// auto refresh every 10s
setInterval(loadNotifications, 10000);


async function loadRecentSummary() {
    const summaryBox = document.getElementById("recent-summary");
    if (!summaryBox) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/notifications");
        const data = await res.json();

        // 1️⃣ No notifications → hide and exit
        if (!data.items || data.items.length === 0) {
            summaryBox.classList.add("hidden");
            return;
        }

        // 2️⃣ Notifications exist → show latest
        const latest = data.items[0];
        // [id, goal_id, message, created_at, read]

        summaryBox.innerHTML = `
            <strong>Recent Summary</strong>
            <div class="summary-text">
                ${latest[2]}
            </div>
        `;

        summaryBox.classList.remove("hidden");

    } catch (err) {
        console.log("Failed to load recent summary", err);
        summaryBox.classList.add("hidden"); // fail-safe
    }
}


window.addEventListener("load", () => {
    loadRecentSummary();
});
