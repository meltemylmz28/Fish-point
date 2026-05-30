plugins {
    id("com.android.application")
    id("kotlin-android")
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.example.frontend"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    // 1. SIKINTI ÇÖZÜMÜ: Java 11 uyumluluğu android bloğunun İÇİNDE olmalı
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    // Kotlin DSL (.kts) için derleyici ayarı android bloğunun İÇİNDE olmalı
    kotlin {
        compilerOptions {
            jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_11)
        }
    }

    defaultConfig {
        applicationId = "com.example.frontend"
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
        val mapsApiKey = System.getenv("GOOGLE_MAPS_API_KEY")
            ?: project.findProperty("GOOGLE_MAPS_API_KEY")?.toString()
            ?: ""
        manifestPlaceholders["MAPS_API_KEY"] = mapsApiKey
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("debug")
        }
    }
} // Android bloğu tüm ayarlardan SONRA burada kapanmalı!

flutter {
    source = "../.."
}