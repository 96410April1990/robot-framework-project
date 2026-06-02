class PracticeTestTableLocators:
    TEST_TABLE_PAGE = "//a[contains(text(),'Test Table')]"
    TEST_TABLE_PAGE_HEADER = "xpath=//h1[contains(text(),'Test Table')]"
    TEST_TABLE_FILTER_TEXT = "xpath=//h3[contains(text(),'Filters')]"
    TEST_TABLE_ANY_RADIO_BTN = "xpath=//label[contains(text(),'Any')]"
    TEST_TABLE_JAVA_RADIO_BTN = "xpath=//label[contains(text(),'Java')]"
    TEST_TABLE_PYTHON_RADIO_BTN = "xpath=//label[contains(text(),'Python')]"
    TEST_TABLE_BEGINNER_CHECKBOX = "xpath=//label[contains(text(),'Beginner')]"
    TEST_TABLE_INTERMEDIATE_CHECKBOX = "xpath=//label[contains(text(),'Intermediate')]"
    TEST_TABLE_ADVANCED_CHECKBOX = "xpath=//label[contains(text(),'Advanced')]"
    TEST_TABLE_NO_MATCHING_RECORDS_MSG = "xpath=//div[contains(text(),'No matching courses.')]"
    TEST_TABLE_SORT_BY_DROPDOWN_MENU = "#sortBy"
    TEST_TABLE_CHECK = "xpath=//table"
    TEST_TABLE_COLUMN_ID = "xpath=//table//thead//th[normalize-space()='ID']"
    TEST_TABLE_COLUMN_COURSE_NAME = "xpath=//table//thead//th[normalize-space()='Course Name']"
    TEST_TABLE_COLUMN_LANGUAGE = "xpath=//table//thead//th[normalize-space()='Language']"
    TEST_TABLE_COLUMN_LEVEL = "xpath=//table//thead//th[normalize-space()='Level']"
    TEST_TABLE_COLUMN_ENROLLMENTS = "xpath=//table//thead//th[normalize-space()='Enrollments']"
    TEST_TABLE_COLUMN_LINK = "xpath=//table//thead//th[normalize-space()='Link']"
    TEST_TABLE_FIRST_ROW = "xpath=//table//tbody//tr[1]"

    # Table structure
    TEST_TABLE                   = "xpath=//table"
    TEST_TABLE_COLUMN_HEADERS    = "xpath=//table//thead//th"
    TEST_TABLE_ROWS              = "xpath=//table//tbody//tr"
    TEST_TABLE_ALL_CELLS         = "xpath=//table//tbody//td"

    # Specific column header by name — replace 'Name' at call time using .filter()
    TEST_TABLE_HEADER_BY_NAME    = "xpath=//table//thead//th[normalize-space()='{name}']"

    # Specific row by 1-based index  (use .nth(index-1) in code — see page methods)
    TEST_TABLE_ROW_CELLS         = "xpath=//table//tbody//tr[{row}]/td"
