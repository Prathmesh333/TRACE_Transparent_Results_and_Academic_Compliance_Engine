"""
Opti-Scholar: Correlation Engine Service
Pearson correlation between attendance and grades
"""

import numpy as np
from scipy import stats
from typing import List, Optional


class CorrelationEngine:
    """Calculate attendance-grade correlations by subject."""
    
    # Significance thresholds
    CRITICAL_THRESHOLD = 0.7
    MODERATE_THRESHOLD = 0.4
    
    def __init__(self):
        """Initialize correlation engine."""
        pass
    
    async def analyze(
        self,
        student_id: str,
        subject_data: Optional[dict] = None
    ) -> dict:
        """
        Analyze attendance-grade correlation by subject.
        
        Args:
            student_id: Student identifier
            subject_data: Optional subject performance data
            
        Returns:
            Correlations by subject with significance levels
        """
        # Fetch subject data if not provided
        if subject_data is None:
            subject_data = await self._fetch_subject_data(student_id)
        
        correlations = []
        
        for subject, data in subject_data.items():
            attendance_rates = data.get("attendance_rates", [])
            grades = data.get("grades", [])
            
            if len(attendance_rates) < 3 or len(grades) < 3:
                continue
            
            # Ensure equal length
            min_len = min(len(attendance_rates), len(grades))
            attendance_rates = attendance_rates[:min_len]
            grades = grades[:min_len]
            
            # Calculate Pearson correlation
            r, p_value = stats.pearsonr(attendance_rates, grades)
            
            # Determine significance
            abs_r = abs(r)
            if abs_r >= self.CRITICAL_THRESHOLD:
                significance = "critical"
                interpretation = f"Strong correlation - attendance highly impacts grades"
            elif abs_r >= self.MODERATE_THRESHOLD:
                significance = "moderate"
                interpretation = f"Moderate correlation - attendance matters for this subject"
            else:
                significance = "low"
                interpretation = f"Weak correlation - flexible attendance may be acceptable"
            
            correlations.append({
                "subject": subject,
                "pearson_r": round(r, 2),
                "p_value": round(p_value, 4),
                "significance": significance,
                "interpretation": interpretation
            })
        
        # Sort by absolute correlation strength
        correlations.sort(key=lambda x: abs(x["pearson_r"]), reverse=True)
        
        return {
            "correlations": correlations
        }
    
    async def _fetch_subject_data(self, student_id: str) -> dict:
        """Fetch subject performance data from database."""
        # TODO: Implement actual database query
        # For demo, return sample data
        
        return {
            "Mathematics": {
                "attendance_rates": [95, 90, 85, 92, 88, 95, 80, 85, 90, 92],
                "grades": [9.0, 8.5, 8.0, 9.0, 8.2, 9.2, 7.0, 7.5, 8.5, 9.0]
            },
            "Physics": {
                "attendance_rates": [90, 85, 88, 92, 87, 90, 85, 88, 92, 90],
                "grades": [8.5, 8.0, 8.2, 8.8, 8.0, 8.5, 7.8, 8.0, 8.7, 8.5]
            },
            "Art": {
                "attendance_rates": [70, 85, 60, 95, 75, 65, 90, 80, 70, 85],
                "grades": [8.0, 8.2, 7.5, 8.5, 8.0, 8.0, 8.3, 8.0, 7.8, 8.2]
            },
            "History": {
                "attendance_rates": [85, 88, 82, 90, 85, 88, 80, 85, 90, 88],
                "grades": [7.5, 7.8, 7.2, 8.0, 7.5, 7.8, 7.0, 7.5, 8.0, 7.8]
            }
        }
