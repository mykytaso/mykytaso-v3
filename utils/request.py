def get_client_ip(request):
    """Extract client IP address from request headers."""
    ipaddress = (
        request.META.get("HTTP_X_REAL_IP")
        or request.META.get("HTTP_X_FORWARDED_FOR")
        or request.META.get("REMOTE_ADDR")
        or ""
    )

    if "," in ipaddress:  # multiple ips in the header
        ipaddress = ipaddress.split(",", 1)[0]
    return ipaddress
