from behave import given, use_step_matcher


use_step_matcher('re')


@given('ExampleProject is running')
def start_proj(context):
    context.response = context.client.get(context.example_url)
    assert context.response.status == 200


@when('a request is made')
def example_request(context):
    context.response = context.client.get(context.example_url)
    assert context.response.status == 200


@then('a response is returned')
def example_response(context):
    assert context.response.status == 200
    assert context.response.data != {}
