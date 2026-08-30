
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# =========================================================
# REQUEST HISTORY
# =========================================================

request_history = []

MAX_HISTORY = 100


def save_request(method, path, status, body=None):

    item = {
        "method": method,
        "path": path,
        "status": status,
        "body": body,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    request_history.insert(0, item)

    # সর্বোচ্চ 100টি request রাখবে
    if len(request_history) > MAX_HISTORY:
        request_history.pop()


# =========================================================
# DATA
# =========================================================

data = []


# =========================================================
# API
# =========================================================

@app.route("/api/data", methods=["GET"])
def get_data():

    result = {
        "success": True,
        "count": len(data),
        "data": data
    }

    save_request(
        "GET",
        "/api/data",
        200
    )

    return jsonify(result)


@app.route("/api/data", methods=["POST"])
def post_data():

    body = request.get_json(silent=True)

    if not body:

        save_request(
            "POST",
            "/api/data",
            400,
            None
        )

        return jsonify({
            "success": False,
            "message": "JSON data required"
        }), 400


    name = str(body.get("name", "")).strip()
    message = str(body.get("message", "")).strip()


    if not name or not message:

        save_request(
            "POST",
            "/api/data",
            400,
            body
        )

        return jsonify({
            "success": False,
            "message": "name এবং message দিতে হবে"
        }), 400


    new_item = {

        "id": len(data) + 1,

        "name": name,

        "message": message,

        "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }


    data.append(new_item)


    save_request(
        "POST",
        "/api/data",
        201,
        body
    )


    return jsonify({

        "success": True,

        "message":
            "Data added successfully",

        "data":
            new_item

    }), 201


# =========================================================
# PUT
# =========================================================

@app.route("/api/data/<int:item_id>", methods=["PUT"])
def update_data(item_id):

    body = request.get_json(silent=True)

    for item in data:

        if item["id"] == item_id:

            if body:

                if "name" in body:
                    item["name"] = str(
                        body["name"]
                    )

                if "message" in body:
                    item["message"] = str(
                        body["message"]
                    )


            save_request(
                "PUT",
                f"/api/data/{item_id}",
                200,
                body
            )


            return jsonify({
                "success": True,
                "message": "Data updated",
                "data": item
            })


    save_request(
        "PUT",
        f"/api/data/{item_id}",
        404,
        body
    )


    return jsonify({
        "success": False,
        "message": "Data not found"
    }), 404


# =========================================================
# DELETE
# =========================================================

@app.route("/api/data/<int:item_id>", methods=["DELETE"])
def delete_data(item_id):

    for index, item in enumerate(data):

        if item["id"] == item_id:

            deleted = data.pop(index)


            save_request(
                "DELETE",
                f"/api/data/{item_id}",
                200
            )


            return jsonify({

                "success": True,

                "message":
                    "Data deleted",

                "data":
                    deleted
            })


    save_request(
        "DELETE",
        f"/api/data/{item_id}",
        404
    )


    return jsonify({

        "success": False,

        "message":
            "Data not found"

    }), 404


# =========================================================
# REQUEST HISTORY API
# =========================================================

@app.route("/api/history")
def history():

    return jsonify({

        "success": True,

        "count":
            len(request_history),

        "requests":
            request_history
    })


# =========================================================
# CLEAR HISTORY
# =========================================================

@app.route("/api/history/clear", methods=["POST"])
def clear_history():

    request_history.clear()

    return jsonify({

        "success": True,

        "message":
            "History cleared"
    })


# =========================================================
# WEBSITE
# =========================================================

@app.route("/")
def home():

    return render_template_string("""

<!DOCTYPE html>

<html lang="bn">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Python API Dashboard</title>


<style>

/* =========================
   RESET
========================= */

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    font-family:
        Arial,
        sans-serif;

    background:
        #0f172a;

    color:
        #e2e8f0;
}


/* =========================
   HEADER
========================= */

.header {

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #9333ea
        );

    padding:
        35px 20px;

    text-align:
        center;

    box-shadow:
        0 10px 30px
        rgba(0,0,0,.3);
}


.header h1 {

    margin:
        0;

    font-size:
        32px;
}


.header p {

    margin:
        10px 0 0;

    opacity:
        .9;
}


/* =========================
   CONTAINER
========================= */

.container {

    width:
        94%;

    max-width:
        1200px;

    margin:
        30px auto;
}


/* =========================
   GRID
========================= */

.grid {

    display:
        grid;

    grid-template-columns:
        1fr 1fr;

    gap:
        25px;
}


@media(max-width: 800px) {

    .grid {

        grid-template-columns:
            1fr;
    }
}


/* =========================
   PANEL
========================= */

.panel {

    background:
        #1e293b;

    border:
        1px solid #334155;

    border-radius:
        18px;

    padding:
        25px;

    box-shadow:
        0 10px 30px
        rgba(0,0,0,.2);
}


.panel h2 {

    margin-top:
        0;

    color:
        white;
}


/* =========================
   INPUT
========================= */

input,
textarea,
select {

    width:
        100%;

    padding:
        13px;

    margin-bottom:
        14px;

    border:
        1px solid #475569;

    border-radius:
        10px;

    background:
        #0f172a;

    color:
        white;

    font-size:
        15px;

    outline:
        none;
}


textarea {

    height:
        120px;

    resize:
        vertical;
}


input:focus,
textarea:focus {

    border-color:
        #6366f1;
}


/* =========================
   BUTTON
========================= */

button {

    border:
        none;

    border-radius:
        10px;

    padding:
        12px 18px;

    background:
        #6366f1;

    color:
        white;

    font-size:
        15px;

    cursor:
        pointer;
}


button:hover {

    opacity:
        .85;
}


.danger {

    background:
        #dc2626;
}


.green {

    background:
        #059669;
}


/* =========================
   API URL
========================= */

.url {

    background:
        #020617;

    padding:
        14px;

    border-radius:
        10px;

    margin-bottom:
        15px;

    font-family:
        monospace;

    word-break:
        break-all;
}


/* =========================
   REQUEST CARD
========================= */

.request-card {

    background:
        #0f172a;

    border:
        1px solid #334155;

    border-radius:
        14px;

    padding:
        18px;

    margin-bottom:
        14px;
}


.request-top {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    gap:
        10px;

    margin-bottom:
        10px;
}


.method {

    font-weight:
        bold;

    padding:
        6px 10px;

    border-radius:
        7px;

    background:
        #334155;
}


.status {

    padding:
        5px 9px;

    border-radius:
        7px;

    background:
        #065f46;

    color:
        #a7f3d0;
}


.path {

    color:
        #93c5fd;

    font-family:
        monospace;

    word-break:
        break-all;
}


.time {

    font-size:
        12px;

    color:
        #94a3b8;

    margin-top:
        8px;
}


.body {

    background:
        #020617;

    padding:
        10px;

    margin-top:
        10px;

    border-radius:
        8px;

    white-space:
        pre-wrap;

    word-break:
        break-word;

    font-family:
        monospace;

    font-size:
        13px;
}


/* =========================
   RESULT
========================= */

.result {

    margin-top:
        15px;

    background:
        #020617;

    padding:
        15px;

    border-radius:
        10px;

    white-space:
        pre-wrap;

    overflow:
        auto;

    font-family:
        monospace;

    font-size:
        13px;
}


/* =========================
   STATS
========================= */

.stats {

    display:
        grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap:
        15px;

    margin-bottom:
        25px;
}


.stat {

    background:
        #1e293b;

    border:
        1px solid #334155;

    border-radius:
        14px;

    padding:
        20px;

    text-align:
        center;
}


.stat-number {

    font-size:
        28px;

    font-weight:
        bold;

    color:
        #a5b4fc;
}


.stat-title {

    color:
        #94a3b8;

    font-size:
        13px;

    margin-top:
        5px;
}


@media(max-width:600px) {

    .stats {

        grid-template-columns:
            1fr;
    }
}


.empty {

    text-align:
        center;

    padding:
        30px;

    color:
        #94a3b8;
}

</style>

</head>


<body>


<!-- HEADER -->

<div class="header">

    <h1>🚀 Python API Dashboard</h1>

    <p>
        GET • POST • PUT • DELETE
    </p>

</div>



<div class="container">


<!-- STATS -->

<div class="stats">

    <div class="stat">

        <div
            class="stat-number"
            id="dataCount">
            0
        </div>

        <div class="stat-title">
            Total Data
        </div>

    </div>


    <div class="stat">

        <div
            class="stat-number"
            id="requestCount">
            0
        </div>

        <div class="stat-title">
            Requests
        </div>

    </div>


    <div class="stat">

        <div
            class="stat-number">
            API
        </div>

        <div class="stat-title">
            Online
        </div>

    </div>

</div>



<div class="grid">


<!-- =========================
     SEND REQUEST
========================= -->

<div class="panel">

    <h2>
        📤 Send POST Request
    </h2>


    <div class="url">
        POST /api/data
    </div>


    <input
        id="name"
        placeholder="Name"
    >


    <textarea
        id="message"
        placeholder="Message">
    </textarea>


    <button
        onclick="sendPost()">

        🚀 Send POST

    </button>


    <div
        id="postResult"
        class="result">

        Response এখানে দেখাবে...

    </div>

</div>



<!-- =========================
     API TEST
========================= -->

<div class="panel">

    <h2>
        🧪 API Tester
    </h2>


    <select id="method">

        <option value="GET">
            GET
        </option>

        <option value="POST">
            POST
        </option>

        <option value="PUT">
            PUT
        </option>

        <option value="DELETE">
            DELETE
        </option>

    </select>


    <input
        id="apiPath"
        value="/api/data"
        placeholder="API path"
    >


    <textarea
        id="apiBody"
        placeholder='JSON Body

{
  "name": "Test",
  "message": "Hello"
}'>
    </textarea>


    <button
        onclick="sendRequest()">

        ⚡ Send Request

    </button>


    <div
        id="apiResult"
        class="result">

        Response এখানে দেখাবে...

    </div>

</div>


</div>



<!-- =========================
     HISTORY
========================= -->

<div
    class="panel"
    style="margin-top:25px;">

    <div
        style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:10px;
        ">

        <h2>
            📡 Request History
        </h2>

        <button
            class="danger"
            onclick="clearHistory()">

            🗑 Clear

        </button>

    </div>


    <div id="history">

        Loading...

    </div>

</div>


</div>



<script>

/* ==========================================
   POST
========================================== */

async function sendPost() {

    const name =
        document.getElementById(
            "name"
        ).value;

    const message =
        document.getElementById(
            "message"
        ).value;


    const result =
        document.getElementById(
            "postResult"
        );


    if (!name || !message) {

        result.textContent =
            "Name এবং Message দিন";

        return;
    }


    try {

        const response =
            await fetch(
                "/api/data",
                {

                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            name:
                                name,

                            message:
                                message

                        })
                }
            );


        const data =
            await response.json();


        result.textContent =
            JSON.stringify(
                data,
                null,
                2
            );


        document.getElementById(
            "name"
        ).value = "";

        document.getElementById(
            "message"
        ).value = "";


        loadAll();

    }
    catch(error) {

        result.textContent =
            "Error: " + error;

    }

}



/* ==========================================
   API TESTER
========================================== */

async function sendRequest() {

    const method =
        document.getElementById(
            "method"
        ).value;


    const path =
        document.getElementById(
            "apiPath"
        ).value;


    const bodyText =
        document.getElementById(
            "apiBody"
        ).value;


    const result =
        document.getElementById(
            "apiResult"
        );


    const options = {

        method:
            method,

        headers: {
            "Content-Type":
                "application/json"
        }

    };


    if (
        method === "POST" ||
        method === "PUT"
    ) {

        if (bodyText.trim()) {

            try {

                JSON.parse(bodyText);

                options.body =
                    bodyText;

            }
            catch(error) {

                result.textContent =
                    "Invalid JSON";

                return;
            }

        }

    }


    try {

        const response =
            await fetch(
                path,
                options
            );


        const text =
            await response.text();


        let output;


        try {

            output =
                JSON.stringify(
                    JSON.parse(text),
                    null,
                    2
                );

        }
        catch {

            output =
                text;
        }


        result.textContent =
            "Status: " +
            response.status +
            "\\n\\n" +
            output;


        loadAll();

    }
    catch(error) {

        result.textContent =
            "Request Error: " +
            error;

    }

}



/* ==========================================
   LOAD HISTORY
========================================== */

async function loadHistory() {

    try {

        const response =
            await fetch(
                "/api/history"
            );


        const result =
            await response.json();


        const history =
            document.getElementById(
                "history"
            );


        document.getElementById(
            "requestCount"
        ).textContent =
            result.count;


        if (
            result.requests.length === 0
        ) {

            history.innerHTML =
                '<div class="empty">' +
                'কোনো request নেই' +
                '</div>';

            return;
        }


        history.innerHTML = "";


        result.requests.forEach(
            item => {

                const card =
                    document.createElement(
                        "div"
                    );


                card.className =
                    "request-card";


                let body = "";


                if (item.body) {

                    body =
                        JSON.stringify(
                            item.body,
                            null,
                            2
                        );

                }


                card.innerHTML = `

                    <div
                        class="request-top">

                        <span class="method">
                            ${item.method}
                        </span>

                        <span class="status">
                            ${item.status}
                        </span>

                    </div>


                    <div class="path">
                        ${escapeHTML(
                            item.path
                        )}
                    </div>


                    <div class="time">
                        🕒 ${item.time}
                    </div>


                    ${
                        body
                        ?
                        `<div class="body">
                            ${escapeHTML(body)}
                        </div>`
                        :
                        ""
                    }

                `;


                history.appendChild(
                    card
                );

            }
        );


    }
    catch(error) {

        console.log(error);

    }

}



/* ==========================================
   GET DATA COUNT
========================================== */

async function loadData() {

    try {

        const response =
            await fetch(
                "/api/data"
            );


        const result =
            await response.json();


        document.getElementById(
            "dataCount"
        ).textContent =
            result.count;

    }
    catch(error) {

        console.log(error);

    }

}



/* ==========================================
   CLEAR HISTORY
========================================== */

async function clearHistory() {

    await fetch(
        "/api/history/clear",
        {
            method:
                "POST"
        }
    );


    loadHistory();

}



/* ==========================================
   LOAD EVERYTHING
========================================== */

function loadAll() {

    loadHistory();

    loadData();

}


function escapeHTML(text) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text;

    return div.innerHTML;

}


loadAll();


/* প্রতি 2 সেকেন্ডে history update */

setInterval(
    loadHistory,
    2000
);

</script>


</body>

</html>

""")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
