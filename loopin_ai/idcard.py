import easyocr
import torch
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from boundbox import BoundBox

DEPARTMENT_DATA_PATH = Path(__file__).parent.parent / Path('data/departments.csv')
dapartments_table = np.loadtxt(str(DEPARTMENT_DATA_PATH), dtype=str, delimiter=',', encoding='utf-8')

def get_college(input: str) -> tuple:
    colleges = dapartments_table[0]
    max_index = -1
    max_similarity = 0.0

    for i, college in enumerate(colleges):
        intersection = len(set.intersection(*[set(input), set(college)]))
        union = len(set.union(*[set(input), set(college)]))
        jaccard_similarity = intersection / float(union)
        if jaccard_similarity > max_similarity:
            max_similarity = jaccard_similarity
            max_index = i

    if max_similarity > 0.67:
        return max_index, colleges[max_index]
    else:
        return -1, None
    

def get_department(college_index: int, input: str) -> tuple:
    departments_in_college = []
    max_index = -1
    max_similarity = 0.0

    for i, row in enumerate(dapartments_table):
        if i == 0:
            continue
        if row[college_index] != "":
            departments_in_college.append(row[college_index])

    for i, department in enumerate(departments_in_college):
        intersection = len(set.intersection(*[set(input), set(department)]))
        union = len(set.union(*[set(input), set(department)]))
        jaccard_similarity = intersection / float(union)
        if jaccard_similarity > max_similarity:
            max_similarity = jaccard_similarity
            max_index = i
            
    if max_similarity > 0.67:
        return max_index + 1, departments_in_college[max_index] 
    else:
        return -1, None
        

class IDCard:
    def __init__(self):
        self.universityName: str = ""
        self.name: str = ""
        self.college: str = ""
        self.department: str = ""
        self.student_id: int = 0
        self.gray = None
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
        self.universityName: str = "경희대학교"
        self.src = src
        self.gray, self.blurred, self.edged = self.process_image(self.src)
        self.reader = easyocr.Reader(['en', 'ko'], gpu=torch.cuda.is_available())
        self.result = self.reader.readtext(self.src, detail=1)[:4]
        self.name, self.college, self.department, self.student_id = self.extract_info()
        print("Done")

    def extract_info(self):
        src_h = (float)(self.src.shape[0])
        src_w = (float)(self.src.shape[1])

        name_data = self.result[0]
        box = name_data[0]
        name = name_data[1]
        name_box_normalized = BoundBox((float)(box[0][0]) / src_w, (float)(box[0][1]) / src_h, (float)(box[2][0]) / src_w, (float)(box[2][1]) / src_h)
        print(name_box_normalized)
        if not name_box_normalized.is_point_inside(0.35, 0.1):
            return None
        
        
        college_data = self.result[1]
        box = college_data[0]
        college_index, college = get_college(college_data[1])
        college_box_normalized = BoundBox((float)(box[0][0]) / src_w, (float)(box[0][1]) / src_h, (float)(box[2][0]) / src_w, (float)(box[2][1]) / src_h)
        print(college_box_normalized)
        if(not college_box_normalized.is_point_inside(0.35, 0.19)) or college_index == -1:
            return None

        department_data = self.result[2]
        box = department_data[0]
        department_input = department_data[1]

        # 세부전공 정보 제거
        if("|" in department_input):
            department_input = department_input.split("|")[0]
            department_input.strip()
        elif("/") in department_input:
            department_input = department_input.split("/")[0]
            department_input.strip()
        
        department_index, department = get_department(college_index, department_input)
        department_box_normalized = BoundBox((float)(box[0][0]) / src_w, (float)(box[0][1]) / src_h, (float)(box[2][0]) / src_w, (float)(box[2][1]) / src_h)
        print(department_box_normalized)
        if(not department_box_normalized.is_point_inside(0.35, 0.25)) or department_index == -1:
            return None

        student_id_data = self.result[3]
        box = student_id_data[0]
        if len(student_id_data[1]) != 10:
            return None
        try:
            student_id = int(student_id_data[1])
        except:
            return None
        student_id_box_normalized = BoundBox((float)(box[0][0]) / src_w, (float)(box[0][1]) / src_h, (float)(box[2][0]) / src_w, (float)(box[2][1]) / src_h)
        print(student_id_box_normalized)
        if(not student_id_box_normalized.is_point_inside(0.35, 0.33)):
            return None
        
        return (name, college, department, student_id)

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
