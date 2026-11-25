"""Flask 后端：提供业务数据与检查校验接口，并在生产环境托管 Vue 构建产物。

开发：`python app.py`（默认 5000 端口），前端 Vite 通过 /api 代理访问
生产：`npm run build` 后由本服务单端口托管 dist 与 /api
"""

import json
import os

from flask import Flask, abort, jsonify, request, send_from_directory

import data as D
import db
from check_service import check_license, check_material, license_quality, material_quality

BASE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.normpath(os.path.join(BASE, "..", "frontend", "dist"))

app = Flask(__name__)
db.init_db()


# ---------------- 业务数据 ----------------

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/bootstrap")
def bootstrap():
    """首屏所需的全量基础数据，减少请求次数。"""
    return jsonify(
        {
            "brand": D.BRAND,
            "user": D.USER,
            "positions": D.POSITIONS,
            "homeFunctions": D.HOME_FUNCTIONS,
            "courses": D.COURSES,
            "notices": D.NOTICES,
            "messages": D.MESSAGES,
            "inspectionFuncs": D.INSPECTION_FUNCS,
            "orgTree": D.ORG_TREE,
            "scenes": D.SCENES,
            "effects": D.PHOTO_EFFECTS,
        }
    )


@app.get("/api/orgs")
def orgs():
    return jsonify(D.ORG_TREE)


@app.get("/api/scenes")
def scenes():
    return jsonify(D.SCENES)


@app.get("/api/scenes/<scene_id>")
def scene_detail(scene_id):
    scene = next((s for s in D.SCENES if s["id"] == scene_id), None)
    if not scene:
        abort(404)
    return jsonify(scene)


@app.get("/api/license/records/<org_code>")
def license_record(org_code):
    record = D.LICENSE_RECORDS.get(org_code)
    if not record:
        return jsonify({"error": "该机构暂无备案数据"}), 404
    return jsonify(record)


@app.get("/api/messages")
def messages():
    return jsonify(D.MESSAGES)


@app.get("/api/notices")
def notices():
    return jsonify(D.NOTICES)


# ---------------- 质量校验（拍摄步骤实时反馈） ----------------

@app.post("/api/quality/material")
def quality_material():
    body = request.get_json(silent=True) or {}
    photos = body.get("photos") or []
    ok, msgs = material_quality(photos)
    return jsonify({"ok": ok, "messages": msgs})


@app.post("/api/quality/license")
def quality_license():
    body = request.get_json(silent=True) or {}
    photos = body.get("photos") or []
    ok, msgs = license_quality(photos)
    return jsonify({"ok": ok, "messages": msgs})


# ---------------- 提交检查 ----------------

@app.post("/api/checks/material")
def submit_material():
    body = request.get_json(silent=True) or {}
    org = body.get("org") or {}
    scene_id = body.get("sceneId")
    photos = body.get("photos") or []

    result = check_material(org.get("code"), scene_id, photos)
    if "error" in result:
        return jsonify(result), 400

    scene_name = next((s["name"] for s in D.SCENES if s["id"] == scene_id), "")
    db.save_check(
        check_type="material",
        org_name=org.get("name", ""),
        org_code=org.get("code", ""),
        scene=scene_name,
        result=result["result"],
        photo_count=len(photos),
        detail=json.dumps(result.get("anomalies", []), ensure_ascii=False),
    )
    return jsonify(result)


@app.post("/api/checks/license")
def submit_license():
    body = request.get_json(silent=True) or {}
    org = body.get("org") or {}
    photos = body.get("photos") or []

    result = check_license(org.get("code"), photos)
    if "error" in result:
        return jsonify(result), 400

    db.save_check(
        check_type="license",
        org_name=org.get("name", ""),
        org_code=org.get("code", ""),
        scene="金融许可证核验",
        result=result["result"],
        photo_count=len(photos),
        detail=json.dumps(result.get("diffs", []), ensure_ascii=False),
    )
    return jsonify(result)


# ---------------- 检查记录 ----------------

@app.get("/api/checks")
def checks():
    limit = request.args.get("limit", default=20, type=int)
    return jsonify({"items": db.list_checks(limit), "stats": db.stats()})


# ---------------- 前端静态托管（生产） ----------------

@app.get("/")
@app.get("/<path:path>")
def serve_spa(path=""):
    if path.startswith("api/"):
        abort(404)
    if path:
        target = os.path.join(DIST, path)
        if os.path.isfile(target):
            return send_from_directory(DIST, path)
    index_file = os.path.join(DIST, "index.html")
    if os.path.isfile(index_file):
        return send_from_directory(DIST, "index.html")
    return (
        jsonify(
            {
                "message": "前端尚未构建",
                "hint": "cd frontend && npm install && npm run build",
            }
        ),
        200,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
