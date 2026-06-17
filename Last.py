import cv2
import time
import requests  # 수업 시간에 사용한 간단한 telegram 전송 방식을 위해 requests 사용
from gpiozero import MotionSensor

# ==========================================
# 1. 하드웨어 및 텔레그램 기본 설정
# ==========================================
# [Section 3] PIR 인체 감지 센서 설정 (GPIO 16번 핀)
pir = MotionSensor(16)

# [Section 7] 텔레그램 봇 설정 (수업 시간 기본 방식)
TELEGRAM_TOKEN = "8788783011:AAFWfn213e4UEn3E954XM9kBxa3MK8yjHC4"
CHAT_ID = "8210798076"

# DroidCam 스트리밍 URL 설정
DROIDCAM_URL = "http://172.30.1.25:4747/video"

# ==========================================
# 2. AI 모델 불러오기 (수업 자료 파일 마지막 페이지 코드 그대로 반영)
# ==========================================
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# 나이 예측 모델 불러오기
age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')
# 성별 예측 모델 불러오기
gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')

# 나이 및 성별 예측 결과 레이블 (수업 자료와 100% 일치)
age_list = ['(0 ~ 2)', '(4 ~ 6)', '(8 ~ 12)', '(15 ~ 20)', '(25 ~ 32)', '(38 ~ 43)', '(48 ~ 53)', '(60 ~ 100)']
gender_list = ['Male', 'Female']
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# ==========================================
# 3. 메인 루프 (수업 시간 while문 스타일)
# ==========================================
def main():
    print("보안 시스템 가동 중...")
    
    # DroidCam 비디오 연결
    camera = cv2.VideoCapture(DROIDCAM_URL)
    
    while camera.isOpened():
        # PIR 센서가 감지되면 (값 1)
        if pir.value == 1:
            print("침입자 감지! 사진 촬영을 시작합니다.")
            
            # DroidCam 버퍼 비우기 (최신 화면 확보)
            for i in range(3):
                camera.read()
                
            _, img = camera.read()
            if img is None:
                continue
            
            # 수업 자료 흐름: 흑백 변환 후 얼굴 검출
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
            
            info = "Unknown"
            
            # 검출된 얼굴 분석
            for (x, y, w, h) in faces:
                face = img[int(y):int(y+h), int(x):int(x+w)].copy()
                if face.size == 0:
                    continue
                
                # 가중치 분석용 blob 생성
                blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                
                # 성별 예측
                gender_net.setInput(blob)
                gender_preds = gender_net.forward()
                gender = gender_list[gender_preds.argmax()]
                
                # 나이 예측
                age_net.setInput(blob)
                age_preds = age_net.forward()
                age = age_list[age_preds.argmax()]
                
                info = "Gender: " + gender + ", Age: " + age
                
                # 이미지에 사각형 및 텍스트 그리기
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(img, info, (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                break  # 첫 번째 얼굴만 처리하고 나감
            
            # 분석된 이미지 저장
            cv2.imwrite("alert.jpg", img)
            
            # [Section 7] 텔레그램 메시지 및 사진 전송 (기본 requests 방식)
            text_url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
            photo_url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendPhoto"
            
            # 1. 텍스트 경보 전송
            message = "[경보] 침입자 발생! 분석 결과: " + info
            requests.post(text_url, data={"chat_id": CHAT_ID, "text": message})
            
            # 2. 사진 전송
            with open("alert.jpg", "rb") as f:
                requests.post(photo_url, data={"chat_id": CHAT_ID}, files={"photo": f})
                
            print("텔레그램 전송 완료.")
            
            # 감지 후 도배 방지를 위한 대기 시간
            time.sleep(5.0)
            print("다시 감시 중...")
            
        time.sleep(0.1)

    camera.release()

if __name__ == '__main__':
    main()
