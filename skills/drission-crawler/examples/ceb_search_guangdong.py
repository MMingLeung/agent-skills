#!/usr/bin/env python3
"""CEB 首页搜索「广东」并等待新 TAB。默认不保存/提交。"""

from __future__ import annotations

import json
import time
from pathlib import Path

from DrissionPage import Chromium, ChromiumOptions

# 任务级参数（timeout / poll / retry / max_depth / writeback）
TIMEOUT = 30.0
POLL = 0.5
RETRY = 3
MAX_DEPTH = 1
WRITEBACK = "log"

HOME_URL = "https://www.cebpubservice.com/"
SEARCH_TEXT = "广东"
INPUT_LOCATOR = "css:#InputValue"
SEARCH_BTN_LOCATOR = "css:div.search_img"


def log(step: str, **kwargs) -> None:
    payload = {"step": step, **kwargs}
    print(json.dumps(payload, ensure_ascii=False))


def wait_ele(tab, locator: str, timeout: float = TIMEOUT, poll: float = POLL):
    deadline = time.time() + timeout
    last_err = None
    while time.time() < deadline:
        try:
            ele = tab.ele(locator, timeout=poll)
            if ele:
                return ele
        except Exception as exc:  # noqa: BLE001
            last_err = exc
        time.sleep(poll)
    raise TimeoutError(f"wait failed: {locator}; last={last_err}")


def wait_new_tab(browser, before_ids: set[int], timeout: float = TIMEOUT, poll: float = POLL):
    deadline = time.time() + timeout
    while time.time() < deadline:
        tabs = browser.get_tabs()
        for t in tabs:
            tid = getattr(t, "tab_id", None) or id(t)
            if tid not in before_ids:
                return t
        # 也兼容 latest_tab 已切到新页但 id 集合尚未刷新的情况
        latest = browser.latest_tab
        lid = getattr(latest, "tab_id", None) or id(latest)
        if lid not in before_ids and getattr(latest, "url", "") and latest.url != HOME_URL.rstrip("/"):
            return latest
        time.sleep(poll)
    raise TimeoutError("new tab did not open within timeout")


def main() -> int:
    evidence_dir = Path(__file__).resolve().parent / "output" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    co = ChromiumOptions()
    co.set_argument("--window-size", "1400,900")
    browser = Chromium(co)
    tab = browser.latest_tab

    try:
        # 1) open home
        log("open_home", url=HOME_URL, timeout=TIMEOUT, poll=POLL, retry=RETRY, max_depth=MAX_DEPTH, writeback=WRITEBACK)
        tab.get(HOME_URL)
        log("scope", url=tab.url, title=tab.title, tab_id=getattr(tab, "tab_id", None))

        # 2) wait + locate input
        for attempt in range(1, RETRY + 1):
            try:
                inp = wait_ele(tab, INPUT_LOCATOR)
                candidates = tab.eles(INPUT_LOCATOR)
                log(
                    "locate_input",
                    attempt=attempt,
                    locator=INPUT_LOCATOR,
                    candidate_count=len(candidates),
                    visible=bool(getattr(inp, "states", None) and inp.states.is_displayed),
                    placeholder=inp.attr("placeholder"),
                    html=(inp.html or "")[:200],
                )
                break
            except Exception as exc:  # noqa: BLE001
                log("locate_input_retry", attempt=attempt, error=str(exc))
                if attempt >= RETRY:
                    raise
                time.sleep(POLL)
        else:
            raise RuntimeError("input not found")

        # 3) input + readback
        inp = tab.ele(INPUT_LOCATOR)
        inp.clear()
        inp.input(SEARCH_TEXT)
        inp = tab.ele(INPUT_LOCATOR)  # 重新定位后回读
        value = inp.value if hasattr(inp, "value") else inp.attr("value")
        log("input_readback", expected=SEARCH_TEXT, actual=value)
        if value != SEARCH_TEXT:
            raise AssertionError(f"input readback failed: {value!r}")

        # 4) locate search button + click
        btn = wait_ele(tab, SEARCH_BTN_LOCATOR)
        btn_candidates = tab.eles(SEARCH_BTN_LOCATOR)
        log(
            "locate_search_btn",
            locator=SEARCH_BTN_LOCATOR,
            candidate_count=len(btn_candidates),
            class_=btn.attr("class"),
            html=(btn.html or "")[:200],
        )

        before_ids = set()
        for t in browser.get_tabs():
            before_ids.add(getattr(t, "tab_id", None) or id(t))
        before_count = len(before_ids)
        home_url_before = tab.url
        log("before_click", tab_count=before_count, home_url=home_url_before)

        btn = tab.ele(SEARCH_BTN_LOCATOR)
        btn.click()

        # 5) postcondition: new tab opened
        new_tab = wait_new_tab(browser, before_ids)
        # settle URL/title on new tab
        deadline = time.time() + TIMEOUT
        while time.time() < deadline:
            if new_tab.url and new_tab.url not in ("about:blank", home_url_before):
                break
            time.sleep(POLL)

        after_count = len(browser.get_tabs())
        log(
            "new_tab_opened",
            before_count=before_count,
            after_count=after_count,
            new_url=new_tab.url,
            new_title=new_tab.title,
            new_tab_id=getattr(new_tab, "tab_id", None),
            save_submit_publish=False,
        )

        # 切到新 TAB 做一次 live 证据（不关闭浏览器）
        browser.activate_tab(new_tab)
        shot = evidence_dir / "ceb_search_guangdong_newtab.png"
        try:
            new_tab.get_screenshot(path=str(shot), full_page=False)
            log("evidence_screenshot", path=str(shot))
        except Exception as exc:  # noqa: BLE001
            log("evidence_screenshot_skip", error=str(exc))

        print("\n=== LIVE RESULT ===")
        print(f"home: {home_url_before}")
        print(f"new_tab url: {new_tab.url}")
        print(f"new_tab title: {new_tab.title}")
        print(f"tab_count: {before_count} -> {after_count}")
        print("browser kept open for inspection")
        return 0
    except Exception as exc:  # noqa: BLE001
        log("failure", error=type(exc).__name__, message=str(exc), url=getattr(tab, "url", None), title=getattr(tab, "title", None))
        try:
            fail_shot = evidence_dir / "ceb_search_guangdong_fail.png"
            tab.get_screenshot(path=str(fail_shot), full_page=False)
            log("failure_screenshot", path=str(fail_shot))
        except Exception:
            pass
        raise


if __name__ == "__main__":
    raise SystemExit(main())
