import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import requests
import time
from datetime import datetime

# 📩 Webhook Discord (remplace par le tien)
WEBHOOK_URL = "https://discord.com/api/webhooks/your_WEBHOOK"

# ⏱ Temps minimum entre deux alertes (en secondes)
ALERT_COOLDOWN = 8

# 📊 Compteurs
bird_count_hour = 0  # Nombre d'oiseaux détectés dans l'heure
bird_count_daily = {}  # Stockage des détections par heure

# 🕒 Initialisation du temps
last_alert_time = 0
current_hour = datetime.now().hour

# 📷 Initialisation de la caméra
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 1280)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# 🎯 Chargement du modèle YOLO
model = YOLO("yolov8n_ncnn_model")

# 📤 Fonction d'envoi de l'alerte Discord avec image
def send_discord_alert(message, image_path=None):
    files = {"file": open(image_path, "rb")} if image_path else None
    data = {"content": message}
    response = requests.post(WEBHOOK_URL, data=data, files=files)
    if response.status_code in [200, 204]:
        print("✅ Alerte envoyée")
    else:
        print("❌ Erreur Discord:", response.text)

# 📤 Fonction d'envoi du résumé horaire
def send_hourly_summary():
    global bird_count_hour, bird_count_daily
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    # Sauvegarde des résultats
    bird_count_daily[now.hour] = bird_count_hour
    # Envoi du résumé
    summary_msg = f"📊 Rapport horaire ({timestamp})\nTotal oiseaux détectés cette heure : {bird_count_hour}"
    send_discord_alert(summary_msg)
    # Réinitialisation du compteur horaire
    bird_count_hour = 0

# 📤 Fonction d'envoi du résumé journalier
def send_daily_summary():
    global bird_count_daily
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y")
    # Création du message récapitulatif
    summary_msg = f"📅 Rapport de la journée ({timestamp})\n"
    total_birds = 0
    for hour, count in bird_count_daily.items():
        summary_msg += f"🕒 {hour}h - {count} oiseaux détectés\n"
        total_birds += count
    summary_msg += f"\n🔢 Total de la journée : {total_birds} oiseaux détectés"
    send_discord_alert(summary_msg)
    # Réinitialisation des données pour la nouvelle journée
    bird_count_daily = {}

# 🔄 Boucle principale
while True:
    frame = picam2.capture_array()
    results = model(frame)
    annotated_frame = results[0].plot()

    # Détection des classes présentes
    detected_classes = [results[0].names[int(cls)] for cls in results[0].boxes.cls]

    # Vérifie l'heure actuelle
    now = datetime.now()
    if now.hour != current_hour:
        send_hourly_summary()  # Envoi du résumé horaire
        current_hour = now.hour  # Mise à jour de l'heure de référence

    if now.hour == 0 and now.minute == 0:
        # À minuit, on envoie le résumé journalier
        send_daily_summary()

    # Vérifie si un oiseau est détecté ET qu'on respecte le délai
    current_time = time.time()
    if "bird" in detected_classes and current_time - last_alert_time > ALERT_COOLDOWN:
        bird_count_hour += 1  # Incrémente le compteur horaire

        # 🖼 Sauvegarde image annotée
        image_path = "/tmp/oiseau_detecte.jpg"
        cv2.imwrite(image_path, annotated_frame)

        # 📤 Envoi message + image
        message = f"🦜 Un oiseau a été détecté !\n📅 Heure : {now.strftime('%H:%M:%S')}"
        send_discord_alert(message, image_path)

        # ⏱ Mise à jour du dernier envoi
        last_alert_time = current_time

    # Affichage FPS
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time
    text = f'FPS: {fps:.1f}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = annotated_frame.shape[1] - text_size[0] - 10
    text_y = text_size[1] + 10
    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Affichage image
    cv2.imshow("Camera", annotated_frame)

    # Sortie si touche "q"
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()