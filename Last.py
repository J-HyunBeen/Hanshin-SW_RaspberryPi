import cv2
import time
import requests  # 수업 시간에 사용한 간단한 telegram 전송 방식을 위해 requests 사용
from gpiozero import MotionSensor

# ==========================================
# 1. 하드웨어 및 텔레그램 기본 설정
# ==========================================
# PIR 인체 감지 센서 설정 (GPIO 16번 핀 사용)
pir = MotionSensor(16)

# 텔레그램 알림용 봇 토큰 및 사용자 ID 설정
TELEGRAM_TOKEN = "8788783011:AAFWfn213e4UEn3E954XM9kBxa3MK8yjHC4"
CHAT_ID = "8210798076"

# IP 웹캠(DroidCam) 스트리밍 URL
DROIDCAM_URL = "http://172.30.1.25:4747/video"

# ==========================================
# 2. Open CV DNN AI 모델 로드 (수업 자료 참고)
# ==========================================
# Haar Cascade 기반 얼굴 검출 파일 로드
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Caffe 프레임워크 기반의 나이/성별 예측 사전학습 모델 로드
age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')

# 모델 출력값 매핑을 위한 레이블 리스트 정의
age_list = ['(0 ~ 2)', '(4 ~ 6)', '(8 ~ 12)', '(15 ~ 20)', '(25 ~ 32)', '(38 ~ 43)', '(48 ~ 53)', '(60 ~ 100)']
gender_list = ['Male', 'Female']

# 모델 학습에 사용된 이미지 평균값 (채널별 RGB 백그라운드 차감용)
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# ==========================================
# 3. 메인 제어 루프
# ==========================================
def main():
    print("보안 시스템 가동 중...")
    
    # DroidCam 비디오 스트리밍 연결 시도
    camera = cv2.VideoCapture(DROIDCAM_URL)
    
    while camera.isOpened():
        # PIR 센서에 움직임이 감지되면 (HIGH 상태)
        if pir.value == 1:
            print("침입자 감지! 사진 촬영을 시작합니다.")
            
            # 실시간 화면 유지를 위해 카메라 버퍼에 쌓인 이전 프레임 비우기
            for i in range(3):
                camera.read()
                
            _, img = camera.read()
            if img is None:
                continue
            
            # 연산 속도 향상 및 정확도를 위해 흑백 이미지로 변환 후 얼굴 검출
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
            
            info = "Unknown"
            
            # 검출된 얼굴 영역이 존재하면 루프 진입
            for (x, y, w, h) in faces:
                # 원본 이미지에서 얼굴 영역(ROI)만 크롭
                face = img[int(y):int(y+h), int(x):int(x+w)].copy()
                if face.size == 0:
                    continue
                
                # DNN 모델 입력 규격(227x227)에 맞게 블롭(Blob) 생성 및 전처리
                blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                
                # 성별 예측 진행 및 최대 확률값 인덱스 추출
                gender_net.setInput(blob)
                gender_preds = gender_net.forward()
                gender = gender_list[gender_preds.argmax()]
                
                # 나이 예측 진행 및 최대 확률값 인덱스 추출
                age_net.setInput(blob)
                age_preds = age_net.forward()
                age = age_list[age_preds.argmax()]
                
                info = "Gender: " + gender + ", Age: " + age
                
                # 시각화를 위해 검출된 얼굴에 사각형을 그리고 분석 정보 텍스트 삽입
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(img, info, (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                break  # 다중 검출 시에도 과부하 방지를 위해 첫 번째 얼굴만 처리
            
            # 전송할 최종 분석 이미지 저장
            cv2.imwrite("alert.jpg", img)
            
            # 텔레그램 API 엔드포인트 설정
            text_url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
            photo_url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendPhoto"
            
            # 1. 침입 알림 텍스트 메시지 발송
            message = "[경보] 침입자 발생! 분석 결과: " + info
            requests.post(text_url, data={"chat_id": CHAT_ID, "text": message})
            
            # 2. 캡처된 훼손/분석 파일 전송
            with open("alert.jpg", "rb") as f:
                requests.post(photo_url, data={"chat_id": CHAT_ID}, files={"photo": f})
                
            print("텔레그램 전송 완료.")
            
            # 메시지 연속 도배 및 과부하 방지를 위한 딜레이 시간 적용
            time.sleep(5.0)
            print("다시 감시 중...")
            
        time.sleep(0.1)

    camera.release()

if __name__ == '__main__':
    main()
