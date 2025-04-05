import easyocr
import torch
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class IDCard:
    def __init__(self):
        self.name: str = ""
        self.college: str = ""
        self.department: str = ""
        self.student_id: int = 0
        self.gary = None
        self.blurred = None
        self.edged = None

    def process_image(self, src: np.ndarray) -> tuple:
        # Convert to grayscale
        gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply Canny edge detection
        edged = cv2.Canny(blurred, 75, 200)
        
        return (gray, blurred, edged)
    
    def __str__(self):
        return f"Name: {self.name}, College: {self.college}, Department: {self.department}, Student ID: {self.student_id}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "college": self.college,
            "department": self.department,
            "student_id": self.student_id
        }

class KyungheeLagacy(IDCard):
    def __init__(self, src: np.ndarray):
        super().__init__()
        self.src = src
        self.edged = self.process_image()
        self.reader = easyocr.Reader(['en', 'ko'], gpu=torch.cuda.is_available())
        self.result = self.reader.readtext(self.edged, detail=0)

    def extract_info(self):
        # Extract name, college, department, student ID from the result
        for text in self.result:
            if "Name" in text:
                self.name = text.split(":")[1].strip()
            elif "College" in text:
                self.college = text.split(":")[1].strip()
            elif "Department" in text:
                self.department = text.split(":")[1].strip()
            elif "Student ID" in text:
                self.student_id = int(text.split(":")[1].strip())

class Kyunghee(IDCard):
    def __init__(self, src: np.ndarray):
        super().__init__()
        self.src = src
        self.edged = self.process_image()
        self.reader = easyocr.Reader(['en', 'ko'], gpu=torch.cuda.is_available())
        self.result = self.reader.readtext(self.edged, detail=0)

    def extract_info(self):
        # Extract name, college, department, student ID from the result
        for text in self.result:
            if "Name" in text:
                self.name = text.split(":")[1].strip()
            elif "College" in text:
                self.college = text.split(":")[1].strip()
            elif "Department" in text:
                self.department = text.split(":")[1].strip()
            elif "Student ID" in text:
                self.student_id = int(text.split(":")[1].strip())
