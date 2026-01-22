"""
Theme and Color Configuration
"""
import flet as ft


class AppColors:
    """Application color palette"""
    # Primary colors
    PRIMARY = "#4CAF50"  # Green
    PRIMARY_DARK = "#388E3C"
    PRIMARY_LIGHT = "#C8E6C9"
    
    # Secondary colors
    SECONDARY = "#FF9800"  # Orange
    SECONDARY_DARK = "#F57C00"
    SECONDARY_LIGHT = "#FFE0B2"
    
    # Accent
    ACCENT = "#2196F3"  # Blue
    
    # Status colors
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    ERROR = "#F44336"
    INFO = "#2196F3"
    
    # Status specific
    SCHEDULED = "#2196F3"
    COMPLETED = "#4CAF50"
    CANCELLED = "#F44336"
    PENDING = "#FFC107"
    
    # Neutral colors
    BACKGROUND = "#F5F5F5"
    SURFACE = "#FFFFFF"
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    DIVIDER = "#BDBDBD"


class AppSpacing:
    """Spacing constants"""
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48


class AppBorderRadius:
    """Border radius constants"""
    SM = 4
    MD = 8
    LG = 12
    XL = 16
    ROUND = 999


class AppTheme:
    """Application theme configuration"""
    
    @staticmethod
    def get_light_theme() -> ft.Theme:
        """Get light theme"""
        return ft.Theme(
            color_scheme_seed=AppColors.PRIMARY,
            use_material3=True,
        )
    
    @staticmethod
    def get_common_text_style(
        size: int = 14,
        weight: ft.FontWeight = ft.FontWeight.NORMAL,
        color: str = AppColors.TEXT_PRIMARY
    ) -> ft.TextStyle:
        """Get common text style"""
        return ft.TextStyle(
            size=size,
            weight=weight,
            color=color
        )
    
    @staticmethod
    def get_title_style() -> ft.TextStyle:
        """Get title text style"""
        return ft.TextStyle(
            size=24,
            weight=ft.FontWeight.BOLD,
            color=AppColors.TEXT_PRIMARY
        )
    
    @staticmethod
    def get_subtitle_style() -> ft.TextStyle:
        """Get subtitle text style"""
        return ft.TextStyle(
            size=18,
            weight=ft.FontWeight.W_600,
            color=AppColors.TEXT_PRIMARY
        )
    
    @staticmethod
    def get_body_style() -> ft.TextStyle:
        """Get body text style"""
        return ft.TextStyle(
            size=14,
            weight=ft.FontWeight.NORMAL,
            color=AppColors.TEXT_PRIMARY
        )
    
    @staticmethod
    def get_caption_style() -> ft.TextStyle:
        """Get caption text style"""
        return ft.TextStyle(
            size=12,
            weight=ft.FontWeight.NORMAL,
            color=AppColors.TEXT_SECONDARY
        )
