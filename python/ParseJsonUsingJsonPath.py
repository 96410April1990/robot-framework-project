from jsonpath_ng.ext import parse

data = {
    "company": {
        "name": "Acme Corp",
        "departments": [
            {
                "name": "Engineering",
                "employees": [
                    {
                        "name": "Alice",
                        "role": "Developer",
                        "salary": 90000
                    },
                    {
                        "name": "Bob",
                        "role": "QA",
                        "salary": 75000
                    },
                    {
                        "name": "Prem",
                        "role": "DevOps",
                        "salary": 75010
                    }
                ]
            },
            {
                "name": "Marketing",
                "employees": [
                    {
                        "name": "Carol",
                        "role": "Designer",
                        "salary": 80000
                    },
                    {
                        "name": "Dave",
                        "role": "Manager",
                        "salary": 95000
                    }
                ]
            }
        ]
    }
}

expr = parse("$..name")
all_names = [match.value for match in expr.find(data)]
print("All names in the given json data: ", all_names)

company_name_object = parse("$.company.name").find(data)[0].value
print(company_name_object)

salary = parse("$..salary")
all_salary = [match.value for match in salary.find(data)]
print("All salary in the given json data:", all_salary)

specific_salary = parse("$..employees[?(@.salary >= 75000)]").find(data)
specific_salary_values = [{"name": match.value["name"], "salary": match.value["salary"]} for match in specific_salary]
print("Specific salary:", specific_salary_values)

get_departments = parse("$.company.departments[*].name")
departments = [match.value for match in get_departments.find(data)]
print("Departments:", departments)

get_department_one = parse("$.company.departments[0].name")
department_one = [match.value for match in get_department_one.find(data)]
print("Department one:",department_one)

get_department_two = parse("$.company.departments[1].name")
department_two = [match.value for match in get_department_two.find(data)]
print("Department one:",department_two)

get_department_one_employees = parse("$.company.departments[0].employees[*].name")
department_one_employees = [match.value for match in get_department_one_employees.find(data)]
print("Department one employees:", department_one_employees)

get_department_two_employees = parse("$.company.departments[1].employees[*].name")
department_two_employees = [match.value for match in get_department_two_employees.find(data)]
print("Department two employees:", department_two_employees)

get_department_one_employee_one = parse("$.company.departments[0].employees[0].name")
department_one_employee_one = [match.value for match in get_department_one_employee_one.find(data)]
print("Department one employee one:", department_one_employee_one)

get_department_one_employee_two = parse("$.company.departments[0].employees[1].name")
department_one_employee_two = [match.value for match in get_department_one_employee_two.find(data)]
print("Department one employee two:", department_one_employee_two)

get_department_one_employee_three = parse("$.company.departments[0].employees[2].name")
department_one_employee_three = [match.value for match in get_department_one_employee_three.find(data)]
print("Department one employee three:", department_one_employee_three)

get_department_two_name = parse("$.company.departments[1].name")
department_two_name = [match.value for match in get_department_two_name.find(data)]
print("Department one name:", department_two_name)

get_department_two_employee_names = parse("$.company.departments[1].employees[*].name")
department_two_employee_names = [match.value for match in get_department_two_employee_names.find(data)]
print("Department two employee names:", department_two_employee_names)

get_department_two_employee_one_name = parse("$.company.departments[1].employees[0].name")
department_two_employee_one_name = [match.value for match in get_department_two_employee_one_name.find(data)]
print("Department two employee one name:", department_two_employee_one_name)

get_department_two_employee_one_role = parse("$.company.departments[1].employees[0].role")
department_two_employee_one_role = [match.value for match in get_department_two_employee_one_role.find(data)]
print("Department two employee one role:", department_two_employee_one_role)

get_department_two_employee_one_salary = parse("$.company.departments[1].employees[0].salary")
department_two_employee_one_salary = [match.value for match in get_department_two_employee_one_salary.find(data)]
print("Department two employee one salary:", department_two_employee_one_salary)

get_department_two_employee_two_name = parse("$.company.departments[1].employees[1].name")
department_two_employee_two_name = [match.value for match in get_department_two_employee_two_name.find(data)]
print("Department two employee two name:", department_two_employee_two_name)

get_department_two_employee_two_role = parse("$.company.departments[1].employees[1].role")
department_two_employee_two_role = [match.value for match in get_department_two_employee_two_role.find(data)]
print("Department two employee two role:", department_two_employee_two_role)

get_department_two_employee_two_salary = parse("$.company.departments[1].employees[1].salary")
department_two_employee_two_salary = [match.value for match in get_department_two_employee_two_salary.find(data)]
print("Department two employee two salary:", department_two_employee_two_salary)