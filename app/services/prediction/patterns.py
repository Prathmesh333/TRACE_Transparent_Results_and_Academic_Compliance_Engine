"""
Opti-Scholar: Pattern Miner Service
Sequential pattern mining for attendance behavior discovery
"""

from datetime import datetime, timedelta
from typing import List, Optional
from collections import Counter


class PatternMiner:
    """Discover attendance patterns using sequential pattern mining."""
    
    # Known pattern templates
    PATTERN_TEMPLATES = [
        ("monday_after_holiday", "Misses class on Monday after long weekend", ["Monday"]),
        ("friday_late", "Leaves early or misses Friday classes", ["Friday"]),
        ("start_of_week", "Regular absences at start of week", ["Monday", "Tuesday"]),
        ("end_of_week", "Regular absences at end of week", ["Thursday", "Friday"]),
        ("consecutive", "Consecutive day absences", None),
        ("mid_week", "Absences in middle of week", ["Wednesday"]),
    ]
    
    def __init__(self, min_confidence: float = 0.6, min_occurrences: int = 3):
        """
        Initialize miner.
        
        Args:
            min_confidence: Minimum confidence threshold for patterns
            min_occurrences: Minimum occurrences to report a pattern
        """
        self.min_confidence = min_confidence
        self.min_occurrences = min_occurrences
    
    async def mine(
        self,
        student_id: str,
        attendance_records: Optional[List[dict]] = None
    ) -> dict:
        """
        Mine attendance patterns for a student.
        
        Args:
            student_id: Student identifier
            attendance_records: Optional attendance data (fetched if not provided)
            
        Returns:
            Discovered patterns with confidence scores
        """
        # Fetch attendance if not provided
        if attendance_records is None:
            attendance_records = await self._fetch_attendance(student_id)
        
        if len(attendance_records) < 10:
            return {
                "patterns": [],
                "analysis_period": "Insufficient data"
            }
        
        # Extract absences
        absences = [
            r for r in attendance_records 
            if r.get("status") in ["absent", "late"]
        ]
        
        # Analyze patterns
        patterns = []
        
        # Check day-of-week patterns
        day_patterns = self._analyze_day_patterns(absences)
        patterns.extend(day_patterns)
        
        # Check consecutive absence patterns
        consecutive_patterns = self._analyze_consecutive(absences)
        patterns.extend(consecutive_patterns)
        
        # Check holiday-related patterns
        holiday_patterns = self._analyze_holiday_patterns(absences)
        patterns.extend(holiday_patterns)
        
        # Filter by confidence and occurrences
        filtered_patterns = [
            p for p in patterns 
            if p["confidence"] >= self.min_confidence 
            and p["occurrences"] >= self.min_occurrences
        ]
        
        # Sort by confidence
        filtered_patterns.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Determine analysis period
        if attendance_records:
            dates = [r.get("date") for r in attendance_records if r.get("date")]
            if dates:
                start_date = min(dates)
                end_date = max(dates)
                analysis_period = f"{start_date} to {end_date}"
            else:
                analysis_period = "Last 90 days"
        else:
            analysis_period = "Last 90 days"
        
        return {
            "patterns": filtered_patterns,
            "analysis_period": analysis_period
        }
    
    def _analyze_day_patterns(self, absences: List[dict]) -> List[dict]:
        """Analyze which days are most frequently missed."""
        patterns = []
        
        # Count absences by day of week
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_counts = Counter()
        
        for absence in absences:
            date_str = absence.get("date")
            if date_str:
                try:
                    if isinstance(date_str, str):
                        date = datetime.fromisoformat(date_str)
                    else:
                        date = date_str
                    day_name = day_names[date.weekday()]
                    day_counts[day_name] += 1
                except (ValueError, TypeError):
                    continue
        
        total_absences = sum(day_counts.values())
        
        if total_absences > 0:
            for day, count in day_counts.most_common(3):
                frequency = count / total_absences
                
                if frequency > 0.25:  # More than 25% of absences on this day
                    patterns.append({
                        "pattern_type": f"Frequent absences on {day}",
                        "confidence": min(0.95, frequency * 1.5),
                        "occurrences": count,
                        "sample_dates": self._get_sample_dates(absences, day)
                    })
        
        return patterns
    
    def _analyze_consecutive(self, absences: List[dict]) -> List[dict]:
        """Find consecutive absence patterns."""
        patterns = []
        
        # Sort absences by date
        sorted_absences = sorted(
            [a for a in absences if a.get("date")],
            key=lambda x: x["date"]
        )
        
        if len(sorted_absences) < 2:
            return patterns
        
        # Count consecutive sequences
        consecutive_count = 0
        
        for i in range(len(sorted_absences) - 1):
            try:
                date1 = sorted_absences[i]["date"]
                date2 = sorted_absences[i + 1]["date"]
                
                if isinstance(date1, str):
                    date1 = datetime.fromisoformat(date1)
                if isinstance(date2, str):
                    date2 = datetime.fromisoformat(date2)
                
                diff = (date2 - date1).days
                
                if diff == 1:
                    consecutive_count += 1
            except (ValueError, TypeError):
                continue
        
        if consecutive_count >= 3:
            patterns.append({
                "pattern_type": "Tendency for consecutive-day absences",
                "confidence": min(0.9, consecutive_count * 0.15),
                "occurrences": consecutive_count,
                "sample_dates": []
            })
        
        return patterns
    
    def _analyze_holiday_patterns(self, absences: List[dict]) -> List[dict]:
        """Analyze patterns around holidays/weekends."""
        patterns = []
        
        monday_after_weekend = 0
        friday_before_weekend = 0
        
        for absence in absences:
            date_str = absence.get("date")
            if date_str:
                try:
                    if isinstance(date_str, str):
                        date = datetime.fromisoformat(date_str)
                    else:
                        date = date_str
                    
                    if date.weekday() == 0:  # Monday
                        monday_after_weekend += 1
                    elif date.weekday() == 4:  # Friday
                        friday_before_weekend += 1
                except (ValueError, TypeError):
                    continue
        
        if monday_after_weekend >= 3:
            patterns.append({
                "pattern_type": "Misses class on Monday after weekend",
                "confidence": min(0.95, monday_after_weekend * 0.2),
                "occurrences": monday_after_weekend,
                "sample_dates": []
            })
        
        if friday_before_weekend >= 3:
            patterns.append({
                "pattern_type": "Misses class on Friday before weekend",
                "confidence": min(0.90, friday_before_weekend * 0.18),
                "occurrences": friday_before_weekend,
                "sample_dates": []
            })
        
        return patterns
    
    def _get_sample_dates(self, absences: List[dict], day_name: str) -> List[str]:
        """Get sample dates for a specific day pattern."""
        samples = []
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for absence in absences[:10]:
            date_str = absence.get("date")
            if date_str:
                try:
                    if isinstance(date_str, str):
                        date = datetime.fromisoformat(date_str)
                    else:
                        date = date_str
                    
                    if day_names[date.weekday()] == day_name:
                        samples.append(date.strftime("%Y-%m-%d"))
                        
                        if len(samples) >= 3:
                            break
                except (ValueError, TypeError):
                    continue
        
        return samples
    
    async def _fetch_attendance(self, student_id: str) -> List[dict]:
        """Fetch attendance records from database."""
        # TODO: Implement actual database query
        # For demo, return sample data
        
        base_date = datetime.now()
        records = []
        
        # Generate sample attendance with patterns
        for i in range(90):
            date = base_date - timedelta(days=i)
            
            # Skip weekends
            if date.weekday() >= 5:
                continue
            
            # Create pattern: frequently absent on Mondays
            if date.weekday() == 0 and i % 3 == 0:
                status = "absent"
            elif date.weekday() == 4 and i % 5 == 0:
                status = "late"
            else:
                status = "present"
            
            records.append({
                "date": date.isoformat(),
                "status": status
            })
        
        return records
