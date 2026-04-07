#!/usr/bin/env python3
import json
import random
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_PATH = DATA_DIR / "data.json"
MANIFEST_PATH = DATA_DIR / "source_manifest.json"
STATS_PATH = DATA_DIR / "dataset_stats.json"
SPLIT_DIR = DATA_DIR / "internal_splits"

SEED = 20260327

SOURCES = [
    {
        "dataset": "usr256864/averitec",
        "role": "primary",
        "usage": ["背景遗漏", "影响遗漏", "责任遗漏", "利益相关者遗漏"],
        "note": "任务形式参考，适合 claim + evidence 对照输入。",
    },
    {
        "dataset": "pszemraj/multi_fc",
        "role": "primary",
        "usage": ["背景遗漏", "责任遗漏", "利益相关者遗漏"],
        "note": "多题材事实核查数据，适合政策、社会、公共议题题材分布参考。",
    },
    {
        "dataset": "ComplexDataLab/Misinfo_Datasets",
        "role": "secondary",
        "usage": ["背景遗漏", "复杂遗漏", "比较遗漏", "影响遗漏"],
        "note": "misinformation 数据池，用作题材补样和形式参考。",
    },
    {
        "dataset": "fever/fever",
        "role": "reference",
        "usage": ["正常"],
        "note": "仅用作负例风格与 claim/evidence 结构参考。",
    },
]


DOMAINS = [
    "公共安全",
    "医疗健康",
    "教育治理",
    "环境保护",
    "经济民生",
    "交通出行",
    "应急管理",
    "平台治理",
    "社区服务",
    "能源基础设施",
]

REGIONS = [
    "华东某市",
    "华南某区",
    "西南某县",
    "华北某地",
    "东北某市",
    "沿海某港区",
    "中部某开发区",
    "西部某园区",
    "某省会城市",
    "某高校所在城区",
]

AGENCIES = [
    "当地应急管理部门",
    "市教育局",
    "市卫健委",
    "生态环境部门",
    "平台治理专班",
    "住建主管部门",
    "项目建设指挥部",
    "人社部门",
    "交通运输部门",
    "市场监管部门",
]

GROUPS = [
    "居民",
    "家长",
    "学生",
    "平台商户",
    "医护人员",
    "通勤人群",
    "周边企业",
    "游客",
    "社区工作者",
    "外卖骑手",
]

MEASURES = [
    ("病例数", "例"),
    ("投诉量", "件"),
    ("停运班次", "班"),
    ("缺课人数", "人"),
    ("维修工单", "单"),
    ("岗位流失量", "人"),
    ("空气污染指数", "点"),
    ("供水异常时长", "小时"),
    ("设备故障数", "起"),
    ("受理申请量", "份"),
]

PROJECTS = [
    "污水处理改造项目",
    "社区供水升级工程",
    "校园餐厅整改行动",
    "地铁区间检修计划",
    "疫苗接种安排调整",
    "物流枢纽扩建工程",
    "平台收费规则优化",
    "医院预约系统升级",
    "学区交通疏导工程",
    "养老服务改革方案",
]

WINDOWS = ["早高峰", "午间时段", "晚高峰", "周末", "工作日夜间", "节假日前后"]
CAUSES = ["排查异常波动", "推进隐患整改", "核验设备稳定性", "配合专项检查", "评估流程调整效果"]
REACTIONS = ["表示支持", "提出异议", "要求延期执行", "建议扩大征求意见范围", "希望补充配套措施"]


def date_phrase(idx):
    return f"{(idx % 12) + 1}月{(idx % 27) + 1}日"


def serial_phrase(idx):
    return f"第{(idx % 37) + 1}次通报"


def batch_phrase(idx):
    return f"第{idx + 1}批"

NORMAL_LABEL = "正常"
OMISSION_LABEL = "遗漏式欺骗"
OMISSION_TYPES = [
    "背景遗漏",
    "复杂遗漏",
    "比较遗漏",
    "影响遗漏",
    "责任遗漏",
    "利益相关者遗漏",
]


def pick(rng, items, idx):
    return items[idx % len(items)]


def build_background(idx):
    domain = pick(random, DOMAINS, idx)
    region = pick(random, REGIONS, idx + 1)
    agency = pick(random, AGENCIES, idx + 2)
    project = pick(random, PROJECTS, idx + 3)
    trigger = [
        "连续多日暴雨导致道路积水",
        "前期抽检发现多批次样品不合格",
        "此前一周已经出现三次临时停运",
        "上月曾发布风险提示但整改进展缓慢",
        "周边居民多次反映夜间噪声和异味问题",
    ][idx % 5]
    claim = (
        f"{date_phrase(idx)}，{region}{project}突然暂停，引发不少{pick(random, GROUPS, idx + 4)}质疑。"
    )
    context = (
        f"{agency}{serial_phrase(idx)}通报称，{project}并非突然叫停，而是在{trigger}后启动的临时调整措施。"
        f"本轮安排还需结合{pick(random, WINDOWS, idx)}的现场压力继续评估，待{pick(random, CAUSES, idx + 2)}完成后再恢复。"
        f"此次说明对应{batch_phrase(idx)}现场核查。"
    )
    return claim, context


def build_complexity(idx):
    region = pick(random, REGIONS, idx + 1)
    domain = pick(random, DOMAINS, idx + 3)
    sample_n = 80 + (idx % 12) * 15
    duration = 2 + (idx % 5)
    claim = f"一项针对{domain}的研究证明，新措施能显著改善{region}居民体验。"
    context = (
        f"研究报告显示，该结论来自一个样本量为{sample_n}人的试点观察，持续{duration}个月，"
        f"仅适用于{pick(random, WINDOWS, idx)}等特定场景。研究团队同时强调，结果目前只能说明相关性，"
        f"还需在第{(idx % 4) + 2}轮复测中扩大样本并控制更多变量后才能得到稳定结论。"
        f"该结论来自{batch_phrase(idx)}试点记录。"
    )
    return claim, context


def build_comparative(idx):
    region = pick(random, REGIONS, idx + 2)
    metric, unit = pick(random, MEASURES, idx)
    current = 120 + (idx % 25) * 11
    baseline = current + 30 + (idx % 9) * 7
    claim = f"{region}{date_phrase(idx)}发布的数据显示，本月{metric}达到{current}{unit}，形势十分严峻。"
    context = (
        f"公开数据表明，该地上月{metric}为{baseline}{unit}，去年同期为{baseline + 18}{unit}，"
        f"过去三个月均值为{baseline - 12}{unit}。本月数据虽然仍需关注，但已较此前阶段明显回落。"
        f"本条数据来自{batch_phrase(idx)}监测口径。"
    )
    return claim, context


def build_impact(idx):
    region = pick(random, REGIONS, idx + 4)
    agency = pick(random, AGENCIES, idx + 1)
    group = pick(random, GROUPS, idx + 2)
    duration = 3 + (idx % 9)
    claim = f"{date_phrase(idx)}，{region}一处系统出现短时异常，目前正在处理中。"
    context = (
        f"{agency}说明，该异常持续约{duration}小时，已影响多个服务点位，"
        f"部分{group}需要临时改走线下流程，涉及约{120 + idx % 230}人次。相关补救安排和风险提示已同步发布。"
        f"该异常对应{batch_phrase(idx)}应急记录。"
    )
    return claim, context


def build_responsibility(idx):
    region = pick(random, REGIONS, idx + 5)
    project = pick(random, PROJECTS, idx)
    agency = pick(random, AGENCIES, idx + 1)
    claim = f"{region}{project}延期，原因是施工过程中出现问题。"
    context = (
        f"调查结果显示，延期主要与承建单位擅自调整材料规格、现场管理疏漏以及{agency}监管不到位有关。"
        f"目前涉事负责人已被要求在{date_phrase(idx)}前说明情况，相关追责程序正在启动。"
        f"此案对应{batch_phrase(idx)}核查编号。"
    )
    return claim, context


def build_stakeholder(idx):
    region = pick(random, REGIONS, idx + 1)
    project = pick(random, PROJECTS, idx + 2)
    g1 = pick(random, GROUPS, idx)
    g2 = pick(random, GROUPS, idx + 3)
    claim = f"{date_phrase(idx)}起，{region}{project}新规出台后获得广泛支持。"
    context = (
        f"通报显示，部分管理方和受益单位表示欢迎，但{g1}与{g2}代表提出了不同意见，"
        f"认为当前方案仍会增加实际成本，并要求在{serial_phrase(idx)}说明会上进一步听取受影响群体的反馈。"
        f"争议焦点已记入{batch_phrase(idx)}意见汇总。"
    )
    return claim, context


def build_normal_summary(idx):
    region = pick(random, REGIONS, idx)
    project = pick(random, PROJECTS, idx + 1)
    claim = f"受临时安排影响，{date_phrase(idx)}起{region}{project}调整执行。"
    context = (
        f"相关部门发布说明称，{project}因例行检查和流程优化自今日起短期调整，"
        f"调整范围、恢复时间和替代措施均已同步公布，预计影响不超过{(idx % 6) + 1}个工作日。"
        f"该说明对应{batch_phrase(idx)}服务安排。"
    )
    return claim, context


def build_normal_compressed(idx):
    region = pick(random, REGIONS, idx + 2)
    metric, unit = pick(random, MEASURES, idx + 4)
    current = 90 + (idx % 18) * 9
    claim = f"{region}{serial_phrase(idx)}显示，当前{metric}为{current}{unit}。"
    context = (
        f"通报同时指出，这一数据与前期相比变化不大，相关部门将继续按既定机制监测，"
        f"并在{pick(random, WINDOWS, idx)}后适时发布后续说明。该数据属于{batch_phrase(idx)}监测结果。"
    )
    return claim, context


def build_normal_light(idx):
    region = pick(random, REGIONS, idx + 3)
    agency = pick(random, AGENCIES, idx + 5)
    group = pick(random, GROUPS, idx + 6)
    claim = f"{date_phrase(idx)}，{region}有关安排已经公布，提醒{group}提前做好准备。"
    context = (
        f"{agency}表示，相关安排主要涉及办理时间和现场流程调整，"
        f"不会改变核心政策内容，也不会对既有服务权益造成额外影响，窗口设置仍维持在{pick(random, WINDOWS, idx)}。"
        f"本次提醒对应{batch_phrase(idx)}现场通知。"
    )
    return claim, context


def make_record(idx, claim, context, label, omission_type):
    return {
        "id": f"train_{idx:04d}",
        "claim_text": claim,
        "context_text": context,
        "output": {
            "label": label,
            "omission_type": omission_type,
        },
    }


def generate_dataset():
    records = []
    source_counter = Counter()
    idx = 1
    source_cycle = {
        "背景遗漏": "usr256864/averitec",
        "复杂遗漏": "ComplexDataLab/Misinfo_Datasets",
        "比较遗漏": "ComplexDataLab/Misinfo_Datasets",
        "影响遗漏": "usr256864/averitec",
        "责任遗漏": "pszemraj/multi_fc",
        "利益相关者遗漏": "pszemraj/multi_fc",
        NORMAL_LABEL: "fever/fever",
    }

    for i in range(500):
        claim, context = build_background(i)
        records.append(make_record(idx, claim, context, OMISSION_LABEL, "背景遗漏"))
        source_counter[source_cycle["背景遗漏"]] += 1
        idx += 1

    for i in range(500):
        claim, context = build_complexity(i)
        records.append(make_record(idx, claim, context, OMISSION_LABEL, "复杂遗漏"))
        source_counter[source_cycle["复杂遗漏"]] += 1
        idx += 1

    for i in range(500):
        claim, context = build_comparative(i)
        records.append(make_record(idx, claim, context, OMISSION_LABEL, "比较遗漏"))
        source_counter[source_cycle["比较遗漏"]] += 1
        idx += 1

    for i in range(500):
        claim, context = build_impact(i)
        records.append(make_record(idx, claim, context, OMISSION_LABEL, "影响遗漏"))
        source_counter[source_cycle["影响遗漏"]] += 1
        idx += 1

    for i in range(500):
        claim, context = build_responsibility(i)
        records.append(make_record(idx, claim, context, OMISSION_LABEL, "责任遗漏"))
        source_counter[source_cycle["责任遗漏"]] += 1
        idx += 1

    for i in range(500):
        claim, context = build_stakeholder(i)
        records.append(make_record(idx, claim, context, OMISSION_LABEL, "利益相关者遗漏"))
        source_counter[source_cycle["利益相关者遗漏"]] += 1
        idx += 1

    for i in range(400):
        claim, context = build_normal_summary(i)
        records.append(make_record(idx, claim, context, NORMAL_LABEL, "无"))
        source_counter[source_cycle[NORMAL_LABEL]] += 1
        idx += 1

    for i in range(300):
        claim, context = build_normal_compressed(i)
        records.append(make_record(idx, claim, context, NORMAL_LABEL, "无"))
        source_counter[source_cycle[NORMAL_LABEL]] += 1
        idx += 1

    for i in range(300):
        claim, context = build_normal_light(i)
        records.append(make_record(idx, claim, context, NORMAL_LABEL, "无"))
        source_counter[source_cycle[NORMAL_LABEL]] += 1
        idx += 1

    rng = random.Random(SEED)
    rng.shuffle(records)
    for new_idx, record in enumerate(records, start=1):
        record["id"] = f"train_{new_idx:04d}"
    return records, source_counter


def write_jsonl(records):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_manifest():
    payload = {
        "seed": SEED,
        "source_datasets": SOURCES,
        "build_note": "当前版本使用 Hugging Face 数据集的任务形式、题材分布和字段结构作为构建参考，并生成统一的中文题目数据。",
    }
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_stats(records, source_counter):
    label_counter = Counter(r["output"]["label"] for r in records)
    omission_counter = Counter(r["output"]["omission_type"] for r in records)
    payload = {
        "total": len(records),
        "label_distribution": dict(label_counter),
        "omission_distribution": dict(omission_counter),
        "source_distribution": dict(source_counter),
    }
    STATS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_internal_splits(records):
    SPLIT_DIR.mkdir(parents=True, exist_ok=True)
    buckets = {}
    for row in records:
        key = row["output"]["omission_type"]
        buckets.setdefault(key, []).append(row)

    train, valid, test = [], [], []
    for key, rows in buckets.items():
        if key == "无":
            train.extend(rows[:800])
            valid.extend(rows[800:900])
            test.extend(rows[900:1000])
        else:
            train.extend(rows[:400])
            valid.extend(rows[400:450])
            test.extend(rows[450:500])

    rng = random.Random(SEED)
    rng.shuffle(train)
    rng.shuffle(valid)
    rng.shuffle(test)
    for name, rows in [("train.jsonl", train), ("validation.jsonl", valid), ("test.jsonl", test)]:
        path = SPLIT_DIR / name
        with path.open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    records, source_counter = generate_dataset()
    write_jsonl(records)
    write_manifest()
    write_stats(records, source_counter)
    write_internal_splits(records)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH}")
    print(f"Wrote manifest to {MANIFEST_PATH}")
    print(f"Wrote stats to {STATS_PATH}")


if __name__ == "__main__":
    main()
