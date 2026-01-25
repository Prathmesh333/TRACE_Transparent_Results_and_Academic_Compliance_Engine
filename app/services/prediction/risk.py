"""
Opti-Scholar: Risk Classifier Service
Dropout risk prediction using logistic regression
"""

import numpy as np
from typing import Optional, List


class RiskClassifier:
    """Predict dropout risk using logistic regression."""
    
    # Feature weights (pre-trained or configured)
    FEATURE_WEIGHTS = {
        "attendance_rate": -3.5,      # Higher attendance = lower risk
        "grade_average": -2.5,        # Higher grades = lower risk
        "attendance_trend": -1.5,     # Improving trend = lower risk
        "days_since_absence": -0.8,   # More days = lower risk
        "pattern_flags": 1.2,         # More flags = higher risk
    }
    INTERCEPT = 4.0
    
    # Risk thresholds
    HIGH_THRESHOLD = 0.7
    MEDIUM_THRESHOLD = 0.4
    
    def __init__(self):
        """Initialize classifier."""
        pass
    
    async def predict(
        self,
        student_id: str,
        features: Optional[dict] = None
    ) -> dict:
        """
        Predict dropout risk for a student.
        
        Args:
            student_id: Student identifier
            features: Optional pre-computed features
            
        Returns:
            Risk assessment with level, probability, and recommendations
        """
        # Fetch features if not provided
        if features is None:
            features = await self._compute_features(student_id)
        
        # Normalize features
        normalized = self._normalize_features(features)
        
        # Calculate log-odds using logistic regression
        log_odds = self.INTERCEPT
        for feature, weight in self.FEATURE_WEIGHTS.items():
            log_odds += weight * normalized.get(feature, 0)
        
        # Convert to probability
        probability = 1 / (1 + np.exp(-log_odds))
        probability = float(probability)
        
        # Determine risk level
        if probability >= self.HIGH_THRESHOLD:
            if probability >= 0.85:
                risk_level = "critical"
            else:
                risk_level = "high"
        elif probability >= self.MEDIUM_THRESHOLD:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Calculate contributing factors
        contributing_factors = self._get_contributing_factors(features, normalized)
        
        # Generate recommendations
        recommended_actions = self._generate_recommendations(
            risk_level, 
            contributing_factors
        )
        
        return {
            "risk_level": risk_level,
            "probability": round(probability, 2),
            "contributing_factors": contributing_factors,
            "recommended_actions": recommended_actions
        }
    
    def _normalize_features(self, features: dict) -> dict:
        """Normalize features to 0-1 scale."""
        normalized = {}
        
        # Attendance rate (0-100 -> 0-1)
        normalized["attendance_rate"] = features.get("attendance_rate", 80) / 100
        
        # Grade average (0-10 -> 0-1)
        normalized["grade_average"] = features.get("grade_average", 7) / 10
        
        # Attendance trend (-1 to 1, already normalized)
        trend = features.get("attendance_trend", 0)
        normalized["attendance_trend"] = max(-1, min(1, trend))
        
        # Days since absence (0-30+ -> 0-1)
        days = features.get("days_since_absence", 5)
        normalized["days_since_absence"] = min(1, days / 30)
        
        # Pattern flags (0-5 -> 0-1)
        flags = features.get("pattern_flags", 0)
        normalized["pattern_flags"] = min(1, flags / 5)
        
        return normalized
    
    def _get_contributing_factors(
        self, 
        features: dict, 
        normalized: dict
    ) -> List[dict]:
        """Identify factors contributing to risk."""
        factors = []
        
        # Check each feature
        if normalized["attendance_rate"] < 0.75:
            factors.append({
                "factor": "Attendance rate",
                "value": f"{features.get('attendance_rate', 0):.0f}%",
                "impact": "high"
            })
        
        if normalized["grade_average"] < 0.6:
            factors.append({
                "factor": "Grade average",
                "value": f"{features.get('grade_average', 0):.1f}/10",
                "impact": "high"
            })
        
        if normalized["attendance_trend"] < 0:
            factors.append({
                "factor": "Attendance trend",
                "value": "declining",
                "impact": "medium"
            })
        
        if normalized["pattern_flags"] > 0.4:
            factors.append({
                "factor": "Absence patterns",
                "value": f"{features.get('pattern_flags', 0)} flags",
                "impact": "medium"
            })
        
        return factors
    
    def _generate_recommendations(
        self, 
        risk_level: str,
        factors: List[dict]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if risk_level in ["critical", "high"]:
            recommendations.append("Schedule immediate meeting with counselor")
            recommendations.append("Assign peer mentor for support")
            recommendations.append("Contact parent/guardian")
        
        if risk_level == "medium":
            recommendations.append("Send personalized check-in message")
            recommendations.append("Recommend tutoring resources")
        
        # Factor-specific recommendations
        for factor in factors:
            if factor["factor"] == "Attendance rate":
                recommendations.append("Review attendance barriers (transportation, health)")
            elif factor["factor"] == "Grade average":
                recommendations.append("Provide subject-specific study materials")
            elif factor["factor"] == "Attendance trend":
                recommendations.append("Monitor closely over next 2 weeks")
        
        if not recommendations:
            recommendations.append("Continue regular monitoring")
            recommendations.append("Encourage participation in study groups")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    async def _compute_features(self, student_id: str) -> dict:
        """Compute features from database for a student."""
        # TODO: Implement actual database queries
        # For demo, return sample data based on student_id
        
        if student_id == "STU-404":
            # High-risk demo student
            return {
                "attendance_rate": 72,
                "grade_average": 6.5,
                "attendance_trend": -0.15,
                "days_since_absence": 3,
                "pattern_flags": 2
            }
        else:
            # Normal student
            return {
                "attendance_rate": 88,
                "grade_average": 7.5,
                "attendance_trend": 0.05,
                "days_since_absence": 12,
                "pattern_flags": 0
            }
