# 일본어 동영상 한국어 자막 자동 생성기

## 1. 소개

이 프로그램은 우분투 환경에서 일본어 음성이 포함된 동영상 파일(AVI, MP4)을 입력받아, 음성을 인식하고 한국어로 번역하여 최종적으로 한국어 자막 파일(.srt)을 자동 생성하는 파이썬 스크립트입니다. 모든 기능은 무료 오픈소스 도구들을 활용하여 구현되었습니다.

## 2. 주요 기능

*   **오디오 추출**: 동영상 파일에서 오디오 트랙을 추출하여 임시 MP3 파일로 저장합니다.
*   **음성 인식 (Speech-to-Text, STT)**: 추출된 일본어 오디오에서 음성을 텍스트로 변환하고, 각 대화의 시작 및 종료 시간을 포함한 타임스탬프 정보를 추출합니다. 이를 위해 OpenAI의 `Whisper` 모델을 사용합니다.
    *   **텍스트 번역**: 현재 번역 기능은 제거되었습니다. 음성 인식으로 변환된 일본어 텍스트를 그대로 자막으로 사용합니다.

*   **SRT 자막 파일 생성**: 번역된 한국어 텍스트와 `Whisper`에서 추출한 타임스탬프 정보를 결합하여 표준 SRT 형식의 자막 파일을 생성합니다.

## 3. 설치 방법

### 3.1. 시스템 의존성 설치 (FFmpeg)

동영상에서 오디오를 추출하기 위해 `ffmpeg`가 필요합니다. 우분투 터미널에서 다음 명령어를 실행하여 설치합니다.

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### 3.2. Conda 환경 설정 및 Python 의존성 설치

안정적인 실행 환경을 위해 Conda 가상 환경을 사용하는 것을 권장합니다. 다음 단계를 따라 환경을 설정하고 필요한 라이브러리를 설치합니다.

1.  **Miniconda 설치 (설치되어 있지 않은 경우):**
    ```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda3
rm miniconda.sh
$HOME/miniconda3/bin/conda init bash
source ~/.bashrc
    ```

2.  **Conda 환경 생성 및 활성화:**
    ```bash
conda create -n subtitle_env python=3.10 -y
conda activate subtitle_env
    ```

3.  **`requirements.txt` 파일 생성:**
    다음 내용을 포함하는 `requirements.txt` 파일을 생성합니다.
    ```
torch==2.1.0
torchaudio==2.1.0
numpy==1.24.4
googletrans
    ```

4.  **기본 의존성 설치:**
    ```bash
pip install -r requirements.txt --index-url https://download.pytorch.org/whl/cpu
    ```
    **참고:** `torch`와 `torchaudio`는 CPU 버전으로 설치됩니다. GPU 가속을 사용하려면 `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`와 같이 사용자의 CUDA 버전에 맞는 명령어를 사용해야 합니다. `create_subtitle.py` 스크립트에서는 `device="cpu"`로 명시되어 있습니다.

5.  **`openai-whisper` 직접 설치:**
    `openai-whisper`는 GitHub 저장소에서 직접 클론하여 개발 모드로 설치합니다. 이는 버전 호환성 문제를 해결하는 데 도움이 됩니다.
    ```bash
pip uninstall -y openai-whisper # 기존 설치된 whisper 제거
git clone https://github.com/openai/whisper.git
cd whisper
pip install -e .
cd .. # 프로젝트 루트 디렉토리로 돌아오기
    ```

**번역 라이브러리 (`googletrans`) 참고 사항:**

`googletrans` 라이브러리는 Google Translate의 비공식 API를 사용하므로, 예기치 않은 오류나 서비스 중단이 발생할 수 있습니다. 만약 번역 단계에서 문제가 발생하면, 다른 번역 솔루션을 고려해야 합니다.


## 4. 사용 방법

`create_subtitle.py` 스크립트를 실행하고, 자막을 생성할 동영상 파일의 경로를 인자로 전달합니다.

```bash
python create_subtitle.py [동영상_파일_경로]
```

**예시:**

```bash
python create_subtitle.py [동영상_파일_경로]
```

**예시:**

```bash
python create_subtitle.py my_japanese_video.mp4
```

**음원 파일 유지 및 재활용:**

개발 및 디버깅 편의를 위해 `--keep-audio` 옵션을 사용하여 동영상에서 추출된 임시 오디오 파일(`temp_audio_[동영상_파일_이름].mp3`)을 삭제하지 않고 유지할 수 있습니다. 이 옵션을 사용하면 스크립트 재실행 시 이미 존재하는 오디오 파일을 재활용하여 오디오 추출 단계를 건너뛰고 음성 인식부터 다시 시작할 수 있습니다.

```bash
python create_subtitle.py my_japanese_video.mp4 --keep-audio
```

스크립트가 성공적으로 실행되면, 입력 동영상 파일과 동일한 디렉토리에 `[동영상_파일_이름]_ko.srt` 형식의 한국어 자막 파일이 생성됩니다. 예를 들어, `my_japanese_video.mp4`를 입력하면 `my_japanese_video_ko.srt` 파일이 생성됩니다.

## 5. 참고 사항

*   `Whisper` 모델은 기본적으로 `small` 모델을 사용합니다. 더 높은 정확도를 원하시면 `create_subtitle.py` 파일 내 `whisper.load_model("small")` 부분을 `"base"`, `"medium"`, `"large"` 등으로 변경할 수 있습니다. 단, 모델 크기가 커질수록 음성 인식 시간이 길어지고 더 많은 시스템 리소스가 필요합니다.
*   번역은 `deep-translator==1.9.0` 라이브러리를 통해 Google Translate API를 사용합니다. 대량의 번역 요청 시 일시적인 제한이 발생할 수 있습니다.
*   임시 오디오 파일(`temp_audio_[동영상_파일_이름].mp3`)은 작업 완료 후 자동으로 삭제됩니다.
