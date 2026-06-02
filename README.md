ENV=dev pytest playwright/tests/PracticeTestAutomationTests.py --alluredir=playwright/allure-results -v && allure generate playwright/allure-results --clean -o playwright/allure-report && allure open allure-report

python3 -m http.server 8080



# Step 1 - already running, wait for it to finish
ENV=dev pytest tests/PracticeTestAutomationTests.py --alluredir=allure-results -v

# Step 2 - only after Step 1 exits 0
allure generate allure-results --clean -o allure-report

# Step 3 - opens browser at localhost (keep terminal open)
allure open allure-report



ENV=dev pytest tests/PracticeTestAutomationTests.py --alluredir=allure-results -v && allure generate allure-results --clean -o allure-report && allure open allure-report