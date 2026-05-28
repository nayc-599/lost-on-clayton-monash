# this file maps each building with the faculties that building accomodates for

from __future__ import annotations

# we have 11 buildings, map faculties that host their classes in the buildings to the building
FACULTY_TO_BUILDINGS: dict[str, list[str]] = {
    "Arts": ["Menzies", "Matheson Library", "LTB", "Monash Sport"],
    
    "Arts, Design and Architecture": ["Menzies", "Matheson Library", "LTB"],
    
    "Business and Economics": ["BLTB", "Campus Centre", "LTB", "Matheson Library", "Mathematics Building", "Menzies", "Monash Sport", "Science Lectures"],
    
    "Engineering": ["Alan Finkle", "Hargrave Library", "LTB", "Mathematics Building"],
    
    "Information Technology": ["Alan Finkle", "Hargrave Library", "LTB"],
    
    "Science": ["BLTB", "Hargrave Library", "LTB", "Mathematics Building", "Science Lectures", "Senior physics"],
    
    "Education": ["Matheson Library", "LTB", "Monash Sport", "Science Lectures"],
    
    "Law": ["Menzies", "LTB"],
    
    "Medicine, Nursing and Health Sciences": ["BLTB", "Hargrave Library", "Monash Sport", "Science Lectures"]
} 