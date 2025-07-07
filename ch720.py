import os
from moviepy import VideoFileClip
from moviepy.video.fx.MultiplySpeed import MultiplySpeed


def process_video_to_vertical_720p(input_path, output_path):
    """
    16:9 영상을 9:16 세로 영상으로 변환하고 720p로 업스케일링합니다.
    """
    try:
        # with 구문을 사용해 파일을 안전하게 열고 자동으로 닫습니다.
        with VideoFileClip(input_path) as clip:
            print(f"▶️ 처리 시작: '{input_path}' (해상도: {clip.w}x{clip.h})")

            # 1단계: 영상 자르기
            (w, h) = clip.size
            new_w = h * 9 / 16

            if new_w % 2 != 0:
                new_w = int(new_w) + 1
            
            cropped_clip = clip.cropped(width=new_w, height=h, x_center=w/2, y_center=h/2)

            # 2단계: 크기 조정 (업스케일링)
            if cropped_clip.h < 1920:
                final_clip = cropped_clip.resized(height=1920)
            else:
                final_clip = cropped_clip
            
            finall_clip = final_clip.with_effects([ MultiplySpeed(factor=0.8)])

            # 3단계: 최종 영상 파일로 저장
            finall_clip.write_videofile(output_path, 
                                      codec="libx264", 
                                      threads=4, 
                                      ffmpeg_params=['-pix_fmt', 'yuv420p', '-aspect', '9:16'])
            
            print(f"✅ 처리 완료: '{output_path}'\n")

    except Exception as e:
        print(f"❌ '{input_path}' 처리 중 오류 발생: {e}\n")

if __name__ == "__main__":
    # --- 설정: 입력 폴더와 출력 폴더 경로를 지정하세요 ---
    input_folder = "input"   # 원본 동영상이 있는 폴더
    output_folder = "output" # 변환된 동영상을 저장할 폴더

    # 출력 폴더가 없으면 자동으로 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"'{output_folder}' 폴더를 생성했습니다.")

    # 입력 폴더의 모든 파일을 하나씩 처리
    for filename in os.listdir(input_folder):
        # .mp4 파일만 골라서 처리 (다른 확장자도 추가 가능)
        if filename.lower().endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            process_video_to_vertical_720p(input_path, output_path)

    print("모든 작업이 완료되었습니다.")