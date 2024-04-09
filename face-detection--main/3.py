import os
import face_recognition
import pyttsx3

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            images.append(face_recognition.load_image_file(img_path))
    return images

def compare_faces(face_encoding, known_face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    return any(matches)

def get_face_encodings(images):
    face_encodings = []
    for img in images:
        face_locations = face_recognition.face_locations(img)
        if face_locations:
            face_encoding = face_recognition.face_encodings(img, face_locations)[0]
            face_encodings.append(face_encoding)
    return face_encodings

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_face(input_image_path, dataset_folder):
    
    input_image = face_recognition.load_image_file(input_image_path)

    dataset_persons = ["ashwanth", "gautam", "deena", "dhivya"]
    dataset_images = {person: load_images_from_folder(os.path.join(dataset_folder, person)) for person in dataset_persons}

    input_face_encodings = face_recognition.face_encodings(input_image)

    if not input_face_encodings:
        print("No face found in the input image. Obstacle detected.")
        text_to_speech("No face found in the input image. Obstacle detected.")
        return

    for person, person_images in dataset_images.items():
        known_face_encodings = get_face_encodings(person_images)

        for input_face_encoding in input_face_encodings:
            if known_face_encodings and compare_faces(input_face_encoding, known_face_encodings):
                print(f"Human face detected and {person}'s face recognized!")
                text_to_speech(f"Human face detected and {person}'s face recognized!")
                return

    print("Human face detected, but known faces not recognized.")
    text_to_speech("Human face detected, but known faces not recognized.")

image_name = input("Enter the image name with the format .jpeg/jpg/png: ")
image_path = os.path.join('.', image_name)

recognize_face(image_path, r'.\dataset')
