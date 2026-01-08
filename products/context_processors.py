from .models import SiteBanner

def active_banner(request):
    """
    Повертає останній активний банер для відображення на всіх сторінках.
    """
    banner = SiteBanner.objects.filter(is_active=True).order_by('-created_at').first()
    return {'site_banner': banner}
