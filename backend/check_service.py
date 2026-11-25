"""检查业务逻辑：图像质量校验、内容异常判定、备案信息一致性比对。

前端上传的是"拍摄结果"的描述（画幅 + 效果类型），本模块据此产出
服务端的校验结论，模拟真实场景中由视觉服务返回的结果。
"""

from data import SCENES, LICENSE_RECORDS

MIN_RESOLUTION = 1440


def _effects(photos):
    return [p.get("effect") for p in photos if isinstance(p, dict)]


# ---------------- 宣传物料 ----------------

def material_quality(photos):
    """返回 (ok, messages)"""
    msgs = []
    for p in photos:
        eff = p.get("effect")
        if eff == "blur" and not any("模糊" in m for m in msgs):
            msgs.append("拍摄的图像质量模糊，请重新拍摄")
        if eff == "lowres" and not any("分辨率" in m for m in msgs):
            msgs.append(f"拍摄的图像分辨率过低，未达到分辨率最低标准 {MIN_RESOLUTION}，请重新提高分辨率拍摄")
    return (len(msgs) == 0), msgs


def material_anomalies(scene_id, photos):
    scene = next((s for s in SCENES if s["id"] == scene_id), None)
    if not scene:
        return []
    if "content" not in _effects(photos):
        return []
    return scene["anomalies"][:3]


def check_material(org, scene_id, photos):
    if not org:
        return {"error": "请选择被查机构！"}
    if not scene_id:
        return {"error": "请选择场景！"}
    if not photos:
        return {"error": "请至少拍摄一张宣传物料照片！"}

    ok, msgs = material_quality(photos)
    if not ok:
        return {"error": "请删除校验不通过的照片后再进行下一步！", "quality": {"ok": False, "messages": msgs}}

    anomalies = material_anomalies(scene_id, photos)
    result = "anomaly" if anomalies else "pass"
    return {
        "quality": {"ok": True, "messages": []},
        "anomalies": anomalies,
        "result": result,
        "photoCount": len(photos),
    }


# ---------------- 金融许可证 ----------------

def license_quality(photos):
    msgs = []
    for p in photos:
        eff = p.get("effect")
        if eff == "blur" and not any("模糊" in m for m in msgs):
            msgs.append("拍摄的金融许可证图像质量模糊，请重新拍摄")
        if eff == "lowres" and not any("分辨率" in m for m in msgs):
            msgs.append(f"拍摄的金融许可证分辨率过低，未达到分辨率最低标准 {MIN_RESOLUTION}")
    return (len(msgs) == 0), msgs


def simulate_ocr(org_code, mismatch):
    """模拟证件识别结果；mismatch=True 时构造与备案不一致的数据。"""
    record = LICENSE_RECORDS.get(org_code)
    if not record:
        return None
    if not mismatch:
        return {"code": record["code"], "name": record["name"], "address": record["address"]}
    return {
        "code": record["code"],
        "name": "华信银行股份有限公司广东省分行",
        "address": "广州市东风中路 509 号",
    }


def compare(record, ocr):
    diffs = []
    if not record or not ocr:
        return diffs
    labels = {"code": "机构编号", "name": "机构名称", "address": "机构地址"}
    for key in ("code", "name", "address"):
        if ocr.get(key) != record.get(key):
            diffs.append({"field": labels[key], "ocr": ocr.get(key), "record": record.get(key)})
    return diffs


def check_license(org_code, photos):
    if not org_code:
        return {"error": "请选择被查机构！"}
    record = LICENSE_RECORDS.get(org_code)
    if not record:
        return {"error": "该机构暂无备案数据"}
    if not photos:
        return {"error": "请拍摄金融许可证照片！"}

    ok, msgs = license_quality(photos)
    if not ok:
        return {"error": "请提供通过校验的金融许可证照片！", "quality": {"ok": False, "messages": msgs}}

    mismatch = "mismatch" in _effects(photos)
    ocr = simulate_ocr(org_code, mismatch)
    diffs = compare(record, ocr)
    return {
        "quality": {"ok": True, "messages": []},
        "record": record,
        "ocr": ocr,
        "diffs": diffs,
        "result": "anomaly" if diffs else "pass",
    }
