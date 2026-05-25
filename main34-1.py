import cv2
from gpiozero import Buzzer
import time

# 라즈베리파이 16번 핀에 부저 연결 설정
buzzerPin = Buzzer(16)

def main():
    # IP 웹캠(핸드폰 주소 등)에서 비디오 스트림 가져오기
    camera = cv2.VideoCapture("http://172.30.1.25:4747/video")
    
    # 영상 해상도 설정 (가로 640, 세로 480)
    camera.set(3, 640)
    camera.set(4, 480)
    
    # OpenCV에서 제공하는 Haar Cascade 검출기 모델 경로 지정 (얼굴, 눈)
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'
    
    # 지정한 xml 파일로 분류기(Classifier) 객체 생성
    face_cascade = cv2.CascadeClassifier(face_xml)
    eye_cascade = cv2.CascadeClassifier(eye_xml)
    
    # 카메라가 정상적으로 열려있는 동안 무한 루프 수행
    while(camera.isOpened()):
        # 카메라로부터 한 프레임씩 이미지 읽어오기
        _, image = camera.read()
        
        # 연산 속도 향상 및 정확도를 위해 흑백(Gray) 이미지로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 흑백 이미지에서 얼굴 찾기 (파라미터 조절로 검출 민감도 세팅)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # 터미널 창에 현재 프레임에서 발견된 얼굴 개수 출력 (디버깅용)
        print("faces detected Number: " + str(len(faces)))

        # 발견된 얼굴이 하나라도 있다면 진입
        if len(faces):
            for (x, y, w, h) in faces:
                # 원본 컬러 영상에 얼굴 영역 사각형 그리기 (파란색, 두께 2)
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # 눈을 더 잘 찾기 위해 얼굴 범위만 잘라냄 (ROI 설정)
                face_gray = gray[y:y+h, x:x+w]
                face_color = image[y:y+h, x:x+w]
                
                # 잘라낸 얼굴(흑백) 영역 안에서만 눈 검출 수행
                eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5)
                
                # 졸음 운전 감지 로직: 감지된 눈이 1개 이하(눈을 감음)이면 부저 울림
                if len(eyes) <= 1:
                    buzzerPin.on()
                else:
                    buzzerPin.off()
                
                # 검출된 눈 영역에 사각형 그리기 (초록색, 두께 2)
                # 얼굴 좌표 기준(face_color)이므로 얼굴 사각형 안에 알맞게 그려짐
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
        # 'result'라는 이름의 윈도우 창에 최종 처리된 이미지 띄우기
        cv2.imshow('result', image)
        
        # 키보드 'q' 키를 누르면 루프 탈출 (프로그램 종료)
        if cv2.waitKey(1) == ord('q'):
            break
    
    # 루프 탈출 후 메모리 해제 및 창 닫기, 부저 끄기 안전장치
    cv2.destroyAllWindows()
    buzzerPin.off()

if __name__ == '__main__':
    main()
