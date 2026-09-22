# CleanIcon — 自用 Android 图标包制作方案

> 一句话：**图标包 = 一个能被启动器查到的 App + 一份 `appfilter` 映射表 + 一堆干净图标。**
> 本项目吸收 [完美图标补全计划](https://github.com/pzcn/Perfect-Icons-Completion-Project) 的 **Adapted Icon（适配 / 分层图标）** 思想：不直接搬用 App 自带的脏图标，而是把「干净背景 + 内容前景」分离出来，去掉图标上的营销牛皮癣，再按安全区缩放、合成。

本方案给出一套**最小可用、可本地构建、装到自己手机上就能用**的图标包实现方式，写法参考 `ref/iOS26.apk`（已确认可在你的手机上生效）。

---

## 一、先看参考包长什么样

`ref/iOS26.apk` 是一个基于 **Blueprint**（`dev.jahir.blueprint`）模板做的商业图标包（包名 `com.panpandada.ios26.pay`），反编译后与图标包功能相关的核心内容其实很少：

```
iOS26.apk
├── AndroidManifest.xml          # 关键：Activity 上挂了一堆启动器识别的 intent-filter
├── assets/
│   ├── appfilter.xml            # 关键：ComponentInfo{包名/Activity} -> drawable名 映射表（约 2000 条）
│   ├── drawable.xml             # 关键：图标清单 + 分类，供“图标选择器”展示
│   ├── themeinfo.xml            # Atom Launcher 等旧启动器用
│   ├── themecfg.xml             # 桌面主题（壁纸等）
│   ├── desk.xml / app_func_theme.xml  # 特定启动器（Atom/GO 等）的桌面主题配置
│   ├── themefont.ttf
│   └── iconsets/Minimal Weather.zip   # Kustom 天气图标集（可忽略）
├── res/
│   ├── drawable-nodpi/*.png     # 关键：真正的图标，817 张，214×214 / 216×216
│   └── ...                      # 大量是 Blueprint 模板自带的 UI 资源
└── classes.dex                  # Blueprint 框架代码（主题预览、申请图标、计费校验等）
```

要点：

- **图标本体**在 `res/drawable-nodpi/`，文件名就是资源名（`aima.png`、`airbnb.png` …），大小统一 **214×214**。
- **appfilter.xml / drawable.xml 有两位**：`assets/` 下的给启动器读，`res/xml/` 下的给模板自己的 UI 读。自用只需管 `assets/` 下的。
- 打包时 `classes.dex` 占了 4.3MB，绝大部分是模板 UI、广告/计费 SDK。**自用完全不需要这些**，只保留图标 + 两个 xml + 一个极简 Activity 即可。
- 参考包对 `res/` 里的模板 UI 资源做了混淆（文件名被改成 `-8.png`、`0A.png` 这类），所以想从里面取图标要用 apktool 解码，不能直接解压。

### appfilter.xml 的实际格式

```xml
<?xml version="1.0" encoding="UTF-8"?>
<resources>
    <!-- 图标遮罩/底图（旧启动器用，现代启动器可忽略） -->
    <iconback img1="iconback" />
    <iconmask img1="iconmask" />
    <iconupon img1="iconupon" />
    <scale factor="1.1" />

    <!-- 通用遗留名：启动器猜不出 Activity 时按类型兜底 -->
    <item component=":PHONE"    drawable="phone" />
    <item component=":SMS"      drawable="sms" />
    <item component=":CALENDAR" drawable="calendar" />

    <!-- 主体：包名/Activity -> drawable 资源名 -->
    <item component="ComponentInfo{com.tencent.mm/com.tencent.mm.ui.LauncherUI}" drawable="wechat" />
    <item component="ComponentInfo{com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity}" drawable="qq" />

    <!-- 可选：日历动态图标，prefix 指向 calendar_d1..d31 一组图 -->
    <calendar component="ComponentInfo{com.android.calendar/com.android.calendar.AllInOneActivity}" prefix="calendar_d" />
</resources>
```

### drawable.xml 的实际格式

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <version>1</version>
    <category title="New" />        <!-- 分类标题，后面跟属于该分类的 item -->
    <item drawable="aima" />
    <item drawable="airbnb" />
    ...
</resources>
```

### 启动器识别的 intent-filter（从参考包提取，可直接照抄）

图标包能被启动器发现，靠的是 Manifest 里这个 Activity 上挂的一堆 `intent-filter`。参考包挂得很全，照抄即可覆盖市面上绝大多数启动器：

```xml
<activity android:name=".MainActivity" android:exported="true">
    <intent-filter>
        <action android:name="com.motorola.launcher.ACTION_ICON_PACK" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
    <intent-filter>
        <action android:name="org.adw.launcher.THEMES" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="org.adw.launcher.icons.ACTION_PICK_ICON" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="com.anddoes.launcher.THEME" />
    </intent-filter>
    <intent-filter>
        <action android:name="com.dlto.atom.launcher.THEME" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <action android:name="com.gau.go.launcherex.theme" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="com.fede.launcher.THEME_ICONPACK" />
    </intent-filter>
    <intent-filter>
        <action android:name="com.gtp.nextlauncher.theme" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="com.gridappsinc.launcher.theme.apk_action" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="com.teslacoilsw.launcher.THEME" /> <!-- Nova -->
    </intent-filter>
    <intent-filter>
        <action android:name="com.novalauncher.THEME" />
        <category android:name="com.novalauncher.category.CUSTOM_ICON_PICKER" />
    </intent-filter>
    <intent-filter>
        <action android:name="ch.deletescape.lawnchair.ICONPACK" />
        <category android:name="ch.deletescape.lawnchair.PICK_ICON" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <action android:name="com.lge.launcher2.THEME" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="net.oneplus.launcher.icons.ACTION_PICK_ICON" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="ginlemon.smartlauncher.THEMES" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="com.sonymobile.home.ICON_PACK" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <action android:name="com.tsf.shell.themes" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
    <intent-filter>
        <action android:name="com.phonemetra.turbo.launcher.THEMES" />
        <category android:name="android.intent.category.DEFAULT" />
    </intent-filter>
</activity>
```

> 挂多不挂少：多加几个 filter 不会有副作用（最多在启动器的图标包列表里多出现一条），少挂了对应启动器就发现不了。

---

## 二、Adapted Icon（适配图标）思想

**问题**：国内 App 喜欢在图标上叠加促销 / 活动内容（俗称「牛皮癣」），例如双十一、周年庆、5G 角标。直接把这类图做成图标包，只是把「脏」原样搬到了桌面上。

**思路（来自[完美图标补全计划](https://github.com/pzcn/Perfect-Icons-Completion-Project)）**：一个图标本质上是「背景 + 内容」两层。MIUI 12 起的「完美图标」、以及 Android 原生的 Adaptive Icon，都要求 App 自己提供分层图标，系统再按蒙版裁剪、合成，并做视差 / 暗色适配。参考项目做的事，就是给**没有适配**或**适配不完美**的 App 补一套分层图标：把内容抠成前景，把背景补干净，丢掉营销信息。CleanIcon 沿用的正是这套做法。

### 2.1 分层图标的三个层次

| 层 | 文件 | 说明 |
| --- | --- | --- |
| 背景 | `0.png` | 纯背景 / 渐变 / 纹理，**不含任何文字、角标、活动信息**；尽量不留透明洞 |
| 前景 | `1.png` | 图标主体内容，其余位置透明 |
| （可选）单色层 | monochrome | Android 13+ 主题图标用，由系统统一上色 |

MIUI / HyperOS 的「完美图标」只用 `0` / `1` 两层；Android 原生 `<adaptive-icon>` 对应 `<background>` / `<foreground>`，13+ 再增加 `<monochrome>`。

### 2.2 需要适配的三种情况

参考项目把适配对象分成三类，CleanIcon 沿用它来判断「哪些图标该重做」：

1. **完全没适配**：App 只提供静态方图 —— 按官方样式重绘为分层图标。
2. **适配不完美**：整个图标都被当成前景，移动 / 缩放时前后景不分（如某些地图、相机图标）。
3. **适配后仍有牛皮癣**：分层了但角标、活动 banner 还在（如带 5G 字样的营业厅）。

### 2.3 安全区与分辨率（关键参数）

系统不会整张显示，只取图片中心一块：

- **HyperOS / MIUI 新遮罩**：可见区 = 图片边长的 **66.6%**；老 MIUI 12–14 为 **62.5%**（demo 已过时，按 66.6% 做）。
- 因此**内容必须落在中心安全区内**，四周留白 / 透明；圆角蒙版还会再切掉一点四角，关键视觉别贴边。
- 普通静态分层图标分辨率 **≤ 432×432**；动态图标的 `quietImage.png` **≤ 365×365**；前景背景**同尺寸、正方形**。
- Android 原生 adaptive icon 的对应关系：108dp 画布，其中 72dp 可见、66dp 安全区（约 61%）—— 和 MIUI 的 66.6% 是同一套「中心安全区」思想。

### 2.4 怎么落到 CleanIcon 上

即使只做一个普通启动器图标包，也建议按 Adapted Icon 的方式产出图标：

- **先清理再缩放**：先把原图里的活动角标 / 文字去掉、把背景补全，而不是整张缩进去。
- **能分层就分层**：保留 `0.png`（背景）和 `1.png`（前景），需要时再合成为一张扁平 PNG 给老启动器用；将来遇到支持分层 / 主题图标的桌面（HyperOS、Lawnchair 主题图标等）可以直接复用。
- **统一安全区**：所有图标都缩放到同一个中心占比（推荐 66.6%），桌面看上去大小、留白才一致。

> 注意：标准启动器图标包（`appfilter.xml`）多数只消费扁平 PNG，分层图标主要面向 MIUI / HyperOS 主题，以及支持主题图标的桌面。CleanIcon 的做法是「**分层存档、按需合成**」，两边都不吃亏。

---

## 三、图标包的工作原理（决定了我们要做什么）

1. 启动器（Nova / ADW / Apex / Lawnchair / 部分厂商桌面）通过 `queryIntentActivities` 查上面那些 action，拿到图标包 App。
2. 启动器用 `createPackageContext(包名, CONTEXT_IGNORE_SECURITY)` 打开图标包 App 的 `assets/appfilter.xml`，解析出 `ComponentInfo{包名/Activity} -> drawable名`。
3. 桌面上的应用图标，启动器把它的 ComponentInfo 拿去查表，命中就用图标包里 `getIdentifier(drawable名, "drawable", 图标包包名)` 取图。
4. `drawable.xml` 用来在图标选择器里列出所有可选图标。
5. `iconback/iconmask/iconupon/scale` 是给旧启动器做统一外形遮罩/底图（现代启动器多数忽略）。

**结论：图标包本质就是「一个能被查到的 App + 一份映射表 + 一堆图片资源」，不需要任何复杂代码。** 参考包之所以大，全是模板 UI 和 SDK 的负担。

---

## 四、推荐方案：极简 Gradle 工程

用 Android Studio 新建空项目后，删掉用不到的东西，最终只要这些文件：

```
MyIcons/
├── settings.gradle
├── build.gradle
├── gradle.properties
├── layers/                        # 分层图标源文件（可选，Adapted Icon，不打包）
│   └── com.tencent.mm/{0,1}.png   # 背景 / 前景，合成后进 drawable-nodpi
└── app/
    ├── build.gradle
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/example/myicons/MainActivity.java   # 极简说明页，让 App 可启动
        ├── assets/
        │   ├── appfilter.xml      # 映射表
        │   └── drawable.xml       # 图标清单
        └── res/
            ├── drawable-nodpi/    # 所有图标 PNG（文件名即 drawable 名）
            │   ├── wechat.png
            │   ├── qq.png
            │   └── ...
            ├── drawable-nodpi/iconback.png   # 可选遮罩三件套
            ├── drawable-nodpi/iconmask.png
            ├── drawable-nodpi/iconupon.png
            ├── mipmap-*/ic_launcher.png      # 自己 App 的图标
            └── values/strings.xml            # 应用名
```

### 4.1 `settings.gradle`

```groovy
pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositories { google(); mavenCentral() }
}
rootProject.name = "MyIcons"
include ':app'
```

### 4.2 根 `build.gradle`

```groovy
plugins {
    id 'com.android.application' version '8.5.2' apply false
}
```

### 4.3 `app/build.gradle`

```groovy
plugins { id 'com.android.application' }

android {
    namespace 'com.example.myicons'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.myicons"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false          // 自用无需混淆
        }
    }

    // 注：PNG 默认就不压缩，无需额外配置；图标放 drawable-nodpi 即不会被密度缩放
}
```

> 全部依赖为空：纯资源 App，不需要 appcompat、不需要 Kotlin。

### 4.4 `app/src/main/AndroidManifest.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Android 11+ 让本 App 能枚举已安装应用（若做“未适配图标”列表才需要） -->
    <queries>
        <intent>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent>
    </queries>

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.DeviceDefault.Light">

        <!-- 把上面「启动器 intent-filter」整段粘进来 -->
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <!-- ... 启动器 intent-filter ... -->
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

### 4.5 `MainActivity.java`（极简说明页，20 行足够）

```java
package com.example.myicons;

import android.app.Activity;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        TextView tv = new TextView(this);
        tv.setPadding(64, 160, 64, 64);
        tv.setGravity(Gravity.CENTER_HORIZONTAL);
        tv.setTextSize(16);
        tv.setText("MyIcons 图标包\n\n"
                + "应用方法：\n"
                + "1. 打开桌面设置\n"
                + "2. 找到「图标样式 / 图标包 / 主题」\n"
                + "3. 选择 MyIcons 并应用\n\n"
                + "若桌面未显示本图标包，\n"
                + "请确认桌面支持第三方图标包。");
        setContentView(tv);
    }
}
```

### 4.6 `res/values/strings.xml`

```xml
<resources>
    <string name="app_name">MyIcons</string>
</resources>
```

---

## 五、图标资源规范

| 项目 | 建议 |
| --- | --- |
| 目录 | `app/src/main/res/drawable-nodpi/`（nodpi = 不做密度缩放，最适合图标包） |
| 尺寸 | 扁平图参考包用 214×214；建议统一 **192×192** 或 **216×216**，PNG 带透明通道（分层图见下） |
| 命名 | 只能用小写字母、数字、下划线，且不能以数字开头。**不能带点**（如 `com.tencent.mm.png` 非法 → 用 `com_tencent_mm.png`） |
| 格式 | PNG（也支持 webp / vector drawable，但 PNG 最省事） |
| 数量 | 自用不必追求全适配，先做自己常用的 30～80 个 |
| 遮罩三件套 | `iconback.png`（底）、`iconmask.png`（形状遮罩）、`iconupon.png`（前景高光），可只放一张全透明的 `iconback` 让旧启动器不炸 |

### 分层图标（Adapted Icon）规范

按第二节的思想，推荐**分层存档、按需合成**：源文件放工程根的 `layers/`（不打进 APK），合成后的扁平 PNG 才进 `res/drawable-nodpi/`。

```
MyIcons/
├── layers/                          # 分层源文件（素材存档，不打包）
│   └── com.tencent.mm/
│       ├── 0.png                    # 背景：无牛皮癣、无透明洞
│       └── 1.png                    # 前景：主体内容，其余透明
└── app/src/main/res/drawable-nodpi/
    └── com_tencent_mm.png           # 合成后的扁平图标（启动器实际读取）
```

制作要点：

- 前景背景**同尺寸正方形**，静态分层 **≤ 432×432**；内容统一缩放到中心 **66.6%**（HyperOS）安全区内。
- 背景要**补齐**被 banner 盖住的部分，单拿出背景也不应有空白；补不上就重绘或改纯色 / 渐变。
- 用 ImageMagick 合成扁平图（`0` 在下、`1` 在上）：

```bash
# A) 已有分层，合成扁平图标
magick layers/com.tencent.mm/0.png layers/com.tencent.mm/1.png \
       -background none -compose over -composite -resize 216x216 \
       app/src/main/res/drawable-nodpi/com_tencent_mm.png

# B) 只有一张干净方图：按比例缩到 66.6% 安全区再居中导出（避免变形）
S=216; VIS=$((S*666/1000))          # 144
magick clean.png -resize ${VIS}x${VIS} \
       -background none -gravity center -extent ${S}x${S} \
       app/src/main/res/drawable-nodpi/clean.png
```

> `-resize` 负责等比缩放、`-extent` 只负责居中补画布，二者配合才不会拉伸。批量处理时用 `mogrify` 或循环即可。

### 图标来源

- 自己画：Figma / Illustrator / Inkscape 导出 PNG。
- 网络图标集：注意授权，自用一般没问题，**分发**要谨慎。
- 高清原图：可在 [icon.yukonga.top](https://icon.yukonga.top/) 找 iOS 高清 App 图标，或从 APK 内提取，再按 Adapted Icon 方式清理分层。
- 参考项目的现成分层图（需遵守其授权）：[Perfect-Icons-Completion-Project](https://github.com/pzcn/Perfect-Icons-Completion-Project) 的 `icons/<包名>/{0,1}.png`，可作为自用素材。
- 想复用参考包的图标（仅自用）：必须用 apktool 解码才能拿到带名字的图——

```bash
java -jar apktool.jar d -f -o ref_dec ref/iOS26.apk
ls ref_dec/res/drawable-nodpi/          # 817 张带名字的图标
```

> 参考包里的图是 iOS 风格、受版权/商标约束，请勿公开分发。

---

## 六、制作流程（从零到装到手机）

### 步骤 1：建工程

用 Android Studio「Empty Views Activity」，或直接按第四节手写文件。**命令行也完全可以**（见步骤 4）。

### 步骤 2：放入图标

把图标 PNG 全部扔进 `app/src/main/res/drawable-nodpi/`，文件名 = 你要用的 drawable 名（如 `wechat.png`、`taobao.png`）。

### 步骤 3：生成 appfilter.xml

这是最费时的一步：需要知道每个应用在手机上的 `包名/Activity`。**不要手抄**，用下一节的脚本从 adb 自动生成。

### 步骤 4：构建

```bash
cd MyIcons
./gradlew assembleDebug          # 首次会自动下载 Gradle / AGP
# 产物：app/build/outputs/apk/debug/app-debug.apk（已用 debug key 签名，可直接安装）
```

没有 Android Studio 时，需要：
- JDK 17+（`apt install openjdk-17-jdk`）
- Android SDK Command-line Tools，配置 `ANDROID_HOME` 和 `local.properties`：

```properties
sdk.dir=/path/to/Android/Sdk
```

安装 SDK：`sdkmanager "platforms;android-34" "build-tools;34.0.0"`

### 步骤 5：安装并应用

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

然后在手机上：桌面设置 → 图标样式 / 图标包 / 主题 → 选择 MyIcons。

常见启动器路径：

- **Nova**：Nova 设置 → 外观 → 图标样式 → 图标主题
- **Lawnchair**：主页设置 → 通用 → 图标样式 → 图标包
- **ADW / Apex**：桌面设置 → 主题设置 → 图标包
- **MIUI / HyperOS**：主题壁纸 → 混搭 → 图标 → 选择本地图标包（部分版本需第三方桌面）
- **一加 / OPPO / realme**：桌面设置 → 图标样式 / 个性化

---

## 七、自动生成 appfilter.xml 的脚本

放在 `tools/gen_appfilter.py`，配合 `adb` 使用。它做三件事：

1. 用 adb 列出手机上所有“可启动”的 `包名/Activity`；
2. 用「图标文件名 ≈ 包名」的约定去匹配 `drawable-nodpi/` 里的图标；
3. 生成 `assets/appfilter.xml` 与 `assets/drawable.xml`。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用法:
    python3 tools/gen_appfilter.py                 # 全部应用
    python3 tools/gen_appfilter.py --third-party   # 只看第三方应用
图标命名约定: 包名里的 '.' 换成 '_'，例如 com.tencent.mm -> com_tencent_mm.png
也可以在 icons 目录里放一个 alias.json 做手工映射: {"com.tencent.mm": "wechat"}
"""
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR  = os.path.join(ROOT, "app/src/main/res/drawable-nodpi")
ASSETS    = os.path.join(ROOT, "app/src/main/assets")
AF        = os.path.join(ASSETS, "appfilter.xml")
DW        = os.path.join(ASSETS, "drawable.xml")
ALIAS     = os.path.join(ROOT, "alias.json")


def adb(*args):
    return subprocess.run(["adb", *args], capture_output=True, text=True).stdout


def list_launchables(third_party=False):
    """返回 [(package, activity), ...]"""
    out = adb("shell", "cmd", "package", "query-activities", "--brief",
              "-a", "android.intent.action.MAIN",
              "-c", "android.intent.category.LAUNCHER")
    pairs, seen = [], set()
    for line in out.splitlines():
        line = line.strip()
        if "/" not in line or line.startswith("No ") or " " in line:
            continue
        pkg, act = line.split("/", 1)
        act = act if act.startswith(".") else act
        key = (pkg, act)
        if key not in seen:
            seen.add(key)
            pairs.append((pkg, act))

    if not pairs:  # 老系统回退：逐包 resolve
        list_args = ["shell", "pm", "list", "packages"]
        if third_party:
            list_args.append("-3")
        pkgs = [l.split(":")[-1].strip()
                for l in adb(*list_args).splitlines() if ":" in l]
        for p in pkgs:
            r = adb("shell", "cmd", "package", "resolve-activity", "--brief",
                    "-c", "android.intent.category.LAUNCHER", p).strip()
            if "/" in r:
                pairs.append(tuple(r.split("/", 1)))

    if third_party:
        sys_pkgs = set(l.split(":")[-1].strip()
                       for l in adb("shell", "pm", "list", "packages", "-s").splitlines()
                       if ":" in l)
        pairs = [p for p in pairs if p[0] not in sys_pkgs]
    return pairs


def norm(name):
    """android 资源名合法化: 小写、非 [a-z0-9_] 变 _、数字开头加前缀"""
    s = re.sub(r"[^a-z0-9_]", "_", name.lower())
    if re.match(r"^\d", s):
        s = "n_" + s
    return s


def main():
    third_party = "--third-party" in sys.argv

    icons = {}
    for f in os.listdir(ICON_DIR):
        if f.lower().endswith((".png", ".webp", ".xml")):
            icons[os.path.splitext(f)[0].lower()] = os.path.splitext(f)[0]

    alias = json.load(open(ALIAS, encoding="utf-8")) if os.path.exists(ALIAS) else {}

    pairs = list_launchables(third_party)
    used, entries, missing = set(), [], []

    for pkg, act in pairs:
        draw = alias.get(pkg)
        if not draw:
            draw = icons.get(norm(pkg)) or icons.get(norm(pkg.split(".")[-1]))
        if draw and draw not in used:
            entries.append((pkg, act, draw))
            used.add(draw)
        elif not draw:
            missing.append(f"{pkg}/{act}")

    os.makedirs(ASSETS, exist_ok=True)

    # ---- appfilter.xml ----
    with open(AF, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<resources>\n')
        fh.write('    <iconback img1="iconback" />\n')
        fh.write('    <iconmask img1="iconmask" />\n')
        fh.write('    <iconupon img1="iconupon" />\n')
        fh.write('    <scale factor="1.1" />\n\n')
        for pkg, act, draw in sorted(entries):
            fh.write(f'    <item component="ComponentInfo{{{pkg}/{act}}}" drawable="{draw}" />\n')
        fh.write('</resources>\n')

    # ---- drawable.xml ----
    with open(DW, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n')
        fh.write('    <version>1</version>\n')
        fh.write('    <category title="All" />\n')
        for name in sorted(icons.values()):
            fh.write(f'    <item drawable="{name}" />\n')
        fh.write('</resources>\n')

    print(f"[OK] 匹配 {len(entries)} 个应用, 写入 {AF} 和 {DW}")
    if missing:
        print(f"[提示] {len(missing)} 个应用暂无图标，已跳过。示例:")
        for m in missing[:15]:
            print("   ", m)


if __name__ == "__main__":
    main()
```

使用：

```bash
# 手机开启 USB 调试并连接
adb devices
python3 tools/gen_appfilter.py --third-party
./gradlew assembleDebug && adb install -r app/build/outputs/apk/debug/app-debug.apk
```

几点说明：

- 脚本只给**能找到图标**的应用生成映射；没图标的会被跳过，启动器会回退成原图标，不会出错。
- 想手工指定对应关系，写 `alias.json`：`{"com.tencent.mm": "wechat"}`，优先级最高。
- 不同 Android 版本 `cmd package query-activities` 的输出略有差异，脚本已带 `resolve-activity` 回退。
- 也可用现成的图形工具生成 appfilter，例如 **Appfilter Generator** 网页版、**Icon Pack Helper** 等，再手工粘回 `assets/appfilter.xml`。

---

## 八、三个方案怎么选

| 方案 | 说明 | 适合 |
| --- | --- | --- |
| **A. 极简工程（本方案）** | 图标 + 两个 xml + 一个说明页，APK 几百 KB | ✅ **自用首选** |
| B. Blueprint / CandyBar 模板 | 带图标选择器、壁纸、申请图标、统计的完整框架；参考包就是 Blueprint | 想做成能给别人用的产品 |
| C. 反编译参考包换图 | `apktool d` → 换 `res/drawable-nodpi` 和 `assets/*.xml` → `apktool b` → 重签名 | 只想改参考包图标、且不怕踩坑 |

方案 C 注意：参考包带计费/盗版校验（`piracychecker`），重新签名后 App 界面可能报错；且资源被混淆，重打包容易失败。**不推荐**，除非你只在意它被启动器读取的 `assets/`（启动器不校验签名，多数情况下仍能用）。

---

## 九、常见问题

**Q: 装上了，但桌面图标包里看不到我的 App？**
- 检查 Manifest 里 `android:exported="true"`（targetSdk 31+ 强制要求）。
- 检查 intent-filter 是否至少包含你所用桌面对应的 action。
- 有些厂商桌面只认自家格式（MIUI 主题包 ≠ 标准图标包），需要用支持标准图标包的第三方桌面（Nova / Lawnchair 等）。

**Q: 图标比原来的大/小、有白边？**
- 扁平图要留安全边距（建议四周各留 ~8% 透明边）。参考包用 `<scale factor="1.1"/>` 微调。
- 分层 / 适配图标则是内容占中心 **66.6%**（见第二节），两者别混用。
- 确认放在 `drawable-nodpi`，别放 `xxhdpi` 等密度目录，否则会被系统缩放。

**Q: appfilter 写了但没生效？**
- `drawable` 名必须和 `res/drawable-nodpi/` 里的文件名完全一致（不含扩展名），且必须是小写。
- ComponentInfo 里的 Activity 必须是完整类名或 `.开头`，且和手机上的真实值一致（Activity 名写错是最常见原因，用脚本自动生成可避免）。
- 应用图标包后，部分桌面需要重启或重新应用一次。

**Q: 资源名带点/大写导致构建失败？**
- Android 资源名只允许 `[a-z0-9_]`，包名要先把 `.` 换成 `_`、大写转小写。

**Q: 图标上的活动角标 / 双十一贴纸（牛皮癣）怎么去掉？**
- 这正是 Adapted Icon 要解决的问题：把主体抠成前景、把背景补干净，再合成。没有现成分层素材时，可用内容填充 / 重绘背景（见第二节、第五节）。

**Q: 分层图标在普通启动器里没生效？**
- 标准 `appfilter.xml` 一般只吃扁平 PNG，分层主要给 MIUI / HyperOS 主题和支持主题图标的桌面用。CleanIcon 的做法是分层存档、合成为扁平图，保证两边都能用。

**Q: 需要给 Android 13+ 做「主题图标（monochrome）」吗？**
- 图标包一般无法替**别的** App 声明 monochrome 主题层，这属于 App 自身；但如果你要的是 MIUI / HyperOS「完美图标」或自家主题图标，则应提供分层（`0.png` / `1.png`，必要时再加单色层），见第二节。

**Q: 自用需要签名吗？**
- Android 要求所有 APK 必须签名。`assembleDebug` 用的 debug key 就够自用；要长期使用/升级，建议 `keytool` 生成一个自己的 keystore 并配置 release 签名。

---

## 十、进阶（按需）

- **日历动态图标**：在 `appfilter.xml` 加 `<calendar component="..." prefix="calendar_d"/>`，并准备 `calendar_d1.png` … `calendar_d31.png`，启动器会按当天日期取图。
- **内置图标分类**：在 `drawable.xml` 里多次用 `<category title="常用"/>` 分段，方便在图标选择器里查找。
- **自动打包脚本**：写个 `Makefile` 串起 `gen_appfilter.py` → `gradlew assembleRelease` → `apksigner` → `adb install`，改完图标一条命令上线。
- **图标制作流水线**：用 ImageMagick 批量统一尺寸：`mogrify -resize 216x216 -background none -gravity center -extent 216x216 *.png`。
- **Adapted Icon 流水线**：把「抠图 / 补背景 → 缩到 66.6% 安全区 → 合成扁平图」写成脚本，批量处理 `layers/<包名>/{0,1}.png`。
- **导出 MIUI / HyperOS 主题（mtz）**：把 `layers/<包名>/{0,1}.png` 按主题结构打包，即可在 HyperOS 上获得完美图标效果（可参考参考项目的 `addition/module` 与 `transform_config.xml`）。
- **做成模板工程**：把 `appfilter.xml` / `drawable.xml` 生成逻辑抽成参数，方便以后做多套配色（如深色/浅色图标集）。

---

## 附：一键跑通的最短路径

```bash
# 0. 准备: JDK17 + Android SDK + adb, 手机开 USB 调试
# 1. 建工程 (按第四节)
# 2. 放图标到 app/src/main/res/drawable-nodpi/
# 3. 生成映射表
python3 tools/gen_appfilter.py --third-party
# 4. 构建安装
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
# 5. 手机桌面设置里选 MyIcons
```
