# -*- coding: utf-8 -*-
"""经纬系列门户 · 系列账本（数字唯一来源 = 各站脚本产物）

python tools/build_series_stats.py          # 读六站产物 → docs/series-stats.json
python tools/build_series_stats.py --check  # 校验 README/index.html 卡片数字与产物一致，漂移即 exit 1

门户卡片第二行的风味短语（如「盘江考溯江纪源俱在」）保持手写——本脚本只锁数字 token，
因为数字才会因各站数据演进而漂移，短语不会。
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(os.path.dirname(ROOT))  # D:/W_A_W


def load(rel):
    return io.open(os.path.join(W, rel), encoding="utf-8").read()


def loadj(rel):
    return json.loads(load(rel))


def fmt_wan(n):  # 461590 → "46.2 万"
    return "%.1f 万" % (n / 10000.0)


def thousands(n):  # 24631 → "24,631"
    return "{:,}".format(n)


# ── 各站提取器（读各站自己的脚本产物；任一站缺件即响，不静默跳过）──

def ext_fangyu():
    t = load("HHH/data/site_data.js")
    sd = json.loads(t[t.find("{"): t.rfind("}") + 1])
    fus = counties = 0
    for p in sd["provinces"]:
        for f in p["fu"]:
            fus += 1 + len(f.get("zhou", []))          # 府 + 属州 = 府州 380（check_stats 口径）
            counties += len(f.get("xian", []))
            for z in f.get("zx", []):                   # 县总数 = xian + zx[].x = 1111（check_stats 口径）
                counties += len(z.get("x", []))
    return {"fus": fus, "counties": counties}


def ext_shuidao():
    t = load("SDJW/data/river_data.js")
    sjz = json.loads(t[t.find("const SJZ = ") + len("const SJZ = "):].rstrip().rstrip(";"))
    cites = loadj("SDJW/data/intermediate/citations.json")
    x = load("SDJW/data/crossref.js")
    m = re.search(r'"total"\s*:\s*(\d+)', x)
    return {"waterways": sjz["meta"]["waterways"], "cites": len(cites["counts"]),
            "crossref_total": int(m.group(1)) if m else 0}


def ext_xiake():
    s = loadj("XXK/docs/stats.json")["meta"]
    return {"pieces": s["pieces"], "days": s["days"], "anchored": s["anchored"],
            "km": int(round(s["kmTotal"])), "chars": s["charsOrig"]}


def ext_qielan():
    st = loadj("LYGL/docs/stats.json")
    t = load("LYGL/data/site_data.js")
    sd = json.loads(t[t.find("{"): t.rfind("}") + 1])
    wall_gates = [g for g in sd["gates"] if g.get("wall") in ("东", "南", "西", "北")]
    return {"temples": len(sd["temples"]), "gates": len(wall_gates), "wards": len(sd["wards"]),
            "chars": st["total_chars"]}


def ext_yuanhe():
    s = loadj("YHJZ/data/stats.json")
    return {"states": s["states"], "counties": s["counties_listed"], "chars": s["fetch"]["total_chars"]}


def ext_huanyu():
    s = loadj("TPHY/docs/stats.json")
    return {"prefects": s["zhou_count"], "counties": s["xian_count"],
            "chars": s["total_chars"], "mapped": s["xian_coord"]}


EXTRACTORS = {"fangyu": ext_fangyu, "shuidao": ext_shuidao, "xiake": ext_xiake,
              "qielan": ext_qielan, "yuanhe": ext_yuanhe, "huanyu": ext_huanyu}


def collect():
    out = {}
    for k, fn in EXTRACTORS.items():
        out[k] = fn()
    return out


# ── 门户卡片数字 token 期望（模板与 index.html 卡片逐一对应）──

def card_tokens(d):
    fy, sd, xk, ql, yh, hy = (d["fangyu"], d["shuidao"], d["xiake"],
                              d["qielan"], d["yuanhe"], d["huanyu"])
    return {
        "fangyu-jingwei": ["府州 %d" % fy["fus"], "县 %d" % fy["counties"]],
        "shuidao-jingwei": ["水道 %d" % sd["waterways"], "引书考古 %d 种" % sd["cites"],
                            "引水经注 %d 次" % sd["crossref_total"]],
        "xiake-jingwei": ["日条 %d" % xk["days"], "锚点 %d" % xk["anchored"],
                          "里程 %s km" % thousands(xk["km"]), "原文 %s" % fmt_wan(xk["chars"])],
        "qielan-jingwei": ["伽蓝 %d" % ql["temples"], "墙门 %d" % ql["gates"], "里坊 %d" % ql["wards"],
                           "白文 %s" % fmt_wan(ql["chars"])],
        "yuanhe-jingwei": ["州府 %d" % yh["states"], "县 %d" % yh["counties"], "语料 %s" % fmt_wan(yh["chars"])],
        "huanyu-jingwei": ["府州军监 %d" % hy["prefects"], "县 %d" % hy["counties"],
                           "全文 %s" % fmt_wan(hy["chars"]), "县上图 %d" % hy["mapped"]],
    }


def check():
    d = collect()
    toks = card_tokens(d)
    html = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    problems = []
    for repo, want in toks.items():
        m = re.search(r'href="https://v-t-v\.github\.io/%s/".*?(?=<a class="card"|\Z)' % repo, html, re.S)
        if not m:
            problems.append("%s: 卡片未找到" % repo)
            continue
        card = m.group(0)
        for tk in want:
            if tk.replace(",", ",") not in card:
                # 千分位在 HTML 中亦为半角逗号，直接判
                problems.append("%s: 缺数字 token「%s」" % (repo, tk))
    for p in problems:
        print("✗ " + p)
    if problems:
        print("门户数字漂移 %d 处——改站数据后须同步 index.html 或调整提取器" % len(problems))
        sys.exit(1)
    print("门户数字与六站脚本产物全符（%d 站 × %d token）" % (len(toks), sum(len(v) for v in toks.values())))


def build():
    d = collect()
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    io.open(os.path.join(ROOT, "docs", "series-stats.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(d, ensure_ascii=False, indent=2))
    print("docs/series-stats.json 写出（六站）")
    for k, v in d.items():
        print("  %s: %s" % (k, json.dumps(v, ensure_ascii=False)[:120]))


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        build()
