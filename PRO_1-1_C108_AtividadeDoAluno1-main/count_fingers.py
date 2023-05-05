import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

#faz os pontos
mp_hands = mp.solutions.hands

#liga os pontos
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Defina uma função para contar os dedos
def countFingers(image, hand_landmarks, handNo=0):
    print()
    if(hand_landmarks):
        landmarks = hand_landmarks[handNo].landmark
        fingers = []
        for lm_index in tipIds:
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index-2].y

            thumb_tip_x = landmarks[lm_index].x
            thumb_bottom_x = landmarks[lm_index-2].x
            if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        print("DEDO com id ",lm_index," está Aberto")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        print("DEDO com id ",lm_index," está Fechado")
            else:
                    if thumb_tip_x > thumb_bottom_x:
                        fingers.append(1)
                        print("POLEGAR está Aberto")

                    if thumb_tip_x < thumb_bottom_x:
                        fingers.append(0)
                        print("POLEGAR está Fechado")
        total_fingers = fingers.count(1)
        text = f"dedos: {total_fingers}"
        cv2.putText(image,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)            


# Defina uma função para 
def drawHandLanmarks(image, hand_landmarks):

    # Desenhar as conexões entre os pontos de referência
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detecte os pontos de referência das mãos 
    results = hands.process(image)

    # Obtenha a posição do ponto de referência do resultado processado
    hand_landmarks = results.multi_hand_landmarks

    # Desenhe os pontos de referência
    drawHandLanmarks(image, hand_landmarks)

    # Obtenha a posição dos dedos da mão        
    countFingers(image,hand_landmarks)

    cv2.imshow("Controlador de Midia", image)

    # Saia da tela ao pressionar a barra de espaços
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
