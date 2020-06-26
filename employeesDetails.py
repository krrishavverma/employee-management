from flask_restful import Resource, reqparse
from flask import request
import json
from db_function import all_employees, delete_employee, add_employee, single_employee, edit_employee


# for all the employees
class allEmployeesInfo(Resource):

    def get(self):
        all_employee = all_employees(self)

        if all_employee:
            return all_employee
        else:
            return("No employee find")


class employeeInfo(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('real_name',
                        type=str,
                        required=False)
    parser.add_argument('tz',
                        type=str,
                        required=False)
    parser.add_argument('activity_periods',
                        type=str,
                        required=False)

    # individual employee details
    def get(self, id):
        employee_detail = single_employee(self, id)
        return employee_detail

    # add new employee
    def post(self, id):
        new_employee = employeeInfo.parser.parse_args()

        if new_employee['real_name'] is None or new_employee['tz'] is None or new_employee['activity_periods'] is None:
            return ('Please provide all the details of the employee')

        activity_periods = eval(new_employee['activity_periods'])

        new_employee_detail = {
            'id': id,
            'real_name': new_employee['real_name'],
            'tz': new_employee['tz'],
            'activity_periods': [{
                'start_time': activity_periods['start_time'],
                'end_time': activity_periods['end_time']
            }]
        }

        msg = add_employee(self, new_employee_detail)
        return msg

    # edit employee detail
    def put(self, id):
        new_employee = employeeInfo.parser.parse_args()
        msg = edit_employee(self, new_employee, id)
        return msg

    # delete employee detail
    def delete(self, id):
        msg = delete_employee(self, id)
        if msg is None:
            return ("Caught exception : Requested resource not found while deleting data table"), 400
        else:
            return msg
