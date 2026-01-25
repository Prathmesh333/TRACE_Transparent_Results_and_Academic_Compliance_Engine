"""
Opti-Scholar: Ticket Router Service
Sentiment-driven support ticket routing
"""

from typing import Optional

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False


class TicketRouter:
    """Route support tickets using sentiment analysis and topic extraction."""
    
    # Topic keywords for classification
    TOPIC_KEYWORDS = {
        "grade_dispute": ["grade", "unfair", "wrong", "incorrect", "appeal", "regrade"],
        "technical": ["error", "bug", "not working", "crash", "login", "password"],
        "academic": ["syllabus", "schedule", "class", "assignment", "homework"],
        "personal": ["stress", "anxiety", "health", "family", "emergency"],
        "administrative": ["fees", "registration", "enrollment", "documents"]
    }
    
    # Queue routing rules
    ROUTING_RULES = {
        ("negative", "grade_dispute"): "teacher",
        ("negative", "personal"): "counselor",
        ("negative", "technical"): "technical",
        ("negative", "academic"): "teacher",
        ("negative", "administrative"): "admin",
        ("neutral", "grade_dispute"): "teacher",
        ("neutral", "academic"): "teacher",
        ("neutral", "administrative"): "admin",
        ("positive", None): "teacher",
    }
    
    # Urgency modifiers based on keywords
    URGENCY_KEYWORDS = {
        "critical": ["urgent", "emergency", "immediately", "asap", "critical"],
        "high": ["important", "soon", "help", "please", "need"],
        "medium": ["question", "wondering", "curious"],
    }
    
    def __init__(self):
        """Initialize router with sentiment analyzer."""
        if VADER_AVAILABLE:
            try:
                self.analyzer = SentimentIntensityAnalyzer()
            except Exception:
                self.analyzer = None
        else:
            self.analyzer = None
    
    async def route(
        self,
        student_id: str,
        subject: str,
        message: str
    ) -> dict:
        """
        Analyze and route a support ticket.
        
        Args:
            student_id: Student identifier
            subject: Ticket subject line
            message: Ticket message content
            
        Returns:
            Routing decision with sentiment, urgency, and queue
        """
        full_text = f"{subject} {message}".lower()
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(full_text)
        
        # Extract topic
        topic = self._extract_topic(full_text)
        
        # Determine urgency
        urgency = self._determine_urgency(full_text, sentiment)
        
        # Route to queue
        queue = self._determine_queue(sentiment, topic, urgency)
        
        # Estimate response time
        response_time = self._estimate_response_time(urgency)
        
        return {
            "sentiment": sentiment,
            "urgency": urgency,
            "queue": queue,
            "topic": topic,
            "estimated_response_time": response_time,
            "auto_response_sent": True
        }
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text using VADER."""
        if self.analyzer:
            scores = self.analyzer.polarity_scores(text)
            compound = scores["compound"]
            
            if compound >= 0.05:
                return "positive"
            elif compound <= -0.05:
                return "negative"
            else:
                return "neutral"
        else:
            # Fallback: simple keyword-based sentiment
            negative_words = ["unfair", "wrong", "angry", "frustrated", "upset", "bad", "terrible"]
            positive_words = ["thank", "great", "appreciate", "good", "excellent", "happy"]
            
            neg_count = sum(1 for w in negative_words if w in text)
            pos_count = sum(1 for w in positive_words if w in text)
            
            if neg_count > pos_count:
                return "negative"
            elif pos_count > neg_count:
                return "positive"
            else:
                return "neutral"
    
    def _extract_topic(self, text: str) -> Optional[str]:
        """Extract primary topic from ticket text."""
        topic_scores = {}
        
        for topic, keywords in self.TOPIC_KEYWORDS.items():
            score = sum(1 for k in keywords if k in text)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        return None
    
    def _determine_urgency(self, text: str, sentiment: str) -> str:
        """Determine urgency level."""
        # Check for urgency keywords
        for level, keywords in self.URGENCY_KEYWORDS.items():
            if any(k in text for k in keywords):
                return level
        
        # Default based on sentiment
        if sentiment == "negative":
            return "medium"
        return "low"
    
    def _determine_queue(
        self,
        sentiment: str,
        topic: Optional[str],
        urgency: str
    ) -> str:
        """Determine which queue to route to."""
        # Check routing rules
        key = (sentiment, topic)
        if key in self.ROUTING_RULES:
            return self.ROUTING_RULES[key]
        
        # Check sentiment-only rules
        for (s, t), queue in self.ROUTING_RULES.items():
            if s == sentiment and t is None:
                return queue
        
        # Default routing
        if urgency in ["critical", "high"]:
            return "admin"
        return "teacher"
    
    def _estimate_response_time(self, urgency: str) -> str:
        """Estimate response time based on urgency."""
        estimates = {
            "critical": "1 hour",
            "high": "4 hours",
            "medium": "24 hours",
            "low": "48 hours"
        }
        return estimates.get(urgency, "24 hours")
