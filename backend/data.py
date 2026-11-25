"""种子数据：机构、场景、岗位、课程、备案信息等。

说明：本文件中的机构、网点、人员、地址均为示例数据，不含真实业务信息。
"""

BRAND = {"name": "华信员工 3.0", "short": "华信银行"}

USER = {
    "name": "张三",
    "title": "副科长",
    "role": "风险检查管理岗",
    "roleCode": "440000000",
    "org": "华信银行股份有限公司广东省分行",
    "dept": "渠道与运营管理部内控督导科",
    "branch": "华信银行长堤支行",
    "branchRole": "网点负责人",
    "avatar": "张",
}

POSITIONS = [
    {"name": "风险检查管理岗", "code": "440000000", "desc": "渠道与运营管理部内控督导科"},
    {"name": "网点运营督导岗", "code": "440000001", "desc": "渠道与运营管理部"},
    {"name": "内控合规审查岗", "code": "440000002", "desc": "内控合规部"},
    {"name": "网点负责人", "code": "440000003", "desc": "华信银行长堤支行"},
]

ORG_TREE = [
    {
        "name": "华信银行广东省分行",
        "code": "440000000",
        "children": [
            {
                "name": "华信银行广州分行",
                "code": "440100000",
                "children": [
                    {"name": "华信银行长堤支行", "code": "440100101"},
                    {"name": "华信银行惠福西路支行", "code": "440100102"},
                ],
            },
            {
                "name": "华信银行珠海分行",
                "code": "440400000",
                "children": [
                    {"name": "华信银行湖心路支行", "code": "440400201"},
                    {"name": "华信银行航空新城支行", "code": "440400202"},
                ],
            },
        ],
    }
]

SCENES = [
    {
        "id": "scene1",
        "name": "场景1：自助银行区域",
        "requirements": {
            "public": "自助银行区域需公示操作指引、风险提示及客服电话，公示材料摆放规范、内容完整。",
            "detail": "识别要求：物料摆放方向正常、没有旋转；物料文字清晰；单张照片物料不超过 8 个。",
        },
        "anomalies": [
            "海报上存在二维码",
            "海报上存在连续 5-11 位数字",
            "海报上存在 020、0755 等区号前缀",
            "海报上包含电话、热线等关键字",
        ],
    },
    {
        "id": "scene2",
        "name": "场景2：公众教育栏位",
        "requirements": {
            "public": "公众教育栏位需公示客户投诉渠道及处理流程等宣教材料，摆放规范、内容完整。",
            "detail": "识别要求：物料摆放方向正常、没有旋转；物料文字清晰；材料名称符合公示要求。",
        },
        "anomalies": [
            "公示材料名称不是客户投诉渠道及处理流程",
            "海报上存在二维码",
            "海报上包含电话、热线等关键字",
            "物料摆放歪斜、未对准定位框",
        ],
    },
    {
        "id": "scene3",
        "name": "场景3：大堂",
        "requirements": {
            "public": "大堂服务区需公示服务价目表、业务流程及投诉处理流程，摆放醒目、分类清晰。",
            "detail": "识别要求：物料摆放方向正常、没有旋转；物料文字清晰；单张照片物料不超过 8 个。",
        },
        "anomalies": [
            "海报上存在二维码",
            "价目表中存在连续 5-11 位数字",
            "海报上包含电话、热线等关键字",
            "公示材料名称与要求不符",
        ],
    },
    {
        "id": "scene4",
        "name": "场景4：（后台自定义）",
        "requirements": {
            "public": "按后台自定义规则配置公示要求，检查对应物料的摆放规范性。",
            "detail": "识别要求：以系统后台配置的物料摆放识别规则为准。",
        },
        "anomalies": [
            "海报上存在二维码",
            "海报上存在连续数字串",
            "海报上包含联系方式关键字",
            "物料内容与备案要求不符",
        ],
    },
]

LICENSE_RECORDS = {
    "440100101": {
        "code": "440100101-LIC",
        "name": "华信银行股份有限公司广州长堤支行",
        "address": "广州市越秀区长堤大马路 318 号大楼首层前后座、阁楼",
    },
    "440100102": {
        "code": "440100102-LIC",
        "name": "华信银行股份有限公司广州惠福西路支行",
        "address": "广州市越秀区惠福西路 66 号",
    },
    "440400201": {
        "code": "440400201-LIC",
        "name": "华信银行股份有限公司珠海湖心路支行",
        "address": "珠海市金湾区湖心路 128 号",
    },
    "440400202": {
        "code": "440400202-LIC",
        "name": "华信银行股份有限公司珠海航空新城支行",
        "address": "珠海市金湾区航空新城 8 号",
    },
}

# 拍摄效果可选值（前端展示用）
PHOTO_EFFECTS = {
    "material": [
        {"id": "normal", "label": "正确拍摄"},
        {"id": "content", "label": "存在内容异常"},
        {"id": "blur", "label": "模糊"},
        {"id": "lowres", "label": "分辨率不足"},
    ],
    "license": [
        {"id": "normal", "label": "正确拍摄"},
        {"id": "mismatch", "label": "信息不一致"},
        {"id": "blur", "label": "模糊"},
        {"id": "lowres", "label": "分辨率不足"},
    ],
}

HOME_FUNCTIONS = [
    {"id": "todo", "label": "事务待办", "icon": "assets/home/u77.svg", "grad": "linear-gradient(154.44deg,#1b94f9 8%,#3fdffe 91%)"},
    {"id": "schedule", "label": "日程管理", "icon": "assets/home/u78.svg", "grad": "linear-gradient(135deg,#a36aff 0%,#1b94f9 100%)"},
    {"id": "learn", "label": "华信学习", "icon": "assets/home/u79.svg", "grad": "linear-gradient(135deg,#a36aff 0%,#1b94f9 100%)"},
    {"id": "wiki", "label": "知识百科", "icon": "assets/home/u80.svg", "grad": "linear-gradient(135deg,#a36aff 0%,#1b94f9 100%)"},
    {"id": "welfare", "label": "员工福利", "icon": "assets/home/u81.svg", "grad": "linear-gradient(135deg,#ffad4a 0%,#ffc92d 100%)"},
    {"id": "travel", "label": "员工差旅", "icon": "assets/home/u82.svg", "grad": "linear-gradient(154.44deg,#1b94f9 8%,#3fdffe 91%)"},
    {"id": "leave", "label": "员工请假", "icon": "assets/home/u83.svg", "grad": "linear-gradient(135deg,#ff5b8c 0%,#ff9ebb 100%)"},
    {"id": "product", "label": "产品服务", "icon": "assets/home/u84.svg", "grad": "linear-gradient(154.44deg,#1b94f9 8%,#3fdffe 91%)"},
    {"id": "hr", "label": "人力资源", "icon": "assets/home/u85.svg", "grad": "linear-gradient(135deg,#14d4dc 0%,#22d8a0 100%)"},
    {"id": "ai", "label": "AI助手", "icon": "assets/home/u86.svg", "grad": "linear-gradient(135deg,#ffad4a 0%,#ffc92d 100%)"},
    {"id": "rule", "label": "制度检索", "icon": "assets/home/u87.svg", "grad": "linear-gradient(154.44deg,#1b94f9 8%,#3fdffe 91%)"},
    {"id": "more", "label": "更多功能", "icon": "assets/home/u88.svg", "grad": "linear-gradient(135deg,#5b8def 0%,#1b94f9 100%)"},
]

COURSES = [
    {"title": "客户信息九要素代理维护规范"},
    {"title": "【投诉处理之技巧方法】之如何正确地看待投诉..."},
]

INSPECTION_FUNCS = [
    {
        "id": "license",
        "title": "金融许可证核验",
        "desc": "核验机构金融许可证的实物状态合规性与信息一致性",
        "descLong": "通过拍摄金融许可证，自动识别并与新一代网点管理系统备案数据比对，核验信息一致性。",
        "color": "#1b94f9",
        "icon": "card",
    },
    {
        "id": "material",
        "title": "宣传物料摆放规范性检查",
        "desc": "根据不同场景的物料摆放规则，检查宣传物料的摆放是否合规",
        "descLong": "根据不同场景的物料摆放规则，检查宣传物料的摆放是否合规。",
        "color": "#14d4dc",
        "icon": "image",
    },
]

NOTICES = [
    "+02-03 09:22 宣传物料摆放规范性检查，使用人 XX部-李四",
    "+02-01 14:05 金融许可证核验任务已下发，请及时处理",
]

MESSAGES = [
    {"title": "检查标准更新通知", "desc": "宣传物料识别规则 v2.0 已上线", "time": "09:30"},
    {"title": "检查任务已完成", "desc": "华信银行长堤支行 · 物料检查已通过", "time": "昨天"},
]
