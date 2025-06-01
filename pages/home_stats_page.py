# pages/home_stats_page.py
import time
from playwright.sync_api import Page
from .home_selectors import STAT_BLOCK, STAT_BLOCK_TITLE, STAT_BLOCK_NUMBER

class HomeStatsPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_homepage(self) -> None:
        """Navigate to the SDS homepage."""
        self.page.goto(
            "https://s-d-s.co.uk/",
            wait_until="domcontentloaded",
            timeout=30000
        )

    def _get_stable_number_by_title(
        self,
        title_text: str,
        timeout: float = 10.0,
        poll_interval: float = 0.5
    ) -> str:
        """
        Wait until the “.pwr-stat__number” for a given title
        (e.g. “CUSTOMERS” or “USERS”) stops changing. Return the final string.
        """
        start_time = time.time()
        prev_number = None
        stable_count = 0

        while time.time() - start_time < timeout:
            elements = self.page.locator(STAT_BLOCK)
            count = elements.count()
            for i in range(count):
                title = elements.nth(i).locator(STAT_BLOCK_TITLE).text_content()
                if title and title.strip().upper() == title_text.upper():
                    number = elements.nth(i).locator(STAT_BLOCK_NUMBER).text_content().strip()
                    if number == prev_number:
                        stable_count += 1
                        if stable_count >= 2:
                            return number
                    else:
                        prev_number = number
                        stable_count = 0
                    break
            time.sleep(poll_interval)

        raise TimeoutError(f"{title_text} number did not stabilize in time.")

    def get_customers_text(self) -> str:
        return self._get_stable_number_by_title("CUSTOMERS")

    def get_users_text(self) -> str:
        return self._get_stable_number_by_title("USERS")
