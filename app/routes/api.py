"""API routes for external integrations and proxy endpoints."""
import requests
from flask import Blueprint, request, jsonify
from functools import wraps

api_bp = Blueprint('api', __name__, url_prefix='/api')


def handle_json_request(f):
    """Decorator to handle JSON requests with error handling."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('DEBUG API REQUEST: content-type=', request.headers.get('Content-Type'))
        print('DEBUG API REQUEST: data=', request.get_data(as_text=True)[:500])

        if not request.is_json:
            print('DEBUG API REQUEST: not JSON')
            return jsonify({'error': 'Request must be JSON'}), 400
        return f(*args, **kwargs)
    return decorated_function


def extract_status_payload(data):
    """Accept both the old and new payload naming conventions."""
    if not data:
        return None

    id_value = data.get('idNumber') or data.get('idnumber')
    phone_value = data.get('phoneNumber') or data.get('mobile')

    if not id_value or not phone_value:
        return None

    return {
        'idNumber': str(id_value),
        'phoneNumber': str(phone_value)
    }


def parse_upstream_json(response):
    """Reject HTML/empty responses from upstream services instead of crashing."""
    content_type = (response.headers.get('Content-Type') or '').lower()
    if 'json' not in content_type:
        raise ValueError('Upstream service returned a non-JSON HTML response.')

    try:
        return response.json()
    except ValueError as exc:
        raise ValueError('Upstream service returned invalid JSON.') from exc


@api_bp.route('/sassa-status', methods=['POST'])
@api_bp.route('/srd-outcome', methods=['POST'])
@handle_json_request
def sassa_status_proxy():
    """
    Proxy endpoint for SASSA status check with fallback.

    Accepts either:
      {"idNumber": "...", "phoneNumber": "..."}
      or
      {"idnumber": "...", "mobile": "..."}
    """
    try:
        data = request.get_json()
        print('DEBUG API PAYLOAD:', data)
        payload = extract_status_payload(data)

        if not payload:
            print('DEBUG API PAYLOAD MISSING: data=', data)
            return jsonify({'error': 'Missing required fields: idNumber/phoneNumber or idnumber/mobile'}), 400

        print('DEBUG API PAYLOAD EXTRACTED:', payload)

        primary_url = 'https://srd.sassa.gov.za/srdweb/api/web/outcome'
        secondary_url = 'https://status.grantza.org.za/check-status'

        for url in [primary_url, secondary_url]:
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=10,
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 200:
                    try: 
                        return jsonify(parse_upstream_json(response)), 200
                    except ValueError:
                        continue
            except (requests.RequestException, requests.Timeout):
                continue

        return jsonify({
            'error': 'SASSA status service responded with an unexpected format or is temporarily unavailable.'
        }), 502

    except Exception as e:
        return jsonify({'error': str(e)}), 500
