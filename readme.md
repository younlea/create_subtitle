# 일본어 동영상 한국어 자막 자동 생성기

## 1. 소개

이 프로그램은 우분투 환경에서 일본어 음성이 포함된 동영상 파일(AVI, MP4)을 입력받아, 음성을 인식하고 한국어로 번역하여 최종적으로 한국어 자막 파일(.srt)을 자동 생성하는 파이썬 스크립트입니다. 모든 기능은 무료 오픈소스 도구들을 활용하여 구현되었습니다.

## 2. 주요 기능

*   **오디오 추출**: 동영상 파일에서 오디오 트랙을 추출하여 임시 MP3 파일로 저장합니다.
*   **음성 인식 (Speech-to-Text, STT)**: 추출된 일본어 오디오에서 음성을 텍스트로 변환하고, 각 대화의 시작 및 종료 시간을 포함한 타임스탬프 정보를 추출합니다. 이를 위해 OpenAI의 `Whisper` 모델을 사용합니다.
*   **텍스트 번역**: 음성 인식으로 변환된 일본어 텍스트를 한국어로 번역합니다. `deep-translator==1.9.0` 라이브러리를 활용하여 Google Translate API를 사용합니다.
*   **SRT 자막 파일 생성**: 번역된 한국어 텍스트와 `Whisper`에서 추출한 타임스탬프 정보를 결합하여 표준 SRT 형식의 자막 파일을 생성합니다.

## 3. 설치 방법

### 3.1. 시스템 의존성 설치 (FFmpeg)

동영상에서 오디오를 추출하기 위해 `ffmpeg`가 필요합니다. 우분투 터미널에서 다음 명령어를 실행하여 설치합니다.

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### 3.2. Python 의존성 설치 및 GPU 가속 설정

프로그램 실행에 필요한 파이썬 라이브러리들을 설치합니다. 특히 `Whisper` 모델의 음성 인식 속도를 향상시키기 위해 GPU(CUDA) 가속을 활용할 수 있습니다. 이를 위해 PyTorch를 CUDA 지원 버전으로 설치해야 합니다.

먼저 `requirements.txt` 파일을 생성하고 다음 내용을 추가합니다.

```
openai-whisper
deep-translator==1.9.0
```

그 다음, 터미널에서 다음 명령어를 실행하여 라이브러리들을 설치합니다. **사용자의 CUDA 버전에 맞는 PyTorch 버전을 설치해야 합니다.** 예를 들어, CUDA 12.1을 사용하는 경우:

```bash
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**참고:** `torch` 설치 시 `--index-url` 뒤의 URL은 사용자의 CUDA 버전에 따라 변경될 수 있습니다. [PyTorch 공식 웹사이트](https://pytorch.org/get-started/locally/)에서 본인의 환경에 맞는 설치 명령어를 확인하십시오.


## 4. 사용 방법

`create_subtitle.py` 스크립트를 실행하고, 자막을 생성할 동영상 파일의 경로를 인자로 전달합니다.

```bash
python create_subtitle.py [동영상_파일_경로]
```

**예시:**

```bash
python create_subtitle.py my_japanese_video.mp4
```

스크립트가 성공적으로 실행되면, 입력 동영상 파일과 동일한 디렉토리에 `[동영상_파일_이름]_ko.srt` 형식의 한국어 자막 파일이 생성됩니다. 예를 들어, `my_japanese_video.mp4`를 입력하면 `my_japanese_video_ko.srt` 파일이 생성됩니다.

## 5. 참고 사항

*   `Whisper` 모델은 기본적으로 `small` 모델을 사용합니다. 더 높은 정확도를 원하시면 `create_subtitle.py` 파일 내 `whisper.load_model("small")` 부분을 `"base"`, `"medium"`, `"large"` 등으로 변경할 수 있습니다. 단, 모델 크기가 커질수록 음성 인식 시간이 길어지고 더 많은 시스템 리소스가 필요합니다.
*   번역은 `deep-translator==1.9.0` 라이브러리를 통해 Google Translate API를 사용합니다. 대량의 번역 요청 시 일시적인 제한이 발생할 수 있습니다.
*   임시 오디오 파일(`temp_audio_[동영상_파일_이름].mp3`)은 작업 완료 후 자동으로 삭제됩니다.
