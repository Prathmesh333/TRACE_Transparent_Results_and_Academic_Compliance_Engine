"""
Opti-Scholar: Distribution Analyzer Service
Grade distribution health analysis with skewness and kurtosis
"""

import numpy as np
from scipy import stats
from typing import List, Optional


class DistributionAnalyzer:
    """Analyze grade distribution health using statistical measures."""
    
    def __init__(self, skewness_threshold: float = 1.0, kurtosis_threshold: float = 2.0):
        """
        Initialize analyzer.
        
        Args:
            skewness_threshold: Threshold for skewness alert
            kurtosis_threshold: Threshold for kurtosis alert
        """
        self.skewness_threshold = skewness_threshold
        self.kurtosis_threshold = kurtosis_threshold
    
    async def analyze(
        self,
        exam_id: str,
        grades: Optional[List[float]] = None
    ) -> dict:
        """
        Analyze grade distribution for an exam.
        
        Args:
            exam_id: Exam identifier
            grades: Optional list of grades (fetched if not provided)
            
        Returns:
            Distribution analysis with statistics and health indicators
        """
        # Fetch grades if not provided
        if grades is None:
            grades = await self._fetch_exam_grades(exam_id)
        
        if len(grades) < 5:
            return self._insufficient_data_result()
        
        grades_array = np.array(grades)
        
        # Calculate descriptive statistics
        count = len(grades_array)
        mean = float(np.mean(grades_array))
        median = float(np.median(grades_array))
        std = float(np.std(grades_array))
        min_score = float(np.min(grades_array))
        max_score = float(np.max(grades_array))
        
        # Calculate distribution shape
        skewness = float(stats.skew(grades_array))
        kurtosis = float(stats.kurtosis(grades_array))
        
        # Normality test (Shapiro-Wilk for small samples)
        if count <= 50:
            _, p_value = stats.shapiro(grades_array)
        else:
            _, p_value = stats.normaltest(grades_array)
        
        is_normal = p_value > 0.05
        
        # Health check
        is_healthy = True
        alert_type = None
        recommendation = None
        
        if skewness > self.skewness_threshold:
            is_healthy = False
            alert_type = "inflation"
            recommendation = "Grade distribution is right-skewed - possible grade inflation"
        elif skewness < -self.skewness_threshold:
            is_healthy = False
            alert_type = "deflation"
            recommendation = "Grade distribution is left-skewed - possible harsh grading"
        elif abs(kurtosis) > self.kurtosis_threshold:
            is_healthy = False
            alert_type = "clustering"
            recommendation = "Unusual clustering in grade distribution - review grading rubric"
        
        # Generate histogram bins
        histogram = self._generate_histogram(grades_array)
        
        return {
            "count": count,
            "mean": mean,
            "median": median,
            "std_dev": std,
            "min": min_score,
            "max": max_score,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "is_normal": is_normal,
            "is_healthy": is_healthy,
            "alert_type": alert_type,
            "recommendation": recommendation,
            "histogram": histogram
        }
    
    def _generate_histogram(self, grades: np.ndarray) -> list:
        """Generate histogram bins for visualization."""
        bins = [
            (0, 2, "0-2"),
            (3, 4, "3-4"),
            (5, 6, "5-6"),
            (7, 8, "7-8"),
            (9, 10, "9-10")
        ]
        
        histogram = []
        for low, high, label in bins:
            count = int(np.sum((grades >= low) & (grades <= high)))
            histogram.append({"bin": label, "count": count})
        
        return histogram
    
    def _insufficient_data_result(self) -> dict:
        """Return result for insufficient data."""
        return {
            "count": 0,
            "mean": 0.0,
            "median": 0.0,
            "std_dev": 0.0,
            "min": 0.0,
            "max": 0.0,
            "skewness": 0.0,
            "kurtosis": 0.0,
            "is_normal": True,
            "is_healthy": True,
            "alert_type": None,
            "recommendation": "Insufficient data for analysis",
            "histogram": []
        }
    
    async def _fetch_exam_grades(self, exam_id: str) -> List[float]:
        """Fetch all grades for an exam from database."""
        # TODO: Implement actual database query
        # For demo, return sample distribution
        return [
            8.5, 7.0, 9.0, 6.5, 8.0, 7.5, 9.5, 6.0, 8.5, 7.0,
            8.0, 7.5, 9.0, 6.5, 8.5, 7.0, 8.5, 7.5, 8.0, 7.0,
            9.0, 8.0, 7.5, 8.5, 7.0, 8.0, 9.0, 7.5, 8.0, 7.5,
            3.5, 4.0, 9.5, 10.0, 8.5, 7.0, 8.0, 7.5, 8.5, 7.0,
            8.0, 9.0, 7.5, 8.0, 7.0
        ]
