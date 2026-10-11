#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 adb 扫描手机上可启动的 包名/Activity，按「资源名 ≈ 包名」匹配
app/src/main/res/drawable-nodpi/ 里的图标，生成 appfilter.xml 与 drawable.xml，
同时写入 assets/ 和 res/xml/。

用法:
    python3 tools/gen_appfilter.py                 # 全部应用
    python3 tools/gen_appfilter.py --third-party   # 只看第三方应用

命名约定: 包名里的 '.' 换成 '_'，例如 com.tencent.mm -> com_tencent_mm.png
也可在项目根放 alias.json 手工指定: {"com.tencent.mm": "com_tencent_mm"}

注意: 只有当设备上至少匹配到一个应用时才会写文件；否则原样保留当前 xml。
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(ROOT, "app/src/main/res/drawable-nodpi")
ASSETS = os.path.join(ROOT, "app/src/main/assets")
RES_XML = os.path.join(ROOT, "app/src/main/res/xml")
ALIAS = os.path.join(ROOT, "alias.json")


def adb(*args):
    try:
        return subprocess.run(["adb", *args], capture_output=True, text=True).stdout
    except OSError:
        return ""


def launchables(third_party):
    """返回 [(package, activity), ...]"""
    out = adb("shell", "cmd", "package", "query-activities", "--brief",
              "-a", "android.intent.action.MAIN",
              "-c", "android.intent.category.LAUNCHER")
    pairs, seen = [], set()
    for line in out.splitlines():
        line = line.strip()
        if "/" not in line or " " in line:
            continue
        pkg, act = line.split("/", 1)
        if (pkg, act) not in seen:
            seen.add((pkg, act))
            pairs.append((pkg, act))
    if third_party:
        sys_pkgs = {l.split(":")[-1].strip()
                    for l in adb("shell", "pm", "list", "packages", "-s").splitlines()
                    if ":" in l}
        pairs = [p for p in pairs if p[0] not in sys_pkgs]
    return pairs


def res_name(s):
    """Android 资源名合法化: 小写、非 [a-z0-9_] 变 _、数字开头加前缀"""
    s = re.sub(r"[^a-z0-9_]", "_", s.lower())
    return "n_" + s if s[:1].isdigit() else s


def main():
    if not os.path.isdir(ICON_DIR):
        print(f"[错误] 找不到图标目录: {ICON_DIR}")
        return 1

    third_party = "--third-party" in sys.argv
    alias = json.load(open(ALIAS, encoding="utf-8")) if os.path.exists(ALIAS) else {}

    icons = {os.path.splitext(f)[0].lower()
             for f in os.listdir(ICON_DIR)
             if f.lower().endswith((".png", ".webp"))}

    pairs = launchables(third_party)
    if not pairs:
        print("[错误] 没有从设备获取到应用，请确认 adb 已连接（adb devices）。未修改任何文件。")
        return 1

    entries, used = [], set()
    for pkg, act in pairs:
        name = alias.get(pkg) or res_name(pkg)
        if name in icons and name not in used:
            used.add(name)
            entries.append((pkg, act, name))

    if not entries:
        print("[错误] 设备上的应用与本项目图标没有匹配（检查资源名 / 用 alias.json）。未修改任何文件。")
        return 1

    appfilter = ['<?xml version="1.0" encoding="UTF-8"?>', "<resources>"]
    for pkg, act, name in sorted(entries):
        appfilter.append(f'    <item component="ComponentInfo{{{pkg}/{act}}}" drawable="{name}"/>')
    appfilter.append("</resources>")

    drawable = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>",
                "    <version>1</version>"]
    for name in sorted(used):
        drawable.append(f'    <item drawable="{name}"/>')
    drawable.append("</resources>")

    for d in (ASSETS, RES_XML):
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "appfilter.xml"), "w", encoding="utf-8").write(
            "\n".join(appfilter) + "\n")
        open(os.path.join(d, "drawable.xml"), "w", encoding="utf-8").write(
            "\n".join(drawable) + "\n")

    print(f"[OK] 匹配 {len(entries)} 个应用，写入 assets/ 与 res/xml/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
