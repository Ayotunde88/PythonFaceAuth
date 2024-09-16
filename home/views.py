from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from facedetector.settings import BASE_DIR
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import face_recognition
import dlib
import os
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def passParam(first_name, last_name, email, phonenumber):
    return first_name, last_name, email, phonenumber


predictor_path = os.path.join(BASE_DIR, 'models/shape_predictor_68_face_landmarks.dat')
face_recognition_model_path = os.path.join(BASE_DIR, 'models/dlib_face_recognition_resnet_model_v1.dat')

# Initialize dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_recognition_model_path)

def encode_face(image):
    # Load the image
    image = Image.open(BytesIO(image.read()))
    image_np = np.array(image)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    detections = detector(gray)
    
    if len(detections) == 0:
        raise ValueError("No face detected")
    
    # Extract features for the first detected face
    for detection in detections:
        shape = sp(gray, detection)
        face_descriptor = facerec.compute_face_descriptor(gray, shape)
        return np.array(face_descriptor)
    
    raise ValueError("Face could not be encoded")

def home(request):
    
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def basic_info(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')

        if not all([first_name, last_name, email, phonenumber]):
            print('All fields are required')
            messageClass = 'basicinfo'
            return JsonResponse({'status': 'error', 'message': 'All fields are required','messageclass':messageClass})
        
        passParam(first_name, last_name, email, phonenumber)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def other_details(request):
    if request.method == 'POST':
        purposeOfVisit = request.POST.get('purposeOfVisit')
        visitingWhom = request.POST.get('visitingWhom')
        if not all([purposeOfVisit, visitingWhom]):
            print('All fields are required')
            messageClass = 'otherdetails'
            return JsonResponse({'status': 'error', 'message': 'All fields are required','messageclass':messageClass})
        
        print('success')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def biometric(request):
    if request.method == 'POST':
        if 'face_image' in request.FILES:
            image_file = request.FILES['face_image']
            file_name = default_storage.save('temp_face_image.jpg', image_file)
            file_path = default_storage.path(file_name)

            # Load the image
            image = face_recognition.load_image_file(file_path)
            print(image)
            uploaded_face_encoding = face_recognition.face_encodings(image)
            if not uploaded_face_encoding:
                return JsonResponse({'status': 'fail', 'message': 'No face detected in the uploaded image'})

            uploaded_face_encoding = uploaded_face_encoding[0]
            print(uploaded_face_encoding)
            # Compare with faces in the database
            all_faces = Users.objects.all()
            for face in all_faces:
                stored_face_encoding = np.frombuffer(face.features, dtype=np.float64)
                match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)

                if match[0]:
                    print("Face match found")
                    return JsonResponse({'status': 'success', 'message': 'Face match found'})
        
            # # If no match found, save the new face encoding in the database
            # new_face_features = uploaded_face_encoding.tobytes()
            # new_face_image = Users(image=file_name, features=new_face_features)
            # new_face_image.save()

            return JsonResponse({'status': 'success', 'message': 'Face added to database and detected'})

        else:
            return JsonResponse({'status': 'fail', 'message': 'No image file uploaded'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method'})

