from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# =========================================================
# CONFIG
# =========================================================

DATABASE = "api_data.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def init_database():

    conn = get_db()

    cursor = conn.cursor()


    # Data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)


    # Request history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL,
            path TEXT NOT NULL,
            status INTEGER NOT NULL,
            body TEXT,
            created_at TEXT NOT NULL
        )
    """)


    conn.commit()

    conn.close()


init_database()


# =========================================================
# REQUEST LOGGER
# =========================================================

def log_request(
    method,
    path,
    status,
    body=None
):

    conn = get_db()

    conn.execute("""
        INSERT INTO requests
        (method, path, status, body, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        method,
        path,
        status,
        str(body) if body else "",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()

    conn.close()


# =========================================================
# GET API
# =========================================================

@app.route("/api/data", methods=["GET"])
def get_data():

    conn = get_db()

    rows = conn.execute("""
        SELECT *
        FROM data
        ORDER BY id DESC
    """).fetchall()

    conn.close()


    result = []

    for row in rows:

        result.append({
            "id": row["id"],
            "name": row["name"],
            "message": row["message"],
            "time": row["created_at"]
        })


    log_request(
        "GET",
        "/api/data",
        200
    )


    return jsonify({

        "success": True,

        "count": len(result),

        "data": result

    })


# =========================================================
# POST API
# =========================================================

@app.route("/api/data", methods=["POST"])
def post_data():

    body = request.get_json(
        silent=True
    )


    if not body:

        log_request(
            "POST",
            "/api/data",
            400
        )

        return jsonify({

            "success": False,

            "message":
                "JSON data required"

        }), 400


    name = str(
        body.get("name", "")
    ).strip()


    message = str(
        body.get("message", "")
    ).strip()


    if not name or not message:

        log_request(
            "POST",
            "/api/data",
            400,
            body
        )

        return jsonify({

            "success": False,

            "message":
                "name এবং message দিতে হবে"

        }), 400


    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    conn = get_db()

    cursor = conn.execute("""
        INSERT INTO data
        (name, message, created_at)
        VALUES (?, ?, ?)
    """, (
        name,
        message,
        now
    ))


    new_id = cursor.lastrowid

    conn.commit()

    conn.close()


    new_data = {

        "id": new_id,

        "name": name,

        "message": message,

        "time": now
    }


    log_request(
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
            new_data

    }), 201


# =========================================================
# PUT API
# =========================================================

@app.route(
    "/api/data/<int:item_id>",
    methods=["PUT"]
)
def update_data(item_id):

    body = request.get_json(
        silent=True
    )


    if not body:

        log_request(
            "PUT",
            f"/api/data/{item_id}",
            400
        )

        return jsonify({

            "success": False,

            "message":
                "JSON data required"

        }), 400


    conn = get_db()


    row = conn.execute("""
        SELECT *
        FROM data
        WHERE id = ?
    """, (item_id,)).fetchone()


    if not row:

        conn.close()


        log_request(
            "PUT",
            f"/api/data/{item_id}",
            404,
            body
        )


        return jsonify({

            "success": False,

            "message":
                "Data not found"

        }), 404


    name = body.get(
        "name",
        row["name"]
    )


    message = body.get(
        "message",
        row["message"]
    )


    conn.execute("""
        UPDATE data

        SET name = ?,
            message = ?

        WHERE id = ?
    """, (
        name,
        message,
        item_id
    ))


    conn.commit()


    updated = conn.execute("""
        SELECT *
        FROM data
        WHERE id = ?
    """, (item_id,)).fetchone()


    conn.close()


    result = {

        "id": updated["id"],

        "name": updated["name"],

        "message": updated["message"],

        "time": updated["created_at"]
    }


    log_request(
        "PUT",
        f"/api/data/{item_id}",
        200,
        body
    )


    return jsonify({

        "success": True,

        "message":
            "Data updated successfully",

        "data":
            result

    })


# =========================================================
# DELETE API
# =========================================================

@app.route(
    "/api/data/<int:item_id>",
    methods=["DELETE"]
)
def delete_data(item_id):

    conn = get_db()


    row = conn.execute("""
        SELECT *
        FROM data
        WHERE id = ?
    """, (item_id,)).fetchone()


    if not row:

        conn.close()


        log_request(
            "DELETE",
            f"/api/data/{item_id}",
            404
        )


        return jsonify({

            "success": False,

            "message":
                "Data not found"

        }), 404


    conn.execute("""
        DELETE FROM data
        WHERE id = ?
    """, (item_id,))


    conn.commit()

    conn.close()


    log_request(
        "DELETE",
        f"/api/data/{item_id}",
        200
    )


    return jsonify({

        "success": True,

        "message":
            "Data deleted successfully"

    })


# =========================================================
# REQUEST HISTORY
# =========================================================

@app.route(
    "/api/history",
    methods=["GET"]
)
def get_history():

    conn = get_db()


    rows = conn.execute("""
        SELECT *
        FROM requests
        ORDER BY id DESC
        LIMIT 100
    """).fetchall()


    conn.close()


    history = []


    for row in rows:

        history.append({

            "id": row["id"],

            "method":
                row["method"],

            "path":
                row["path"],

            "status":
                row["status"],

            "body":
                row["body"],

            "time":
                row["created_at"]

        })


    return jsonify({

        "success": True,

        "count":
            len(history),

        "requests":
            history

    })


# =========================================================
# CLEAR HISTORY
# =========================================================

@app.route(
    "/api/history/clear",
    methods=["POST"]
)
def clear_history():

    conn = get_db()

    conn.execute(
        "DELETE FROM requests"
    )

    conn.commit()

    conn.close()


    return jsonify({

        "success": True,

        "message":
            "History cleared"

    })


# =========================================================
# DASHBOARD
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

<title>Flask API Dashboard</title>


<style>

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


.header {

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #9333ea
        );

    padding:
        40px 20px;

    text-align:
        center;
}


.header h1 {

    margin: 0;

    font-size:
        32px;
}


.header p {

    margin:
        10px 0 0;

    opacity:
        .9;
}


.container {

    width:
        94%;

    max-width:
        1200px;

    margin:
        30px auto;
}


.stats {

    display:
        grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap:
        18px;

    margin-bottom:
        25px;
}


.stat {

    background:
        #1e293b;

    border:
        1px solid #334155;

    padding:
        22px;

    border-radius:
        15px;

    text-align:
        center;
}


.number {

    font-size:
        30px;

    font-weight:
        bold;

    color:
        #a5b4fc;
}


.label {

    color:
        #94a3b8;

    margin-top:
        5px;
}


.grid {

    display:
        grid;

    grid-template-columns:
        1fr 1fr;

    gap:
        25px;
}


.panel {

    background:
        #1e293b;

    border:
        1px solid #334155;

    border-radius:
        18px;

    padding:
        25px;
}


.panel h2 {

    margin-top:
        0;

    color:
        white;
}


.url {

    background:
        #020617;

    padding:
        13px;

    border-radius:
        9px;

    font-family:
        monospace;

    margin-bottom:
        15px;

    color:
        #93c5fd;
}


input,
textarea,
select {

    width:
        100%;

    padding:
        13px;

    margin-bottom:
        14px;

    background:
        #0f172a;

    color:
        white;

    border:
        1px solid #475569;

    border-radius:
        10px;

    outline:
        none;

    font-size:
        15px;
}


textarea {

    height:
        120px;

    resize:
        vertical;
}


button {

    border:
        none;

    padding:
        12px 18px;

    border-radius:
        10px;

    background:
        #6366f1;

    color:
        white;

    cursor:
        pointer;

    font-size:
        15px;
}


button:hover {

    opacity:
        .85;
}


.danger {

    background:
        #dc2626;
}


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

    min-height:
        80px;
}


.history {

    margin-top:
        25px;
}


.request {

    background:
        #0f172a;

    border:
        1px solid #334155;

    padding:
        17px;

    border-radius:
        13px;

    margin-bottom:
        12px;
}


.request-top {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;
}


.method {

    font-weight:
        bold;

    background:
        #334155;

    padding:
        6px 10px;

    border-radius:
        7px;
}


.status {

    color:
        #86efac;

    background:
        #064e3b;

    padding:
        6px 10px;

    border-radius:
        7px;
}


.path {

    color:
        #93c5fd;

    font-family:
        monospace;

    margin-top:
        10px;

    word-break:
        break-all;
}


.time {

    color:
        #64748b;

    font-size:
        12px;

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

    font-family:
        monospace;

    font-size:
        12px;
}


.empty {

    text-align:
        center;

    padding:
        30px;

    color:
        #64748b;
}


@media(max-width:800px) {

    .grid {

        grid-template-columns:
            1fr;
    }

    .stats {

        grid-template-columns:
            1fr;
    }

}

</style>

</head>


<body>


<div class="header">

    <h1>🚀 Flask API Dashboard</h1>

    <p>
        GET • POST • PUT • DELETE
    </p>

</div>


<div class="container">


<!-- STATS -->

<div class="stats">

    <div class="stat">

        <div
            class="number"
            id="dataCount">
            0
        </div>

        <div class="label">
            Total Data
        </div>

    </div>


    <div class="stat">

        <div
            class="number"
            id="requestCount">
            0
        </div>

        <div class="label">
            Total Requests
        </div>

    </div>


    <div class="stat">

        <div
            class="number">
            🟢
        </div>

        <div class="label">
            API Online
        </div>

    </div>

</div>



<div class="grid">


<!-- POST -->

<div class="panel">

    <h2>📤 POST Data</h2>

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


    <button onclick="postData()">

        🚀 Send POST

    </button>


    <div
        id="postResult"
        class="result">

        Response...

    </div>

</div>



<!-- API TESTER -->

<div class="panel">

    <h2>🧪 API Tester</h2>


    <select id="method">

        <option>GET</option>

        <option>POST</option>

        <option>PUT</option>

        <option>DELETE</option>

    </select>


    <input
        id="path"
        value="/api/data"
        placeholder="/api/data"
    >


    <textarea
        id="body"
        placeholder='JSON Body'>

    </textarea>


    <button onclick="sendRequest()">

        ⚡ Send Request

    </button>


    <div
        id="apiResult"
        class="result">

        Response...

    </div>

</div>


</div>



<!-- HISTORY -->

<div class="panel history">

    <div
        style="
        display:flex;
        justify-content:space-between;
        align-items:center;
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


// ==========================================
// POST
// ==========================================

async function postData() {

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



// ==========================================
// API TESTER
// ==========================================

async function sendRequest() {

    const method =
        document.getElementById(
            "method"
        ).value;


    const path =
        document.getElementById(
            "path"
        ).value;


    const body =
        document.getElementById(
            "body"
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

        if (body.trim()) {

            try {

                JSON.parse(body);

                options.body =
                    body;

            }
            catch {

                result.textContent =
                    "❌ Invalid JSON";

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



// ==========================================
// HISTORY
// ==========================================

async function loadHistory() {

    try {

        const response =
            await fetch(
                "/api/history"
            );


        const result =
            await response.json();


        document.getElementById(
            "requestCount"
        ).textContent =
            result.count;


        const history =
            document.getElementById(
                "history"
            );


        history.innerHTML = "";


        if (
            result.requests.length === 0
        ) {

            history.innerHTML =
                '<div class="empty">' +
                'কোনো Request নেই' +
                '</div>';

            return;
        }


        result.requests.forEach(
            item => {

                const div =
                    document.createElement(
                        "div"
                    );


                div.className =
                    "request";


                let body = "";


                if (item.body) {

                    body =
                        item.body;

                }


                div.innerHTML = `

                    <div
                        class="request-top">

                        <span
                            class="method">

                            ${item.method}

                        </span>


                        <span
                            class="status">

                            ${item.status}

                        </span>

                    </div>


                    <div
                        class="path">

                        ${escapeHTML(
                            item.path
                        )}

                    </div>


                    <div
                        class="time">

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
                    div
                );

            }
        );


    }
    catch(error) {

        console.log(error);

    }

}



// ==========================================
// DATA COUNT
// ==========================================

async function loadDataCount() {

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



// ==========================================
// CLEAR HISTORY
// ==========================================

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



// ==========================================
// SECURITY
// ==========================================

function escapeHTML(text) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        text;

    return div.innerHTML;

}



// ==========================================
// LOAD
// ==========================================

function loadAll() {

    loadHistory();

    loadDataCount();

}


loadAll();


setInterval(
    loadHistory,
    3000
);

</script>


</body>

</html>
""")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
