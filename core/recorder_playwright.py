#!/usr/bin/env python3
"""
Playwright-based recorder for cloning dynamic login pages.
Supports headless/headful, MITM proxy interception, and cookie capture.
"""

import asyncio
import json
import os
import hashlib
import base64
from pathlib import Path
from datetime import datetime
import sqlite3
from typing import Dict, List, Optional

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
except ImportError:
    # Playwright may be installed via pipx in an isolated venv
    import sys
    import glob
    _pipx_venv = os.path.expanduser("~/.local/share/pipx/venvs/playwright")
    _candidates = glob.glob(os.path.join(_pipx_venv, "lib", "python*", "site-packages"))
    for _path in _candidates:
        if _path not in sys.path:
            sys.path.insert(0, _path)
    try:
        from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    except ImportError:
        print("[-] Playwright not installed. Run: pip install playwright && playwright install")
        exit(1)

class PlaywrightRecorder:
    """Record and replay dynamic login flows with Playwright"""
    
    def __init__(self, database_path="./database.db", headless=True, stealth=True):
        self.db_path = database_path
        self.headless = headless
        self.stealth = stealth
        self.browser = None
        self.context = None
        self.page = None
        self.session_id = None
        self.intercepted_requests = []
        self.intercepted_cookies = []
        self.screenshots = []
        self.form_fields = []
        self.csrf_tokens = {}
        self.auth_endpoints = set()
        self.device_emulation = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'viewport': {'width': 1280, 'height': 720},
            'device_scale_factor': 1
        }
    
    async def init_browser(self, use_proxy=False, proxy_url=None):
        """Initialize Playwright browser with optional proxy"""
        self.playwright = await async_playwright().start()
        
        launch_args = {
            'headless': self.headless,
            'args': []
        }
        
        # Add stealth options
        if self.stealth and self.headless:
            launch_args['args'].extend([
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage'
            ])
        
        # Add proxy if specified
        context_args = {}
        if use_proxy and proxy_url:
            context_args['proxy'] = {'server': proxy_url}
        
        self.browser = await self.playwright.chromium.launch(**launch_args)
        self.context = await self.browser.new_context(
            user_agent=self.device_emulation['user_agent'],
            viewport=self.device_emulation['viewport'],
            **context_args
        )
        
        # Setup route handlers for network interception
        await self.context.route('**/*', self._handle_route)
        
        self.page = await self.context.new_page()
        
        # Setup cookie logger
        await self.page.add_init_script("""
            window.socialfish_captured_cookies = [];
            const originalCookie = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
            Object.defineProperty(document, 'cookie', {
                get: originalCookie.get,
                set: function(value) {
                    window.socialfish_captured_cookies.push({
                        timestamp: new Date().toISOString(),
                        cookie_set: value
                    });
                    return originalCookie.set.call(document, value);
                }
            });
        """)
        
        print("[+] Playwright browser initialized")
    
    async def _handle_route(self, route):
        """Intercept and log network requests"""
        request = route.request
        
        # Log request
        req_data = {
            'method': request.method,
            'url': request.url,
            'headers': dict(request.all_headers()),
            'post_data': request.post_data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Continue request
        response = await route.continue_()
        
        # Log response
        res_data = {
            'status': response.status,
            'headers': dict(response.all_headers()),
            'timestamp': datetime.now().isoformat()
        }
        
        # Mark auth-like endpoints
        if request.method == 'POST' and any(keyword in request.url.lower() for keyword in ['login', 'auth', 'signin', 'password']):
            self.auth_endpoints.add(request.url)
            res_data['is_auth_endpoint'] = True
        
        self.intercepted_requests.append({
            'request': req_data,
            'response': res_data
        })
    
    async def record_flow(self, target_url: str, wait_for_selector: str = None, timeout: int = 300):
        """
        Record user interaction with login flow
        
        Args:
            target_url: Initial URL to navigate to
            wait_for_selector: CSS selector to wait for before ending recording (e.g., redirect confirmation)
            timeout: Recording timeout in seconds
        """
        print(f"[*] Starting recording session for {target_url}")
        
        # Generate session ID
        self.session_id = hashlib.sha256(f"{target_url}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        try:
            # Navigate to target
            await self.page.goto(target_url, wait_until='networkidle')
            print(f"[+] Navigated to {target_url}")
            
            # Take initial screenshot
            screenshot_path = await self._save_screenshot('initial')
            self.screenshots.append(screenshot_path)
            
            # Detect forms
            await self._detect_forms()
            
            # Wait for user interaction or timeout
            start_time = datetime.now()
            while (datetime.now() - start_time).total_seconds() < timeout:
                
                # Take periodic screenshots
                if (datetime.now() - start_time).total_seconds() % 10 == 0:
                    screenshot_path = await self._save_screenshot(f'step_{int((datetime.now() - start_time).total_seconds())}')
                    self.screenshots.append(screenshot_path)
                
                # Check for selector if provided
                if wait_for_selector:
                    try:
                        await self.page.wait_for_selector(wait_for_selector, timeout=1000)
                        print(f"[+] Detected completion selector: {wait_for_selector}")
                        break
                    except:
                        pass
                
                # Check if page changed
                await asyncio.sleep(1)
            
            # Capture final state
            await self._capture_final_state()
            print(f"[+] Recording completed. Session ID: {self.session_id}")
            
            return self.session_id
        
        except Exception as e:
            print(f"[-] Recording error: {e}")
            return None
    
    async def _detect_forms(self):
        """Auto-detect form fields and CSRF tokens"""
        forms = await self.page.query_selector_all('form')
        
        for i, form in enumerate(forms):
            # Get form attributes
            form_attrs = await form.evaluate("""elem => ({
                id: elem.id,
                name: elem.name,
                action: elem.action,
                method: elem.method
            })""")
            
            # Get all input fields
            inputs = await form.query_selector_all('input')
            fields = []
            
            for input_elem in inputs:
                field_data = await input_elem.evaluate("""elem => ({
                    type: elem.type,
                    name: elem.name,
                    id: elem.id,
                    class: elem.className,
                    value: elem.value,
                    placeholder: elem.placeholder
                })""")
                fields.append(field_data)
                
                # Detect CSRF tokens
                if any(keyword in field_data.get('name', '').lower() for keyword in ['csrf', 'token', 'nonce', '_token']):
                    self.csrf_tokens[field_data['name']] = field_data.get('id') or field_data.get('name')
            
            self.form_fields.append({
                'form_index': i,
                'form_attrs': form_attrs,
                'fields': fields
            })
        
        print(f"[+] Detected {len(self.form_fields)} form(s)")
        if self.csrf_tokens:
            print(f"[+] Detected CSRF tokens: {list(self.csrf_tokens.keys())}")
    
    async def _capture_final_state(self):
        """Capture cookies, network logs, and final screenshot"""
        
        # Get all cookies from context
        cookies = await self.context.cookies()
        for cookie in cookies:
            self.intercepted_cookies.append({
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': cookie.get('domain'),
                'path': cookie.get('path'),
                'secure': cookie.get('secure'),
                'httpOnly': cookie.get('httpOnly'),
                'sameSite': cookie.get('sameSite'),
                'expires': cookie.get('expires')
            })
        
        # Get cookies set via JavaScript
        js_cookies = await self.page.evaluate("window.socialfish_captured_cookies || []")
        self.intercepted_cookies.extend(js_cookies)
        
        print(f"[+] Captured {len(self.intercepted_cookies)} cookie(s)")
        print(f"[+] Captured {len(self.intercepted_requests)} network request(s)")
    
    async def _save_screenshot(self, label: str) -> str:
        """Save screenshot with label"""
        screenshots_dir = Path(f"./templates/screenshots/{self.session_id}")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot_path = screenshots_dir / f"{label}_{datetime.now().strftime('%H%M%S')}.png"
        await self.page.screenshot(path=str(screenshot_path))
        
        return str(screenshot_path)
    
    def save_template(self, template_name: str, description: str = "", tags: str = ""):
        """Save recording as a reusable template"""
        
        template_data = {
            'name': template_name,
            'description': description,
            'tags': tags.split(',') if tags else [],
            'base_url': self.page.url,
            'forms': self.form_fields,
            'csrf_tokens': self.csrf_tokens,
            'auth_endpoints': list(self.auth_endpoints),
            'cookies': self.intercepted_cookies,
            'created_at': datetime.now().isoformat()
        }
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO templates(name, base_url, description, tags, form_selectors, csrf_token_selectors, auth_endpoints, captured_fields)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            template_name,
            self.page.url,
            description,
            ','.join(tags.split(',')),
            json.dumps(self.form_fields),
            json.dumps(self.csrf_tokens),
            json.dumps(list(self.auth_endpoints)),
            json.dumps([f.get('name') for form in self.form_fields for f in form.get('fields', [])])
        ))
        conn.commit()
        template_id = cur.lastrowid
        conn.close()
        
        # Save template JSON file
        templates_dir = Path("./templates/json")
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        with open(templates_dir / f"{template_id}_{template_name}.json", 'w') as f:
            json.dump(template_data, f, indent=2)
        
        print(f"[+] Template saved: {template_name} (ID: {template_id})")
        return template_id
    
    async def replay_template(self, template_data: Dict, submit_data: Dict = None, headless=True):
        """Replay a saved template with new credentials"""
        
        print(f"[*] Replaying template: {template_data.get('name')}")
        
        # Re-init browser if needed
        if not self.browser:
            await self.init_browser()
        
        self.form_fields = template_data.get('forms', [])
        self.csrf_tokens = template_data.get('csrf_tokens', {})
        
        try:
            # Navigate to base URL
            base_url = template_data.get('base_url')
            await self.page.goto(base_url, wait_until='networkidle')
            
            # Fill forms if submit_data provided
            if submit_data and self.form_fields:
                for form_data in self.form_fields:
                    for field in form_data.get('fields', []):
                        field_name = field.get('name')
                        if field_name in submit_data:
                            selector = f"input[name='{field_name}']"
                            await self.page.fill(selector, submit_data[field_name])
                            print(f"[+] Filled field: {field_name}")
                    
                    # Submit form
                    submit_button = await form_data.get('form_attrs', {}).get('action')
                    forms = await self.page.query_selector_all('form')
                    if forms:
                        await forms[0].evaluate("form => form.submit()")
                        print("[+] Form submitted")
                        await asyncio.sleep(2)
            
            # Capture final state
            await self._capture_final_state()
            
            return {
                'session_id': self.session_id,
                'cookies': self.intercepted_cookies,
                'requests': self.intercepted_requests,
                'screenshots': self.screenshots
            }
        
        except Exception as e:
            print(f"[-] Replay error: {e}")
            return None
    
    async def close(self):
        """Close browser and cleanup"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        print("[+] Browser closed")

# Async wrapper for sync calling
def record_login_flow(target_url: str, headless=True, stealth=True):
    """Synchronous wrapper for recording"""
    async def _record():
        recorder = PlaywrightRecorder(headless=headless, stealth=stealth)
        await recorder.init_browser()
        session_id = await recorder.record_flow(target_url)
        await recorder.close()
        return session_id
    
    return asyncio.run(_record())

def main():
    """CLI test"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Playwright Recorder')
    subparsers = parser.add_subparsers(dest='command')
    
    record_parser = subparsers.add_parser('record', help='Record login flow')
    record_parser.add_argument('url', help='Target URL')
    record_parser.add_argument('--headless', action='store_true', default=True)
    record_parser.add_argument('--stealth', action='store_true', default=True)
    record_parser.add_argument('--save-template', help='Save as template')
    
    args = parser.parse_args()
    
    if args.command == 'record':
        session_id = record_login_flow(args.url, args.headless, args.stealth)
        print(f"[+] Session: {session_id}")

if __name__ == "__main__":
    main()
