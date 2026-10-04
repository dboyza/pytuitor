"""Optional authored mixed reviews, one session per syllabus chapter."""

from pytuitor.content.reviews.core import CORE
from pytuitor.content.reviews.depth import DEPTH
from pytuitor.content.reviews.online import ONLINE

REVIEWS = CORE | DEPTH | ONLINE
