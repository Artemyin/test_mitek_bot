import face_recognition
from PIL import Image, ImageDraw


def draw_box_face_locations(file):
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
    face_encodings = face_recognition.face_encodings(image, face_locations)
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    pil_image.save(file)
    return len(face_locations)
