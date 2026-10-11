# CleanIcon

> 从 [完美图标补全计划](https://github.com/pzcn/Perfect-Icons-Completion-Project) 取分层图标（背景 `0.png` + 前景 `1.png`），合成干净整图，打包成适用于 **OPPO ColorOS** 的**自适应图标包（adaptive icon pack）**。

国内 App 常在图标上叠促销 / 活动角标（「牛皮癣」）。完美图标计划已经把图标拆成分层并去掉这些内容；本项目只覆盖 `ref/applist.csv` 里列出的应用，合成后交给 ColorOS 用系统自适应图标遮罩统一显示。

> 覆盖情况：`applist.csv` 共 160 个应用，已覆盖 **103** 个；其余 57 个完美图标计划里确实没有，见 `ref/missing.csv`。
>
> 图标以**手动**方式添加 / 修改，不使用自动化脚本。

## 快速开始

```bash
# 构建（图标已随仓库提供）
./gradlew assembleDebug
# 产物：app/build/outputs/apk/debug/app-debug.apk

# 安装
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

ColorOS 上应用：

1. **全局**：设置 → 个性化定制 / 主题商店 → 图标，选择 CleanIcon；
2. **单个**：长按桌面图标 → 编辑 → 点图标 → 在图标来源里切到 CleanIcon。

更换后桌面未刷新，重启一次手机即可（无需清除桌面数据）。

## 手动添加 / 修改图标

### 1. 取图层并合成

从完美图标计划取该应用的 `0.png`（背景）/ `1.png`（前景）。图标在仓库里有多个存放路径，常见位置：

```
icons/<包名>/                      主图标库
themes/{perfectcurve,luck7,lrone}/icons/<包名>/
themes/{explore,default,coloros*}/icons/<包名>/
addition/Icons_Archiving/*/<包名>/  历史 / 动态图标
themes/*/icons/<包名>/             其余主题
```

合成整图（前景缩放到与背景同尺寸后叠加）：

```bash
S=432
magick 0.png -resize ${S}x${S} -gravity center -background none -extent ${S}x${S} /tmp/bg.png
magick 1.png -resize ${S}x${S} -gravity center -background none -extent ${S}x${S} /tmp/fg.png
magick /tmp/bg.png /tmp/fg.png -background none -compose over -composite \
  app/src/main/res/drawable-nodpi/<资源名>.png
```

**资源名规则**：包名 `.` → `_`、大写转小写、数字开头加前缀（如 `com.tencent.mm` → `com_tencent_mm`）。

### 2. 加映射（`appfilter.xml`）

在 `app/src/main/assets/appfilter.xml` **和** `app/src/main/res/xml/appfilter.xml`（两份保持一致）各加一条：

```xml
<item component="ComponentInfo{包名/Activity}" drawable="<资源名>"/>
```

`Activity` 可查 `tools/components.json`（包名 → 启动 Activity 对照），或连手机用 `tools/gen_appfilter.py` 列出来。

### 3. 登记图标（`drawable.xml`）

同样两份 `drawable.xml` 各加一条：

```xml
<item drawable="<资源名>"/>
```

然后重新 `./gradlew assembleDebug`。

## 图层规格

完美图标图层与自适应图标共用「中心安全区」：

| 项 | 值 |
| --- | --- |
| 画布 | 正方形 PNG，**≤ 432×432**（推荐 432） |
| `0.png` | 背景，铺满整张画布 |
| `1.png` | 前景，主体居中，其余透明 |
| 可见区 | 中心 **66.6%**，四周会被裁掉 |

背景四角透明时，建议先用主色补满画布，避免非圆形遮罩露底。

> 真分层 `<adaptive-icon>` 也可行，但 Android 会把每层放大 1.5× 再遮罩、实际只显示图层中心 **44.4%**，需先把图层缩到 **2/3**。兼容性优先就用上面的合成整图方案。

## 映射表（精确生成）

`fetch` 用的对照表是离线整理的，未必与设备一致。连上手机后可列出真实 `包名/Activity`，按「资源名 ≈ 包名」重写两份 `appfilter.xml` / `drawable.xml`：

```bash
python3 tools/gen_appfilter.py --third-party
```

## 工程结构

```
CleanIcon/
├── app/src/main/
│   ├── AndroidManifest.xml                # 启动器 intent-filter（被发现的关键）
│   ├── java/com/megasuite/cleanicon/MainActivity.java   # 极简说明页
│   ├── assets/{appfilter,drawable}.xml
│   ├── res/xml/{appfilter,drawable}.xml   # 双份，兼容只读 res 的桌面
│   └── res/drawable-nodpi/*.png           # 合成后的图标
├── tools/
│   ├── gen_appfilter.py                   # 用 adb 精确生成映射
│   └── components.json                    # 包名 → 启动 Activity 对照
└── ref/                                   # 本地素材（已 gitignore）
    ├── applist.csv                        # 要覆盖的应用
    └── missing.csv                        # 完美图标计划里缺失的应用
```

## 原理

图标包 = 一个能被桌面发现的 App + 映射表 + 一堆图片：

1. 桌面通过 Manifest 里的 `intent-filter` 发现图标包；
2. 读 `appfilter.xml`：`ComponentInfo{包名/Activity} → drawable 资源名`；
3. `getIdentifier(资源名, "drawable", 本包包名)` 取图，再套系统遮罩。

不需要任何业务代码。完整 intent-filter 清单可照抄现成图标包（Blueprint / CandyBar 模板）的 Manifest，**挂多不挂少**。

## 注意

- **素材版权**：图层版权 / 商标归各权利人；自用可以，公开分发前请确认授权。
- 桌面看不到图标包：确认 `android:exported="true"`，且 intent-filter 含对应启动器的 action。

## 致谢

- [完美图标补全计划](https://github.com/pzcn/Perfect-Icons-Completion-Project) —— 干净的分层图标素材。
- 启动 Activity 对照整理自公开图标包 [Arcticons](https://github.com/Donnnno/Arcticons)（GPL-3.0）。
