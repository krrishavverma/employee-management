from flask import Flask, request
from flask_restful import Resource, Api
from employeesDetails import allEmployeesInfo, employeeInfo


application = app = Flask(__name__)
api = Api(app)

api.add_resource(allEmployeesInfo, '/employees')
api.add_resource(employeeInfo, '/employees/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)
