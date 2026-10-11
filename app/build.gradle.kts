plugins {
    id("com.android.application")
}

android {
    namespace = "com.megasuite.cleanicon"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.megasuite.cleanicon"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    // 纯资源 App：图标放在 res/drawable-nodpi/，不做密度缩放。
    // PNG 默认不压缩，无需额外配置。
}

// AGP 9 会默认带上 kotlin-stdlib；本项目是纯 Java，去掉以缩小 APK。
configurations.configureEach {
    exclude(group = "org.jetbrains.kotlin", module = "kotlin-stdlib")
}
