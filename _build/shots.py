from playwright.sync_api import sync_playwright
import sys
routes={"home":"/","about":"/about/","campaign":"/campaign/"}
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw,(w,h) in {"desk":(1366,900),"phone":(390,844)}.items():
        pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=1)
        for k,r in routes.items():
            pg.goto("http://localhost:8765"+r+"?notrack=1"); pg.wait_for_timeout(1500)
            pg.screenshot(path=f"/home/claude/shots/{k}-{vw}.png",full_page=True)
    b.close()
