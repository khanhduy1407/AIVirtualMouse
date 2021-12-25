"""
AI Virtual Mouse
Bởi: NKDuy
"""

import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy   # pip install autopy==4.0.0

#################
wCam, hCam = 640, 480
frameR = 100  # Giảm khung hình
smoothening = 7
#################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    # 1. Tìm dấu vân tay
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Lấy đầu ngón trỏ và ngón giữa
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Kiểm tra ngón tay nào hướng lên
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255))

        # 4. Chỉ ngón trỏ: Chế độ di chuyển
        if fingers[1] == 1 and fingers[2] == 0:

            # 5. Chuyển đổi tọa độ
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # 6. Làm mượt giá trị
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Di chuyển chuột
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Cả ngón trỏ và ngón giữa đều hướng lên: Chế độ nhấp
        if fingers[1] == 1 and fingers[2] == 1:

            # 9. Tìm khoảng cách giữa các ngón tay
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)

            # 10. Nhấp chuột nếu khoảng cách ngắn
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11. Tỷ lệ khung hình
    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12. Hiển thị
    cv2.imshow("Virtual Mouse", cv2.flip(img, 1))
    cv2.waitKey(1)
