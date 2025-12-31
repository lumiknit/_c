import sys
import os
from PIL import Image

def split_chess_pieces_image(input_image_path):
    """
    가로로 6개의 정사각형 이미지가 나열된 이미지 파일을 읽어 분할합니다.
    입력 파일명에서 접미사를 추출하여 결과 파일명에 반영합니다.
    예: piece_black.png -> k_black.png, q_black.png ...
    """
    piece_names = ['k', 'q', 'r', 'b', 'n', 'p']
    expected_count = len(piece_names)

    try:
        # 1. 파일 경로 및 이름 분석 (접미사 추출 로직)
        # 디렉토리 경로
        output_dir = os.path.dirname(input_image_path)
        if not output_dir:
            output_dir = '.'

        # 확장자가 포함된 파일명 (예: piece_black.png)
        filename_with_ext = os.path.basename(input_image_path)
        # 확장자 분리 (예: filename_body="piece_black", ext=".png")
        filename_body, ext = os.path.splitext(filename_with_ext)
        ext = ext.lower() # 확장자 소문자 통일

        # 접미사 결정 로직: 마지막 언더스코어(_)를 찾습니다.
        last_underscore_index = filename_body.rfind('_')

        if last_underscore_index != -1:
            # 언더스코어가 있으면, 그 부분부터 끝까지가 접미사 (예: "_black")
            suffix = filename_body[last_underscore_index:]
        else:
            # 언더스코어가 없으면 접미사 없음 (예: "pieces.png" -> k.png)
            suffix = ""

        print(f"입력 파일: {filename_with_ext}")
        print(f"감지된 접미사: '{suffix}' (확장자: {ext})")


        # 2. 이미지 로드 및 유효성 검사
        img = Image.open(input_image_path)
        img_width, img_height = img.size
        square_size = img_height # 정사각형 한 변의 길이는 높이 기준

        print(f"이미지 크기: {img_width}x{img_height}, 개별 크기: {square_size}x{square_size}")

        if img_width != square_size * expected_count:
            print(f"\n[오류] 이미지 비율이 맞지 않습니다.")
            print(f"예상 너비: {square_size * expected_count}px (높이 {square_size}px * 6개)")
            print(f"실제 너비: {img_width}px")
            return

        print("\n이미지 분할 및 저장을 시작합니다...")

        # 3. 자르기 및 저장 반복
        for i in range(expected_count):
            # 영역 계산
            left = i * square_size
            upper = 0
            right = (i + 1) * square_size
            lower = square_size
            box = (left, upper, right, lower)

            # 이미지 자르기
            cropped_img = img.crop(box)

            # 접미사를 포함한 출력 파일명 생성
            # 예: "k" + "_black" + ".png" -> "k_black.png"
            output_filename = f"{piece_names[i]}{suffix}{ext}"
            output_path = os.path.join(output_dir, output_filename)

            # 저장
            cropped_img.save(output_path)
            print(f" -> 저장 완료: {output_filename}")

        print("\n모든 작업이 완료되었습니다.")

    except FileNotFoundError:
        print(f"[오류] 파일을 찾을 수 없습니다: {input_image_path}")
    except Exception as e:
        print(f"[오류] 문제가 발생했습니다: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python split_chess_suffix.py <이미지파일_접미사.png>")
        print("예시 1: python split_chess_suffix.py assets/pieces_black.png")
        print("   -> 결과: assets/k_black.png, assets/q_black.png ... 생성")
        print("예시 2: python split_chess_suffix.py pieces.png")
        print("   -> 결과: k.png, q.png ... 생성 (접미사 없음)")
    else:
        input_path = sys.argv[1]
        split_chess_pieces_image(input_path)
