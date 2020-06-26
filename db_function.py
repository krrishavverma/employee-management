import boto3
from boto3.dynamodb.conditions import Key
import json
from dynamodb_json import json_util

dynamodb_resource = boto3.resource('dynamodb', region_name='us-west-2')

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')


# give all the details from the table
def all_employees(self):
    employeesDetails = []

    try:
        response = dynamodb_client.scan(TableName='rishav-employees-data')

        try:
            employees = response['Items']
            for employee in employees:
                employee = json_util.loads(employee)

                employeesDetails.append(employee)
            return (employeesDetails)
        except KeyError:
            return ("No employee find")
        except Exception as e:
            return (e)
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        return ("Caught exception : {} while getting data from employee_details table".format(e.response.get("Error", None).get("Message", None))), 400
    except Exception as e:
        return e


# give individual detail
def single_employee(self, id):
    try:
        response = dynamodb_client.get_item(
            Key={
                'id': {
                    'S': id,
                }
            },
            TableName='rishav-employees-data',
        )

        try:
            employeeDeatil = response['Item']
            employeeDeatil = json_util.loads(employeeDeatil)

            return employeeDeatil

        except KeyError:
            return({"message": "Employee  with id {} not exist".format(id)})
        except Exception as e:
            return e

    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        ("Caught exception : {} while getting data from table".format(
            e.response.get("Error", None).get("Message", None))), 400

    except Exception as e:
        return e


# add new employee detail to the table
def add_employee(self, data):

    try:
        id = data["id"]

        response = dynamodb_client.get_item(
            Key={
                'id': {
                    'S': id,
                }
            },
            TableName='rishav-employees-data',
        )

        try:
            db_data = response['Item']
            return ("Employee with id {} exist".format(id))

        except KeyError:
            table = dynamodb_resource.Table('rishav-employees-data')
            table.put_item(
                Item=data
            )
            return data
        except Exception as e:
            return e
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        return ("Caught exception : {} while adding employee to the table".format(e.response.get("Error", None).get("Message", None))), 400
    except Exception as e:
        return e


# modify the existing detail of particular employee
def edit_employee(self, data, id):

    try:
        response = dynamodb_client.get_item(
            Key={
                'id': {
                    'S': id,
                }
            },
            TableName='rishav-employees-data',
        )

        try:
            employee_data = response['Item']
            employee_data = json_util.loads(employee_data)

            if data['real_name'] is not None:
                employee_data['real_name'] = data['real_name']
            if data['tz'] is not None:
                employee_data['tz'] = data['tz']
            if data['activity_periods'] is not None:
                employee_data['activity_periods'] = data['activity_periods']

            table = dynamodb_resource.Table('rishav-employees-data')
            table.put_item(
                Item=employee_data
            )
            return employee_data

        except KeyError:
            return {"message": "Employee with id {} does not exist".format(id)}
        except Exception as e:
            return e
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        return ("Caught exception : {} while updating data to table".format(e.response.get("Error", None).get("Message", None))), 400
    except Exception as e:
        return e


# delete the employee from the table
def delete_employee(self, id):
    try:
        table = dynamodb_resource.Table('rishav-employees-data')
        table.delete_item(
            Key={
                'id': id
            }
        )

        return {"message": "Employee with id {} is deleted".format(id)}
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        ("Caught exception : {} while deleting data from table".format(
            e.response.get("Error", None).get("Message", None))), 400

    except Exception as e:
        return e, 400
