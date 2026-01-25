"""
Opti-Scholar: Anomaly Detector Service
Z-score based temporal anomaly detection for grades
"""

import numpy as np
from typing import Optional, List


class AnomalyDetector:
    """Detect temporal anomalies in student grades using statistical analysis."""
    
    def __init__(self, threshold: float = 2.5, window_size: int = 5):
        """
        Initialize detector.
        
        Args:
            threshold: Z-score threshold for flagging (default 2.5)
            window_size: Number of historical grades to consider
        """
        self.threshold = threshold
        self.window_size = window_size
    
    async def detect(
        self,
        student_id: str,
        current_score: float,
        exam_id: str,
        historical_grades: Optional[List[float]] = None
    ) -> dict:
        """
        Detect if current grade is anomalous for a student.
        
        Uses Z-score analysis: z = (x - μ) / σ
        
        Args:
            student_id: Student identifier
            current_score: The new grade to check
            exam_id: Current exam identifier
            historical_grades: Optional list of past grades (fetched if not provided)
            
        Returns:
            Anomaly detection result
        """
        # Fetch historical grades if not provided
        if historical_grades is None:
            historical_grades = await self._fetch_historical_grades(student_id)
        
        # Need minimum history for analysis
        if len(historical_grades) < 3:
            return {
                "is_anomaly": False,
                "z_score": 0.0,
                "direction": None,
                "historical_mean": current_score,
                "historical_std": 0.0,
                "window_size": len(historical_grades),
                "recommendation": "Insufficient history for analysis",
                "alert_level": "normal"
            }
        
        # Calculate statistics
        grades_array = np.array(historical_grades[-self.window_size:])
        mean = float(np.mean(grades_array))
        std = float(np.std(grades_array))
        
        # Handle zero standard deviation
        if std < 0.01:
            std = 1.0  # Prevent division by zero
        
        # Calculate Z-score
        z_score = (current_score - mean) / std
        
        # Determine if anomaly
        is_anomaly = abs(z_score) > self.threshold
        
        # Determine direction
        if z_score > self.threshold:
            direction = "spike"
            recommendation = "Unusually high score - verify for integrity"
            alert_level = "warning"
        elif z_score < -self.threshold:
            direction = "drop"
            recommendation = "Significant grade drop - student may need support"
            alert_level = "warning"
        else:
            direction = None
            recommendation = None
            alert_level = "normal"
        
        return {
            "is_anomaly": is_anomaly,
            "z_score": float(z_score),
            "direction": direction,
            "historical_mean": mean,
            "historical_std": std,
            "window_size": len(grades_array),
            "recommendation": recommendation,
            "alert_level": alert_level
        }
    
    async def _fetch_historical_grades(self, student_id: str) -> List[float]:
        """Fetch historical grades for a student from database."""
        # TODO: Implement actual database query
        # For demo, return sample data
        
        if student_id == "STU-404":
            # Demo student with consistent high grades
            return [9.0, 9.2, 8.8, 9.5, 9.0]
        else:
            # Random sample for other students
            return [7.0, 7.5, 6.8, 7.2, 7.0]
