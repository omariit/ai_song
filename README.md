# AI Song Generator - برنامج توليد الأغاني بالذكاء الاصطناعي

برنامج يقوم بإنشاء أغاني بصيغة MP3 من النصوص العربية والاختيار من عدة أنماط موسيقية.

## المميزات

✓ توليد صوت غنائي من النص باستخدام Bark AI  
✓ اختيار من 4 أنماط موسيقية مختلفة (إلكتروني، حماسي، هادئ، درامي)  
✓ إمكانية تحديد السرعة (Tempo) اختيارياً  
✓ نظام logging شامل لتتبع جميع العمليات  
✓ واجهة ويب سهلة الاستخدام  
✓ تحميل ملفات MP3 تلقائياً بعد الإنشاء

## المتطلبات

- Python 3.10+
- FFmpeg (لتحويل الصوت إلى MP3)
- PyTorch 2.1+
- Bark (TTS)

## التثبيت

### 1. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 2. تثبيت FFmpeg

**على Windows:**
```bash
choco install ffmpeg
```

**على macOS:**
```bash
brew install ffmpeg
```

**على Linux:**
```bash
sudo apt-get install ffmpeg
```

## البدء السريع

### شغيل التطبيق
```bash
python app.py
```

افتح المتصفح على `http://localhost:5000`

### واجهة الويب

1. **أدخل نص الأغنية** (Lyrics)
2. **اختر الستايل**: إلكتروني / حماسي / هادئ / درامي
3. **حدد السرعة** (اختياري): 40-240 BPM
4. **اضغط "إنشاء ملف MP3"**
5. **تحميل الملف**

## نظام السجلات (Logging)

جميع العمليات يتم تسجيلها في:
```
logs/ai_song_YYYYMMDD_HHMMSS.log
```

## هيكل المشروع

```
ai song/
├── app.py              # تطبيق Flask
├── generate_song.py    # محرك التوليد
├── requirements.txt    # المكتبات
├── README.md           # هذا الملف
├── templates/
│   └── index.html      # الواجهة
└── logs/               # السجلات
```

## استكشاف الأخطاء

### خطأ: "Weights only load failed"
**الحل**: تم تطبيقه تلقائياً

### خطأ: "FFmpeg not found"
**الحل**: تأكد من تثبيت FFmpeg

## الملاحظات

- **أول مرة**: قد تستغرق 5-10 دقائق (تحميل النموذج)
- **المرات اللاحقة**: أسرع بكثير
- **الموارد**: يفضل GPU للأداء الأفضل

---

**الإصدار**: 2.0

> إذا كنت تستخدم جهاز CPU فقط، ستحتاج أيضاً إلى تثبيت PyTorch للمعالج المركزي:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

3. تأكد من أن FFmpeg مثبت على جهازك لتصدير MP3. يمكنك تثبيته من:

- https://ffmpeg.org/download.html

4. شغّل التطبيق:

```bash
python app.py
```

5. افتح المتصفح وزُر:

```text
http://127.0.0.1:5000
```

6. أدخل نص الأغنية واختر الستايل، ثم اضغط "إنشاء ملف MP3" لتحميل `song.mp3`.

## تعديل اللحن من النص والستايل

- يتم تحويل النص إلى صوت غنائي تلقائياً باستخدام مكتبة Bark المفتوحة.
- الخلفية الموسيقية تُنشأ أيضاً بواسطة Bark بوصفيّات ستايل مختلفة.
- لا تحتاج لإدخال أرقام نغمات أو مدّد يدوياً.

## تشغيل السكربت بدون واجهة

```bash
python generate_song.py
```

## تعديل اللحن

- لتغيير سرعة الإيقاع، عدّل Tempo في واجهة الويب أو في كود `generate_song.py`.
- لتغيير الستايل، اختر بين "إلكتروني" و"حماسي" و"هادئ" و"درامي".
- يمكن تعديل طريقة توليد الصوت في `generate_song.py` إذا أردت تغيير تدرجات النغمات أو الموجات الصوتية.

## أوامر Git للرفع إلى GitHub

```bash
git init
 git add generate_song.py app.py README.md templates/index.html
 git commit -m "Add HTML UI and Flask backend for MIDI song generator"
 git branch -M main
 git remote add origin <YOUR_GITHUB_REPO_URL>
 git push -u origin main
```
