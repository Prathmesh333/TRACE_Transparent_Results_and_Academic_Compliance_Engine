"""
Opti-Scholar: Resource Recommender Service
RAG-powered study resource recommendations
"""

from typing import List, Optional

from app.core.config import settings


class ResourceRecommender:
    """Recommend learning resources using RAG (Retrieval Augmented Generation)."""
    
    # Sample resource database (in production, use FAISS/ChromaDB)
    RESOURCES = [
        {
            "id": "1",
            "title": "Thermodynamics Crash Course",
            "type": "video",
            "url": "https://youtube.com/watch?v=thermodynamics",
            "difficulty": "intermediate",
            "topics": ["thermodynamics", "heat transfer", "energy"],
            "duration_minutes": 15
        },
        {
            "id": "2",
            "title": "Newton's Laws Explained",
            "type": "video",
            "url": "https://youtube.com/watch?v=newtons-laws",
            "difficulty": "beginner",
            "topics": ["newton", "force", "motion", "physics"],
            "duration_minutes": 12
        },
        {
            "id": "3",
            "title": "Physics Practice Quiz",
            "type": "quiz",
            "url": "https://resources.opti-scholar.com/quiz/physics-101",
            "difficulty": "beginner",
            "topics": ["physics", "mechanics", "force"],
            "question_count": 20
        },
        {
            "id": "4",
            "title": "Heat Transfer Calculations Guide",
            "type": "pdf",
            "url": "https://resources.opti-scholar.com/pdf/heat-transfer",
            "difficulty": "advanced",
            "topics": ["heat transfer", "calculations", "thermodynamics"]
        },
        {
            "id": "5",
            "title": "Algebra Fundamentals",
            "type": "video",
            "url": "https://youtube.com/watch?v=algebra-basics",
            "difficulty": "beginner",
            "topics": ["algebra", "math", "equations"],
            "duration_minutes": 20
        },
        {
            "id": "6",
            "title": "Calculus Practice Problems",
            "type": "quiz",
            "url": "https://resources.opti-scholar.com/quiz/calculus",
            "difficulty": "intermediate",
            "topics": ["calculus", "derivatives", "integrals", "math"],
            "question_count": 15
        }
    ]
    
    def __init__(self):
        """Initialize recommender."""
        # TODO: Initialize FAISS vector store in production
        pass
    
    async def recommend(
        self,
        student_id: str,
        failed_topics: List[str],
        preferred_formats: Optional[List[str]] = None
    ) -> dict:
        """
        Recommend resources based on failed topics.
        
        Args:
            student_id: Student identifier
            failed_topics: List of topics the student needs help with
            preferred_formats: Optional list of preferred resource types
            
        Returns:
            Recommended resources with relevance scores
        """
        recommendations = []
        
        # Normalize topics for matching
        normalized_topics = [t.lower().strip() for t in failed_topics]
        
        for resource in self.RESOURCES:
            # Calculate relevance score
            relevance = self._calculate_relevance(
                resource["topics"],
                normalized_topics
            )
            
            if relevance > 0:
                # Apply format filter
                if preferred_formats and resource["type"] not in preferred_formats:
                    relevance *= 0.5  # Reduce but don't exclude
                
                rec = {
                    "title": resource["title"],
                    "type": resource["type"],
                    "url": resource["url"],
                    "difficulty": resource["difficulty"],
                    "relevance_score": round(relevance, 2)
                }
                
                # Add type-specific fields
                if "duration_minutes" in resource:
                    rec["duration_minutes"] = resource["duration_minutes"]
                if "question_count" in resource:
                    rec["question_count"] = resource["question_count"]
                
                recommendations.append(rec)
        
        # Sort by relevance
        recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Return top 5
        return {
            "recommendations": recommendations[:5]
        }
    
    def _calculate_relevance(
        self,
        resource_topics: List[str],
        query_topics: List[str]
    ) -> float:
        """Calculate relevance score between resource and query topics."""
        if not resource_topics or not query_topics:
            return 0.0
        
        # Simple set intersection for demo
        resource_set = set(t.lower() for t in resource_topics)
        query_set = set(query_topics)
        
        # Count matching topics
        matches = len(resource_set.intersection(query_set))
        
        # Also check partial matches
        partial_matches = 0
        for q in query_topics:
            for r in resource_set:
                if q in r or r in q:
                    partial_matches += 0.5
        
        total_matches = matches + partial_matches
        
        # Normalize by query size
        if len(query_topics) > 0:
            relevance = min(1.0, total_matches / len(query_topics))
        else:
            relevance = 0.0
        
        return relevance
