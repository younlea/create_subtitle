import argparse
import subprocess
import os
import whisper
from deep_translator import GoogleTranslator

def extract_audio(video_path, audio_output_path):
    command = [
        'ffmpeg',
        '-i',
        video_path,
        '-vn',
        '-acodec',
        'libmp3lame',
        '-q:a',
        '2',
        audio_output_path
    ]
    subprocess.run(command, check=True)
    print(f"오디오 추출 완료: {audio_output_path}")

def transcribe_audio(audio_path):
    model = whisper.load_model("small", device="cuda") # 작은 모델 사용, 필요시 "base", "medium", "large" 등으로 변경 가능. GPU(CUDA) 사용 명시.
    print("음성 인식 모델 로드 완료.")
    result = model.transcribe(audio_path, language="ja", word_timestamps=True)
    print("음성 인식 완료.")
    return result

def translate_text(text, source_lang='ja', target_lang='ko'):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    translated_text = translator.translate(text)
    return translated_text

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def create_srt_file(transcription_result, output_srt_path):
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(transcription_result['segments']):
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            original_text = segment['text'].strip()
            translated_text = translate_text(original_text)

            f.write(f"{i + 1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{translated_text}\n\n")
    print(f"SRT 자막 파일 생성 완료: {output_srt_path}")

def main():
    parser = argparse.ArgumentParser(description="일본어 동영상에서 한국어 자막을 생성합니다.")
    parser.add_argument("video_path", help="입력 동영상 파일 경로 (AVI 또는 MP4)")
    args = parser.parse_args()

    video_path = args.video_path
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_output_path = f"temp_audio_{base_name}.mp3"
    output_srt_path = f"{base_name}_ko.srt"

    try:
        # 1. 오디오 추출
        extract_audio(video_path, audio_output_path)

        # 2. 음성 인식
        transcription_result = transcribe_audio(audio_output_path)

        # 3. 자막 파일 생성 (번역 포함)
        create_srt_file(transcription_result, output_srt_path)

        print("모든 작업이 성공적으로 완료되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        # 임시 오디오 파일 삭제
        if os.path.exists(audio_output_path):
            os.remove(audio_output_path)
            print(f"임시 오디오 파일 삭제: {audio_output_path}")

if __name__ == "__main__":
    main()
