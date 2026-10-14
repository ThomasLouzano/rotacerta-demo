"""Local browser regression tests. Install playwright and Chromium to run.
No connection to a GitHub account or any external messaging/vision service.
"""
from __future__ import annotations
import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def run() -> dict:
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}/docs/'
    report = {'source': 'RotaCerta v12', 'platform': 'Chromium / localhost', 'tests': []}
    errors = []
    external = []
    try:
        with sync_playwright() as p:
            exe = os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium')
            browser = p.chromium.launch(executable_path=exe if Path(exe).exists() else None, headless=True, args=['--no-sandbox'])
            context = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True)
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: external.append(request.url) if not request.url.startswith(('http://127.0.0.1', 'data:', 'blob:')) else None)
            page.goto(url, wait_until='networkidle')
            page.wait_for_function('window.RotaCertaPWA?.getStatus().offlineReady === true')
            assert page.locator('#rc-auth-form').count() == 1
            assert page.locator('.rc-auth-market img').evaluate('(img)=>img.complete && img.naturalWidth>0')
            assert page.evaluate('window.RotaCertaDemo.getState().orders.length') == 30
            report['tests'].append('Initial login and complete Amaro logo; 30 fictitious orders')
            for width, height in [(320,700),(360,780),(390,844),(430,932),(768,1024),(1280,800)]:
                page.set_viewport_size({'width':width,'height':height})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (width,height,'horizontal overflow')
                image=page.locator('.rc-auth-market img').bounding_box()
                assert image and image['width']>0 and image['height']>0
            report['tests'].append('Login layout: 320, 360, 390, 430, 768 and 1280px without horizontal overflow')
            page.set_viewport_size({'width':390,'height':844})
            manifest = page.evaluate('fetch("./manifest.webmanifest").then(r=>r.json())')
            assert manifest['display']=='standalone' and manifest['scope']=='./'
            assert any(i['sizes']=='192x192' for i in manifest['icons'])
            assert any(i['sizes']=='512x512' for i in manifest['icons'])
            assert all(page.request.get(url+i['src'].removeprefix('./')).ok for i in manifest['icons'])
            report['tests'].append('Relative manifest, icons, service-worker activation and scoped cache')
            for role,home in [('Atendente','atendimento'),('Expedição','expedicao'),('Motorista','motorista'),('Administrador','dashboard')]:
                page.locator(f'.rc-auth-role[data-role="{role}"]').click()
                page.locator('#rc-auth-form button[type="submit"]').click()
                page.wait_for_function('(p)=>window.RotaCertaDemo.getUI().page===p',arg=home)
                page.evaluate('window.RotaCertaDemo.navigate("login")')
            report['tests'].append('All four login profiles route to their proper workspace')
            # Functional flow: create -> boxes -> dispatch -> manifest -> deliver.
            page.locator('.rc-auth-role[data-role="Atendente"]').click()
            page.locator('#rc-auth-form button[type="submit"]').click()
            page.locator('[data-action="begin-attendance"]').first.click()
            page.locator('#att-phone').fill('(00) 00000-0999')
            page.locator('#att-name').fill('Cliente de teste PWA')
            page.locator('#attendant-form button[type="submit"]').click()
            page.locator('#att-neighborhood').select_option(label='Centro')
            page.locator('#att-street').fill('Rua de teste')
            page.locator('#att-number').fill('10')
            page.locator('#attendant-form input[name="consent"]').check()
            page.locator('#attendant-form button[type="submit"]').click()
            new_id=page.evaluate('window.RotaCertaDemo.getState().orders.at(-1).id')
            page.locator('[data-action="open-volumes"]').click()
            page.locator('#box-add').fill('951, 952')
            page.locator('[data-action="add-box"]').click()
            page.locator('[data-box-field="type"][data-code="CX-952"]').select_option('cold')
            page.locator('#volume-form button[type="submit"]').click()
            assert page.evaluate('(id)=>window.RotaCertaDemo.getState().orders.find(o=>o.id===id).status',new_id)=='ready'
            page.locator('select[data-action="role"]').select_option('Expedição')
            page.locator('[data-action="dispatch-begin"]').click()
            page.locator(f'[data-dispatch-select="{new_id}"]').check()
            page.locator('[data-dispatch-select="111"]').check()
            page.locator('#dispatch-vehicle').select_option('3')
            page.locator('[data-action="dispatch-to-check"]').click()
            assert page.locator('[data-action="dispatch-confirm"]').is_disabled()
            for _ in range(2):
                count=page.locator('[data-dispatch-check]').count()
                for index in range(count):
                    page.locator('[data-dispatch-check]').nth(index).check()
                page.locator('[data-action="dispatch-confirm"]').click()
            manifest_id=page.evaluate('window.RotaCertaDemo.getState().routes.at(-1).id')
            notices=page.evaluate('window.RotaCertaDemo.getState().notifications.length')
            assert notices==4, 'Loading must not message clients'
            page.locator('[data-action="dispatch-show-driver"]').click()
            page.locator(f'[data-action="driver-pick"][data-id="{manifest_id}"]').click()
            page.locator('[data-action="start-route"]').click()
            assert page.evaluate('window.RotaCertaDemo.getState().notifications.length')==notices+1
            page.locator('[data-action="confirm"]').click()
            page.locator('#confirm-physical').check()
            page.locator('#complete-button').click()
            page.wait_for_timeout(1350)
            assert page.evaluate('window.RotaCertaDemo.getState().notifications.length')==notices+2
            report['tests'].append('Created order with two boxes, cold-box linkage, dispatch checks, manifest and one delivery; notices simulated at correct events')
            # App shell must remain usable after its first successful online load.
            page.reload(wait_until='networkidle')
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            await_orders=page.evaluate('window.RotaCertaDemo.getState().orders.length')
            context.set_offline(True)
            page.reload(wait_until='domcontentloaded')
            page.wait_for_selector('#rc-auth-form')
            assert page.evaluate('window.RotaCertaDemo.getState().orders.length')==await_orders==31
            page.locator('.rc-auth-role[data-role="Atendente"]').click()
            page.locator('#rc-auth-form button[type="submit"]').click()
            assert page.evaluate('window.RotaCertaDemo.getUI().page')=='atendimento'
            report['tests'].append('Offline reload preserves 31 local orders and opens attendance without internet')
            context.set_offline(False)
            page.evaluate('window.RotaCertaDemo.navigate("login")')
            page.locator('[data-pwa-about]').click()
            assert page.locator('.modal').is_visible()
            assert 'Não existe sincronização' in page.locator('.modal').inner_text()
            page.locator('.modal [data-action="close"]').last.click()
            report['tests'].append('Installation/about controls explain the local-only demo and simulated integrations')
            report['external_requests'] = external
            report['javascript_errors'] = errors
            assert not errors, errors
            assert not external, external
            report['tests'].append('No uncaught JavaScript errors or external requests during the scenario')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return report

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
