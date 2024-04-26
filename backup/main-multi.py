import cv2
import numpy as np
import imutils
import easyocr

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

# Inisialisasi pembaca OCR
reader = easyocr.Reader(['en'])

# Buat struktur data untuk mapping nomor plat ke nama orang
plate_to_name = {
    "123": "Yoga",
    "456": "Nanang",
}

while True:
    # Baca frame dari webcam
    ret, frame = cap.read()

    # Ubah frame menjadi grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Reduksi noise
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

    # Deteksi tepi
    edged = cv2.Canny(bfilter, 30, 200)

    # Temukan kontur
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx

            # Buat mask
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0, 255, -1)
            new_image = cv2.bitwise_and(frame, frame, mask=mask)

            # Temukan koordinat kotak pembatas
            (x, y) = np.where(mask == 255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))

            # Potong gambar
            cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

            # Lakukan OCR pada gambar yang dipotong
            result = reader.readtext(cropped_image)

            # Ekstrak teks
            if result:
                text = result[0][-2]

                # Validasi nomor plat dan cetak nama orang di terminal
                if text in plate_to_name:
                    name = plate_to_name[text]
                    print("Nomor ID:", text)
                    print("Nama Pemilik:", name)

                    # Gambar teks dan kotak pembatas pada gambar asli
                    font = cv2.FONT_HERSHEY_SIMPLEX 
                    frame = cv2.putText(frame, text=name, org=(location[0][0][0], location[1][0][1] + 60), fontFace=font,
                                        fontScale=1, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
                    frame = cv2.rectangle(frame, tuple(location[0][0]), tuple(location[2][0]), (255, 255, 255), 3)

    # Tampilkan frame
    cv2.imshow('License Plate Recognition', frame)

    # Tahan tampilan frame sampai tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup webcam dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
