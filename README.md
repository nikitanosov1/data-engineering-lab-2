# Заметки по ЛР2

## Пример работы TG бота

<img width="800" height="898" alt="image" src="https://github.com/user-attachments/assets/829abbd3-2a4c-4dae-9bf4-b85061a339e9" />


## Как запустить проект?

```
cd n8n
docker compose up -d
cd ..
cd auto-subtitle-service
docker compose up -d
```

## О проекте

```mermaid
flowchart TD
  T[Telegram Trigger] --> IF{URL или файл?}
  IF -- URL --> D[HTTP Request: скачать]
  IF -- Файл --> MBD[Move Binary Data]
  D --> WBF[Write Binary File input.mp4]
  MBD --> WBF
  WBF --> FFM[Execute: ffmpeg → audio.wav]
  FFM --> STT[STT: auto_subtitle]
  STT --> LLM[HTTP Request: LLM EN→RU]
  LLM --> SRT[Write Binary File out_ru.srt]
  SRT --> BURN[Execute: ffmpeg инкрустация]
  BURN --> RBF[Read Binary File output_ru.mp4]
  RBF --> SEND[Telegram: отправить видео]
```

В качестве STT (Sound To Text) была использована [вот эта утилита](https://github.com/m1guelpf/auto-subtitle).
Она завернута в докер контейнер с реализованным API
