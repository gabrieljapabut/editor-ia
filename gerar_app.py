# Gera o projeto Android completo. Rodado automaticamente pelo GitHub Actions.
import os

ARQUIVOS = {}

ARQUIVOS["settings.gradle.kts"] = r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "EditorIA"
include(":app")
'''

ARQUIVOS["build.gradle.kts"] = r'''plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
'''

ARQUIVOS["gradle.properties"] = r'''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
'''

ARQUIVOS["app/build.gradle.kts"] = r'''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.editorvideoia"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.editorvideoia"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "0.1"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}
'''

ARQUIVOS["app/src/main/AndroidManifest.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:label="Editor IA"
        android:theme="@android:style/Theme.Material.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
'''

ARQUIVOS["app/src/main/java/com/editorvideoia/MainActivity.kt"] = r'''package com.editorvideoia

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.MediaController
import android.widget.TextView
import android.widget.VideoView

class MainActivity : Activity() {

    private lateinit var video: VideoView
    private lateinit var status: TextView
    private val codigoEscolherVideo = 1001

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val margem = (16 * resources.displayMetrics.density).toInt()
        val raiz = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(margem, margem * 2, margem, margem)
        }

        val titulo = TextView(this).apply {
            text = "Editor IA para YouTube"
            textSize = 22f
        }

        val botao = Button(this).apply {
            text = "Escolher vídeo"
            setOnClickListener { escolherVideo() }
        }

        video = VideoView(this)
        val alturaVideo = (320 * resources.displayMetrics.density).toInt()
        video.layoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT, alturaVideo
        )

        status = TextView(this).apply {
            text = "Versão 0.1: app base funcionando. Próximas ferramentas: desfoque de rostos, narração, efeitos."
            textSize = 14f
        }

        raiz.addView(titulo)
        raiz.addView(botao)
        raiz.addView(video)
        raiz.addView(status)
        setContentView(raiz)
    }

    private fun escolherVideo() {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "video/*"
        }
        startActivityForResult(intent, codigoEscolherVideo)
    }

    @Deprecated("Usado por ser simples e sem dependências")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == codigoEscolherVideo && resultCode == RESULT_OK) {
            val uri: Uri? = data?.data
            if (uri != null) {
                val controles = MediaController(this)
                controles.setAnchorView(video)
                video.setMediaController(controles)
                video.setVideoURI(uri)
                video.start()
                status.text = "Vídeo carregado."
            }
        }
    }
}
'''

for caminho, conteudo in ARQUIVOS.items():
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("criado:", caminho)
