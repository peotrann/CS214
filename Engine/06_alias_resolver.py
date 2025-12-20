# 06_alias_resolver.py
import re

def normalize_text(s):
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"[^\w\s<>=>]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# PHƯƠNG TIỆN (6/6)
MANUAL_PT_ALIAS = {
    "ô tô": "PT01",
    "xe ô tô": "PT01",
    "xe hơi": "PT01",
    "xe bốn bánh": "PT01",
    "rơ moóc": "PT01",
    "sơ mi rơ moóc": "PT01",

    "xe máy": "PT02",
    "mô tô": "PT02",
    "xe gắn máy": "PT02",
    "xe máy điện": "PT02",

    "máy kéo": "PT03",
    "xe chuyên dùng": "PT03",

    "xe đạp": "PT04",
    "xe đạp điện": "PT04",

    "xe thô sơ": "PT05",
    "xích lô": "PT05",
    "xe súc vật kéo": "PT05",

    "người đi bộ": "PT06",
    "người đi đường": "PT06",
}

# HÀNH VI (32/32)
MANUAL_HV_ALIAS = {
    "không chấp hành biển báo": "HV01",
    "không chấp hành vạch kẻ đường": "HV01",

    "vượt đèn đỏ": "HV02",
    "không chấp hành đèn tín hiệu": "HV02",

    "không chấp hành hiệu lệnh csgt": "HV03",
    "không chấp hành chỉ huy giao thông": "HV03",

    "chuyển hướng trái quy định": "HV04",
    "rẽ sai quy định": "HV04",

    "dừng xe trái quy định": "HV05",
    "dừng xe sai nơi": "HV05",

    "đỗ xe trái quy định": "HV06",
    "đỗ xe sai nơi": "HV06",

    "chuyển làn trái quy định": "HV07",

    "bấm còi trái quy định": "HV08",
    "dùng đèn pha sai quy định": "HV08",

    "chạy quá tốc độ": "HV09",
    "vượt quá tốc độ": "HV09",

    "không giữ khoảng cách an toàn": "HV10",

    "dùng điện thoại khi lái xe": "HV11",
    "sử dụng thiết bị khi lái xe": "HV11",

    "đi vào đường cấm": "HV12",

    "đi ngược chiều": "HV13",

    "vượt xe trái quy định": "HV14",

    "đi sai làn": "HV15",
    "đi sai phần đường": "HV15",

    "vi phạm nồng độ cồn": "HV16",
    "uống rượu bia lái xe": "HV16",

    "sử dụng ma túy": "HV17",

    "không đội mũ bảo hiểm": "HV18",

    "không thắt dây an toàn": "HV19",

    "lạng lách đánh võng": "HV20",

    "không dừng lại sau tai nạn": "HV21",
    "bỏ trốn sau tai nạn": "HV21",

    "vi phạm giấy tờ": "HV22",
    "không có giấy tờ": "HV22",

    "ném vật thể nguy hiểm": "HV23",

    "dẫn dắt vật nuôi trái quy định": "HV24",

    "vi phạm an toàn kỹ thuật": "HV25",

    "vi phạm vệ sinh môi trường": "HV26",
    "đổ rác ra đường": "HV26",

    "quay đầu trái quy định": "HV27",

    "lùi xe trái quy định": "HV28",

    "chở quá số người": "HV29",
    "chở hàng quá quy định": "HV29",

    "vi phạm biển số": "HV30",
}

# ĐIỀU KIỆN (30/30)
MANUAL_DK_ALIAS = {
    "nồng độ cồn mức 1": "DK01",
    "cồn dưới 50mg": "DK01",

    "nồng độ cồn mức 2": "DK02",
    "cồn 50 đến 80mg": "DK02",

    "nồng độ cồn mức 3": "DK03",
    "cồn trên 80mg": "DK03",

    "quá tốc độ 5": "DK04",
    "quá tốc độ 5 đến 10": "DK04",

    "quá tốc độ 10 đến 20": "DK05",

    "quá tốc độ 20 đến 35": "DK06",

    "quá tốc độ trên 35": "DK07",

    "mô tô quá tốc độ trên 20": "DK08",

    "không mang giấy tờ": "DK09",

    "không có giấy tờ": "DK10",
    "giấy tờ hết hạn": "DK10",

    "giấy tờ giả": "DK11",
    "tẩy xóa giấy tờ": "DK11",

    "không rõ nguồn gốc": "DK12",

    "gây tai nạn": "DK13",
    "tai nạn giao thông": "DK13",

    "bỏ trốn sau tai nạn": "DK14",

    "không chấp hành kiểm tra": "DK15",

    "dưới 16 tuổi": "DK16",
    "14 đến dưới 16": "DK16",

    "16 đến dưới 18": "DK17",

    "hỏng phanh": "DK18",
    "hỏng lái": "DK18",

    "hỏng đèn": "DK19",
    "hỏng còi": "DK19",
    "hỏng gương": "DK19",

    "lắp đèn trái phép": "DK20",

    "che biển số": "DK21",
    "biển số giả": "DK21",

    "rơi vãi dầu": "DK22",
    "rơi vãi hóa chất": "DK22",

    "đổ phế thải": "DK23",

    "trong hầm": "DK24",
    "hầm đường bộ": "DK24",

    "trên cao tốc": "DK25",

    "chở từ 3 người": "DK26",

    "tổ chức vi phạm": "DK27",

    "tái phạm": "DK28",

    "dưới 175cc": "DK29",

    "trên 175cc": "DK30",
}

# RESOLVER CORE
def resolve_alias(text, alias_map):
    text = normalize_text(text)
    matches = []

    for phrase, _id in alias_map.items():
        if phrase in text:
            matches.append((len(phrase), _id))

    if not matches:
        return None

    matches.sort(reverse=True)
    return matches[0][1]

def resolve_vehicle(text):
    return resolve_alias(text, MANUAL_PT_ALIAS)

def resolve_action(text):
    return resolve_alias(text, MANUAL_HV_ALIAS)

def resolve_condition(text):
    return resolve_alias(text, MANUAL_DK_ALIAS)
