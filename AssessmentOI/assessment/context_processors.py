import os

def export_vars(request):
    data = {}
    data['ENVIRONMENT'] = os.environ['ENVIRONMENT']
    return data