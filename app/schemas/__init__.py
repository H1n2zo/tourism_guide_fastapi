from app.schemas.destination import (
    DestinationResponse,
    DestinationListResponse,
    DestinationImageResponse
)
from app.schemas.category import CategoryResponse
from app.schemas.route import RouteResponse
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewStats
)
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackResponse,
    FeedbackStats
)
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse,
    UserWithToken
)

__all__ = [
    # Destinations
    "DestinationResponse",
    "DestinationListResponse",
    "DestinationImageResponse",
    # Categories
    "CategoryResponse",
    # Routes
    "RouteResponse",
    # Reviews
    "ReviewCreate",
    "ReviewResponse",
    "ReviewStats",
    # Feedback
    "FeedbackCreate",
    "FeedbackResponse",
    "FeedbackStats",
    # Auth
    "UserRegister",
    "UserLogin",
    "Token",
    "UserResponse",
    "UserWithToken",
]