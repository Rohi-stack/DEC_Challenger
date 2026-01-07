
// --- SIDEBAR LOGIC ---
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Close sidebar if clicking outside of it (Optional User Experience improvement)
document.addEventListener('click', function (event) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.querySelector('.menu-toggle');

    // If sidebar is open AND click is NOT on sidebar AND click is NOT on toggle button
    if (sidebar.classList.contains('open') &&
        !sidebar.contains(event.target) &&
        !toggle.contains(event.target)) {
        sidebar.classList.remove('open');
    }
});

// --- GOOGLE AUTH & API LOGIC ---
const CLIENT_ID = '150745998816-ndet54lnu9qo15mugethd1k6874knkun.apps.googleusercontent.com';
const SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.profile';
let tokenClient;
let accessToken = null;

function initGIS() {
    tokenClient = google.accounts.oauth2.initTokenClient({
        client_id: CLIENT_ID,
        scope: SCOPES,
        callback: (tokenResponse) => {
            accessToken = tokenResponse.access_token;
            onLoginSuccess();
        },
    });
}

function handleAuth() {
    tokenClient.requestAccessToken();
}

function onLoginSuccess() {
    document.getElementById('authorize_button').style.display = 'none';
    document.getElementById('content_section').style.display = 'flex';

    fetch('https://www.googleapis.com/oauth2/v1/userinfo?alt=json', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    }).then(res => res.json()).then(data => {
        document.getElementById('user_name').innerText = data.given_name;
        document.getElementById('user_image').src = data.picture;
        document.getElementById('greeting_text').innerText = `Welcome back, Agent ${data.given_name}.`;
    });
}

async function processCommand() {

    const inputBox = document.getElementById("user_input");
    const messageText = inputBox.value.trim();

    if (!messageText) {
        console.log("Empty input");
        return;
    }

    const payload = {
        text: messageText
    };

    try {
        const response = await fetch("http://127.0.0.1:3000/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log("Saved:", data);

        inputBox.value = "";

    } catch (err) {
        console.log("Error sending message", err);
    }
}


async function createGoogleMeet() {
    const resultContent = document.getElementById('result-content');

    const event = {
        'summary': 'Hackathon Sync',
        'description': 'Created by PPA',
        'start': { 'dateTime': new Date().toISOString() },
        'end': { 'dateTime': new Date(new Date().getTime() + 30 * 60000).toISOString() },
        'conferenceData': {
            'createRequest': {
                'requestId': "req" + Date.now(),
                'conferenceSolutionKey': { 'type': 'hangoutsMeet' }
            }
        }
    };

    try {
        const response = await fetch('https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(event)
        });

        if (!response.ok) {
            throw new Error(`Google API Error: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.conferenceData && data.conferenceData.entryPoints) {
            const meetLink = data.conferenceData.entryPoints[0].uri;
            resultContent.innerHTML = `
                        <p style="color: #94a3b8; font-size: 0.9rem;">MEETING SECURELY CREATED</p>
                        <a href="${meetLink}" target="_blank" class="meet-link">
                            🎥 Click to Join Google Meet
                        </a>
                    `;
        } else {
            resultContent.innerHTML = `<p class="error-msg">Event created, but NO Meet link found. <br>Ensure "Google Calendar API" is enabled in Cloud Console.</p>`;
        }
    } catch (error) {
        console.error(error);
        resultContent.innerHTML = `<p class="error-msg">API Error: ${error.message}</p>`;
    }
}

window.onload = initGIS;
