"""Opti-Scholar Management Services Package"""
from app.services.management.recommender import ResourceRecommender
from app.services.management.router import TicketRouter

__all__ = ["ResourceRecommender", "TicketRouter"]
