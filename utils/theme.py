"""
Theme and Color Configuration
Premium Design System
"""
import flet as ft


class AppColors:
    """Premium Application Color Palette"""
    # Brand Identity (Nature & Professionalism)
    PRIMARY = "#10B981"      # Emerald 500 - Fresh, health-oriented
    PRIMARY_DARK = "#059669" # Emerald 600
    PRIMARY_LIGHT = "#D1FAE5" # Emerald 100
    
    # Secondary Identity (Energy & Warmth)
    SECONDARY = "#F59E0B"    # Amber 500
    SECONDARY_DARK = "#D97706"
    SECONDARY_LIGHT = "#FEF3C7"
    
    # Accent (Trust & Clarity)
    ACCENT = "#0EA5E9"       # Sky 500
    
    # Functional Colors
    SUCCESS = "#10B981"      # Same as Primary
    WARNING = "#F59E0B"
    ERROR = "#EF4444"        # Red 500
    INFO = "#3B82F6"         # Blue 500
    
    # Neutral Scale (Modern Grayscale)
    BACKGROUND = "#F8FAFC"   # Slate 50
    SURFACE = "#FFFFFF"      # White
    SURFACE_VARIANT = "#F1F5F9" # Slate 100
    
    TEXT_PRIMARY = "#0F172A" # Slate 900 (High contrast)
    TEXT_SECONDARY = "#64748B" # Slate 500 (Medium contrast)
    TEXT_ON_PRIMARY = "#FFFFFF"
    
    DIVIDER = "#E2E8F0"      # Slate 200
    BORDER = "#CBD5E1"       # Slate 300
    
    # Status Specific
    SCHEDULED = "#0EA5E9"    # Sky
    COMPLETED = "#10B981"    # Emerald
    CANCELLED = "#EF4444"    # Red
    PENDING = "#F59E0B"      # Amber


class AppSpacing:
    """Spacing constants"""
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48
    SECTION = 64


class AppBorderRadius:
    """Border radius constants"""
    SM = 6
    MD = 12
    LG = 16
    XL = 24
    ROUND = 999


class AppShadows:
    """Shadow presets"""
    sm = ft.BoxShadow(
        blur_radius=2,
        color="#0D000000",  # 0.05 opacity black
        offset=ft.Offset(0, 1),
    )
    md = ft.BoxShadow(
        blur_radius=4,
        color="#1A000000",  # 0.1 opacity black
        offset=ft.Offset(0, 2),
    )
    lg = ft.BoxShadow(
        blur_radius=10,
        color="#1A000000",  # 0.1 opacity black
        offset=ft.Offset(0, 4),
    )


class AppTheme:
    """Application theme configuration"""
    
    @staticmethod
    def get_light_theme() -> ft.Theme:
        """Get light theme"""
        return ft.Theme(
            color_scheme_seed=AppColors.PRIMARY,
            use_material3=True,
            font_family="Roboto",
        )
    
    @staticmethod
    def get_header_style() -> ft.TextStyle:
        return ft.TextStyle(
            size=28,
            weight=ft.FontWeight.BOLD,
            color=AppColors.TEXT_PRIMARY,
            letter_spacing=-0.5
        )
    
    @staticmethod
    def get_title_style() -> ft.TextStyle:
        return ft.TextStyle(
            size=24,
            weight=ft.FontWeight.BOLD,
            color=AppColors.TEXT_PRIMARY,
            letter_spacing=-0.5
        )
    
    @staticmethod
    def get_subtitle_style() -> ft.TextStyle:
        return ft.TextStyle(
            size=16,
            weight=ft.FontWeight.W_500,
            color=AppColors.TEXT_SECONDARY
        )
    
    @staticmethod
    def get_body_style() -> ft.TextStyle:
        return ft.TextStyle(
            size=14,
            weight=ft.FontWeight.NORMAL,
            color=AppColors.TEXT_PRIMARY
        )
    
    @staticmethod
    def get_caption_style() -> ft.TextStyle:
        return ft.TextStyle(
            size=12,
            weight=ft.FontWeight.NORMAL,
            color=AppColors.TEXT_SECONDARY
        )
