# pages/home_selectors.py

# ——————————————————————————————————————
# Home Stats Page Selectors
# ——————————————————————————————————————

# Container for each stat block (CUSTOMERS, USERS, HOMES BUILT, etc.)
STAT_BLOCK             = ".pwr-stat"

# Within a STAT_BLOCK:
STAT_BLOCK_TITLE       = ".pwr-stat__title"
STAT_BLOCK_NUMBER      = ".pwr-stat__number"


# ——————————————————————————————————————
# Landval Demo Page (Book-a-Demo) Selectors
# ——————————————————————————————————————

# The HubSpot “Book a demo” form (wrapped in <form class="hs-form">…</form>)
DEMO_FORM             = "form.hs-form"

# Individual input fields inside that form:
INPUT_FIRSTNAME       = "input[name='firstname']"
INPUT_LASTNAME        = "input[name='lastname']"
INPUT_PHONE           = "input[name='phone']"
INPUT_EMAIL           = "input[name='email']"
INPUT_COMPANY         = "input[name='company']"

# The “Enquiry Type” checkboxes are rendered as <label>…<input type="checkbox" name="enquiry_type___products" value="Landval">…
# We will click the label that contains the product name, e.g. Landval, ProVal, etc.
CHECKBOX_BY_LABEL_FMT = "label:has-text('{}')"  # e.g. CHECKBOX_BY_LABEL_FMT.format("Landval")

# The “Message” textarea:
TEXTAREA_MESSAGE      = "textarea[name='message']"

# The Submit button inside that form:
BUTTON_SUBMIT         = "input[type='submit']"

# After successful submission, HubSpot replaces the form with a <div class="submitted-message">…</div>
SUCCESS_BANNER        = "div.submitted-message"

# Phone-format error under the phone field:
ERROR_PHONE_FMT       = "label.hs-error-msg:has-text('A valid phone number')"

# Per-field “missing required” error:
ERROR_MISSING_FIELD   = "label.hs-error-msg:has-text('Please complete this required field')"

# Roll-up error at bottom: “Please complete all required fields.”
ERROR_ROLLUP          = "div.hs_error_rollup label:has-text('Please complete all required fields')"
