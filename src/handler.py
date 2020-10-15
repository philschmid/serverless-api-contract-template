import time


def handler(event, context):
    if 'body' in event:
        return  event['body']
    else:
        return {'message':'send body pls'}
