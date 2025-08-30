# test_zillow_parse.py

import sys
# Add the parent directory to the path so we can import the function
sys.path.append('..')
from parse_zillow import parse_zillow_stats

# The HTML snippet you provided
test_html = """
<dl class="styles__StyledOverviewStats-fshdp-8-111-1__sc-1x11gd9-0 kpgmGL">
    <dt><strong>204 days</strong></dt>
    <dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp">on Zillow</dt>
    <span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
    <dt><strong>1,188</strong></dt>
    <dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp"><button type="button" aria-expanded="false" aria-haspopup="false" class="TriggerText-c11n-8-111-1__sc-d96jze-0 hAKmPK TooltipPopper-c11n-8-111-1__sc-1v2hxhd-0 isapNu">views</button></dt>
    <span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
    <dt><strong>61</strong></dt>
    <dt class="styles__StyledOverviewStatsLabel-fshdp-8-111-1__sc-17pxa3r-0 iwFocp"><button type="button" aria-expanded="false" aria-haspopup="false" class="TriggerText-c11n-8-111-1__sc-d96jze-0 hAKmPK TooltipPopper-c11n-8-111-1__sc-1v2hxhd-0 isapNu">saves</button></dt>
    <span class="styles__StyledOverviewStatsDivider-fshdp-8-111-1__sc-1x11gd9-1 iOpxAQ">|</span>
</dl>
"""

def run_test():
    """Runs a test on the parse_zillow_stats function."""
    print("Running test...")
    stats = parse_zillow_stats(test_html)

    # Check if the function returned a dictionary
    if stats is None:
        print("Test failed: Function returned None.")
        return False
    
    # Check if the values match the expected output
    expected_stats = {
        'days_on_zillow': 204,
        'views': 1188,
        'saves': 61
    }

    if stats == expected_stats:
        print("Test passed! 🎉")
        print(f"Parsed stats: {stats}")
        return True
    else:
        print("Test failed: Parsed stats do not match expected stats.")
        print(f"Expected: {expected_stats}")
        print(f"Got: {stats}")
        return False

# Run the test when the file is executed
if __name__ == "__main__":
    run_test()