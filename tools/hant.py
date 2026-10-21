#!/usr/bin/env python3
"""Generate the Traditional Chinese text of every page from its Simplified text.

Each page carries English, Simplified and Traditional Chinese as sibling spans:

    <span lang="en">…</span><span lang="zh-Hans">…</span><span lang="zh-Hant">…</span>

Edit only the English and the Simplified spans, then run this script from the site root:

    pip install opencc-python-reimplemented
    python3 tools/hant.py            # rewrite the zh-Hant spans in place
    python3 tools/hant.py --check    # exit 1 if any page is out of date

It converts with OpenCC's Taiwan-standard profile (s2twp: Taiwan characters and
vocabulary, e.g. 信息 → 資訊, 数据 → 資料), then applies PHRASES below. Never hand-edit
a zh-Hant span — the next run overwrites it. Put the correction in PHRASES instead.
"""

import argparse
import pathlib
import re
import sys

try:
    from opencc import OpenCC
except ImportError:
    sys.exit("OpenCC is missing: pip install opencc-python-reimplemented")

# Simplified phrase -> Traditional text, applied before OpenCC, longest first.
# Use it for terms OpenCC gets wrong for this site, Taiwan academic usage it
# doesn't know, and proper names that must not be localised.
PHRASES = {
    # OpenCC turns 程序 into 程式 ("software program"), wrong for a programme committee.
    "程序委员会": "程序委員會",
    # Other s2twp misfires on this site's text.
    "通过现行章程": "通過現行章程",   # ratified, not 透過 "via"
    "无法通过验证": "無法通過驗證",
    "类型": "類型",                 # not 型別, a programming "type"
    "循环": "循環",                 # not 迴圈, a programming "loop"
    "表示": "表示",                 # 对表示 would become 對錶 ("pair with a watch")
    "文本": "文本",                 # not 文字, which reads as word processing
    "一个": "一個",                 # not 一箇
    "链接": "連結",                 # 附上链接 would become 附上鍊接
    "发布": "發布",                 # announcements, not 釋出 (software release)
    "高级讲师": "資深講師",
    "实时": "即時",
    "在线": "在線上",
    "设备": "設備",
    "会员门户": "會員入口",
    "证书": "憑證",
    "提供访问": "提供存取",
    # Proper names: keep as the institution writes them.
    "语言大数据与计算人文研究中心": "語言大數據與計算人文研究中心",
    # The logo caption is about the simplified character itself.
    "“汉”": "「汉」",
    # Taiwan NLP terminology.
    "大语言模型": "大型語言模型",
    "语义": "語意",
    "分词": "斷詞",
    "识别": "辨識",
    "拼写": "拼字",
    "抽取": "擷取",
    "挖掘": "探勘",
    "数据增强": "資料擴增",
    "鲁棒性": "穩健性",
    "数字人文": "數位人文",
    "数字化": "數位化",
    "项目": "計畫",
    "质量控制": "品質控制",
    "盲文": "點字",
    "社交媒体": "社群媒體",
    "开放获取": "開放取用",
    "可复用": "可重複使用",
    "许可协议": "授權條款",
    "系统演示": "系統展示",
    "音视频": "影音",
    "网络连接": "網路連線",
    "渠道": "管道",
    "访问": "造訪",
    "邮件列表": "郵件清單",
    "README 文件": "README 檔案",
    "计算机": "電腦",
    # Contact wording.
    "联系方式": "聯絡方式",
    "联系我们": "聯絡我們",
    "联系邮箱": "聯絡信箱",
    "发送邮件至": "來信至",
    # Place names as written in Taiwan.
    "澳大利亚": "澳洲",
    "悉尼": "雪梨",
    "巴塞罗那": "巴塞隆納",
    "海得拉巴": "海德拉巴",
}

# Taiwan typesetting uses corner brackets for quotation marks.
QUOTES = str.maketrans({"“": "「", "”": "」", "‘": "『", "’": "』"})

_cc = None


def to_hant(text):
    global _cc
    if _cc is None:
        for profile in ("s2twp", "s2twp.json"):
            try:
                _cc = OpenCC(profile)
                break
            except Exception:
                continue
        else:
            sys.exit("This OpenCC build has no s2twp profile.")
    # Swap protected phrases for private-use placeholders, convert, swap back.
    held = []

    def hold(match):
        held.append(PHRASES[match.group(0)])
        return f"{len(held) - 1}"

    pattern = "|".join(re.escape(k) for k in sorted(PHRASES, key=len, reverse=True))
    text = re.sub(pattern, hold, text)
    text = _cc.convert(text).translate(QUOTES)
    return re.sub("(\\d+)", lambda m: held[int(m.group(1))], text)


HANS = re.compile(r'<span lang="zh-Hans">(.*?)</span>(<span lang="zh-Hant">.*?</span>)?', re.S)
TITLE = re.compile(r'(data-title-zh-hans="([^"]*)")(\s+data-title-zh-hant="[^"]*")?')


def render(source):
    source = HANS.sub(
        lambda m: f'<span lang="zh-Hans">{m.group(1)}</span><span lang="zh-Hant">{to_hant(m.group(1))}</span>',
        source)
    return TITLE.sub(lambda m: f'{m.group(1)} data-title-zh-hant="{to_hant(m.group(2))}"', source)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="report stale pages instead of rewriting them")
    args = parser.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    stale = []
    for page in sorted(root.glob("*.html")) + sorted(root.glob("dclp/*.html")):
        before = page.read_text(encoding="utf-8")
        after = render(before)
        if after != before:
            stale.append(page.relative_to(root))
            if not args.check:
                page.write_text(after, encoding="utf-8")

    verb = "out of date" if args.check else "updated"
    print(f"{len(stale)} page(s) {verb}" + "".join(f"\n  {p}" for p in stale))
    sys.exit(1 if args.check and stale else 0)


if __name__ == "__main__":
    main()
