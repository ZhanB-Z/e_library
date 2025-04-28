from flet import colors

# Color scheme - Dark Theme
class AppColors:
    PRIMARY = "#555555"        # Medium gray for primary elements
    SECONDARY = "#888888"      # Lighter gray for secondary elements
    ACCENT = "#9b59b6"         # Purple accent for special elements
    BACKGROUND = "#212121"     # Dark background
    CARD_BACKGROUND = "#2c2c2c"  # Slightly lighter for cards
    TEXT_PRIMARY = "#ffffff"   # White text
    TEXT_SECONDARY = "#cccccc" # Light gray text
    ERROR = "#e74c3c"          # Red for errors
    WARNING = "#f39c12"        # Orange for warnings
    SUCCESS = "#27ae60"        # Green for success

# Typography
class AppTypography:
    HEADER_SIZE = 20           # Header font size
    SUBHEADER_SIZE = 20        # Subheader font size
    TITLE_SIZE = 20            # Title font size
    SUBTITLE_SIZE = 18         # Subtitle font size
    BODY_SIZE = 16             # Body font size
    CAPTION_SIZE = 14          # Caption font size
    BUTTON_SIZE = 16           # Button text size
    
    WEIGHT_LIGHT = "w300"
    WEIGHT_REGULAR = "w400"
    WEIGHT_MEDIUM = "w500"
    WEIGHT_BOLD = "w700"

# Spacing
class AppSpacing:
    XS = 4
    SMALL = 8
    MEDIUM = 16
    LARGE = 24
    XL = 32
    XXL = 48

# Input fields
class AppInputs:
    FIELD_WIDTH = 300          # Width of input fields

# Progress indicators
class AppProgress:
    RING_WIDTH = 20            # Progress ring width
    RING_HEIGHT = 20           # Progress ring height
    RING_STROKE_WIDTH = 4      # Progress ring stroke width
    BAR_WIDTH = 40             # Progress bar width

# Tab styling
class AppTabs:
    HEIGHT = 100               # Tab element height
    MARGIN_BOTTOM = 100        # Margin between tabs and other elements
    ANIMATION_DURATION = 300   # Tab animation duration