from enum import Enum

sentiments = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
topics = ['PRICING', 'CUSTOMER_SERVICE', 'FEATURES']

class TaskStatus(Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'